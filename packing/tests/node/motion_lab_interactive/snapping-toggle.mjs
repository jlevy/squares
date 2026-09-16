// The live motion lab's browser reducer toggles snapping without touching the state it was
// given, which the Python test holds against `snap.set_snapping`. Prints the flags as JSON.
//
// Reads `{ model }` as JSON on stdin: the model's source exactly as the page inlines it.
import { readFileSync } from "node:fs";
import { runInThisContext } from "node:vm";

/** @type {{ model: string }} */
const { model } = JSON.parse(readFileSync(0, "utf8"));
runInThisContext(model, { filename: "free-quench-model.js" });
/** @type {{ setSnapping(state: object, enabled: boolean): { snapping_enabled: boolean } }} */
const editor = Reflect.get(globalThis, "MotionLabEditor");
const base = {
  side: 3,
  squares: [{ square_id: 0, x: 0.5, y: 0.5, theta: 0 }],
  groups: [[0]],
  snapping_enabled: true,
};
const off = editor.setSnapping(base, false);
process.stdout.write(
  JSON.stringify({
    off: off.snapping_enabled,
    sourceUntouched: base.snapping_enabled,
    back: editor.setSnapping(off, true).snapping_enabled,
  }),
);
