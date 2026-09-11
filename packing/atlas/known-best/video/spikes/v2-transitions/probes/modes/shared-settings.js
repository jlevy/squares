// The settings that are shared between the modes, read after a switch in both directions.
() => {
  const api = window.atlasTransitions;
  api.setMode("pack");
  api.setMode("animate");
  const s = api.state();
  return {
    style: s.style,
    anneal: s.anneal,
    speed: s.speed,
    initial: s.initial,
    desaturate: s.desaturate,
    range: api.range(),
  };
};
