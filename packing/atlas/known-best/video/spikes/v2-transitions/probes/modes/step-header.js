// The step header in each mode, with the stage's own box beside it: the tag is absolutely
// positioned, so hiding it must move nothing. o.n is the size Pack is put on.
(o) => {
  const api = window.atlasTransitions;
  const e = document.getElementById("kind-tag");
  const box = () => document.getElementById("stage").getBoundingClientRect().toJSON();
  api.setMode("pack");
  api.setStepN(o.n);
  const packed = { hidden: e.getClientRects().length === 0, stage: box() };
  api.setMode("animate");
  const swept = { hidden: e.getClientRects().length === 0, stage: box(), text: e.textContent };
  api.setMode("pack");
  api.setStepN(o.n);
  return { packed, swept };
};
