// The frontier atlas's table as laid out: its width, the width of what scrolls it
// sideways and how far it runs past that (`scrolls`, 0 when it fits), its header cells,
// and each row named in `rows` (ids such as "n-11").
//
// A header cell reports the words it shows, its name for a screen reader, its classes,
// its box, how it sits in its cell and whether it sticks. A row reports its height and
// every cell: its classes, its width, `vertical_align`, the room its content leaves
// above and below inside the cell's padding (equal when the content is centred), the
// decimals it sets under a closed form, and the words a line break splits (`broken`). The drawing and the case number are
// reported apart, each with its box's middle, since those two are what a reader sees
// side by side: `thumb` is the drawing's cell, with the drawing's size and whether
// anything else is in the cell, and `n` is the number's own text, with its weight.
// Null where the page has no such table.
async (/** @type {{rows: string[]}} */ { rows }) => {
  const table = document.querySelector(".site-frontier table.site-table");
  if (!(table instanceof HTMLTableElement)) {
    return null;
  }
  for (const id of rows) {
    const row = document.getElementById(id);
    const image = row?.querySelector(".site-thumb img");
    const expected = `atlas/house/${id}.svg`;
    if (!(image instanceof HTMLImageElement) || image.getAttribute("src") !== expected) {
      throw new Error(`missing or mismatched drawing for ${id}`);
    }
    image.loading = "eager";
    await image.decode();
    if (!image.complete || image.naturalWidth !== 1000 || image.naturalHeight !== 1000) {
      throw new Error(`invalid drawing dimensions for ${id}`);
    }
  }
  // Decoded drawings can reveal new font runs after a resize. Measure the final
  // font metrics and table layout rather than the fallback frame.
  table.getBoundingClientRect();
  await document.fonts.ready;
  await new Promise((resolve) => requestAnimationFrame(resolve));
  await new Promise((resolve) => requestAnimationFrame(resolve));
  /** What scrolls the table sideways: its nearest ancestor that clips or scrolls. */

  const frame = (() => {
    for (let held = table.parentElement; held; held = held.parentElement) {
      if (getComputedStyle(held).overflowX !== "visible") {
        return held;
      }
    }
    return document.documentElement;
  })();
  /** @param {number} value */
  const round = (value) => Math.round(value * 10) / 10;
  /** @param {Element} el */
  const words = (el) => (el.textContent ?? "").replace(/\s+/g, " ").trim();
  /** @param {DOMRect} box */
  const middle = (box) => round((box.top + box.bottom) / 2);
  /** The box around what a node holds.
   * @param {Node} node */
  const held = (node) => {
    const range = document.createRange();
    range.selectNodeContents(node);
    return range.getBoundingClientRect();
  };
  /** The words of a cell that a line break splits, outside its typeset math: each run
   * of characters up to a space, a hyphen or a slash that sits on more than one line.
   * @param {Element} cell */
  const broken = (cell) => {
    /** @type {string[]} */
    const found = [];
    const walker = document.createTreeWalker(cell, NodeFilter.SHOW_TEXT);
    const range = document.createRange();
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      if (node.parentElement?.closest(".katex")) {
        continue;
      }
      for (const word of (node.textContent ?? "").matchAll(/[^\s\-\u2010-\u2014/]+/g)) {
        range.setStart(node, word.index);
        range.setEnd(node, word.index + word[0].length);
        const tops = new Set([...range.getClientRects()].map((rect) => Math.round(rect.top)));
        if (tops.size > 1) {
          found.push(word[0]);
        }
      }
    }
    return found;
  };
  /** @param {HTMLTableCellElement} cell */
  const measured = (cell) => {
    const style = getComputedStyle(cell);
    const box = cell.getBoundingClientRect();
    const content = held(cell);
    const empty = content.height === 0;
    return {
      classes: cell.className,
      width: round(box.width),
      vertical_align: style.verticalAlign,
      above: empty ? null : round(content.top - box.top - Number.parseFloat(style.paddingTop)),
      below: empty
        ? null
        : round(box.bottom - Number.parseFloat(style.paddingBottom) - content.bottom),
      approx: [...cell.querySelectorAll(".site-approx")].map(words),
      broken: broken(cell),
    };
  };
  return {
    table_width: round(table.getBoundingClientRect().width),
    frame_width: frame.clientWidth,
    scrolls: frame.scrollWidth - frame.clientWidth,
    page_scrolls: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    head: [...(table.tHead?.rows[0]?.cells ?? [])].map((cell) => {
      const style = getComputedStyle(cell);
      const box = cell.getBoundingClientRect();
      return {
        words: words(cell),
        label: cell.getAttribute("aria-label"),
        classes: cell.className,
        sorts: cell.getAttribute("data-sort"),
        sorted: cell.getAttribute("aria-sort"),
        width: round(box.width),
        top: round(box.top),
        vertical_align: style.verticalAlign,
        position: style.position,
        font: style.fontFamily,
        font_size: style.fontSize,
      };
    }),
    rows: rows.map((id) => {
      const row = document.getElementById(id);
      if (!(row instanceof HTMLTableRowElement)) {
        return null;
      }
      const cells = [...row.cells];
      const thumbCell = cells.find((cell) => cell.classList.contains("site-thumb"));
      const drawing = thumbCell?.querySelector("img");
      const link = cells
        .find((cell) => cell.classList.contains("site-col-n"))
        ?.querySelector("a[data-case]");
      const drawn = drawing?.getBoundingClientRect();
      const number = link ? held(link) : null;
      return {
        id,
        shown: row.getClientRects().length > 0,
        top: round(row.getBoundingClientRect().top),
        height: round(row.getBoundingClientRect().height),
        cells: cells.map(measured),
        thumb:
          thumbCell && drawn
            ? {
                index: cells.indexOf(thumbCell),
                width: round(drawn.width),
                height: round(drawn.height),
                left: round(drawn.left),
                middle: middle(drawn),
                alone: thumbCell.children.length === 1 && words(thumbCell) === "",
              }
            : null,
        n:
          link && number
            ? {
                words: words(link),
                weight: getComputedStyle(link).fontWeight,
                left: round(number.left),
                middle: middle(number),
              }
            : null,
      };
    }),
  };
};
