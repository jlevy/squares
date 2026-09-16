// The scene as drawn, as one JSON string: the view, the container, every shown pool element's
// identity, pose, opacity and fill, and the mark's opacity and pose. (The pool keeps hidden
// elements for every identity ever shown, so the raw outerHTML grows with the pairs visited;
// the picture does not.)
() =>
  JSON.stringify([
    /** @type {Element} */ (document.getElementById("packing-svg")).getAttribute("viewBox"),
    /** @type {Element} */ (document.getElementById("container")).getAttribute("width"),
    Array.from(/** @type {NodeListOf<SVGGElement>} */ (document.querySelectorAll("#squares g")))
      .filter((g) => g.style.display !== "none")
      .map((g) => [
        g.dataset.identity,
        g.getAttribute("transform"),
        g.getAttribute("opacity"),
        /** @type {Element} */ (g.firstElementChild).getAttribute("fill"),
      ]),
    /** @type {Element} */ (document.getElementById("mark")).getAttribute("opacity"),
    /** @type {Element} */ (document.getElementById("mark")).getAttribute("transform"),
  ]);
