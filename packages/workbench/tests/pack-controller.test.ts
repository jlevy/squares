import assert from "node:assert/strict";
import { test } from "node:test";
import { maximumPackContainerSide, parsePackSnapshot } from "../src/api/pack-api.ts";
import { PackController } from "../src/app/pack-controller.ts";
import { describePackValidity } from "../src/app/pack-panel.ts";
import { createGridPackStart } from "../src/simulation/pack.ts";
import { createColourSystem } from "../src/view/colour.ts";
import { paintPack } from "../src/view/pack-scene.ts";
import { sceneSvg } from "../src/view/stage-renderer.ts";

test("independent Pack supports count 1, off-catalogue 17, and 325", () => {
  for (const n of [1, 17, 325]) {
    const controller = new PackController({ n, seed: 0 });
    const initial = controller.state();
    assert.equal(initial.snapshot.poses.length, n);
    assert.equal(initial.assessment.valid, true);
    const receipt = controller.step(1);
    assert.equal(receipt.configuration.n, n);
    assert.equal(receipt.configuration.reference, null);
    assert.equal(receipt.configuration.guided, false);
    assert.equal(receipt.configuration.effectiveSeed, 0);
  }
});

test("a half-size or barely overlapping import is no packing, and the readout says so", () => {
  const controller = new PackController();
  const half = {
    squareSide: 0.5,
    container: { originX: 0, originY: 0, side: 1 },
    poses: [
      { x: 0.25, y: 0.25, angle: 0 },
      { x: 0.75, y: 0.25, angle: 0 },
    ],
  };
  controller.load(half);
  const shrunk = controller.state().assessment;
  assert.equal(shrunk.valid, false);
  assert.equal(shrunk.reason, "unit-size");
  const shrunkText = describePackValidity(shrunk);
  assert.equal(shrunkText.valid, false);
  assert.match(shrunkText.status, /not unit squares \(side 0\.5000\)/);
  assert.match(shrunkText.fact, /^Not a packing/);
  assert.match(shrunkText.side, /^bounding side/);

  const overlap = 5e-9;
  controller.load({
    squareSide: 1,
    container: { originX: 0, originY: 0, side: 2 },
    poses: [
      { x: 0.5, y: 0.5, angle: 0 },
      { x: 1.5 - overlap, y: 0.5, angle: 0 },
    ],
  });
  const pressed = controller.state().assessment;
  assert.equal(pressed.valid, false);
  assert.equal(pressed.reason, "pair-overlap");
  const pressedText = describePackValidity(pressed);
  assert.match(pressedText.status, /not a valid packing \(pair overlap 5\.00e-9\)/);
  assert.match(pressedText.fact, /^Not a packing: pair overlap 5\.00e-9/);

  controller.load({
    squareSide: 1,
    container: { originX: 0, originY: 0, side: 2 },
    poses: [
      { x: 0.5, y: 0.5, angle: 0 },
      { x: 1.5, y: 0.5, angle: 0 },
    ],
  });
  const touching = describePackValidity(controller.state().assessment);
  assert.equal(touching.valid, true);
  assert.equal(touching.status, "valid unit packing");
  assert.equal(touching.fact, "Valid unit packing");
  assert.equal(touching.side, "required side 2.000000");
});

test("exact seeds and restart reproduce a random run independently of batching", () => {
  const controller = new PackController({ n: 17, seed: 4294967295, startKind: "random" });
  const initial = controller.export();
  const first = controller.step(12);
  controller.restart();
  assert.deepEqual(controller.export(), initial);
  controller.step(3);
  assert.deepEqual(controller.step(9), first);
  const before = controller.state();
  assert.throws(() => controller.configure({ seed: 4294967296 }));
  assert.deepEqual(controller.state(), before);
  assert.throws(() => controller.configure({ n: 0 }));
  assert.deepEqual(controller.state(), before);
});

test("snapshot import/export isolates ownership and invalid input is transactional", () => {
  const controller = new PackController();
  const snapshot = createGridPackStart(5);
  controller.load(parsePackSnapshot(JSON.parse(JSON.stringify(snapshot))));
  snapshot.container.side = 100;
  assert.equal(controller.state().configuration.startKind, "given");
  assert.equal(controller.export().container.side, 3);
  const state = controller.state();
  state.configuration.physics.jiggle = 999;
  state.snapshot.container.side = 200;
  assert.equal(controller.state().configuration.physics.jiggle, 20);
  assert.equal(controller.export().container.side, 3);
  assert.throws(() => controller.load({ ...snapshot, squareSide: Number.NaN }));
  assert.equal(controller.export().container.side, 3);
  assert.throws(() => parsePackSnapshot({ ...snapshot, poses: [{ x: "1", y: 1, angle: 0 }] }));
});

test("a container out of proportion to its squares is refused before it reaches a run", () => {
  const huge = {
    squareSide: 1,
    container: { originX: 0, originY: 0, side: 1e6 },
    poses: [{ x: 0.5, y: 0.5, angle: 0 }],
  };
  assert.throws(() => parsePackSnapshot(huge), {
    name: "RangeError",
    message:
      "Pack snapshot container side 1000000 is too large for n = 1 squares of side 1; the most accepted is 8",
  });
  const controller = new PackController();
  const before = controller.state();
  assert.throws(() => controller.load(huge), RangeError);
  assert.throws(() => new PackController({ startKind: "given", snapshot: huge }), RangeError);
  assert.deepEqual(controller.state(), before);

  // Four grid sides plus four squares, in the snapshot's own square units.
  assert.equal(maximumPackContainerSide(1, 1), 8);
  assert.equal(maximumPackContainerSide(17, 1), 24);
  assert.equal(maximumPackContainerSide(400, 1), 84);
  assert.equal(maximumPackContainerSide(17, 0.5), 12);
  const atBound = { ...huge, container: { originX: 0, originY: 0, side: 8 } };
  assert.equal(parsePackSnapshot(atBound).container.side, 8);
  const pastBound = { ...huge, container: { originX: 0, originY: 0, side: 8.000001 } };
  assert.throws(() => parsePackSnapshot(pastBound), RangeError);
  const scaled = { ...huge, squareSide: 1_000, container: { originX: 0, originY: 0, side: 8_000 } };
  assert.equal(parsePackSnapshot(scaled).container.side, 8_000);

  // Every start Pack makes for itself, and every run's own export, stays inside the bound.
  for (const n of [1, 2, 3, 17, 100, 325, 400]) {
    for (const startKind of ["grid", "random"] as const) {
      const run = new PackController({ n, seed: 3, startKind });
      const start = run.export();
      assert.ok(start.container.side <= maximumPackContainerSide(n, start.squareSide));
      run.step(10);
      assert.doesNotThrow(() => run.load(run.export()));
    }
  }
});

test("successful Resolve retains raw evidence and begins a fresh repaired phase", () => {
  const controller = new PackController({ n: 2, physics: { jiggle: 0, jiggleTorque: 0 } });
  const overlapping = {
    ...createGridPackStart(2),
    poses: [
      { x: 0.5, y: 0.5, angle: 0 },
      { x: 0.5, y: 0.5, angle: 0 },
    ],
  };
  controller.load(overlapping);
  const repair = controller.resolve();
  assert.equal(repair.raw.valid, false);
  assert.equal(repair.termination.resolved, true);
  assert.deepEqual(controller.export(), repair.repaired?.snapshot);
  assert.deepEqual(controller.state().repair, repair);
  assert.equal(controller.state().latest, null);
  assert.equal(controller.state().configuration.startKind, "given");
  assert.equal(controller.step(1).work.baseSteps, 1);
  assert.equal(controller.state().repair, null);
});

test("failed Resolve does not replace raw state", () => {
  const controller = new PackController({ n: 17, startKind: "random", seed: 7 });
  const before = controller.export();
  const repair = controller.resolve(1);
  assert.equal(repair.termination.resolved, false);
  assert.deepEqual(controller.export(), before);
  assert.deepEqual(repair.raw.snapshot, before);
});

test("Pack scene normalizes nonzero origins without altering numerical geometry", () => {
  const colours = createColourSystem({
    palette: ["#123456", "#234567", "#345678"],
    shades: ["#123456", "#234567", "#345678"].map((colour) =>
      Array.from({ length: 5 }, () => colour),
    ),
    angleToleranceDegrees: 0.5,
  });
  const snapshot = {
    squareSide: 0.5,
    container: { originX: 8, originY: -4, side: 2 },
    poses: [{ x: 9, y: -3, angle: Math.PI / 4 }],
  };
  const painted = paintPack(snapshot, colours);
  assert.equal(painted.scene.motion, "packing-snapshot");
  assert.deepEqual(painted.scene.squares[0], {
    index: 0,
    identity: 1,
    x: 1,
    y: 1,
    angleDegrees: 45,
    opacity: 1,
    scale: 0.5,
  });
  assert.equal(snapshot.poses[0]?.x, 9);
  assert.match(sceneSvg(painted), /svg/);
});
