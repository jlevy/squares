// Over a grid of laws, every setting at which the force at a penetration is not a push, or
// at which touching is not zero. o.laws is the grid; the shipped law is put back after.
(o) => {
  const api = window.atlasTransitions;
  const bad = [];
  const ds = [-0.6, -0.42, -0.4, -0.3, -0.2, -0.15, -0.08, -0.02, -0.002, -1e-9];
  for (const law of o.laws) {
    api.setLaw(law);
    const key = api.law().key;
    if (api.lawForce(0) !== 0) bad.push([key, 0, api.lawForce(0), 'not zero at touching']);
    for (const d of ds) {
      const f = api.lawForce(d);
      if (!(f > 0)) bad.push([key, d, f, 'not repulsive at a penetration']);
    }
  }
  api.setLawPreset('default');
  return bad;
}
