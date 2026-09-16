// Installed before parsing, with the measurement mode: `full` observes the whole page, and
// `parameters` only the fourteen Figure 6 parameter targets. Wrappers observe the original
// calls and return their original promises, preserving resolution order and rejection
// behavior. No waits, styles, input events, or rendering mutations are introduced by the
// instrument. `finish()` on the installed `__mathStartup` stops it and returns the report.
//
// An init script takes no argument, so `exposed` and `activeVariant` come from
// `__squaresMathProbes`, which `math/library.js` installs when an earlier init script applies
// it with `{install: true}`.
/** @param {{ mode: string }} o */
({ mode }) => {
  const library = globalThis.__squaresMathProbes;
  if (!library) {
    throw new Error("check_math_startup/startup needs math/library installed before it");
  }
  const full = mode === "full";
  const clock = () => performance.now();
  /** @type {SquaresMathStartupState} */
  const state = {
    mode,
    metrics: { instrumentation_installed_ms: clock() },
    counters: {
      frames: 0,
      font_hooks: 0,
      katex_hooks: 0,
      runtime_hooks: 0,
      katex_calls: 0,
      ready_calls: 0,
      render_calls: 0,
      hydrate_calls: 0,
      hydrate_hooks: 0,
      anchor_samples: 0,
    },
    capabilities: { longtask: false, layout_shift: false },
    fonts: [],
    ready: [],
    renders: [],
    hydrates: [],
    katex: [],
    longtasks: [],
    shifts: [],
    targets: [],
    anchors: [],
    snapshots: [],
    errors: [],
    stop: false,
    pre_reveal_frame_observed: false,
    pending_observed: false,
  };
  globalThis.__mathStartup = state;
  const metrics = state.metrics;
  /**
   * @param {string} name
   * @param {number} [value]
   */
  const first = (name, value = clock()) => {
    if (metrics[name] == null) {
      metrics[name] = value;
    }
  };
  /**
   * @param {unknown} promise
   * @param {SquaresMathStartupCall} record
   */
  const observed = (promise, record) => {
    const thenable = /** @type {PromiseLike<unknown> | null | undefined} */ (promise);
    // Returning this exact promise matters: observation must not become a font gate.
    if (thenable && typeof thenable.then === "function") {
      thenable.then(
        () => {
          record.end_ms = clock();
          record.outcome = "resolved";
        },
        (error) => {
          record.end_ms = clock();
          record.outcome = "rejected";
          record.error = String(error);
        },
      );
    }
    return promise;
  };
  /** @type {(() => void)[]} */
  const originals = [];
  /**
   * @param {any} owner
   * @param {string} key
   * @param {(original: (this: any, ...args: any[]) => any) => (this: any, ...args: any[]) => any} make
   */
  function wrap(owner, key, make) {
    const original = owner?.[key];
    if (typeof original !== "function") {
      return false;
    }
    owner[key] = make(original);
    originals.push(() => {
      owner[key] = original;
    });
    return true;
  }
  const fontOwners = [
    globalThis.FontFace?.prototype,
    document.fonts && Object.getPrototypeOf(document.fonts),
  ];
  for (const [index, owner] of fontOwners.entries()) {
    if (
      wrap(
        owner,
        "load",
        (original) =>
          /** @param {unknown[]} args */
          function (...args) {
            if (state.stop) {
              return original.apply(this, args);
            }
            /** @type {SquaresMathStartupCall} */
            const record = {
              kind: index === 0 ? "face" : "set",
              start_ms: clock(),
              request:
                index === 0 ? `${this.family} ${this.style} ${this.weight}` : String(args[0]),
              outcome: "pending",
            };
            state.fonts.push(record);
            try {
              return observed(original.apply(this, args), record);
            } catch (error) {
              record.end_ms = clock();
              record.outcome = "threw";
              throw error;
            }
          },
      )
    ) {
      state.counters.font_hooks++;
    }
  }
  if (document.fonts) {
    document.fonts.addEventListener("loading", () => first("font_loading_event_ms"));
    document.fonts.addEventListener("loadingdone", () => {
      metrics.font_loading_done_ms = clock();
    });
  }
  /** @type {WeakMap<object, SquaresMathStartupCall>} */
  const sources = new WeakMap();
  /**
   * @param {string} name
   * @param {(api: any) => void} install
   */
  function globalObject(name, install) {
    let value = Reflect.get(globalThis, name);
    const installed = new WeakSet();
    /** @param {any} object */
    const accept = (object) => {
      if (object && !installed.has(object)) {
        installed.add(object);
        install(object);
      }
    };
    Object.defineProperty(globalThis, name, {
      configurable: true,
      enumerable: true,
      get: () => value,
      set: (object) => {
        value = object;
        accept(object);
      },
    });
    accept(value);
  }
  globalObject("katex", (api) => {
    first("katex_available_ms");
    if (
      wrap(
        api,
        "render",
        (original) =>
          /** @param {any[]} args */
          function (...args) {
            if (state.stop) {
              return original.apply(this, args);
            }
            /** @type {SquaresMathStartupCall} */
            const record = {
              start_ms: clock(),
              source: String(args[0]),
              target: args[1]?.id || null,
            };
            state.counters.katex_calls++;
            try {
              return original.apply(this, args);
            } finally {
              record.duration_ms = clock() - record.start_ms;
              state.katex.push(record);
            }
          },
      )
    ) {
      state.counters.katex_hooks++;
    }
  });
  globalObject("kpressMathText", (api) => {
    first("runtime_available_ms");
    if (
      wrap(
        api,
        "ready",
        (original) =>
          /** @param {unknown[]} args */
          function (...args) {
            first("first_ready_call_ms");
            state.counters.ready_calls++;
            /** @type {SquaresMathStartupCall} */
            const record = { start_ms: clock(), outcome: "pending" };
            state.ready.push(record);
            return observed(original.apply(this, args), record);
          },
      )
    ) {
      state.counters.runtime_hooks++;
    }
    if (
      wrap(
        api,
        "hydrate",
        (original) =>
          /** @param {any[]} args */
          function (...args) {
            state.counters.hydrate_calls++;
            const [source, node] = args;
            /** @type {SquaresMathStartupCall} */
            const record = {
              start_ms: clock(),
              source: String(source),
              target: node?.id || null,
              outcome: "pending",
            };
            if (node) {
              sources.set(node, record);
            }
            state.hydrates.push(record);
            return observed(original.apply(this, args), record);
          },
      )
    ) {
      state.counters.hydrate_hooks++;
    }
    if (
      wrap(
        api,
        "render",
        (original) =>
          /** @param {any[]} args */
          function (...args) {
            state.counters.render_calls++;
            const [source, node] = args;
            /** @type {SquaresMathStartupCall} */
            const record = {
              start_ms: clock(),
              source: String(source),
              target: node?.id || null,
              outcome: "pending",
            };
            if (node) {
              sources.set(node, record);
            }
            state.renders.push(record);
            return observed(original.apply(this, args), record);
          },
      )
    ) {
      state.counters.runtime_hooks++;
    }
  });
  /** @type {PerformanceObserver[]} */
  const observers = [];
  /** @type {(() => void)[]} */
  const drainObservers = [];
  for (const [type, capability, records] of /** @type {const} */ ([
    ["longtask", "longtask", state.longtasks],
    ["layout-shift", "layout_shift", state.shifts],
  ])) {
    if (!globalThis.PerformanceObserver?.supportedEntryTypes?.includes(type)) {
      continue;
    }
    state.capabilities[capability] = true;
    /** @param {any[]} entries */
    const receive = (entries) => {
      for (const entry of entries) {
        records.push(
          type === "longtask"
            ? { start_ms: entry.startTime, duration_ms: entry.duration }
            : {
                start_ms: entry.startTime,
                value: entry.value,
                had_recent_input: entry.hadRecentInput,
                sources: (entry.sources || []).map(
                  /** @param {any} source */
                  (source) => ({
                    node: source.node?.id || source.node?.tagName || null,
                    previous: source.previousRect.toJSON(),
                    current: source.currentRect.toJSON(),
                  }),
                ),
              },
        );
      }
    };
    const observer = new PerformanceObserver((list) => {
      if (!state.stop) {
        receive(list.getEntries());
      }
    });
    observer.observe({ type, buffered: true });
    observers.push(observer);
    drainObservers.push(() => receive(observer.takeRecords()));
  }
  document.addEventListener("DOMContentLoaded", () => first("dom_content_loaded_observed_ms"));
  window.addEventListener("load", () => first("load_observed_ms"));
  const pending = () => {
    const root = document.documentElement;
    if (!root) {
      return;
    }
    if (root.hasAttribute("data-kpress-math-pending")) {
      state.pending_observed = true;
      first("pending_set_ms");
    } else if (state.pending_observed) {
      first("pending_cleared_ms");
    }
    if (root.classList.contains("math-ready")) {
      first("math_ready_marker_ms");
    }
  };
  let dirty = true;
  const mutations = new MutationObserver(() => {
    dirty = true;
    pending();
  });
  mutations.observe(document, {
    subtree: true,
    childList: true,
    attributes: true,
    attributeFilter: ["data-kpress-math-pending", "class", "hidden"],
  });
  const { exposed, activeVariant } = library;
  const mathWrapper =
    ".katex,.kpress-math,.kpress-math-render," +
    ".kpress-math-semantic,.tex,.tex-d,.squares-math-variant";
  /** @param {string | null | undefined} text */
  const normalized = (text) => (text || "").replace(/\s+/g, "").replace(/\\mkern1mu/g, "");
  /** @param {Element} node */
  const annotation = (node) =>
    [...node.querySelectorAll('annotation[encoding="application/x-tex"]')]
      .filter(activeVariant)
      .map((part) => /** @type {string} */ (part.textContent).trim());
  /** @param {Element} node */
  const visibleMath = (node) => {
    const maths = [...node.querySelectorAll(".katex")].filter(activeVariant);
    return (
      maths.length > 0 &&
      ![...node.querySelectorAll(".katex-error")].some(activeVariant) &&
      maths.every((math) => {
        // The publication's pending rule necessarily hides these targets. Avoid
        // forcing prepared-page layout merely to measure an invisible formula.
        // Eligible targets still undergo the same actual exposure checks below.
        if (!full && document.documentElement.hasAttribute("data-kpress-math-pending")) {
          const target = /** @type {HTMLElement | null} */ (
            math.closest('.tex,.tex-d,[data-kpress-math-prepared="true"]')
          );
          if (target && target.dataset.squaresMathReady !== "true") {
            return false;
          }
        }
        const html = math.querySelector(".katex-html");
        return (
          html &&
          /** @type {string} */ (html.textContent).trim() &&
          exposed(html) &&
          annotation(math).every(Boolean) &&
          annotation(math).length > 0
        );
      })
    );
  };
  /** @param {Element} node */
  const active = (node) => !node.closest(".cert-figure[hidden]") && exposed(node);
  /** @param {Element} node */
  const slugOf = (node) =>
    /** @type {HTMLElement | null} */ (node.closest(".cert-figure"))?.dataset.cert || null;
  /** @returns {SquaresMathStartupSnapshot} */
  const snapshot = () => {
    const viewport = document.querySelector("[data-kpress-viewport]") || document.scrollingElement;
    return {
      at_ms: clock(),
      width: innerWidth,
      height: innerHeight,
      scroll_x: viewport?.scrollLeft || 0,
      scroll_y: viewport?.scrollTop || 0,
      document_scroll_x: scrollX,
      document_scroll_y: scrollY,
      visibility: document.visibilityState,
      focused: document.hasFocus(),
      hash: location.hash,
      document_ready_state: document.readyState,
      math_ready: document.documentElement.classList.contains("math-ready"),
      certificate_elements: document.querySelectorAll(".cert-figure").length,
      active_certificates: [
        ...new Set(
          [.../** @type {NodeListOf<HTMLElement>} */ (document.querySelectorAll(".cert-figure"))]
            .filter((node) => (full ? active(node) : !node.closest("[hidden]")))
            .map((node) => node.dataset.cert),
        ),
      ],
    };
  };
  /** @type {Element[]} */
  let prose = [];
  /** @type {Element[]} */
  let captions = [];
  /** @type {Element[]} */
  let parameters = [];
  /** @type {WeakMap<Element, number>} */
  const targetTimes = new WeakMap();
  /** @type {WeakMap<Node, SquaresMathStartupAnchor[]>} */
  const anchorNodes = new WeakMap();
  /** @type {{ node: Text, block: Element, range: Range, record: SquaresMathStartupAnchor }[]} */
  const tracked = [];
  /** @type {WeakMap<Element, { last: ChildNode | null, count: number }>} */
  const blockEdges = new WeakMap();
  const expectedLabels = [
    "\\varphi",
    "K",
    "\\varphi",
    "\\theta",
    "d",
    "D",
    "B",
    "B(\\cos d + \\sin d)",
  ];
  /**
   * @param {Element} node
   * @param {number} index
   */
  function correctTarget(node, index) {
    if (!visibleMath(node)) {
      return false;
    }
    const texts = annotation(node);
    if (index < 8 && normalized(texts.join("")) !== normalized(expectedLabels[index])) {
      return false;
    }
    if (node.id.startsWith("s-phi-")) {
      const slider = /** @type {HTMLInputElement | null} */ (
        document.getElementById(node.id.slice(2))
      );
      if (
        !slider ||
        normalized(texts[0]) !== normalized(`${(Number(slider.value) / 10).toFixed(3)}^{\\circ}`)
      ) {
        return false;
      }
    }
    const containers = [node, ...node.querySelectorAll(mathWrapper)].filter(activeVariant);
    return containers.every((container) => {
      const request = sources.get(container);
      return (
        !request ||
        annotation(container).some((text) => normalized(text) === normalized(request.source))
      );
    });
  }
  function discoverAnchors() {
    const blocks = document.querySelectorAll(
      '.kpress-prose p, .kpress-figcaption, figcaption, figure[data-figure="6"] .caps, ' +
        'figure[data-figure="6"] dt',
    );
    for (const block of blocks) {
      const previous = blockEdges.get(block);
      if (
        previous &&
        previous.last === block.lastChild &&
        previous.count === block.childNodes.length
      ) {
        continue;
      }
      if (!block.querySelector(mathWrapper) || !active(block)) {
        continue;
      }
      blockEdges.set(block, { last: block.lastChild, count: block.childNodes.length });
      const category = block.closest(".kpress-figcaption,figcaption")
        ? "caption"
        : block.closest('figure[data-figure="6"]')
          ? "parameter"
          : "prose";
      const walker = document.createTreeWalker(
        block,
        NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT,
        {
          acceptNode(node) {
            // Reject whole math subtrees. Prepared markup must not cost the observer
            // a walk through thousands of glyph spans that the control lacks.
            if (node.nodeType === Node.ELEMENT_NODE) {
              return /** @type {Element} */ (node).matches(mathWrapper)
                ? NodeFilter.FILTER_REJECT
                : NodeFilter.FILTER_SKIP;
            }
            return /** @type {string} */ (node.textContent).trim()
              ? NodeFilter.FILTER_ACCEPT
              : NodeFilter.FILTER_REJECT;
          },
        },
      );
      /** @type {Text[]} */
      const texts = [];
      while (walker.nextNode()) {
        const node = /** @type {Text} */ (walker.currentNode);
        texts.push(node);
      }
      // At most four persistent characters per block. The outside edges detect
      // rewrapping without walking every KaTeX glyph on every frame.
      for (const text of new Set(
        /** @type {Text[]} */ ([texts[0], texts.at(-1)].filter(Boolean)),
      )) {
        if (anchorNodes.has(text)) {
          continue;
        }
        const value = /** @type {string} */ (text.textContent);
        const offsets = new Set([value.search(/\S/), value.search(/\s*$/) - 1]);
        /** @type {SquaresMathStartupAnchor[]} */
        const anchors = [];
        for (const offset of offsets) {
          if (offset < 0) {
            continue;
          }
          const range = document.createRange();
          range.setStart(text, offset);
          range.setEnd(text, offset + 1);
          /** @type {SquaresMathStartupAnchor} */
          const record = {
            id: `anchor-${tracked.length}`,
            category,
            text: value.trim().replace(/\s+/g, " ").slice(0, 100),
            character: value[offset],
            offset,
            block: block.id || block.tagName.toLowerCase(),
            samples: 0,
            initial: null,
            final: null,
            max_absolute_px: 0,
            max_local_px: 0,
            max_start_x_px: 0,
            max_start_y_px: 0,
            max_bottom_px: 0,
          };
          tracked.push({ node: text, block, range, record });
          anchors.push(record);
          state.anchors.push(record);
        }
        anchorNodes.set(text, anchors);
      }
    }
  }
  function discover() {
    if (full) {
      prose = [...document.querySelectorAll(".kpress-prose p")].filter(
        (node) => !node.closest(".cert-figure,figcaption,.kpress-figcaption") && active(node),
      );
      captions = [...document.querySelectorAll(".kpress-figcaption,figcaption")].filter(active);
    }
    const figure = [...document.querySelectorAll('figure[data-figure="6"]')].find((node) =>
      full ? active(node) : !node.closest("[hidden]"),
    );
    // Keep labels before readouts so the eight published label contracts are stable.
    parameters = figure
      ? [
          ...figure.querySelectorAll(".panel .ctl .caps, .panel .kv dt"),
          ...figure.querySelectorAll(".panel .kv dd"),
        ]
      : [];
    if (full) {
      discoverAnchors();
    }
    dirty = false;
  }
  /** @param {number} at */
  function sampleAnchors(at) {
    /** @type {Map<Element, DOMRect | null>} */
    const blocks = new Map();
    for (const { node, block, range, record } of tracked) {
      if (!node.isConnected) {
        continue;
      }
      if (!blocks.has(block)) {
        blocks.set(block, active(block) ? block.getBoundingClientRect() : null);
      }
      const box = blocks.get(block);
      if (!box) {
        continue;
      }
      if (
        !(
          /** @type {Element} */ (node.parentElement).checkVisibility({
            opacityProperty: true,
            visibilityProperty: true,
          })
        )
      ) {
        continue;
      }
      const rect = range.getBoundingClientRect();
      if (rect.width <= 0 || rect.height <= 1) {
        continue;
      }
      /** @type {SquaresMathStartupPosition} */
      const position = {
        at_ms: at,
        x: rect.x,
        y: rect.y,
        bottom: rect.bottom,
        local_x: rect.x - box.x,
        local_y: rect.y - box.y,
        local_bottom: rect.bottom - box.y,
      };
      record.initial ||= position;
      record.final = position;
      record.samples++;
      record.bounds ||= {};
      const bounds = record.bounds;
      for (const key of /** @type {const} */ ([
        "x",
        "y",
        "bottom",
        "local_x",
        "local_y",
        "local_bottom",
      ])) {
        bounds[key] ||= { min: position[key], max: position[key] };
        const extent = /** @type {{ min: number, max: number }} */ (bounds[key]);
        extent.min = Math.min(extent.min, position[key]);
        extent.max = Math.max(extent.max, position[key]);
      }
      /** @param {"x" | "y" | "bottom" | "local_x" | "local_y" | "local_bottom"} key */
      const span = (key) => {
        const extent = /** @type {{ min: number, max: number }} */ (bounds[key]);
        return extent.max - extent.min;
      };
      record.max_start_x_px = span("x");
      record.max_start_y_px = span("y");
      record.max_bottom_px = span("bottom");
      record.max_absolute_px = Math.max(
        record.max_absolute_px,
        record.max_start_x_px,
        record.max_start_y_px,
        record.max_bottom_px,
      );
      record.max_local_px = Math.max(span("local_x"), span("local_y"), span("local_bottom"));
      state.counters.anchor_samples++;
    }
  }
  function sample() {
    if (state.stop) {
      return;
    }
    const start = clock();
    state.counters.frames++;
    first("first_frame_ms", start);
    pending();
    if (dirty) {
      discover();
    }
    if (full) {
      sampleAnchors(start);
    }
    if (full && state.anchors.some((anchor) => anchor.samples)) {
      first("first_anchor_frame_ms", start);
      const current = snapshot(),
        previous = state.snapshots.at(-1);
      const changed =
        !previous ||
        /** @type {(keyof SquaresMathStartupSnapshot)[]} */ (Object.keys(current)).some(
          (key) =>
            key !== "at_ms" && JSON.stringify(current[key]) !== JSON.stringify(previous[key]),
        );
      if (changed) {
        state.snapshots.push(current);
      }
    }
    if (metrics.first_prose_math_ms == null && prose.some(visibleMath)) {
      first("first_prose_math_ms", start);
    }
    if (metrics.first_caption_math_ms == null && captions.some(visibleMath)) {
      first("first_caption_math_ms", start);
    }
    const ready = parameters.map((node, index) => {
      const correct = correctTarget(node, index);
      if (correct && !targetTimes.has(node)) {
        targetTimes.set(node, start);
      }
      return correct;
    });
    if (ready.some(Boolean)) {
      first("first_parameter_math_ms", start);
    }
    // Scroll offsets can flush layout too. In parameter mode take the first
    // state snapshot only after a target already required an exposure check.
    if (!full && ready.some(Boolean) && !state.snapshots.length) {
      state.snapshots.push(snapshot());
    }
    if (parameters.length === 14 && ready.every(Boolean)) {
      first("parameters_ready_ms", start);
    } else if (state.anchors.some((anchor) => anchor.samples)) {
      state.pre_reveal_frame_observed = true;
    }
    const duration = clock() - start;
    metrics.sampler_total_ms = (metrics.sampler_total_ms || 0) + duration;
    metrics.sampler_max_ms = Math.max(metrics.sampler_max_ms || 0, duration);
    if (full || metrics.parameters_ready_ms == null) {
      requestAnimationFrame(sample);
    }
  }
  requestAnimationFrame(sample);
  state.finish = () => {
    const validationStart = clock();
    drainObservers.forEach((drain) => {
      drain();
    });
    state.stop = true;
    pending();
    mutations.disconnect();
    observers.forEach((observer) => {
      observer.disconnect();
    });
    originals.forEach((restore) => {
      restore();
    });
    // Parameter-mode sampling stopped at first readiness. Re-read final coverage
    // so a later addition, removal, or reclassification cannot evade validation.
    discover();
    state.snapshots.push(snapshot());
    first("observation_end_ms");
    state.targets = parameters.map((node, index) => ({
      id: node.id || `figure6-${slugOf(node)}-label-${index}`,
      slug: slugOf(node),
      source: annotation(node),
      first_visible_ms: targetTimes.get(node) ?? null,
      correct: correctTarget(node, index),
      exposed: active(node),
      in_viewport:
        node.getBoundingClientRect().top < innerHeight && node.getBoundingClientRect().bottom > 0,
    }));
    const nav = /** @type {Record<string, number> | undefined} */ (
      /** @type {unknown} */ (performance.getEntriesByType("navigation")[0])
    );
    if (nav) {
      for (const [metric, key] of Object.entries({
        response_start_ms: "responseStart",
        response_end_ms: "responseEnd",
        dom_interactive_ms: "domInteractive",
        dom_content_loaded_ms: "domContentLoadedEventEnd",
        load_event_ms: "loadEventEnd",
      })) {
        metrics[metric] = nav[key] || null;
      }
    }
    const paints = performance.getEntriesByType("paint");
    for (const entry of paints) {
      metrics[`${entry.name.replaceAll("-", "_")}_ms`] = entry.startTime;
    }
    const firstReady = state.ready[0];
    metrics.initial_ready_end_ms = firstReady?.end_ms ?? null;
    metrics.initial_ready_wait_ms =
      firstReady?.end_ms != null ? firstReady.end_ms - firstReady.start_ms : null;
    metrics.last_font_end_ms =
      state.fonts.reduce((max, entry) => Math.max(max, entry.end_ms || 0), 0) || null;
    /** @param {SquaresMathStartupCall} entry */
    const duration = (entry) => /** @type {number} */ (entry.duration_ms);
    metrics.katex_total_ms = state.katex.reduce((sum, entry) => sum + duration(entry), 0);
    metrics.katex_max_ms = Math.max(0, ...state.katex.map(duration));
    metrics.first_katex_call_ms = state.katex[0]?.start_ms ?? null;
    metrics.last_katex_end_ms = state.katex.length
      ? Math.max(...state.katex.map((entry) => entry.start_ms + duration(entry)))
      : null;
    metrics.first_render_call_ms = state.renders[0]?.start_ms ?? null;
    metrics.last_render_end_ms = state.renders.length
      ? Math.max(...state.renders.map((entry) => entry.end_ms || 0)) || null
      : null;
    metrics.first_hydrate_call_ms = state.hydrates[0]?.start_ms ?? null;
    metrics.last_hydrate_end_ms = state.hydrates.length
      ? Math.max(...state.hydrates.map((entry) => entry.end_ms || 0)) || null
      : null;
    metrics.post_ready_to_first_katex_ms =
      metrics.first_katex_call_ms != null && metrics.initial_ready_end_ms != null
        ? metrics.first_katex_call_ms - metrics.initial_ready_end_ms
        : null;
    metrics.longtask_total_ms = state.capabilities.longtask
      ? /** @type {{ duration_ms: number }[]} */ (state.longtasks).reduce(
          (sum, entry) => sum + entry.duration_ms,
          0,
        )
      : null;
    metrics.layout_shift_score = state.capabilities.layout_shift
      ? /** @type {{ value: number, had_recent_input: boolean }[]} */ (state.shifts)
          .filter((entry) => !entry.had_recent_input)
          .reduce((sum, entry) => sum + entry.value, 0)
      : null;
    /** @param {SquaresMathStartupAnchorExtent} key */
    const anchorMax = (key) => Math.max(0, ...state.anchors.map((anchor) => anchor[key]));
    metrics.anchor_max_displacement_px = anchorMax("max_absolute_px");
    metrics.anchor_max_local_displacement_px = anchorMax("max_local_px");
    metrics.anchor_max_start_x_px = anchorMax("max_start_x_px");
    metrics.anchor_max_start_y_px = anchorMax("max_start_y_px");
    metrics.anchor_max_bottom_px = anchorMax("max_bottom_px");
    if (!full) {
      for (const name of [
        "anchor_max_displacement_px",
        "anchor_max_local_displacement_px",
        "anchor_max_start_x_px",
        "anchor_max_start_y_px",
        "anchor_max_bottom_px",
      ]) {
        metrics[name] = null;
      }
    }
    state.source = {
      url: location.href,
      title: document.title,
      revision_url:
        /** @type {HTMLAnchorElement | null} */ (
          document.querySelector('a[href*="github.com/jlevy/squares/blob/"]')
        )?.href || null,
    };
    metrics.finish_validation_ms = clock() - validationStart;
    return { ...state, finish: undefined };
  };
};
