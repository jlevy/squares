// The self-test's real-KaTeX baseline fixture: one caption appended to the page, holding each
// source rendered inline by the page's own `squaresMath`, each in a keyed slot the math
// preparation measures. Each formula's `.strut` styles as first drawn are kept in
// `baselineOriginalStruts`, for `restore_original_struts.js` to put back.
//
// Takes the TeX sources.
/** @param {string[]} sources */
async (sources) => {
  const caption = document.createElement("figcaption");
  caption.className = "kpress-figcaption";
  caption.dataset.baselineFixture = "true";
  /** @type {Element} */ (document.querySelector(".cert-page")).append(caption);
  globalThis.baselineOriginalStruts = [];
  for (const [index, source] of sources.entries()) {
    const target = document.createElement("span");
    target.className = "tex";
    target.dataset.squaresMathKey = String(index);
    caption.append("Reference ", target, " text.", document.createElement("br"));
    await /** @type {SquaresMathHost} */ (squaresMath).render(target, source, false);
    /** @type {(string | null)[][]} */ (baselineOriginalStruts).push(
      [...target.querySelectorAll(".base > .strut")].map((strut) => strut.getAttribute("style")),
    );
  }
};
