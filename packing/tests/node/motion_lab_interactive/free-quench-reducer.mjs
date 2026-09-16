// The live motion lab's browser model, `free-quench-model.js`: one reducer snaps, rotates and
// releases, playback keeps the events that matter, and the timeline windows a long run.
// Prints what the Python test asserts on, as JSON.
//
// Reads `{ model }` as JSON on stdin: the model's source exactly as the page inlines it.
import { readFileSync } from "node:fs";
import { runInThisContext } from "node:vm";

/** @type {{ model: string }} */
const { model } = JSON.parse(readFileSync(0, "utf8"));
runInThisContext(model, { filename: "free-quench-model.js" });
/** @type {any} */
const editor = Reflect.get(globalThis, "MotionLabEditor");
const baseline = {
  side: 3,
  squares: [
    { square_id: 0, x: 0.5, y: 1.5, theta: 0 },
    { square_id: 1, x: 1.51, y: 1.5, theta: 0 },
  ],
  groups: [[0], [1]],
  snapping_enabled: true,
};
const snapped = editor.applyBestSnap(baseline, 1, 0.05);
const before = Math.hypot(
  snapped.state.squares[0].x - snapped.state.squares[1].x,
  snapped.state.squares[0].y - snapped.state.squares[1].y,
);
const rotated = editor.rotateGroup(snapped.state, 1, Math.PI / 3);
const after = Math.hypot(
  rotated.squares[0].x - rotated.squares[1].x,
  rotated.squares[0].y - rotated.squares[1].y,
);
const request = editor.releaseQuenchRequest(rotated, 3, 4);
const longEvents = Array.from({ length: 2651 }, (_, index) => {
  let phase = index % 2 ? "fixed-angle-lp" : "angular-probe";
  if (index === 0) {
    phase = "setup";
  }
  if (index === 177) {
    phase = "angle-accepted";
  }
  if (index === 2650) {
    phase = "stop";
  }
  return { phase };
});
const playback = editor.selectPlaybackIndices(longEvents, 160);
const windowed = editor.timelineWindow(longEvents.length, 1300, 20);
process.stdout.write(
  JSON.stringify({
    snapped,
    before,
    after,
    request,
    fixed: editor.phasePresentation({ phase: "fixed-angle-lp" }),
    probe: editor.phasePresentation({ phase: "angular-probe", outcome: "rejected" }),
    playback,
    windowed,
  }),
);
