// Fault: an unrendered native formula whose semantic MathML is clipped out of sight. True
// when the fault is in the DOM.
() => {
  const host = resetPdfMathGuardNode("native");
  delete host.dataset.kpressMathRendered;
  const semantic = /** @type {HTMLElement} */ (host.querySelector(".kpress-math-semantic"));
  semantic.style.cssText =
    "clip:rect(0px,0px,0px,0px); " +
    "clip-path:inset(50%); width:1px; height:1px; " +
    "overflow:hidden; position:absolute";
  return !!semantic.querySelector("math");
};
