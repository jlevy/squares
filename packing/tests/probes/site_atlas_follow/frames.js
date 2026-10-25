// Let `count` frames pass, as a reader who has stopped scrolling waits.
async (/** @type {{count: number}} */ { count }) => {
  for (let frame = 0; frame < count; frame += 1) {
    await new Promise((resolve) => requestAnimationFrame(resolve));
  }
  return count;
};
