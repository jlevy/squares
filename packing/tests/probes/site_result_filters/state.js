// A table of results under its filter bar, as a reader has it now: whether Hide
// superseded is checked and what the HTML starts it at, the count's words, the rows
// showing and the rows that are current, which is to say not superseded, and how the
// checkbox and its label lie in the bar.
// Null where the page has no such bar, checkbox and table.
() => {
  const bar = document.querySelector(".site-result-filters");
  const box = bar?.querySelector('input[data-filter="current"]');
  const table = bar?.parentElement?.querySelector(":scope > .site-table-wrap table");
  if (
    !(bar instanceof HTMLElement) ||
    !(box instanceof HTMLInputElement) ||
    !(table instanceof HTMLTableElement)
  ) {
    return null;
  }
  /** @param {number} value */
  const round = (value) => Math.round(value * 10) / 10;
  /**
   * The lines a label's own words are set on: one box per line.
   * @param {Element} label
   */
  const words = (label) => {
    const text = [...label.childNodes].find(
      (node) => node.nodeType === Node.TEXT_NODE && (node.textContent ?? "").trim() !== "",
    );
    if (!text) {
      return [];
    }
    const range = document.createRange();
    range.selectNodeContents(text);
    return [...range.getClientRects()].map((line) => ({
      top: round(line.top),
      bottom: round(line.bottom),
    }));
  };
  const rows = [...(table.tBodies[0]?.rows ?? [])];
  /** @param {HTMLTableRowElement} row */
  const name = (row) => row.id || (row.dataset.result ?? "");
  const edge = bar.getBoundingClientRect();
  const label = box.labels?.[0] ?? null;
  const frame = label?.getBoundingClientRect();
  return {
    type: box.type,
    checked: box.checked,
    starts_checked: box.defaultChecked,
    focused: document.activeElement === box,
    reachable: box.tabIndex === 0 && !box.disabled,
    accent: getComputedStyle(box).accentColor,
    label: (label?.textContent ?? "").trim(),
    label_lines: label ? words(label) : [],
    label_before: frame ? round(edge.left - frame.left) : null,
    label_after: frame ? round(frame.right - edge.right) : null,
    bar_overflow: bar.scrollWidth - bar.clientWidth,
    // The labels in the bar: a preset-only control's is out of it until a link sets it.
    labels: [...bar.querySelectorAll("label:not([hidden])")].map((other) => ({
      filter: other.querySelector("[data-filter]")?.getAttribute("data-filter") ?? "",
      lines: words(other),
      after: round(other.getBoundingClientRect().right - edge.right),
    })),
    count: (bar.querySelector(".site-count")?.textContent ?? "").trim(),
    total: rows.length,
    shown: rows.filter((row) => !row.hidden).map(name),
    current: rows.filter((row) => row.dataset.current === "true").map(name),
  };
};
