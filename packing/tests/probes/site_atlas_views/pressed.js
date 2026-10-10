// Press a control of the atlas and say, before the browser has drawn anything, what the
// press started: the view and the size the block is then in, how many tiles are in a move
// and how many
// of the elements after them, the moves' duration and easing, and the properties they
// animate. `press` is the control's selector. Read in the same task as the press, so a
// move cannot have finished between the two. A move is an animation the script started;
// the wash a tab or a tile takes is a CSS transition and is not counted.
(/** @type {{press: string}} */ { press }) => {
  const control = document.querySelector(press);
  const block = document.querySelector("[data-atlas-grid]");
  if (!(control instanceof HTMLElement) || !(block instanceof HTMLElement)) {
    return null;
  }
  const scrollBefore = window.scrollY;
  control.click();
  const moves = document
    .getAnimations()
    .flatMap((animation) =>
      !(animation instanceof CSSTransition) &&
      animation.effect instanceof KeyframeEffect &&
      animation.effect.target !== null
        ? [animation.effect]
        : [],
    );
  const tiles = moves.filter((effect) => effect.target?.matches(".site-atlas-cell") === true);
  const timing = tiles[0]?.getComputedTiming();
  const tileMoves = tiles.map((effect) => {
    const motionTiming = effect.getComputedTiming();
    return {
      n: Number(effect.target?.getAttribute("data-atlas-n")),
      duration: Number(motionTiming.duration),
      easing: motionTiming.easing,
      properties: [
        ...new Set(
          effect
            .getKeyframes()
            .flatMap((frame) =>
              Object.keys(frame).filter(
                (name) => !["offset", "computedOffset", "easing", "composite"].includes(name),
              ),
            ),
        ),
      ].sort(),
    };
  });
  return {
    scroll_before: scrollBefore,
    scroll_after: window.scrollY,
    view: block.dataset.atlasView ?? null,
    size: block.dataset.atlasSize ?? null,
    moving: tiles.length,
    followers: moves.length - tiles.length,
    duration: timing ? Number(timing.duration) : null,
    easing: timing?.easing ?? null,
    properties: [...new Set(tileMoves.flatMap((motion) => motion.properties))].sort(),
    tile_moves: tileMoves,
  };
};
