// The inline `display` style of the element with this id.
/** @param {{id: string}} o */
(o) => {
  const element = document.getElementById(o.id);
  if (element == null) {
    throw new Error(`probe requires #${o.id}`);
  }
  return element.style.display;
};
