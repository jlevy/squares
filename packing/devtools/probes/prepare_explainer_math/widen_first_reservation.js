// The stable wrong-width control: widen the first measured box by 12px before fonts arrive.
() => {
  const box = /** @type {HTMLElement} */ (
    /** @type {HTMLElement[]} */ (globalThis.__squaresGeometryBoxes)[0]
  );
  box.style.width = `${box.getBoundingClientRect().width + 12}px`;
};
