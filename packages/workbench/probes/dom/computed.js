// One computed style property of the element with this id. o.property names it.
/** @param {{id: string, property: keyof CSSStyleDeclaration}} o */
(o) => {
  const element = document.getElementById(o.id);
  if (element == null) {
    throw new Error(`probe requires #${o.id}`);
  }
  return getComputedStyle(element)[o.property];
};
