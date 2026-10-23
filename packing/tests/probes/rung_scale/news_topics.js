// Computed News chip colors and reset/count geometry, independent of CSS selectors' source order.
() => {
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d", { willReadFrequently: true });
  if (!context) {
    throw new Error("A canvas is required to measure rendered topic colors");
  }
  /** @param {string} color */
  const rgb = (color) => {
    context.clearRect(0, 0, 1, 1);
    context.fillStyle = color;
    context.fillRect(0, 0, 1, 1);
    return [...context.getImageData(0, 0, 1, 1).data].slice(0, 3);
  };
  /** @param {number[]} channels */
  const luminance = (channels) =>
    channels.reduce((total, value, index) => {
      const channel = value / 255;
      const linear = channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4;
      return total + linear * ([0.2126, 0.7152, 0.0722][index] ?? 0);
    }, 0);
  const samples = [...document.querySelectorAll(".site-chip[data-news-topic]")].map((chip) => {
    const style = getComputedStyle(chip);
    const ink = rgb(style.color);
    const background = rgb(style.backgroundColor);
    const first = luminance(ink);
    const second = luminance(background);
    return {
      topic: chip.getAttribute("data-news-topic"),
      role: chip.closest("[data-site-filter-summary]")
        ? "summary"
        : chip.matches("button")
          ? "option"
          : "tag",
      ink,
      background,
      contrast: (Math.max(first, second) + 0.05) / (Math.min(first, second) + 0.05),
    };
  });
  /** @param {string} selector */
  const box = (selector) => {
    const rect = document.querySelector(selector)?.getBoundingClientRect();
    return rect ? { right: rect.right, top: rect.top, bottom: rect.bottom } : null;
  };
  return {
    samples,
    reset: box("[data-news-reset]"),
    count: box("[data-news-count]"),
    titleBottom: document.querySelector("h1")
      ? getComputedStyle(document.querySelector("h1")).marginBottom
      : null,
    overflow: document.documentElement.scrollWidth - innerWidth,
  };
};
