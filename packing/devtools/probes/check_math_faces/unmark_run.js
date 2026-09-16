// Remove the id `mark_latin_run` gave, if the marked run is still there.
/** @param {string} mark */
(mark) => {
  const el = document.getElementById(mark);
  if (el) {
    el.removeAttribute("id");
  }
};
