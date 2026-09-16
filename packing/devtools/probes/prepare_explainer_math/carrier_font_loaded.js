// Load the carrier-metrics control face, and fail unless exactly one face loaded.
async () => {
  const faces = await document.fonts.load('16px "Squares Carrier Control"');
  if (faces.length !== 1 || faces[0]?.status !== "loaded") {
    throw new Error("the carrier-metrics control did not load");
  }
};
