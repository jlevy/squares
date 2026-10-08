/* Keep SVG labels at the publication support-text size through viewBox scaling. A
   diagram that names in `--paper-diagram-fit-from` (a registered length, so read here in
   px) the narrowest width its labels were laid out for at that size, and is drawn
   narrower, as the T-060 paper's are on a phone, takes labels that shrink with it in
   proportion, so each stays in its box: a floor of 0.7 of the support size, tried on
   2026-10-03, ran the roadmap's titles into their boxes' edges and its arrows. */
(() => {
  const diagrams = [
    ...document.querySelectorAll(
      ".line-fig svg, .chart svg, .n11-paper figure > svg, .n11-diagram",
    ),
  ].map((svg) => /** @type {SVGSVGElement} */ (svg));
  function sizeDiagramLabels() {
    const sizes = [];
    for (const svg of diagrams) {
      const width = svg.getBoundingClientRect().width;
      if (!width) {
        continue;
      }
      const matrix = svg.getScreenCTM();
      const scale = matrix && Math.hypot(matrix.c, matrix.d);
      if (!scale) {
        continue;
      }
      const fitFrom = parseFloat(
        getComputedStyle(svg).getPropertyValue("--paper-diagram-fit-from"),
      );
      const shrink = fitFrom > width ? width / fitFrom : 1;
      const size = (parseFloat(getComputedStyle(svg.parentElement).fontSize) * shrink) / scale;
      const caption = svg.closest("figure")?.querySelector("figcaption");
      const noteSize = caption
        ? (parseFloat(getComputedStyle(caption).fontSize) * shrink) / scale
        : null;
      sizes.push({ svg, size, noteSize });
    }
    // Reading the next diagram after a label mutation would force style/layout again.
    for (const { svg, size, noteSize } of sizes) {
      svg.style.setProperty("--paper-diagram-font-size", `${size}px`);
      if (noteSize !== null) {
        svg.style.setProperty("--paper-diagram-note-size", `${noteSize}px`);
      }
    }
  }
  const diagramObserver = new ResizeObserver(sizeDiagramLabels);
  diagrams.forEach((svg) => {
    diagramObserver.observe(svg);
  });
  window.addEventListener("beforeprint", sizeDiagramLabels);
  window.addEventListener("afterprint", sizeDiagramLabels);
  window.matchMedia("print").addEventListener("change", sizeDiagramLabels);
  void document.fonts.ready.then(sizeDiagramLabels);
  sizeDiagramLabels();
})();
