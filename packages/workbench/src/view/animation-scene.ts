import type { AnimationSample } from "../animation/trace.js";
import { measurePackingGeometry } from "../core/geometry.ts";
import type { AnimationDocument } from "../data/animation.js";
import type { ColourSystem } from "./colour.js";
import type { PaintedSceneFrame } from "./scene-types.js";

/** Trace playback is presentation; even feasible keyframes do not certify an interpolated pose. */
export function paintAnimation(
  sample: AnimationSample,
  document: AnimationDocument,
  colours: ColourSystem,
): PaintedSceneFrame {
  const hue = document.palette?.hue ?? "angle-class";
  const shade = document.palette?.shade ?? "full-side-contact";
  const angles = sample.squares.map((square) => (square.angle * 180) / Math.PI);
  const geometry = measurePackingGeometry(
    {
      squareSide: 1,
      container: { originX: 0, originY: 0, side: sample.side },
      poses: sample.squares,
    },
    { gap: 0.004, angleToleranceRadians: (colours.angleToleranceDegrees * Math.PI) / 180 },
  );
  const contacts = shade === "full-side-contact" ? geometry.contacts : undefined;
  const angleFills = colours.atlasFills(angles, contacts);
  const fills = sample.squareIds.map((identity, index) => {
    const base =
      hue === "identity"
        ? colours.identityFill(identity)
        : hue === "uniform"
          ? colours.identityFill(1)
          : angleFills[index];
    if (base === undefined) {
      throw new RangeError("animation palette is missing a square");
    }
    const shaded =
      shade === "full-side-contact" && hue !== "angle-class"
        ? colours.mix(base, "#000000", Math.min(4, contacts?.[index] ?? 0) * 0.08)
        : base;
    const muted = sample.assessment?.valid !== true || sample.locked?.[index] === false;
    return shade === "evidence" && muted ? colours.desaturate(shaded, 1, 0.12) : shaded;
  });
  const padding = sample.side * 0.07;
  return {
    fills,
    scene: {
      pairIndex: 0,
      n: sample.n,
      containerSide: sample.side,
      viewBox: { x: -padding, y: -sample.side - padding, size: sample.side + 2 * padding },
      squares: sample.squares.map((square, index) => {
        const identity = sample.squareIds[index];
        if (identity === undefined) {
          throw new RangeError("animation is missing a square identity");
        }
        return {
          index,
          identity,
          x: square.x,
          y: square.y,
          angleDegrees: (square.angle * 180) / Math.PI,
          opacity: 1,
          scale: 1,
        };
      }),
      presentation: {
        drain: 0,
        newTint: 0,
        resting: 1,
        homeward: false,
        mark: null,
        linksOpacity: 0,
        ghostOpacity: 0,
      },
      motion: "direct-illustration",
    },
  };
}
