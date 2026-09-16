// Installed before parsing: breaks the math font of exactly one printed formula. The error is
// a real invalid FontFace response. The timeout holds the matching FontFaceSet request beyond
// KPress's own deadline, rather than replacing its render promise with a synthetic rejection.
// Only one printed formula is affected: the first laid-out `.tex` caption formula with TeX in
// it (`wrapper: "tex"`), or the first laid-out native `.kpress-math` (`wrapper: "native"`).
/** @param {{ wrapper: "tex" | "native", mode: "error" | "timeout" | null }} o */
({ wrapper, mode }) => {
  const family = "PDF Math Fault Control";
  /** @type {HTMLElement | undefined} */
  let selected;
  document.fonts.add(new FontFace(family, "url(data:font/woff2;base64,AA==)"));
  if (mode === "timeout") {
    const fontSet = Object.getPrototypeOf(document.fonts),
      load = fontSet.load;
    /**
     * @param {string} spec
     * @param {string} [text]
     */
    fontSet.load = function (spec, text) {
      if (spec.includes(family)) {
        return new Promise(() => {});
      }
      return load.call(this, spec, text);
    };
  }
  Object.defineProperty(globalThis, "kpressMathText", {
    configurable: true,
    /** @param {Record<string, (...args: any[]) => unknown>} api */
    set(api) {
      for (const key of ["render", "hydrate"]) {
        const original = /** @type {(...args: unknown[]) => unknown} */ (api[key]);
        /**
         * @this {unknown}
         * @param {string} source
         * @param {Element} node
         * @param {unknown[]} args
         */
        api[key] = function (source, node, ...args) {
          const owner = /** @type {HTMLElement | null} */ (
            node.closest(wrapper === "tex" ? ".tex" : ".kpress-math")
          );
          const wanted =
            wrapper === "native" || (owner?.closest("figcaption") && source.includes("\\"));
          if (owner?.getClientRects().length && wanted && !selected) {
            selected = owner;
            selected.dataset.pdfMathFault = wrapper;
            globalThis.pdfMathFaultSource = source;
            const style = document.createElement("style");
            style.textContent =
              "[data-pdf-math-fault] .katex-html * " +
              '{ font-family: "PDF Math Fault Control" !important; }';
            document.head.appendChild(style);
          }
          return original.call(this, source, node, ...args);
        };
      }
      // Drop this trap, then store the wrapped API as a plain value.
      Reflect.deleteProperty(globalThis, "kpressMathText");
      globalThis.kpressMathText = /** @type {KpressMathText} */ (/** @type {unknown} */ (api));
    },
  });
};
