// Put the focus on the selected size tab without scrolling the page, as a reader tabbing
// through the controls does, so the next Tab reaches the tiles; whether there was one.
() => {
  const tab = document.querySelector(
    '[data-atlas-grid] [data-atlas-size-tab][aria-selected="true"]',
  );
  if (!(tab instanceof HTMLElement)) {
    return false;
  }
  tab.focus({ preventScroll: true });
  return true;
};
