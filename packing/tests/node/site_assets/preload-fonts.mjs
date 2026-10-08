import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

const activate = /** @type {() => void} */ (probe("devtools/probes/site_assets/preload_fonts.js"));
const owned = "../assets/fonts/source-sans-3-latin-wght-normal.0123456789abcdef.woff2";
for (const protocol of ["http:", "https:", "file:", "data:"]) {
  for (const href of [
    owned,
    "https://other.test/font.woff2",
    "../assets/fonts/../font.woff2",
    "assets/fonts/font.bad.woff2",
  ]) {
    /** @type {string[][]} */
    const changes = [];
    const link = {
      getAttribute() {
        return href;
      },
      /** @param {string} value */
      set crossOrigin(value) {
        changes.push(["cors", value]);
      },
      /** @param {string} value */
      set rel(value) {
        changes.push(["rel", value]);
      },
    };
    Object.assign(globalThis, {
      location: { protocol },
      document: { querySelectorAll: () => [link] },
    });
    activate();
    assert.deepEqual(
      changes,
      href !== owned || protocol === "data:"
        ? []
        : protocol === "file:"
          ? [["rel", "preload"]]
          : [
              ["cors", "anonymous"],
              ["rel", "preload"],
            ],
    );
  }
}
