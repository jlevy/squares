// One annealing level's free run, then another level's, then the first level's again, as the
// first square's final pose each time: a level must reproduce itself rather than hand back
// whatever was built last. The dial is put back on the level it was found at, so nothing here
// names a default. o.index is the pair, o.levels the two levels.
/** @param {{index: number, levels: [number, number]}} o */
(o) => {
  const api = window.atlasTransitions;
  const found = api.anneal().level;
  api.setAnneal(o.levels[0]);
  const first = api.physics(o.index, "bodies", "free").final[0];
  api.setAnneal(o.levels[1]);
  const other = api.physics(o.index, "bodies", "free").final[0];
  api.setAnneal(o.levels[0]);
  const again = api.physics(o.index, "bodies", "free").final[0];
  api.setAnneal(found);
  return { first, other, again, level: api.anneal().level };
};
