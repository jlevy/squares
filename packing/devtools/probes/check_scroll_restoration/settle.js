// Settlement before an observation: the page's math renders, its fonts, and two frames.
async () => {
  await globalThis.squaresMath?.settled?.();
  await document.fonts.ready;
  await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
};
