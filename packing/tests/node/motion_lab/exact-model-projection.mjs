// The n = 5 motion lab's browser model, `exact-n5-model.js`, run on the manifest: for each
// scene, the poses it projects and predicts, its phases, its control state, and the text it
// gives the slider and the stage at 0%, 50% and 100%. Prints them as JSON, keyed by scene,
// for the Python test to compare with its own projection.
//
// Reads `{ model, manifest }` as JSON on stdin: the model's source exactly as the renderer
// inlines it, and the manifest the page carries.
import { readFileSync } from "node:fs";
import { runInThisContext } from "node:vm";

/** @typedef {{ id: string, mode: string }} Scene */

/** @type {{ model: string, manifest: { scenes: Scene[] } }} */
const { model, manifest } = JSON.parse(readFileSync(0, "utf8"));
// A classic script: its top-level functions become this realm's globals, as on the page.
runInThisContext(model, { filename: "exact-n5-model.js" });
/** @type {(scene: Scene, progress: number, tangent: boolean) => unknown} */
const posesAt = Reflect.get(globalThis, "posesAt");
/** @type {(scene: Scene, progress: number) => unknown} */
const phaseAt = Reflect.get(globalThis, "phaseAt");
/** @type {(scene: Scene) => unknown} */
const sceneControlState = Reflect.get(globalThis, "sceneControlState");
/** @type {(scene: Scene, progress: number) => unknown} */
const parameterValueText = Reflect.get(globalThis, "parameterValueText");
/** @type {(scene: Scene, progress: number) => unknown} */
const stageDescriptionText = Reflect.get(globalThis, "stageDescriptionText");

const progressValues = [0, 0.5, 1];
/** @type {Record<string, object>} */
const result = {};
for (const scene of manifest.scenes) {
  const useTangent = scene.mode === "second-order-obstruction";
  result[scene.id] = {
    projected: progressValues.map((progress) => posesAt(scene, progress, useTangent)),
    predictor: progressValues.map((progress) => posesAt(scene, progress, true)),
    phases: progressValues.map((progress) => phaseAt(scene, progress)),
    controls: sceneControlState(scene),
    parameterValueText: progressValues.map((progress) => parameterValueText(scene, progress)),
    stageDescriptions: progressValues.map((progress) => stageDescriptionText(scene, progress)),
  };
}
process.stdout.write(JSON.stringify(result));
