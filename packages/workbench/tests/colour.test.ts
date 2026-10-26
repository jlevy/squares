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
    angleCentres: [],
  };
}

test("angle classes are seam-safe and stable slots depend only on their angle", () => {
  const colours = createColourSystem(fixtureColour());
  const map = colours.buildAngleMap([89.8, 0.2, 44.4, 44.6, 65.1299]);
  // The pins are classes of their own: 44.6 joins 45 and 44.4, outside it, stays apart, so
  // in a frame each takes the slot it takes alone.
  assert.equal(map.classes, 4);
  assert.deepEqual(map.sizes, [2, 1, 1, 1]);
  assert.equal(map.centres[0], 0);
  assert.ok(Math.abs((map.centres[1] ?? 0) - 44.4) < 1e-9);
  assert.equal(map.centres[2], 45);
  assert.deepEqual(map.slots.slice(0, 3), [0, 10, 1]);
  assert.deepEqual(
    [0, 0.4, 0.6, 44.4, 44.6, 45].map((angle) => colours.slotForAngle(angle)),
    [0, 0, 2, 10, 1, 1],
  );
  assert.deepEqual(
    [89.8, 0.2, 44.4, 44.6, 65.1299].map((angle) => map.slotOf(angle)),
    [0, 0, 10, 1, 15],
  );

  const sameAngleAlone = colours.angleFills([65.1299], [0])[0];
  const sameAngleTogether = colours.angleFills([10, 65.1299, 30], [0, 0, 0])[1];
  assert.equal(sameAngleAlone, sameAngleTogether);
});

test("a tilt the atlas shares keeps its class and slot in every frame (#554)", () => {
  // Two shared centres either side of the 65-degree band edge, as the atlas's are.
  const centres = [64.7291, 65.256];
  const shared = createColourSystem({ ...fixtureColour(), angleCentres: centres });
  const alone = createColourSystem(fixtureColour());
  // n = 29 carries 64.7413 and 65.0374; T-151's n = 272 carries 64.5234, 65.1017 and 65.3157.
  const n29 = [64.7413, 65.0374];
  const n272 = [65.1017, 65.3157, 64.5234];
  // Clustered frame by frame, n = 29's two tilts made one class at 64.9387 in slot 14 and
  // n = 272's first two one at 65.2087 in slot 15: 65.0374 and 65.1017 drew in two colours.
  assert.deepEqual(alone.buildAngleMap(n29).slots, [14]);
  assert.deepEqual(alone.buildAngleMap(n272).slots, [15, 14]);
  assert.notEqual(
    alone.buildAngleMap(n29).slotOf(65.0374),
    alone.buildAngleMap(n272).slotOf(65.1017),
  );
  // From shared centres, each frame's classes are the shared ones and every tilt takes the
  // slot of its class's centre, whichever frame it is in and whatever else is in it.
  const first = shared.buildAngleMap(n29);
  const second = shared.buildAngleMap(n272);
  assert.deepEqual(first.centres, centres);
  assert.deepEqual(first.slots, [14, 15]);
  assert.deepEqual(second.centres, [65.256, 64.7291]);
  assert.deepEqual(second.slots, [15, 14]);
  assert.deepEqual(second.sizes, [2, 1]);
  for (const angle of [...n29, ...n272]) {
    assert.equal(first.slotOf(angle), second.slotOf(angle));
    assert.equal(first.slotOf(angle), shared.slotForAngle(angle));
  }
  assert.equal(first.classOf(65.0374), 1);
  assert.equal(second.classOf(65.0374), 0);
  // A tilt no shared class holds clusters with its frame's others, as every tilt once did.
  const loose = shared.buildAngleMap([20.1, 20.4, 64.7]);
  assert.equal(loose.classes, 2);
  assert.ok(Math.abs((loose.centres[0] ?? 0) - 20.25) < 1e-9);
  assert.equal(loose.classOf(20.3), 0);
  assert.equal(loose.classOf(64.9), 1);
  assert.equal(loose.classOf(30), -1);
  // Centres that are unsorted, too close together or inside a pinned class are refused.
  for (const angleCentres of [[65.256, 64.7291], [64.7291, 65.2], [0.3], [44.8], [90]]) {
    assert.throws(() => createColourSystem({ ...fixtureColour(), angleCentres }), /centre/);
  }
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
        angleCentres: [],
      }),
    /palette/,
  );
});

/** A hex colour's OKLab chroma, which is what a blend must not let sag. */
function chromaOf(colours: ReturnType<typeof createColourSystem>, hex: string): number {
  // `trim` scales chroma toward neutral, so the distance a full trim moves a colour is that
  // colour's chroma, read through the system's own conversions rather than a second copy.
  const neutral = colours.trim(hex, 0);
  const channels = (value: string): number[] =>
    [1, 3, 5].map((at) => Number.parseInt(value.slice(at, at + 2), 16));
  const [r, g, b] = channels(hex);
  const [nr, ng, nb] = channels(neutral);
  return Math.hypot((r ?? 0) - (nr ?? 0), (g ?? 0) - (ng ?? 0), (b ?? 0) - (nb ?? 0));
}

test("a blend between distant hues crosses through neutral, never a third hue", () => {
  const colours = createColourSystem(fixtureColour());
  // Green to scarlet is close to a half turn of hue, and it is the blend the page runs most:
  // every newly placed square is tinted along it. Neither a chord across the a-b plane nor an
  // arc around the wheel is right for it -- the chord lands on a muddy olive and the arc runs
  // through yellow, and yellow is a colour neither end has and the picture never shows. The
  // blend collapses chroma to nothing at the crossing instead and brings it back on the far
  // side, so the change reads as green, greyer, scarlet.
  const green = "#3f8a63";
  const scarlet = "#a43b47";
  const ends = Math.min(chromaOf(colours, green), chromaOf(colours, scarlet));
  assert.ok(chromaOf(colours, colours.mix(green, scarlet, 0.5)) < ends * 0.05);
  // Approaching the crossing from either side, chroma only falls.
  const falling = [0.1, 0.25, 0.4].map((at) => chromaOf(colours, colours.mix(green, scarlet, at)));
  const rising = [0.6, 0.75, 0.9].map((at) => chromaOf(colours, colours.mix(green, scarlet, at)));
  assert.deepEqual(
    falling,
    [...falling].sort((a, b) => b - a),
  );
  assert.deepEqual(
    rising,
    [...rising].sort((a, b) => a - b),
  );
  // The green side stays green and the scarlet side stays scarlet: at no point does a third
  // hue appear. Green has more green channel than red; scarlet has more red than green.
  const channels = (value: string): number[] =>
    [1, 3, 5].map((at) => Number.parseInt(value.slice(at, at + 2), 16));
  for (const at of [0.1, 0.25, 0.4]) {
    const [red, greenCh] = channels(colours.mix(green, scarlet, at));
    assert.ok((greenCh ?? 0) >= (red ?? 0), `${colours.mix(green, scarlet, at)} at ${at}`);
  }
  for (const at of [0.6, 0.75, 0.9]) {
    const [red, greenCh] = channels(colours.mix(green, scarlet, at));
    assert.ok((red ?? 0) >= (greenCh ?? 0), `${colours.mix(green, scarlet, at)} at ${at}`);
  }
});

test("two shades of one family blend directly, without a wash in the middle", () => {
  const colours = createColourSystem(fixtureColour());
  // The crossing is for hues far enough apart that the way between them runs through a colour
  // neither has. Shades of one family are the same colour moving a little, and taking those
  // through neutral would put a grey pulse in the middle of a change nobody should notice.
  const before = "#2fa88f";
  const after = "#2f9d7d";
  const ends = Math.min(chromaOf(colours, before), chromaOf(colours, after));
  for (const at of [0.25, 0.5, 0.75]) {
    assert.ok(chromaOf(colours, colours.mix(before, after, at)) > ends * 0.9);
  }
});

test("a blend takes the short way round the hue wheel and neutrals borrow a hue", () => {
  const colours = createColourSystem(fixtureColour());
  // These two straddle the seam where hue wraps: `labToPolar` reports them at +175.6 and
  // -178.2 degrees, so the short way between them is 6 degrees through teal and the long way
  // is 354 degrees through green, yellow, red and blue. Both endpoints are teal, so red is
  // their weakest channel; a midpoint where red has become the strongest is a blend that
  // travelled the long way, which is the same defect as the chord, wearing a different shape.
  const greenSide = "#2fa88f";
  const blueSide = "#2fa494";
  const channels = (value: string): number[] =>
    [1, 3, 5].map((at) => Number.parseInt(value.slice(at, at + 2), 16));
  for (const progress of [0.25, 0.5, 0.75]) {
    const middle = colours.mix(greenSide, blueSide, progress);
    const [red, green, blue] = channels(middle);
    assert.ok(
      (red ?? 0) < (green ?? 0) && (red ?? 0) < (blue ?? 0),
      `${middle} at ${progress} left the short arc between ${greenSide} and ${blueSide}`,
    );
  }
  // A neutral endpoint has no hue of its own; reading its noisy angle would swing the blend
  // through hues neither colour has.
  const fromGrey = colours.mix("#808080", "#3f8a63", 0.5);
  assert.ok(chromaOf(colours, fromGrey) > 0, fromGrey);
  assert.equal(colours.mix("#808080", "#3f8a63", 1), "#3f8a63");
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
      homeward: 1,
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
    stillPair: false,
    movingSlots: null,
  });
  assert.deepEqual(receipt.fills, colours.identityFills(2));
  assert.deepEqual(receipt.contacts, [3, 3]);
  assert.deepEqual(receipt.contactEdges, [0, 1]);
  assert.deepEqual([...receipt.touching], [1]);
  assert.equal(receipt.overlap, 0);
  assert.equal(receipt.scheme, "identity");
});
