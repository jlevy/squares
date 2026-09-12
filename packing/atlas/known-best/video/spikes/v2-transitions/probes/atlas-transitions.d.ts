// The page's API, declared once so the probes can be type-checked.
//
// Every probe reaches `window.atlasTransitions`, which `assets/workbench.js` assigns at the end of
// its IIFE. Nothing on the page is TypeScript and nothing is built, so there is no declaration to
// import: this file is it. It is the only non-`.js` file under `probes/`, which is also why
// `check_probes.py` -- which globs `*.js` -- does not mistake it for a probe.
//
// **Derived from the object literal, not from the calls.** Every member below is read off
// `window.atlasTransitions = { ... }` in `assets/workbench.js` and the function it names, so the
// declaration says what the page offers rather than what the probes happen to have used so far.
// Where a getter really does hand back an open-ended record -- a pair's statistics, say -- it is
// written with an index signature, because that is the truth about it.
//
// Nothing here is loaded at runtime. A `.d.ts` has no emit, and the probes are read as text by
// `probes.probe()` and evaluated in the browser exactly as they sit on disk.

// ---------------------------------------------------------------- the page's vocabulary

/** Which aspect the page is showing: one n optimised, or a range animated end to end. */
type AtlasAspect = "pack" | "animate";

/** The solvers. `tween` interpolates toward the record; the other two run the physics. */
type AtlasStyle = "tween" | "physics" | "bodies";

/** What the physics is told about where the squares are meant to end up. */
type AtlasSimMode = "snap" | "free" | "blind";

/** How a step's motion is staged. The page reads these from its own data (`motion_phases`). */
type AtlasPhase =
  | "add-then-move"
  | "move-then-add"
  | "simultaneous"
  | "rotate-first"
  | "slide-first";

/** How a square takes its colour. */
type AtlasScheme = "identity" | "angle-stable" | "angle-continuous";

/** What an open-ended run starts from. */
type AtlasInitial = "previous" | "random" | "grid" | "record";

/** Who attracts whom. Repulsion is never masked. */
type AtlasRelationshipKind = "general" | "groups" | "contact";

/** Where the target contact graph comes from. */
type AtlasTargetSource = "record" | "drawn";

/**
 * What the target graph is, which is the source unless a caller has handed one in: `setTargetGraph`
 * overrides the source for as long as it holds, and reports itself as `given`.
 */
type AtlasTargetFrom = AtlasTargetSource | "given";

/** How the squares grow. */
type AtlasGrowthRule = "constant" | "clean";

/** What a step is, in the corpus the page carries. */
type AtlasPairKind = "matched" | "prefix" | "shared-picture";

// ---------------------------------------------------------------- the shapes it hands back

/** The three beats of a step, in seconds. */
interface AtlasTiming {
  dwell: number;
  move: number;
  settle: number;
}

/** One law's four parameters. The same shape describes the pair law and the wall law. */
interface AtlasLaw {
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
type AtlasLawInput = { [K in keyof AtlasLaw]?: unknown };

/** Each law parameter's [low, high], which is also what the sliders are built from. */
interface AtlasLawBounds {
  rigidity: [number, number];
  repulsion: [number, number];
  attraction: [number, number];
  range: [number, number];
}

/** The pair law, with what it implies about the picture. */
interface AtlasLawState extends AtlasLaw {
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
interface AtlasRange {
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
interface AtlasAnneal {
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
interface AtlasGapBar {
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
interface AtlasColour {
  overlap: number;
  deepestOverlap: number;
  overlapPairs: number;
  /** The scheme chosen, and the one this frame was actually painted in. */
  scheme: AtlasScheme;
  painted: AtlasScheme;
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
interface AtlasRelationship {
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
interface AtlasGrowth {
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

/**
 * The open-ended run.
 *
 * With no run on the stage only the first three are reported, so everything a run carries is
 * optional here -- that is not a hedge, it is the two shapes `optimizeState()` actually returns.
 */
interface AtlasOptimize {
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
  feasible?: number;
  record?: number;
  excess?: number;
  penetration?: number | null;
  near?: number;
  held?: number;
  msPerStep?: number;
}

/** The hand: which square it holds, and how. */
interface AtlasHand {
  held: number;
  /** Undefined when there is no run to have edited. */
  edited: boolean | undefined;
  rotating: boolean;
}

/** Where a dragged square was put. */
interface AtlasDrag {
  index: number;
  x: number;
  y: number;
  /** Degrees, which is what the stage draws in. */
  angle: number;
}

/** An edge under the cursor, mid-gesture. */
interface AtlasLinkDrag {
  from: number;
  x: number;
  y: number;
}

/** What dropping an edge did, and the graph it left. */
interface AtlasLinkEnd {
  added: boolean;
  from?: number;
  to?: number;
  edges: [number, number][];
}

/** What a run reached, measured against the record it was aiming at. */
interface AtlasMiss {
  /** The largest distance a square's centre ends from the record's. */
  centre: number;
  /** The largest angle error, modulo a quarter turn. */
  angle: number;
  side: number;
  record: number;
  excess: number;
}

/** One cached trajectory, reported. */
interface AtlasPhysics {
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
interface AtlasContinuous {
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
interface AtlasSchedule {
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
interface AtlasPairSummary {
  index: number;
  n: number;
  kind: AtlasPairKind;
  stats: { [measure: string]: number };
}

/** A block of squares that move together, with the riders that come along. */
interface AtlasBlock {
  cluster: number;
  drift_max: number;
  from: [number, number];
  to: [number, number];
  turn: number;
  members: number[];
  riders: number[];
}

/** The square this step adds, and the rule that chose it. */
interface AtlasNewSquare {
  index: number;
  identity: number;
  rule: string;
  tied: number;
}

/** Where the sequence stands: a fraction of the whole, and the n on the stage. */
interface AtlasProgress {
  position: number;
  /** Null until a frame has been drawn. */
  n: number | null;
}

/** What `restart` put back. */
interface AtlasRestart {
  mode: AtlasAspect;
  n: number;
  playing: boolean;
  t: number;
  steps: number;
}

/** What `reset` put back: every physics parameter, as it now stands. */
interface AtlasReset {
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
interface AtlasState {
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
  /** The n the frame drew, which lags the step while a continuous run is rolling. */
  shownN: number | null;
}

/**
 * An edge list as the page will take one: pairs, or a flat run of indices, in any mix. Everything
 * is folded to a < b, deduplicated and dropped where it names a square this n does not have.
 */
type AtlasEdgeInput = Iterable<number | readonly number[]>;

// ---------------------------------------------------------------- the API itself

/** The object `assets/workbench.js` assigns to `window.atlasTransitions`. */
interface AtlasTransitions {
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
  setDesatFloor(v: number): number;
  desatFloor(): number;
  /** The stage's area compensation. 1 is the atlas's own chroma. Clamped to [0.3, 1]. */
  setStageChroma(v: number): number;
  stageChroma(): number;

  /** The greens as a pure function of the identity, needing nothing on the stage. */
  identityFills(count?: number): string[];
  setAnimateStandardize(on: boolean): boolean;
  animateStandardize(): boolean;

  setPhase(phase: AtlasPhase): void;
  setStyle(style: AtlasStyle): void;
  setOverlay(on: boolean): void;
  setCapture(on: boolean): void;
  setAutoAdvance(on: boolean): void;
  setDesaturate(on: boolean): void;
  setSnap(on: boolean): void;
  setBlind(on: boolean): void;
  setBlindInflate(factor: number): void;

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

interface Window {
  atlasTransitions: AtlasTransitions;
  /**
   * Not the page's: `gapbar/sample-run` parks its samples here for `gapbar/samples` to collect,
   * one `[t, the bar's hand, the frame's own summed overlap]` per tick.
   */
  __samples: number[][];
}

/**
 * `sizeAdjust` is a real `FontFace` descriptor -- CSS Fonts 4, shipped in Chromium since 92, which
 * is the browser Playwright drives here -- that TypeScript's `lib.dom.d.ts` does not yet carry.
 * Declared rather than cast away, so `candidate/font_faces` reads it as the string it is.
 */
interface FontFace {
  sizeAdjust: string;
}
