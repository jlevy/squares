// The Visualize page's film starter, run against a stand-in document and film: it starts
// the film a reader has not asked to keep still, and leaves it at its poster for a reader
// who asks for reduced motion, in a card's framed preview, on a page with no such film,
// and in a browser that refuses to start it.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import vm from "node:vm";

const SOURCE = readFileSync(new URL("../../../devtools/overview/film.js", import.meta.url), "utf8");

class HTMLVideoElement {
  autoplay = false;
  plays = 0;
  pauses = 0;
  /** @type {Promise<void>} */
  outcome = Promise.resolve();

  play() {
    this.plays += 1;
    return this.outcome;
  }

  pause() {
    this.pauses += 1;
  }
}

/**
 * The film after the starter has run on a page: `reduced` is the reader's motion
 * preference, `view` the root's `data-site-view`, `film` what the page's marked film is.
 * @param {{ reduced?: boolean, view?: string | null, film?: object | null }} [options]
 * @returns {{ film: object | null, queries: string[], selectors: string[] }}
 */
function visited({ reduced = false, view = null, film = new HTMLVideoElement() } = {}) {
  /** @type {string[]} */
  const queries = [];
  /** @type {string[]} */
  const selectors = [];
  const context = vm.createContext({
    HTMLVideoElement,
    document: {
      documentElement: {
        /** @param {string} name */
        getAttribute: (name) => (name === "data-site-view" ? view : null),
      },
      querySelectorAll: () => [],
      /** @param {string} selector */
      querySelector: (selector) => {
        selectors.push(selector);
        return film;
      },
    },
    window: {
      /** @param {string} query */
      matchMedia: (query) => {
        queries.push(query);
        return { matches: reduced };
      },
    },
  });
  vm.runInContext(SOURCE, context);
  return { film, queries, selectors };
}

void test("a visit starts the film the page marks, and only that one", () => {
  const { film, queries, selectors } = visited();
  assert.ok(film instanceof HTMLVideoElement);
  assert.equal(film.autoplay, true);
  assert.equal(film.plays, 1);
  assert.equal(film.pauses, 0);
  assert.deepEqual(selectors, ["video[data-autoplay]"]);
  assert.deepEqual(queries, ["(prefers-reduced-motion: reduce)"]);
});

void test("a reader who asks for reduced motion keeps the poster", () => {
  const { film } = visited({ reduced: true });
  assert.ok(film instanceof HTMLVideoElement);
  assert.equal(film.autoplay, false);
  assert.equal(film.plays, 0);
});

void test("a page framed in a card's popover does not start its film", () => {
  const { film } = visited({ view: "embed" });
  assert.ok(film instanceof HTMLVideoElement);
  assert.equal(film.autoplay, false);
  assert.equal(film.plays, 0);
});

void test("a page with no marked film, or something else marked, is left alone", () => {
  assert.equal(visited({ film: null }).film, null);
  const other = { autoplay: false, play: () => assert.fail("not a film") };
  assert.equal(visited({ film: other }).film, other);
  assert.equal(other.autoplay, false);
});

void test("a browser that refuses to start the film raises nothing and keeps the play control", async () => {
  const film = new HTMLVideoElement();
  const refused = Promise.reject(new Error("NotAllowedError"));
  film.outcome = refused;
  /** @type {unknown[]} */
  const unhandled = [];
  /** @param {unknown} reason */
  const record = (reason) => {
    unhandled.push(reason);
  };
  process.on("unhandledRejection", record);
  try {
    visited({ film });
    assert.equal(film.plays, 1);
    // No handler is attached here: the starter's own is what keeps this handled.
    await new Promise((resolve) => setImmediate(resolve));
    await new Promise((resolve) => setImmediate(resolve));
    assert.deepEqual(unhandled, []);
    assert.equal(film.pauses, 1);
  } finally {
    process.off("unhandledRejection", record);
  }
});
