// The boxes the two modes must lay out identically, and whether the position bar is gone.
() => {
  /** @param {string} id */
  const r = (id) => {
    const element = document.getElementById(id);
    if (element == null) {
      throw new Error(`probe requires #${id}`);
    }
    const b = element.getBoundingClientRect();
    return [b.x, b.y, b.width, b.height];
  };
  return {
    stage: r("stage"),
    facts: r("facts"),
    svg: r("packing-svg"),
    progress: document.getElementById("progress") === null,
  };
};
