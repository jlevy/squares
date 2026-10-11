// Press one control of the atlas, wait `wait` milliseconds into the move it starts, and
// press another, as a reader who changes their mind does. Each control takes the focus
// as it is pressed, as a pointer's press gives it in Chromium. Reports how many tiles
// were in a move just before the second press and just after it, and the farthest the
// drawing of any tile then in the window jumped across that press, in CSS pixels: a
// second change starts from where the first had got to, so nothing a reader can see
// jumps. `first` and `second` are the controls' selectors.
async (/** @type {{first: string, second: string, wait: number}} */ { first, second, wait }) => {
  const one = document.querySelector(first);
  const two = document.querySelector(second);
  if (!(one instanceof HTMLElement) || !(two instanceof HTMLElement)) {
    return null;
  }
  const moving = () =>
    document
      .getAnimations()
      .filter(
        (animation) =>
          !(animation instanceof CSSTransition) &&
          animation.effect instanceof KeyframeEffect &&
          animation.effect.target?.matches(".site-atlas-cell") === true &&
          animation.playState === "running",
      ).length;
  const drawings = () =>
    [...document.querySelectorAll(".site-atlas-cells .site-atlas-cell :is(svg, img)")].map(
      (drawing) => drawing.getBoundingClientRect(),
    );
  one.focus();
  one.click();
  await new Promise((resolve) => setTimeout(resolve, wait));
  const before = { moving: moving(), drawings: drawings() };
  two.focus();
  two.click();
  const after = { moving: moving(), drawings: drawings() };
  let jump = 0;
  let watched = 0;
  for (const [index, was] of before.drawings.entries()) {
    const is = after.drawings[index];
    if (is !== undefined && was.width > 0 && was.bottom > 0 && was.top < window.innerHeight) {
      watched += 1;
      jump = Math.max(
        jump,
        Math.abs(is.left - was.left),
        Math.abs(is.top - was.top),
        Math.abs(is.width - was.width),
      );
    }
  }
  return {
    moving_before: before.moving,
    moving_after: after.moving,
    watched,
    jump: Math.round(jump * 100) / 100,
  };
};
