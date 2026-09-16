// The explainer's shared math helpers, returned as one object. A probe that needs them is
// handed this object in its argument, through a handle from `page.evaluate_handle`; an init
// script, which takes no argument, reads the copy installed as `__squaresMathProbes` by an
// earlier init script that called this with `{install: true}`.
/**
 * @param {{ install?: boolean }} [options]
 * @returns {SquaresMathProbes}
 */
(options) => {
  // Variant selection follows the publication's root-attribute CSS without flushing
  // layout. A hidden certificate is still intended content; only another saved-font
  // profile is dormant. Malformed metadata must fail instead of silently losing math.
  /** @param {Element} node */
  const activeVariant = (node) => {
    const root = document.documentElement.dataset;
    const context =
      (root.kpressFontSet === "system" ? "system" : "custom") +
      "-" +
      (root.kpressProseFont === "sans" ? "sans" : "serif");
    let active = true;
    for (
      let variant = /** @type {HTMLElement | null | undefined} */ (
        node.closest(".squares-math-variant")
      );
      variant;
      variant = /** @type {HTMLElement | null | undefined} */ (
        variant.parentElement?.closest(".squares-math-variant")
      )
    ) {
      const contexts = (variant.dataset.squaresMathContexts || "").trim().split(/\s+/);
      if (contexts.some((value) => !/^(custom|system)-(serif|sans)$/.test(value))) {
        throw new Error("malformed saved-font math variant contexts");
      }
      if (!contexts.includes(context)) {
        active = false;
      }
    }
    return active;
  };

  // checkVisibility ignores clipping. Intersect the element's box with ancestor overflow,
  // legacy clip rectangles, and inset clip paths before calling semantic fallback visible.
  // Unrecognised clip shapes are not evidence of readable fallback.
  /** @param {Element} node */
  const exposed = (node) => {
    if (!node.checkVisibility({ opacityProperty: true, visibilityProperty: true })) {
      return false;
    }
    const rect = node.getBoundingClientRect();
    let { left, right, top, bottom } = rect;
    /** @param {{ left: number, right: number, top: number, bottom: number }} box */
    const intersect = (box) => {
      left = Math.max(left, box.left);
      right = Math.min(right, box.right);
      top = Math.max(top, box.top);
      bottom = Math.min(bottom, box.bottom);
    };
    for (let parent = /** @type {Element | null} */ (node); parent; parent = parent.parentElement) {
      const style = getComputedStyle(parent),
        box = parent.getBoundingClientRect();
      // The probe covers the document, including content a reader can scroll into view.
      // Project that content into its scroll viewport before checking outer clipping.
      if (/^(auto|scroll)$/.test(style.overflowX) && parent.scrollWidth > parent.clientWidth) {
        const width = right - left;
        left = box.left;
        right = Math.min(box.right, left + width);
      }
      if (/^(auto|scroll)$/.test(style.overflowY) && parent.scrollHeight > parent.clientHeight) {
        const height = bottom - top;
        top = box.top;
        bottom = Math.min(box.bottom, top + height);
      }
      if (/^(hidden|clip)$/.test(style.overflowX)) {
        left = Math.max(left, box.left);
        right = Math.min(right, box.right);
      }
      if (/^(hidden|clip)$/.test(style.overflowY)) {
        top = Math.max(top, box.top);
        bottom = Math.min(bottom, box.bottom);
      }
      const clip = (style.clip || "auto").match(/^rect\(([^)]+)\)$/);
      if (clip) {
        const defaults = [0, box.width, box.height, 0];
        const edges = /** @type {string} */ (clip[1])
          .trim()
          .split(/[,\s]+/)
          .map((value, i) => (value === "auto" ? defaults[i] : parseFloat(value)));
        if (edges.length !== 4 || !edges.every(Number.isFinite)) {
          return false;
        }
        const [edgeTop, edgeRight, edgeBottom, edgeLeft] =
          /** @type {[number, number, number, number]} */ (edges);
        intersect({
          left: box.left + edgeLeft,
          right: box.left + edgeRight,
          top: box.top + edgeTop,
          bottom: box.top + edgeBottom,
        });
      }
      const path = style.clipPath || "none";
      if (path !== "none") {
        const inset = path.match(/^inset\(([^)]+)\)$/);
        if (!inset) {
          return false;
        }
        const values = /** @type {string} */ (
          /** @type {string} */ (inset[1]).split(/\s+round\s+/)[0]
        )
          .trim()
          .split(/\s+/);
        if (values.length < 1 || values.length > 4) {
          return false;
        }
        const [first, second, third, fourth] = /** @type {[string, ...string[]]} */ (values);
        const insets = [first, second || first, third || first, fourth || second || first];
        const pixels = insets.map(
          (value, i) =>
            parseFloat(value) * (value.endsWith("%") ? (i % 2 ? box.width : box.height) / 100 : 1),
        );
        if (!pixels.every(Number.isFinite)) {
          return false;
        }
        const [insetTop, insetRight, insetBottom, insetLeft] =
          /** @type {[number, number, number, number]} */ (pixels);
        intersect({
          left: box.left + insetLeft,
          right: box.right - insetRight,
          top: box.top + insetTop,
          bottom: box.bottom - insetBottom,
        });
      }
      if (right - left <= 1 || bottom - top <= 1) {
        return false;
      }
    }
    return right - left > 1 && bottom - top > 1;
  };

  // Describe actual glyph runs, including hidden staging. Query each CSS family
  // separately: WebKit can report a family list ready while a later face is pending.
  // Native load matching, rather than a second CSS matching engine, handles weights,
  // unicode ranges, and families excluded from the glyph run.
  /**
   * @param {Element} math
   * @param {SquaresFontObserver} observe
   * @returns {SquaresFontRequirement[]}
   */
  const requiredFonts = (math, observe) => {
    const html = math.querySelector(".katex-html");
    if (!html) {
      return [];
    }
    const walker = document.createTreeWalker(html, NodeFilter.SHOW_TEXT);
    /** @type {Map<string, Set<string>>} */
    const groups = new Map();
    while (walker.nextNode()) {
      const node = walker.currentNode,
        text = /** @type {string} */ (node.textContent);
      if (!text.trim()) {
        continue;
      }
      const style = getComputedStyle(/** @type {Element} */ (node.parentElement));
      for (const family of families(style.fontFamily)) {
        const spec = `${style.fontStyle} ${style.fontWeight} ${style.fontSize} ${family}`;
        if (!groups.has(spec)) {
          groups.set(spec, new Set());
        }
        for (const character of text) {
          /** @type {Set<string>} */ (groups.get(spec)).add(character);
        }
      }
    }
    return [...groups].map(([spec, characters]) => {
      const text = [...characters].join("");
      try {
        return { spec, text, ...observe(spec, text) };
      } catch (error) {
        return {
          spec,
          text,
          ready: false,
          outcome: /** @type {const} */ ("rejected"),
          faces: [],
          error: String(error),
        };
      }
    });

    /** @param {string} list */
    function families(list) {
      const parts = [];
      let start = 0,
        quote = "",
        escaped = false;
      for (let index = 0; index < list.length; index++) {
        const character = list[index];
        if (escaped) {
          escaped = false;
        } else if (character === "\\") {
          escaped = true;
        } else if (quote) {
          if (character === quote) {
            quote = "";
          }
        } else if (character === '"' || character === "'") {
          quote = character;
        } else if (character === ",") {
          parts.push(list.slice(start, index).trim());
          start = index + 1;
        }
      }
      parts.push(list.slice(start).trim());
      return parts.filter(Boolean);
    }
  };

  // A readiness oracle separate from the renderer's cache. In WebKit, even a
  // single-family check() can return true while load() remains pending. Discovering
  // staged glyphs before rAF lets already-ready promises settle before first exposure;
  // a previously unseen visible closure must fail instead of passing vacuously.
  /**
   * @param {SquaresFontLoad} load
   * @returns {SquaresFontObserver}
   */
  const fontLoadObserver = (load) => {
    /** @type {Map<string, { outcome: SquaresFontObservation["outcome"], faces: FontFace[], error?: string }>} */
    const requests = new Map();
    return (spec, text) => {
      const key = JSON.stringify([spec, text]);
      if (!requests.has(key)) {
        /** @type {{ outcome: SquaresFontObservation["outcome"], faces: FontFace[], error?: string }} */
        const record = { outcome: "pending", faces: [] };
        requests.set(key, record);
        try {
          Promise.resolve(load(spec, text)).then(
            (faces) => {
              record.outcome = "resolved";
              record.faces = [...faces];
            },
            (error) => {
              record.outcome = "rejected";
              record.error = String(error);
            },
          );
        } catch (error) {
          record.outcome = "rejected";
          record.error = String(error);
        }
      }
      const record =
        /** @type {{ outcome: SquaresFontObservation["outcome"], faces: FontFace[], error?: string }} */ (
          requests.get(key)
        );
      const faces = record.faces.map((face) => ({
        family: face.family,
        style: face.style,
        weight: face.weight,
        unicodeRange: face.unicodeRange,
        status: face.status,
      }));
      return {
        outcome: record.outcome,
        faces,
        ...(record.error ? { error: record.error } : {}),
        ready: record.outcome === "resolved" && faces.every((face) => face.status === "loaded"),
      };
    };
  };

  // Batched hydration changes a few wrappers at a time. Rewalking the whole prepared
  // page after every batch can consume the bootstrap watchdog in the observer itself.
  // Ancestor changes still cover their descendants; stylesheet edits cover the page.
  /**
   * @param {readonly MutationRecord[]} [records]
   * @returns {Iterable<Element>}
   */
  const mutatedMath = (records) => {
    if (!records) {
      return document.querySelectorAll(".katex");
    }
    /** @type {Set<Element>} */
    const result = new Set();
    /** @param {Node | null | undefined} node */
    const element = (node) =>
      node?.nodeType === 1 ? /** @type {Element} */ (node) : node?.parentElement;
    /** @param {Node | null | undefined} node */
    const styles = (node) => {
      const el = element(node);
      return (
        el?.closest('style, link[rel="stylesheet"]') ||
        el?.querySelector?.('style, link[rel="stylesheet"]')
      );
    };
    /** @param {Node} node */
    const collect = (node) => {
      const el = element(node);
      if (!el) {
        return;
      }
      const math = el.closest(".katex");
      if (math) {
        result.add(math);
      } else {
        for (const child of el.querySelectorAll(".katex")) {
          result.add(child);
        }
      }
    };
    for (const record of records) {
      const changed = [...(record.addedNodes || []), ...(record.removedNodes || [])];
      if (styles(record.target) || changed.some(styles)) {
        return document.querySelectorAll(".katex");
      }
      if (record.type === "childList") {
        const math = element(record.target)?.closest(".katex");
        if (math) {
          result.add(math);
        }
        for (const node of record.addedNodes) {
          collect(node);
        }
      } else {
        collect(record.target);
      }
    }
    return result;
  };

  const library = { activeVariant, exposed, requiredFonts, fontLoadObserver, mutatedMath };
  if (options?.install) {
    globalThis.__squaresMathProbes = library;
  }
  return library;
};
