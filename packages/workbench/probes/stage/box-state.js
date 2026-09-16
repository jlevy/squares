// The stage's box and trace and the gap bar's pointer as drawn now: the trace's and the box's
// sides, the trace's opacity, the box's stroke and whether it is the page's green, whether the
// pointer is locked, the pointer's and the record rule's x on the bar, and whether the box is
// drawn over its trace.
() => {
  /** @param {string} id */
  const element = (id) => {
    const found = document.querySelector(`#${id}`);
    if (found == null) {
      throw new Error(`probe requires #${id}`);
    }
    return found;
  };
  const trace = element("bound-trace");
  const box = element("bound-box");
  const pointer = /** @type {SVGGraphicsElement} */ (element("gapbar-box"));
  const met = getComputedStyle(document.documentElement).getPropertyValue("--met").trim();
  const matrix = pointer.transform.baseVal.consolidate()?.matrix ?? null;
  return {
    trace: Number(trace.getAttribute("width")),
    box: Number(box.getAttribute("width")),
    traceOpacity: Number(trace.getAttribute("opacity")),
    boxStroke: box.getAttribute("stroke"),
    green: box.getAttribute("stroke") === met,
    pointerLocked: pointer.classList.contains("is-locked"),
    pointerX: matrix === null ? null : matrix.e,
    recordX: Number(element("gapbar-record-rule").getAttribute("x1")),
    boxOverTrace: trace.nextElementSibling === box,
  };
};
