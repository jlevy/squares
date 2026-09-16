// Load every face that is not a math face, then wait two frames. Reading fonts can change
// ordinary prose widths too; those settle here, without waiting for the math requests the
// geometry probe deliberately holds.
async () => {
  await Promise.all(
    [...document.fonts]
      .filter((face) => !/^(?:["']?KaTeX_|["']?KPress Math Text)/.test(face.family))
      .map((face) => face.load()),
  );
  await new Promise((done) => requestAnimationFrame(() => requestAnimationFrame(done)));
};
