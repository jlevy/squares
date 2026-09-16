import type { PackingAssessment, SquarePose } from "../core/runtime-contracts.js";
import type { AnimationDocument, AnimationFrame } from "../data/animation.js";

export interface AnimationSample {
  n: number;
  side: number;
  squares: SquarePose[];
  squareIds: number[];
  locked: boolean[] | null;
  guided: boolean;
  phase: string;
  label: string | null;
  interpolated: boolean;
  /** A keyframe's check does not transfer to interpolated geometry. */
  assessment: PackingAssessment | null;
}

function keyframe(n: number, frame: AnimationFrame): AnimationSample {
  return {
    n,
    side: frame.side,
    squares: frame.squares.map((pose) => ({ ...pose })),
    squareIds: [...frame.squareIds],
    locked: frame.locked === null ? null : [...frame.locked],
    guided: frame.guided,
    phase: frame.phase,
    label: frame.label,
    interpolated: false,
    assessment: frame.assessment,
  };
}

function lerp(from: number, to: number, progress: number): number {
  return from + (to - from) * progress;
}

/** Deterministic trace replay: equal-time keyframes select the last frame at that time. */
export function sampleAnimation(document: AnimationDocument, logicalTime: number): AnimationSample {
  if (!Number.isFinite(logicalTime)) {
    throw new RangeError("animation time must be finite");
  }
  const time = Math.max(0, Math.min(1, logicalTime));
  let from = document.frames[0];
  if (from === undefined) {
    throw new RangeError("animation has no frames");
  }
  if (time < from.t) {
    return keyframe(document.n, from);
  }
  for (const to of document.frames.slice(1)) {
    if (to.t <= time) {
      from = to;
      continue;
    }
    if (time === from.t) {
      return keyframe(document.n, from);
    }
    const progress = (time - from.t) / (to.t - from.t);
    return {
      n: document.n,
      side: lerp(from.side, to.side, progress),
      squares: from.squares.map((pose, index) => {
        const target = to.squares[index];
        if (target === undefined) {
          throw new RangeError("animation frame lost a square");
        }
        return {
          x: lerp(pose.x, target.x, progress),
          y: lerp(pose.y, target.y, progress),
          // Recorded radians retain full turns; do not silently choose a shorter rotation.
          angle: lerp(pose.angle, target.angle, progress),
        };
      }),
      squareIds: [...from.squareIds],
      locked: null,
      guided: from.guided || to.guided,
      phase: from.phase,
      label: from.label,
      interpolated: true,
      assessment: null,
    };
  }
  return keyframe(document.n, from);
}
