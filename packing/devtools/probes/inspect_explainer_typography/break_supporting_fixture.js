// The self-test's known supporting-typography violations, put into its valid fixture: a
// footnote at the wrong size and colour, an underlined link, and one SVG label moved onto
// the other.
() => {
  const footnote = /** @type {HTMLElement} */ (document.querySelector("#footnote"));
  footnote.style.fontSize = "24px";
  footnote.style.color = "#f00";
  /** @type {HTMLAnchorElement} */ (document.querySelector("a")).style.textDecoration = "underline";
  const labels = document.querySelectorAll("svg text");
  /** @type {Element} */ (labels[1]).setAttribute("x", "10");
  /** @type {Element} */ (labels[1]).setAttribute("y", "40");
};
