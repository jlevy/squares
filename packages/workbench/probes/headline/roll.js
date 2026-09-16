// The headline through one step, at each instant o.at (seconds): for the still slot and both
// rolling slots, the opacity each is seen at (its own times every ancestor's up to the stage),
// whether its `n =` and its digits are drawn, the digits' text, and where `=` and the digits
// sit on the page. o.n is the step's n.
/** @param {{n: number, at: number[]}} o */
(o) => {
  const api = window.atlasTransitions;
  api.pause();
  api.setStepN(o.n);
  const stage = /** @type {HTMLElement} */ (document.getElementById("stage"));
  const read = (/** @type {string} */ id) => {
    const slot = /** @type {HTMLElement} */ (document.getElementById(id));
    let seen = 1;
    for (let e = /** @type {Element | null} */ (slot); e && e !== stage; e = e.parentElement) {
      seen *= Number(getComputedStyle(e).opacity);
    }
    const equals = slot.querySelector(".katex-html .mrel");
    const digits = slot.querySelector(".katex-html .mord.mathbf");
    const box = (/** @type {Element | null} */ e) => {
      const r = e?.getBoundingClientRect();
      return r ? [r.left, r.top] : null;
    };
    const shown = (/** @type {Element | null} */ e) =>
      e !== null && getComputedStyle(e).visibility === "visible";
    return {
      seen,
      equalsShown: shown(equals),
      digitsShown: shown(digits),
      digits: digits?.textContent ?? null,
      equalsAt: box(equals),
      digitsAt: box(digits),
    };
  };
  return o.at.map((t) => {
    api.seek(t);
    return {
      t,
      still: read("numeral-static"),
      leaving: read("numeral-a"),
      arriving: read("numeral-b"),
    };
  });
};
