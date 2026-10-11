// Move the page and table frames to their extremes, or reset both, for a reusable
// before/after column-geometry measurement. No production controls or data are changed.
/** @param {{ position: "bottom" | "right" | "reset" }} o */
async ({ position }) => {
  const frames = new Set();
  for (const table of document.querySelectorAll("table.site-table")) {
    for (let frame = table.parentElement; frame; frame = frame.parentElement) {
      if (getComputedStyle(frame).overflowX !== "visible") {
        frames.add(frame);
        break;
      }
    }
  }
  if (position === "bottom") {
    window.scrollTo(0, document.documentElement.scrollHeight);
  } else if (position === "right") {
    for (const frame of frames) {
      frame.scrollLeft = frame.scrollWidth;
    }
  } else {
    window.scrollTo(0, 0);
    for (const frame of frames) {
      frame.scrollLeft = 0;
    }
  }
  await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
};
