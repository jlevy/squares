// The width of the stage's view box, as the attribute's text: the scale the view is held at.
() =>
  /** @type {string} */ (
    /** @type {Element} */ (document.getElementById("packing-svg")).getAttribute("viewBox")
  ).split(" ")[2];
