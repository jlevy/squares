// The shipped 404 alias script against a location/document fixture. Browser arrival
// checks exercise the production page separately; these cases keep the unit gate fast.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import vm from "node:vm";

const source = readFileSync(
  new URL("../../../devtools/overview/not-found.js", import.meta.url),
  "utf8",
);
const aliases = {
  cases: [11],
  results: ["result/t-001.html"],
  rows: ["t-001"],
  allResults: "all-results.html",
};

/** @param {string} address @returns {string | null} */
function arrival(address) {
  const url = new URL(address);
  /** @type {string | null} */
  let destination = null;
  const location = {
    pathname: url.pathname,
    origin: url.origin,
    search: url.search,
    hash: url.hash,
    /** @param {string} value */
    replace(value) {
      destination = value;
    },
  };
  const document = {
    documentElement: { dataset: { siteRoot: "/squares/" } },
    getElementById() {
      return { textContent: JSON.stringify(aliases) };
    },
  };
  vm.runInNewContext(source, { document, location, URL });
  return destination;
}

for (const alias of ["cases/n-11.html", "cases/011.html", "cases/n-011.html"]) {
  void test(`${alias} preserves query and fragment at the canonical case`, () => {
    assert.equal(
      arrival(`https://example.org/squares/${alias}?view=embed#proof`),
      "https://example.org/squares/cases/11.html?view=embed#proof",
    );
  });
}

void test("uppercase result ID leads to its retained page", () => {
  assert.equal(
    arrival("https://example.org/squares/result/T-001.html?view=embed#proof"),
    "https://example.org/squares/result/t-001.html?view=embed#proof",
  );
});

void test("missing canonical result page leads to its known row", () => {
  assert.equal(
    arrival("https://example.org/squares/result/t-001.html?view=embed#proof"),
    "https://example.org/squares/all-results.html?view=embed#t-001",
  );
});

for (const path of ["cases/012.html", "result/T-999.html", "result/T-001.html/evil"]) {
  void test(`unknown address ${path} keeps the 404 page`, () => {
    assert.equal(arrival(`https://example.org/squares/${path}#proof`), null);
  });
}

void test("a path outside the project cannot redirect", () => {
  assert.equal(arrival("https://example.org/result/T-001.html"), null);
});
