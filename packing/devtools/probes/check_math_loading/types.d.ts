// The instrumentation `check_math_loading`'s init scripts install and its own and
// `check_math_faces`'s probes read.

/** `hold_fonts`: holds font loads until released. */
interface SquaresMathLoadControl {
  heldLoads: number;
  released: boolean;
  release(): void;
  nativeLoad: FontFaceSet["load"];
  timing: {
    started: number;
    firstFontCall: number | null;
    firstHeldLoad: number | null;
    domContentLoaded: number | null;
    earlyEventsStarted: number | null;
    earlyEventsCompleted: number | null;
    released: number | null;
  };
}

/** `first_paint`: what the frame sampler has seen. */
interface SquaresMathLoadingState {
  frames: number;
  mathFontChecks: number;
  unreadyMath: string[];
  earlyMath: string | null;
  fallback: string | null;
  stop: boolean;
}

/** `first_paint`: the fonts at the first frame a formula was exposed. */
interface SquaresMathFirstPaint {
  at: number;
  faces: SquaresFontFaceSummary[];
  required: SquaresFontRequirement[];
}

declare var __mathLoadControl: SquaresMathLoadControl | undefined;
declare var __mathLoadingState: SquaresMathLoadingState | undefined;
declare var __mathFirstPaint: SquaresMathFirstPaint | null | undefined;
