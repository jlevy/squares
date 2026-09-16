// The arriving square and the container, as [its opacity, the mark's opacity, the mark's
// stroke width, the container's side]. Takes {identity}.
/** @param {{identity: number}} o */
(o) => {
  const square = document.querySelector(`#squares g[data-identity="${o.identity}"]`);
  const mark = document.getElementById("mark");
  const stroke = mark?.firstElementChild;
  const width = document.getElementById("container")?.getAttribute("width");
  if (square == null || mark == null || stroke == null || width == null) {
    throw new Error("probe requires the arriving square, mark, and container");
  }
  return [
    Number(square.getAttribute("opacity")),
    mark.getAttribute("opacity"),
    stroke.getAttribute("stroke-width"),
    parseFloat(width),
  ];
};
