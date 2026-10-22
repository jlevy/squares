// `render_n11_lower_bounds_explainer_pdf/absolute_links.js` against anchor stand-ins:
//
//   node absolute-links.mjs
//
// The page is drawn from a `file://` URL and served a level below the site's root, under
// `papers/`. Each relative link has to come out as the address a reader of the PDF can
// open: resolved against the page's own published URL, so a link that climbs to the root
// lands on the root, and a link to a file beside the page stays beside it.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

const absoluteLinks = /** @type {(page: string) => void} */ (
  probe("devtools/probes/render_n11_lower_bounds_explainer_pdf/absolute_links.js")
);

const PAGE = "https://squaremath.org/papers/n11-lower-bounds-explainer.html";

/** @param {string} href */
const anchor = (href) => ({
  href,
  getAttribute() {
    return this.href;
  },
  /** @param {string} _name @param {string} value */
  setAttribute(_name, value) {
    this.href = value;
  },
});

const anchors = [
  "../known-best-1-100.pdf",
  "n11-lower-bounds-explainer.md",
  "../papers.html",
  ".././",
  "../all-results.html#t-060",
  "#fn-3",
  "https://github.com/jlevy/squares",
  "mailto:someone@example.org",
].map(anchor);
Object.assign(globalThis, { document: { querySelectorAll: () => anchors } });

absoluteLinks(PAGE);

assert.deepEqual(
  anchors.map((a) => a.href),
  [
    "https://squaremath.org/known-best-1-100.pdf",
    "https://squaremath.org/papers/n11-lower-bounds-explainer.md",
    "https://squaremath.org/papers.html",
    "https://squaremath.org/",
    "https://squaremath.org/all-results.html#t-060",
    "#fn-3",
    "https://github.com/jlevy/squares",
    "mailto:someone@example.org",
  ],
);
