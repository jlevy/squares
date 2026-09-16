// The missing-reservation control: unwrap the first laid-out reserved box before discovery,
// leaving its base in place. A checker that measures only surviving boxes would silently
// accept this subset.
() => {
  const box = /** @type {HTMLElement} */ (
    [...document.querySelectorAll(".squares-math-box")].find(
      (node) => node.getBoundingClientRect().width > 0,
    )
  );
  const base = /** @type {HTMLElement} */ (box.firstElementChild);
  base.style.position = "";
  box.replaceWith(base);
};
