// Every piece of text the stage draws, with the id of its nearest ancestor that has one. Text a
// viewer cannot see is left out: a node with no box, one hidden by `visibility`, one inside a
// part drawn at opacity zero, and the screen-reader-only elements, which are clipped to a pixel.
() => {
  const stage = /** @type {HTMLElement} */ (document.getElementById("stage"));
  const walker = document.createTreeWalker(stage, NodeFilter.SHOW_TEXT);
  /** @type {{text: string, owner: string | null}[]} */
  const drawn = [];
  for (let node = walker.nextNode(); node !== null; node = walker.nextNode()) {
    const text = (node.textContent ?? "").trim();
    const parent = node.parentElement;
    if (text === "" || parent === null || parent.closest(".sr-only, script, style, title")) {
      continue;
    }
    const range = document.createRange();
    range.selectNodeContents(node);
    const boxed = [...range.getClientRects()].some((r) => r.width > 0 && r.height > 0);
    let seen = 1;
    for (let e = /** @type {Element | null} */ (parent); e && e !== stage; e = e.parentElement) {
      const style = getComputedStyle(e);
      if (style.display === "none") {
        seen = 0;
      }
      seen *= Number(style.opacity);
    }
    if (!boxed || seen <= 0 || getComputedStyle(parent).visibility !== "visible") {
      continue;
    }
    drawn.push({ text, owner: parent.closest("[id]")?.id ?? null });
  }
  return drawn;
};
