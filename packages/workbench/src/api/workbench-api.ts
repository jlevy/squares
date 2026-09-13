/**
 * Public browser API for the packing workbench.
 *
 * This module is the authoritative type contract for the page, probes, capture tools, and
 * browser-driven measurements. The implementation object in the live workbench is checked against
 * this interface; the legacy probe declaration only installs it on `Window`.
 */

/** Which aspect the page is showing: one n optimised, or a range animated end to end. */
export type AtlasAspect = "pack" | "animate";

/** The solvers. `tween` interpolates toward the record; the other two run the physics. */
export type AtlasStyle = "tween" | "physics" | "bodies";

/** What the physics is told about where the squares are meant to end up. */
export type AtlasSimMode = "snap" | "free" | "blind";

/** How a step's motion is staged. The page reads these from its own data (`motion_phases`). */
export type AtlasPhase =
  | "add-then-move"
  | "move-then-add"
  | "simultaneous"
  | "rotate-first"
  | "slide-first";

/** How a square takes its colour. */
export type AtlasScheme = "identity" | "angle-stable" | "angle-continuous";

/** The selected schemes plus the atlas palette used for an Animate rest frame. */
export type AtlasPaintScheme = AtlasScheme | "angle-atlas";

/** What an open-ended run starts from. */
export type AtlasInitial = "previous" | "random" | "grid" | "record";

/** Who attracts whom. Repulsion is never masked. */
export type AtlasRelationshipKind = "general" | "groups" | "contact";

/** Where the target contact graph comes from. */
export type AtlasTargetSource = "record" | "drawn";

/**
 * What the target graph is, which is the source unless a caller has handed one in: `setTargetGraph`
 * overrides the source for as long as it holds, and reports itself as `given`.
 */
export type AtlasTargetFrom = AtlasTargetSource | "given";

/** How the squares grow. */
export type AtlasGrowthRule = "constant" | "clean";

/** What a step is, in the corpus the page carries. */
export type AtlasPairKind = "matched" | "prefix" | "shared-picture";

// ---------------------------------------------------------------- the shapes it hands back

/** The three beats of a step, in seconds. */
export interface AtlasTiming {
  dwell: number;
  move: number;
  /** Final guided correction after free movement, before the settle. */
  correct: number;
  settle: number;
}

/** One law's four parameters. The same shape describes the pair law and the wall law. */
export interface AtlasLaw {
  rigidity: number;
  repulsion: number;
  attraction: number;
  range: number;
}

/**
 * A law as a caller may hand one in.
 *
 * The values are `unknown` because that is what `setLawOf` accepts: it reads each key it knows,
 * puts it through `Number`, and drops it where the result is not finite. So a string, a NaN or a
 * missing key all mean "leave this parameter alone" -- which is exactly what
 * `law/clamps-and-round-trips` puts to the page.
 */
export type AtlasLawInput = { [K in keyof AtlasLaw]?: unknown };

/** Each law parameter's [low, high], which is also what the sliders are built from. */
export interface AtlasLawBounds {
  rigidity: [number, number];
  repulsion: [number, number];
  attraction: [number, number];
  range: [number, number];
}

/** The pair law, with what it implies about the picture. */
export interface AtlasLawState extends AtlasLaw {
  /** The slope past the knee, which is zero once the rigidity is above the tolerance. */
  steep: number;
  bounds: AtlasLawBounds;
  defaults: AtlasLaw;
  presets: string[];
  /** What a run is keyed by: two runs with the same key draw the same trajectory. */
  key: string;
  pushAtKnee: number;
  pullPeak: number;
}

/** The range -- the page's one spine -- and where the step on the stage sits inside it. */
export interface AtlasRange {
  from: number;
  to: number;
  first: number;
  last: number;
  steps: number;
  span: number;
  /** 1-based position inside the range, or 0 when the step on the stage is outside it. */
  step: number;
  inside: boolean;
  duration: number;
  min: number;
  max: number;
}

/** The annealing dial, and what the level it is on means. */
export interface AtlasAnneal {
  level: number;
  min: number;
  max: number;
  dflt: number;
  amplitude: number;
  decayPower: number;
  span: number;
  move: number;
  steps: number;
}

/** What the gap bar is showing, which is keyed to the n on the panel. */
export interface AtlasGapBar {
  n: number;
  record: number;
  lower: number;
  lo: number;
  hi: number;
  side: number;
  /** Where the hand sits along the bar, as a fraction. */
  x: number;
  excess: number;
  met: boolean;
  /** Whether `side` is a claim at all: only an arrangement without overlaps is a packing. */
  valid: boolean;
  overlap: number;
}

/** What the frame was painted from, and what the painter measured while it painted. */
export interface AtlasColour {
  overlap: number;
  deepestOverlap: number;
  overlapPairs: number;
  /** The scheme chosen, and the one this frame was actually painted in. */
  scheme: AtlasScheme;
  painted: AtlasPaintScheme;
  schemes: AtlasScheme[];
  greens: string[];
  greenStride: number;
  animateStandardize: boolean;
  /** How many angle classes the frame's angles fell into. */
  classes: number;
  centres: number[];
  sizes: number[];
  slots: number[];
  contacts: number[];
  tolerance: number;
  contactGap: number;
  palette: string[];
  shades: string[][];
  /** The fill of every drawn square, read back off the stage. */
  fills: (string | null)[];
}

/** The relationship graph: what is being attracted, and how much of it the picture has realised. */
export interface AtlasRelationship {
  kind: AtlasRelationshipKind;
  kinds: AtlasRelationshipKind[];
  target: AtlasTargetFrom;
  sources: AtlasTargetSource[];
  /** How many edges the hand-drawn graph holds for this step. */
  drawn: number;
  key: string;
  edges: number;
  met: number;
  fraction: number;
  /** The mask in force, or null under `general`, where nothing is masked. */
  maskEdges: number | null;
  frameEdges: number;
  side: number;
  record: number;
  attracting: boolean;
}

/** Start small and grow: the dial, and what the arrangement under it has reached. */
export interface AtlasGrowth {
  on: boolean;
  size: number;
  rate: number;
  rule: AtlasGrowthRule;
  rules: AtlasGrowthRule[];
  bounds: { size: [number, number]; rate: [number, number] };
  defaults: { on: boolean; size: number; rate: number; rule: AtlasGrowthRule };
  growing: boolean;
  stalled: boolean;
  done: boolean;
  /** The numbers below need a run to exist; without one they are null. */
  side: number | null;
  sideAtSize: number | null;
  unitSide: number | null;
  record: number;
  penetration: number | null;
  clean: boolean;
  packing: boolean;
  suspect: boolean;
  excess: number | null;
}

/** The container used when the optimizer admitted one exact packing snapshot. */
export interface AtlasPackingContainer {
  originX: number;
  originY: number;
  side: number;
}

/** A copied unit-square pose set retained at the instant it ranked. Angles are degrees. */
export interface AtlasBestPacking {
  seed: number;
  at: number;
  required: number;
  squareSide: 1;
  container: AtlasPackingContainer;
  poses: [number, number, number][];
  maxPairOverlap: number;
  maxWallOverlap: number;
}

/**
 * The open-ended run.
 *
 * With no run on the stage only the first three are reported, so everything a run carries is
 * optional here -- that is not a hedge, it is the two shapes `optimizeState()` actually returns.
 */
export interface AtlasOptimize {
  on: boolean;
  initial: AtlasInitial;
  edited: boolean;
  running?: boolean;
  /** Whether the run is pulled toward the record's poses, or finding the packing itself. */
  springs?: boolean;
  n?: number;
  pair?: number;
  time?: number;
  steps?: number;
  side?: number;
  required?: number;
  size?: number;
  /** The smallest box the run has held the squares in without overlap; null until it has one. */
  best?: number | null;
  bestAt?: number;
  bestPenetration?: number | null;
  bestWallPenetration?: number | null;
  /** The exact copied pose, size and container snapshot underlying `best`. */
  bestPacking?: AtlasBestPacking | null;
  feasible?: number;
  /** The unsigned 32-bit seed this run was created with. */
  seed?: number;
  record?: number;
  excess?: number;
  penetration?: number | null;
  /** Pair overlap recomputed after integration on the pose being reported. */
  exactPenetration?: number | null;
  /** Wall overhang recomputed after integration on the pose being reported. */
  wallPenetration?: number | null;
  /** True only when the reported pose is a valid packing of unit squares. */
  packing?: boolean;
  invalidReason?: string | null;
  near?: number;
  held?: number;
  msPerStep?: number;
}

/** The hand: which square it holds, and how. */
export interface AtlasHand {
  held: number;
  /** Undefined when there is no run to have edited. */
  edited: boolean | undefined;
  rotating: boolean;
}

/** Where a dragged square was put. */
export interface AtlasDrag {
  index: number;
  x: number;
  y: number;
  /** Degrees, which is what the stage draws in. */
  angle: number;
}

/** An edge under the cursor, mid-gesture. */
export interface AtlasLinkDrag {
  from: number;
  x: number;
  y: number;
}

/** What dropping an edge did, and the graph it left. */
export interface AtlasLinkEnd {
  added: boolean;
  from?: number;
  to?: number;
  edges: [number, number][];
}

/** What a run reached, measured against the record it was aiming at. */
export interface AtlasMiss {
  /** The largest distance a square's centre ends from the record's. */
  centre: number;
  /** The largest angle error, modulo a quarter turn. */
  angle: number;
  side: number;
  record: number;
  excess: number;
}

/** One cached trajectory, reported. */
export interface AtlasPhysics {
  pair: number;
  n: number;
  style: AtlasStyle;
  mode: AtlasSimMode;
  bodies: number;
  steps: number;
  ms: number;
  bytes: number;
  maxSpeedPerMove: number;
  maxPenetration: number;
  maxPenetrationLate: number;
  anneal: number;
  annealSpan: number;
  annealAmplitude: number;
  miss: AtlasMiss;
  /** Every square's final pose, as [x, y, degrees]. */
  final: [number, number, number][];
}

/** Playing the whole sequence back to back. */
export interface AtlasContinuous {
  on: boolean;
  fullBeat: boolean;
  prefetch: boolean;
  dwell: number;
  move: number;
  settle: number;
  staticDwell: number;
  pair: number;
  pairs: number;
  staticPairs: number;
  timing: AtlasTiming;
  total: number;
  remaining: number;
}

/** The instants of one step, in seconds from its start. */
export interface AtlasSchedule {
  moveStart: number;
  moveEnd: number;
  end: number;
  /** When the new square starts to appear, and when it has arrived. */
  arrive: number;
  arrived: number;
  blocksStart: number;
  blocksEnd: number;
  roll: number;
}

/**
 * One step of the corpus, as the API reports it.
 *
 * `stats` is the record's own measurements of the step, carried through from the page's data
 * unchanged. It is open-ended by construction -- the builder writes whatever it measured -- so it
 * is an index signature rather than a list of keys that would go stale.
 */
export interface AtlasPairSummary {
  index: number;
  n: number;
  kind: AtlasPairKind;
  stats: { [measure: string]: number };
}

/** A block of squares that move together, with the riders that come along. */
export interface AtlasBlock {
  cluster: number;
  drift_max: number;
  from: [number, number];
  to: [number, number];
  turn: number;
  members: number[];
  riders: number[];
}

/** The square this step adds, and the rule that chose it. */
export interface AtlasNewSquare {
  index: number;
  identity: number;
  rule: string;
  tied: number;
}

/** Where the sequence stands: a fraction of the whole, and the n on the stage. */
export interface AtlasProgress {
  position: number;
  /** Null until a frame has been drawn. */
  n: number | null;
}

/** What `restart` put back. */
export interface AtlasRestart {
  mode: AtlasAspect;
  n: number;
  playing: boolean;
  t: number;
  steps: number;
}

/** What `reset` put back: every physics parameter, as it now stands. */
export interface AtlasReset {
  law: AtlasLawState;
  relationship: AtlasRelationship;
  growth: AtlasGrowth;
  anneal: number;
}

/**
 * Everything the page is currently showing.
 *
 * `mode` has meant the simulation mode since revision 6; the Pack-or-Animate aspect is `aspect`.
 */
export interface AtlasState {
  tab: "single";
  aspect: AtlasAspect;
  pair: number;
  n: number;
  t: number;
  duration: number;
  playing: boolean;
  /** The colour scheme. It was the constant 'angle' for one revision. */
  rule: AtlasScheme;
  phase: AtlasPhase;
  style: AtlasStyle;
  links: boolean;
  capture: boolean;
  timing: AtlasTiming;
  desaturate: boolean;
  snap: boolean;
  blind: boolean;
  blindInflate: number;
  mode: AtlasSimMode;
  anneal: number;
  speed: number;
  initial: AtlasInitial;
  optimizing: boolean;
  seed: number;
  /** The n the frame drew, which lags the step while a continuous run is rolling. */
  shownN: number | null;
}

/**
 * An edge list as the page will take one: pairs, or a flat run of indices, in any mix. Everything
 * is folded to a < b, deduplicated and dropped where it names a square this n does not have.
 */
export type AtlasEdgeInput = Iterable<number | readonly number[]>;

// ---------------------------------------------------------------- the API itself

/** The object `assets/workbench.js` assigns to `window.atlasTransitions`. */
export interface AtlasTransitions {
  // The tabs are gone; these two are no-ops kept so nothing that called them breaks.
  setTab(): "single";
  tab(): "single";

  // The chooser for n, which is the range collapsed onto one value.
  setStepN(n: number): number;
  stepN(): number;

  // The range, and the run that plays it end to end.
  setRange(from: number, to: number): AtlasRange;
  range(): AtlasRange;
  playRange(): AtlasContinuous;
  transport(): void;
  /** Back to the beginning of whatever play would play, with every setting kept. */
  restart(): AtlasRestart;

  // Which aspect the page is showing.
  setMode(next: string): AtlasAspect;
  mode(): AtlasAspect;

  // The gap bar, and the call that redraws it on demand.
  gapBar(): AtlasGapBar;
  refreshGap(): AtlasGapBar;

  seek(seconds: number): void;
  /** The step's length in seconds; the step on the stage unless another is named. */
  duration(pairIndex?: number): number;
  play(): void;
  pause(): void;
  select(index: number): void;
  setTiming(timing?: Partial<AtlasTiming> | null): void;

  /** The colouring is one map and is always on, so this is a no-op kept for callers. */
  setColorRule(): AtlasScheme;
  colour(): AtlasColour;
  /** The angle map as a pure function, testable with nothing on the stage at all. */
  fillsFor(angles: readonly number[], contacts?: readonly number[]): string[];
  atlasFillsFor(angles: readonly number[], contacts?: readonly number[]): string[];

  setColorScheme(scheme: AtlasScheme): AtlasScheme;
  colorScheme(): AtlasScheme;
  colorSchemes(): AtlasScheme[];

  /** How far a moving square is drained, as the chroma it keeps. Clamped to [0, 1]. */
  setDesatFloor(v: unknown): number;
  desatFloor(): number;
  /** The stage's area compensation. 1 is the atlas's own chroma. Clamped to [0.3, 1]. */
  setStageChroma(v: number): number;
  stageChroma(): number;

  /** The greens as a pure function of the identity, needing nothing on the stage. */
  identityFills(count?: number): string[];
  setAnimateStandardize(on: boolean): boolean;
  animateStandardize(): boolean;

  setPhase(phase: AtlasPhase): void;
  setStyle(style: string): void;
  setOverlay(on: boolean): void;
  setCapture(on: boolean): void;
  setAutoAdvance(on: boolean): void;
  setDesaturate(on: boolean): void;
  setSnap(on: boolean): void;
  setBlind(on: boolean): void;
  setBlindInflate(factor: number): void;

  /** Set the run seed when it is an integer in [0, 2^32 - 1]; invalid values are ignored. */
  setSeed(seed: unknown): number;
  seed(): number;

  /** Playback only: `seek(t)` is unchanged by it. Clamped to [0.05, 2]. */
  setSpeed(multiplier: number): number;
  speed(): number;

  setInitial(kind: AtlasInitial): AtlasInitial;
  initial(): AtlasInitial;
  initials(): AtlasInitial[];
  optimize(on: boolean): AtlasOptimize;
  optimizeStep(steps?: number): AtlasOptimize;
  optimizeState(): AtlasOptimize;

  // The hand. `pickAt` takes world coordinates, `poseOf` gives them back, so a test can drive a
  // drag without a mouse.
  /** The index of the square under the point, or -1. */
  pickAt(wx: number, wy: number): number;
  /** The index grabbed, or -1. Without a point, the square is grabbed at its own centre. */
  grab(index: number, wx?: number, wy?: number): number;
  dragTo(wx: number, wy: number, rotating?: boolean): AtlasDrag | null;
  release(): number;
  hand(): AtlasHand;
  /** Where the frame drew square i, as [x, y, degrees], or null if it did not. */
  poseOf(i: number): [number, number, number] | null;

  setAnneal(level: number): AtlasAnneal;
  anneal(): AtlasAnneal;

  // The one force law, its presets, its sampled shape, and its two draggable control points.
  setLaw(next?: AtlasLawInput | null): AtlasLawState;
  law(): AtlasLawState;
  setLawPreset(name: string): AtlasLawState;
  lawPresets(): string[];
  /** The law sampled over the gaps it acts on, as [gap, force]. */
  lawCurve(count?: number): [number, number][];
  lawForce(d: number): number;
  dragLaw(which: "knee" | "pull", gap: number, force: number): AtlasLawState;

  // The walls' own law, the same shape for the other relationship a square has.
  setWallLaw(next?: AtlasLawInput | null): AtlasLaw;
  wallLaw(): AtlasLaw;
  wallForce(d: number): number;

  // The table itself, so a caller can ask what parameters and laws exist.
  lawNames(): string[];
  lawParams(): string[];
  /** Where a law's controls live, which is the prefix of every one of its slider ids. */
  lawPrefix(name: string): string;
  setLawOf(name: string, next?: AtlasLawInput | null): AtlasLaw;

  setRelationship(kind: AtlasRelationshipKind): AtlasRelationship;
  relationship(): AtlasRelationship;
  relationships(): AtlasRelationshipKind[];
  /** Hand the page a target graph, or null to go back to the source. */
  setTargetGraph(edges?: AtlasEdgeInput | null): AtlasRelationship;
  /** The target graph in force, flat: a, b, a, b. */
  targetGraph(): number[];

  // The hand-drawn contact graph, and the pointer gesture that builds it.
  edges(): [number, number][];
  setEdges(pairs?: AtlasEdgeInput | null): [number, number][];
  clearEdges(): [number, number][];
  /** True if the edge was added, false if it was taken away. */
  toggleEdge(a: number, b: number): boolean;
  setTargetSource(kind: AtlasTargetSource): AtlasTargetFrom;
  targetSource(): AtlasTargetFrom;
  targetSources(): AtlasTargetSource[];
  setDrawing(on: boolean): boolean;
  drawing(): boolean;
  linkStart(index: number): number;
  linkMove(wx: number, wy: number): AtlasLinkDrag | null;
  linkEnd(index: number): AtlasLinkEnd;
  linkCancel(): void;

  setGrowth(next?: Partial<Pick<AtlasGrowth, "on" | "size" | "rate" | "rule">> | null): AtlasGrowth;
  growth(): AtlasGrowth;
  growthRules(): AtlasGrowthRule[];
  /** Every physics parameter back where it started. */
  reset(): AtlasReset;
  /** The picture's own contact graph, as pairs of indices. */
  contactGraph(): [number, number][];

  sequenceDuration(): number;
  seekSequence(seconds: number): void;
  /** Run (or fetch from the cache) one trajectory and report it, without changing the stage. */
  physics(index: number, style?: AtlasStyle, mode?: AtlasSimMode): AtlasPhysics;

  // The whole sequence back to back, and the jump to a given n.
  playAll(): AtlasContinuous;
  stopAll(): AtlasContinuous;
  setContinuous(
    options?: Partial<Pick<AtlasContinuous, "on" | "fullBeat" | "prefetch">> | null,
  ): AtlasContinuous;
  /** The n actually reached, which is the nearest one the page carries. */
  goTo(n: number): number;
  continuous(): AtlasContinuous;

  styles(): AtlasStyle[];
  /** Which of them the mode on show actually offers. */
  solvers(): AtlasStyle[];
  progress(): AtlasProgress;
  schedule(): AtlasSchedule;
  pairs(): AtlasPairSummary[];

  phases(): AtlasPhase[];
  blocks(): AtlasBlock[];
  /** Which block each square of the current step belongs to; -1 for none. */
  blockOf(): number[];
  identities(): { from: number[]; to: number[] };
  newSquare(): AtlasNewSquare;
  state(): AtlasState;
}

/** A browser-like host that can expose the workbench API. */
export interface WorkbenchApiHost {
  atlasTransitions?: AtlasTransitions;
}

/**
 * Preserve the exact inferred implementation type while checking it against the public contract.
 * Object literals passed here fail type checking on missing, extra, or incompatible members.
 */
export function defineWorkbenchApi<const Api extends AtlasTransitions>(api: Api): Api {
  return api;
}

/** Install one contract-checked API object on the browser compatibility global. */
export function installWorkbenchApi<const Api extends AtlasTransitions>(
  host: WorkbenchApiHost,
  api: Api,
): Api {
  host.atlasTransitions = api;
  return api;
}
