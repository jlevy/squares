import type { AtlasAspect, AtlasStyle } from "../api/workbench-api.js";

export interface StepRange {
  from: number;
  to: number;
}

export interface NormalizedRange extends StepRange {
  collapsed: boolean;
  forcedAspect: AtlasAspect | null;
}

export interface PairIndexBounds {
  first: number;
  last: number;
}

function supportedAt(supportedSteps: readonly number[], index: number): number {
  const value = supportedSteps[index];
  if (value === undefined) {
    throw new RangeError("the workbench requires at least one supported packing size");
  }
  return value;
}

function roundedOr(value: unknown, fallback: number): number {
  const numeric = Number(value);
  return Number.isFinite(numeric) ? Math.round(numeric) : fallback;
}

/** Return the first nearest supported packing size, preserving legacy tie-breaking. */
export function nearestSupportedIndex(
  supportedSteps: readonly number[],
  requested: number,
): number {
  supportedAt(supportedSteps, 0);
  let best = 0;
  let distance = Infinity;
  for (let index = 0; index < supportedSteps.length; index += 1) {
    const candidate = supportedAt(supportedSteps, index);
    const nextDistance = Math.abs(candidate - requested);
    if (nextDistance < distance) {
      best = index;
      distance = nextDistance;
    }
  }
  return best;
}

/** Clamp a requested range and snap a collapsed range to a size the data actually carries. */
export function normalizeRange(
  supportedSteps: readonly number[],
  current: StepRange,
  requestedFrom: unknown,
  requestedTo: unknown,
): NormalizedRange {
  const minimum = supportedAt(supportedSteps, 0);
  const maximum = supportedAt(supportedSteps, supportedSteps.length - 1);
  let from = roundedOr(requestedFrom, current.from);
  let to = roundedOr(requestedTo, current.to);
  from = Math.max(minimum, Math.min(maximum, from));
  to = Math.max(from, Math.min(maximum, to));
  const collapsed = from === to;
  if (collapsed) {
    from = supportedAt(supportedSteps, nearestSupportedIndex(supportedSteps, from));
    to = from;
  }
  return {
    from,
    to,
    collapsed,
    forcedAspect: collapsed ? null : "animate",
  };
}

/** Find the carried pair indices for a range, falling back to one nearest sparse step. */
export function rangeIndexBounds(
  supportedSteps: readonly number[],
  range: StepRange,
): PairIndexBounds {
  supportedAt(supportedSteps, 0);
  let first = -1;
  let last = -1;
  for (let index = 0; index < supportedSteps.length; index += 1) {
    const step = supportedAt(supportedSteps, index);
    if (step >= range.from && step <= range.to) {
      if (first < 0) {
        first = index;
      }
      last = index;
    }
  }
  if (first < 0) {
    const nearest = nearestSupportedIndex(supportedSteps, range.to);
    return { first: nearest, last: nearest };
  }
  return { first, last };
}

export interface AspectTransitionInput {
  currentAspect: AtlasAspect;
  currentRange: StepRange;
  currentStepN: number;
  rememberedPackN: number | null;
  rememberedAnimateRange: StepRange | null;
  supportedSteps: readonly number[];
  target: string;
}

export interface AspectTransition {
  changed: boolean;
  aspect: AtlasAspect;
  range: StepRange;
  pairIndex: number;
  rememberedPackN: number | null;
  rememberedAnimateRange: StepRange | null;
}

/** Plan a Pack/Animate switch without touching simulation or the DOM. */
export function planAspectTransition(input: AspectTransitionInput): AspectTransition {
  const aspect: AtlasAspect =
    input.target === "animate" || input.target === "sweep" ? "animate" : "pack";
  if (aspect === input.currentAspect) {
    return {
      changed: false,
      aspect,
      range: { ...input.currentRange },
      pairIndex: nearestSupportedIndex(input.supportedSteps, input.currentStepN),
      rememberedPackN: input.rememberedPackN,
      rememberedAnimateRange: input.rememberedAnimateRange,
    };
  }

  let rememberedPackN = input.rememberedPackN;
  let rememberedAnimateRange = input.rememberedAnimateRange;
  let requested: StepRange;
  if (input.currentAspect === "pack") {
    rememberedPackN = input.currentStepN;
  } else {
    rememberedAnimateRange = { ...input.currentRange };
  }
  if (aspect === "pack") {
    const packN = rememberedPackN ?? input.currentStepN;
    requested = { from: packN, to: packN };
  } else {
    requested = rememberedAnimateRange ?? {
      from: supportedAt(input.supportedSteps, 0),
      to: supportedAt(input.supportedSteps, input.supportedSteps.length - 1),
    };
  }
  const range = normalizeRange(
    input.supportedSteps,
    input.currentRange,
    requested.from,
    requested.to,
  );
  return {
    changed: true,
    aspect,
    range: { from: range.from, to: range.to },
    pairIndex: rangeIndexBounds(input.supportedSteps, range).first,
    rememberedPackN,
    rememberedAnimateRange,
  };
}

/** Solver choices that have meaning in each aspect. */
export function availableStyles(aspect: AtlasAspect): AtlasStyle[] {
  return aspect === "pack" ? ["physics", "bodies"] : ["tween", "physics", "bodies"];
}

export interface TransportState {
  aspect: AtlasAspect;
  playing: boolean;
  optimizing: boolean;
  continuous: boolean;
  pairIndex: number;
  firstPairIndex: number;
  lastPairIndex: number;
  atEnd: boolean;
}

export type TransportIntent =
  | "pause"
  | "resume-pack"
  | "start-pack"
  | "start-range"
  | "resume-animation";

/** Turn the shared transport button's state into one explicit application action. */
export function transportIntent(state: TransportState): TransportIntent {
  if (state.playing) {
    return "pause";
  }
  if (state.optimizing) {
    return "resume-pack";
  }
  if (state.aspect === "pack") {
    return "start-pack";
  }
  if (
    state.lastPairIndex > state.firstPairIndex &&
    (!state.continuous || (state.pairIndex >= state.lastPairIndex && state.atEnd))
  ) {
    return "start-range";
  }
  return "resume-animation";
}

export const navigation = Object.freeze({
  nearestSupportedIndex,
  normalizeRange,
  rangeIndexBounds,
  planAspectTransition,
  availableStyles,
  transportIntent,
});

export type NavigationModule = typeof navigation;
