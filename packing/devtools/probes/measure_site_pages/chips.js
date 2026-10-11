// Every chip the page shows (`.site-chip`), as laid out: what kind it is, its words, the
// surface it sits on, its font size and line height, its box (`inline_size` and
// `block_size`, its border box's width and height), and how many lines its words take,
// the block size over the line height, which is 1 for a chip that does not wrap.
// `white_space` is the chip's computed value, `nowrap` wherever the one chip rule holds.
//
// A chip is a `rung` for a rating (S, V or C), `kind` for what a result is, `standing`
// for a chip of a result's status line (its status, who has the next move, and whether
// it is superseded), `novelty` for a novelty label, and `chip` for any other; its
// surface is a table, a popover, the rating ladders, a card or the prose. `scope` keeps
// only the chips inside an element it matches, for what a press opened; without one,
// the chips inside a popover are left out, since a closed popover shows none.
(/** @type {{scope?: string | null} | undefined} */ options) => {
  const scope = options?.scope ?? null;
  /** @param {number} value */
  const round = (value) => Math.round(value * 10) / 10;
  /** @param {Element} chip */
  const kind = (chip) => {
    if (chip.classList.contains("site-rung-fill")) {
      return "rung";
    }
    if (chip.hasAttribute("data-kind")) {
      return "kind";
    }
    if (["data-status", "data-activity", "data-standing"].some((name) => chip.hasAttribute(name))) {
      return "standing";
    }
    return chip.hasAttribute("data-novelty") ? "novelty" : "chip";
  };
  /** @param {Element} chip */
  const surface = (chip) => {
    if (chip.closest("[popover]")) {
      return "popover";
    }
    if (chip.closest("table")) {
      return "table";
    }
    if (chip.closest(".site-ladders")) {
      return "ladders";
    }
    return chip.closest(".site-card") ? "card" : "prose";
  };
  const root = scope ? document.querySelector(scope) : document;
  if (!root) {
    return [];
  }
  return [...root.querySelectorAll(".site-chip")]
    .filter((chip) => chip.getClientRects().length > 0)
    .filter((chip) => scope !== null || !chip.closest("[popover]"))
    .map((chip) => {
      const style = getComputedStyle(chip);
      const box = chip.getBoundingClientRect();
      const line = Number.parseFloat(style.lineHeight);
      return {
        chip: kind(chip),
        text: (chip.textContent ?? "").trim(),
        kind: chip.getAttribute("data-kind"),
        status: chip.getAttribute("data-status"),
        standing: chip.getAttribute("data-standing"),
        fill: style.backgroundColor,
        ink: style.color,
        surface: surface(chip),
        font_size: round(Number.parseFloat(style.fontSize)),
        line_height: round(line),
        inline_size: round(box.width),
        block_size: round(box.height),
        lines: line > 0 ? Math.round(box.height / line) : 0,
        white_space: style.whiteSpace,
      };
    });
};
