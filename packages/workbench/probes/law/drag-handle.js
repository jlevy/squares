// Drag one of the plot's handles, and read the four numbers and the four sliders back:
// a drag is the same setter the sliders write through, so neither can get ahead of the
// other. o.handle is 'knee' or 'pull', o.d the gap it is dragged to, o.f the force.
/** @param {{handle: "knee" | "pull", d: number, f: number}} o */
(o) => {
  const api = window.atlasTransitions;
  const l = api.dragLaw(o.handle, o.d, o.f);
  return {
    law: { rigidity: l.rigidity, repulsion: l.repulsion, attraction: l.attraction, range: l.range },
    sliders: ["rigidity", "repulsion", "attraction", "range"].map(
      (k) => /** @type {HTMLInputElement} */ (document.getElementById(`law-${k}`)).value,
    ),
    shown: (() => {
      const pull = document.getElementById("lp-pull");
      if (pull == null) {
        throw new Error("probe requires #lp-pull");
      }
      return pull.style.display !== "none";
    })(),
  };
};
