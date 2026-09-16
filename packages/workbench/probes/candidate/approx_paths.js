// The approximately-equal badge's outlines, as [d, transform, stroke width] each.
() =>
  Array.from(document.querySelectorAll("#facts-a .badge-muted .glyph-path")).map((p) => [
    p.getAttribute("d"),
    p.getAttribute("transform"),
    p.getAttribute("stroke-width"),
  ]);
