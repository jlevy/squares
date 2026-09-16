// The groups mask rides the correspondence overlay's own control: the box is ticked and
// unticked and the mask's own display read either way.
() => {
  const api = window.atlasTransitions;
  api.setRelationship("groups");
  const box = /** @type {HTMLInputElement} */ (document.getElementById("links-toggle"));
  const links = document.getElementById("mask-links");
  if (links == null) {
    throw new Error("probe requires #mask-links");
  }
  box.checked = true;
  box.dispatchEvent(new Event("change"));
  const on = links.style.display !== "none";
  box.checked = false;
  box.dispatchEvent(new Event("change"));
  const off = links.style.display === "none";
  api.setRelationship("contact");
  return { on, off, links: api.state().links };
};
