// Computed News chip colors and reset/count geometry, independent of CSS selectors' source order.
/** @param {{topicSelector?: string, topicAttribute?: string, protectRungs?: boolean} | null} config */
(config) => {
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
  const selector = config?.topicSelector ?? ".site-chip[data-news-topic]";
  const attribute = config?.topicAttribute ?? "data-news-topic";
  const samples = [...document.querySelectorAll(selector)].map((chip) => {
    const style = getComputedStyle(chip);
    const ink = rgb(style.color);
    const background = rgb(style.backgroundColor);
    const first = luminance(ink);
    const second = luminance(background);
    return {
      topic: chip.getAttribute(attribute),
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
  const title = document.querySelector("h1");
  return {
    samples,
    protected: config?.protectRungs
      ? [
          ...document.querySelectorAll(
            '.site-rung-fill, .site-chip[data-status="confirmed"], .site-chip[data-status="reviewed"], .site-chip[data-status="recorded"], .site-significance',
          ),
        ].map((chip) => {
          const style = getComputedStyle(chip);
          return {
            key: chip.matches(".site-significance")
              ? "--site-significance"
              : (chip.getAttribute("data-status") ??
                `${chip.getAttribute("data-rung")}${chip.getAttribute("data-level")}`),
            channels: rgb(chip.matches(".site-significance") ? style.color : style.backgroundColor),
          };
        })
      : [],
    reset: box("[data-news-reset]"),
    count: box("[data-news-count]"),
    topics: box("[data-site-filter-trigger]"),
    titleBottom: title ? getComputedStyle(title).marginBottom : null,
    overflow: document.documentElement.scrollWidth - innerWidth,
  };
};
