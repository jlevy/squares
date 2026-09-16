// True once no connected measured box is hidden.
() =>
  /** @type {HTMLElement[]} */ (__squaresGeometryBoxes)
    .filter((box) => box.isConnected)
    .every((box) => getComputedStyle(box).visibility !== "hidden");
