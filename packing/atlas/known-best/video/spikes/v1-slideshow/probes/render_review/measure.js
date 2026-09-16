// The facts panel's layout at the instant on the stage, and the type every text-bearing element
// on the stage resolves to: what `render_review.check` holds to the stage budget for every n.
() => {
  const facts = /** @type {Element} */ (document.querySelector("#facts .facts"));
  const r = facts.getBoundingClientRect();
  let right = 0,
    bottom = 0;
  facts.querySelectorAll("*").forEach((el) => {
    // The drawn radical's <use> reports the geometry of its 400000-unit path, not
    // the clipped box it is drawn in; the box itself (the svg element) is measured.
    if (el.closest("svg") && el.tagName.toLowerCase() !== "svg") {
      return;
    }
    const b = el.getBoundingClientRect();
    if (b.width === 0 && b.height === 0) {
      return;
    }
    if (b.right > right) {
      right = b.right;
    }
    if (b.bottom > bottom) {
      bottom = b.bottom;
    }
  });
  // How far the deepest ink of a value line reaches into the note line under it:
  // positive means the two overlap. The note's cap top sits about 6px below the
  // top of its 30px line; the radical box and the fraction box are measured as
  // boxes, which is where their ink ends.
  let intrusion = -999;
  facts.querySelectorAll(".line").forEach((line) => {
    const sub = line.nextElementSibling;
    if (!sub?.classList.contains("sub") || !sub.textContent) {
      return;
    }
    let deepest = line.getBoundingClientRect().top;
    line.querySelectorAll("*").forEach((el) => {
      if (el.closest("svg") && el.tagName.toLowerCase() !== "svg") {
        return;
      }
      const b = el.getBoundingClientRect();
      if (b.height && b.bottom > deepest) {
        deepest = b.bottom;
      }
    });
    const d = deepest - (sub.getBoundingClientRect().top + 6);
    if (d > intrusion) {
      intrusion = d;
    }
  });
  // The exact line's baseline, via its equals sign, when the line is not empty.
  const eq = facts.querySelector(".line.exact .eqsign");
  const eqTop = eq ? eq.getBoundingClientRect().top : null;
  // The lower-bound line's top, which must not depend on the order of the exact
  // slot and the degree note above it; and the degree note's seat: the value line
  // directly above it and its distance from that line's bottom (0, or the 5px a
  // nested radical's line is lifted by).
  const exact = /** @type {Element} */ (facts.querySelector(".line.exact"));
  const lowerTop = /** @type {Element} */ (
    facts.querySelector(".line.lower")
  ).getBoundingClientRect().top;
  const degree = facts.querySelector(".sub .degree");
  let degreeUnder = null,
    degreeGap = null;
  if (degree) {
    const sub = /** @type {HTMLElement} */ (degree.parentElement);
    const above = /** @type {Element} */ (sub.previousElementSibling);
    degreeUnder = above.classList.contains("side")
      ? "side"
      : above.classList.contains("exact")
        ? "exact"
        : above.className;
    degreeGap = sub.getBoundingClientRect().top - above.getBoundingClientRect().bottom;
  }
  // Every element on the stage that directly holds text: its computed size, and
  // its computed family and weight (the first family of the stack is the one the
  // rule asks for; PT Serif is embedded at 400 only, so any other weight on a
  // serif element would be synthesised).
  /** @type {Set<number>} */
  const sizes = new Set();
  /** @type {Set<string>} */
  const serifWeights = new Set();
  /** @type {Set<string>} */
  const weights = new Set();
  document.querySelectorAll("#stage *").forEach((el) => {
    for (const node of el.childNodes) {
      if (node.nodeType === 3 && /** @type {string} */ (node.textContent).trim()) {
        const cs = getComputedStyle(el);
        sizes.add(parseFloat(cs.fontSize));
        const family = /** @type {string} */ (cs.fontFamily.split(",")[0]).replace(/"/g, "").trim();
        weights.add(`${family} ${cs.fontWeight}`);
        if (family === "PT Serif") {
          serifWeights.add(cs.fontWeight);
        }
        break;
      }
    }
  });
  // The faces the document declares, whatever their load state.
  /** @type {string[]} */
  const faces = [];
  document.fonts.forEach((f) => {
    faces.push(`${f.family.replace(/"/g, "")}|${f.style}|${f.weight}`);
  });
  const footer = /** @type {Element} */ (document.querySelector(".stage-footer"));
  const spans = footer.querySelectorAll(":scope > span");
  const fb = footer.getBoundingClientRect();
  return {
    intrusion,
    eqTop,
    lowerTop,
    degreeUnder,
    degreeGap,
    exactEmpty: exact.classList.contains("empty"),
    exactTall: exact.classList.contains("tall"),
    serifWeights: Array.from(serifWeights).sort(),
    weights: Array.from(weights).sort(),
    faces: faces.sort(),
    top: r.top,
    bottom: Math.max(r.bottom, bottom),
    right: Math.max(r.right, right),
    badges: facts.querySelectorAll(".status .badge").length,
    open: facts.querySelectorAll(".open li").length,
    record: facts.querySelectorAll(".record div").length,
    recordHeight: /** @type {Element} */ (facts.querySelector(".record")).getBoundingClientRect()
      .height,
    fill: /** @type {HTMLElement} */ (document.getElementById("progress-fill")).style.width,
    cursor: /** @type {HTMLElement} */ (document.getElementById("progress-cursor")).textContent,
    cursorGap: (() => {
      const c = /** @type {HTMLElement} */ (
        document.getElementById("progress-cursor")
      ).getBoundingClientRect();
      const lo = /** @type {Element} */ (
        document.querySelector("#progress .end.lo")
      ).getBoundingClientRect();
      const hi = /** @type {Element} */ (
        document.querySelector("#progress .end.hi")
      ).getBoundingClientRect();
      return Math.min(c.left - lo.right, hi.left - c.right);
    })(),
    sizes: Array.from(sizes).sort((a, b) => a - b),
    footerTop: fb.top,
    footerGap:
      spans.length === 2
        ? /** @type {Element} */ (spans[1]).getBoundingClientRect().left -
          /** @type {Element} */ (spans[0]).getBoundingClientRect().right
        : null,
    footerOverflow: footer.scrollWidth - footer.clientWidth,
    barTop: /** @type {HTMLElement} */ (document.getElementById("progress")).getBoundingClientRect()
      .top,
    trackTop: /** @type {Element} */ (
      document.querySelector("#progress .track")
    ).getBoundingClientRect().top,
  };
};
