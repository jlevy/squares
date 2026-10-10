// Geometry and prepared mathematics of one canonical or fetched case article.
() => {
  const panel = document.querySelector("[data-case-popover]:popover-open");
  const close = panel?.querySelector(".site-popover-close");
  const article =
    panel?.querySelector("article.site-case") ?? document.querySelector("article.site-case");
  if (!(article instanceof HTMLElement)) {
    throw new Error("No visible case article");
  }
  const title = article.querySelector(".site-case-title");
  const eyebrow = article.querySelector(".site-case-eyebrow");
  const status = article.querySelector(".site-case-status");
  const titleMath = title?.querySelector(".katex");
  const interval = article.querySelector(".site-case-interval");
  const drawing = article.querySelector(".site-case-figure > svg");
  const figure = article.querySelector(".site-case-figure");
  const gap = article.querySelector(".site-atlas-gap");
  const actions = panel?.querySelector(".site-popover-actions");
  const proven = article.querySelector(".site-atlas-pop-bound");
  const facts = article.querySelector(".site-case-summary-facts");
  if (
    !(
      title &&
      eyebrow &&
      status &&
      titleMath &&
      interval &&
      drawing &&
      figure &&
      gap &&
      proven &&
      facts
    )
  ) {
    throw new Error("The case summary is incomplete");
  }
  const glyphs = [...interval.querySelectorAll(".katex-html .mord")].map((node) =>
    node.getBoundingClientRect(),
  );
  const line = interval.getBoundingClientRect();
  const box = article.getBoundingClientRect();
  const formulas = [...article.querySelectorAll("[data-kpress-math-prepared]")];
  const bounds = article.querySelector(".site-case-bounds");
  if (!(bounds && title.parentElement)) {
    throw new Error("The case bounds or heading are incomplete");
  }
  const grid = bounds.getBoundingClientRect();
  const panels = [...bounds.children].map((node) => node.getBoundingClientRect());
  const first = panels[0];
  const last = panels.at(-1);
  const preceding = panels.at(-2);
  const lastPanel = bounds.lastElementChild;
  if (!(first && last && preceding && lastPanel)) {
    throw new Error("The case bound panels are incomplete");
  }
  const values = [...article.querySelectorAll(".site-atlas-gap-values > span")].map((node) =>
    node.getBoundingClientRect(),
  );
  const valuesOverlap = values.some((value, index) =>
    values
      .slice(index + 1)
      .some(
        (other) =>
          value.left < other.right &&
          value.right > other.left &&
          value.top < other.bottom &&
          value.bottom > other.top,
      ),
  );
  return {
    pageWidth: document.documentElement.scrollWidth,
    viewportWidth: innerWidth,
    viewportHeight: innerHeight,
    articleWidth: box.width,
    articleScrollWidth: article.scrollWidth,
    articleLeft: box.left,
    articleRight: box.right,
    articleCenter: (box.left + box.right) / 2,
    panelCenter: panel
      ? (panel.getBoundingClientRect().left + panel.getBoundingClientRect().right) / 2
      : null,
    close: close
      ? {
          float: getComputedStyle(close).cssFloat,
          position: getComputedStyle(close).position,
        }
      : null,
    titleFamily: getComputedStyle(title).fontFamily,
    titleSize: Number.parseFloat(getComputedStyle(title).fontSize),
    titleScale: Number.parseFloat(getComputedStyle(title).getPropertyValue("--paper-title-scale")),
    titleMathFamily: getComputedStyle(titleMath).fontFamily,
    titleMathSize: Number.parseFloat(getComputedStyle(titleMath).fontSize),
    titlePrepared: title.querySelectorAll('[data-kpress-math-prepared="true"]').length,
    titleMathText: title.querySelector(".kpress-math-semantic math")?.textContent,
    eyebrow: {
      text: eyebrow.textContent,
      center: (eyebrow.getBoundingClientRect().left + eyebrow.getBoundingClientRect().right) / 2,
      bottom: eyebrow.getBoundingClientRect().bottom,
    },
    titleCenter:
      (titleMath.getBoundingClientRect().left + titleMath.getBoundingClientRect().right) / 2,
    titleTop: titleMath.getBoundingClientRect().top,
    titleBottom: titleMath.getBoundingClientRect().bottom,
    statusTop: status.getBoundingClientRect().top,
    statusClasses: [...status.children].map((node) => node.className),
    actions: [...(panel?.querySelectorAll(".site-popover-action") ?? [])].map((node) => {
      const arrow = getComputedStyle(node, "::after");
      return {
        destination: node.getAttribute("data-go"),
        content: arrow.content,
        mask: arrow.maskImage,
        width: arrow.width,
        height: arrow.height,
      };
    }),
    titleParentSize: Number.parseFloat(getComputedStyle(title.parentElement).fontSize),
    sansBase:
      Number.parseFloat(getComputedStyle(facts).fontSize) /
      Number.parseFloat(getComputedStyle(facts).getPropertyValue("--paper-note-scale")),
    intervalWidth: interval.clientWidth,
    intervalScrollWidth: interval.scrollWidth,
    intervalOverflow: getComputedStyle(interval).overflowX,
    intervalTop: line.top,
    intervalBottom: line.bottom,
    glyphTop: Math.min(...glyphs.map((glyph) => glyph.top)),
    glyphBottom: Math.max(...glyphs.map((glyph) => glyph.bottom)),
    drawingWidth: drawing.getBoundingClientRect().width,
    drawingHeight: drawing.getBoundingClientRect().height,
    figureBottom: figure.getBoundingClientRect().bottom,
    drawingCenter:
      (drawing.getBoundingClientRect().left + drawing.getBoundingClientRect().right) / 2,
    gapTop: gap.getBoundingClientRect().top,
    footerPadding: actions
      ? {
          top: getComputedStyle(actions).paddingBlockStart,
          bottom: getComputedStyle(actions).paddingBlockEnd,
        }
      : null,
    gapValuesOverlap: valuesOverlap,
    gapValues: [...article.querySelectorAll(".site-atlas-gap-values > span")].map((node) => ({
      top: node.getBoundingClientRect().top,
      bottom: node.getBoundingClientRect().bottom,
      lineHeight: getComputedStyle(node).lineHeight,
      fontSize: getComputedStyle(node).fontSize,
    })),
    bounds: {
      count: panels.length,
      columns: getComputedStyle(bounds).gridTemplateColumns.split(" ").length,
      width: grid.width,
      center: (grid.left + grid.right) / 2,
      firstWidth: first.width,
      lastWidth: last.width,
      lastCenter: (last.left + last.right) / 2,
      lastTop: last.top,
      precedingTop: preceding.top,
      lastStyle: {
        inlineSize: getComputedStyle(lastPanel).inlineSize,
        boxSizing: getComputedStyle(lastPanel).boxSizing,
        paddingStart: getComputedStyle(lastPanel).paddingInlineStart,
        paddingEnd: getComputedStyle(lastPanel).paddingInlineEnd,
        borderStart: getComputedStyle(lastPanel).borderInlineStartWidth,
        borderEnd: getComputedStyle(lastPanel).borderInlineEndWidth,
        transition: getComputedStyle(lastPanel).transition,
      },
    },
    provenTop: proven.getBoundingClientRect().top,
    rem: Number.parseFloat(getComputedStyle(document.documentElement).fontSize),
    panelWidth: panel?.clientWidth,
    panelScrollWidth: panel?.scrollWidth,
    formulas: formulas.length,
    errors: article.querySelectorAll("[data-kpress-math-error]").length,
    unprepared: article.querySelectorAll('.kpress-math:not([data-kpress-math-rendered="true"])')
      .length,
    semantics: [...article.querySelectorAll(".kpress-math-semantic math")].map(
      (node) => node.outerHTML,
    ),
    overflowing: [...document.querySelectorAll("body *")]
      .filter((node) => {
        for (let ancestor = node.parentElement; ancestor; ancestor = ancestor.parentElement) {
          if (["auto", "scroll", "hidden", "clip"].includes(getComputedStyle(ancestor).overflowX)) {
            return false;
          }
        }
        return true;
      })
      .map((node) => ({
        element: node.tagName,
        classes: node.getAttribute("class"),
        text: node.textContent?.slice(0, 80),
        left: node.getBoundingClientRect().left,
        right: node.getBoundingClientRect().right,
      }))
      .filter((node) => node.right > innerWidth + 1 || node.left < -1)
      .slice(0, 30),
    generalBound: [...article.querySelectorAll(".site-case-prose p")].find((node) =>
      node.textContent?.includes("General bound:"),
    )?.innerHTML,
  };
};
