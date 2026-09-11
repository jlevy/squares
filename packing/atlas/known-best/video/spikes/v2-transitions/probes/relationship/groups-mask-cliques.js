// The groups mask counted three ways: what the relationship reports, what `blockOf` implies
// clique by clique, and what `blocks()` implies over members and riders together.
() => {
  const api = window.atlasTransitions;
  const of = api.blockOf();
  const c = new Map();
  for (const k of of) if (k >= 0) c.set(k, (c.get(k) || 0) + 1);
  let byOf = 0;
  for (const k of c.values()) byOf += k * (k - 1) / 2;
  let byBlocks = 0;
  for (const b of api.blocks()) {
    const k = b.members.length + b.riders.length;
    byBlocks += k * (k - 1) / 2;
  }
  return {maskEdges: api.relationship().maskEdges, byOf, byBlocks, blocks: api.blocks().length};
}
