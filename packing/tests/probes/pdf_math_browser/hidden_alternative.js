// A dormant prepared profile may retain raw source. Its visible sibling supplies the printed
// formula; clipped semantic copies elsewhere on the real page remain beside their
// successfully rendered KaTeX too. True when the dormant alternative has no layout.
() => {
  const host = resetPdfMathGuardNode("tex");
  const alternative = document.createElement("span");
  alternative.className = "squares-math-variant";
  alternative.dataset.squaresMathContexts = "system-sans";
  alternative.textContent = "\\frac{1}{2}";
  host.appendChild(alternative);
  return alternative.getClientRects().length === 0;
};
