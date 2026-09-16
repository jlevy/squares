// A fixture beside the page's first certificate, and a reset that fills it with a fresh copy
// of a printed `.tex` or native `.kpress-math` formula, so each fault starts from real
// prepared nodes under the page's own CSS.
() => {
  /** @param {string} selector */
  const printed = (selector) =>
    /** @type {Element} */ (
      [...document.querySelectorAll(selector)].find(
        (node) => node.getClientRects().length && node.querySelector(".katex-html"),
      )
    );
  const fixture = document.createElement("div");
  fixture.id = "pdf-math-guard-control";
  /** @type {Element} */ (document.querySelector(".cert-page")).appendChild(fixture);
  globalThis.pdfMathGuardNodes = {
    tex: printed(".tex").cloneNode(true),
    native: printed(".kpress-math").cloneNode(true),
  };
  globalThis.resetPdfMathGuardNode = (kind) => {
    fixture.replaceChildren(
      /** @type {NonNullable<typeof globalThis.pdfMathGuardNodes>} */ (
        globalThis.pdfMathGuardNodes
      )[kind].cloneNode(true),
    );
    return /** @type {HTMLElement} */ (fixture.firstElementChild);
  };
};
