// Figure 2 under Letter print media, measured at the physical six-inch text width.
() => {
  const image = /** @type {HTMLImageElement | null} */ (
    document.querySelector('img[src$="known-best-1-100.svg"]')
  );
  const figure = image?.closest("figure");
  const caption = figure?.querySelector("figcaption");
  if (!image || !figure || !caption) {
    throw new Error("the complete atlas figure and caption must be present");
  }
  const imageBox = image.getBoundingClientRect();
  const figureBox = figure.getBoundingClientRect();
  const captionBox = caption.getBoundingClientRect();
  const figureStyle = getComputedStyle(figure);
  const imageStyle = getComputedStyle(image);
  return {
    image_loaded: image.complete && image.naturalWidth > 0,
    image_visible: image.checkVisibility({ visibilityProperty: true }),
    natural_width: image.naturalWidth,
    natural_height: image.naturalHeight,
    image_width: imageBox.width,
    image_height: imageBox.height,
    figure_height: figureBox.height,
    figure_outer_height:
      figureBox.height + parseFloat(figureStyle.marginTop) + parseFloat(figureStyle.marginBottom),
    caption_visible: caption.checkVisibility({ visibilityProperty: true }),
    caption_height: captionBox.height,
    caption_below_image: captionBox.top >= imageBox.bottom,
    caption_inside_figure: captionBox.bottom <= figureBox.bottom,
    object_fit: imageStyle.objectFit,
    image_overflow: imageStyle.overflow,
    figure_overflow: figureStyle.overflow,
    link: image.closest("a")?.getAttribute("href"),
  };
};
