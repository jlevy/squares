import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { runInNewContext } from "node:vm";

// The probe is a file the checkers hand to a page; here it runs against a stand-in document,
// so its rule for what counts as drawn is checked without a browser.
const source = readFileSync(new URL("../probes/stage/visible-count.js", import.meta.url), "utf8");

type Square = {
  style: { display: string };
  dataset: { identity: string };
  getAttribute: (name: string) => string | null;
  firstElementChild: { getBoundingClientRect: () => { width: number } } | null;
};

function square(opacity: string | null, { display = "", width = 10 } = {}): Square {
  return {
    style: { display },
    dataset: { identity: "1" },
    getAttribute: (name) => (name === "opacity" ? opacity : null),
    firstElementChild: { getBoundingClientRect: () => ({ width }) },
  };
}

function drawn(squares: Square[]): number {
  const document = { querySelectorAll: () => squares };
  const probe: unknown = runInNewContext(source, { Array, Error, Number, document });
  assert.equal(typeof probe, "function");
  return (probe as () => number)();
}

test("a square counts as drawn only with a readable opacity above the threshold", () => {
  assert.equal(drawn([square(null)]), 1);
  assert.equal(drawn([square("1")]), 1);
  assert.equal(drawn([square("0.5")]), 1);
  assert.equal(drawn([square("0.01")]), 0);
  assert.equal(drawn([square("0")]), 0);
});

test("an opacity that does not read as a number is not drawn", () => {
  assert.equal(drawn([square("NaN")]), 0);
  assert.equal(drawn([square("none")]), 0);
});

test("a hidden or zero-width square is not drawn", () => {
  assert.equal(drawn([square("1", { display: "none" })]), 0);
  assert.equal(drawn([square("1", { width: 0 })]), 0);
  assert.equal(drawn([square("1"), square("NaN"), square("0.4")]), 2);
});
