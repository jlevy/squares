// What has the focus, two frames after it moved: the case of the tile it is on, if any,
// whether any part of that element is drawn where the window shows the stage, whether it
// matches `:focus-visible`, and the block's following.
async () => {
  await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  const block = document.querySelector("[data-atlas-grid]");
  const cells = block?.querySelector(".site-atlas-cells");
  const focused = document.activeElement;
  if (
    !(block instanceof HTMLElement) ||
    !(cells instanceof HTMLElement) ||
    !(focused instanceof HTMLElement)
  ) {
    return null;
  }
  const stage = cells.getBoundingClientRect();
  const drawn = focused.getBoundingClientRect();
  const left = Math.max(stage.left, 0);
  const right = Math.min(stage.right, window.innerWidth);
  const top = Math.max(stage.top, 0);
  const bottom = Math.min(stage.bottom, window.innerHeight);
  return {
    n: cells.contains(focused) ? (focused.dataset.atlasN ?? null) : null,
    seen: drawn.right > left && drawn.left < right && drawn.bottom > top && drawn.top < bottom,
    visible: focused.matches(":focus-visible"),
    follow: block.dataset.atlasFollow ?? null,
  };
};
