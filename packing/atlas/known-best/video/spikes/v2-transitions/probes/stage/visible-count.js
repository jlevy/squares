// How many squares are actually drawn: on the stage, not transparent, and with a width.
() =>
  Array.from(document.querySelectorAll("#squares g[data-identity]")).filter(
    (e) =>
      e.style.display !== "none" &&
      Number(e.getAttribute("opacity") === null ? 1 : e.getAttribute("opacity")) > 0.01 &&
      e.firstElementChild.getBoundingClientRect().width > 0,
  ).length;
