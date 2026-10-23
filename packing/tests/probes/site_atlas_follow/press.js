// Press the control `selector` names where it stands, without scrolling it into view, as
// a key press on a focused tab does; whether there was one.
(/** @type {{selector: string}} */ { selector }) => {
  const control = document.querySelector(selector);
  if (!(control instanceof HTMLElement)) {
    return false;
  }
  control.click();
  return true;
};
