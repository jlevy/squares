// What the solver select offers in the view on show, without switching views: the options that
// are neither hidden nor disabled, the solvers the API says this view offers, every style the page
// knows, the style in force and the fallback note beside the select.
() => {
  const api = window.atlasTransitions;
  const select = /** @type {HTMLSelectElement | null} */ (document.getElementById("style-select"));
  const note = document.getElementById("solver-note");
  if (select == null || note == null) {
    throw new Error("probe requires #style-select and #solver-note");
  }
  return {
    shown: Array.from(select.options)
      .filter((option) => !option.hidden && !option.disabled)
      .map((option) => option.value),
    solvers: api.solvers(),
    styles: api.styles(),
    style: api.state().style,
    note: note.textContent,
  };
};
