// A head script: the required math-font failure control. Every math face reports unready to
// `document.fonts.check` and rejects `document.fonts.load`, each rejection counted in
// `__squaresRejectedFonts`; every other face is untouched.
() => {
  const fonts = Object.getPrototypeOf(document.fonts);
  const check = fonts.check,
    load = fonts.load;
  /** @param {string} spec */
  const required = (spec) => /KPress Math Text|KaTeX_/.test(spec);
  globalThis.__squaresRejectedFonts = 0;
  /**
   * @this {FontFaceSet}
   * @param {string} spec
   * @param {string} [text]
   */
  fonts.check = function (spec, text) {
    return required(spec) ? false : check.call(this, spec, text);
  };
  /**
   * @this {FontFaceSet}
   * @param {string} spec
   * @param {string} [text]
   */
  fonts.load = function (spec, text) {
    if (!required(spec)) {
      return load.call(this, spec, text);
    }
    /** @type {number} */ (__squaresRejectedFonts)++;
    return Promise.reject(new Error("required math-font failure control"));
  };
};
