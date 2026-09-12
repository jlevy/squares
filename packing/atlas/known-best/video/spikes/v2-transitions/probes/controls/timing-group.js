// The step-animation group in each mode: the boxes around it, whether it is drawn, whether
// it is alone in its row, and whether it holds the timing and phasing controls.
// o.n is the size Pack is put on.
(o) => {
  const api = window.atlasTransitions;
  const box = document.getElementById("step-anim-box");
  const geo = () => {
    const r = (id) => {
      const b = document.getElementById(id).getBoundingClientRect();
      return [b.x, b.y, b.width, b.height];
    };
    const b = box.getBoundingClientRect();
    return {
      stage: r("stage"),
      controls: r("controls"),
      facts: r("facts"),
      svg: r("packing-svg"),
      shake: r("shake-box"),
      law: r("law-box"),
      box: [b.x, b.y, b.width, b.height],
      visibility: getComputedStyle(box).visibility,
      display: getComputedStyle(box).display,
      focusable: box.contains(document.activeElement),
      alone_in_row:
        Array.from(box.parentElement.children).filter((e) => e.classList.contains("subpanel"))
          .length === 1,
      holds: ["t-dwell", "t-move", "t-settle", "phase-seg", "fullbeat-toggle"].every((id) =>
        box.contains(document.getElementById(id)),
      ),
    };
  };
  api.setMode("animate");
  const animating = geo();
  api.setMode("pack");
  api.setStepN(o.n);
  const packing = geo();
  return { animating, packing };
};
