// The approximately-equal glyph's metrics as the build stamped them into the page.
() => {
  const data = document.getElementById("atlas-data")?.textContent;
  if (data == null) {
    throw new Error("probe requires #atlas-data text");
  }
  return JSON.parse(data).metrics.approx;
};
