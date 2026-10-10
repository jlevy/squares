// Load every face that is not a math face, then wait two frames. Reading fonts can change
// ordinary prose widths too; those settle here, without waiting for the math requests the
// geometry probe deliberately holds. A face declared only from local() sources is a
// metric-adjusted stand-in for a shipped face while that one loads (`paper-type.css`): once
// the shipped face is in it draws nothing that face covers, and WebKit refuses to load one
// on demand.
async () => {
  /** @param {string} family */
  const unquoted = (family) => family.replace(/^["']|["']$/g, "");
  /** @param {string} family @param {string} weight @param {string} style */
  const slot = (family, weight, style) =>
    `${unquoted(family)}|${weight === "normal" ? "400" : weight}|${style}`;
  const localOnly = new Set();
  for (const sheet of document.styleSheets) {
    for (const rule of sheet.cssRules) {
      if (rule instanceof CSSFontFaceRule) {
        const src = rule.style.getPropertyValue("src");
        if (
          /local\(/.test(src) &&
          src.replace(/local\([^()]*\)/g, "").replace(/[\s,]/g, "") === ""
        ) {
          localOnly.add(
            slot(
              rule.style.getPropertyValue("font-family"),
              rule.style.getPropertyValue("font-weight") || "normal",
              rule.style.getPropertyValue("font-style") || "normal",
            ),
          );
        }
      }
    }
  }
  await Promise.all(
    [...document.fonts]
      .filter((face) => !/^(?:["']?KaTeX_|["']?KPress Math Text)/.test(face.family))
      .filter((face) => !localOnly.has(slot(face.family, face.weight, face.style)))
      .map((face) => face.load()),
  );
  await new Promise((done) => requestAnimationFrame(() => requestAnimationFrame(done)));
};
