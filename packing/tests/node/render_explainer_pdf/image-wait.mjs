// `render_explainer_pdf/images_decoded.js` against small image-element stand-ins:
//
//   node image-wait.mjs <case>
//
// where <case> is one of the keys of `CASES`. Each case installs its own `document`.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

/** @type {() => Promise<void>} */
const waitForImages = probe("devtools/probes/render_explainer_pdf/images_decoded.js");
/** @param {object} document */
const install = (document) => Object.assign(globalThis, { document });

/** @type {Record<string, () => Promise<void>>} */
const CASES = {
  "lazy-images-go-eager": async () => {
    /** @type {string[]} */
    const calls = [];
    const image = {
      loading: "lazy",
      complete: true,
      naturalWidth: 640,
      naturalHeight: 480,
      currentSrc: "file:///atlas.svg",
      async decode() {
        calls.push(this.loading);
      },
    };
    install({ images: [image] });
    await waitForImages();
    assert.deepEqual(calls, ["eager"]);
  },
  // A changed request may reject while its replacement is already drawable.
  "rejection-of-an-available-image": async () => {
    const image = {
      loading: "lazy",
      complete: true,
      naturalWidth: 640,
      naturalHeight: 480,
      currentSrc: "file:///atlas.svg",
      async decode() {
        throw new Error("the request changed");
      },
    };
    install({ images: [image] });
    await waitForImages();
  },
  "no-drawable-current-request": async () => {
    install({
      images: [
        {
          loading: "lazy",
          complete: false,
          naturalWidth: 0,
          naturalHeight: 0,
          currentSrc: "",
          src: "file:///missing-atlas.svg",
          async decode() {
            throw new Error("request failed");
          },
        },
        {
          loading: "eager",
          complete: true,
          naturalWidth: 0,
          naturalHeight: 0,
          currentSrc: "file:///empty-atlas.svg",
          src: "file:///empty-atlas.svg",
          async decode() {},
        },
      ],
    });
    await assert.rejects(waitForImages(), (/** @type {Error} */ error) => {
      assert.match(error.message, /2 required images are not drawable after decode/);
      assert.match(error.message, /missing-atlas[.]svg.*complete=false.*0x0.*request failed/);
      assert.match(error.message, /empty-atlas[.]svg.*complete=true.*0x0/);
      return true;
    });
  },
};

const run = CASES[String(process.argv[2])];
if (!run) {
  throw new Error(`no image-wait case ${process.argv[2]}; cases: ${Object.keys(CASES).join(", ")}`);
}
await run();
