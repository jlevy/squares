// The scarlet mark, as [opacity, stroke width, the stroke colour as computed].
() => {
  const mark = document.getElementById("mark");
  const stroke = mark?.firstElementChild;
  if (mark == null || stroke == null) {
    throw new Error("probe requires #mark and its stroke");
  }
  return [
    mark.getAttribute("opacity"),
    stroke.getAttribute("stroke-width"),
    getComputedStyle(stroke).stroke,
  ];
};
