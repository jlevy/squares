// The facts panel through one step's handover, read without the page's own matching rule. For
// each slot of the n and n + 1 layers: its drawn parts (an SVG whole; any other element with no
// element children and a box, the slot itself when it has none; KaTeX's hidden MathML skipped),
// each keyed by its text or bare markup and its box, and for a lone digit the number it is drawn
// in. Then, at each instant o.at (seconds), the opacity each part is seen at (its own times
// every ancestor's up to the panel) and the headline's arriving numeral's opacity, which is the
// crossfade the page runs. o.n is the step's n.
/** @param {{n: number, at: number[]}} o */
(o) => {
  const api = window.atlasTransitions;
  api.pause();
  api.setStepN(o.n);
  const schedule = api.schedule();
  api.seek(schedule.arrive);
  const facts = /** @type {HTMLElement} */ (document.getElementById("facts"));
  const numeral = /** @type {HTMLElement} */ (document.getElementById("numeral-b"));
  const layers = ["facts-a", "facts-b"].map(
    (id) => /** @type {HTMLElement} */ (document.getElementById(id)),
  );
  const drawn = (/** @type {Element} */ el) => {
    const r = el.getBoundingClientRect();
    return r.width > 0 || r.height > 0;
  };
  const partsOf = (/** @type {Element | undefined} */ slot) => {
    /** @type {Element[]} */
    const out = [];
    if (slot === undefined) {
      return out;
    }
    const walk = (/** @type {Element} */ el) => {
      for (const child of el.children) {
        if (child.classList.contains("katex-mathml")) {
          continue;
        }
        if (child instanceof SVGElement || child.children.length === 0) {
          if (drawn(child)) {
            out.push(child);
          }
        } else {
          walk(child);
        }
      }
    };
    if (slot.children.length === 0) {
      if (drawn(slot) && (slot.textContent ?? "").trim() !== "") {
        out.push(slot);
      }
    } else {
      walk(slot);
    }
    return out;
  };
  const keyOf = (/** @type {Element} */ el) => {
    const r = el.getBoundingClientRect();
    const h = (/** @type {number} */ v) => Math.round(v * 2);
    const bare = /** @type {Element} */ (el.cloneNode(true));
    bare.removeAttribute("style");
    const what = el instanceof SVGElement ? bare.outerHTML : `${el.localName}:${el.textContent}`;
    return `${what}@${h(r.left)},${h(r.top)},${h(r.width)},${h(r.height)}`;
  };
  // The number a lone digit is drawn in, or null for any other part.
  const numberOf = (/** @type {Element} */ el) =>
    /^[0-9]$/.test(el.textContent ?? "")
      ? (el.parentElement?.closest(".mord")?.textContent ?? null)
      : null;
  const seen = (/** @type {Element} */ el) => {
    let value = 1;
    for (let e = /** @type {Element | null} */ (el); e && e !== facts; e = e.parentElement) {
      value *= Number(getComputedStyle(e).opacity);
    }
    return value;
  };
  const count = Math.max(layers[0].children.length, layers[1].children.length);
  const slots = [];
  for (let i = 0; i < count; i++) {
    const a = layers[0].children[i];
    const b = layers[1].children[i];
    const parts = [partsOf(a), partsOf(b)];
    slots.push({
      name: (a ?? b)?.className ?? "",
      parts,
      keys: parts.map((side) => side.map(keyOf)),
      numbers: parts.map((side) => side.map(numberOf)),
      seen: /** @type {number[][][]} */ ([]),
    });
  }
  const enter = [];
  for (const t of o.at) {
    api.seek(t);
    enter.push(Number(getComputedStyle(numeral).opacity));
    for (const slot of slots) {
      slot.seen.push(slot.parts.map((side) => side.map(seen)));
    }
  }
  api.seek(0);
  return {
    schedule,
    enter,
    slots: slots.map(({ name, keys, numbers, seen: s }) => ({ name, keys, numbers, seen: s })),
  };
};
