import type { GeometrySnapshot } from "../core/geometry.ts";
import type { ColourSystem } from "./colour.ts";
import type { PaintedSceneFrame } from "./scene-types.ts";

/** Normalize display coordinates without modifying the measured source snapshot. */
export function paintPack(snapshot: GeometrySnapshot, colours: ColourSystem): PaintedSceneFrame {
  const { side, originX, originY } = snapshot.container;
  const padding = side * 0.07;
  const angles = snapshot.poses.map((pose) => (pose.angle * 180) / Math.PI);
  return {
    fills: colours.atlasFills(angles),
    scene: {
      pairIndex: 0,
      n: snapshot.poses.length,
      containerSide: side,
      viewBox: { x: -padding, y: -side - padding, size: side + 2 * padding },
      squares: snapshot.poses.map((pose, index) => ({
        index,
        identity: index + 1,
        x: pose.x - originX,
        y: pose.y - originY,
        angleDegrees: (pose.angle * 180) / Math.PI,
        opacity: 1,
        scale: snapshot.squareSide,
      })),
      presentation: {
        drain: 0,
        newTint: 0,
        resting: 1,
        homeward: false,
        mark: null,
        linksOpacity: 0,
        ghostOpacity: 0,
      },
      motion: "packing-snapshot",
    },
  };
}
