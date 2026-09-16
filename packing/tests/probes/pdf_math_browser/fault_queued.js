// Fault: a printed formula still queued for rendering. True when the fault is in the DOM.
() => {
  const host = resetPdfMathGuardNode("tex");
  host.dataset.squaresMathQueued = "true";
  return host.getClientRects().length > 0;
};
