// The snap box driven from the page: flipped, and put back where it was.
() => {
  const api = window.atlasTransitions;
  const box = document.getElementById("snap-toggle");
  const was = api.state().snap;
  box.checked = !was;
  box.dispatchEvent(new Event("change"));
  const flipped = api.state().snap;
  box.checked = was;
  box.dispatchEvent(new Event("change"));
  return {
    was,
    flipped,
    back: api.state().snap,
    shown: document.getElementById("snap-toggle").checked,
  };
};
