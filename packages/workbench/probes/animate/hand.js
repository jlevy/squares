// The hand: which square is held, and whether a drag is under way on the document.
() => ({
  held: window.atlasTransitions.hand().held,
  dragging: document.body.classList.contains("dragging"),
});
