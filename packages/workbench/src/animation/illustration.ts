import type { AtlasPhase } from "../api/workbench-api.js";
import type { CorpusBlock } from "../data/corpus.js";
import type { SceneFrame, SceneMark, SceneSquare } from "../view/scene-types.js";
import { type PairSchedule, phaseProgress, ramp } from "./timeline.ts";

export type DegreePose = readonly [number, number, number, ...unknown[]];

/** A prepared correspondence keeps block construction outside the per-frame path. */
export interface MotionTrack {
  ident: number;
  a: DegreePose;
  b: DegreePose;
  turn: number;
  block: Pick<CorpusBlock, "turn" | "from" | "to"> | null;
  dx: number;
  dy: number;
  rx: number;
  ry: number;
}

export interface IllustrationInput {
  pairIndex: number;
  n: number;
  fromSide: number;
  toSide: number;
  tracks: readonly MotionTrack[];
  arriving: { identity: number; pose: DegreePose };
  previousIndex: number | null;
  phase: AtlasPhase;
  schedule: PairSchedule;
  seconds: number;
  moveSeconds: number;
  padding: number;
  drain: number;
  resting: number;
  links: boolean;
  tint: number;
  mark: { wide: number; thin: number; fade: number };
}

function lerp(from: number, to: number, progress: number): number {
  return from + (to - from) * progress;
}

function easeOut(progress: number): number {
  return 1 - (1 - progress) ** 3;
}

/** Block rotation and residual translation are independent of drawing and simulation. */
export function interpolateBlockPose(
  track: MotionTrack,
  progress: { rot: number; slide: number },
): [number, number, number] {
  if (track.block === null) {
    return [
      lerp(track.a[0], track.b[0], progress.slide),
      lerp(track.a[1], track.b[1], progress.slide),
      track.a[2] + track.turn * progress.rot,
    ];
  }
  const angle = (track.block.turn * progress.rot * Math.PI) / 180;
  const cosine = Math.cos(angle);
  const sine = Math.sin(angle);
  return [
    lerp(track.block.from[0], track.block.to[0], progress.slide) +
      cosine * track.dx -
      sine * track.dy +
      track.rx * progress.slide,
    lerp(track.block.from[1], track.block.to[1], progress.slide) +
      sine * track.dx +
      cosine * track.dy +
      track.ry * progress.slide,
    track.a[2] + track.turn * progress.rot,
  ];
}

function previousMark(input: IllustrationInput, squares: readonly SceneSquare[]): SceneMark | null {
  if (input.previousIndex === null) {
    return null;
  }
  const previous = squares[input.previousIndex];
  if (previous === undefined) {
    throw new RangeError("previous square is absent from the illustration");
  }
  const fade = input.moveSeconds * input.mark.fade;
  const gone = ramp(input.seconds, input.schedule.moveStart, input.schedule.moveStart + fade);
  return gone >= 1 ? null : { ...previous, opacity: 1 - gone, strokeWidth: input.mark.thin };
}

/** Sampling a direct illustration never calls a solver and never grants evidence. */
export function illustrationFrame(input: IllustrationInput): SceneFrame {
  const { schedule, seconds } = input;
  const progress = ramp(seconds, schedule.blocksStart, schedule.blocksEnd);
  const phased = phaseProgress(input.phase, progress);
  const arrival = easeOut(ramp(seconds, schedule.arrive, schedule.arrived));
  const growth =
    input.phase === "add-then-move"
      ? phaseProgress("simultaneous", ramp(seconds, schedule.arrive, schedule.arrived)).e
      : phased.e;
  const side = lerp(input.fromSide, input.toSide, growth);
  const view = side * (1 + 2 * input.padding);
  const squares: SceneSquare[] = input.tracks.map((track, index) => {
    const [x, y, angleDegrees] = interpolateBlockPose(track, phased);
    return { index, identity: track.ident, x, y, angleDegrees, opacity: 1, scale: 1 };
  });
  const arriving: SceneSquare = {
    index: squares.length,
    identity: input.arriving.identity,
    x: input.arriving.pose[0],
    y: input.arriving.pose[1],
    angleDegrees: input.arriving.pose[2],
    opacity: arrival,
    scale: arrival > 0 ? lerp(0.8, 1, arrival) : 1,
  };
  const settled = easeOut(ramp(seconds, schedule.moveEnd, schedule.end));
  const mark: SceneMark | null =
    arrival > 0
      ? {
          ...arriving,
          strokeWidth: lerp(input.mark.wide, input.mark.thin, settled),
        }
      : previousMark(input, squares);
  squares.push(arriving);
  return {
    pairIndex: input.pairIndex,
    n: input.n,
    containerSide: side,
    viewBox: { x: side / 2 - view / 2, y: -side / 2 - view / 2, size: view },
    squares,
    presentation: {
      drain: input.drain,
      newTint: arrival > 0 ? input.tint * (1 - settled) : 0,
      resting: input.resting,
      homeward: seconds >= schedule.moveEnd,
      mark,
      linksOpacity: input.links ? (progress <= 0 ? 0.35 : 1 - phased.e) : 0,
      ghostOpacity: input.links ? (seconds > schedule.moveStart ? 1 - arrival : 0) : 0,
    },
    motion: "direct-illustration",
  };
}
