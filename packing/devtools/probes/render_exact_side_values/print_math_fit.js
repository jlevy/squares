// Printing has no horizontal scrolling: every expanded display must fit its column.
() => {
  const hosts = [
    .../** @type {NodeListOf<HTMLElement>} */ (
      document.querySelectorAll(".exact-side-values-paper .kpress-math-display")
    ),
  ];
  const overflows = [];
  for (const [index, host] of hosts.entries()) {
    const source =
      host.dataset.kpressMathSource ||
      host.querySelector(".katex-mathml annotation")?.textContent ||
      "";
    const column = host.getBoundingClientRect();
    const html = host.querySelector(".katex-html");
    if (!html || column.width <= 0) {
      overflows.push({ index, source: source.slice(0, 160), reason: "unmeasured" });
      continue;
    }
    const boxes = [html, ...html.querySelectorAll(".base")].map((box) =>
      box.getBoundingClientRect(),
    );
    const left = Math.min(...boxes.map((box) => box.left));
    const right = Math.max(...boxes.map((box) => box.right));
    if (left < column.left - 1 || right > column.right + 1) {
      overflows.push({
        index,
        source: source.slice(0, 160),
        reason: "overflow",
        column_width: column.width,
        formula_width: right - left,
        left_overflow: Math.max(0, column.left - left),
        right_overflow: Math.max(0, right - column.right),
      });
    }
  }
  return { checked: hosts.length, overflows };
};
