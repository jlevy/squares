// Self-test: add a dormant saved-font variant, which the walk must skip, and a hidden
// certificate's sans formula, which it must still count.
() => {
  const dormant = document.createElement("span");
  dormant.className = "squares-math-variant";
  dormant.dataset.squaresMathContexts = "custom-sans";
  dormant.style.display = "none";
  dormant.innerHTML = '<span class="katex">dormant</span>';
  const certificate = document.createElement("div");
  certificate.hidden = true;
  certificate.innerHTML =
    '<p class="sans"><span class="katex" ' +
    'data-kpress-math-face="sans">hidden certificate</span></p>';
  document.body.append(dormant, certificate);
};
