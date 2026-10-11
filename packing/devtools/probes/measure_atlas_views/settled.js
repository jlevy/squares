// Whether the atlas has tiles placed and neither the tiles nor their container is in a move.
() =>
  document.querySelector(".site-atlas-cells .site-atlas-cell") !== null &&
  document
    .getAnimations()
    .every(
      (animation) =>
        animation instanceof CSSTransition ||
        !(animation.effect instanceof KeyframeEffect) ||
        animation.effect.target?.matches(".site-atlas-cell, .site-atlas-cells") !== true ||
        animation.playState === "finished",
    );
