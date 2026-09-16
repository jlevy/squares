// Stamp `data-shot` on the first laid-out paragraph of the document that contains `start`,
// and say whether there was one.
/** @param {{ key: string, start: string }} o */
({ key, start }) => {
  const found = [...document.querySelectorAll(".cert-page p")].find(
    (p) =>
      p.getBoundingClientRect().width > 0 && /** @type {string} */ (p.textContent).includes(start),
  );
  if (!found) {
    return false;
  }
  found.setAttribute("data-shot", key);
  return true;
};
