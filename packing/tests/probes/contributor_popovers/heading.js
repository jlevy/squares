/** @param {string} selector */
async (selector) => {
  await document.fonts.ready;
  const heading = document.querySelector(selector);
  if (!(heading instanceof HTMLElement)) {
    throw new Error("Missing generated page heading");
  }
  const style = getComputedStyle(heading);
  const reference = document.createElement("span");
  reference.style.fontFamily = "var(--kpress-font-sans)";
  heading.append(reference);
  const sans = getComputedStyle(reference).fontFamily;
  reference.remove();
  return {
    family: style.fontFamily,
    size: style.fontSize,
    weight: style.fontWeight,
    fontStyle: style.fontStyle,
    leading: style.lineHeight,
    spacing: style.letterSpacing,
    align: style.textAlign,
    transform: style.textTransform,
    sans,
  };
};
