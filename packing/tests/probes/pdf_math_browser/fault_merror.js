// Fault: an unrendered native formula whose semantic MathML is a parse error. True when the
// fault is in the DOM.
() => {
  const host = resetPdfMathGuardNode("native");
  delete host.dataset.kpressMathRendered;
  const math = /** @type {Element} */ (host.querySelector(".kpress-math-semantic math"));
  math.innerHTML = "<merror><mtext>unparsed formula</mtext></merror>";
  return math.checkVisibility();
};
