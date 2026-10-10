// Read actual native-SVG theme colors and contrast without changing packing hues.
/** @param {{scroll_top: boolean}} options */
async (options) => {
  if (options.scroll_top) {
    window.scrollTo({ top: 0, behavior: "instant" });
    await new Promise((resolve) => requestAnimationFrame(() => resolve(undefined)));
    await new Promise((resolve) => requestAnimationFrame(() => resolve(undefined)));
  }
  const svg = document.querySelector("[data-homepage-atlas-svg]");
  if (!(svg instanceof SVGSVGElement)) {
    throw new Error("Missing homepage Atlas SVG");
  }
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 1;
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
  /** @param {number[]} a @param {number[]} b */
  const contrast = (a, b) => {
    const first = luminance(a);
    const second = luminance(b);
    return (Math.max(first, second) + 0.05) / (Math.min(first, second) + 0.05);
  };
  /** @param {string} selector @param {"fill" | "stroke"} property */
  const color = (selector, property = "fill") => {
    const element = svg.querySelector(selector);
    if (!element) {
      throw new Error(`Missing Atlas theme feature: ${selector}`);
    }
    return rgb(getComputedStyle(element)[property]);
  };
  const background = color('[data-feature="atlas-background"]');
  const label = color('[data-feature="packing-label"]');
  const samples = [1, 5, 36, 291, 324].flatMap((n) => {
    const group = document.querySelector(
      `[data-homepage-atlas-svg] g[data-n="${n}"] [data-feature="square-fills"]`,
    );
    if (!group) {
      return [];
    }
    return [...group.querySelectorAll("polygon")].filter(
      (_, i, polygons) => i === 0 || i === polygons.length - 1,
    );
  });
  return {
    mode: document.documentElement.dataset.kpressTheme,
    resolved: document.documentElement.dataset.kpressResolvedTheme,
    cases: [
      ...document.querySelectorAll('[data-homepage-atlas-svg] g[data-feature="packing-card"]'),
    ].filter((card) => card.getClientRects().length > 0).length,
    background,
    page_background: rgb(getComputedStyle(svg).getPropertyValue("--kpress-doc-bg")),
    label_contrast: contrast(label, background),
    outline: color('[data-feature="container-outline"]', "stroke"),
    container: color('[data-feature="container-outline"]'),
    grid: color('[data-feature="square-fills"]', "stroke"),
    label,
    filter: getComputedStyle(svg).filter,
    palette_samples: samples.length,
    palette_unchanged: samples.every((polygon) => {
      const retained = polygon.getAttribute("fill");
      return (
        retained !== null && rgb(getComputedStyle(polygon).fill).join() === rgb(retained).join()
      );
    }),
  };
};
