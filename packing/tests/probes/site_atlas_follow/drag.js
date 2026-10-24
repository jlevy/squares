// A finger dragged `by` pixels sideways across the triangle's stage, in eight steps a
// frame apart, then lifted, as a phone's touch screen sends it. Two frames pass.
async (/** @type {{by: number}} */ { by }) => {
  const cells = document.querySelector("[data-atlas-grid] .site-atlas-cells");
  if (!(cells instanceof HTMLElement)) {
    return false;
  }
  const box = cells.getBoundingClientRect();
  const y = Math.min(Math.max(box.top, 0) + 100, window.innerHeight - 1);
  const from = box.left + box.width / 2;
  /** @param {string} type @param {number} x */
  const touch = (type, x) =>
    cells.dispatchEvent(
      new PointerEvent(type, {
        pointerType: "touch",
        pointerId: 7,
        isPrimary: true,
        clientX: x,
        clientY: y,
        bubbles: true,
      }),
    );
  const frame = () => new Promise((resolve) => requestAnimationFrame(resolve));
  touch("pointerdown", from);
  for (let step = 1; step <= 8; step += 1) {
    touch("pointermove", from + (by * step) / 8);
    await frame();
  }
  touch("pointerup", from + by);
  await frame();
  await frame();
  return true;
};
