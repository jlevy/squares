// A standalone atlas drawing remains the same image under the link's hover wash.
(/** @type {{holder: string}} */ { holder }) => {
  const held = document.querySelector(holder);
  const image = held?.querySelector("img");
  if (!(held instanceof HTMLElement) || !(image instanceof HTMLImageElement)) {
    return null;
  }
  const style = getComputedStyle(held);
  const painted = getComputedStyle(image);
  return {
    hover: held.matches(":hover"),
    background: style.backgroundColor,
    source: image.currentSrc,
    filter: painted.filter,
    opacity: painted.opacity,
    natural_width: image.naturalWidth,
  };
};
