import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { test } from "node:test";
import { sampleAnimation } from "../src/animation/trace.ts";
import { decodeAnimation } from "../src/data/animation.ts";
import { paintAnimation } from "../src/view/animation-scene.ts";
import { createColourSystem } from "../src/view/colour.ts";
import { sceneSvg } from "../src/view/stage-renderer.ts";

const colours = createColourSystem({
  palette: Array.from({ length: 20 }, (_, index) => `#${(0x123400 + index * 200).toString(16)}`),
  shades: Array.from({ length: 20 }, (_, family) =>
    Array.from(
      { length: 5 },
      (_, shade) => `#${(0x123400 + family * 200 + shade * 10).toString(16)}`,
    ),
  ),
  angleToleranceDegrees: 0.5,
});
const input: unknown = JSON.parse(
  await readFile(new URL("fixtures/packing-animation-v1.json", import.meta.url), "utf8"),
);

test("trace drawing keeps identity order and all palette switches affect their declared channel", () => {
  const document = decodeAnimation(input);
  const sample = sampleAnimation(document, 0);
  document.palette = { hue: "identity", shade: "none" };
  const identity = paintAnimation(sample, document, colours);
  assert.deepEqual(
    identity.scene.squares.map((square) => square.identity),
    [2, 1],
  );
  assert.deepEqual(identity.fills, [colours.identityFill(2), colours.identityFill(1)]);
  document.palette = { hue: "uniform", shade: "none" };
  assert.equal(new Set(paintAnimation(sample, document, colours).fills).size, 1);
  document.palette = { hue: "angle-class", shade: "none" };
  assert.deepEqual(paintAnimation(sample, document, colours).fills, colours.atlasFills([0, 0]));
  document.palette = { hue: "identity", shade: "full-side-contact" };
  assert.notDeepEqual(paintAnimation(sample, document, colours).fills, identity.fills);
  document.palette = { hue: "identity", shade: "evidence" };
  const invalid = paintAnimation(sampleAnimation(document, 0.5), document, colours);
  assert.notDeepEqual(invalid.fills, identity.fills);
  const interpolated = paintAnimation(sampleAnimation(document, 0.25), document, colours);
  assert.equal(interpolated.scene.motion, "direct-illustration");
  assert.match(sceneSvg(interpolated), /<svg/);
});

test("browser import bounds worst-case geometry work before examining frame contents", () => {
  assert.throws(
    () =>
      decodeAnimation({
        contract: "packing.squares:PackingAnimation/v1",
        name: "oversized",
        n: 324,
        frames: Array(100).fill(null),
      }),
    /geometry-check budget/,
  );
  const document = decodeAnimation(input);
  assert.throws(
    () =>
      decodeAnimation({
        contract: document.contract,
        name: "empty source",
        n: 1,
        source: { strategy: "" },
        frames: [],
      }),
    /must not be empty/,
  );
});
