// The boxes of the bar's own pieces, in the stage's own units: the track, the shaded open
// span, the two bold bound rules, the two numerals, and how many reference marks the scale
// carries for this n.
() => {
  const stage = document.getElementById("stage");
  if (stage == null) {
    throw new Error("probe requires #stage");
  }
  const s = stage.getBoundingClientRect();
  const k = s.width / 1920;
  /** @param {string} selector */
  const box = (selector) => {
    const element = document.querySelector(selector);
    if (element == null) {
      throw new Error(`probe requires ${selector}`);
    }
    const b = element.getBoundingClientRect();
    return {
      l: (b.left - s.left) / k,
      r: (b.right - s.left) / k,
      t: (b.top - s.top) / k,
      b: (b.bottom - s.top) / k,
    };
  };
  return {
    track: box(".gapbar-plot .track"),
    open: box("#gapbar-open"),
    rec: box("#gapbar-record-rule"),
    low: box("#gapbar-lower-rule"),
    lowLabel: box("#gapbar-lower-label"),
    recLabel: box("#gapbar-record-label"),
    refTicks: document.querySelectorAll("#gapbar-ticks line").length,
    refNums: [...document.querySelectorAll("#gapbar-ticks text")].map((t) => t.textContent),
  };
};
