// Whether every drawing in the atlas's tiles has loaded and decoded, so a picture of the
// tiles shows each packing rather than its reserved, empty box.
() => {
  const images = [...document.querySelectorAll(".site-atlas-cells img")];
  return (
    images.length > 0 &&
    images.every(
      (image) => image instanceof HTMLImageElement && image.complete && image.naturalWidth > 0,
    )
  );
};
