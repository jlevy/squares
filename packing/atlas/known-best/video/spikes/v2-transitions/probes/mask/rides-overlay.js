// The groups mask rides the correspondence overlay's own control: the box is ticked and
// unticked and the mask's own display read either way.
() => {
  const api = window.atlasTransitions;
  api.setRelationship('groups');
  const box = document.getElementById('links-toggle');
  box.checked = true;
  box.dispatchEvent(new Event('change'));
  const on = document.getElementById('mask-links').style.display !== 'none';
  box.checked = false;
  box.dispatchEvent(new Event('change'));
  const off = document.getElementById('mask-links').style.display === 'none';
  api.setRelationship('contact');
  return {on, off, links: api.state().links};
}
