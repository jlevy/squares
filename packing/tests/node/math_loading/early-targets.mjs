// `check_math_loading/early_events.js`: the early-input targets are frozen before any event can
// reset the sliders, and each ends at a value distinct from where it started.
import assert from "node:assert/strict";
import { probe } from "../probe.mjs";

const sliders = ["kslider-one", "phi-one", "kslider-two", "phi-two"].map((id) => ({
  id,
  min: "0",
  max: "450",
  step: "1",
  value: id.startsWith("phi-") ? "196" : "0",
  /** @type {string[]} */
  events: [],
  dispatchEvent() {
    this.events.push(this.value);
  },
}));
const initial = sliders.map((slider) => slider.value);
Object.assign(globalThis, {
  document: { querySelectorAll: () => sliders },
  window: {
    dispatchEvent() {
      sliders.forEach((slider, i) => {
        slider.value = /** @type {string} */ (initial[i]);
      });
    },
  },
});

/** @type {readonly { id: string, value: string }[]} */
const targets = probe("devtools/probes/check_math_loading/early_events.js")();
assert.equal(Object.isFrozen(targets), true);
assert.equal(new Set(targets.map((target) => target.value)).size, sliders.length);
for (const [i, target] of targets.entries()) {
  const slider = /** @type {(typeof sliders)[number]} */ (sliders[i]);
  assert.equal(Object.isFrozen(target), true);
  assert.notEqual(target.value, initial[i], "dropping all input must change output");
  assert.notEqual(target.value, slider.value, "boot resets cannot revise expectations");
  assert.equal(slider.events.length, 2);
  assert.notEqual(slider.events[0], slider.events[1]);
  assert.equal(slider.events[1], target.value);
}
