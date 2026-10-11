// Freeze the layout in the click task, then compare the next animation frame. The
// immediate record is the verdict; the animation-frame record only exposes a
// geometric CSS transition that the reduced-motion path must never start.
async (/** @type {{press: string}} */ { press }) => {
  const control = document.querySelector(press);
  const block = document.querySelector("[data-atlas-grid]");
  const cells = block?.querySelector(".site-atlas-cells");
  if (
    !(control instanceof HTMLElement) ||
    !(block instanceof HTMLElement) ||
    !(cells instanceof HTMLElement)
  ) {
    return null;
  }
  const read = () => {
    const origin = cells.getBoundingClientRect();
    const wrappers = [...cells.querySelectorAll(".site-atlas-row, .site-atlas-segment")].filter(
      (element) => element.getClientRects().length > 0,
    );
    const rows = wrappers.filter((element) => element.matches(".site-atlas-row"));
    const tiles = [...cells.querySelectorAll(".site-atlas-cell")].filter(
      (element) => element.getClientRects().length > 0,
    );
    const elements = [...wrappers, ...tiles];
    const transitions = document
      .getAnimations()
      .flatMap((animation) =>
        animation instanceof CSSTransition &&
        animation.effect instanceof KeyframeEffect &&
        animation.effect.target !== null &&
        wrappers.includes(animation.effect.target)
          ? [animation.transitionProperty]
          : [],
      );
    return {
      view: block.dataset.atlasView,
      line_gap: rows[1] ? Number.parseFloat(getComputedStyle(rows[1]).marginBlockStart) : 0,
      row_gap: Number.parseFloat(getComputedStyle(cells).rowGap),
      transitions,
      durations: [
        ...new Set(wrappers.map((element) => getComputedStyle(element).transitionDuration)),
      ],
      properties: [
        ...new Set(wrappers.map((element) => getComputedStyle(element).transitionProperty)),
      ],
      geometry: elements.map((element, index) => {
        const box = element.getBoundingClientRect();
        return {
          key: element.matches(".site-atlas-cell")
            ? `tile:${element.getAttribute("data-atlas-n")}`
            : `wrapper:${index}`,
          left: box.left - origin.left,
          top: box.top - origin.top,
          width: box.width,
          height: box.height,
        };
      }),
    };
  };
  control.click();
  const immediate = read();
  await new Promise((resolve) => requestAnimationFrame(resolve));
  return { immediate, next_frame: read() };
};
