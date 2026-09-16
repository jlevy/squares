// Self-test: a prose paragraph and a figure caption, each with a single Latin `.mord` run,
// for sampling the drawn faces across a whole print medium.
() => {
  document.body.classList.add("kpress-prose");
  /** @type {Element} */ (
    /** @type {Element} */ (document.querySelector("#b")).parentElement
  ).classList.add("kpress-figcaption");
  document.querySelectorAll(".katex").forEach((node) => {
    node.innerHTML = '<span class="mord">x</span>';
  });
};
