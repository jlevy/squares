import assert from "node:assert/strict";
import { test } from "node:test";
import { measurePackingGeometry } from "../src/core/geometry.ts";
import type { CorpusColour } from "../src/data/corpus.ts";
import { createColourSystem } from "../src/view/colour.ts";
import type { SceneFrame } from "../src/view/scene-types.ts";

function hex(index: number): string {
  return `#${index.toString(16).padStart(6, "0")}`;
}

function fixtureColour(): CorpusColour {
  return {
    palette: Array.from({ length: 20 }, (_, index) => hex(index + 1)),
    shades: Array.from({ length: 20 }, (_, family) =>
      Array.from({ length: 5 }, (_unused, shade) => hex(100 + family * 5 + shade)),
    ),
    angleToleranceDegrees: 0.5,
  };
}

test("angle classes are seam-safe and stable slots depend only on their angle", () => {
  const colours = createColourSystem(fixtureColour());
  const map = colours.buildAngleMap([89.8, 0.2, 44.4, 44.6, 65.1299]);
  assert.equal(map.classes, 3);
  assert.deepEqual(map.sizes, [2, 2, 1]);
  assert(Math.min(map.centres[0] ?? 90, 90 - (map.centres[0] ?? 0)) < 1e-12);
  assert.deepEqual(
    [0, 0.4, 0.6, 44.4, 44.6, 45].map((angle) => colours.slotForAngle(angle)),
    [0, 0, 2, 10, 1, 1],
  );

  const sameAngleAlone = colours.angleFills([65.1299], [0])[0];
  const sameAngleTogether = colours.angleFills([10, 65.1299, 30], [0, 0, 0])[1];
  assert.equal(sameAngleAlone, sameAngleTogether);
});

test("atlas slots rank unpinned classes by size with a stable identity tie break", () => {
  const colours = createColourSystem(fixtureColour());
  const map = colours.buildAtlasMap([10, 10.2, 10.1, 20, 20.2, 30]);
  assert.deepEqual(map.sizes, [3, 2, 1]);
  assert.deepEqual(map.slots, [2, 3, 4]);
  assert.equal(map.slotOf(10), 2);
  assert.equal(map.slotOf(20), 3);
  assert.equal(map.slotOf(30), 4);
});

test("contact shading and identity colours retain their documented invariants", () => {
  const colours = createColourSystem(fixtureColour());
  assert.deepEqual(colours.angleFills([0, 0, 0, 0, 0], [0, 1, 2, 3, 4]), [
    hex(104),
    hex(103),
    hex(102),
    hex(101),
    hex(100),
  ]);

  const identities = colours.identityFills(90);
  assert.equal(colours.greens.length, 42);
  assert.equal(new Set(colours.greens).size, 42);
  assert.deepEqual(identities.slice(42, 84), identities.slice(0, 42));
  assert.deepEqual([...identities.slice(0, 42)].sort(), [...colours.greens].sort());
});

test("colour transformation endpoints are exact and invalid palette shapes fail early", () => {
  const colours = createColourSystem(fixtureColour());
  assert.equal(colours.mix("#123456", "#abcdef", 0), "#123456");
  assert.equal(colours.mix("#123456", "#abcdef", 1), "#abcdef");
  assert.equal(colours.desaturate("#123456", 0, 0.125), "#123456");
  assert.equal(colours.trim("#123456", 1), "#123456");

  assert.throws(
    () =>
      createColourSystem({
        palette: ["#000000", "#ffffff"],
        shades: [Array(5).fill("#000000"), Array(5).fill("#ffffff")],
        angleToleranceDegrees: 0.5,
      }),
    /palette/,
  );
});

test("one scene receipt carries fills, contacts, overlap, and touching evidence", () => {
  const colours = createColourSystem(fixtureColour());
  const scene: SceneFrame = {
    pairIndex: 0,
    n: 2,
    containerSide: 2,
    viewBox: { x: 0, y: 0, size: 2 },
    squares: [
      { index: 0, identity: 1, x: 0.5, y: 0.5, angleDegrees: 0, opacity: 1, scale: 1 },
      { index: 1, identity: 2, x: 1.5, y: 0.5, angleDegrees: 0, opacity: 1, scale: 1 },
    ],
    presentation: {
      drain: 0,
      newTint: 0,
      resting: 1,
      homeward: true,
      mark: null,
      linksOpacity: 0,
      ghostOpacity: 0,
    },
    motion: "packing-snapshot",
  };
  const geometry = measurePackingGeometry(
    {
      squareSide: 1,
      container: { originX: 0, originY: 0, side: 2 },
      poses: scene.squares.map((square) => ({ x: square.x, y: square.y, angle: 0 })),
    },
    { gap: 0.01, angleToleranceRadians: Math.PI / 360 },
  );
  const receipt = colours.paintScene(scene, geometry, {
    scheme: "identity",
    mode: "pack",
    animateStandardize: true,
    stageChroma: 1,
    desaturationFloor: 0.15,
    scarlet: "#a3123f",
    tintChroma: 0.6,
    restSource: null,
    restTarget: null,
    holdsColour: null,
    movingSlots: null,
  });
  assert.deepEqual(receipt.fills, colours.identityFills(2));
  assert.deepEqual(receipt.contacts, [3, 3]);
  assert.deepEqual(receipt.contactEdges, [0, 1]);
  assert.deepEqual([...receipt.touching], [1]);
  assert.equal(receipt.overlap, 0);
  assert.equal(receipt.scheme, "identity");
});
