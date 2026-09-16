// How many lines of text each slot of both facts layers draws: the text's boxes grouped by
// vertical centre, a new line wherever a box's centre sits more than half its own height from
// every line so far. A slot with no text draws none.
() =>
  ["facts-a", "facts-b"].flatMap((id) =>
    [.../** @type {HTMLElement} */ (document.getElementById(id)).children].map((slot) => {
      /** @type {number[]} */
      const centres = [];
      const walker = document.createTreeWalker(slot, NodeFilter.SHOW_TEXT);
      for (let node = walker.nextNode(); node !== null; node = walker.nextNode()) {
        if (
          (node.textContent ?? "").trim() === "" ||
          node.parentElement?.closest(".katex-mathml")
        ) {
          continue;
        }
        const range = document.createRange();
        range.selectNodeContents(node);
        for (const r of range.getClientRects()) {
          const centre = r.top + r.height / 2;
          if (r.height > 0 && centres.every((c) => Math.abs(c - centre) > r.height / 2)) {
            centres.push(centre);
          }
        }
      }
      return { layer: id, name: slot.className, lines: centres.length };
    }),
  );
