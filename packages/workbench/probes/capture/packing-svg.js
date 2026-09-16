() => {
  const stage = document.getElementById("packing-svg");
  if (!(stage instanceof SVGElement)) {
    throw new Error("capture requires #packing-svg");
  }
  return stage.outerHTML;
};
