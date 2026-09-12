// The side a blind run reaches at the default inflation, at 1.25, and at the default again,
// so the first and the third say whether it is reproducible. Takes {index}.
(o) => {
  const A = window.atlasTransitions;
  const a = A.physics(o.index, "bodies", "blind").miss.side;
  A.setBlindInflate(1.25);
  const b = A.physics(o.index, "bodies", "blind").miss.side;
  A.setBlindInflate(1.12);
  const c = A.physics(o.index, "bodies", "blind").miss.side;
  return [a, b, c];
};
