// The contact-bias box turned on and off, with the law and the graph read either side of
// each press. The box is read back from the page as well as from the state, because
// `setLaw` runs `updateSegments`, which writes the box from the relationship.
() => {
  const api = window.atlasTransitions;
  const box = document.getElementById("bias-toggle");
  const before = api.law().attraction;
  box.checked = true;
  box.dispatchEvent(new Event("change"));
  const on = {
    kind: api.relationship().kind,
    attraction: api.law().attraction,
    range: api.law().range,
    checked: document.getElementById("bias-toggle").checked,
  };
  box.checked = false;
  box.dispatchEvent(new Event("change"));
  const off = {
    kind: api.relationship().kind,
    attraction: api.law().attraction,
    checked: document.getElementById("bias-toggle").checked,
  };
  return { before, on, off };
};
