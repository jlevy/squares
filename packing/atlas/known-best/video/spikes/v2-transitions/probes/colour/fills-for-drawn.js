// The map driven by the angles the frame actually drew, which is the same question the
// painter asked, put to the pure function instead. o.angles is what was drawn.
(o) =>
  window.atlasTransitions.fillsFor(
    o.angles,
    o.angles.map(() => 0),
  );
