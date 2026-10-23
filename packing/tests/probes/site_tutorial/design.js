// Actual tutorial figures, image containment, and inherited paper caption roles.
async () => {
  await document.fonts.ready;
  const root = document.querySelector(".site-page");
  if (!root) {
    throw new Error("Tutorial has no prose column");
  }
  for (const image of root.querySelectorAll("figure img")) {
    if (image instanceof HTMLImageElement) {
      image.loading = "eager";
      await image.decode();
    }
  }
  const base = Number.parseFloat(getComputedStyle(root).fontSize);
  const section = root.querySelector("h2");
  const paragraph = root.querySelector("p");
  return {
    measure: root.getBoundingClientRect().width,
    noteSize: base * (19 / 18) * 0.92,
    bodyFont: paragraph ? getComputedStyle(paragraph).fontFamily : null,
    sectionFont: section ? getComputedStyle(section).fontFamily : null,
    sectionStyle: section ? getComputedStyle(section).fontStyle : null,
    overflow: document.documentElement.scrollWidth > innerWidth,
    figures: [...root.querySelectorAll("figure")].map((figure) => {
      const image = figure.querySelector("img");
      const caption = figure.querySelector("figcaption");
      if (!image || !caption) {
        throw new Error("Figure is missing an image or caption");
      }
      const imageBox = image.getBoundingClientRect();
      const figureBox = figure.getBoundingClientRect();
      const style = getComputedStyle(caption.querySelector("p") ?? caption);
      return {
        loaded: image.complete && image.naturalWidth > 0,
        imageCentre: imageBox.left + imageBox.width / 2,
        figureCentre: figureBox.left + figureBox.width / 2,
        imageWidth: imageBox.width,
        figureWidth: figureBox.width,
        font: style.fontFamily,
        style: style.fontStyle,
        weight: style.fontWeight,
        size: Number.parseFloat(style.fontSize),
        leading: Number.parseFloat(style.lineHeight) / Number.parseFloat(style.fontSize),
      };
    }),
  };
};
