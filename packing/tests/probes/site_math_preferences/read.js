// Read actual glyph families and geometry; hidden fallback trees contribute no boxes.
() => ({
  prose: document.documentElement.dataset.kpressProseFont ?? "serif",
  fonts: document.documentElement.dataset.kpressFontSet ?? "custom",
  mathScripts: [...document.scripts].filter((script) => /katex|math-runtime/.test(script.src))
    .length,
  formulas: [...document.querySelectorAll("[data-font-role]")].map((section) => {
    const host = section.querySelector(".kpress-math-render");
    if (!(host instanceof HTMLElement)) {
      throw new Error("missing prepared font fixture");
    }
    // Inline wrapper rectangles can change with font substitution while the
    // visual math stays fixed. A paragraph measures its position against prose.
    const paragraph = host.closest("p") ?? host.parentElement ?? host;
    const at = paragraph.getBoundingClientRect();
    const visible = [...host.querySelectorAll(".katex-html")].filter(
      (node) => node.getClientRects().length > 0,
    );
    const glyph = [...host.querySelectorAll(".mathnormal, .mord")].find(
      (node) => node.getClientRects().length > 0,
    );
    return {
      role: section.getAttribute("data-font-role"),
      visualCount: visible.length,
      semantics: section.querySelectorAll("math").length,
      family: glyph ? getComputedStyle(glyph).fontFamily : null,
      hostFont: getComputedStyle(host).font,
      paragraphWidth: at.width,
      paragraphHeight: at.height,
      nodes: [...host.querySelectorAll(".strut, .vlist, .mord, .mrel, .mathnormal, .sizing")]
        .filter((node) => node.getClientRects().length > 0)
        .map((node) => {
          const box = node.getBoundingClientRect();
          return {
            classes: [...node.classList].filter((name) => !/^sm[0-9a-f]{10}$/.test(name)).join(" "),
            left: box.left - at.left,
            top: box.top - at.top,
            width: box.width,
            height: box.height,
            font: getComputedStyle(node).font,
            verticalAlign: getComputedStyle(node).verticalAlign,
          };
        }),
    };
  }),
});
