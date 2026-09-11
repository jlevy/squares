// Which solvers each mode offers, what is selected, and what the fallback note says, walked
// through Animate, Pack, a choice made in Pack, the tween asked for in Pack, and back.
// o.n is the size Pack is put on.
(o) => {
  const api = window.atlasTransitions;
  const shown = () =>
    Array.from(document.getElementById("style-select").options)
      .filter((opt) => !opt.hidden && !opt.disabled)
      .map((opt) => opt.value);
  const note = () => document.getElementById("solver-note").textContent;
  api.setMode("animate");
  api.setStyle("tween");
  const animating = {
    shown: shown(),
    solvers: api.solvers(),
    style: api.state().style,
    note: note(),
  };
  api.setMode("pack");
  api.setStepN(o.n);
  const packing = {
    shown: shown(),
    solvers: api.solvers(),
    style: api.state().style,
    note: note(),
  };
  api.setStyle("bodies");
  const chosen = { style: api.state().style, note: note() };
  api.setStyle("tween");
  const asked = { style: api.state().style, note: note() };
  api.setMode("animate");
  const back = { shown: shown(), style: api.state().style, note: note() };
  api.setMode("pack");
  api.setStepN(o.n);
  api.setStyle("bodies");
  return { animating, packing, chosen, asked, back };
};
