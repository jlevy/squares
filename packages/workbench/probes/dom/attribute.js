// One attribute of the element with this id. o.id is the id, o.name the attribute.
/** @param {{id: string, name: string}} o */
(o) => {
  const element = document.getElementById(o.id);
  if (element == null) {
    throw new Error(`probe requires #${o.id}`);
  }
  return element.getAttribute(o.name);
};
