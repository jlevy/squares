// Every one of these angles at every contact count, flattened: the whole map as one table,
// so two stages can be compared. o.angles is the list of angles.
(o) => {
  const out = [];
  for (const a of o.angles) {
    for (let k = 0; k <= 4; k++) {
      out.push(window.atlasTransitions.fillsFor([a], [k])[0]);
    }
  }
  return out;
};
