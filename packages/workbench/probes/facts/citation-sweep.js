// Every n's CITATION section as the facts panel draws it with the setting at o.on. Each step into
// n + 1 is shown paused at its start, where layer A is n's, and the last step's layer B is the
// last n's. For each n: how many citation slots the layer built, the head's word where it is
// drawn as a head, the frontier record named on its line and where that ends, and each drawn
// line's slot, words and extent in stage px; with them, the column's two edges. The setting and the step on the stage are put back afterwards.
/** @param {{on: boolean}} o */
(o) => {
  const api = window.atlasTransitions;
  const was = api.citations();
  const step = api.state().pair;
  api.pause();
  api.setCitations(o.on);
  const stage = /** @type {HTMLElement} */ (document.getElementById("stage"));
  const frame = stage.getBoundingClientRect();
  const scale = frame.width / stage.offsetWidth;
  const x = (/** @type {number} */ v) => Math.round(((v - frame.left) / scale) * 100) / 100;
  const note = /** @type {HTMLElement} */ (document.getElementById("stage-note"));
  const column = {
    left: x(note.getBoundingClientRect().left),
    right: x(note.getBoundingClientRect().right),
  };
  const read = (/** @type {string} */ id) => {
    const layer = /** @type {HTMLElement} */ (document.getElementById(id));
    const head = layer.querySelector(".head-cite");
    return {
      built: layer.querySelectorAll(".head-cite, .cite-line").length,
      head: head?.classList.contains("section-head")
        ? (head.firstElementChild?.textContent ?? "")
        : null,
      record: head?.querySelector(".cite-record-name")?.textContent ?? null,
      recordRight: (() => {
        const record = head?.querySelector(".cite-record");
        return record == null ? null : x(record.getBoundingClientRect().right);
      })(),
      lines: [...layer.querySelectorAll(".cite-line")]
        .filter((line) => line.children.length > 0)
        .map((line) => {
          const box = line.getBoundingClientRect();
          return {
            slot: line.classList.contains("cite-lower") ? "lower" : "upper",
            bound: line.querySelector(".cite-bound")?.textContent ?? null,
            text: line.querySelector(".cite-text")?.textContent ?? null,
            corrects: line.querySelector(".cite-corrects")?.textContent ?? null,
            note: line.querySelector(".cite-note")?.textContent ?? null,
            left: x(box.left),
            right: x(box.right),
          };
        }),
    };
  };
  const pairs = api.pairs();
  const drawn = [];
  for (const pair of pairs) {
    api.select(pair.index);
    api.seek(0);
    drawn.push({ n: pair.n, ...read("facts-a") });
  }
  const last = pairs[pairs.length - 1];
  if (last !== undefined) {
    drawn.push({ n: last.n + 1, ...read("facts-b") });
  }
  api.setCitations(was);
  api.select(step);
  api.seek(0);
  return { column, drawn };
};
