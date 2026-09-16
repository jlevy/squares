// A head script: the pre-paint attributes a fresh browser sets from saved reading
// preferences. A page loaded by `set_content` has no persistent origin to save them in, so
// they are assigned in the head, before the normal bootstrap and body, and are not changed
// after math renders.
/** @param {{ proseFont: string, fontSet: string }} o */
({ proseFont, fontSet }) => {
  document.documentElement.dataset.kpressProseFont = proseFont;
  document.documentElement.dataset.kpressFontSet = fontSet;
};
