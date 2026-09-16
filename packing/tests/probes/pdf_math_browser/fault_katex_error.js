// Fault: a printed formula showing KaTeX's error. True when the fault is in the DOM.
() => {
  const host = resetPdfMathGuardNode("tex");
  const error = document.createElement("span");
  error.className = "katex-error";
  error.textContent = "unparsed formula";
  host.appendChild(error);
  return error.checkVisibility();
};
