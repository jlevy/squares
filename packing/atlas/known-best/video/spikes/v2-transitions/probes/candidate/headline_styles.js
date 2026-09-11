// The headline's six settings: the two `n =` glyph styles, the line's colour, the numeral's
// size and weight, and the line's size.
() => [
  getComputedStyle(document.querySelector("#facts .nline .n-var")).fontStyle,
  getComputedStyle(document.querySelector("#facts .nline .n-eq")).fontStyle,
  getComputedStyle(document.querySelector("#facts .nline")).color,
  getComputedStyle(document.querySelector("#facts-a .n-val")).fontSize,
  getComputedStyle(document.querySelector("#facts-a .n-val")).fontWeight,
  getComputedStyle(document.querySelector("#facts .nline")).fontSize,
];
