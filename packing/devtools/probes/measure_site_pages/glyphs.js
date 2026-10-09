// How a page's glyphs are drawn, role by role: every property that decides what a reader
// sees of a run of text or a formula, read from the laid-out page.
//
// `text` is one row for each distinct setting of each role (prose, a heading, a caption,
// a table cell, a footnote, a chip, a link of the bar, and as `other` every run no role
// names, by the element and component that hold it): the face asked for, weight, size,
// line height, style, colour and effective opacity, and the properties that change how a
// face is rasterised, `text-rendering`, `-webkit-font-smoothing`, `font-synthesis`,
// `font-optical-sizing`, `font-variation-settings` and `font-feature-settings`; with how
// many elements of the role are set that way.
//
// `math` is one row for each distinct setting of the formulas on each surface, inline
// and display apart: how it is typeset (KaTeX's HTML, with or without its MathML), the
// face of the formula and of its letters, weight, colour and whether that is the text's
// own, the same rasterisation properties, and `scale`, the formula's font size over the
// size of the text it sits in. A formula whose TeX is one of `tex` is a row of its own,
// so the same formula can be compared on two pages.
//
// `faces` is every face the document declares (`document.fonts`): family, weight, style,
// `font-display`, whether its bytes are inlined or a file of the site's shared assets,
// and whether it loaded. `root` is what
// the page stamped on `<html>`, `katex` its checked running or prepared renderer,
// `prepared_katex` the build-time version record, `publication` whether it
// carries the papers' publication layer, `reading` whether it has a reading column at
// all (the workbench and a result overview opened alone have none), `sans` and `prose`
// the faces that lead the two text stacks, and `tokens` what the shared text tokens come
// to under the reading column, as numbers.
//
// The first element of each row is marked with `mark`, so the caller can ask the browser
// which platform face drew it and shoot it. A formula's `glyphs` are the faces its runs
// ask for, and the first run of each is marked as well (`parts`), since the browser
// answers for an element's own text only.
(/** @type {{wrappers: string, mark: string, tex?: string[]}} */ options) => {
  const { wrappers, mark } = options;
  const wanted = new Set(options.tex ?? []);
  /** @param {string} family */
  const faceName = (family) => family.trim().replace(/^["']|["']$/g, "");
  /** @param {string} family */
  const first = (family) => faceName(family.split(",")[0] ?? "");
  /** @param {number} value */
  const round = (value) => Math.round(value * 1000) / 1000;
  const canvas = document.createElement("canvas");
  canvas.width = 1;
  canvas.height = 1;
  const context = canvas.getContext("2d", { willReadFrequently: true });
  /**
   * A CSS colour as the sRGB bytes it paints, whatever space it was written in.
   * @param {string} color
   */
  const rgb = (color) => {
    if (!context) {
      return color;
    }
    context.clearRect(0, 0, 1, 1);
    context.fillStyle = "#000";
    context.fillStyle = color;
    context.fillRect(0, 0, 1, 1);
    const [red, green, blue, alpha] = context.getImageData(0, 0, 1, 1).data;
    return `rgb(${red} ${green} ${blue}${alpha === 255 ? "" : ` / ${round((alpha ?? 0) / 255)}`})`;
  };
  /** @param {Element} el */
  const opacity = (el) => {
    let value = 1;
    for (let at = /** @type {Element | null} */ (el); at; at = at.parentElement) {
      value *= Number.parseFloat(getComputedStyle(at).opacity);
    }
    return round(value);
  };
  /**
   * What decides how an element's own glyphs are drawn. A diagram's label is sized in its
   * drawing's own units and painted in its fill, so its size is the one it has on the
   * page, through the drawing's scale, and its colour its fill.
   * @param {Element} el
   */
  const drawing = (el) => {
    const style = getComputedStyle(el);
    const matrix = el instanceof SVGGraphicsElement ? el.getScreenCTM() : null;
    const scale = matrix ? Math.hypot(matrix.a, matrix.b) : 1;
    return {
      family: first(style.fontFamily),
      weight: style.fontWeight,
      size: Math.round(Number.parseFloat(style.fontSize) * scale * 100) / 100,
      line_height:
        style.lineHeight === "normal"
          ? "normal"
          : Math.round(Number.parseFloat(style.lineHeight) * scale * 100) / 100,
      style: style.fontStyle,
      color: rgb(matrix ? style.fill : style.color),
      opacity: opacity(el),
      text_rendering: style.textRendering,
      smoothing: style.getPropertyValue("-webkit-font-smoothing") || "auto",
      synthesis: style.getPropertyValue("font-synthesis"),
      optical_sizing: style.getPropertyValue("font-optical-sizing"),
      variation: style.getPropertyValue("font-variation-settings"),
      features: style.getPropertyValue("font-feature-settings"),
      letter_spacing: style.letterSpacing,
      transform: style.textTransform,
    };
  };
  /** @param {Element} el */
  const shown = (el) =>
    el.getClientRects().length > 0 && getComputedStyle(el).visibility !== "hidden";
  /** @param {Element} el */
  const ownText = (el) =>
    [...el.childNodes].some((node) => node.nodeType === 3 && (node.textContent ?? "").trim());
  let marks = 0;
  /**
   * @param {Element} el
   * @param {string} [part]
   */
  const stamp = (el, part) => {
    marks += 1;
    const id = `${part ?? "s"}${marks}`;
    el.setAttribute(mark, id);
    return id;
  };

  // A role is the first of these an element matches; `outside` keeps a general role, a
  // paragraph or a list item, to the reading text.
  const chrome =
    "nav, figure, figcaption, table, blockquote, details, [popover], .kpress-toc, .hero, " +
    ".site-hero, .site-card, .kpress-footnotes, .credits, .colophon, .site-colophon, " +
    ".panel, .site-ladders, .doc-links, .site-case-reader, .kpress-tooltip";
  /** @type {[string, string, string?][]} */
  const roles = [
    ["nav name", ".site-name-text"],
    ["nav link", ".site-nav a:not(.site-name)"],
    ["section tab", '.site-tabs :is(a, [role="tab"])'],
    ["source chip", ".doc-links .chip"],
    ["chip", ".site-chip"],
    ["page title", ".hero h1, .site-hero h1, .site-title"],
    ["subtitle", ".subtitle"],
    ["credits name", ".credits strong"],
    ["credits", ".credits, .credits :is(p, div, span, a, time)"],
    ["card label", ".site-card-label"],
    ["card headline", ".site-card-value"],
    ["card note", ".site-card-note"],
    ["caption lead", ":is(figcaption, .kpress-figcaption, caption) strong"],
    ["caption", "figcaption, .kpress-figcaption, caption, :is(figcaption, caption) p"],
    ["figure label", "figure svg text, figure svg tspan"],
    ["footnote", ".kpress-footnotes li, .kpress-footnotes li p"],
    ["table head", "th"],
    ["table cell", "td"],
    ["blockquote", "blockquote, blockquote p"],
    ["summary", "summary"],
    ["contents entry", ".kpress-toc a"],
    [
      "colophon",
      ".colophon, .site-colophon, .site-colophon p, " +
        ":is(.colophon, .site-colophon) :is(.site-colophon-line, .site-colophon-part)",
    ],
    ["h1", "h1"],
    ["h2", "h2"],
    ["h3", "h3"],
    ["h4", "h4"],
    ["code block", "pre code"],
    ["inline code", ":is(p, li) code", chrome],
    ["strong", ":is(p, li) strong", chrome],
    ["emphasis", ":is(p, li) em", chrome],
    ["link", ":is(p, li) a:not(.kpress-footnote-ref a, .kpress-footnote-ref)", chrome],
    ["list item", "li", chrome],
    ["prose", "p", chrome],
    // Whatever else the page shows as text, so no run goes unmeasured: named for the
    // element that holds it, a component's own class where it has one.
    ["", "body *:not(script, style, svg *)"],
  ];
  /** @type {Map<string, Record<string, unknown>>} */
  const text = new Map();
  const taken = new Set();
  for (const [named, selector, outside] of roles) {
    for (const el of document.querySelectorAll(selector)) {
      if (taken.has(el) || !shown(el) || !ownText(el) || el.closest(wrappers)) {
        continue;
      }
      if (outside && el.parentElement?.closest(outside)) {
        continue;
      }
      taken.add(el);
      const component = el.closest("[class]")?.classList[0] ?? "";
      const role = named || `other (${el.tagName.toLowerCase()} in .${component})`;
      const drawn = drawing(el);
      const key = `${role}|${JSON.stringify(drawn)}`;
      const row = text.get(key);
      if (row) {
        row.count = /** @type {number} */ (row.count) + 1;
        continue;
      }
      text.set(key, {
        role,
        ...drawn,
        count: 1,
        example: (el.textContent ?? "").trim().replace(/\s+/g, " ").slice(0, 40),
        mark: stamp(el),
      });
    }
  }

  /** @type {[string, string][]} */
  const surfaces = [
    [".site-card-value", "card headline"],
    [".site-card-note", "card note"],
    [".site-popover-value", "popover headline"],
    [".site-atlas-pop", "visual summary"],
    [".site-popover", "popover"],
    [".site-chip", "chip"],
    [".site-nav", "nav"],
    [".hero h1, .site-hero h1, .site-title", "page title"],
    [".subtitle", "subtitle"],
    ["figcaption, .kpress-figcaption, caption", "caption"],
    [".panel, .tip-panel, .mass-line", "panel"],
    [".site-case-head", "case head"],
    [".site-case-bounds", "case bounds"],
    [".site-case-data", "case detail"],
    ["summary", "summary"],
    ["details", "details"],
    ["th", "table head"],
    ["td", "table cell"],
    ["h1, h2, h3, h4, h5, h6", "heading"],
    [".kpress-footnotes", "footnote"],
    ["blockquote", "blockquote"],
    ["li", "list item"],
  ];
  /**
   * A formula's glyph runs by the face each asks for: the first element with text of its
   * own for each family, weight and style its HTML sets a glyph in.
   * @param {Element} katex
   */
  const runs = (katex) => {
    /** @type {Map<string, Element>} */
    const found = new Map();
    for (const node of katex.querySelectorAll(".katex-html *")) {
      if (!shown(node) || !ownText(node)) {
        continue;
      }
      const style = getComputedStyle(node);
      const face =
        `${first(style.fontFamily)} ${style.fontWeight}` +
        (style.fontStyle === "normal" ? "" : ` ${style.fontStyle}`);
      if (!found.has(face)) {
        found.set(face, node);
      }
    }
    return found;
  };
  /** @type {Map<string, Record<string, unknown>>} */
  const math = new Map();
  for (const katex of document.querySelectorAll(".katex")) {
    if (!shown(katex)) {
      continue;
    }
    // The text a formula sits in is the first element outside every wrapper: KaTeX's own
    // auto-render puts a bare span between the formula and kpress's box.
    let host = katex.parentElement;
    let display = false;
    while (host?.closest(`${wrappers}, .katex-display`)) {
      display ||= host.matches(".katex-display, .tex-d, .kpress-math-display");
      host = host.parentElement;
    }
    if (!host) {
      continue;
    }
    const drawn = drawing(katex);
    const around = drawing(host);
    const glyphs = runs(katex);
    // A prepared formula keeps its one semantic MathML subtree beside the visual
    // wrapper. Associate only this formula's host, never a surrounding paragraph.
    const prepared = katex.closest('[data-kpress-math-prepared="true"]');
    const semantic = prepared?.closest(".kpress-math") ?? prepared ?? katex;
    const mathml = semantic.querySelectorAll("math");
    const tex = semantic.querySelector("annotation")?.textContent ?? "";
    const setting = {
      surface: surfaces.find(([selector]) => host.closest(selector))?.[1] ?? "prose",
      layout: display ? "display" : "inline",
      typeset:
        (katex.querySelector(".katex-html") ? "KaTeX HTML" : "no HTML") +
        (mathml.length === 1 ? " + MathML" : mathml.length ? " + duplicate MathML" : ""),
      math: drawn.family,
      glyphs: [...glyphs.keys()].sort().join(" + "),
      weight: drawn.weight,
      scale: round(drawn.size / around.size),
      text: around.family,
      text_weight: around.weight,
      text_size: around.size,
      color: drawn.color,
      text_color: around.color === drawn.color ? "same" : around.color,
      opacity: drawn.opacity,
      text_rendering: drawn.text_rendering,
      text_text_rendering: around.text_rendering,
      smoothing: drawn.smoothing,
      synthesis: drawn.synthesis,
      face_mark:
        katex.closest("[data-kpress-math-face]")?.getAttribute("data-kpress-math-face") ?? "",
      prepared: prepared ? "yes" : "no",
    };
    const key = JSON.stringify(setting) + (wanted.has(tex) ? `|${tex}` : "");
    const row = math.get(key);
    if (row) {
      row.count = /** @type {number} */ (row.count) + 1;
      continue;
    }
    math.set(key, {
      ...setting,
      count: 1,
      size: drawn.size,
      example: tex.replace(/\s+/g, " ").slice(0, 40),
      compared: wanted.has(tex),
      mark: stamp(katex),
      parts: Object.fromEntries([...glyphs].map(([face, node]) => [face, stamp(node, "g")])),
    });
  }

  /** @type {Map<string, {family: string, weight: string, style: string, display: string, status: string, inlined: boolean, shared: boolean, optional_local: boolean, faces: number}>} */
  const faces = new Map();
  /** @type {Map<string, boolean>} */
  const inlined = new Map();
  // A face of the site's shared assets, as its stylesheet beside the faces names it.
  /** @type {Map<string, boolean>} */
  const shared = new Map();
  /** @type {Map<string, boolean>} */
  const optionalLocal = new Map();
  // Each metric-adjusted local alias (site.css, paper-type.css) by family, weight and
  // style, with the exact local sources it may name.
  /** @type {Map<string, string[]>} */
  const fallbackSources = new Map([
    ["Site Prose Georgia|400|normal", ["Georgia"]],
    ["Site Prose Times|400|normal", ["Times New Roman", "Liberation Serif"]],
    ["Site Sans Arial|400|normal", ["Arial", "Liberation Sans"]],
    ["Site Sans Arial|700|normal", ["Arial Bold", "Liberation Sans Bold"]],
  ]);
  for (const sheet of document.styleSheets) {
    for (const rule of sheet.cssRules) {
      if (rule instanceof CSSFontFaceRule) {
        // A rule that names no weight or style declares the normal one, which is how the
        // loaded face reports it.
        const src = rule.style.getPropertyValue("src");
        const weight = rule.style.getPropertyValue("font-weight") || "normal";
        const slant = rule.style.getPropertyValue("font-style") || "normal";
        const family = faceName(rule.style.getPropertyValue("font-family"));
        const named = `${family}|${weight}|${slant}`;
        const localSource = /local\(\s*(?:"([^"]+)"|'([^']+)'|([^()]+))\s*\)/g;
        const locals = [...src.matchAll(localSource)].map((match) =>
          (match[1] ?? match[2] ?? match[3] ?? "").trim(),
        );
        const expected = fallbackSources.get(
          `${family}|${weight === "normal" ? "400" : weight}|${slant}`,
        );
        const optional =
          expected !== undefined &&
          locals.length === expected.length &&
          locals.every((name, index) => name === expected[index]) &&
          src.replace(localSource, "").replace(/[\s,]/g, "") === "";
        // Missing optional host fallbacks do not mean a shipped font failed. Every
        // declaration of this face must contain exactly the expected local sources.
        optionalLocal.set(named, (optionalLocal.get(named) ?? true) && optional);
        inlined.set(named, (inlined.get(named) ?? true) && !/url\(\s*(?!["']?data:)/.test(src));
        shared.set(
          named,
          (shared.get(named) ?? true) && !/url\(\s*(?!["']?(?:data:|\.\.\/fonts\/))/.test(src),
        );
      }
    }
  }
  for (const face of document.fonts) {
    const family = faceName(face.family);
    const named = `${family}|${face.weight}|${face.style}`;
    const key = `${named}|${face.display}|${face.status}`;
    const row = faces.get(key);
    if (row) {
      row.faces += 1;
      continue;
    }
    faces.set(key, {
      family,
      weight: face.weight,
      style: face.style,
      display: face.display,
      status: face.status,
      inlined: inlined.get(named) ?? false,
      shared: shared.get(named) ?? false,
      optional_local: optionalLocal.get(named) ?? false,
      faces: 1,
    });
  }

  const root = document.documentElement;
  // A token's value as a number: the letter spacing of a ruler under the reading column
  // that is set to it, read back and removed, since a custom property computes to its
  // text (`calc(19 / 18)`) and not to what it comes to. Letter spacing computes to the
  // length itself, where a box's width would be capped by the column and rounded to a
  // sixty-fourth of a pixel. A length is in pixels; a token the page does not set is
  // absent.
  const scope = document.querySelector(".kpress") ?? document.body;
  const ruler = document.createElement("span");
  ruler.style.cssText = "position:absolute;visibility:hidden";
  scope.append(ruler);
  /**
   * @param {string} name
   * @param {boolean} length
   */
  const token = (name, length) => {
    ruler.style.letterSpacing = "";
    ruler.style.letterSpacing = length ? `var(${name})` : `calc(1px * var(${name}))`;
    return ruler.style.letterSpacing && getComputedStyle(scope).getPropertyValue(name).trim()
      ? Math.round(Number.parseFloat(getComputedStyle(ruler).letterSpacing) * 1e4) / 1e4
      : null;
  };
  /** @type {[string, boolean][]} */
  const names = [
    ["--kpress-font-size-base", true],
    ["--kpress-font-size-h2", true],
    ["--kpress-font-weight-sans-regular", false],
    ["--paper-font-scale-sans", false],
    ["--paper-font-weight-sans-medium", false],
    ["--paper-font-weight-sans-bold", false],
    ["--paper-title-scale", false],
    ["--paper-subtitle-scale", false],
    ["--paper-support-scale", false],
    ["--paper-note-scale", false],
    ["--paper-colophon-scale", false],
    ["--paper-heading-leading", false],
  ];
  const tokens = Object.fromEntries(names.map(([name, length]) => [name, token(name, length)]));
  ruler.remove();
  const runtime = /** @type {{katex?: {version?: string}}} */ (globalThis).katex?.version ?? "";
  const preparedVersions = [...document.head.querySelectorAll('meta[name="site-math-katex"]')].map(
    (meta) => meta.getAttribute("content") ?? "",
  );
  const preparedKatex = preparedVersions.join(" / ");
  return {
    katex: runtime || preparedKatex,
    runtime_katex: runtime,
    prepared_katex: preparedKatex,
    platform: navigator.platform,
    publication: document.querySelector(".cert-page") !== null,
    reading: document.querySelector(".kpress-prose") !== null,
    sans: first(getComputedStyle(scope).getPropertyValue("--kpress-font-sans")),
    prose: first(getComputedStyle(scope).getPropertyValue("--kpress-font-prose")),
    root: Object.fromEntries(
      [...root.attributes]
        .filter((attribute) => attribute.name.startsWith("data-"))
        .map((attribute) => [attribute.name, attribute.value]),
    ),
    tokens,
    text: [...text.values()],
    math: [...math.values()],
    faces: [...faces.values()],
  };
};
