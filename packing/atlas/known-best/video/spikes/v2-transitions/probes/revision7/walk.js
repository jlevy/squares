// Where the sequence stands at the start, the middle and the end of the first pair,
// the middle one and the last: nine readings in the order they are walked.
() => {
  const A = window.atlasTransitions;
  const out = [];
  const pairs = A.pairs();
  for (const i of [0, Math.floor(pairs.length / 2), pairs.length - 1]) {
    A.select(i);
    for (const u of [0, 0.5, 1]) { A.seek(A.duration() * u); out.push(A.progress().position); }
  }
  return out;
}
