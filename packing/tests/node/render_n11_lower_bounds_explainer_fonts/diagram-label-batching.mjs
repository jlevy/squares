// The shipped label script must read every diagram before its first style mutation.
// The stand-ins refuse a read after any write and retain the publication scaling cases.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { runInNewContext } from "node:vm";

const [sourcePath] = /** @type {[string]} */ (process.argv.slice(2));
const source = readFileSync(sourcePath, "utf8");
let writing = false;
const read = () => assert.equal(writing, false, "geometry read after a label mutation");

/** @param {number} width @param {number} fit @param {number | null} scale
 * @param {number} support @param {number | null} note */
function diagram(width, fit, scale, support, note) {
  const parent = { fontSize: support };
  const caption = note === null ? null : { fontSize: note };
  /** @type {Map<string, string>} */
  const values = new Map();
  return {
    width,
    fit,
    scale,
    parentElement: parent,
    caption,
    values,
    getBoundingClientRect() {
      read();
      return { width: this.width };
    },
    getScreenCTM() {
      read();
      return this.scale === null ? null : { c: 0, d: this.scale };
    },
    closest() {
      return { querySelector: () => caption };
    },
    style: {
      /** @param {string} name @param {string} value */
      setProperty(name, value) {
        writing = true;
        values.set(name, value);
      },
    },
  };
}
const first = diagram(400, 800, 0.5, 17, 15.6);
const second = diagram(900, 800, 0.75, 20, null);
const diagrams = [
  first,
  second,
  diagram(0, 800, 0.5, 17, 15.6),
  diagram(400, 800, null, 17, 15.6),
  diagram(400, 800, 0, 17, 15.6),
];
/** @type {(() => void) | undefined} */
let resize, finishFonts;
/** @type {Map<string, () => void>} */
const listeners = new Map();
/** @type {typeof diagrams} */
const observed = [];
/** @type {Promise<void>} */
const fontsReady = new Promise((resolve) => {
  finishFonts = () => resolve();
});
runInNewContext(source, {
  Math,
  parseFloat,
  document: {
    /** @param {string} selector */
    querySelectorAll(selector) {
      assert.equal(selector, ".line-fig svg, .chart svg, .n11-paper figure > svg, .n11-diagram");
      return diagrams;
    },
    fonts: { ready: fontsReady },
  },
  /** @param {ReturnType<typeof diagram> | {fontSize: number}} element */
  getComputedStyle(element) {
    read();
    if ("fit" in element) {
      return {
        /** @param {string} name */
        getPropertyValue(name) {
          assert.equal(name, "--paper-diagram-fit-from");
          return String(element.fit);
        },
      };
    }
    return { fontSize: String(element.fontSize) };
  },
  ResizeObserver: class {
    /** @param {() => void} callback */
    constructor(callback) {
      resize = callback;
    }
    /** @param {ReturnType<typeof diagram>} element */
    observe(element) {
      observed.push(element);
    }
  },
  window: {
    /** @param {string} name @param {() => void} callback */
    addEventListener(name, callback) {
      listeners.set(name, callback);
    },
    /** @param {string} query */
    matchMedia(query) {
      assert.equal(query, "print");
      return {
        /** @param {string} name @param {() => void} callback */
        addEventListener(name, callback) {
          assert.equal(name, "change");
          listeners.set("print-change", callback);
        },
      };
    },
  },
});
assert.equal(observed.length, diagrams.length);
observed.forEach((item, index) => {
  assert.equal(item, diagrams[index]);
});
assert.deepEqual(
  [...first.values],
  [
    ["--paper-diagram-font-size", "17px"],
    ["--paper-diagram-note-size", "15.6px"],
  ],
);
assert.deepEqual([...second.values], [["--paper-diagram-font-size", `${20 / 0.75}px`]]);
for (const item of diagrams.slice(2)) {
  assert.equal(item.values.size, 0);
}
assert.deepEqual([...listeners.keys()], ["beforeprint", "afterprint", "print-change"]);
assert.ok(resize);
assert.ok(finishFonts);
writing = false;
first.width = 200;
/** @type {() => void} */ (finishFonts)();
await fontsReady;
assert.equal(first.values.get("--paper-diagram-font-size"), "8.5px");
assert.equal(first.values.get("--paper-diagram-note-size"), "7.8px");
for (const callback of [resize, ...listeners.values()]) {
  writing = false;
  first.width = 200;
  callback();
  assert.equal(first.values.get("--paper-diagram-font-size"), "8.5px");
  assert.equal(first.values.get("--paper-diagram-note-size"), "7.8px");
}
writing = false;
first.width = 400;
first.parentElement.fontSize = 22;
assert.ok(first.caption);
first.caption.fontSize = 18;
resize();
assert.equal(first.values.get("--paper-diagram-font-size"), "22px");
assert.equal(first.values.get("--paper-diagram-note-size"), "18px");
process.stdout.write("complete");
