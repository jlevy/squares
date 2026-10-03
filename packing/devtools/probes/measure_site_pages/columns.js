// The columns of every shared data table (`.site-table`) as laid out, and what makes its
// rows tall. For each table that is showing: its classes, the heading above it, its
// width and the width of what scrolls it sideways (`frame_width`, the nearest ancestor
// that clips or scrolls, with `scrolls` how far the table runs past it, 0 when it
// fits), how many rows show, and `layout`, `table` or, on a phone, where a row is a
// card, `cards`. `top` and `height` place the component, the table with its filter bar,
// on the page, to find it in a full-page screenshot.
//
// In the `table` layout each column is reported under its header's words with its width
// and what its cells hold: `lines`, the most lines any cell of it takes; `held`, the
// width of the widest content a cell of it holds, so a column can be held to what it
// holds, and `held_by`, the key of the row whose cell holds it; `overflows`, the rows
// whose cell shows something past its own box, with by how much; and `tallest`, the
// tallest row whose height this column's cell sets, with that row's key, its height and
// the lines the cell takes. A row's height is set by the cell
// whose content is tallest, so a column that never sets one reports no `tallest`. A
// cell's content is measured as the box around what it holds, with what a negative
// margin sets past the cell's edge, and its lines as that height over the cell's own
// line height: exact for a cell of words, and a count of line boxes at the cell's line
// height for one of chips or math, whose lines are taller. `broken` lists the
// words of the column that a line break splits, which a cell too narrow for its longest
// word does to it ("Queuingthe" over "orydotcom"); a break after a hyphen or a slash is
// a word's own and is not counted, and typeset math is passed over.
//
// What a column's lines may not do is reported with them. `split` lists the values of a
// list of cases (`.site-n-value`) that sit on more than one line, a range cut at its
// dash. `piece` is the widest piece of typeset math in the column, with its row, its
// width and its text: KaTeX sets a formula as pieces a line cannot end inside (`.base`),
// so the widest is the least a cell of formulas can be. `wrapped` counts the formulas set
// on more than one line, and `cuts` lists the pieces a line ends after that close with
// neither a relation nor a binary operator, the only places a formula may end a line. `stranded` lists the punctuation that begins a line, such as
// the comma after a formula that filled its line.
//
// In the `cards` layout no column has a width and none sets a row's height alone; the
// table reports its tallest card (`tallest_row`, as it does in either layout) and each
// cell's class with the most lines it takes, so a cell that wraps badly on a phone shows
// there.
() => {
  /** @param {number} value */
  const round = (value) => Math.round(value * 10) / 10;
  /** @param {Element} el */
  const shown = (el) => el.getClientRects().length > 0;
  /** @param {Element} el */
  const words = (el) => (el.textContent ?? "").replace(/\s+/g, " ").trim();
  /** Where what a cell shows starts and ends across the line: the span of the boxes of
   * its words and of its elements, passing over an element a pixel wide or tall and all
   * it holds, as a visually hidden copy is (KaTeX's MathML, KPress's semantic math),
   * whose words keep their own width inside the clip. `null` for a cell that shows
   * nothing.
   * @param {Element} cell
   * @returns {{ left: number, right: number } | null} */
  const shownExtent = (cell) => {
    let left = Number.POSITIVE_INFINITY;
    let right = Number.NEGATIVE_INFINITY;
    const range = document.createRange();
    /** @param {DOMRect} box */
    const add = (box) => {
      if (box.width > 0 && box.height > 0) {
        left = Math.min(left, box.left);
        right = Math.max(right, box.right);
      }
    };
    /** @param {Node} node */
    const visit = (node) => {
      for (const child of node.childNodes) {
        if (child.nodeType === Node.TEXT_NODE && (child.textContent ?? "").trim()) {
          range.selectNodeContents(child);
          [...range.getClientRects()].forEach(add);
        } else if (child instanceof Element) {
          const box = child.getBoundingClientRect();
          if (box.width > 1 && box.height > 1) {
            add(box);
            visit(child);
          }
        }
      }
    };
    visit(cell);
    return right > left ? { left, right } : null;
  };
  /** The height and width of what a cell holds, the lines that height is at the cell's
   * line height, and how far what it shows runs past the cell's own box on either side.
   * @param {Element} cell */
  const content = (cell) => {
    const range = document.createRange();
    range.selectNodeContents(cell);
    const { height } = range.getBoundingClientRect();
    const style = getComputedStyle(cell);
    const line = Number.parseFloat(style.lineHeight) || Number.parseFloat(style.fontSize) * 1.2;
    const extent = shownExtent(cell);
    const box = cell.getBoundingClientRect();
    return {
      height: round(height),
      width: extent ? round(extent.right - extent.left) : 0,
      overflow: extent ? round(Math.max(0, extent.right - box.right, box.left - extent.left)) : 0,
      lines: height > 0 ? Math.max(1, Math.round(height / line)) : 0,
    };
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
  /** The values of a list of cases in a cell that a line break cuts.
   * @param {Element} cell */
  const split = (cell) =>
    [...cell.querySelectorAll(".site-n-value")]
      .filter(
        (value) =>
          new Set([...value.getClientRects()].map((rect) => Math.round(rect.top))).size > 1,
      )
      .map(words);
  /** Whether a piece of a formula closes with a relation or a binary operator, after
   * which KaTeX lets a line end: its last atom, the space after it aside.
   * @param {Element} piece */
  const closes = (piece) => {
    const atoms = [...piece.children].filter(
      (atom) => !atom.classList.contains("mspace") && !atom.classList.contains("strut"),
    );
    const last = atoms.at(-1);
    return Boolean(last?.classList.contains("mrel") || last?.classList.contains("mbin"));
  };
  /** The typeset math of a cell: its widest piece, how many of its formulas take more
   * than one line, and the pieces a line ends after that do not close with a relation
   * or a binary operator.
   * @param {Element} cell */
  const math = (cell) => {
    const line = Number.parseFloat(getComputedStyle(cell).lineHeight) || 20;
    /** @type {{ width: number, text: string } | null} */
    let piece = null;
    /** @type {string[]} */
    const cuts = [];
    let wrapped = 0;
    for (const formula of cell.querySelectorAll(".katex-html")) {
      const pieces = [...formula.children].filter((child) => child.classList.contains("base"));
      let ends = 0;
      for (const [index, base] of pieces.entries()) {
        const box = base.getBoundingClientRect();
        if (!piece || box.width > piece.width) {
          piece = { width: round(box.width), text: words(base) };
        }
        const next = pieces[index + 1];
        if (next && next.getBoundingClientRect().top - box.top > line / 2) {
          ends += 1;
          if (!closes(base)) {
            cuts.push(words(base));
          }
        }
      }
      wrapped += ends > 0 ? 1 : 0;
    }
    return { piece, cuts, wrapped };
  };
  /** The punctuation that begins a line of a cell: a comma, a stop or a closing bracket
   * at the start edge of what holds it, after something else.
   * @param {Element} cell */
  const stranded = (cell) => {
    /** @type {string[]} */
    const found = [];
    const walker = document.createTreeWalker(cell, NodeFilter.SHOW_TEXT);
    const range = document.createRange();
    let first = true;
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      const text = node.textContent ?? "";
      const holder = node.parentElement;
      if (holder?.closest(".katex, .kpress-math-render, .kpress-math-semantic")) {
        first = false;
        continue;
      }
      const mark = /^\s*([,.;:)\]])/.exec(text);
      if (mark && !first && holder) {
        const at = text.indexOf(mark[1] ?? "");
        range.setStart(node, at);
        range.setEnd(node, at + 1);
        const style = getComputedStyle(holder);
        const edge = holder.getBoundingClientRect().left + Number.parseFloat(style.paddingLeft);
        const box = range.getBoundingClientRect();
        if (box.width > 0 && Math.abs(box.left - edge) < 1 && style.display !== "inline") {
          found.push(text.trim().slice(0, 24));
        }
      }
      if (text.trim()) {
        first = false;
      }
    }
    return found;
  };
  /** A row's key: its id, the result it names, or its first cell's words.
   * @param {HTMLTableRowElement} row */
  const key = (row) =>
    row.id || row.getAttribute("data-result") || words(row.cells[0] ?? row).slice(0, 24);
  /** The width inside the nearest ancestor that clips or scrolls `element` sideways,
   * or the page's own layout width where none does.
   * @param {Element} element */
  const frameWidth = (element) => {
    for (let frame = element.parentElement; frame; frame = frame.parentElement) {
      if (getComputedStyle(frame).overflowX !== "visible") {
        return frame.clientWidth;
      }
    }
    return document.documentElement.clientWidth;
  };
  /** The heading a table sits under.
   * @param {Element} table */
  const section = (table) => {
    for (let at = /** @type {Element | null} */ (table); at; at = at.parentElement) {
      for (let before = at.previousElementSibling; before; before = before.previousElementSibling) {
        if (before.matches("h1, h2, h3")) {
          return words(before);
        }
      }
    }
    return "";
  };
  return [...document.querySelectorAll("table.site-table")]
    .filter((table) => table instanceof HTMLTableElement && shown(table))
    .map((found) => {
      const table = /** @type {HTMLTableElement} */ (found);
      const wrap = table.closest(".site-table-wrap") ?? table;
      // The bar is right above the table, or above the legend a table of results sets
      // between them (`overview_sections.rung_legend`).
      let bar = wrap.previousElementSibling;
      while (bar?.classList.contains("site-rung-legend")) {
        bar = bar.previousElementSibling;
      }
      const tools = bar?.classList.contains("site-table-tools") && shown(bar) ? bar : wrap;
      const top = tools.getBoundingClientRect().top;
      const box = table.getBoundingClientRect();
      const frame = frameWidth(table);
      const rows = [...(table.tBodies[0]?.rows ?? [])].filter(shown);
      const heads = [...(table.tHead?.rows[0]?.cells ?? [])];
      const cards = !heads.some(shown);
      const base = {
        table: [...table.classList].filter((item) => !item.startsWith("kpress-")).join("."),
        section: section(table),
        layout: cards ? "cards" : "table",
        table_width: round(box.width),
        frame_width: round(frame),
        scrolls: Math.max(0, round(box.width - frame)),
        shown_rows: rows.length,
        top: Math.round(top + window.scrollY),
        height: Math.round(wrap.getBoundingClientRect().bottom - top),
      };
      const measured = rows.map((row) => ({
        key: key(row),
        height: round(row.getBoundingClientRect().height),
        cells: [...row.cells].map((cell) => ({
          ...content(cell),
          ...math(cell),
          name: cell.className,
          broken: broken(cell),
          split: split(cell),
          stranded: stranded(cell),
        })),
      }));
      const tallestRow = measured.reduce(
        (best, row) => (best && best.height >= row.height ? best : row),
        /** @type {(typeof measured)[number] | null} */ (null),
      );
      const names = cards
        ? [...new Set(measured.flatMap((row) => row.cells.map((cell) => cell.name)))]
        : heads.map(words);
      const columns = names.map((name, index) => {
        const cellsOf = measured.flatMap((row) => {
          const cell = cards ? row.cells.find((item) => item.name === name) : row.cells[index];
          return cell ? [{ row, cell }] : [];
        });
        // The rows this column's cell sets the height of: none of the row's other cells
        // holds more.
        const sets = cards
          ? []
          : cellsOf.filter(({ row, cell }) =>
              row.cells.every((other) => other.height <= cell.height),
            );
        const tallest = sets.reduce(
          (best, item) => (best && best.row.height >= item.row.height ? best : item),
          /** @type {(typeof sets)[number] | null} */ (null),
        );
        const widest = cellsOf.reduce(
          (best, item) =>
            item.cell.piece && (best?.cell.piece?.width ?? 0) < item.cell.piece.width ? item : best,
          /** @type {(typeof cellsOf)[number] | null} */ (null),
        );
        const holds = cellsOf.reduce(
          (best, item) => (best && best.cell.width >= item.cell.width ? best : item),
          /** @type {(typeof cellsOf)[number] | null} */ (null),
        );
        const head = heads[index];
        return {
          column: name,
          width: cards || !head ? null : round(head.getBoundingClientRect().width),
          lines: Math.max(0, ...cellsOf.map(({ cell }) => cell.lines)),
          held: Math.max(0, ...cellsOf.map(({ cell }) => cell.width)),
          held_by: holds ? holds.row.key : null,
          overflows: cellsOf
            .filter(({ cell }) => cell.overflow > 0.5)
            .map(({ row, cell }) => ({ row: row.key, by: cell.overflow })),
          broken: [...new Set(cellsOf.flatMap(({ cell }) => cell.broken))],
          split: [...new Set(cellsOf.flatMap(({ cell }) => cell.split))],
          cuts: [...new Set(cellsOf.flatMap(({ cell }) => cell.cuts))],
          wrapped: cellsOf.reduce((sum, { cell }) => sum + cell.wrapped, 0),
          stranded: [...new Set(cellsOf.flatMap(({ cell }) => cell.stranded))],
          piece: widest ? { row: widest.row.key, ...widest.cell.piece } : null,
          tallest: tallest
            ? { row: tallest.row.key, height: tallest.row.height, lines: tallest.cell.lines }
            : null,
        };
      });
      return {
        ...base,
        tallest_row: tallestRow ? { row: tallestRow.key, height: tallestRow.height } : null,
        columns,
      };
    });
};
