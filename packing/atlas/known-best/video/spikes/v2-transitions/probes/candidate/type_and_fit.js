// The census of computed font sizes of every visible text-bearing HTML element on the
// stage, and, at rest and at the settle of every pair, the visible layer's extent and
// each slot's top and height.
() => {
  const api = window.atlasTransitions;
  api.setCapture(true);
  const stage = document.getElementById("stage");
  const facts = document.getElementById("facts");
  const d = api.duration();
  const sizes = new Map();
  let svgGlyphs = 0;
  const census = () => {
    const walker = document.createTreeWalker(stage, NodeFilter.SHOW_TEXT);
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      if (!node.textContent.trim()) {
        continue;
      }
      const el = node.parentElement;
      if (!(el instanceof HTMLElement)) {
        svgGlyphs++;
        continue;
      }
      const cs = getComputedStyle(el);
      if (cs.display === "none" || cs.visibility === "hidden" || el.getClientRects().length === 0) {
        continue;
      }
      const size = parseFloat(cs.fontSize);
      if (!sizes.has(size)) {
        sizes.set(size, new Set());
      }
      sizes.get(size).add(el.id || el.className || el.tagName.toLowerCase());
    }
  };
  const SLOTS = [
    ".numeral",
    ".head-proved",
    ".side",
    ".star-line",
    ".exact",
    ".badges",
    ".head-open",
    ".open-items",
  ];
  const fits = [];
  const count = api.pairs().length;
  for (let i = 0; i < count; i++) {
    api.select(i);
    for (const [t, layer, other] of /** @type {[number, string, string][]} */ ([
      [0, "facts-a", "facts-b"],
      [d, "facts-b", "facts-a"],
    ])) {
      api.seek(t);
      census();
      const root = document.getElementById(layer);
      let bottom = 0,
        right = 0;
      const walker = document.createTreeWalker(facts, NodeFilter.SHOW_TEXT);
      for (let node = walker.nextNode(); node; node = walker.nextNode()) {
        if (!node.textContent.trim()) {
          continue;
        }
        const el = node.parentElement;
        if (el.closest(`#${other}`)) {
          continue;
        }
        const r = el.getBoundingClientRect();
        if (r.width === 0) {
          continue;
        }
        bottom = Math.max(bottom, r.bottom);
        right = Math.max(right, r.right);
      }
      root.querySelectorAll("svg").forEach((s) => {
        const r = s.getBoundingClientRect();
        bottom = Math.max(bottom, r.bottom);
        right = Math.max(right, r.right);
      });
      const slots = SLOTS.map((sel) => {
        const r = root.querySelector(sel).getBoundingClientRect();
        return [sel, Math.round(r.top * 100) / 100, Math.round(r.height * 100) / 100];
      });
      // The headline: the numeral against the `n =` line it shares a row with. Read
      // through `offset*` rather than `getBoundingClientRect`, because the numeral
      // carries the roll's transform and a client rect would measure that instead of
      // the layout. The line is constant and lives OUTSIDE both fading layers, so it
      // is found on the document rather than in `root`.
      const numeralEl = /** @type {HTMLElement} */ (root.querySelector(".numeral"));
      const nlineEl = /** @type {HTMLElement} */ (document.querySelector(".nline"));
      fits.push({
        n: api.state().n + (t > 0 ? 1 : 0),
        t,
        bottom,
        right,
        slots,
        numeralLeft: numeralEl.offsetLeft,
        numeralTop: numeralEl.offsetTop,
        nlineRight: nlineEl.offsetLeft + nlineEl.offsetWidth,
        nlineTop: nlineEl.offsetTop,
      });
    }
  }
  // Revision 12 held the panel clear of the position bar along the bottom of the stage.
  // Revision 16 removed that bar entirely -- the owner found it distracting -- so the
  // clearance is now to the stage's own foot, and the two numbers the callers read are the
  // stage's bottom rather than the bar's top.
  const stageBox = document.getElementById("stage").getBoundingClientRect();
  const barTop = stageBox.bottom;
  const pnTop = stageBox.bottom;
  const box = facts.getBoundingClientRect();
  return {
    sizes: Array.from(sizes, ([s, k]) => [s, Array.from(k).sort()]).sort((a, b) => a[0] - b[0]),
    svgGlyphs,
    fits,
    pnTop,
    barTop,
    factsLeft: box.left,
    factsRight: box.right,
  };
};
