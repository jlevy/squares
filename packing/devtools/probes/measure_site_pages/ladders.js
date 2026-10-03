// The rating ladders as laid out: for each `.site-ladders` diagram on the page, its width,
// where it sits on the page (its top and height, to find it in a full-page screenshot),
// how many columns its rungs stand in, and every rung with its label, the ladder it
// belongs to, its column and its cell's height, then its description: the words, the
// box's width and height, the line height, how many lines the words take, how far they
// run past the box (0 when they fit), and whether the box sits beside the chip or under
// it. A significance rung's mark (`.site-significance`) stands for its chip throughout,
// its label read from the mark's words. A chip's title is reported as it reads, and
// `parts` counts what the rung holds: two, its chip and its description. `head_rules` and `row_rules` are the distinct widths of
// the rule under a column's head and of the rules a cell draws above and below itself,
// so `[1]` and `[0]` say one rule under the heads and none between the rows.
// `gutter_left` and `gutter_right` are the room between the diagram and the nearest
// ancestor that clips or scrolls sideways, or the page's own layout width where none
// does: negative where the diagram runs under the clip, 0 where it is flush. `frame`
// names what was measured against. `heights` is every distinct rung height, so one value
// means every row of the diagram is the same height; `empty` counts the cells that hold
// no rung and whether each takes room.
() => {
  /** What draws a rung: a chip, or for significance its mark (`significance_mark`). */
  const MARK = ".site-chip, .site-significance";
  /** @param {number} value */
  const round = (value) => Math.round(value * 10) / 10;
  /** The distinct widths of the block-side borders `sides` names, over `elements`.
   * @param {Element[]} elements
   * @param {("borderBlockStartWidth" | "borderBlockEndWidth")[]} sides */
  const rules = (elements, sides) => [
    ...new Set(
      elements.flatMap((element) =>
        sides.map((side) => round(Number.parseFloat(getComputedStyle(element)[side]))),
      ),
    ),
  ];
  /** @param {Element} element */
  const lines = (element) => {
    const range = document.createRange();
    range.selectNodeContents(element);
    return new Set([...range.getClientRects()].map((rect) => Math.round(rect.top))).size;
  };
  /** The inner left and right edges of what clips `element` sideways, and its name.
   * @param {Element} element */
  const clip = (element) => {
    for (let frame = element.parentElement; frame; frame = frame.parentElement) {
      if (getComputedStyle(frame).overflowX !== "visible") {
        const left = frame.getBoundingClientRect().left + frame.clientLeft;
        const name = [frame.tagName.toLowerCase(), ...frame.classList].join(".");
        return { left, right: left + frame.clientWidth, name };
      }
    }
    return { left: 0, right: document.documentElement.clientWidth, name: "page" };
  };
  return [...document.querySelectorAll(".site-ladders")]
    .filter((diagram) => diagram.getClientRects().length > 0)
    .map((diagram) => {
      const box = diagram.getBoundingClientRect();
      const frame = clip(diagram);
      const cells = [...diagram.querySelectorAll(".site-ladders-cell")];
      const rungs = cells.filter((cell) => cell.querySelector(MARK));
      const lefts = [
        ...new Set(rungs.map((cell) => Math.round(cell.getBoundingClientRect().left))),
      ];
      lefts.sort((a, b) => a - b);
      const measured = rungs.map((cell) => {
        const rect = cell.getBoundingClientRect();
        const chip = cell.querySelector(MARK);
        const meaning = cell.querySelector(".site-ladders-meaning");
        const words = meaning?.getBoundingClientRect();
        return {
          rung: (chip?.textContent ?? "").trim(),
          ladder: cell.getAttribute("data-ladder") ?? "",
          column: lefts.indexOf(Math.round(rect.left)) + 1,
          top: Math.round(rect.top - box.top),
          height: round(rect.height),
          meaning: (meaning?.textContent ?? "").trim(),
          meaning_width: round(words?.width ?? 0),
          meaning_height: round(words?.height ?? 0),
          line_height: meaning ? round(Number.parseFloat(getComputedStyle(meaning).lineHeight)) : 0,
          lines: meaning ? lines(meaning) : 0,
          overflow: meaning ? Math.max(0, meaning.scrollHeight - meaning.clientHeight) : 0,
          beside: (words?.left ?? 0) >= (chip?.getBoundingClientRect().right ?? 0),
          title: chip?.getAttribute("title") ?? "",
          parts: cell.querySelector(".site-ladders-rung")?.children.length ?? 0,
        };
      });
      return {
        block_width: round(box.width),
        gutter_left: round(box.left - frame.left),
        gutter_right: round(frame.right - box.right),
        frame: frame.name,
        top: Math.round(box.top + window.scrollY),
        height: Math.round(box.height),
        columns: lefts.length,
        heads: [...diagram.querySelectorAll(".site-ladders-head")].map((head) =>
          (head.querySelector(".site-ladders-name")?.textContent ?? "").trim(),
        ),
        head_rules: rules(
          [...diagram.querySelectorAll(".site-ladders-head")],
          ["borderBlockEndWidth"],
        ),
        row_rules: rules(rungs, ["borderBlockStartWidth", "borderBlockEndWidth"]),
        heights: [...new Set(measured.map((rung) => rung.height))],
        empty: cells
          .filter((cell) => !cell.querySelector(MARK))
          .map((cell) => round(cell.getBoundingClientRect().height)),
        rungs: measured,
      };
    });
};
