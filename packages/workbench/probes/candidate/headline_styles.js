// The headline's six settings: the two `n =` glyph styles, the line's colour, the numeral's
// size and weight, and the line's size.
() => {
  /** @param {string} selector */
  const style = (selector) => {
    const element = document.querySelector(selector);
    if (element == null) {
      throw new Error(`probe requires ${selector}`);
    }
    return getComputedStyle(element);
  };
  return [
    style("#facts .nline .n-var").fontStyle,
    style("#facts .nline .n-eq").fontStyle,
    style("#facts .nline").color,
    style("#facts-a .n-val").fontSize,
    style("#facts-a .n-val").fontWeight,
    style("#facts .nline").fontSize,
  ];
};
