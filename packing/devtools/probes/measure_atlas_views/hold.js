// Hold every move at one point of its course, so a screenshot shows it there: `fraction`
// 0 is where everything was, 1 where it is going. Each move the script started, of a
// tile or of what follows the tiles (the sections after the block), is paused and set to
// that share of its own duration; a hover wash, a CSS transition, is not a move. Returns
// how many moves were held.
(/** @type {{fraction: number}} */ { fraction }) => {
  const moves = document
    .getAnimations()
    .filter(
      (animation) =>
        !(animation instanceof CSSTransition) &&
        !(animation instanceof CSSAnimation) &&
        animation.effect instanceof KeyframeEffect,
    );
  for (const move of moves) {
    const length = Number(move.effect?.getComputedTiming().endTime ?? 0);
    move.pause();
    move.currentTime = length * fraction;
  }
  return moves.length;
};
