// The page's images, forced and decoded: `loading="lazy"` is excluded from the `load` event,
// and nothing else in the settlement chain waits on an image. A decode rejection is accepted
// only when the image's current request is already complete with nonzero intrinsic
// dimensions; every other rejection, and a resolved decode that still leaves no drawable
// image, refuses the export with the source and state. `render_explainer_pdf` says why.
async () => {
  const images = [...document.images];
  for (const image of images) {
    image.loading = "eager";
  }
  const failures = (
    await Promise.all(
      images.map(async (image, index) => {
        /** @type {string | null} */
        let rejection = null;
        try {
          await image.decode();
        } catch (error) {
          rejection = error instanceof Error ? error.message : String(error);
        }
        if (image.complete && image.naturalWidth > 0 && image.naturalHeight > 0) {
          return null;
        }
        const source = image.currentSrc || image.src || `image ${index + 1}`;
        const reason =
          rejection === null
            ? "decode resolved without a drawable current request"
            : `decode rejected: ${rejection}`;
        return (
          `${source}: complete=${image.complete}, ` +
          `natural=${image.naturalWidth}x${image.naturalHeight}, ${reason}`
        );
      }),
    )
  ).filter((failure) => failure !== null);
  if (failures.length > 0) {
    const noun = failures.length === 1 ? "image is" : "images are";
    throw new Error(
      `${failures.length} required ${noun} not drawable after decode: ${failures.join("; ")}`,
    );
  }
};
