import assert from "node:assert/strict";
import { test } from "node:test";
import {
  appendPackStartCandidateCount,
  createAppendPackStart,
} from "../src/simulation/start-proposals.ts";

test("append proposal recenters the previous snapshot and preserves deterministic scan ties", () => {
  const proposal = createAppendPackStart(
    {
      squareSide: 1,
      container: { originX: 5, originY: -2, side: 1 },
      poses: [{ x: 5.5, y: -1.5, angle: 0.25 }],
    },
    3,
    { gridStep: 1 },
  );
  assert.deepEqual(proposal, {
    squareSide: 1,
    container: { originX: 0, originY: 0, side: 3 },
    poses: [
      { x: 1.5, y: 1.5, angle: 0.25 },
      { x: 0.5, y: 0.5, angle: 0 },
    ],
  });
  assert.equal(appendPackStartCandidateCount(3, 1, 1), 9);
});

test("append proposal rejects empty, nonfinite and shrinking sources", () => {
  assert.throws(
    () =>
      createAppendPackStart(
        {
          squareSide: 1,
          container: { originX: 0, originY: 0, side: 1 },
          poses: [],
        },
        2,
      ),
    /nonempty/,
  );
  assert.throws(
    () =>
      createAppendPackStart(
        {
          squareSide: 1,
          container: { originX: 0, originY: 0, side: 2 },
          poses: [{ x: Number.NaN, y: 0.5, angle: 0 }],
        },
        2,
      ),
    /finite/,
  );
  assert.throws(
    () =>
      createAppendPackStart(
        {
          squareSide: 1,
          container: { originX: 0, originY: 0, side: 2 },
          poses: [{ x: 0.5, y: 0.5, angle: 0 }],
        },
        1.5,
      ),
    /smaller/,
  );
  assert.throws(() => appendPackStartCandidateCount(3, 1, 1e-9), /limited/);
});
