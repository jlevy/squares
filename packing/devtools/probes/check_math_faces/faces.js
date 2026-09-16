// The walk. Returns `{ nodes, marked, tables, bold_advances, findings }` for the medium the
// page is in.
//
// The face of the WORDS around an expression is read off the nearest ancestor that is not
// part of the math markup. kpress's `.kpress-math` and `.kpress-math-render` wrappers
// declare the prose face themselves, and `.katex` is where `katex-text-face.css` puts the
// composite, so asking any of those would answer with the choice already made rather than
// with the sentence the formula sits in.
//
// Sans or prose is decided by comparing that container's computed `font-family` against
// both of the tokens in scope on it, `--kpress-font-sans` and `--kpress-font-prose`. Both
// sides come from the same medium's computed values, so the test reads the print stack
// under print and the screen stack on screen without naming either, and a container that
// matches neither is reported rather than guessed at.
//
// The re-typeset comparison recovers each expression's own TeX from the annotation KaTeX
// writes into its MathML copy, so it needs no source of its own and covers whatever the
// page happens to contain. The probe span is appended to the same container, so it
// inherits the same font stack and the same size, and it is removed again; nothing here
// leaves a mark on the page beyond the marks the page itself made.
//
// `wrappers` is the renderer's list of math wrapper selectors, `math` is
// `math/library.js`'s helpers, and `fontAdvance` is `font_advance.js`'s measurement.
/**
 * @param {{
 *   wrappers: string,
 *   advance_tolerance: number,
 *   math: SquaresMathProbes,
 *   fontAdvance: (element: Element) => number,
 * }} o
 */
({ wrappers, advance_tolerance, math, fontAdvance }) => {
  /** @type {string[]} */
  const findings = [];
  /** @type {string[]} */
  const boldAdvances = [];
  const { activeVariant } = math;
  const nodes = [...document.querySelectorAll(".katex")].filter(activeVariant);
  /** @param {Element} node */
  const sans = (node) => !!node.closest('[data-kpress-math-face="sans"]');
  const marked = nodes.filter(sans);
  /** @param {string | null | undefined} value */
  const first = (value) =>
    /** @type {string} */ ((value || "").split(",")[0]).trim().replace(/^["']|["']$/g, "");

  /** @param {Element} node */
  const container = (node) => {
    let el = node.parentElement;
    while (el?.matches(wrappers)) {
      el = el.parentElement;
    }
    return el;
  };
  /** @param {Element} el */
  const where = (el) => {
    const parts = [];
    for (
      let e = /** @type {Element | null} */ (el);
      e && e !== document.body;
      e = e.parentElement
    ) {
      const cls =
        typeof e.className === "string" && e.className.trim()
          ? `.${e.className.trim().split(/\s+/).join(".")}`
          : "";
      parts.unshift(e.tagName.toLowerCase() + cls);
      if (parts.length > 3) {
        break;
      }
    }
    return parts.join(" > ");
  };

  const seam = globalThis.kpressMathText;
  if (!seam || typeof seam.installTablesFor !== "function") {
    findings.push("the page installed no math text seam; its init did not run");
    return {
      nodes: nodes.length,
      marked: marked.length,
      tables: [],
      bold_advances: boldAdvances,
      findings,
    };
  }
  if (nodes.length === 0) {
    findings.push("the page rendered no mathematics at all");
  }

  for (const node of nodes) {
    const words = container(node);
    if (!words) {
      continue;
    }
    const style = getComputedStyle(words);
    const drawn = first(style.fontFamily);
    const isSans = drawn === first(style.getPropertyValue("--kpress-font-sans"));
    const isProse = drawn === first(style.getPropertyValue("--kpress-font-prose"));
    const at = `${where(node)} [${drawn}]`;
    if (!isSans && !isProse) {
      findings.push(`mathematics in words set in neither the sans nor the prose: ${at}`);
    } else if (isSans && !sans(node)) {
      findings.push(`sans words, serif mathematics: ${at}`);
    } else if (isProse && !isSans && sans(node)) {
      findings.push(`serif words, sans mathematics: ${at}`);
    }
  }

  /* Read the emitted declarations, not the renderer's pruning table: a saved sans
     preference moves prose's bold mathematics into this family too. CSS can synthesize
     a missing bold slot without reporting a font load failure, but the resulting glyphs
     no longer match KaTeX's 650 metrics. `.textbf` requests upstream's 700, which CSS
     matches to the composite's pinned 650 slot. */
  const sansSlots = new Set(
    [...document.fonts]
      .filter((face) => first(face.family) === "KPress Math Text Sans")
      .map((face) => `${face.style} ${face.weight}`),
  );
  for (const node of marked) {
    for (const run of node.querySelectorAll(".mathbf, .boldsymbol, .textbf")) {
      const style = getComputedStyle(run);
      const slot = `${style.fontStyle} 650`;
      if (!sansSlots.has(slot)) {
        findings.push(`sans mathematics requests an undeclared ${slot} slot: ${where(run)}`);
      }
      /* A declared family alone cannot tell a real 650 instance from synthetic bold.
         Compare its resolved face with the 650 advance in KPress's table. The enlarged
         sample preserves the distinction when small glyphs are snapped to whole pixels. */
      const text = /** @type {string} */ (run.textContent);
      if (
        style.fontStyle === "normal" &&
        /^[A-Za-z]$/.test(text) &&
        run.checkVisibility({ visibilityProperty: true })
      ) {
        const table = globalThis.kpressKatexTextMetrics?.sans?.["Main-Bold"];
        const metric = table?.[/** @type {number} */ (text.codePointAt(0))];
        if (!metric) {
          findings.push(`no 650 metric for sans bold ${text}`);
          continue;
        }
        const actual = fontAdvance(run);
        const expected = metric[4];
        boldAdvances.push(`${text}: ${actual}em | 650: ${expected}em`);
        if (Math.abs(actual - /** @type {number} */ (expected)) > advance_tolerance) {
          findings.push(
            `sans bold glyph does not match its 650 metrics: ${text} draws ${actual}em, expected ${expected}em`,
          );
        }
      }
    }
  }

  /* One expression of each kind, re-typeset from its own source under both sets. */
  /** @type {string[]} */
  const tables = [];
  /** @param {Element} node */
  const source = (node) => {
    const tex = node.querySelector('annotation[encoding="application/x-tex"]');
    return tex ? tex.textContent : null;
  };
  /** @param {Element} el */
  const geometry = (el) =>
    [.../** @type {NodeListOf<HTMLElement>} */ (el.querySelectorAll(".vlist"))]
      .map((v) => v.style.height)
      .join("|");
  /**
   * @param {Element} node
   * @param {Element} host
   */
  const under = (node, host) => {
    const probe = document.createElement("span");
    probe.style.position = "absolute";
    probe.style.visibility = "hidden";
    /** @type {Element} */ (container(node)).appendChild(probe);
    /* The seam picks the set from the element it is handed, so it is handed one that
       lives where the set under test does; `probe` then only has to be somewhere the
       size and the stack are the node's own. */
    seam.installTablesFor(host, globalThis.squaresMath?.context);
    try {
      katex.render(/** @type {string} */ (source(node)), probe, {
        throwOnError: false,
        displayMode: !!node.closest(".katex-display"),
      });
    } catch (_error) {
      probe.textContent = "";
    }
    const measured = geometry(probe);
    probe.remove();
    return measured;
  };

  /* Detached control hosts select either table without inheriting the reader's global
     preference. The measured formula itself stays attached under its actual cascade. */
  const sansHost = document.createElement("span");
  sansHost.className = "sans-text";
  const proseHost = document.createElement("span");
  /** @type {[string, Element[]][]} */
  const contexts = [
    ["supporting", marked.filter((node) => !node.closest(".kpress-prose > p"))],
    ["prose", nodes.filter((node) => node.closest(".kpress-prose > p"))],
  ];
  for (const [label, pool] of contexts) {
    const node = pool.find((n) => n.querySelector(".vlist") && source(n));
    if (!node) {
      findings.push(`no ${label} fraction to check the metric table on`);
      continue;
    }
    const live = geometry(node);
    const asSans = under(node, sansHost);
    const asProse = under(node, proseHost);
    tables.push(`${label}: live ${live} | sans ${asSans} | prose ${asProse}`);
    if (asSans === asProse) {
      findings.push(
        `${label}: the two metric sets lay this expression out identically, ` +
          "so the comparison proves nothing",
      );
    } else if (live !== (sans(node) ? asSans : asProse)) {
      findings.push(
        `${label}: laid out from the wrong metric table -- live ${live}, sans ${asSans}, prose ${asProse}`,
      );
    }
  }
  seam.restore();

  /* Only the glyphs an exposed formula uses must be ready. Unused registered
     styles may remain unloaded; demanding them would restore the startup barrier. */
  const paint = globalThis.__mathFirstPaint;
  if (!paint) {
    findings.push("nothing recorded the first mathematics node; the init script did not run");
  } else {
    if (!Array.isArray(paint.required) || !paint.required.length) {
      findings.push("first mathematics paint has no required-glyph observations");
    }
    const late = (paint.required || [])
      .filter((face) => !face.ready)
      .map((face) => `${face.spec} [${face.text}]`);
    if (late.length) {
      findings.push(
        `mathematics was painted before ${late.length} of its faces: ${late.join(", ")}`,
      );
    }
  }
  const loading = globalThis.__mathLoadingState;
  if (!loading || !(loading.mathFontChecks > 0)) {
    findings.push("no first-visible-frame glyph font checks ran");
  }
  for (const failure of loading?.unreadyMath || []) {
    findings.push(`a formula appeared before its required glyph fonts: ${failure}`);
  }
  return {
    nodes: nodes.length,
    marked: marked.length,
    tables,
    bold_advances: boldAdvances,
    findings,
  };
};
