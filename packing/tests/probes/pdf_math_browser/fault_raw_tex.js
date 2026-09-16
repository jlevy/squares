// Fault: a finished fallback that exposes the formula's TeX source. True when the fault is
// in the DOM.
() => {
  const host = resetPdfMathGuardNode("tex");
  host.className = "";
  host.dataset.squaresMathReady = "true";
  host.textContent = "\\frac{1}{2}";
  return host.checkVisibility();
};
