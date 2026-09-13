import type { AtlasAspect } from "../api/workbench-api.js";

const FINE_TRANSLATION = 0.05;
const COARSE_TRANSLATION = 0.2;
const ROTATION_STEP_DEGREES = 15;

export interface StageDescriptionInput {
  aspect: AtlasAspect;
  n: number;
  squareCount: number;
  containerSide: number;
  playing: boolean;
  edited: boolean;
}

/** Describe the current packing without announcing every animation frame. */
export function stageDescription(input: StageDescriptionInput): string {
  const activity = input.playing
    ? input.aspect === "pack"
      ? "The packing strategy is running."
      : "The transition is playing."
    : "Playback is paused.";
  const editing = input.edited ? "The arrangement has been edited by hand." : "";
  return [
    `${input.aspect === "pack" ? "Pack" : "Animate"} mode shows n = ${input.n}.`,
    `${input.squareCount} squares are inside a container of side ${input.containerSide.toFixed(4)}.`,
    activity,
    editing,
  ]
    .filter((part) => part.length > 0)
    .join(" ");
}

export type StageKeyCommand =
  | { kind: "focus-square" }
  | { kind: "move-square"; dx: number; dy: number }
  | { kind: "rotate-square"; degrees: number }
  | { kind: "leave-square" };

/** Map stage-local keys to the same edit operations as the pointer hand. */
export function stageKeyCommand(
  key: string,
  shiftKey: boolean,
  squareFocused: boolean,
): StageKeyCommand | null {
  if (!squareFocused) {
    return key === "Enter" ? { kind: "focus-square" } : null;
  }
  const amount = shiftKey ? COARSE_TRANSLATION : FINE_TRANSLATION;
  switch (key) {
    case "ArrowLeft":
      return { kind: "move-square", dx: -amount, dy: 0 };
    case "ArrowRight":
      return { kind: "move-square", dx: amount, dy: 0 };
    case "ArrowDown":
      return { kind: "move-square", dx: 0, dy: -amount };
    case "ArrowUp":
      return { kind: "move-square", dx: 0, dy: amount };
    case "q":
    case "Q":
      return { kind: "rotate-square", degrees: -ROTATION_STEP_DEGREES };
    case "e":
    case "E":
      return { kind: "rotate-square", degrees: ROTATION_STEP_DEGREES };
    case "Escape":
      return { kind: "leave-square" };
    default:
      return null;
  }
}

export interface ReducedMotionState {
  aspect: AtlasAspect;
  optimizing: boolean;
  pairIndex: number;
  firstPairIndex: number;
  lastPairIndex: number;
  atPairEnd: boolean;
}

export type ReducedMotionAction =
  | "initialize-pack"
  | "step-pack"
  | "finish-pair"
  | "finish-next-pair"
  | "restart-and-finish";

/** Plan one discrete transport press for a viewer who requests reduced motion. */
export function reducedMotionAction(state: ReducedMotionState): ReducedMotionAction {
  if (state.aspect === "pack") {
    return state.optimizing ? "step-pack" : "initialize-pack";
  }
  if (state.pairIndex < state.firstPairIndex || state.pairIndex > state.lastPairIndex) {
    return "restart-and-finish";
  }
  if (!state.atPairEnd) {
    return "finish-pair";
  }
  return state.pairIndex < state.lastPairIndex ? "finish-next-pair" : "restart-and-finish";
}

export const accessibility = Object.freeze({
  stageDescription,
  stageKeyCommand,
  reducedMotionAction,
});

export type AccessibilityModule = typeof accessibility;
