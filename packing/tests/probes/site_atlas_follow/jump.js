// Go to the fragment `hash` on the same page, as a link to a tile does, and let ten frames
// pass for the page to settle there; the fragment the address then names.
async (/** @type {{hash: string}} */ { hash }) => {
  location.hash = hash;
  for (let frame = 0; frame < 10; frame += 1) {
    await new Promise((resolve) => requestAnimationFrame(resolve));
  }
  return location.hash;
};
