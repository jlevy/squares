// How the stylesheet unveils the triangle's stage: its animation's delay and length in
// milliseconds, and the stage's opacity at the animation's start and once it has run.
// Seeking the animation leaves it finished.
() => {
  const cells = document.querySelector("[data-atlas-grid] .site-atlas-cells");
  if (!(cells instanceof HTMLElement)) {
    return null;
  }
  const unveil = cells
    .getAnimations()
    .find(
      (animation) =>
        animation instanceof CSSAnimation && animation.animationName === "site-atlas-unveil",
    );
  if (unveil === undefined) {
    return { delay: null, length: null, start: null, end: null };
  }
  const timing = unveil.effect?.getTiming();
  const delay = Number(timing?.delay ?? 0);
  const length = Number(timing?.duration ?? 0);
  unveil.currentTime = 0;
  const start = Number.parseFloat(getComputedStyle(cells).opacity);
  unveil.finish();
  const end = Number.parseFloat(getComputedStyle(cells).opacity);
  return { delay, length, start, end };
};
