// Self-test: add a bold run to the sans formula, whose 650 slot no face declares yet.
() => {
  const bold = document.createElement("span");
  bold.className = "mathbf";
  /** @type {Element} */ (document.querySelector("#b .katex")).appendChild(bold);
};
