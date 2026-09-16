// `math/library.js`'s `activeVariant`: saved-font variants do not discard hidden
// certificates, and malformed variant metadata throws rather than dropping math.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

const document = { documentElement: { dataset: /** @type {Record<string, string>} */ ({}) } };
Object.assign(globalThis, { document });

const plain = { hidden: true, closest: () => null };
/**
 * @param {string | undefined} contexts
 * @param {object} [parent]
 */
const variant = (contexts, parent = plain) => ({
  dataset: { squaresMathContexts: contexts },
  parentElement: parent,
  closest() {
    return this;
  },
});

/** @type {{ activeVariant: (node: object) => boolean }} */
const { activeVariant: active } = probe("devtools/probes/math/library.js")();

for (const fontSet of ["custom", "system"]) {
  for (const proseFont of ["serif", "sans"]) {
    document.documentElement.dataset = { kpressFontSet: fontSet, kpressProseFont: proseFont };
    const key = `${fontSet}-${proseFont}`;
    const choices = ["custom-serif", "custom-sans", "system-serif", "system-sans"];
    for (const context of choices) {
      assert.equal(active(variant(context)), context === key);
    }
    assert.equal(active(variant(choices.join(" "))), true);
    assert.equal(active(plain), true, "hidden certificates remain intended math");
  }
}
for (const contexts of ["", undefined, "custom-mono", "system-serif unknown"]) {
  assert.throws(() => active(variant(contexts)), /malformed saved-font math variant/);
}
document.documentElement.dataset = { kpressFontSet: "invalid", kpressProseFont: "invalid" };
assert.equal(active(variant("custom-serif")), true, "invalid settings use defaults");
