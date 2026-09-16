// The law sampled the way the plot draws it: how many samples, whether they rise, how many
// disagree with `lawForce`, and where the curve ends. o.preset is the law, o.samples the ask.
/** @param {{preset: string, samples: number}} o */
(o) => {
  const api = window.atlasTransitions;
  api.setLawPreset(o.preset);
  const c = api.lawCurve(o.samples);
  const first = c[0];
  const last = c.at(-1);
  if (first === undefined || last === undefined) {
    throw new Error("law curve returned no samples");
  }
  return {
    n: c.length,
    rising: c.every((r, i) => i === 0 || r[0] > (c[i - 1]?.[0] ?? r[0])),
    off: c.filter((r) => r[1] !== api.lawForce(r[0])).length,
    ends: [first[0], last[0]],
  };
};
