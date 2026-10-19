// Load retained thumbnail assets before saving the media-card screenshot.
async () => {
  const images = [...document.querySelectorAll(".site-homepage-media img")];
  await Promise.all(
    images.map(async (image) => {
      if (!(image instanceof HTMLImageElement)) {
        throw new Error("A homepage media image is not an image");
      }
      image.loading = "eager";
      await image.decode();
    }),
  );
  for (const image of images) {
    image.scrollIntoView({ block: "center" });
    await new Promise((resolve) => requestAnimationFrame(() => resolve(undefined)));
  }
  return window.scrollY;
};
