// The contact-bias box on a law that already pulls, where the graph is all it should touch.
() => {
  const api = window.atlasTransitions;
  const box = /** @type {HTMLInputElement} */ (document.getElementById("bias-toggle"));
  box.checked = true;
  box.dispatchEvent(new Event("change"));
  const on = { kind: api.relationship().kind, attraction: api.law().attraction };
  box.checked = false;
  box.dispatchEvent(new Event("change"));
  return { on, kind: api.relationship().kind };
};
