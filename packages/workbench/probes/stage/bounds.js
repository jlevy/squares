// How the stage draws its container and the catalogue's box and trace: for each, whether it is
// drawn at all, its computed stroke and stroke width, its width attribute and its opacity. The
// catalogue draws the box and trace and leaves `#container` undrawn; a view that draws no box,
// Pack or the animation studio, must hide both and draw the container.
() => {
  /** @param {string} id */
  const read = (id) => {
    const element = document.getElementById(id);
    if (element == null) {
      throw new Error(`probe requires #${id}`);
    }
    const style = getComputedStyle(element);
    const box = element.getBoundingClientRect();
    return {
      shown: style.display !== "none" && style.visibility === "visible" && box.width > 0,
      stroke: style.stroke,
      strokeWidth: style.strokeWidth,
      width: Number(element.getAttribute("width")),
      opacity: Number(style.opacity),
    };
  };
  return { container: read("container"), box: read("bound-box"), trace: read("bound-trace") };
};
