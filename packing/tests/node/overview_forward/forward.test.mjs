// The forwarder, run against a stand-in location and document. On the overview an old
// link to the results table or to one of its rows goes to the results page, one to The
// Frontier Survey goes to the Frontier page, and any other fragment the overview lacks
// goes to the explainer where it is served now, query string and fragment kept. On a forwarder page, which names where it sends a reader in
// `data-moved-to`, every visit goes there, query string and fragment kept.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import vm from "node:vm";

const SOURCE = readFileSync(
  new URL("../../../devtools/overview/forward.js", import.meta.url),
  "utf8",
);

/** Where the explainer is served, from the site's root. */
const EXPLAINER = "papers/n11-lower-bounds-explainer.html";

/**
 * Where the forwarder sends a reader arriving with `search` and `hash`, or null when it
 * leaves them where they are. `moved` is the page's `data-moved-to`, which only a
 * forwarder page has.
 * @param {string} hash
 * @param {{ search?: string, ids?: readonly string[], results?: readonly string[], retired?: string, moved?: string, fileMoved?: string, caseNumbers?: string, protocol?: string, preview?: boolean }} [options]
 * @returns {string | null}
 */
function forwarded(
  hash,
  {
    search = "",
    ids = [],
    results = ["t-018", "t-031", "t-037"],
    retired = '{"t-117":"result/t-117.html","t-118":"result/t-118.html"}',
    moved,
    fileMoved,
    caseNumbers,
    protocol = "https:",
    preview = false,
  } = {},
) {
  /** @type {string | null} */
  let target = null;
  const context = vm.createContext({
    URL,
    URLSearchParams,
    decodeURIComponent,
    document: {
      documentElement: { dataset: { movedTo: moved, fileMovedTo: fileMoved, caseNumbers } },
      /** @param {string} id */
      getElementById: (id) => (ids.includes(id) ? {} : null),
      /** @param {string} selector */
      querySelector: (selector) =>
        selector === "[data-atlas-preview]"
          ? preview
            ? {}
            : null
          : {
              /** @param {string} name */
              getAttribute: (name) =>
                name === "data-result-ids"
                  ? results.join(" ")
                  : name === "data-retired-results"
                    ? retired
                    : null,
            },
    },
    window: {
      location: {
        href: `${protocol}//example.test/squares/cases.html${search}${hash}`,
        protocol,
        hash,
        search,
        /** @param {string} url */
        replace: (url) => {
          target = url;
        },
      },
    },
  });
  vm.runInContext(SOURCE, context);
  return target;
}

void test("the old results section goes to the results page", () => {
  assert.equal(forwarded("#every-result"), "all-results.html#every-result");
});

void test("a result's row goes to its row on the results page", () => {
  assert.equal(forwarded("#t-018"), "all-results.html#t-018");
  assert.equal(forwarded("#t-037", { search: "?x=1" }), "all-results.html?x=1#t-037");
  assert.equal(
    forwarded("#%74-031", { search: "?kind=rigidity&current=true" }),
    "all-results.html?kind=rigidity&current=true#%74-031",
  );
});

void test("only statically registered results forward, with current page ids taking precedence", () => {
  for (const hash of ["#t-999", "#t-31", "#T-031", "#t-031%2Foutside", "#%E0%A4"]) {
    assert.equal(forwarded(hash), null, hash);
  }
  assert.equal(forwarded("#t-031", { results: [] }), null);
  assert.equal(forwarded("#t-031", { ids: ["t-031"] }), null);
});

void test("registered retired result fragments forward to their own explanatory tombstones", () => {
  for (const { hash, path } of [
    { hash: "#t-117", path: "result/t-117.html" },
    { hash: "#%74-118", path: "result/t-118.html" },
  ]) {
    assert.equal(
      forwarded(hash, { search: "?current=true&review=legacy" }),
      `${path}?current=true&review=legacy${hash}`,
    );
  }
  assert.equal(forwarded("#t-117", { ids: ["t-117"] }), null);
});

void test("retired result metadata fails closed for malformed or unsafe destinations", () => {
  for (const retired of [
    "{",
    "null",
    "[]",
    '{"t-117":"https://elsewhere.test/result/t-117.html"}',
    '{"t-117":"../result/t-117.html"}',
    '{"t-117":"result/t-118.html"}',
    '{"t-117":"result/t-117.html?redirect=elsewhere"}',
  ]) {
    assert.equal(forwarded("#t-117", { retired }), null, retired);
  }
  assert.equal(forwarded("#t-999"), null);
  assert.equal(forwarded("#%E0%A4"), null);
});

void test("known explainer fragments and certificate selectors retain their target", () => {
  assert.equal(forwarded("#fn-3"), `${EXPLAINER}#fn-3`);
  assert.equal(
    forwarded("#381-100", { search: "?review=fonts" }),
    `${EXPLAINER}?review=fonts#381-100`,
  );
});

void test("a fragment the overview has, or none, stays", () => {
  assert.equal(forwarded("#recent-results", { ids: ["recent-results"] }), null);
  assert.equal(forwarded(""), null);
});

void test("the ladders' two fragments go to the results page where the section is", () => {
  // Verification Ladders left the overview for the results page on 2026-10-02; it was
  // `#verification-at-a-glance` until 2026-10-01, and its heading there keeps an empty
  // anchor of that id, so both fragments are sent on with the fragment kept.
  assert.equal(forwarded("#verification-ladders"), "all-results.html#verification-ladders");
  assert.equal(forwarded("#verification-at-a-glance"), "all-results.html#verification-at-a-glance");
});

void test("the survey's two fragments go to the combined Atlas page", () => {
  // The Frontier Survey left the overview on 2026-10-02, its account the Frontier page's
  // own; it was `#the-survey` until 2026-10-01, and both fragments are sent there.
  assert.equal(forwarded("#the-frontier-survey"), "atlas.html#the-frontier-survey");
  assert.equal(forwarded("#the-survey", { search: "?x=1" }), "atlas.html?x=1#the-survey");
});

void test("a renamed section's old fragment stays while an anchor keeps its id", () => {
  // The Atlas of Square Packings was `#the-atlas`; its heading keeps an empty anchor of
  // that id, without which the old link would be sent to the explainer.
  const atlas = "#the-atlas";
  assert.equal(forwarded(atlas, { ids: ["the-atlas-of-square-packings", "the-atlas"] }), null);
  assert.equal(forwarded(atlas, { ids: ["the-atlas-of-square-packings"] }), null);
});

void test("the compact homepage forwards full atlas state and moved resource fragments", () => {
  for (const hash of ["#the-atlas", "#the-atlas-of-square-packings"]) {
    assert.equal(
      forwarded(hash, { preview: true, ids: [hash.slice(1)], search: "?size=large" }),
      `atlas.html?size=large${hash}`,
    );
  }
  assert.equal(
    forwarded("", { preview: true, search: "?atlas=triangle&size=small" }),
    "atlas.html?atlas=triangle&size=small",
  );
  for (const hash of ["#squares-project-documentation"]) {
    assert.equal(forwarded(hash, { preview: true }), `about.html${hash}`);
  }
  for (const id of ["squares-project-documentation", "learn-more"]) {
    assert.equal(forwarded(`#${id}`, { preview: true, ids: [id] }), null);
  }
  assert.equal(
    forwarded("#the-squares-project", { preview: true, ids: ["the-squares-project"] }),
    null,
  );
  assert.equal(forwarded("#pdfs-and-videos", { preview: true, ids: ["pdfs-and-videos"] }), null);
  assert.equal(forwarded("#the-atlas", { ids: ["the-atlas"], search: "?atlas=triangle" }), null);
});

void test("a forwarder page sends every visit where it names", () => {
  assert.equal(forwarded("", { moved: "all-results.html" }), "all-results.html");
  assert.equal(forwarded("", { moved: "frontier.html" }), "frontier.html");
  const defects = "https://github.com/jlevy/squares/blob/main/defects.md";
  assert.equal(forwarded("", { moved: defects }), defects);
  // `explainer.html`, from the site's root.
  assert.equal(forwarded("", { moved: EXPLAINER }), EXPLAINER);
});

void test("a forwarder page keeps the query string and the fragment", () => {
  assert.equal(
    forwarded("#next-actions", { moved: "all-results.html", search: "?x=1" }),
    "all-results.html?x=1#next-actions",
  );
  // A fragment the old page had is not looked up: a forwarder has no content of its own.
  assert.equal(forwarded("#n-11", { moved: "frontier.html", ids: ["n-11"] }), "frontier.html#n-11");
});

void test("a paper's old address sends every visit on to the paper", () => {
  assert.equal(forwarded("#fn-3", { moved: EXPLAINER }), `${EXPLAINER}#fn-3`);
  assert.equal(
    forwarded("#381-100", { moved: EXPLAINER, search: "?review=fonts" }),
    `${EXPLAINER}?review=fonts#381-100`,
  );
  // `n11-optimality/t-060-explainer.html` and its directory's index, a level down.
  const review = "../papers/n11-optimality-review.html";
  assert.equal(forwarded("#the-capture-graph", { moved: review }), `${review}#the-capture-graph`);
  assert.equal(forwarded("", { moved: review, search: "?view=embed" }), `${review}?view=embed`);
  // Only the overview owned the results table: a moved paper's `#t-018` is the paper's.
  assert.equal(forwarded("#t-018", { moved: EXPLAINER }), `${EXPLAINER}#t-018`);
});

void test("unknown and malformed fragments stay where the reader put them", () => {
  for (const hash of ["#unknown-future-heading", "#fn-9999", "#%E0%A4%A", "#the-atlas"]) {
    assert.equal(forwarded(hash), null);
  }
  assert.equal(forwarded("#proof"), `${EXPLAINER}#proof`);
  assert.equal(
    forwarded("#beyond-point-atoms-the-current-bound"),
    `${EXPLAINER}#beyond-point-atoms-the-current-bound`,
  );
});

void test("retired case directories select registered Atlas rows and preserve record sections", () => {
  for (const moved of ["atlas.html", "../atlas.html"]) {
    const options = { moved, caseNumbers: "11,12,291" };
    assert.equal(forwarded("#n-11", options), `${moved}#n-11`);
    assert.equal(forwarded("#n-00012", options), `${moved}#n-12`);
    assert.equal(
      forwarded("#n-291", { ...options, search: "?recent=true" }),
      `${moved}?recent=true#n-291`,
    );
    assert.equal(
      forwarded("", { ...options, search: "?n=12&view=embed" }),
      `${moved}?view=embed#n-12`,
    );
    assert.equal(forwarded("#n-11", { ...options, search: "?n=12" }), `${moved}#n-12`);
    assert.equal(
      forwarded("#bounds", { ...options, search: "?n=12&view=embed&raw=1" }),
      `${moved.replace("atlas.html", "cases/12.html")}?view=embed&raw=1#bounds`,
    );
    assert.equal(forwarded("#n-999", options), `${moved}#n-999`);
    assert.equal(
      forwarded("#bounds", { ...options, search: "?n=999&view=embed" }),
      `${moved}?n=999&view=embed#bounds`,
    );
  }
});

const EMBED_SOURCE = readFileSync(
  new URL("../../../devtools/overview/embed.js", import.meta.url),
  "utf8",
);
/** @param {string} search @param {string} [pathname] @returns {Record<string, string>} */
function bootstrapped(search, pathname = "/atlas.html") {
  /** @type {Record<string, string>} */
  const attributes = {};
  vm.runInContext(
    EMBED_SOURCE,
    vm.createContext({
      URLSearchParams,
      location: { search, pathname },
      document: {
        documentElement: {
          /** @param {string} name @param {string} value */
          setAttribute(name, value) {
            attributes[name] = value;
          },
        },
        addEventListener() {},
      },
    }),
  );
  return attributes;
}
void test("layout queries establish only whitelisted root attributes before paint", () => {
  assert.deepEqual(bootstrapped("?atlas=triangle&size=large&view=embed"), {
    "data-site-atlas-view": "triangle",
    "data-site-atlas-size": "large",
    "data-site-atlas-scale": "fixed",
    "data-site-view": "embed",
  });
  assert.deepEqual(bootstrapped("?atlas=grid&size=small&view=embed"), {
    "data-site-atlas-view": "grid",
    "data-site-atlas-size": "small",
    "data-site-atlas-scale": "fixed",
    "data-site-view": "embed",
  });
  assert.deepEqual(bootstrapped("?atlas=unknown&size=invalid&view=unknown"), {
    "data-site-atlas-view": "triangle",
    "data-site-atlas-size": "small",
    "data-site-atlas-scale": "fixed",
  });
  assert.deepEqual(bootstrapped("?size=medium"), {
    "data-site-atlas-view": "triangle",
    "data-site-atlas-size": "medium",
    "data-site-atlas-scale": "fixed",
  });
  for (const scale of ["row", "global"]) {
    assert.deepEqual(bootstrapped(`?atlas=grid&size=large&scale=${scale}`), {
      "data-site-atlas-view": "grid",
      "data-site-atlas-size": "large",
      "data-site-atlas-scale": scale,
    });
  }
  assert.equal(bootstrapped("?scale=invalid")["data-site-atlas-scale"], "fixed");
  assert.deepEqual(bootstrapped(""), {
    "data-site-atlas-view": "triangle",
    "data-site-atlas-size": "small",
    "data-site-atlas-scale": "fixed",
  });
  assert.deepEqual(bootstrapped("", "/index.html"), {});
  assert.deepEqual(bootstrapped("?atlas=triangle&size=large&scale=row", "/index.html"), {});
});

void test("case directory migration uses the same Atlas destination for HTTP and files", () => {
  for (const moved of ["atlas.html", "../atlas.html"]) {
    const options = { moved, fileMoved: moved, caseNumbers: "11,12" };
    for (const protocol of ["https:", "file:"]) {
      assert.equal(
        forwarded("#unknown", { ...options, protocol, search: "?view=embed" }),
        `${moved}?view=embed#unknown`,
      );
      assert.equal(forwarded("#n-11", { ...options, protocol }), `${moved}#n-11`);
      assert.equal(forwarded("#n-999", { ...options, protocol }), `${moved}#n-999`);
      assert.equal(
        forwarded("#bounds", { ...options, protocol, search: "?n=12&view=embed" }),
        `${moved.replace("atlas.html", "cases/12.html")}?view=embed#bounds`,
      );
    }
  }
});

void test("related projects retain their homepage destination", () => {
  assert.equal(
    forwarded("#other-square-packing-projects", {
      preview: true,
      ids: ["other-square-packing-projects"],
    }),
    null,
  );
});
