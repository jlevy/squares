// A real height-only animation, even when its one tile is outside the viewport.
(/** @type {{hold: boolean, finish?: boolean}} */ { hold, finish = false }) => {
  const cells = document.querySelector(".site-atlas-cells");
  const control = document.querySelector("button");
  if (!(cells instanceof HTMLElement) || !(control instanceof HTMLElement)) {
    throw new Error("container animation fixture is missing");
  }
  if (finish) {
    for (const animation of cells.getAnimations()) {
      animation.finish();
    }
    return;
  }
  control.onclick = () => {
    const before = cells.getBoundingClientRect().height;
    cells.style.height = `${before + 40}px`;
    cells.dataset.finished = "false";
    const animation = cells.animate([{ height: `${before}px` }, { height: cells.style.height }], {
      duration: 120,
    });
    if (hold) {
      animation.pause();
    }
    void animation.finished.then(() => {
      cells.dataset.finished = "true";
    });
  };
};
