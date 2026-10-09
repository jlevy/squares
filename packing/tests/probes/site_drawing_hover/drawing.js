// Inspect inline artwork or the actual decoded, fetched standalone SVG. A shadow root
// isolates the asset's SVG styles from page CSS; the screenshot still reads the IMG.
async (/** @type {{holder: string}} */ { holder }) => {
  const held = document.querySelector(holder);
  if (!held) {
    return null;
  }
  let graphic = held.querySelector("svg");
  const image = held.querySelector("img");
  /** @type {HTMLDivElement | null} */
  let reference = null;
  /** @type {{x: number, y: number, width: number, height: number} | null} */
  let imageBox = null;
  let sourceUrl = "";
  if (!graphic && image instanceof HTMLImageElement) {
    try {
      await image.decode();
    } catch {
      throw new Error("drawing image did not decode");
    }
    if (!image.complete || image.naturalWidth <= 0 || image.naturalHeight <= 0) {
      throw new Error("drawing image has no decoded artwork");
    }
    const response = await fetch(image.currentSrc);
    if (!response.ok || response.headers.get("content-type")?.split(";")[0] !== "image/svg+xml") {
      throw new Error("drawing response is not successful SVG artwork");
    }
    const source = new DOMParser().parseFromString(await response.text(), "image/svg+xml");
    const root = source.documentElement;
    if (
      !(root instanceof SVGSVGElement) ||
      root.namespaceURI !== "http://www.w3.org/2000/svg" ||
      root.querySelector("parsererror, script, foreignObject")
    ) {
      throw new Error("drawing response has no safe SVG document");
    }
    graphic = root;
    const rectangle = image.getBoundingClientRect();
    imageBox = {
      x: rectangle.x,
      y: rectangle.y,
      width: rectangle.width,
      height: rectangle.height,
    };
    if (imageBox.width <= 0 || Math.abs(imageBox.width - imageBox.height) > 0.01) {
      throw new Error("drawing image has no reserved square viewport");
    }
    sourceUrl = response.url;
    reference = document.createElement("div");
    reference.style.cssText =
      "position:fixed;left:-10000px;top:0;visibility:hidden;pointer-events:none";
    reference.attachShadow({ mode: "closed" }).append(graphic);
    document.body.append(reference);
  }
  if (!graphic) {
    return null;
  }
  try {
    const frame = graphic.querySelector(":scope > rect");
    const outlines = graphic.querySelector(":scope > g");
    if (!(frame instanceof SVGRectElement) || !(outlines instanceof SVGGElement)) {
      throw new Error("drawing artwork lacks its frame or square outlines");
    }
    const paths = [...outlines.querySelectorAll(":scope > path")];
    const squares = paths.reduce(
      (count, path) => count + (path.getAttribute("d")?.match(/M/g)?.length ?? 0),
      0,
    );
    const view = graphic.viewBox.baseVal;
    const geometry = frame.getBBox();
    if (
      !paths.length ||
      !squares ||
      geometry.width <= 0 ||
      geometry.height <= 0 ||
      view.width <= 0 ||
      view.height <= 0
    ) {
      throw new Error("drawing artwork has no square content or frame geometry");
    }
    const box = held.getBoundingClientRect();
    const edge = frame.getBoundingClientRect();
    const style = getComputedStyle(held);
    return {
      hover: held.matches(":hover"),
      focus_visible: held.matches(":focus-visible"),
      active: held.matches(":active"),
      background: style.backgroundColor,
      color: style.color,
      frame_stroke: getComputedStyle(frame).stroke,
      frame_fill: getComputedStyle(frame).fill,
      outline_stroke: getComputedStyle(outlines).stroke,
      square_count: squares,
      path_count: paths.length,
      source_url: sourceUrl,
      namespace: graphic.namespaceURI,
      natural_width: image instanceof HTMLImageElement ? image.naturalWidth : null,
      natural_height: image instanceof HTMLImageElement ? image.naturalHeight : null,
      frame: { x: geometry.x, y: geometry.y, width: geometry.width, height: geometry.height },
      viewbox: { x: view.x, y: view.y, width: view.width, height: view.height },
      image_box: imageBox,
      box: { x: box.left, y: box.top, width: box.width, height: box.height },
      edge: imageBox
        ? {
            x: imageBox.x + ((geometry.x - view.x) / view.width) * imageBox.width,
            y:
              imageBox.y +
              ((geometry.y + geometry.height / 2 - view.y) / view.height) * imageBox.height,
          }
        : { x: edge.left, y: edge.top + edge.height / 2 },
    };
  } finally {
    reference?.remove();
  }
};
