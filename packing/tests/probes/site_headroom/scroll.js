/** @param {number} top */
async (top) => {
  window.scrollTo({ top, behavior: "instant" });
  await new Promise((resolve) => requestAnimationFrame(resolve));
  await new Promise((resolve) => requestAnimationFrame(resolve));
};
