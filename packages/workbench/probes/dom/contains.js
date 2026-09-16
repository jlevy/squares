// Which of these ids are not inside the element with id o.parent: missing from the page, or
// placed somewhere else. An empty answer means the parent holds them all. o.ids is the list.
/** @param {{parent: string, ids: string[]}} o */
(o) => {
  const parent = document.getElementById(o.parent);
  if (parent == null) {
    throw new Error(`probe requires #${o.parent}`);
  }
  return o.ids.filter((id) => {
    const element = document.getElementById(id);
    return element == null || !parent.contains(element);
  });
};
