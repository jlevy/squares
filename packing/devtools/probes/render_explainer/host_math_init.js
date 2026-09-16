// The explainer's host adapter for KPress's shared math runtime, installed as `squaresMath`:
// the page's own formula wrappers and TeX spacing, and nothing the runtime owns.
// `render_explainer.host_math_init` inlines it after the runtime, applied to `MATH_WRAPPERS`,
// the selector for every element that wraps a formula.
/** @param {string} wrappers */
(wrappers) => {
  /** @param {string | null | undefined} value */
  const firstFamily = (value) =>
    /** @type {string} */ ((value || "").split(",")[0]).trim().replace(/^["']|["']$/g, "");
  const context = {
    /** @param {Node} node */
    isSansContext(node) {
      /** @type {(Node & Partial<Pick<Element, "matches">>) | null} */
      let el = node;
      while (el?.matches?.(wrappers)) {
        el = el.parentElement;
      }
      if (el?.nodeType !== 1) {
        return false;
      }
      const style = getComputedStyle(/** @type {Element} */ (el));
      const sans = firstFamily(style.getPropertyValue("--kpress-font-sans"));
      return !!sans && firstFamily(style.fontFamily) === sans;
    },
  };
  // The same one-mu spacing the SVG labels use for an italic function name.
  /** @param {unknown} source */
  const kern = (source) => String(source).replace(/(?<![A-Za-z\\])([a-z])\(/g, "$1\\mkern1mu(");
  /** @type {Set<Promise<unknown>>} */
  const pending = new Set();
  /** @type {Set<Promise<unknown>>} */
  const submitting = new Set();
  /** @type {WeakMap<HTMLElement, number>} */
  const versions = new WeakMap();
  /**
   * @template T
   * @param {Promise<T>} result
   * @param {Set<Promise<unknown>>} [waiting]
   * @returns {Promise<T>}
   */
  function track(result, waiting = pending) {
    waiting.add(result);
    result.then(
      () => waiting.delete(result),
      () => waiting.delete(result),
    );
    return result;
  }
  // Reserve work before its producer runs, including later certificate scripts.
  function reserve() {
    /** @type {(() => void) | undefined} */
    let release;
    /** @type {Promise<void>} */
    const result = new Promise((resolve) => {
      release = resolve;
    });
    void track(result);
    void track(result, submitting);
    return /** @type {() => void} */ (release);
  }
  /** @returns {Promise<void>} */
  function nextTask() {
    return new Promise((resolve) => {
      const channel = new MessageChannel();
      channel.port1.onmessage = () => {
        channel.port1.close();
        channel.port2.close();
        resolve();
      };
      channel.port2.postMessage(null);
    });
  }
  /** @param {ReadonlyArray<() => unknown>} jobs */
  function batch(jobs) {
    const finishSubmission = reserve();
    // Register the whole queue before its first job runs. A task boundary lets
    // completed formulas reveal while later formulas are still being submitted.
    return track(
      Promise.resolve().then(async () => {
        /** @type {unknown[]} */
        const issued = [];
        try {
          for (let start = 0; start < jobs.length; start += 16) {
            if (start) {
              await nextTask();
            }
            for (const job of jobs.slice(start, start + 16)) {
              issued.push(job());
            }
          }
        } finally {
          finishSubmission();
        }
        await Promise.all(issued);
      }),
    );
  }
  /**
   * @param {HTMLElement} el
   * @param {string} source
   * @param {boolean} [display]
   */
  function render(el, source, display) {
    const version = (versions.get(el) || 0) + 1;
    versions.set(el, version);
    const root = document.documentElement.dataset;
    const preference =
      (root.kpressFontSet === "system" ? "system" : "custom") +
      "-" +
      (root.kpressProseFont === "sans" ? "sans" : "serif");
    const variants = /** @type {HTMLElement[]} */ ([
      ...el.querySelectorAll(":scope > .squares-math-variant"),
    ]);
    const target =
      variants.find((node) =>
        /** @type {string} */ (node.dataset.squaresMathContexts).split(" ").includes(preference),
      ) || el;
    const renderMath =
      target.dataset.kpressMathPrepared === "true"
        ? /** @type {KpressMathText} */ (kpressMathText).hydrate
        : /** @type {KpressMathText} */ (kpressMathText).render;
    const result = renderMath(
      kern(source),
      target,
      { displayMode: !!display, throwOnError: false },
      context,
    ).then(
      () => {
        if (versions.get(el) !== version) {
          return true;
        }
        target.dataset.squaresMathReady = "true";
        el.dataset.squaresMathReady = "true";
        return true;
      },
      () => {
        if (versions.get(el) !== version) {
          return true;
        }
        el.textContent = source;
        el.dataset.squaresMathReady = "true";
        return false;
      },
    );
    return track(result);
  }
  /** @param {Set<Promise<unknown>>} waiting */
  async function drain(waiting) {
    while (waiting.size) {
      await Promise.all([...waiting]);
    }
  }
  const submitted = () => drain(submitting);
  const settled = () => drain(pending);
  globalThis.squaresMath = { render, reserve, batch, submitted, settled, context };
};
