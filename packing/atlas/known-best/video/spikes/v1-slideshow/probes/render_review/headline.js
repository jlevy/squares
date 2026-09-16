// The boxes of the headline's marks, [left, top, right, bottom] in page pixels: the `n =` line,
// its `n` and its `=`, the headline and its numeral. `render_review.check_headline` looks for
// each mark's ink inside its box on the capture.
() => {
  const f = /** @type {Element} */ (document.querySelector("#facts"));
  /** @param {string} sel */
  const box = (sel) => {
    const b = /** @type {Element} */ (f.querySelector(sel)).getBoundingClientRect();
    return [b.left, b.top, b.right, b.bottom];
  };
  return {
    lead: box(".lead"),
    var: box(".lead .var"),
    eq: box(".lead .eq"),
    headline: box(".headline"),
    nval: box(".headline .nval"),
  };
};
