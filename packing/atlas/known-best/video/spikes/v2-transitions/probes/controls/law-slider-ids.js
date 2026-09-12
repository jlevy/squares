// The slider ids the page's own parameter table implies: one per law, per parameter.
() => {
  const api = window.atlasTransitions;
  const laws = api.lawNames ? api.lawNames() : [];
  const keys = api.lawParams ? api.lawParams() : [];
  const out = [];
  for (const name of laws) {
    for (const key of keys) {
      out.push(`${api.lawPrefix(name)}-${key}`);
    }
  }
  return out;
};
