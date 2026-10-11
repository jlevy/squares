// HTML labels follow live themes; immutable upstream drawing pixels retain their palette.
/** @param {{scroll_top: boolean}} options */
async (options) => {
  if (options.scroll_top) {
    window.scrollTo({ top: 0, behavior: "instant" });
    await new Promise((resolve) => requestAnimationFrame(() => resolve(undefined)));
    await new Promise((resolve) => requestAnimationFrame(() => resolve(undefined)));
  }
  const cells = document.getElementById("homepage-atlas-cells");
  const image = cells?.querySelector('.site-atlas-cell[data-atlas-n="11"] img');
  const label = cells?.querySelector(".site-atlas-n");
  if (!(image instanceof HTMLImageElement) || !label || !cells) {
    throw new Error("Missing canonical homepage Atlas drawing");
  }
  await image.decode();
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 32;
  const context = canvas.getContext("2d");
  if (!context) {
    throw new Error("No color reader");
  }
  /** @param {string} color */
  const rgb = (color) => {
    context.fillStyle = color;
    context.fillRect(0, 0, 1, 1);
    const [r = 0, g = 0, b = 0] = context.getImageData(0, 0, 1, 1).data;
    return [r, g, b];
  };
  /** @param {number[]} color */
  const luminance = (color) =>
    color
      .map((value) => {
        const channel = value / 255;
        return channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4;
      })
      .reduce((sum, channel, i) => sum + channel * ([0.2126, 0.7152, 0.0722][i] ?? 0), 0);
  const background = rgb(getComputedStyle(cells).getPropertyValue("--kpress-doc-bg"));
  const ink = rgb(getComputedStyle(label).color);
  const light = Math.max(luminance(ink), luminance(background));
  const dark = Math.min(luminance(ink), luminance(background));
  context.clearRect(0, 0, 32, 32);
  context.drawImage(image, 0, 0, 32, 32);
  const pixels = context.getImageData(0, 0, 32, 32).data;
  let whiteSamples = 0;
  let coloredSamples = 0;
  for (let i = 0; i < pixels.length; i += 4) {
    const [r, g, b, alpha] = pixels.slice(i, i + 4);
    if (alpha === 255 && r === 255 && g === 255 && b === 255) {
      whiteSamples += 1;
    } else if (alpha === 255 && (r !== g || g !== b)) {
      coloredSamples += 1;
    }
  }
  const filter = getComputedStyle(image).filter;
  return {
    mode: document.documentElement.dataset.kpressTheme,
    resolved: document.documentElement.dataset.kpressResolvedTheme,
    cases: [...cells.querySelectorAll(".site-atlas-cell")].filter(
      (tile) => tile.getClientRects().length > 0,
    ).length,
    background,
    page_background: background,
    label: ink,
    label_contrast: (light + 0.05) / (dark + 0.05),
    white_samples: whiteSamples,
    colored_samples: coloredSamples,
    palette_signature: pixels.reduce((sum, value, index) => (sum + value * (index + 1)) >>> 0, 0),
    palette_samples: pixels.length / 4,
    palette_unchanged: filter === "none",
    filter,
  };
};
