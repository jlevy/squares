// An init script: save the reading preference for prose font before the page's own init
// reads it.
/** @param {{ proseFont: string }} o */
({ proseFont }) => {
  localStorage.setItem("kpress.proseFont", proseFont);
};
