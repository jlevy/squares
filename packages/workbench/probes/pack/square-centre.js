// The viewport point at the centre of one drawn Pack square, for a real pointer to press.
// o.index is the square's zero-based index.
/** @param {{index: number}} o */
(o) => {
  const node = document.querySelector(`#pack-squares > g[data-pack-index="${o.index}"]`);
  if (node === null) {
    throw new Error(`probe requires Pack square ${o.index}`);
  }
  const box = node.getBoundingClientRect();
  return { x: box.left + box.width / 2, y: box.top + box.height / 2 };
};
