import type { Corpus } from "../data/corpus.js";
import { createDom, requireHtml } from "./dom.ts";

/** Catalogue fact panels only render trusted, build-time mathematical markup. */
export function createFactsView(document: Document, DATA: Corpus, numeralLeft: () => number) {
  const { el, text } = createDom(document);
  const FACTS = DATA.facts;
  const METRICS = DATA.metrics;
  const BADGE_LABELS: Record<string, string> = {
    "O/solid": "optimal",
    "=/solid": "exact",
    "≈/muted": "numerical",
    "R/solid": "rigid",
    "R/muted": "rigid (catalogue)",
  };
  const STAR_LABEL = "new lower bound";
  const OPEN_LABELS: Record<string, string> = {
    optimality: "optimality",
    "exact value": "exact value",
    rigidity: "rigidity",
  };
  function glyphBaseline(glyph: string) {
    const b = METRICS.badge_baseline;
    return /[A-Za-z]/.test(glyph) ? b.letter : glyph === "?" ? b.query : b.math;
  }
  function approxPath() {
    const a = METRICS.approx;
    const k = a.font_size / 1000;
    const baseline = 9.5 + ((a.y0 + a.y1) / 2) * k;
    const tx = 9.5 - (a.advance * k) / 2;
    return el("path", {
      d: a.d,
      class: "glyph-path",
      "stroke-width": String(a.stroke_units),
      transform:
        "translate(" +
        tx.toFixed(3) +
        " " +
        baseline.toFixed(3) +
        ") scale(" +
        k.toFixed(4) +
        " -" +
        k.toFixed(4) +
        ")",
    });
  }
  function badgeSvg(glyph: string, style: string) {
    const s = el("svg", {
      viewBox: "-1 -1 21 21",
      class: `badge badge-${style}`,
      "aria-hidden": "true",
    });
    if (style === "star") {
      const k = (19 * METRICS.star_span) / (2 * METRICS.star_inset);
      const pts = DATA.star_points
        .map((p) => `${(9.5 + p[0] * k).toFixed(3)},${(9.5 + p[1] * k).toFixed(3)}`)
        .join(" ");
      s.appendChild(el("polygon", { points: pts, class: "star" }));
      return s;
    }
    s.appendChild(
      el("rect", { x: "0", y: "0", width: "19", height: "19", rx: "4.5", class: "box" }),
    );
    if (glyph === "≈") {
      s.appendChild(approxPath());
    } else {
      const t = el("text", {
        x: "9.5",
        y: String(glyphBaseline(glyph)),
        "text-anchor": "middle",
        class: "glyph",
      });
      t.textContent = glyph;
      s.appendChild(t);
    }
    return s;
  }
  function badgeItem(cls: string, glyph: string, style: string, label: string) {
    const item = text("span", cls);
    item.appendChild(badgeSvg(glyph, style));
    item.appendChild(text("span", "label", label));
    return item;
  }

  // **A typeset number is split into one span per character.** KaTeX sets a number as one span
  // (`4.67553`, `17`), and the handover holds a part only where the n and n + 1 layers draw it
  // identically, so a digit the two numbers share -- the `1` of 12 and 13 -- crossfaded with
  // itself and lightened mid-roll, against the owner's request that unchanged text never fade
  // out and back. Split, each character is a part of its own. The spans carry no class and no
  // style, so the line is drawn as before; only KaTeX's visible HTML is split, not its MathML.
  function splitNumerals(root: HTMLElement) {
    for (const leaf of root.querySelectorAll(".katex-html .mord")) {
      const digits = leaf.textContent ?? "";
      if (leaf.children.length > 0 || digits.length < 2 || !/[0-9]/.test(digits)) {
        continue;
      }
      leaf.textContent = "";
      for (const character of digits) {
        const span = document.createElement("span");
        span.textContent = character;
        leaf.appendChild(span);
      }
    }
  }

  function buildFacts(layer: HTMLElement, n: number) {
    const f = FACTS[String(n)];
    if (f === undefined) {
      throw new RangeError(`no catalogue facts for n = ${n}`);
    }
    layer.textContent = "";
    // The headline under the packing: `n = 26` is an equation, so it is set as one, the `=`
    // included. It belongs to the picture rather than to the panel, but it rolls with the layer
    // whose facts it names, so it is built here and placed in that layer's headline slot. Each
    // rolling slot draws only the number; a third, still slot draws `n =` and never fades (see
    // `buildPair` and the stylesheet), because a step changes the number and nothing else.
    const numeral = text("div", "numeral");
    numeral.style.left = `${numeralLeft()}px`;
    if (f.html_headline) {
      numeral.innerHTML = f.html_headline;
    } else {
      numeral.appendChild(text("span", "n-val", String(n)));
    }
    const slot = requireHtml(document, layer.id === "facts-a" ? "numeral-a" : "numeral-b");
    slot.textContent = "";
    slot.appendChild(numeral);
    // **The mathematics is set by KaTeX, at build time.** It used to be assembled here from four
    // spans -- an italic `s`, an upright `(n)`, a relation glyph borrowed from a KaTeX face, and a
    // value in tabular figures -- which is an imitation of typesetting rather than typesetting: no
    // real spacing around the relation, no maths italic, and a closed form's fraction written with
    // a solidus because a vinculum was out of reach. The build now renders each line once through
    // the same KaTeX the explainer sets its paper with, so `s(11) <= 3.877084` is set here the way
    // it is set there. See `katex_html` in build_candidate.py for why that happens at build time.
    function mathLine(cls: string, html: string | null) {
      const line = text("div", cls);
      if (html) {
        line.innerHTML = html;
        splitNumerals(line);
      }
      return line;
    }
    // PROVED, in the order a reader wants it: the chained bound on the side, the scarlet note when
    // its lower bound was first proved here, and the badges. Both bounds are proved facts -- a
    // construction proves its upper bound -- so both belong here, and OPEN below carries the
    // questions.
    layer.appendChild(text("div", "section-head head-proved", "Proven"));
    // The bound is one chained statement now, so it is one row. The star sits to the LEFT of
    // the lower bound it marks, inside a slot that is always the star's width whether or not
    // there is a star in it -- otherwise the whole inequality would step sideways at every n
    // that has one, which during a sweep is a line that jitters rather than rolls.
    const bound = mathLine("side", f.html_side);
    const starSlot = text("span", "bound-star");
    if (f.star) {
      starSlot.appendChild(badgeSvg("", "star"));
    }
    bound.insertBefore(starSlot, bound.firstChild);
    layer.appendChild(bound);
    const starLine = text("div", "star-line");
    if (f.star) {
      starLine.appendChild(text("span", "note", STAR_LABEL));
    }
    layer.appendChild(starLine);
    // No closed-form line. It sat under a chain of two bounds and did not say which bound it was
    // the value of -- 108 of the 110 n that had one show `lower <= s(n) <= upper` -- so the owner
    // asked for it to go. The data keeps `html_exact` and `degree` for a design that attaches a
    // form to the bound it belongs to.
    const badges = text("div", "badges");
    for (const b of f.badges) {
      const label = BADGE_LABELS[`${b.glyph}/${b.style}`];
      if (label === undefined) {
        throw new Error(`unknown badge ${b.glyph}/${b.style} for n = ${n}`);
      }
      badges.appendChild(badgeItem("badge-item", b.glyph, b.style, label));
    }
    layer.appendChild(badges);
    // OPEN, always headed even when nothing is open, so the pair of headings is the panel's
    // shape rather than something that appears for some n and not others.
    layer.appendChild(text("div", "section-head head-open", "Open"));
    const items = text("div", "open-items");
    if (f.open.length === 0) {
      items.appendChild(text("span", "open-none", "none"));
    } else {
      for (const key of f.open) {
        items.appendChild(badgeItem("open-item", "?", "query", OPEN_LABELS[key] || key));
      }
    }
    layer.appendChild(items);
    return numeral;
  }
  return { buildFacts };
}
