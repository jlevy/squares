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

const PACK_FINE_TRANSLATION = 0.05;
const PACK_COARSE_TRANSLATION = 0.25;
/** Five degrees. */
const PACK_ROTATION_STEP = Math.PI / 36;

/** One key press as a handler sees it; a `KeyboardEvent` is one. */
export interface KeyChord {
  key: string;
  shiftKey: boolean;
  ctrlKey: boolean;
  metaKey: boolean;
  altKey: boolean;
}

export type PackKeyCommand =
  | { kind: "focus-square" }
  | { kind: "toggle-playback" }
  | { kind: "move-square"; dx: number; dy: number }
  | { kind: "rotate-square"; radians: number }
  | { kind: "cycle-square"; offset: 1 | -1 }
  | { kind: "leave-square" };

/**
 * The Pack panel's one key map, for the stage and for a focused square.
 *
 * A shortcut is a bare key: with Ctrl, Meta or Alt held the key belongs to the browser or
 * the system (Cmd+[ is Back, Ctrl+PageDown changes tab), so every such chord maps to
 * nothing and the handler lets it pass. Shift is part of the map: it selects the coarse
 * stride, and it is how Q and E arrive capitalised, which rotate the same way.
 */
export function packKeyCommand(chord: KeyChord, squareFocused: boolean): PackKeyCommand | null {
  if (chord.ctrlKey || chord.metaKey || chord.altKey) {
    return null;
  }
  if (!squareFocused) {
    switch (chord.key) {
      case "Enter":
        return { kind: "focus-square" };
      case " ":
        return { kind: "toggle-playback" };
      default:
        return null;
    }
  }
  const stride = chord.shiftKey ? PACK_COARSE_TRANSLATION : PACK_FINE_TRANSLATION;
  switch (chord.key) {
    case "ArrowLeft":
      return { kind: "move-square", dx: -stride, dy: 0 };
    case "ArrowRight":
      return { kind: "move-square", dx: stride, dy: 0 };
    case "ArrowUp":
      return { kind: "move-square", dx: 0, dy: stride };
    case "ArrowDown":
      return { kind: "move-square", dx: 0, dy: -stride };
    case "q":
    case "Q":
      return { kind: "rotate-square", radians: -PACK_ROTATION_STEP };
    case "e":
    case "E":
      return { kind: "rotate-square", radians: PACK_ROTATION_STEP };
    case "PageDown":
    case "]":
      return { kind: "cycle-square", offset: 1 };
    case "PageUp":
    case "[":
      return { kind: "cycle-square", offset: -1 };
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
