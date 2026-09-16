import type {
  AtlasAspect,
  AtlasEdgeInput,
  AtlasGrowth,
  AtlasInitial,
  AtlasLawInput,
  AtlasPhase,
  AtlasRelationshipKind,
  AtlasScheme,
  AtlasStyle,
  AtlasTransitions,
} from "./workbench-api.ts";

/** A serialisable API command accepted by browser capture and screenshot tools. */
export type CaptureCommand =
  | ["clearEdges"]
  | ["dragTo", number, number, boolean]
  | ["goTo", number]
  | ["grabAt", number, number]
  | ["importAnimation", string, boolean?]
  | ["leaveAnimation"]
  | ["optimizeStep", number]
  | ["pause"]
  | ["play"]
  | ["playAll"]
  | ["playRange"]
  | ["refreshGap"]
  | ["seek", number]
  | ["seekAnimation", number]
  | ["seekScheduleMoveEnd"]
  | ["seekStepFraction", number]
  | ["select", number]
  | ["setAnneal", number]
  | ["setBlind", boolean]
  | ["setCapture", boolean]
  | ["setColorScheme", AtlasScheme]
  | ["setDesaturate", boolean]
  | ["setDrawing", boolean]
  | ["setEdges", AtlasEdgeInput]
  | ["setGrowth", Partial<Pick<AtlasGrowth, "on" | "size" | "rate" | "rule">>]
  | ["setInitial", AtlasInitial]
  | ["setLaw", AtlasLawInput]
  | ["setLawPreset", string]
  | ["setMode", AtlasAspect]
  | ["setOverlay", boolean]
  | ["setPhase", AtlasPhase]
  | ["setRange", number, number]
  | ["setRelationship", AtlasRelationshipKind]
  | ["setSnap", boolean]
  | ["setSpeed", number]
  | ["setStepN", number]
  | ["setStyle", AtlasStyle];

export type CaptureRead =
  | "animation"
  | "duration"
  | "exportAnimation"
  | "exportAnimationSvg"
  | "gap"
  | "pairs"
  | "sequenceDuration"
  | "state";

export interface CaptureControlRequest {
  /** Restore the capture tools' common baseline before applying commands. */
  prepare?: boolean;
  /** Whether the baseline hides the application chrome. Defaults to true. */
  capture?: boolean;
  commands?: CaptureCommand[];
  read?: CaptureRead[];
}

export interface CaptureControlResult {
  animation?: ReturnType<AtlasTransitions["animationState"]>;
  duration?: number;
  exportAnimation?: string;
  exportAnimationSvg?: string;
  gap?: ReturnType<AtlasTransitions["gapBar"]>;
  pairs?: ReturnType<AtlasTransitions["pairs"]>;
  sequenceDuration?: number;
  state?: ReturnType<AtlasTransitions["state"]>;
}

/**
 * The capture tools' common baseline: the catalogue's step into 17, paused at its start.
 *
 * It enters Animate first. `atlasTransitions` answers only while the catalogue owns the page,
 * and the page opens on the independent Pack panel, so a baseline that set its other settings
 * before entering Animate -- or that entered Pack, the catalogue's old home -- was refused at
 * its first call and no capture could start.
 */
function prepare(api: AtlasTransitions, capture: boolean): void {
  api.setMode("animate");
  api.stopAll();
  api.setCapture(false);
  api.setStyle("tween");
  api.setSnap(true);
  api.setBlind(false);
  api.setDesaturate(true);
  api.setAnneal(3);
  api.setSpeed(1);
  api.setInitial("previous");
  api.reset();
  api.setOverlay(false);
  api.setDrawing(false);
  api.clearEdges();
  api.setColorScheme("identity");
  api.setRange(17, 17);
  api.seek(0);
  api.setCapture(capture);
}

function apply(api: AtlasTransitions, command: CaptureCommand): void {
  switch (command[0]) {
    case "clearEdges":
      api.clearEdges();
      return;
    case "dragTo":
      api.dragTo(command[1], command[2], command[3]);
      return;
    case "goTo":
      api.goTo(command[1]);
      return;
    case "grabAt": {
      const index = api.pickAt(command[1], command[2]);
      api.grab(index, command[1], command[2]);
      return;
    }
    case "importAnimation":
      api.importAnimation(command[1], command[2]);
      return;
    case "leaveAnimation":
      api.leaveAnimation();
      return;
    case "optimizeStep":
      api.optimizeStep(command[1]);
      return;
    case "pause":
      api.pause();
      return;
    case "play":
      api.play();
      return;
    case "playAll":
      api.playAll();
      return;
    case "playRange":
      api.playRange();
      return;
    case "refreshGap":
      api.refreshGap();
      return;
    case "seek":
      api.seek(command[1]);
      return;
    case "seekAnimation":
      api.seekAnimation(command[1]);
      return;
    case "seekScheduleMoveEnd":
      api.seek(api.schedule().moveEnd);
      return;
    case "seekStepFraction":
      api.seek(api.duration() * command[1]);
      return;
    case "select":
      api.select(command[1]);
      return;
    case "setAnneal":
      api.setAnneal(command[1]);
      return;
    case "setBlind":
      api.setBlind(command[1]);
      return;
    case "setCapture":
      api.setCapture(command[1]);
      return;
    case "setColorScheme":
      api.setColorScheme(command[1]);
      return;
    case "setDesaturate":
      api.setDesaturate(command[1]);
      return;
    case "setDrawing":
      api.setDrawing(command[1]);
      return;
    case "setEdges":
      api.setEdges(command[1]);
      return;
    case "setGrowth":
      api.setGrowth(command[1]);
      return;
    case "setInitial":
      api.setInitial(command[1]);
      return;
    case "setLaw":
      api.setLaw(command[1]);
      return;
    case "setLawPreset":
      api.setLawPreset(command[1]);
      return;
    case "setMode":
      api.setMode(command[1]);
      return;
    case "setOverlay":
      api.setOverlay(command[1]);
      return;
    case "setPhase":
      api.setPhase(command[1]);
      return;
    case "setRange":
      api.setRange(command[1], command[2]);
      return;
    case "setRelationship":
      api.setRelationship(command[1]);
      return;
    case "setSnap":
      api.setSnap(command[1]);
      return;
    case "setSpeed":
      api.setSpeed(command[1]);
      return;
    case "setStepN":
      api.setStepN(command[1]);
      return;
    case "setStyle":
      api.setStyle(command[1]);
  }
}

/** Apply capture commands and return requested public-API state in one browser turn. */
export function control(
  api: AtlasTransitions,
  request: CaptureControlRequest,
): CaptureControlResult {
  if (request.prepare === true) {
    prepare(api, request.capture ?? true);
  }
  for (const command of request.commands ?? []) {
    apply(api, command);
  }
  const result: CaptureControlResult = {};
  for (const read of request.read ?? []) {
    switch (read) {
      case "animation":
        result.animation = api.animationState();
        break;
      case "duration":
        result.duration = api.duration();
        break;
      case "exportAnimation":
        result.exportAnimation = api.exportAnimation();
        break;
      case "exportAnimationSvg":
        result.exportAnimationSvg = api.exportAnimationSvg();
        break;
      case "gap":
        result.gap = api.gapBar();
        break;
      case "pairs":
        result.pairs = api.pairs();
        break;
      case "sequenceDuration":
        result.sequenceDuration = api.sequenceDuration();
        break;
      case "state":
        result.state = api.state();
    }
  }
  return result;
}
