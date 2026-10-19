// `preview_site/math_face.js` over a stand-in page: a formula in each face inside serif
// prose, sans text, and a headline. A headline's words are sans, and its math follows
// them unless the headline is mathematics standing alone, which is serif by design
// (paper-design.md, Math).
import assert from "node:assert/strict";
import { afterEach, test } from "node:test";
import { probe } from "../probe.mjs";

const SANS = '"Source Sans 3 Variable", sans-serif';
const SERIF = '"Source Serif 4 Variable", serif';
const FACE = { serif: '"KPress Math Text", serif', sans: '"KPress Math Text Sans", sans-serif' };

/** The stand-in for the page's `Element`, which the probe tests child nodes against. */
class Element {
  /**
   * @param {string} classes
   * @param {Record<string, string>} [attributes]
   */
  constructor(classes, attributes = {}) {
    this.classes = classes.split(" ");
    this.attributes = attributes;
    this.textContent = "";
  }

  /** @param {string} name */
  getAttribute(name) {
    return this.attributes[name] ?? null;
  }

  /** @param {string} selector */
  matches(selector) {
    return selector.split(",").some((one) => this.classes.includes(one.trim().slice(1)));
  }
}

/**
 * A typeset formula in `face` whose host is set in `family`: a paragraph of prose, or a
 * popover's headline holding the formula alone or after `words`.
 * @param {keyof typeof FACE | "stock"} face
 * @param {string} family
 * @param {{ headline?: boolean, words?: string, id?: string }} [options]
 */
function formula(face, family, { headline = false, words = "", id = "host" } = {}) {
  const katex = { fontFamily: face === "stock" ? "KaTeX_Main" : FACE[face] };
  const math = new Element("kpress-math");
  const className = headline ? "site-popover-value" : "prose";
  const host = Object.assign(new Element(className), {
    fontFamily: family,
    tagName: "P",
    className,
    childNodes: words ? [{ textContent: words }, math] : [math],
    /** @param {string} selector */
    closest: (selector) => {
      assert.equal(selector, "[id]");
      return { id };
    },
  });
  return Object.assign(math, {
    parentElement: host,
    /** @param {string} selector */
    querySelector: (selector) => (selector === ".katex" ? katex : { textContent: `tex of ${id}` }),
  });
}

/**
 * An explicitly marked frontier cell with a real MathML root and a visible token.
 * @param {string} family
 * @param {{ id?: string, tokenFamily?: string, visibility?: string, missing?: boolean, insideTable?: boolean }} [options]
 */
function nativeFormula(
  family,
  {
    id = "frontier-cell",
    tokenFamily = family,
    visibility = "visible",
    missing = false,
    insideTable = true,
  } = {},
) {
  const token = {
    namespaceURI: "http://www.w3.org/1998/Math/MathML",
    localName: "mn",
    textContent: "31",
    fontFamily: tokenFamily,
    visibility,
    getBoundingClientRect: () => ({ width: 12, height: 18 }),
  };
  const root = {
    namespaceURI: "http://www.w3.org/1998/Math/MathML",
    localName: "math",
    /** @param {string} selector */
    querySelectorAll: (selector) => {
      assert.equal(selector, "mi, mn, mtext, ms");
      return missing ? [] : [token];
    },
  };
  const host = Object.assign(new Element("frontier-value"), { fontFamily: family });
  return Object.assign(new Element("kpress-math", { "data-site-native-math": "frontier" }), {
    parentElement: host,
    children: [root],
    /** @param {string} selector */
    closest: (selector) => {
      if (selector === "[id]") {
        return { id };
      }
      assert.equal(selector, ".site-frontier td");
      return insideTable ? host : null;
    },
  });
}

/**
 * What the probe reports for a page of these formulas.
 * @param {(ReturnType<typeof formula> | ReturnType<typeof nativeFormula>)[]} formulas
 * @returns {string[]}
 */
function report(formulas) {
  const root = {};
  Object.assign(globalThis, {
    Element,
    document: { documentElement: root, querySelectorAll: () => formulas },
    /** @param {{ fontFamily?: string, visibility?: string }} element */
    getComputedStyle: (element) => ({
      fontFamily: element.fontFamily ?? "",
      visibility: element.visibility ?? "visible",
      getPropertyValue: () => (element === root ? SANS : ""),
    }),
  });
  return /** @type {() => string[]} */ (probe("devtools/probes/preview_site/math_face.js"))();
}

afterEach(() => {
  Reflect.deleteProperty(globalThis, "Element");
  Reflect.deleteProperty(globalThis, "document");
  Reflect.deleteProperty(globalThis, "getComputedStyle");
});

void test("math in the face of its text is not reported, nor is stock KaTeX", () => {
  assert.deepEqual(
    report([formula("serif", SERIF), formula("sans", SANS), formula("stock", SANS)]),
    [],
  );
});

void test("math in the other face from its text is reported", () => {
  assert.deepEqual(report([formula("serif", SANS, { id: "a" }), formula("sans", SERIF)]), [
    "serif math in sans text: p.prose in #a: tex of a",
    "sans math in serif text: p.prose in #host: tex of host",
  ]);
});

void test("a headline that is all math expects serif math though its own face is sans", () => {
  assert.deepEqual(report([formula("serif", SANS, { headline: true })]), []);
  assert.deepEqual(report([formula("sans", SANS, { headline: true, id: "pop" })]), [
    "sans math in a headline that is all math: p.site-popover-value in #pop: tex of pop",
  ]);
});

void test("a headline with words expects its math in their sans face", () => {
  assert.deepEqual(report([formula("sans", SANS, { headline: true, words: "Earlier " })]), []);
  assert.deepEqual(
    report([formula("serif", SANS, { headline: true, words: "Earlier ", id: "pop" })]),
    ["serif math in sans text: p.site-popover-value in #pop: tex of pop"],
  );
});

void test("native frontier math uses its actual visible token face in custom and system text", () => {
  assert.deepEqual(report([nativeFormula(SANS), nativeFormula("Arial, sans-serif")]), []);
});

void test("native frontier math in the wrong actual token face is reported", () => {
  assert.deepEqual(report([nativeFormula(SANS, { tokenFamily: SERIF, id: "row-11" })]), [
    "native frontier math differs from surrounding text in #row-11",
  ]);
});

void test("native frontier math needs a visible token inside a frontier table cell", () => {
  for (const options of [{ missing: true }, { visibility: "hidden" }, { insideTable: false }]) {
    assert.deepEqual(report([nativeFormula(SANS, options)]), [
      "native frontier math has no visible mathematical token",
    ]);
  }
});
