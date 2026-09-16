// The page's entry module. `tools/build-assets.ts` bundles it and everything it imports into the
// one classic script the page inlines, and publishes its exports -- the package's typed API -- as
// the page's `SquaresWorkbench` global, which is how the checkers' probes reach that API.
//
// It is a module rather than a script concatenated after the bundle, so what it uses is an import
// the bundler resolves and `tsc` follows, and a domain leaves this file by moving into a typed
// module that this one imports. Strict mode is a module's, and the bundle keeps it: esbuild opens
// the script with the directive, and `application-build.test.ts` holds the build to that.
import * as workbenchBundle from "./api/browser-entry.js";

export * from "./api/browser-entry.js";

const SQUARES_WORKBENCH_CORE = workbenchBundle.core;

(() => {
  if (typeof document === "undefined") {
    return;
  }
  const {
    el,
    html: htmlNode,
    svg: svgNode,
    input: inputNode,
    select: selectNode,
  } = workbenchBundle.dom.createDom(document);
  const {
    assessCataloguePrecisionFrame,
    assessPackingSnapshot,
    mixUint32Seed,
    PACKING_VALIDITY,
    packingSnapshot,
    parseUint32Seed,
  } = SQUARES_WORKBENCH_CORE;
  const {
    forceAtGap: forceOf,
    forceLawAttracts: attractsOf,
    forceLawSteep: steepOf,
  } = workbenchBundle.simulation;
  const {
    adjacentSupportedStep,
    availableStyles,
    nearestSupportedIndex,
    normalizeRange,
    planAspectTransition,
    rangeIndexBounds,
    transportIntent,
  } = workbenchBundle.navigation;
  const { reducedMotionAction, stageDescription, stageKeyCommand } = workbenchBundle.accessibility;
  const { clampSeparator, mountResizeHandle } = workbenchBundle.resizeHandle;
  const { decodeCorpus, isSimpleTransition } = workbenchBundle.data;
  const {
    baseTiming: timelineBaseTiming,
    displayedCount,
    isStillPair: timelineIsStillPair,
    pairDuration: timelinePairDuration,
    pairSchedule,
    pairTiming: timelinePairTiming,
    ramp: timelineRamp,
    rangeDuration: timelineRangeDuration,
    rangeProgress,
    seekSequence: timelineSeekSequence,
    sequenceDuration: timelineSequenceDuration,
  } = workbenchBundle.timeline;
  const { measureFrameGeometry } = workbenchBundle.geometry;
  const { createColourSystem } = workbenchBundle.colour;
  const { buildTrajectory, sampleTrajectoryPose, sampleTrajectorySide } =
    workbenchBundle.trajectory;
  const {
    advancePackRun,
    createGridPackStart,
    createPackRun,
    createRandomPackStart,
    measurePackRun,
    setPackSquareSide,
    updatePackRun,
  } = workbenchBundle.pack;
  const { createAppendPackStart } = workbenchBundle.startProposals;
  const { illustrationFrame } = workbenchBundle.illustration;
  const { renderStage } = workbenchBundle.stageView;
  /** @type {import("./app/animation-panel.js").AnimationPanel | null} */
  let animationPanel = null;
  /** @type {import("./app/pack-panel.js").PackPanel | null} */
  let packPanel = null;
  /** @type {import("./app/search-panel.js").SearchPanel | null} */
  let searchPanel = null;
  // **Whether the catalogue view owns the page's input.** This controller answers the page's
  // global shortcuts, the stage's keys and pointer, and `atlasTransitions` only while neither
  // independent panel is showing; each of those entry points asks this one question rather than
  // naming the panels itself, so a panel cannot be refused in one place and obeyed in another.
  // Before Pack mounts, the mode stands in for its visibility, so the answer holds from the first
  // event the page can receive, whichever view it opens on.
  function catalogueOwnsPage() {
    if (searchPanel?.visible()) {
      return false;
    }
    return packPanel === null ? state.mode !== "pack" : !packPanel.visible();
  }
  /** @typedef {import("./api/workbench-api.js").AtlasAspect} AtlasAspect */
  /** @typedef {import("./api/workbench-api.js").AtlasGrowth} AtlasGrowth */
  /** @typedef {import("./api/workbench-api.js").AtlasGrowthRule} AtlasGrowthRule */
  /** @typedef {import("./api/workbench-api.js").AtlasInitial} AtlasInitial */
  /** @typedef {import("./api/workbench-api.js").AtlasLaw} AtlasLaw */
  /** @typedef {import("./api/workbench-api.js").AtlasLawBounds} AtlasLawBounds */
  /** @typedef {import("./api/workbench-api.js").AtlasPaintScheme} AtlasPaintScheme */
  /** @typedef {import("./api/workbench-api.js").AtlasRelationshipKind} AtlasRelationshipKind */
  /** @typedef {import("./api/workbench-api.js").AtlasScheme} AtlasScheme */
  /** @typedef {import("./api/workbench-api.js").AtlasStyle} AtlasStyle */
  /** @typedef {import("./api/workbench-api.js").AtlasTargetFrom} AtlasTargetFrom */
  /** @typedef {import("./api/workbench-api.js").AtlasTargetSource} AtlasTargetSource */
  /** @typedef {import("./api/workbench-api.js").AtlasTransitions} WorkbenchApi */
  const DATA = decodeCorpus(JSON.parse(htmlNode("atlas-data").textContent ?? "null"));
  const COLOUR = createColourSystem(DATA.colour);
  const FRAMES = DATA.frames;
  const PAIRS = DATA.pairs;
  // The owner's request of 2026-09-13: a step that only fills the last row of an axis-aligned
  // grid has no phase worth watching, so it can play at double speed. Decided once, from the
  // records themselves rather than from n.
  const SIMPLE = PAIRS.map((p) => isSimpleTransition(FRAMES[p.n], FRAMES[p.n + 1]));
  const FACTS = DATA.facts;
  const METRICS = DATA.metrics;
  const N_MAX = DATA.n_max; // 324: the progress bar always maps to 1..N_MAX
  const PHASES = DATA.motion_phases; // add-then-move (the default), move-then-add, simultaneous, rotate-first, slide-first
  const ARRIVAL_FRACTION = DATA.arrival_fraction; // the share of the move the new square takes to arrive in the two staged modes
  const PAD = 0.045; // container-side fraction of breathing room inside the 1000 px box
  const NEW_FRACTION = 1 / 3; // in the three unstaged modes the new square fades in over the last third of the move
  const ROLL_MAX = 0.4; // seconds for the panel's handover to the next n, from the moment the new square starts to appear
  const MARK_FADE = 0.15; // fraction of the move over which the previous pair's scarlet outline gives way to the normal stroke
  const MARK_WIDE = 4,
    MARK_THIN = 2; // scarlet outline widths, px: at arrival, and through the following dwell
  const TINT = 1.0; // the arriving square starts at the tint colour and settles to its own fill
  const TINT_CHROMA = 0.6; // the share of the accent's chroma that tint colour carries
  // Revision 6: while a pair is in motion the fills lose chroma, and lock back in over the settle,
  // so the resting frame is exactly the retained colours and only the moving picture is muted.
  //: The chroma a fill keeps at full desaturation, as a fraction of its own. 1 leaves the colour
  //: alone and 0 takes it to grey; the owner sets it from the page, so it is a variable rather than
  //: the constant it was. At a third the moving squares still competed with the locked ones for
  //: attention, and at an eighth the locked ones carry the picture, which is the point of locking
  //: them one at a time. The owner lowered the default from 0.15 to 0.08 on 2026-09-13.
  let desatFloor = 0.08;
  // **Chroma and hue move one at a time, and the hue always moves in the grey.** A square's
  // colour changes twice a beat -- it drains and comes back, and it swaps between the scheme a
  // viewer chose and the atlas's own answer for a finished picture. Doing both at once is what
  // made the change read as a lurch: a hue rotation at full chroma is a different colour arriving,
  // where the same rotation at a tenth of the chroma is invisible. So the order is
  //
  //     leaving rest   drain, THEN rotate            (grey out, then quietly become identity)
  //     returning      rotate, THEN saturate         (quietly become the atlas's, then colour up)
  //
  // and at every instant at most one of the two is moving. Each end is a `smootherstep`, which has
  // zero second derivative at both ends, so there is no corner where a change starts or stops.
  // **Every one of these is a FRACTION of the beat it lives in, never a number of seconds.** The
  // beat is the owner's to change, from the three inputs on the page, and a colour transition
  // measured in seconds would lag a beat that got shorter and overrun one that got shorter still.
  // A fraction keeps its share: halve the move and the drain halves with it.
  //
  // The chroma moves fastest, deliberately. It is the one change with nowhere to travel, so a
  // viewer reads it as a state rather than as a motion, and drawing it slowly reads as a fade
  // rather than as the picture going quiet. The hue takes the longer share of each window, because
  // it has further to go and because it is the change that must not be seen happening.
  const DESAT_IN = 0.14; // fraction of the move the chroma takes to drain
  const HUE_OUT = 0.4; // fraction of the move the hue takes to leave, once drained
  const HUE_IN = 0.7; // fraction of the settle the hue takes, before the chroma returns
  // Continuous play (revision 6, feature 4): the beat the whole sequence runs at, back to back.
  // A static append (a grid prefix or a shared picture, where nothing moves) gets a dwell and no
  // move at all, unless the full beat is asked for.
  // A static append used to be a dwell and nothing else, which meant the new square appeared
  // between one frame and the next with no time to be seen arriving -- the owner's report, and
  // exactly right: `move: 0` collapses `arrive` and `arrived` onto the same instant. It now gets
  // a short move and a settle of its own, so the scarlet square comes in and takes its colour.
  // Nothing rearranges (that is what makes it static), and the drain stays off for the same
  // reason: there is no motion to mute.
  // The box's beat on a step (see `drawBounds`): the fraction of the dwell over which the last
  // step's outer trace clears, of the move over which the box grows, and of the move over which
  // the inner trace then fades. Nothing is added or moved until both are done, which is
  // BOX_FIRST of every move.
  const BOUND_CLEAR = 0.3;
  const BOUND_GROW = 0.2;
  const BOUND_FADE = 0.12;
  const BOX_FIRST = BOUND_GROW + BOUND_FADE;
  const CONTINUOUS = {
    // The owner's beat of 2026-09-13, the same as the single-step timing the builder supplies.
    // The moving span is split: the free rearrangement and then the landing.
    dwell: 0.6,
    move: 0.5,
    correct: 0.4,
    settle: 0.3,
    staticDwell: 0.4,
    staticMove: 0.28,
    staticCorrect: 0.12,
    staticSettle: 0.35,
  };
  // Revision 7, feature 2: the annealing dial. It ran 0 to 10 with a default of 3, the revision-6
  // shake; on 2026-09-13 the owner widened it to 0 to 20 and moved the default to 9. Levels 0..10
  // mean exactly what they did. Three things rise with the level, and all three are stated here
  // rather than in the simulator:
  //   amplitude  0 at level 0, 1 (the revision-6 jiggle) at 3, linear on each side of 3: 3 at 10
  //              and about 5.86 at 20;
  //   decay      the shake falls as (1 - tau)^p over the run, p = 1.5 at levels 0..3 easing to
  //              0.35 at 10 and held there above it, since a power at or below zero would never
  //              let the shake die; at 0.35 it is still at 57% of its amplitude four fifths of
  //              the way through instead of 9%;
  //   span       the run is 1 move long up to level 3 and lengthens by a tenth of a move a level
  //              after that, to 1.7 moves at 10 and 2.7 at 20 — extra sub-steps at the same dt
  //              (the wall clock of a step stays 1/120 s), so a high level buys more simulated
  //              time to settle in rather than a faster shake in the same time. The move on the
  //              clock lengthens with it, which is why `timing` takes the style: only B and C are
  //              annealed.
  const ANNEAL = {
    min: 0,
    max: 20,
    dflt: 9,
    /** @type {(level: number) => number} */
    amplitude: (L) => (L <= 3 ? L / 3 : 1 + (L - 3) * (2 / 7)),
    /** @type {(level: number) => number} */
    decayPower: (L) => (L <= 3 ? 1.5 : 1.5 - (Math.min(L, 10) - 3) * (1.15 / 7)),
    /** @type {(level: number) => number} */
    span: (L) => (L <= 3 ? 1 : 1 + (L - 3) * 0.1),
  };
  // Revision 9: the playback speed. The ends are the owner's — slow enough to watch a settle
  // (0.05x, twenty seconds of wall clock for a one-second move) and fast enough to skim (2x). The
  // slider is logarithmic between them, so half way is the geometric mean rather than 1.02x, and
  // 1x is a value the slider can actually land on because the readout rounds to two places.
  const SPEED = { min: 0.05, max: 2, steps: 1000 };
  /** @param {number} m */
  const speedToSlider = (m) =>
    Math.round((Math.log(m / SPEED.min) / Math.log(SPEED.max / SPEED.min)) * SPEED.steps);
  /** @param {number | string} v */
  const sliderToSpeed = (v) => SPEED.min * (SPEED.max / SPEED.min) ** (Number(v) / SPEED.steps);
  const DEG = Math.PI / 180;
  const _QUARTER = Math.PI / 2;
  // Scarlet is defined once, in the stylesheet, and read back here for the fill tint.
  const SCARLET = getComputedStyle(document.documentElement).getPropertyValue("--new").trim();
  // The best known upper bound's green, which the stage's box turns when it locks at that side.
  const MET = getComputedStyle(document.documentElement).getPropertyValue("--met").trim();

  const state = {
    // Revision 9: one view. Revision 8's two tabs were the same operation over a different span, so
    // the range below is the single spine and `tab` is gone from the page. The API keeps `setTab`
    // and `tab` as no-ops for anything that still calls them.
    pair: 0,
    t: 0,
    playing: false,
    // **Four phases, not three.** The move was one span with the correction hidden inside it
    // as two fractions -- the spring stiffened at 0.68 of it, the poses eased onto their targets
    // over the last 0.12 -- so lengthening the search lengthened the landing with it, which
    // nobody wants and which no control said was happening. `move` is now the free
    // rearrangement and `correct` the landing, and the two fractions are derived from their
    // ratio rather than fixed. Defaults keep today's beat: 0.55 + 0.25 is 0.8 at a ratio of
    // 0.6875, against the 0.68 that was written down.
    timing: {
      dwell: DATA.timing.dwell,
      move: DATA.timing.move,
      correct: DATA.timing.correct,
      settle: DATA.timing.settle,
    },
    phase: PHASES[0],
    /** @type {AtlasStyle} */
    style: "tween", // 'tween' (style A, the block tween), 'physics' (B) or 'bodies' (C)
    desaturate: true, // drain the fills' chroma while the pair moves, lock the colour back in over the settle
    snap: true, // blend the physics onto the record's poses over the last of the move, and end on them exactly
    blind: false, // run the physics with no knowledge of the target poses at all
    anneal: ANNEAL.dflt, // how hard and how long the physical styles shake: 0 none, 20 the loudest
    links: false,
    // Revision 12: the stage takes two different press-drag-release gestures, and a toggle is what
    // keeps them apart. Off — the shipped behaviour — a press picks a square up and moves it. On, a
    // press starts an edge and the release lands it on whatever square is under the cursor.
    drawing: false,
    capture: false,
    autoAdvance: true,
    // Revision 10: which of the two aspects the page is showing. 'pack' is one fixed n, played as
    // the open-ended optimisation; 'animate' is a range, played end to end. The range below is still
    // the one spine: Pack is that range with its two ends equal.
    /** @type {AtlasAspect} */
    mode: "pack",
    // The range Animate was last left on, so switching to Pack and back does not lose it. Null until
    // Animate has been entered once, when it opens on the whole corpus.
    animate: null,
    // And the n Pack was last left on, for the same reason in the other direction. Null until Pack
    // has been left once, which cannot happen before the page has an n on the stage.
    packN: null,
    // Continuous play across the whole sequence: on, whether static appends take the full beat, and
    // whether the next pair is simulated during this one's dwell.
    continuous: { on: false, fullBeat: false, fastSimple: true, prefetch: true },
    // Revision 9: the range, stated as the values of n stepped *into*, which is the unit the chooser
    // and the chips have always used. 17 to 17 is the one step 16 -> 17 (the page's default), 2 to
    // 324 is the whole corpus. Clamped to what the page carries by `setRange`.
    range: { from: 17, to: 17 },
    // Revision 9: the playback rate. It multiplies the wall-clock delta the animation clock is
    // advanced by and the simulated time an open-ended run covers per frame, and nothing else.
    speed: 1,
    // **The run's seed.** Every generator on this page used to be seeded from n alone, so a
    // given n and parameter set had exactly one blind trial and it was the same trial every
    // time. That is the right property for an animation -- it is what makes a capture
    // reproducible across builds -- and it makes a success RATE impossible, because a rate
    // over one sample is either 0 or 1.
    //
    // Zero is the default and mixes to nothing, so every recorded measurement, every capture
    // and every checker sees exactly the trajectories it saw before. A non-zero seed is a
    // different draw of the same distribution.
    seed: 0,
    // Revision 9: what an open-ended Optimize run starts from, and whether one is on the stage.
    /** @type {AtlasInitial} */
    initial: "previous",
    optimizing: false,
    liveN: null,
  };

  // ---------------------------------------------------------------- maths
  /** @param {number} v */
  const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
  /** @type {(a: number, b: number, progress: number) => number} */
  const lerp = (a, b, u) => a + (b - a) * u;
  /** @param {number} u */
  const easeInOut = (u) => (u < 0.5 ? 4 * u * u * u : 1 - (-2 * u + 2) ** 3 / 2);
  /** @param {number} u */
  const easeOut = (u) => 1 - (1 - u) ** 3;
  //: Absorbs float rounding where two computed angles, times or law settings are compared as equal or
  //: tied. It never measures geometry, so it is not the validity tolerance (`PACKING_VALIDITY`).
  const ROUNDING = 1e-9;
  // Shortest signed turn modulo 90, in (-45, 45]; an exact 45 degree tie turns counter-clockwise, so
  // the direction is a rule rather than a rounding accident (the symmetric colour sweep looks the same
  // either way).
  /** @param {number} a @param {number} b */
  function angleDelta(a, b) {
    let d = (((b - a) % 90) + 90) % 90;
    if (d > 45 + ROUNDING) {
      d -= 90;
    }
    return d;
  }
  // A block member's own turn: the block's turn plus the correction from where the block leaves
  // it to its own final tilt, the correction taken the way round that keeps the total turn
  // smallest. (A square that rides a 45 degree block but ends upright is an exact tie for the
  // correction; the rule above would send it round by 90 rather than let it stay upright.)
  /** @param {number} blockTurn @param {number} a @param {number} b */
  function memberTurn(blockTurn, a, b) {
    const d = (((b - a - blockTurn) % 90) + 90) % 90;
    const one = blockTurn + d,
      other = blockTurn + d - 90;
    return Math.abs(one) <= Math.abs(other) + ROUNDING ? one : other;
  }
  /** @param {number} v @param {number} [d] */
  const fmt = (v, d) => v.toFixed(d);

  // Colour and geometry are pure package modules. The retained controller keeps only user state and
  // degree-buffer adaptation until it, too, moves under the package boundary.
  const PALETTE = COLOUR.palette;
  const SHADES = COLOUR.shades;
  const ANGLE_TOL = COLOUR.angleToleranceDegrees;
  const GREENS = COLOUR.greens;
  const GREEN_STRIDE = COLOUR.greenStride;
  /** @type {readonly AtlasScheme[]} */
  const COLOR_SCHEMES = COLOUR.schemes;
  const foldAngle = COLOUR.foldAngle;
  const angleGap = COLOUR.angleGap;
  const angleFills = COLOUR.angleFills;
  const atlasFills = COLOUR.atlasFills;
  const identityFills = COLOUR.identityFills;
  let stageChroma = 0.85;
  /** @type {AtlasScheme} */
  let colorScheme = "identity";
  const ANIMATE = { standardize: true };
  function standardizing() {
    return colorScheme === "identity" && state.mode === "animate" && ANIMATE.standardize;
  }

  // Geometry uses the same package receipt for contact shading, graph evidence, and validity.
  const CONTACT = { gap: 0.01 };

  // ---------------------------------------------------------------- the relationship graph (revision 11)
  // The force law says *what* the force is; this says *between whom*. They are orthogonal, and the
  // asymmetry between the two halves of the law is the whole point:
  //
  //   **Repulsion always applies to every pair.** No two squares may occupy the same space whatever
  //   any graph says, so the mask is never consulted on the penetrating side of the law.
  //   **Attraction is masked by the graph.** Only the pairs the graph relates are pulled together.
  //
  // Three graphs:
  //   general   every pair attracts — today's behaviour, and the default.
  //   groups    squares in the same block attract each other and nothing across blocks: one
  //             completely connected subgraph per block, taken from the page's own `blockOf`, which
  //             already computes a grouping. A square in no block is a group of one and attracts
  //             nobody, and so is the arriving square, which no block of n carries.
  //   contact   exactly the edges of a target graph, so the settle is biased toward realising that
  //             particular contact structure rather than any old dense one.
  //
  // The natural target is the contact graph of the *retained packing of the current n*, read off the
  // record's own poses with the same full-side test the colouring shades by, and then relabelled
  // into the run's square order through the pair's correspondence. `setTargetGraph` takes a
  // different one, so a graph from anywhere can be tried without touching this code.
  /** @type {AtlasRelationshipKind[]} */
  const RELATIONSHIPS = ["general", "groups", "contact"];
  /** @type {AtlasRelationshipKind} */
  let relKind = "general";
  let targetEdges = null; // a graph supplied from outside, or null to derive it from the record
  // Revision 12: the target graph is pluggable by design, so a graph drawn by hand on the stage is
  // the same object the record-derived one is. Three sources, and the choice is exposed:
  //   record  the contact graph of the retained packing of this n, relabelled into the run's order.
  //   drawn   the edges the owner drew between squares, held per n because an index means a
  //           different square at a different n. This is where a random or enumerated graph would
  //           arrive too: `setEdges(pairs)` takes one, and nothing in the physics has to change.
  //   given   whatever `setTargetGraph(edges)` was handed, which overrides both.
  /** @type {AtlasTargetSource[]} */
  const TARGET_SOURCES = ["record", "drawn"];
  /** @type {AtlasTargetSource} */
  let targetSource = "record";
  const drawnGraphs = new Map(); // packing size -> flat index pairs, a < b, in the order drawn
  /** @returns {AtlasTargetFrom} */
  const targetFrom = () => (targetEdges !== null ? "given" : targetSource);
  const drawnKeyFor = (pairIndex) => PAIRS[pairIndex].n + 1;
  const drawnFor = (pairIndex) => drawnGraphs.get(drawnKeyFor(pairIndex)) || [];
  // The drawn graph, content-addressed, for the trajectory cache key. It is a hash of the *set* of
  // edges — the pairs are sorted before it is taken — rather than a revision counter, because the
  // claim the cache has to hold up is "one graph, one run": drawing an edge and rubbing it out
  // again has to land back on the run it started from, and a counter would key that as a third.
  function drawnHash(pairIndex) {
    const flat = drawnFor(pairIndex);
    const pairs = [];
    for (let i = 0; i + 1 < flat.length; i += 2) {
      pairs.push([flat[i], flat[i + 1]]);
    }
    pairs.sort((x, y) => x[0] - y[0] || x[1] - y[1]);
    let h = 2166136261;
    for (const q of pairs) {
      for (const v of q) {
        h = (h ^ (v + 0x9e3779b9)) >>> 0;
        h = Math.imul(h, 16777619) >>> 0;
      }
    }
    return `${pairs.length}.${h.toString(36)}`;
  }
  const REL_EDGE_CAP = 60000; // a completely connected block of 324 would be 52,326 pairs
  // The mask is per pair as well as per kind, because a trajectory may be precomputed for a pair
  // the stage is not on (continuous play prefetches the next one, and `physics(i, ...)` asks for any
  // of them). Keyed by both, and dropped wholesale when the kind or the target changes.
  const relCache = new Map();
  const REL_CACHE_MAX = 8;
  // The contact graph of one retained frame, in that frame's own square order.
  function recordContactGraph(n) {
    const F = FRAMES[String(n)];
    if (F === undefined) {
      return [];
    }
    const m = F.squares.length;
    const px = new Float64Array(m),
      py = new Float64Array(m),
      pa = new Float64Array(m);
    for (let i = 0; i < m; i++) {
      px[i] = F.squares[i][0];
      py[i] = F.squares[i][1];
      pa[i] = F.squares[i][2];
    }
    return measureFrameGeometry(px, py, pa, F.side, 1, {
      gap: CONTACT.gap,
      angleToleranceDegrees: ANGLE_TOL,
    }).contactEdges;
  }
  // The same graph in the *run's* square order: square i of n is the run's i, and the arriving
  // square, whichever index it has in the frame of n + 1, is the run's last.
  function targetGraphFor(pairIndex) {
    if (targetEdges !== null) {
      return targetEdges.slice();
    }
    if (targetSource === "drawn") {
      return drawnFor(pairIndex).slice();
    }
    const p = PAIRS[pairIndex];
    const raw = recordContactGraph(p.n + 1);
    const toRun = new Int32Array(p.n + 1).fill(-1);
    for (let i = 0; i < p.n; i++) {
      toRun[p.map[i]] = i;
    }
    toRun[p.new] = p.n;
    const out = [];
    for (let e = 0; e < raw.length; e += 2) {
      const a = toRun[raw[e]],
        b = toRun[raw[e + 1]];
      if (a >= 0 && b >= 0) {
        out.push(a);
        out.push(b);
      }
    }
    return out;
  }
  function buildRelationship(pairIndex) {
    const p = PAIRS[pairIndex];
    const N = p.n + 1;
    let edges = [];
    if (relKind === "general") {
      return { mask: null, edges, N };
    }
    if (relKind === "contact") {
      edges = targetGraphFor(pairIndex);
    } else {
      // One completely connected subgraph per block. `block_of` is stated on the squares of n; the
      // arriving square is in none of them.
      const of = p.block_of;
      const byBlock = new Map();
      for (let i = 0; i < p.n; i++) {
        const k = of[i];
        if (k < 0) {
          continue;
        }
        if (!byBlock.has(k)) {
          byBlock.set(k, []);
        }
        byBlock.get(k).push(i);
      }
      for (const members of byBlock.values()) {
        for (let a = 0; a < members.length && edges.length < 2 * REL_EDGE_CAP; a++) {
          for (let b = a + 1; b < members.length && edges.length < 2 * REL_EDGE_CAP; b++) {
            edges.push(members[a]);
            edges.push(members[b]);
          }
        }
      }
    }
    const mask = new Uint8Array(N * N);
    for (let e = 0; e < edges.length; e += 2) {
      const a = edges[e],
        b = edges[e + 1];
      if (a < 0 || b < 0 || a >= N || b >= N) {
        continue;
      }
      mask[a * N + b] = 1;
      mask[b * N + a] = 1;
    }
    return { mask, edges, N };
  }
  function relationshipFor(pairIndex) {
    const key = `${relKind}/${pairIndex}`;
    let entry = relCache.get(key);
    if (entry === undefined) {
      entry = buildRelationship(pairIndex);
      if (relCache.size >= REL_CACHE_MAX) {
        relCache.delete(relCache.keys().next().value);
      }
      relCache.set(key, entry);
    }
    return entry;
  }
  const maskFor = (pairIndex) => relationshipFor(pairIndex).mask;
  // The trajectory cache key. The source is in it, and so is the drawn graph's revision, because
  // adding one edge by hand is as much a change to what a run does as switching the whole graph.
  const relKey = () =>
    relKind !== "contact"
      ? relKind
      : relKind +
        ":" +
        targetFrom() +
        (targetFrom() === "drawn" ? `:${drawnHash(state.pair)}` : "");

  // ---------------------------------------------------------------- DOM
  const svg = svgNode("packing-svg");
  const stage = htmlNode("stage");
  const stageDescriptionNode = htmlNode("stage-accessible-description");
  const containerRect = svgNode("container");
  const traceRect = svgNode("bound-trace");
  const boxRect = svgNode("bound-box");
  const linksGroup = svgNode("links");
  const maskGroup = svgNode("mask-links");
  const drawLine = svgNode("draw-line");
  const squaresGroup = svgNode("squares");
  const ghost = svgNode("ghost");
  const mark = svgNode("mark");
  const markRect = mark.firstElementChild;
  const factsA = htmlNode("facts-a");
  const factsB = htmlNode("facts-b");
  const live = htmlNode("live");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const SVG_NS = svg.namespaceURI;
  // One measurement of one numeral gives the figure width; the numerals are tabular, so every
  // label's width follows from its digit count and no frame ever has to ask the layout engine. A
  // three-digit label is preferred because it is the least relative error, but a shorter one will
  // do where the span carries no numeral that long.
  // The numeral shares the headline's line, so its box starts where `n =` ends. The width of
  // that line is measured rather than computed: it is one constant string, and a measurement
  // cannot disagree with the face the browser actually loaded -- which a build-time advance
  // sum could, since `=` may come from the symbols face with its own size-adjust. Taken at
  // startup and again on `document.fonts.ready`, as the figure width beside it is.
  let numeralLeft = 152; // the fallback, close enough for the frame before the faces land
  //: The row the headline is centred in: the packing's own box, so `n = 26` sits under the picture
  //: it names rather than under the panel.
  const HEADLINE_ROW = 1000;
  function measureHeadline() {
    // The headline is one rendered expression now, so centring it is centring one box. It is
    // centred on the WIDEST the corpus holds rather than on the current one: `n = 324` is the
    // longest, and centring each n on itself would slide the row as a digit is gained, twice in
    // the film and again mid-roll.
    /** @type {HTMLElement} */
    const shown = document.querySelector(".numeral");
    if (!shown || shown.offsetWidth === 0) {
      return;
    }
    const digits = String(N_MAX).length;
    /** @type {HTMLElement} */
    const current = document.querySelector(".numeral .n-val, .numeral .mord");
    const widest =
      shown.offsetWidth +
      (current?.textContent ? current.offsetWidth / Math.max(1, current.textContent.length) : 0) *
        Math.max(0, digits - (current?.textContent ? current.textContent.length : digits));
    numeralLeft = Math.max(0, (HEADLINE_ROW - widest) / 2);
    document.querySelectorAll(".numeral").forEach((el) => {
      /** @type {HTMLElement} */ (el).style.left = `${numeralLeft}px`;
    });
  }
  //: The width of one figure in the face the gap bar sets its two numbers in, used to decide
  //: whether the record's label would sit on top of the lower bound's. The fallback is Source Sans
  //: 3's figure at 28 px; the real value is measured once the faces land.
  //:
  //: It used to be measured off the progress scale's numerals, which are gone with the scale. That
  //: was always indirect -- those numerals are a different weight from the bar's -- and measuring
  //: the bar's own label is both simpler and more correct, since it is the thing being laid out.
  //: `getComputedTextLength` is the SVG measurement; `offsetWidth` is zero on an SVG text node.
  let _digitWidth = 15.6;
  function measureDigit() {
    const label = gapbarRecordLabel;
    const text = label?.textContent ? label.textContent : "";
    const digits = (text.match(/[0-9]/g) || []).length;
    if (digits > 0 && typeof label.getComputedTextLength === "function") {
      const width = label.getComputedTextLength();
      // The label is digits and a decimal point, nothing else: the relation glyph it used to carry
      // went when the arrows took over saying which bound is which. Counting the point as about
      // half a figure is close enough for a collision test, and the four-fifths fudge the relation
      // needed is gone -- it was making every label read a fifth narrower than it is, which is how
      // `5.12` came to be clamped to `.12` at the left end of the bar.
      if (width > 0) {
        _digitWidth = width / (digits + 0.5);
      }
    }
  }

  // Every square is one DOM element keyed by its global identity: identity k is born as the new
  // square of step k and is carried through every later pair by the identity chain the build
  // composed from the per-pair maps. An element is created once, the first time its identity is
  // shown, and is never re-keyed; a pair shows identities 1..n+1 and hides the rest. Because
  // identities are created in increasing order, the drawing order is birth order, so the newest
  // square always sits on top.
  const pool = new Map();
  function nodeFor(identity) {
    let g = pool.get(identity);
    if (!g) {
      g = el("g", { class: "sq", "data-identity": String(identity) });
      g.appendChild(
        el("rect", {
          x: "-0.5",
          y: "-0.5",
          width: "1",
          height: "1",
          stroke: "#000000",
          "stroke-width": "1.5",
          "stroke-linejoin": "round",
          "vector-effect": "non-scaling-stroke",
        }),
      );
      squaresGroup.appendChild(g);
      pool.set(identity, g);
    }
    return g;
  }

  // ---------------------------------------------------------------- badges (the poster's own marks)
  // A badge is the atlas's 19-unit rounded box (rx 4.5, stroke 1.2) with its glyph, scaled by the
  // panel. The star is the atlas's polygon; the approximately-equal sign is KaTeX_Main's U+2248
  // outline (the latin subset of Source Sans 3 has none), extracted at build time and drawn as a
  // path centred on its own ink, as the slideshow candidate draws it.
  const { buildFacts } = workbenchBundle.factsView.createFactsView(
    document,
    DATA,
    () => numeralLeft,
  );
  let numeralA = null;
  //: Per slot of the facts panel, whether the n layer and the n + 1 layer draw it identically.
  //: An identical slot hands over at the midpoint, which cannot be seen; only a slot that
  //: changes is faded. Filled when the pair's layers are built.
  let factsSame = [];
  //: Per changing slot, its drawn parts split into those held (the same part in the same place in
  //: both layers) and those that crossfade; null where the slot fades whole. A part is a KaTeX span,
  //: an SVG badge or a text element; the facts view splits every typeset number into one span per
  //: character, so a digit two numbers share is a part of its own.
  /** @type {({heldA: Element[], heldB: Element[], fadeA: Element[], fadeB: Element[]} | null)[]} */
  let factsParts = [];
  // The drawing units of one slot: an SVG as a whole, and every other element with no element
  // children. Null when some element mixes its own text with child elements, since that text
  // could not be faded apart from its children; such a slot fades whole.
  function drawnParts(/** @type {Element} */ root) {
    /** @type {Element[]} */
    const parts = [];
    let mixed = false;
    const walk = (/** @type {Element} */ el) => {
      for (const child of el.children) {
        if (child instanceof SVGElement || child.children.length === 0) {
          parts.push(child);
        } else {
          if ([...child.childNodes].some((c) => c.nodeType === 3 && c.textContent?.trim())) {
            mixed = true;
          }
          walk(child);
        }
      }
    };
    walk(root);
    return mixed ? null : parts;
  }
  // Which parts of a changing slot are unchanged: equal markup in an equal box in both layers.
  // Between `4.59 ≤ s(17) ≤ 4.67553` and `4.59 ≤ s(18) ≤ 4.822876`, `4.59 ≤ s(1` and the `4.` of
  // the upper bound are held; `7` and `8`, and the rest of the bound, crossfade. Anything not laid
  // out yet has no box to compare, so it is never held.
  function pairParts(/** @type {Element} */ a, /** @type {Element} */ b) {
    const partsA = drawnParts(a);
    const partsB = drawnParts(b);
    if (partsA === null || partsB === null) {
      return null;
    }
    const place = (/** @type {Element} */ el) => {
      const r = el.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) {
        return null;
      }
      const h = (/** @type {number} */ v) => Math.round(v * 2);
      return `${el.outerHTML}@${h(r.left)},${h(r.top)},${h(r.width)},${h(r.height)}`;
    };
    /** @type {Map<string, Element[]>} */
    const waiting = new Map();
    for (const el of partsB) {
      const key = place(el);
      if (key !== null) {
        waiting.set(key, [...(waiting.get(key) || []), el]);
      }
    }
    /** @type {Element[]} */
    const heldA = [];
    /** @type {Element[]} */
    const heldB = [];
    /** @type {Element[]} */
    const fadeA = [];
    const fadeB = new Set(partsB);
    for (const el of partsA) {
      const key = place(el);
      const twin = key === null ? undefined : waiting.get(key)?.shift();
      if (twin === undefined) {
        fadeA.push(el);
      } else {
        heldA.push(el);
        heldB.push(twin);
        fadeB.delete(twin);
      }
    }
    return { heldA, heldB, fadeA, fadeB: [...fadeB] };
  }
  const numeralStatic = htmlNode("numeral-static");
  const numeralSlotA = htmlNode("numeral-a");
  const numeralSlotB = htmlNode("numeral-b");

  // The current pair's motion, one entry per square of n: its element, its start and end
  // poses, and, for a block member, the block's transform (a rotation about the source pivot
  // that slides to the target pivot) with the square's offset from the pivot, the residual the
  // transform leaves to its own target, and its own turn taken the same way round as the block's.
  let motion = [];
  let lineNodes = [];
  let newNode = null,
    newRect = null,
    newPose = null,
    prevIndex = -1;
  // Revision 7, feature 3: the poses the current frame actually drew, and the record's poses they
  // are measured against. Filled by whichever scene ran, so the readout is what is on the stage
  // rather than a second opinion about it.
  let poseX = null,
    poseY = null,
    poseA = null;
  let sceneSide = 0; // the container side the last frame drew, which is where a drag picks the run up
  let boxSide = 0; // the side the stage's box was last drawn at, which the gap bar points to
  let boxLocked = false; // whether that box is at the best known side of the n it is showing
  let keyboardSquare = 0;
  let tgtX = null,
    tgtY = null,
    tgtA = null;
  //: The two settled arrangements of the current pair, each with its own angle map and contact
  //: counts, and which squares hold their colour right through the move.
  let restSource = null,
    restTarget = null,
    holdsColour = null;
  //: **The moving palette.** While the packing is unsettled the atlas's answer does not exist yet
  //: -- its hue is the angle class and its shade the contact count, and both are properties of an
  //: arrangement that has come to rest. So a moving frame is coloured by what IS true of it: which
  //: squares are parallel and touching. Every connected run of same-angle squares that share a
  //: whole side takes one colour, so a block reads as a block while it travels, and the drain is
  //: what says the colour is provisional.
  //:
  //: There is no fixed correspondence between this palette and the atlas's, and there does not
  //: need to be: which square ends up in which angle class is exactly what the run is deciding, so
  //: the final colours are assigned when the squares are in place and the two are crossfaded over
  //: the settle. What this palette owes is STABILITY, not agreement -- a square keeps its slot, and
  //: when two runs join they take the slot of the lower-numbered one, so a colour changes only when
  //: something about the packing changed.
  let groupSlot = null; // per square: which palette slot it carries while moving
  let groupParent = null; // union-find, carried forward through a move so runs only merge
  let groupSize = null; // each run's member count, so a join repaints the smaller side
  let groupClock = null; // the time it was last advanced to, so a scrub backwards resets it
  //: The shade a moving square is drawn at. Fixed, because the shade is the contact count and that
  //: is exactly what churns while squares are parting: a live count put a fifth of the ramp into
  //: single frames. Mid ramp, so the drained colours sit where the eye can still separate them.
  // Every connected run of same-angle squares that share a whole side, as a palette slot per
  // square. Union-find over the contact graph the painter has already built, so the cost is the
  // edge count and nothing is recomputed: measured at n = 324 it does not move the trajectory's
  // build time, which the gate holds to 400 ms.
  // The slot a square's run starts from, before any merge: spread over the slots the atlas does not
  // reserve for right angles.
  const firstSlot = (i) => 1 + (i % (PALETTE.length - 1));
  //: **How many instants of a step's move and settle its runs are read at.** A frame's colours are a
  //: function of its instant, not of which frames were drawn before it: runs used to merge on every
  //: frame painted, so a still seeked straight to an instant, a film walked to it at 30 fps and one
  //: at 60 fps each painted different runs (at n = 272, 22 to 44 fills of 272 apart). Merging only
  //: at these fixed instants, read off the same poses the stage draws, gives one answer however the
  //: instant is reached. They span the window the moving palette is drawn in, as the per-frame
  //: merge did: forty-eight over the default window of a second and a quarter is a checkpoint
  //: every 26 ms, under two frames, so a merge lands when the contact does.
  const GROUP_CHECKPOINTS = 48;
  let groupFolded = 0; // how many checkpoints are folded into the runs
  let groupSource = null; // the settings the folded checkpoints were read under
  /** @type {{x: Float64Array, y: Float64Array, a: Float64Array} | null} */
  let groupPoses = null;
  function resetGroups(count) {
    for (let i = 0; i < count; i++) {
      groupSlot[i] = firstSlot(i);
      groupParent[i] = i;
      groupSize[i] = 1;
    }
    groupFolded = 0;
    groupSource = null;
    groupClock = null;
  }
  function findGroup(a) {
    const parent = groupParent;
    while (parent[a] !== a) {
      parent[a] = parent[parent[a]];
      a = parent[a];
    }
    return a;
  }
  // **Runs only ever merge, and a join repaints the NEWCOMER.** Two rules, and both were found by
  // measuring rather than by reasoning. Rebuilding the components each frame let a square
  // oscillate between two of them as a contact made and broke at the tolerance: 49 direction
  // reversals at n = 110. And taking the lowest-numbered member's colour meant a whole run
  // repainted because one low-numbered square joined it, cascading as the merges did: 364 hue
  // hops at n = 110, 13 of them on one square. Union by size fixes the second -- the larger run
  // keeps its colour and the smaller adopts it, which is what "they become the same colour as
  // that connected component" means -- and carrying the union-find forward fixes the first.
  function foldGroups(count, edges, angles) {
    const size = groupSize;
    for (let e = 0; e < edges.length; e += 2) {
      const a = edges[e],
        b = edges[e + 1];
      if (a >= count || b >= count) {
        continue;
      }
      if (angleGap(foldAngle(angles[a]), foldAngle(angles[b])) > ANGLE_TOL) {
        continue;
      }
      let ra = findGroup(a),
        rb = findGroup(b);
      if (ra === rb) {
        continue;
      }
      // The larger run keeps its colour; ties go to the lower-numbered root so the result does not
      // depend on the order the edges came in.
      if (size[rb] > size[ra] || (size[rb] === size[ra] && rb < ra)) {
        const s = ra;
        ra = rb;
        rb = s;
      }
      groupParent[rb] = ra;
      size[ra] += size[rb];
    }
    for (let i = 0; i < count; i++) {
      groupSlot[i] = firstSlot(findGroup(i));
    }
  }
  // Every connected run of same-angle squares that share a whole side, as a palette slot per
  // square, for a frame on the step's timeline: the runs are the checkpoints up to `t` folded in
  // order, each read from the poses the scene would draw at its instant. Folding is incremental
  // while the clock runs forward; a scrub back, or a change to anything the poses depend on, starts
  // again from the first checkpoint.
  function assignGroups(count, t) {
    if (groupSlot === null || groupSlot.length !== count) {
      return;
    }
    const p = PAIRS[state.pair];
    const A = FRAMES[String(p.n)];
    const B = FRAMES[String(p.n + 1)];
    const tm = timing();
    const sc = schedule();
    const physical = isPhysical(state.style) && !isStillPair();
    // The window the moving palette is drawn in: from the moment the hue starts to leave, once the
    // chroma has drained, to the moment it is back. Outside it a frame is drawn in its resting
    // colours and its contacts say nothing about runs, so no checkpoint is read there -- in
    // particular not the dwell's own arrangement, where a record's touching squares would all
    // merge before anything had moved.
    const move = sc.moveEnd - sc.moveStart;
    const from = sc.moveStart + move * DESAT_IN;
    const span = sc.moveEnd + (sc.end - sc.moveEnd) * HUE_IN - from;
    const due =
      span <= 0 || t <= from
        ? 0
        : Math.min(
            GROUP_CHECKPOINTS,
            Math.floor(((t - from) / span) * GROUP_CHECKPOINTS + ROUNDING),
          );
    const source = [
      state.pair,
      state.style,
      physical ? trajectoryKey(state.pair, state.style, simMode()) : "",
      simMode(),
      state.phase,
      state.anneal,
      BLIND.inflate,
      sc.moveStart,
      sc.moveEnd,
      sc.end,
      sc.arrive,
      sc.arrived,
      sc.blocksStart,
      sc.blocksEnd,
    ].join("|");
    if (groupClock !== null || source !== groupSource || due < groupFolded) {
      resetGroups(count);
    }
    groupSource = source;
    if (groupPoses === null || groupPoses.x.length !== count) {
      groupPoses = {
        x: new Float64Array(count),
        y: new Float64Array(count),
        a: new Float64Array(count),
      };
    }
    const { x, y, a } = groupPoses;
    for (let k = groupFolded; k < due; k++) {
      const at = from + (span * (k + 1)) / GROUP_CHECKPOINTS;
      let side;
      if (physical) {
        side = physicsFrame(p, A, B, sc, at, x, y, a).side;
      } else {
        const frame = tweenFrame(p, A, B, tm, sc, at);
        for (const square of frame.squares) {
          x[square.index] = square.x;
          y[square.index] = square.y;
          a[square.index] = square.angleDegrees;
        }
        side = frame.containerSide;
      }
      const edges = measureFrameGeometry(x, y, a, side, 1, {
        gap: CONTACT.gap,
        angleToleranceDegrees: ANGLE_TOL,
      }).contactEdges;
      foldGroups(count, edges, a);
    }
    groupFolded = due;
  }
  // The same for an open-ended run, which has no timeline to checkpoint: its runs fold the contacts
  // of each frame it draws, carried forward from the moment the run began.
  function assignRunGroups(count, clock) {
    if (groupSlot === null || groupSlot.length !== count) {
      return;
    }
    if (groupClock === null || groupFolded > 0 || clock < groupClock - ROUNDING) {
      resetGroups(count);
    }
    groupClock = clock;
    foldGroups(count, paintEdges, poseA);
  }
  //: What counts as not moving and not turning, for a square that keeps its colour. A unit side is
  //: 1, so a hundredth of one is under half a pixel at the size the stage draws; half a degree is
  //: the same tolerance the angle classes are seeded with.
  const _HOLD_MOVE_TOL = 0.01;
  const HOLD_TURN_TOL = 0.5;
  // One settled arrangement's answer: the angle map its own classes give, and the contact count
  // each square has in it. `skip` leaves the arriving square out of the source arrangement, where
  // it does not exist yet.
  function restOf(side, poseAt, count, skip) {
    const x = new Float64Array(count),
      y = new Float64Array(count),
      a = new Float64Array(count);
    for (let i = 0; i < count; i++) {
      if (i === skip) {
        x[i] = 1e6;
        y[i] = 1e6;
        a[i] = 0;
        continue;
      }
      const q = poseAt(i);
      x[i] = q[0];
      y[i] = q[1];
      a[i] = q[2];
    }
    return {
      anglesDegrees: a,
      contacts: measureFrameGeometry(x, y, a, side, 1, {
        gap: CONTACT.gap,
        angleToleranceDegrees: ANGLE_TOL,
      }).contacts,
    };
  }
  let currentTrajectory = null; // the trajectory the physical scene last drew from, or null
  let lastMoveU = 0; // where in that trajectory the last frame sampled, 0..1

  function buildPair() {
    const p = PAIRS[state.pair];
    const A = FRAMES[String(p.n)];
    const B = FRAMES[String(p.n + 1)];
    linksGroup.textContent = "";
    lineNodes = [];
    motion = [];
    for (let id = 1; id <= p.n + 1; id++) {
      nodeFor(id);
    }
    // The opacity is the arriving square's, and only the pair that arrived it ever set it: an
    // element that was the new square of an earlier pair would otherwise still be carrying the 0 it
    // was left at, and would be a hole in this pair's packing. (Seen at 323 -> 324 after a visit to
    // 1 -> 2: identity 2 stayed invisible, a white cell in a full 18 x 18 grid.)
    pool.forEach((g, id) => {
      g.style.display = id <= p.n + 1 ? "" : "none";
      g.removeAttribute("opacity");
      g.removeAttribute("display");
      g.removeAttribute("data-square-index");
    });
    for (let i = 0; i < p.n; i++) {
      const a = A.squares[i],
        j = p.map[i],
        b = B.squares[j];
      const id = A.ident[i];
      if (B.ident[j] !== id) {
        throw new Error(`identity chain broken at ${p.n} -> ${p.n + 1}, square ${i}`);
      }
      const node = nodeFor(id);
      node.setAttribute("data-square-index", String(i));
      // Revision 12: the identity is carried on the motion entry as well as on the element, because
      // the painter asks for it every frame and the colour is keyed by it.
      const m = {
        node,
        rect: node.firstElementChild,
        ident: id,
        a,
        b,
        block: null,
        dx: 0,
        dy: 0,
        rx: 0,
        ry: 0,
        turn: angleDelta(a[2], b[2]),
      };
      const k = p.block_of[i];
      if (k >= 0) {
        const blk = p.blocks[k];
        const ct = Math.cos(blk.turn * DEG),
          st = Math.sin(blk.turn * DEG);
        m.block = blk;
        m.dx = a[0] - blk.from[0];
        m.dy = a[1] - blk.from[1];
        m.rx = b[0] - (blk.to[0] + ct * m.dx - st * m.dy);
        m.ry = b[1] - (blk.to[1] + st * m.dx + ct * m.dy);
        m.turn = memberTurn(blk.turn, a[2], b[2]);
      }
      motion.push(m);
      // The correspondence lines are drawn only when they are asked for: building n of them at every
      // pair boundary is the kind of work that shows up as a dropped frame under continuous play,
      // and `setOverlay` rebuilds the pair when it turns them on.
      if (state.links) {
        const line = el("line", {
          x1: a[0],
          y1: a[1],
          x2: b[0],
          y2: b[1],
          "stroke-linecap": "round",
          "vector-effect": "non-scaling-stroke",
        });
        linksGroup.appendChild(line);
        lineNodes.push(line);
      }
    }
    newPose = B.squares[p.new];
    // The frame's drawn poses and the record's, both n + 1 long, the new square last.
    poseX = new Float64Array(p.n + 1);
    poseY = new Float64Array(p.n + 1);
    poseA = new Float64Array(p.n + 1);
    tgtX = new Float64Array(p.n + 1);
    tgtY = new Float64Array(p.n + 1);
    tgtA = new Float64Array(p.n + 1);
    for (let i = 0; i < p.n; i++) {
      tgtX[i] = motion[i].b[0];
      tgtY[i] = motion[i].b[1];
      tgtA[i] = motion[i].b[2];
    }
    tgtX[p.n] = newPose[0];
    tgtY[p.n] = newPose[1];
    tgtA[p.n] = newPose[2];
    // **The atlas map is a function of a settled arrangement, so it is asked of settled ones.**
    // Its hue is the angle CLASS, and its shade the full-side contact count, and both are read from
    // the frame on the stage -- which is right at rest and meaningless in transit. Through a move
    // the classes regroup as squares turn, so a square's hue jumps between families, and contacts
    // break and remake, so its shade jumps a step: measured at n = 17, 14 to 16 of 17 fills changed
    // between consecutive frames over the few hundred milliseconds after the drain begins. That is
    // the flicker.
    //
    // So the two rests are worked out once per pair -- the arrangement this step leaves and the one
    // it lands on -- and a frame in transit borrows whichever it is nearer to. At either rest the
    // borrowed answer IS the live one, so the frames a viewer is left looking at are unchanged.
    restSource = restOf(A.side, (i) => motion[i].a, p.n + 1, p.n);
    restTarget = restOf(B.side, (i) => [tgtX[i], tgtY[i], tgtA[i]], p.n + 1, -1);
    // A square that neither moves nor turns, and sits square to the container, has nothing to be
    // unsettled about: it keeps its colour while the rest of the packing drains around it.
    // A square that sits square to the container is never drained. The owner's rule, and it is the
    // one the picture is built on: the grid is what a viewer can already read, so it keeps its
    // colour and the drain is left to say which squares are still looking for their place. It is
    // the ORIENTATION that decides, not whether the square moves -- an axis-aligned square sliding
    // one cell along a row is still a square a viewer can follow.
    holdsColour = new Uint8Array(p.n + 1);
    for (let i = 0; i <= p.n; i++) {
      const here = i < p.n ? motion[i].a[2] : tgtA[i];
      const there = tgtA[i];
      holdsColour[i] =
        angleGap(foldAngle(here), 0) <= HOLD_TURN_TOL &&
        angleGap(foldAngle(there), 0) <= HOLD_TURN_TOL
          ? 1
          : 0;
    }
    // The moving palette starts spread over the slots the atlas does not reserve for right angles,
    // so two runs that have never touched are unlikely to arrive at the same colour.
    groupSlot = new Int16Array(p.n + 1);
    groupParent = new Int32Array(p.n + 1);
    groupSize = new Int32Array(p.n + 1);
    resetGroups(p.n + 1);
    if (B.ident[p.new] !== p.n + 1) {
      throw new Error(`the new square of ${p.n} -> ${p.n + 1} is not identity ${p.n + 1}`);
    }
    newNode = nodeFor(p.n + 1);
    newNode.setAttribute("data-square-index", String(p.n));
    newRect = newNode.firstElementChild;
    // The square that arrived in the pair before is identity n; it keeps its outline through the dwell.
    prevIndex = p.n > 1 ? A.ident.indexOf(p.n) : -1;
    ghost.setAttribute("transform", `translate(${newPose[0]} ${newPose[1]}) rotate(${newPose[2]})`);
    numeralA = buildFacts(factsA, p.n);
    buildFacts(factsB, p.n + 1);
    // `n =` is drawn once, in its own slot, and never fades or drifts: only the number changes
    // between n. The still copy is the same rendered expression as the rolling ones with its
    // digits hidden, so KaTeX's spacing after the `=` is identical in all three and the rolling
    // number lands exactly where the still one would have been.
    numeralStatic.textContent = "";
    numeralStatic.appendChild(numeralA.cloneNode(true));
    // Which slots read the same for both n. Compared as markup: the two layers are built by the
    // same function into the same absolute slots, so equal markup is an equal picture.
    const slotsA = factsA.children;
    const slotsB = factsB.children;
    factsSame = [];
    for (let i = 0; i < Math.max(slotsA.length, slotsB.length); i++) {
      factsSame.push(
        slotsA[i] !== undefined &&
          slotsB[i] !== undefined &&
          slotsA[i].outerHTML === slotsB[i].outerHTML,
      );
    }
    factsParts = factsSame.map((same, i) =>
      same || slotsA[i] === undefined || slotsB[i] === undefined
        ? null
        : pairParts(slotsA[i], slotsB[i]),
    );
    factsA.style.opacity = "1";
    factsB.style.opacity = "1";
    // The step header (`16 → 17 · matched · max move 1.31 · …`) is gone from the stage: the
    // owner asked for it to go, and the transition's kind and motion statistics stay in
    // `transition-stats.json` for anyone who needs them.
    linksGroup.style.display = state.links ? "" : "none";
    ghost.style.display = state.links ? "" : "none";
  }

  // ---------------------------------------------------------------- timeline
  function timelineConfiguration() {
    return {
      pairs: PAIRS,
      simple: SIMPLE,
      fastSimple: state.continuous.fastSimple,
      boxFirst: BOX_FIRST,
      timing: state.timing,
      continuous: {
        on: state.continuous.on,
        fullBeat: state.continuous.fullBeat,
        beat: {
          dwell: CONTINUOUS.dwell,
          move: CONTINUOUS.move,
          correct: CONTINUOUS.correct,
          settle: CONTINUOUS.settle,
        },
        staticBeat: {
          dwell: CONTINUOUS.staticDwell,
          move: CONTINUOUS.staticMove,
          correct: CONTINUOUS.staticCorrect,
          settle: CONTINUOUS.staticSettle,
        },
      },
      anneal: state.anneal,
      phase: state.phase,
      arrivalFraction: ARRIVAL_FRACTION,
      newFraction: NEW_FRACTION,
      rollMax: ROLL_MAX,
    };
  }
  // The timing that governs one pair: the controls' three values, or, under continuous play, the
  // sequence's own beat, which depends on the pair's kind (revision 6, feature 4).
  // The annealing dial lengthens the move for the two physical styles, and only for them: style A
  // is an interpolation with no shake to prolong. At the default level the factor is exactly 1, so
  // the beat is the revision-6 beat unless the dial is moved.
  // The beat one pair takes under continuous play, whether or not a run is on. Split out in
  // revision 8 so the sequence tab can price a range before the owner presses play: `timing` is
  // exactly what it was, and this is the branch it takes while a run is going.
  // A pair where the arrangement does not rearrange: the new square is appended to a picture the
  // previous n already had. Named here because both the beat and the drain ask the question.
  function isStillPair(pairIndex) {
    return timelineIsStillPair(
      timelineConfiguration(),
      pairIndex === undefined ? state.pair : pairIndex,
    );
  }
  // **Every beat carries all four spans.** The anneal dial and the continuous beat each build a
  // fresh object here, and when `correct` was added they were left at three keys -- so
  // `dwell + move + correct + settle` was NaN on every path but the default one, and a NaN
  // duration turns a seek into a run that never arrives. The gate went from 90 seconds to over
  // seventeen minutes and the cause looked like a cache problem for two rounds.
  //
  // A static append has no landing to speak of, but it still gets a `correct` in proportion:
  // the beat is a shape, and a span that is sometimes absent is a span every caller has to
  // remember.
  function timing(pairIndex, style) {
    return timelinePairTiming(
      timelineConfiguration(),
      pairIndex === undefined ? state.pair : pairIndex,
      style === undefined ? state.style : style,
    );
  }
  function duration(pairIndex) {
    return timelinePairDuration(
      timelineConfiguration(),
      pairIndex === undefined ? state.pair : pairIndex,
      state.style,
    );
  }
  // The instants of one pair. In the default staging the new square arrives over the first
  // ARRIVAL_FRACTION of the move (`arrive` to `arrived`) while the container grows, and the
  // existing squares move, as blocks, over the rest (`blocksStart` to `blocksEnd`); `move-then-add`
  // is the same split the other way round; the three unstaged modes move everything through the
  // whole move and fade the new square in over its last third. The panel's text leaves and
  // returns over `roll` seconds from `arrive`, the moment the new square starts to appear.
  // The n the stage is showing at t: the pair's own n through the dwell and the first half of the
  // roll, and the next one after that. One function, so the panel's numeral, the announcement and
  // the gap bar cannot disagree about which packing is on screen.
  function rollingN(p, sc, t, optimizing) {
    return displayedCount(p.n, sc, t, optimizing);
  }
  function schedule() {
    return pairSchedule(timelineConfiguration(), state.pair, state.style);
  }
  const ramp = timelineRamp;
  // How much chroma the fills carry at t: all of it through the dwell, drained over the first
  // DESAT_IN of the move, held through the motion, and back over the LAST part of the settle --
  // after the hue has finished moving, which is the whole point of the split. A zero-length move
  // (a static append under a tween) never drains at all.
  function chromaLevel(sc, t) {
    const move = sc.moveEnd - sc.moveStart;
    const settle = sc.end - sc.moveEnd;
    const out = smootherstep(ramp(t, sc.moveStart, sc.moveStart + move * DESAT_IN));
    const back = smootherstep(ramp(t, sc.moveEnd + settle * HUE_IN, sc.end));
    return 1 - out * (1 - back);
  }
  // Which hues the fills carry at t: 1 is the atlas's answer, the convention for a finished
  // picture; 0 is the scheme the viewer chose, which is what makes a square trackable while it
  // moves. It leaves only AFTER the chroma is gone and returns BEFORE the chroma comes back, so
  // both rotations happen in the grey and a viewer never watches a colour turn into another colour.
  function hueLevel(sc, t) {
    const move = sc.moveEnd - sc.moveStart;
    const settle = sc.end - sc.moveEnd;
    const leave = smootherstep(
      ramp(t, sc.moveStart + move * DESAT_IN, sc.moveStart + move * (DESAT_IN + HUE_OUT)),
    );
    const back = smootherstep(ramp(t, sc.moveEnd, sc.moveEnd + settle * HUE_IN));
    return 1 - leave * (1 - back);
  }
  function desatLevel(sc, t) {
    if (!state.desaturate) {
      return 0;
    }
    // Nothing moves on a static append, so nothing is unsettled and nothing is muted. Without
    // this the short move added for the arrival would drain a picture that is standing still.
    if (
      state.continuous.on &&
      !state.continuous.fullBeat &&
      isStillPair() &&
      !isPhysical(state.style)
    ) {
      return 0;
    }
    return 1 - chromaLevel(sc, t);
  }
  // Revision 9: which steps playback is allowed to run over — always the range, there being one view.
  // The ends are values of n stepped into, so RANGE_MIN is the first n the page can arrive at.
  /** @type {number[]} */
  const SUPPORTED_STEP_NS = PAIRS.map((pair) => pair.n + 1);
  const RANGE_MIN = SUPPORTED_STEP_NS[0];
  const RANGE_MAX = SUPPORTED_STEP_NS[SUPPORTED_STEP_NS.length - 1];
  function rangeBounds() {
    return rangeIndexBounds(SUPPORTED_STEP_NS, state.range);
  }
  function scopeBounds() {
    return rangeBounds();
  }
  // The span the progress bar's scale covers: the range, read as the n it steps *from* through the n
  // it steps into, so the whole corpus is the shipped 1..324 scale and a single step is its own two
  // numerals. `progress` is measured against the same span, so the fill, the cursor and the riding n
  // all read against the numerals actually drawn.
  // Where the sequence stands, 0 at the start of the range's first step and 1 at the end of its
  // last: a pure function of the pair and the clock. The scale it used to be drawn on is gone --
  // the owner found it distracting, and the stage carries facts about the packing rather than
  // apparatus about the playback -- but the number is still what `progress()` reports, and the
  // transport and the checkers read it.
  function progress() {
    return rangeProgress(
      timelineConfiguration(),
      state.range,
      state.pair,
      state.t,
      state.style,
      state.optimizing,
    );
  }

  // ---------------------------------------------------------------- styles B and C: physics, bodies
  // Style B ("physics"): a deterministic fixed-timestep simulation of all n + 1 squares, each its
  // own body. Style C ("bodies"): the same simulation with every matched block one rigid body whose
  // members are fixed in the body frame (their poses at n relative to the block's centroid); riders,
  // squares that move alone and the new square are single-square bodies. A trajectory is
  // precomputed once per style, pair and move length and cached; seek(t) samples the cache, so a
  // frame is a pure function of t and the same in every run. The simulation's clock is the move:
  // every constant below is stated per move length, so a longer move plays the same trajectory
  // more slowly. At the default 1.4 s move that is 168 steps of 1/120 s. Semi-implicit Euler; unit
  // mass per square; angles in radians inside. The targets are the pair's correspondence: square i
  // of n goes to B.squares[map[i]], the new square is identity n + 1 at its own pose.
  const PHYS = {
    stepsPerSecond: 120,
    omega: 10, // spring natural frequency per move (k = 100): the time constant is a tenth of the move
    zeta: 0.85, // damping ratio, a little under critical, so a square arrives with a hint of overshoot
    springRamp: 0.25, // the spring's stiffness rises (smoothstep) over this first fraction of the move, so
    // squares do not rush before the container has made room
    // Revision 11: the push-apart's stiffness (2500 per unit of penetration, per move^2) and its
    // cap (0.15, past which it stopped growing) left this table and became `LAW.repulsion` and
    // `LAW.rigidity`, which the owner can edit. They were the defaults until 2026-09-13.
    contactDamping: 20, // damping on the closing speed of two overlapping squares
    contactTorque: 0.15, // fraction of a contact's or wall's torque applied to a single square (the push acts at a
    // corner); the rest yields to the angle spring. A block takes the whole torque about its centroid.
    lockIn: 0.7, // from this fraction of the move the push-apart fades out, gone where the final blend begins
    // **Room to move, and then a tightening.** Two measured problems, and one beat each.
    //
    // Room: on 164 of the 323 steps the record's side does not grow at all -- the box at n is the
    // box at n + 1 -- and at the perfect squares there is not even area to give, `side^2 - n` being
    // exactly 0 at n = 100 and at n = 324. Squares with nowhere to go shove rather than pass, and
    // the measure of that is WANDER: how far a square strays from the straight line between where
    // it starts and where it ends, which separates thrashing from travel (a square that legitimately
    // moves 1.2 sides is not wandering). Median wander over the matched steps was 0.66 of a side and
    // the worst 1.07 -- a square swinging a whole square-width out of its way. So the container
    // breathes: it opens past the side it is heading for, holds while the squares rearrange, and is
    // closed again before the blend. The squares are not scaled; the walls move and the repulsion
    // spreads the packing into the room on its own.
    //
    // Tightening: with the room taken the run still ended a visible distance from the record and the
    // blend then carried it the rest of the way, so the last thing a viewer saw was a correction
    // rather than an arrival. Between the push-apart fading and the blend beginning, the spring
    // toward the target is stiffened: the same spring, harder, over a window where nothing else is
    // competing with it.
    open: 0.3, // sides the container opens past its target at the widest
    openBy: 0.3, // fraction of the move by which it is fully open
    shutFrom: 0.62, // fraction of the move from which it closes again, done at `1 - blend`
    tighten: 16.0, // the spring's stiffness multiplier at the end of the tightening window
    // Where the correction begins, as a fraction of the simulation's own progress. The
    // rearrangement is everything before it and the landing everything after, and the beat's
    // `move` and `correct` are how many seconds the reader spends on each side of it.
    tightenFrom: 0.68,
    wall: 2500, // the container's walls: stiffness per unit of corner overhang, per move^2
    wallCap: 0.25,
    inertia: 1 / 6, // a unit square of unit mass about its centre
    grow: 0.5, // the container reaches n + 1's side at this fraction of the move (ease-out, so room opens early)
    jiggle: 20, // jiggle acceleration amplitude per move^2 at the start, decaying as (1 - tau)^1.5
    jiggleTorque: 12, // jiggle angular acceleration amplitude, rad per move^2, decaying the same way
    jiggleHz: [2.5, 4], // a body's jiggle frequency, cycles per move, drawn per axis
    drop: 0, // how far above its target the new square starts (at its target angle). 0: it inflates in
    // place. A drop of 0.5 was tried in the physics spike: where the target is wedged with no
    // clearance the square jams flat on its neighbours and only the lock-in carries it through.
    appear: 0.15, // fraction of the move over which the new square fades in and inflates to full size
    inflateFrom: 0.3, // its side when it first appears
    // The last fraction of the simulation's progress that eases each pose onto its exact
    // target (smoothstep). Inside the correction, so a longer `correct` gives it more
    // seconds without giving it more of the run.
    blend: 0.12,
    maxSpeed: 40, // units per move, per body
    maxSpin: 20, // radians per move, per body
    cell: 1.5, // broad-phase grid cell; two unit squares can only overlap within sqrt 2 of each other
  };
  // What style C changes: the shake is the point of the style, so its jiggle is twice B's. A body's
  // jiggle is an acceleration, the same for every body whatever its mass, as a shaken table gives.
  const BODIES = { jiggle: 40, jiggleTorque: 24 };

  // ---------------------------------------------------------------- the force law (revision 11)
  // One law, a function of the signed gap `d` between two squares along the separating axis the
  // collision test already computes: negative is penetration, zero is touching, positive is a gap.
  // It replaces the hard-coded stiffness and cap; the damping term stays and is added to it.
  //
  //     d <= 0   (depth p = -d)   f = repulsion * ( min(p, rigidity) + steep * max(0, p - rigidity) )
  //     0 < d < range             f = -attraction * 4u(1 - u),  u = d / range
  //     d >= range                f = 0
  //
  // Positive pushes the pair apart, negative pulls it together, which is the sign the push-apart
  // already used. The three pieces meet at zero — f(0) = 0 from both sides — and the attraction is
  // zero again at the edge of its range, so the law is continuous everywhere. Attraction and
  // repulsion never overlap, so **the net force at any penetration is repulsive whatever the
  // attraction is set to**: two squares can be pulled up to touching and never through each other.
  //
  // `steep` is not a fifth parameter: it is derived from the rigidity so that the shipped value is
  // exactly the old law. The old law was `contact * min(p, contactCap)` — linear to a cap and flat
  // past it — so rigidity 0.15 (the old `contactCap`) with steep 0 reproduces it to the bit.
  // That law was the default until 2026-09-13, so the cached trajectories, blind runs and
  // measurements of revisions 6 to 10 reproduce under `{rigidity: 0.15, repulsion: 2500,
  // attraction: 0, range: 0}`. On 2026-09-13 the owner chose a softer, slightly sticky default.
  // Below the shipped rigidity the shared law's slope past the knee climbs linearly, so the
  // hardest setting is a knee at two thousandths of a side with eight times the stiffness past it:
  // effectively rigid at this timestep, and measured stable.
  // ------------------------------------------------------------------ the laws, declared once
  //
  // A law is four numbers describing a force against a signed gap, and there are two of them,
  // because a square has two relationships: with another square, and with a wall. They were
  // written out twice -- markup, sync loop, wiring, cache key, reset, API -- and every one of
  // those was a place to forget one. The wall law's controls did nothing on their first build
  // for exactly that reason: the setter existed and was never exposed.
  //
  // So the parameters are a table and everything else reads it. Adding a fifth parameter, or a
  // third law, is a row here; the sliders, their labels and steps, the readouts, the trajectory
  // cache key, the reset and the API method all follow. Nothing downstream enumerates them, so
  // nothing downstream can fall out of step -- and a check that wanted to know "what parameters
  // are there" asks this rather than listing what it saw.
  const LAW_PARAMS = [
    {
      key: "rigidity",
      label: "rigidity",
      step: 0.001,
      decimals: 3,
      says: "the penetration tolerated before the repulsion climbs",
    },
    {
      key: "repulsion",
      label: "repulsion",
      step: 50,
      decimals: 0,
      says: "the push when penetrating",
    },
    {
      key: "attraction",
      label: "attraction",
      step: 5,
      decimals: 0,
      says: "the pull when separated but close; zero is none",
    },
    {
      key: "range",
      label: "range",
      step: 0.005,
      decimals: 3,
      says: "the gap width the attraction acts over; zero beyond",
    },
  ];
  const LAW_KEYS = LAW_PARAMS.map((d) => d.key);
  /** @type {AtlasLaw} */
  const LAW_DEFAULT = { rigidity: 0.35, repulsion: 950, attraction: 80, range: 0.15 };
  /** @type {AtlasLawBounds} */
  const LAW_BOUNDS = {
    rigidity: [0.002, 0.4], // the penetration tolerated before the repulsion climbs steeply
    repulsion: [200, 8000], // the push per unit of tolerated penetration
    attraction: [0, 400], // the pull when separated but close; zero is none
    range: [0, 0.5], // the gap width the attraction acts over; zero beyond
  };
  const LAW = Object.assign({}, LAW_DEFAULT);
  // The named shapes the owner asked for. `rigid` is a knee at a hundredth of a side with a strong
  // push and seven and a half times the slope past it; `soft` lets a pair sink a third of a side
  // before the push even reaches its knee, and its push is weak enough that the resting overlap of
  // a settle is visibly deeper; `sticky` keeps a firm push and adds a pull reaching a quarter of a
  // side. Measured over 2,400 steps from the grid start (`measure_law.py --laws`).
  //
  // The rigid preset stops at a hundredth of a side rather than at the slider's own hard end
  // because the timestep is fixed at 1/120 s: below about that knee the law is stiffer than the
  // integrator can hold and the run throws squares out of the box — at rigidity 0.004 with
  // repulsion 4000, n = 17 ends needing a side of 6.82 around a box of 5.34 with a 0.21 overlap.
  // The slider still reaches there; the readout says what happened, and the notes say why.
  const LAW_PRESETS = {
    rigid: { rigidity: 0.01, repulsion: 4000, attraction: 0, range: 0 },
    soft: { rigidity: 0.35, repulsion: 400, attraction: 0, range: 0 },
    sticky: { rigidity: 0.08, repulsion: 2500, attraction: 120, range: 0.25 },
  };
  // Revision 15: the law is a function of the signed gap, and there are two relationships it can
  // describe -- square against square, and square against wall. They are the same shape and want
  // different numbers, so the shape takes the law it is evaluating rather than reading one global.
  // The owner's reasoning: a wall is not a neighbour, so borrowing the pair's settings for it was
  // a coincidence of implementation rather than a claim about the physics.
  const lawSteep = () => steepOf(LAW);
  const lawAttracts = () => attractsOf(LAW);
  const lawForce = (d) => forceOf(LAW, d);
  // The walls' own law. The defaults reproduce the shipped behaviour exactly: the old wall was
  // `PHYS.wall * min(overhang, PHYS.wallCap)`, which is this shape with a knee at the cap and no
  // steepening past it, since a rigidity at the shared reference gives a slope of zero there.
  // Attraction is
  // off, so a wall still only pushes until the owner asks otherwise.
  const WALL_DEFAULT = { rigidity: 0.25, repulsion: 2500, attraction: 0, range: 0 };
  const WALL_BOUNDS = {
    rigidity: [0.002, 0.5],
    repulsion: [0, 8000], // zero is a legitimate setting here: walls that do not push at all
    attraction: [0, 400],
    range: [0, 0.5],
  };
  const WALLLAW = Object.assign({}, WALL_DEFAULT);
  // The two laws, and everything a generic routine needs to serve either: where its controls
  // live, what its bounds are, and what it means. `pair` is masked by the relationship graph;
  // `wall` never is, because a wall is not something a square can be told to ignore.
  const LAWS = {
    pair: {
      name: "pair",
      law: LAW,
      bounds: LAW_BOUNDS,
      defaults: LAW_DEFAULT,
      prefix: "law",
      says: "square against square, masked by the relationship graph",
    },
    wall: {
      name: "wall",
      law: WALLLAW,
      bounds: WALL_BOUNDS,
      defaults: WALL_DEFAULT,
      prefix: "wall",
      says: "square against wall, never masked",
    },
  };
  const lawSpec = (name) => LAWS[name] || LAWS.pair;
  // The cache key is the concatenation of every law's every parameter, in table order, so a law
  // or a parameter added above is in the key without anyone remembering to put it there.
  const lawsKey = () =>
    Object.keys(LAWS)
      .map((n) => {
        const s = LAWS[n];
        return `${n}:${LAW_KEYS.map((k) => s.law[k]).join(":")}`;
      })
      .join("|");
  const wallForce = (d) => forceOf(WALLLAW, d);
  // One setter for any law: which one is an argument, not a copy of this function.
  function setLawOf(name, next) {
    const spec = lawSpec(name),
      o = next || {};
    for (const d of LAW_PARAMS) {
      if (o[d.key] === undefined) {
        continue;
      }
      const v = Number(o[d.key]);
      if (!Number.isFinite(v)) {
        continue;
      }
      const [lo, hi] = spec.bounds[d.key];
      // Rounded to the slider's own resolution, so the number shown is the number in use and a
      // law reached twice keys the cache identically both times.
      const q = 10 ** d.decimals;
      spec.law[d.key] = Math.round(Math.max(lo, Math.min(hi, v)) * q) / q;
    }
    // The same tail setLaw runs: the trajectory cache is keyed by the law, so a changed wall law
    // needs its run rebuilt exactly as a changed pair law does.
    markGapBar();
    if (isPhysical(state.style)) {
      ensureTrajectory(state.pair, state.style);
    }
    updateSegments();
    render();
    return Object.assign({}, spec.law);
  }
  const setWallLaw = (next) => setLawOf("wall", next);
  // How many substeps the integrator needs to hold this law.
  //
  // Semi-implicit Euler is stable only while dt < 2/omega, and omega = sqrt(k/m). The law's
  // stiffest slope is `repulsion` inside the knee and `repulsion * steep` past it, so a stiff
  // setting can demand a step the fixed 1/120 s cannot give. That is the whole of the bouncing
  // the rigid preset produced: at rigidity 0.01 and repulsion 4000 the slope reaches about
  // 30,000, so omega is near 173 and the limit near 11.5 ms against a step of 8.3 ms -- already
  // marginal for one contact, and contact forces SUM, so a square wedged against four neighbours
  // sees about four times that and a limit near 5.8 ms. Hence the safety factor: it is not
  // timidity, it is the number of contacts one square can carry.
  //
  // Substepping costs time and nothing else, and it is exact where it is not needed: at the
  // defaults the slope is 2500, omega is 50, the limit is 40 ms, and this returns 1, so the
  // shipped trajectory is unchanged to the bit. A true rigid contact is a constraint rather than
  // a stiff spring and wants projection instead (think-r2qd); this makes the spring honest in the
  // meantime rather than letting the slider reach settings the integrator cannot hold.
  // How the moving span divides. `tightenFrom` is where the correction starts, which is just
  // the two timings' ratio; `blend` is the last part of the correction, at the share it has
  // always had of it -- 0.12 of a span whose correction was 0.32 is three eighths of the
  // correction. Recomputed rather than stored, so a timing change cannot leave them stale.
  // Everything a run has to be keyed by: two runs with the same signature draw the same
  // trajectory. The seed is in it because the seed is in the simulation -- without it two
  // seeds would share one cached run and every trial would report the first one's answer.
  //
  // The two move timings are deliberately NOT in this key. `move` and `correct` are two
  // TIMES -- how long the reader watches the rearrangement, and how long the landing -- and
  // the simulation they play is the same one either way; `moveProgress` warps the clock over
  // it rather than rebuilding it. Deriving the physics' own fractions from the timings was
  // tried and measured: it put the ratio in this key, which every timing change then
  // invalidated, and took the gate from 90 seconds to over 17 minutes of rebuilding
  // trajectories nobody had asked to differ.
  const lawKey = () => `${lawsKey()}|s:${state.seed}`;
  // The blind run (revision 6, feature 3): the simulation is told nothing about where the squares
  // are meant to end up. It starts from the packing of n in a container inflated by `inflate`,
  // drops the new square into the emptiest place a coarse grid can find, and then closes the walls
  // in on the record's side with no target springs at all — only contacts, walls and the decaying
  // jiggle. The contraction clock only runs while the deepest overlap is within `overlapTol`, so a
  // jammed packing stops the squeeze rather than crushing through it.
  const BLIND = {
    inflate: 1.12, // the container starts at this multiple of the record side (adjustable)
    inflateDefault: 1.12, // ... and what `reset` puts it back to
    open: 0.12, // the fraction of the move the picture takes to open from the record of n to that box
    hold: 0.2, // the container holds while the new square inflates, then contraction begins
    close: 0.9, // and would reach the record's side here, if nothing jammed
    overlapTol: 0.08, // contraction pauses while two full-size squares overlap by more than this
    gridStep: 0.25, // the coarse grid of candidate centres for the new square
  };
  const PAD_MIN = 0.012; // the least breathing room the held view keeps around the growing container
  /** @type {AtlasStyle[]} */
  const STYLES = ["tween", "physics", "bodies"];
  /** @param {string} value @returns {value is AtlasStyle} */
  const isAtlasStyle = (value) => STYLES.some((style) => style === value);
  const isPhysical = (style) => style === "physics" || style === "bodies";
  const physicsCache = new Map();
  const PHYS_CACHE_MAX = 16;
  //: Keeps a divisor that a setting can drive to zero (a span of the move, a rigidity) off zero; a
  //: floor on a setting, not a tolerance on any measurement.
  const DIVISOR_FLOOR = 1e-6;
  // Ken Perlin's sixth-degree ease: zero first AND second derivative at both ends, where
  // smoothstep only zeroes the first. Used where a change has to start and stop invisibly.
  // Clamped as well as guarded: just below one the polynomial rounds to 1 + 2^-52, and the colour
  // levels built from it reached the painter a rounding error outside [0, 1], which it refuses --
  // seeking the last instant of a long physical step threw instead of drawing.
  const smootherstep = (x) =>
    x <= 0 ? 0 : x >= 1 ? 1 : Math.min(1, x * x * x * (x * (x * 6 - 15) + 10));
  const containerCurve = (u) => easeOut(clamp01(u / PHYS.grow));
  // How far past its target the box is open at u, in sides. Zero at both ends of the move, so the
  // side it starts from and the side it lands on are exactly the record's.
  function containerOpen(u) {
    const shutSpan = Math.max(DIVISOR_FLOOR, 1 - PHYS.blend - PHYS.shutFrom);
    const open = smootherstep(clamp01(u / PHYS.openBy));
    const shut = smootherstep(clamp01((u - PHYS.shutFrom) / shutSpan));
    return PHYS.open * open * (1 - shut);
  }
  // The side the box has at u: where it is heading, plus the breath.
  const containerSide = (a, b, u) => lerp(a, b, containerCurve(u)) + containerOpen(u);
  // A trajectory is computed in one of three modes. 'snap' is the shipped behaviour: the last
  // PHYS.blend of the move eases every square onto the record's pose and the final state is the
  // record. 'free' runs the same simulation to the end of the move with no blend and no snap, so
  // the panel can say how far the physics landed from the record by itself. 'blind' (revision 6,
  // feature 3) is the honest run: no target springs at all.
  const MODES = ["snap", "free", "blind"];
  function simMode() {
    return state.blind ? "blind" : state.snap ? "snap" : "free";
  }

  // The controller supplies corpus and UI choices; the package trajectory adapter owns every
  // numerical step and is also the Node/headless implementation.
  function simulate(pairIndex, steps, style, mode, level) {
    const p = PAIRS[pairIndex];
    const A = FRAMES[String(p.n)];
    const B = FRAMES[String(p.n + 1)];
    level = level === undefined ? state.anneal : level;
    const amp = ANNEAL.amplitude(level);
    const decayPower = ANNEAL.decayPower(level);
    const span = ANNEAL.span(level);
    const physicalStyle = style === "bodies" ? "bodies" : "physics";
    const simulationMode = MODES.includes(mode) ? mode : simMode();
    const label = `${physicalStyle}/${simulationMode}/a${level} precompute ${p.n} -> ${p.n + 1} (${steps} steps)`;
    console.time(label);
    const started = performance.now();
    const trajectory = buildTrajectory({
      pairIndex,
      pair: p,
      source: A,
      target: B,
      steps,
      style: physicalStyle,
      mode: simulationMode,
      effectiveSeed: withSeed(p.n),
      pairLaw: Object.assign({}, LAW),
      wallLaw: Object.assign({}, WALLLAW),
      relatedMask: maskFor(pairIndex),
      anneal: { level, amplitude: amp, decayPower, span },
      physics: {
        omega: PHYS.omega,
        zeta: PHYS.zeta,
        springRamp: PHYS.springRamp,
        contactDamping: PHYS.contactDamping,
        contactTorque: PHYS.contactTorque,
        lockIn: PHYS.lockIn,
        open: PHYS.open,
        openBy: PHYS.openBy,
        shutFrom: PHYS.shutFrom,
        tighten: PHYS.tighten,
        tightenFrom: PHYS.tightenFrom,
        grow: PHYS.grow,
        jiggle: PHYS.jiggle,
        jiggleTorque: PHYS.jiggleTorque,
        bodiesJiggle: BODIES.jiggle,
        bodiesJiggleTorque: BODIES.jiggleTorque,
        jiggleHz: [PHYS.jiggleHz[0], PHYS.jiggleHz[1]],
        drop: PHYS.drop,
        appear: PHYS.appear,
        inflateFrom: PHYS.inflateFrom,
        blend: PHYS.blend,
        maxSpeed: PHYS.maxSpeed,
        maxSpin: PHYS.maxSpin,
        cell: PHYS.cell,
      },
      blind: {
        inflate: BLIND.inflate,
        hold: BLIND.hold,
        close: BLIND.close,
        overlapTolerance: BLIND.overlapTol,
        gridStep: BLIND.gridStep,
      },
    });
    const ms = performance.now() - started;
    console.timeEnd(label);
    return Object.assign(trajectory, {
      law: lawKey(),
      ms,
      anneal: level,
      annealAmplitude: amp,
      annealSpan: span,
      annealDecay: decayPower,
    });
  }
  // The step count: 120 a second of the annealed move, so a level that lengthens the move buys sub-
  // steps at the same dt rather than a finer integration of the same span.
  function physicsSteps(pairIndex, style) {
    // The whole moving span, not just the rearrangement: the physics runs through the landing
    // too, and `move` stopped being the whole of it when the correction got its own time.
    // Reading `move` alone cut a run's steps by 31 per cent at the shipped beat, which
    // the revision-7 checks caught as every free run suddenly missing by ten times as much.
    // And the base timing, not the one the clock plays: the simple-transition speed-up is
    // presentation, and pricing steps off the played span halved a grid fill's physics work in
    // `physics()` and the annealing benchmark.
    const tm = timelineBaseTiming(timelineConfiguration(), pairIndex, style);
    return Math.max(1, Math.round(PHYS.stepsPerSecond * (tm.move + tm.correct)));
  }
  function ensureTrajectory(pairIndex, style, mode) {
    const key = trajectoryKey(pairIndex, style, mode);
    let tr = physicsCache.get(key);
    if (!tr) {
      tr = simulate(
        pairIndex,
        physicsSteps(pairIndex, style),
        style,
        trajectoryMode(mode),
        state.anneal,
      );
      if (physicsCache.size >= PHYS_CACHE_MAX) {
        physicsCache.delete(physicsCache.keys().next().value);
      }
      physicsCache.set(key, tr);
    }
    return tr;
  }
  function trajectoryMode(mode) {
    return MODES.includes(mode) ? mode : simMode();
  }
  // Everything a trajectory is a function of. The law is in the key: a trajectory drawn under one
  // law is not the trajectory of another.
  function trajectoryKey(pairIndex, style, requestedMode) {
    const mode = trajectoryMode(requestedMode);
    const steps = physicsSteps(pairIndex, style);
    return (
      style +
      "/" +
      mode +
      (mode === "blind" ? `:${BLIND.inflate}` : "") +
      "/a" +
      state.anneal +
      "/L" +
      lawKey() +
      "/R" +
      relKey() +
      "/G" +
      growKey() +
      "/" +
      pairIndex +
      "/" +
      steps
    );
  }
  // The package reader is shared by interactive seek and deterministic capture.
  function samplePose(tr, u, i) {
    return sampleTrajectoryPose(tr, i, u);
  }
  // The container's side at move fraction u, from the same cache: a blind run's box is not a
  // function of the clock, so it has to be read back rather than recomputed.
  function sampleSide(tr, u) {
    return sampleTrajectorySide(tr, u);
  }

  // ---------------------------------------------------------------- editing the law (revision 11)
  // Four numbers, each with a setter and a getter, each in the trajectory cache key, each
  // deterministic. Setting one drops nothing: the cache is keyed rather than cleared, so going back
  // to a law already run is instant and gives the same trajectory it gave before.
  function setLaw(next) {
    const o = next || {};
    for (const key of ["rigidity", "repulsion", "attraction", "range"]) {
      if (o[key] === undefined) {
        continue;
      }
      const v = Number(o[key]);
      if (!Number.isFinite(v)) {
        continue;
      }
      const [lo, hi] = LAW_BOUNDS[key];
      // Rounded to the slider's own resolution, so the number shown is the number in use and the
      // cache key of a law reached twice is the same string both times.
      const q = key === "rigidity" ? 1000 : key === "range" ? 1000 : 1;
      LAW[key] = Math.round(Math.max(lo, Math.min(hi, v)) * q) / q;
    }
    markGapBar();
    if (isPhysical(state.style)) {
      ensureTrajectory(state.pair, state.style);
    }
    drawLawPlot();
    updateSegments();
    render();
    return lawState();
  }
  function setLawPreset(name) {
    const preset = LAW_PRESETS[name] || (name === "default" ? LAW_DEFAULT : null);
    if (preset === null) {
      return lawState();
    }
    return setLaw(preset);
  }
  function lawState() {
    return {
      rigidity: LAW.rigidity,
      repulsion: LAW.repulsion,
      attraction: LAW.attraction,
      range: LAW.range,
      steep: lawSteep(),
      bounds: LAW_BOUNDS,
      defaults: Object.assign({}, LAW_DEFAULT),
      presets: Object.keys(LAW_PRESETS),
      key: lawKey(),
      // The two numbers that say what the law is doing where it matters: the push at the knee, and
      // the deepest pull. The pull is the smaller of the two by construction.
      pushAtKnee: LAW.repulsion * LAW.rigidity,
      pullPeak: lawAttracts() ? LAW.attraction : 0,
    };
  }
  // ---------------------------------------------------------------- the law, drawn (revision 11)
  // The plot's own geometry. The horizontal axis is the signed gap over the whole editable domain,
  // -0.42 (the softest rigidity, and a little past it) through +0.52 (the longest attraction range,
  // and a little past it), so a handle can never be dragged off the plot. The vertical axis is two
  // half-axes: the push above the zero line on a ladder that keeps whatever the law currently peaks
  // at inside the box, and the pull below it on the attraction's own fixed bound. Two half-scales
  // rather than one, because a rigid law's push is two orders of magnitude above any pull and one
  // scale would draw every pull as a flat line.
  const LP = {
    w: 300,
    h: 132,
    zero: 88,
    pullSpan: 44,
    dLo: -0.42,
    dHi: 0.52,
    ladder: [200, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000],
  };
  const lpX = (d) => ((d - LP.dLo) / (LP.dHi - LP.dLo)) * LP.w;
  const lpD = (x) => LP.dLo + (x / LP.w) * (LP.dHi - LP.dLo);
  function lpTop() {
    const peak = Math.max(lawForce(LP.dLo), LAW.repulsion * LAW.rigidity, 1);
    for (const v of LP.ladder) {
      if (peak <= v) {
        return v;
      }
    }
    return LP.ladder[LP.ladder.length - 1];
  }
  const lpPushY = (f, top) => LP.zero - Math.min(1, Math.max(0, f / top)) * LP.zero;
  const lpPullY = (f) =>
    LP.zero + Math.min(1, Math.max(0, -f / LAW_BOUNDS.attraction[1])) * LP.pullSpan;
  const lpY = (f, top) => (f >= 0 ? lpPushY(f, top) : lpPullY(f));
  let lawPlot = null;
  //: How far beside each breakpoint of the force law the plot also samples it, so the corner is drawn
  //: as a corner; an offset along the gap axis of a drawing, unrelated to validity.
  const LAW_BREAKPOINT_OFFSET = 1e-6;
  function drawLawPlot() {
    if (lawPlot === null) {
      lawPlot = {
        svg: svgNode("law-plot"),
        curve: svgNode("lp-curve"),
        cross: svgNode("lp-cross"),
        knee: svgNode("lp-knee"),
        pull: svgNode("lp-pull"),
        vaxis: svgNode("lp-vaxis"),
        top: svgNode("lp-top"),
        left: svgNode("lp-left"),
        right: svgNode("lp-right"),
      };
    }
    const g = lawPlot;
    if (g.svg === null) {
      return;
    }
    const top = lpTop();
    const x0 = lpX(0);
    g.vaxis.setAttribute("x1", fmt(x0, 2));
    g.vaxis.setAttribute("x2", fmt(x0, 2));
    g.cross.setAttribute("cx", fmt(x0, 2));
    // The curve, sampled densely enough that the knee is a corner rather than a bevel, with the two
    // breakpoints (the knee and the edge of the attraction range) sampled exactly.
    const xs = [];
    for (let i = 0; i <= 120; i++) {
      xs.push(lerp(LP.dLo, LP.dHi, i / 120));
    }
    xs.push(-LAW.rigidity, -LAW.rigidity - LAW_BREAKPOINT_OFFSET, 0, LAW_BREAKPOINT_OFFSET);
    if (lawAttracts()) {
      xs.push(LAW.range, LAW.range - LAW_BREAKPOINT_OFFSET, LAW.range / 2);
    }
    xs.sort((a, b) => a - b);
    let d = "";
    for (let i = 0; i < xs.length; i++) {
      const px = lpX(xs[i]),
        py = lpY(lawForce(xs[i]), top);
      d += `${(i === 0 ? "M" : "L") + fmt(px, 2)} ${fmt(py, 2)}`;
    }
    g.curve.setAttribute("d", d);
    g.knee.setAttribute("cx", fmt(lpX(-LAW.rigidity), 2));
    g.knee.setAttribute("cy", fmt(lpPushY(LAW.repulsion * LAW.rigidity, top), 2));
    const attracts = lawAttracts();
    g.pull.style.display = attracts ? "" : "none";
    if (attracts) {
      g.pull.setAttribute("cx", fmt(lpX(LAW.range / 2), 2));
      g.pull.setAttribute("cy", fmt(lpPullY(-LAW.attraction), 2));
    }
    g.top.textContent = String(top);
    g.left.textContent = fmt(LP.dLo, 2);
    g.right.textContent = `+${fmt(LP.dHi, 2)}`;
  }
  // The two handles are the four numbers. The knee's position along the axis is the rigidity and its
  // height the repulsion (the height *is* repulsion x rigidity, so moving it sideways at a fixed
  // height changes the stiffness, which is what "the same push at a different depth" means); the
  // pull's position is half the range and its depth the attraction. Dragging and the sliders write
  // the same state through the same setter, so neither can get ahead of the other.
  // The push scale is frozen for the length of a drag. It is chosen from a ladder that follows the
  // law's own peak, and recomputing it mid-drag made the knee rubbery: dragging it past the shipped
  // rigidity flattens the slope, which drops the peak, which drops the ladder rung, which moves the
  // handle out from under the cursor. Frozen at press, updated on release.
  let lpDrag = null,
    lpDragTop = 0;
  function lpPoint(ev) {
    const r = lawPlot.svg.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) {
      return null;
    }
    return [((ev.clientX - r.left) / r.width) * LP.w, ((ev.clientY - r.top) / r.height) * LP.h];
  }
  function lpNear(pt, node) {
    const dx = pt[0] - Number(node.getAttribute("cx")),
      dy = pt[1] - Number(node.getAttribute("cy"));
    return dx * dx + dy * dy <= 196;
  }
  function lpApply(which, pt, top) {
    if (top === undefined) {
      top = lpTop();
    }
    if (which === "knee") {
      const rigidity = Math.max(
        LAW_BOUNDS.rigidity[0],
        Math.min(LAW_BOUNDS.rigidity[1], -lpD(pt[0])),
      );
      const push = Math.max(0, (LP.zero - Math.min(LP.zero, Math.max(0, pt[1]))) / LP.zero) * top;
      setLaw({ rigidity, repulsion: push / Math.max(rigidity, DIVISOR_FLOOR) });
      return;
    }
    const range = Math.max(0, Math.min(LAW_BOUNDS.range[1], lpD(pt[0]) * 2));
    const pull =
      Math.max(0, Math.min(1, (pt[1] - LP.zero) / LP.pullSpan)) * LAW_BOUNDS.attraction[1];
    setLaw({ range, attraction: pull });
  }
  function lawPlotWiring() {
    if (lawPlot === null) {
      drawLawPlot();
    }
    const svgEl = lawPlot.svg;
    svgEl.addEventListener("pointerdown", (ev) => {
      const pt = lpPoint(ev);
      if (pt === null) {
        return;
      }
      const which = lpNear(pt, lawPlot.knee)
        ? "knee"
        : lawAttracts() && lpNear(pt, lawPlot.pull)
          ? "pull"
          : null;
      if (which === null) {
        return;
      }
      ev.preventDefault();
      lpDrag = which;
      lpDragTop = lpTop();
      svgEl.setPointerCapture(ev.pointerId);
      lpApply(which, pt, lpDragTop);
    });
    svgEl.addEventListener("pointermove", (ev) => {
      if (lpDrag === null) {
        return;
      }
      const pt = lpPoint(ev);
      if (pt === null) {
        return;
      }
      ev.preventDefault();
      lpApply(lpDrag, pt, lpDragTop);
    });
    const end = (ev) => {
      if (lpDrag === null) {
        return;
      }
      if (svgEl.hasPointerCapture(ev.pointerId)) {
        svgEl.releasePointerCapture(ev.pointerId);
      }
      lpDrag = null;
      drawLawPlot();
    };
    svgEl.addEventListener("pointerup", end);
    svgEl.addEventListener("pointercancel", end);
  }
  // For tests and for the checkers: drag a handle to a law directly, without a pointer.
  function dragLaw(which, gap, force) {
    if (lawPlot === null) {
      drawLawPlot();
    }
    const top = lpTop();
    lpApply(which === "pull" ? "pull" : "knee", [lpX(Number(gap)), lpY(Number(force), top)]);
    return lawState();
  }
  // ---------------------------------------------------------------- growth, read and set
  // Revision 13: **the starting size is a property of the arrangement on the stage, not of a run.**
  // Setting it redraws the squares at once, in Pack, whether or not `grow` is on and whether or not
  // a run has been started. Two rules carry that, and `stagePack` below is the second of them.
  //
  //   - A run already on the stage takes the new size where it stands, at any step count, *unless*
  //     it has grown: growth writes the same field every step, so a size the run reached is the
  //     run's own and the setting names what the *next* run will begin at. With growth off `grew`
  //     stays zero for ever, so the stage tracks the slider for the whole of such a run, and no
  //     drag is thrown away to do it — only the size changes, never a pose.
  //   - A Pack stage that has no arrangement of its own gets one, so that the size has something to
  //     be the size of. That is the previous-packing start, which shows the step animation rather
  //     than a run; see `stagePack`.
  function setGrowth(next) {
    const o = next || {};
    const wasSize = GROWTH.size;
    if (o.size !== undefined) {
      const v = Number(o.size);
      if (Number.isFinite(v)) {
        GROWTH.size =
          Math.round(Math.max(GROWTH_BOUNDS.size[0], Math.min(GROWTH_BOUNDS.size[1], v)) * 1000) /
          1000;
      }
    }
    if (o.rate !== undefined) {
      const v = Number(o.rate);
      if (Number.isFinite(v)) {
        GROWTH.rate =
          Math.round(Math.max(GROWTH_BOUNDS.rate[0], Math.min(GROWTH_BOUNDS.rate[1], v)) * 1000) /
          1000;
      }
    }
    if (o.rule !== undefined) {
      GROWTH.rule = GROWTH_RULES.includes(o.rule) ? o.rule : GROWTH_DEFAULT.rule;
    }
    if (o.on !== undefined) {
      GROWTH.on = !!o.on;
    }
    if (opt !== null && opt.grew === 0) {
      setPackSquareSide(opt, GROWTH.size);
    }
    if (GROWTH.size !== wasSize) {
      stagePack();
    }
    markGapBar();
    updateSegments();
    render();
    return growthState();
  }
  // Revision 14: **in Pack, `n` means that many squares packed, so all `n` of them are on the stage
  // from the first frame**, wherever the starting arrangement puts them. The owner's question was
  // "if 17 is set below in pack mode why does the diagram show 16 to begin with", and the answer was
  // that Pack opened on the timeline — the previous packing, with the seventeenth square staged for
  // an arrival it would only make if a step were played. That is the transition model leaking into a
  // mode which has no transitions.
  //
  // So the previous-packing start, which is the only one with no arrangement of its own, is staged
  // as one *always* rather than only below a full starting size: the packing of n with the arriving
  // square at its own starting pose, in the run's own box, which is the frame `optimize()` would
  // begin from at that instant. Revision 13's rule is the same rule with its condition dropped, and
  // the size still applies to the arrangement, because there is now always an arrangement for it to
  // apply to.
  //
  // Animate is untouched. Animate plays a range of steps, its stage is the animation between two
  // records, and the arrival staging and the step header are correct there.
  function stagePack() {
    if (state.mode !== "pack" || state.initial !== "previous" || state.playing) {
      return;
    }
    if (opt === null) {
      state.optimizing = true;
      opt = newOptimizer("previous");
    }
  }
  // What the growth is doing, and — the only figure that is about a packing rather than a picture —
  // the box the arrangement would need **at unit size**.
  function growthState() {
    const size = opt === null ? GROWTH.size : opt.size;
    const record = FRAMES[String(PAIRS[state.pair].n + 1)].side;
    const tight = opt === null ? null : opt.required;
    const unit = tight === null ? null : tight / size;
    const pen = opt === null || !Number.isFinite(opt.pen) ? null : opt.pen;
    const clean = pen !== null && pen <= OPT.feasible;
    const packing = opt?.packingValid === true;
    return {
      on: GROWTH.on,
      size,
      rate: GROWTH.rate,
      rule: GROWTH.rule,
      rules: GROWTH_RULES.slice(),
      bounds: GROWTH_BOUNDS,
      defaults: Object.assign({}, GROWTH_DEFAULT),
      growing: GROWTH.on && opt !== null && size < 1 && !opt.stalled,
      stalled: GROWTH.on && opt !== null && size < 1 && !!opt.stalled,
      done: GROWTH.on && size >= 1,
      // The container the squares are actually in, the tight box around them, and what that box
      // would be if every square were grown to a unit side keeping the arrangement's shape.
      side: opt === null ? null : opt.side,
      sideAtSize: tight,
      unitSide: unit,
      record,
      penetration: pen,
      // Within the growth rule's own overlap allowance, which decides whether the size may climb.
      // It is not a packing test: `packing` is.
      clean,
      // A packing under the one validity contract: unit squares, and pair and wall penetration
      // within 1e-9. It used to be full size with the overlap inside the growth rule's 0.008,
      // which called an arrangement a packing at eight million times the contract's tolerance.
      packing,
      // Below a record as a packing is not a find: it is a report that the geometry lost precision.
      suspect: packing && tight !== null && tight < record - PACKING_VALIDITY.penetrationTolerance,
      excess: packing && unit !== null ? (unit / record - 1) * 100 : null,
    };
  }
  // ---------------------------------------------------------------- reset (revision 11)
  // Every physics parameter back to its default, and the run restarted from the arrangement the
  // page is already showing. It does not touch n, the aspect, or which start is chosen: what is on
  // the stage stays what is on the stage, and only the physics acting on it is put back.
  function resetPhysics() {
    LAW.rigidity = LAW_DEFAULT.rigidity;
    LAW.repulsion = LAW_DEFAULT.repulsion;
    LAW.attraction = LAW_DEFAULT.attraction;
    LAW.range = LAW_DEFAULT.range;
    relKind = "general";
    targetEdges = null;
    // The target goes back to the record's graph and the drawing mode comes off, but
    // the edges the owner drew are *not* thrown away: they are work, like a dragged
    // arrangement, and reset has never touched that either.
    targetSource = "record";
    state.drawing = false;
    relCache.clear();
    GROWTH.on = GROWTH_DEFAULT.on;
    GROWTH.size = GROWTH_DEFAULT.size;
    GROWTH.rate = GROWTH_DEFAULT.rate;
    GROWTH.rule = GROWTH_DEFAULT.rule;
    state.anneal = ANNEAL.dflt;
    state.blind = false;
    state.snap = true;
    BLIND.inflate = BLIND.inflateDefault;
    markGapBar();
    // Restart from the start the page is on, without changing which start that is. A timeline that
    // was not optimizing is left as a timeline. Revision 14: a reset never starts the clock —
    // in Pack every stage is a run now, and a button that says `reset physics` must not also press
    // play, so a run that was paused comes back paused.
    if (state.optimizing) {
      const was = state.playing;
      optimize(true);
      if (!was) {
        pause();
      }
    } else {
      pause();
      if (isPhysical(state.style)) {
        ensureTrajectory(state.pair, state.style);
      }
      drawLawPlot();
      updateSegments();
      render();
    }
    return {
      law: lawState(),
      relationship: relationshipState(),
      growth: growthState(),
      anneal: state.anneal,
    };
  }

  // ---------------------------------------------------------------- choosing the relationship
  // Setting the graph is cheap — it neither clears the trajectory cache nor restarts a run — but it
  // does change what a run does next, so the trajectory key carries it and a live run picks the new
  // mask up on its next step.
  function setRelationship(kind) {
    const next = RELATIONSHIPS.includes(kind) ? kind : "general";
    if (next === relKind) {
      updateSegments();
      return relationshipState();
    }
    relKind = next;
    relCache.clear();
    markGapBar();
    if (isPhysical(state.style)) {
      ensureTrajectory(state.pair, state.style);
    }
    updateSegments();
    render();
    return relationshipState();
  }
  // A graph from anywhere: a flat list of index pairs in the run's own square order, or null to go
  // back to deriving it from the record. Only the contact relationship reads it.
  function setTargetGraph(edges) {
    if (edges === null || edges === undefined) {
      targetEdges = null;
    } else {
      const flat = [];
      for (const e of edges) {
        if (Array.isArray(e)) {
          flat.push(e[0] | 0);
          flat.push(e[1] | 0);
        } else {
          flat.push(e | 0);
        }
      }
      targetEdges = flat;
    }
    graphChanged();
    return relationshipState();
  }
  // ------------------------------------------------- the hand-drawn contact graph (revision 12)
  // The owner: "it would be nice if you can click and drag a link between any two boxes to add to
  // their contact graph." The edges are held per packing size, as a flat list of index pairs in the
  // run's own square order with the lower index first, deduplicated: an index means a different
  // square at a different n, so a graph drawn at n = 11 is not a graph at n = 5, and switching back
  // finds what was left there.
  //
  // Nothing about the physics knows where the edges came from. They arrive at the mask through the
  // one path the record's own graph uses — `targetGraphFor` — so a random or enumerated graph
  // handed to `setEdges` would drive a run exactly as a drawn one does.
  function graphChanged() {
    relCache.clear();
    markGapBar();
    if (isPhysical(state.style)) {
      ensureTrajectory(state.pair, state.style);
    }
    updateSegments();
    render();
  }
  // Index pairs from anything — a flat list or a list of pairs — folded to a < b, deduplicated, and
  // dropped where they name a square this n does not have.
  function normalizeEdges(pairs, N) {
    const flat = [];
    for (const e of pairs || []) {
      if (Array.isArray(e)) {
        flat.push(e[0]);
        flat.push(e[1]);
      } else {
        flat.push(e);
      }
    }
    const seen = new Set(),
      out = [];
    for (let i = 0; i + 1 < flat.length; i += 2) {
      const a = Math.round(Number(flat[i])),
        b = Math.round(Number(flat[i + 1]));
      if (!Number.isFinite(a) || !Number.isFinite(b) || a === b) {
        continue;
      }
      const lo = Math.min(a, b),
        hi = Math.max(a, b);
      if (lo < 0 || hi >= N) {
        continue;
      }
      const key = lo * N + hi;
      if (seen.has(key)) {
        continue;
      }
      seen.add(key);
      out.push(lo);
      out.push(hi);
    }
    return out;
  }
  function writeDrawn(flat) {
    const key = drawnKeyFor(state.pair);
    if (flat.length) {
      drawnGraphs.set(key, flat);
    } else {
      drawnGraphs.delete(key);
    }
    graphChanged();
  }
  // The drawn graph of the n on the stage, as pairs.
  function drawnEdges() {
    const flat = drawnFor(state.pair);
    /** @type {[number, number][]} */
    const out = [];
    for (let i = 0; i + 1 < flat.length; i += 2) {
      out.push([flat[i], flat[i + 1]]);
    }
    return out;
  }
  // Replacing the whole graph points the target at it: a graph nothing reads would be a drawing,
  // not a target, and the point of the call is to drive a run with it.
  function setEdges(pairs) {
    const N = poseA === null ? PAIRS[state.pair].n + 1 : poseA.length;
    writeDrawn(normalizeEdges(pairs, N));
    targetSource = "drawn";
    targetEdges = null;
    graphChanged();
    return drawnEdges();
  }
  function clearEdges() {
    writeDrawn([]);
    return drawnEdges();
  }
  // One edge on or off, which is what a drag between two squares does. Returns whether the edge is
  // there afterwards.
  function toggleEdge(a, b) {
    const N = poseA === null ? PAIRS[state.pair].n + 1 : poseA.length;
    const one = normalizeEdges([[a, b]], N);
    if (one.length !== 2) {
      return false;
    }
    const flat = drawnFor(state.pair).slice();
    let at = -1;
    for (let i = 0; i + 1 < flat.length; i += 2) {
      if (flat[i] === one[0] && flat[i + 1] === one[1]) {
        at = i;
        break;
      }
    }
    if (at >= 0) {
      flat.splice(at, 2);
    } else {
      flat.push(one[0]);
      flat.push(one[1]);
    }
    writeDrawn(flat);
    return at < 0;
  }
  // Which graph the contact relationship reads. `setTargetGraph` still overrides both.
  function setTargetSource(kind) {
    targetSource = TARGET_SOURCES.includes(kind) ? kind : "record";
    graphChanged();
    return targetFrom();
  }
  // What the graph is, how big it is, and — the number that says whether biasing toward a contact
  // graph does anything — how many of the target's edges are in contact on the stage right now.
  function relationshipState() {
    const target = targetGraphFor(state.pair);
    const edges = target.length / 2;
    const N = poseA === null ? 0 : poseA.length;
    let met = 0;
    for (let e = 0; e + 1 < target.length; e += 2) {
      const a = target[e],
        b = target[e + 1];
      if (a >= N || b >= N) {
        continue;
      }
      if (paintTouching.has(a < b ? a * N + b : b * N + a)) {
        met++;
      }
    }
    const entry = relationshipFor(state.pair);
    return {
      kind: relKind,
      kinds: RELATIONSHIPS.slice(),
      target: targetFrom(),
      sources: TARGET_SOURCES.slice(),
      drawn: drawnFor(state.pair).length / 2,
      // What the trajectory cache keys a run by: the graph and, where it is the drawn one, the
      // revision of it. Two graphs are two runs, and one graph twice is one run.
      key: relKey(),
      // The target graph's size, and how much of it the picture has realised.
      edges,
      met,
      fraction: edges > 0 ? met / edges : 0,
      // The mask actually in force, which is the whole target under 'contact', the blocks' own
      // cliques under 'groups' and every pair under 'general'.
      maskEdges: relKind === "general" ? null : entry.edges.length / 2,
      // The picture's own contact graph, which is what `met` was counted against.
      frameEdges: paintTouching.size,
      side: sceneSide,
      record: FRAMES[String(PAIRS[state.pair].n + 1)].side,
      attracting: lawAttracts(),
    };
  }
  // The law sampled, for the plot and for anything that wants to check its shape off the page.
  function lawCurve(count) {
    const m = Math.max(4, Math.round(Number(count) || 60));
    const lo = -Math.max(LAW.rigidity * 2, 0.08);
    const hi = Math.max(lawAttracts() ? LAW.range : 0, 0.08);
    /** @type {[number, number][]} */
    const out = [];
    for (let i = 0; i <= m; i++) {
      const d = lerp(lo, hi, i / m);
      out.push([d, lawForce(d)]);
    }
    return out;
  }

  // Revision 9: the three legend lines are gone from the stage. What a free or blind run reached is
  // still on the API — `physics(index, style, mode).miss` — and the live readout below carries the
  // same numbers frame by frame, so nothing had to be measured differently to drop the prose.

  // ---------------------------------------------------------------- the live gap (revision 7, feature 3)
  // How far off the best known the picture on the stage is, this frame: the largest distance a
  // square's centre is from the record's, the largest angle error modulo 90 degrees, and the side
  // of the smallest axis-aligned box that holds the squares as drawn, against the record's side.
  // It is measured from the poses the scene drew, so it means the same thing under every style: an
  // interpolation shows it closing to nothing, a snapped run reaches nothing at the end, a free run
  // rests at its residual. In a blind run the squares have no correspondence to the record's
  // labelling, so the centre and angle errors are meaningless and only the box is reported.
  // `count` is how many of the squares to measure, from the first: the squares the frame shows.
  // `size` is the side they are drawn at, so a run of shrunken squares reads its own box.
  const gapOut = { centre: 0, angle: 0, side: 0 };
  function gapOf(px, py, pa, count, size) {
    let centre = 0,
      angle = 0,
      x0 = Infinity,
      x1 = -Infinity,
      y0 = Infinity,
      y1 = -Infinity;
    for (let i = 0; i < count; i++) {
      const dx = px[i] - tgtX[i],
        dy = py[i] - tgtY[i];
      const d = Math.sqrt(dx * dx + dy * dy);
      if (d > centre) {
        centre = d;
      }
      const da = Math.abs(angleDelta(tgtA[i], pa[i]));
      if (da > angle) {
        angle = da;
      }
      const cs = Math.cos(pa[i] * DEG) * (size / 2),
        sn = Math.sin(pa[i] * DEG) * (size / 2);
      for (let q = 0; q < 4; q++) {
        const s1 = q & 1 ? -1 : 1,
          s2 = q & 2 ? -1 : 1;
        const vx = px[i] + s1 * cs - s2 * sn,
          vy = py[i] + s1 * sn + s2 * cs;
        if (vx < x0) {
          x0 = vx;
        }
        if (vx > x1) {
          x1 = vx;
        }
        if (vy < y0) {
          y0 = vy;
        }
        if (vy > y1) {
          y1 = vy;
        }
      }
    }
    gapOut.centre = centre;
    gapOut.angle = angle;
    gapOut.side = Math.max(x1 - x0, y1 - y0);
    return gapOut;
  }

  // ---------------------------------------------------------------- the gap bar (revision 8, feature 4)
  // One horizontal bar for the n the range steps into: the proved lower bound at the left, the best
  // known as a labelled tick, the span between them shaded because that is the territory nobody has
  // closed, and a hand on the side the arrangement on the stage would actually need. Both numbers
  // are the ones the panel prints two lines further down, `s(n) <= ...` and `s(n) >= ...`, read
  // straight off the record rather than re-derived.
  // Revision 9: the hand is not redrawn every frame. The motion is already visible in the packing,
  // so a second animated readout of it is noise. The bar redraws when the picture is not moving —
  // through the dwell and from the moment the settle ends — at a step boundary, whenever a setting
  // that changes the answer is touched, and on demand (`refreshGap()` and the button beside it).
  // The two text rows below the bar stay live: they are numbers, not a moving indicator, and a drag
  // has to show its effect on the required side at once.
  let gapBarDirty = true;
  function markGapBar() {
    gapBarDirty = true;
  }
  const GAPBAR = {
    width: 680,
    // How far in from each end of the rail the scale's own ends are marked. The rail is the full
    // width of the column; `sqrt(n)` sits at `inset` and `sqrt(n) + 1` at `width - inset`, so the
    // bar reads as a scale with two ticks on it rather than as a box with two hard ends -- and an
    // arrow pinned to either extreme has room to be drawn whole.
    inset: 34,
    // **Both ends are formulas, and the span is one unit side at every n.**
    //
    // The left end is `sqrt(n)`: n unit squares have area n, so no box with a smaller side can hold
    // them whatever the arrangement. It is the one bound on this bar that needs no citation, and it
    // is where every proved lower bound starts from.
    //
    // The right end is `sqrt(n) + 1`, and it is a BOUND rather than a margin: n unit squares fit a
    // grid of side `ceil(sqrt(n))`, and `ceil(sqrt(n)) < sqrt(n) + 1`, so no best known packing can
    // reach the right end of this bar. Checked against the corpus: no record exceeds the grid
    // bound, and the furthest any sits above the area bound is 0.586 of a side at n = 2, median
    // 0.458. So the bar runs from what area forbids to what a grid achieves.
    //
    // A constant span is what makes two bars comparable -- the same distance means the same
    // distance at n = 11 and at n = 300, which a headroom proportional to the open gap could not
    // say.
    //
    // **The bar runs between whole integers, and the two formulas are marks inside it.** It used
    // to run from `sqrt(n)` to `sqrt(n) + 1` exactly, so both of its ends moved with every n --
    // 5.10 to 6.10 at n = 26, 5.20 to 6.20 at n = 27 -- and nothing on it was ever twice in the
    // same place. A reader watching a sweep had no fixed thing to hold on to. Running from
    // `floor(sqrt(n))` to two above it, the scale changes only when `floor(sqrt(n))` does, which
    // is once per perfect square: one bar for all of 17..24, another for 25..35.
    //
    // Two rather than `ceil(sqrt(n) + 1)`, which would be one at a perfect square and two
    // everywhere else -- and a scale that halves between n = 16 and n = 17 is the problem this
    // change exists to remove.
    span: 2.0,
  };
  // What it takes to say the picture *is* the record: every square on its own target, not merely a
  // box that happens to be small enough. A blind run has no correspondence to the record's
  // labelling, so there the box is the whole test — and it never wins it.
  const GAP_MET = { centre: 0.02, angle: 0.5, side: 0.002 };
  const gapbar = htmlNode("gapbar");
  const gapbarOpen = svgNode("gapbar-open");
  const gapbarLowerRule = svgNode("gapbar-lower-rule");
  const gapbarRecordRule = svgNode("gapbar-record-rule");
  const gapbarTicks = svgNode("gapbar-ticks");
  /** @type {HTMLElement} */
  const gapbarAreaEnd = document.querySelector(".gapbar-area");
  /** @type {HTMLElement} */
  const gapbarGridEnd = document.querySelector(".gapbar-grid");
  // How a number is written on this diagram: an exact integer as an integer, and anything
  // else to three places. `5` rather than `5.00`, because the second says a measurement was
  // taken to two places when in fact the value is four.
  const barNum = (value) => (Number.isInteger(value) ? String(value) : value.toFixed(3));
  const gapbarHand = svgNode("gapbar-hand");
  const gapbarBox = svgNode("gapbar-box");
  const gapbarLowerLabel = svgNode("gapbar-lower-label");
  // An SVG text node, not an HTML one, which is why `measureDigit` can ask it for its
  // `getComputedTextLength`. `getElementById` is typed as returning an HTML element whatever it
  // finds, so the step through `Element` is what lets the SVG type be named at all.
  const gapbarRecordLabel = /** @type {SVGTextElement} */ (
    /** @type {Element} */ (svgNode("gapbar-record-label"))
  );
  let gapbarInfo = null;
  const gapbarOut = {
    n: 0,
    record: 0,
    lower: 0,
    lo: 0,
    hi: 0,
    side: 0,
    x: 0,
    /** @type {number | null} */
    excess: 0,
    met: false,
    // Whether the side above is a claim at all: a bounding box reports a number for any
    // arrangement, and only a packing under the one validity contract has a side.
    valid: false,
    /** @type {string | null} */
    reason: null,
    // The deepest pair or wall penetration, and the tolerance the assessment held it to.
    overlap: 0,
    tolerance: 0,
    /** @type {"packing" | "catalogue-precision"} */
    precision: "packing",
  };
  // The scale and the static marks, once per n rather than once per frame.
  // **The bar is keyed to the n on the panel, not to the n the step is heading for.** Through the
  // dwell the stage shows the packing of n - 1 and the panel says so, but the bar was measuring it
  // against n's record: at the step into 26 that put a 25-square packing, side 5.0000, against a
  // record of 5.6213 and drew the pointer at one per cent of the bar -- eleven per cent "under the
  // best known", for a third of every step. It was reading a true number about the wrong n.
  function gapbarSetup(p, shown) {
    const n = shown || p.n + 1;
    if (gapbarInfo !== null && gapbarInfo.n === n) {
      return gapbarInfo;
    }
    const f = FACTS[String(n)];
    const record = Number(f.side);
    // A proved n carries no separate lower bound: the bound is the value, and the gap is nothing.
    const lower = f.lower === null ? record : Number(f.lower);
    const root = Math.sqrt(n);
    // **One below the grid bound**, not one below the area bound. The two are the same wherever
    // `sqrt(n)` is irrational, and they differ at exactly the n where it matters: at a perfect
    // square `ceil(sqrt(n))` IS `sqrt(n)`, so flooring would start the bar at the record itself
    // and leave it hard against the left end with an empty unit to its right. n = 36 ran 6 to 8
    // with its record at 6; it runs 5 to 7 now, with the record in the middle.
    //
    // The span always contains `[sqrt(n), sqrt(n) + 1]`, which is what the bar is about:
    // `ceil(x) - 1 <= x` and `ceil(x) + 1 >= x + 1` for every x.
    const lo = Math.ceil(root) - 1;
    const hi = lo + GAPBAR.span;
    gapbarInfo = { n, record, lower, lo, hi, proved: f.lower === null };
    const xr = gapbarX(record);
    gapbarOpen.setAttribute("x", fmt(gapbarX(lower), 2));
    gapbarOpen.setAttribute("width", fmt(Math.max(0, xr - gapbarX(lower)), 2));
    const xl = gapbarX(lower);
    const standUpAt = (rule, at) => {
      rule.setAttribute("x1", fmt(at, 2));
      rule.setAttribute("x2", fmt(at, 2));
    };
    standUpAt(gapbarLowerRule, xl);
    standUpAt(gapbarRecordRule, xr);
    // A proved n has one bound, not two in the same place: drawing both would put a four-wide
    // black rule on a four-wide black rule and say there were two facts here.
    gapbarLowerRule.setAttribute("opacity", gapbarInfo.proved ? "0" : "1");
    // The scale's reference marks: the three integers the bar spans, and the two values the
    // formulas name. Deduplicated, because at a perfect square `sqrt(n)` IS an integer and
    // `sqrt(n) + 1` is the next one -- drawing both would stack two rules and two numerals in
    // the same place and claim there were two marks there. Rebuilt per n rather than moved,
    // since how many survive the deduplication changes.
    while (gapbarTicks.firstChild) {
      gapbarTicks.removeChild(gapbarTicks.firstChild);
    }
    const marks = [];
    for (const value of [lo, lo + 1, hi, root, root + 1]) {
      if (!marks.some((seen) => seen === value)) {
        marks.push(value);
      }
    }
    marks.sort((a, b) => a - b);
    for (const value of marks) {
      const at = gapbarX(value);
      const tick = document.createElementNS(SVG_NS, "line");
      tick.setAttribute("class", "ref-tick");
      tick.setAttribute("x1", fmt(at, 2));
      tick.setAttribute("x2", fmt(at, 2));
      tick.setAttribute("y1", "-8");
      // A tick reaches its own label. The integers' labels are on the first row and 34 all but
      // touches them; the two irrational marks are a row further down, so theirs run to 70 --
      // otherwise the number floats below a tick that stopped short of it and a reader has to
      // guess which mark it belongs to, which at n = 26 means guessing between 5 and 5.099.
      tick.setAttribute("y2", Number.isInteger(value) ? "34" : "70");
      gapbarTicks.appendChild(tick);
      const num = /** @type {SVGTextElement} */ (document.createElementNS(SVG_NS, "text"));
      num.setAttribute("class", "gapbar-ref-num");
      num.setAttribute("text-anchor", "middle");
      // Two rows, and which row a value is on is decided by what KIND of value it is rather
      // than by whether it happens to collide. The integers are the scale and sit on the first
      // row a unit apart, which at this width is three hundred pixels and never crowds. The two
      // irrational marks sit on the second, under their own formulas -- and they have to,
      // because `sqrt(26)` is 0.099 from the integer 5, about thirty pixels, against labels
      // twice that wide. On one row they overlapped and read as "55.099".
      num.setAttribute("y", Number.isInteger(value) ? "56" : "92");
      num.textContent = barNum(value);
      gapbarTicks.appendChild(num);
      // Placed after it is in the document, because the width it needs is measured.
      const half = num.getComputedTextLength() / 2;
      num.setAttribute("x", fmt(Math.max(half, Math.min(GAPBAR.width - half, at)), 2));
    }
    // The two numbers, in the relations the panel states them with. The record's sits under its
    // tick unless that would put it on top of the lower bound's, in which case it steps aside: the
    // tick is the mark, the numeral only has to be next to it.
    // **The number alone, with no relation glyph.** Two reasons, and the second is why it looked
    // wrong. The arrow under or over each value already says which bound it is, so a relation on
    // top of it is the same fact twice. And the sans face this bar is set in has no `<=` or `>=`:
    // the glyph fell through to the symbols face, which is a serif at a different size, so the two
    // labels came out in two faces and two sizes -- exactly the thing a diagram label must not do.
    gapbarLowerLabel.textContent = gapbarInfo.proved ? "" : barNum(lower);
    gapbarRecordLabel.textContent = barNum(record);
    // Both values share one line above the rail now, so as well as staying inside the bar they
    // have to stay off each other. The width each needs is MEASURED rather than estimated from a
    // figure width -- an estimate was off by a fifth once and clamped `5.12` to `.12`.
    const halfOf = (label) => (label.getComputedTextLength ? label.getComputedTextLength() : 0) / 2;
    const inside = (x, half) => Math.max(half, Math.min(GAPBAR.width - half, x));
    const lowHalf = halfOf(gapbarLowerLabel);
    const recHalf = halfOf(gapbarRecordLabel);
    let lowAt = inside(xl, lowHalf);
    let recAt = inside(xr, recHalf);
    // The lower bound is always the smaller value, so when they crowd it is the left one that
    // gives way: push them apart about their midpoint and re-clamp.
    const need = lowHalf + recHalf + 10;
    if (!gapbarInfo.proved && recAt - lowAt < need) {
      const middle = (lowAt + recAt) / 2;
      lowAt = inside(middle - need / 2, lowHalf);
      recAt = inside(middle + need / 2, recHalf);
    }
    gapbarLowerLabel.setAttribute("x", fmt(lowAt, 2));
    gapbarRecordLabel.setAttribute("x", fmt(recAt, 2));
    // Each formula sits under the value it names, which is now a mark inside the bar rather
    // than one of its ends. Centred by the stylesheet; placed here, because where the mark is
    // depends on n.
    gapbarAreaEnd.style.left = `${fmt(gapbarX(root), 2)}px`;
    gapbarGridEnd.style.left = `${fmt(gapbarX(root + 1), 2)}px`;
    return gapbarInfo;
  }
  function gapbarX(value) {
    const i = gapbarInfo;
    const span = GAPBAR.width - 2 * GAPBAR.inset;
    return GAPBAR.inset + clamp01((value - i.lo) / (i.hi - i.lo)) * span;
  }
  // The triangle over the rail follows the stage's box on every frame, not only the still
  // ones the hand is measured on: the box's growing and shrinking is the thing it shows. Kept
  // inside the bar by its half-width, like the hand.
  function pointAtBox(p) {
    gapbarSetup(p, state.liveN);
    const HALF = 8;
    const x = Math.max(HALF, Math.min(GAPBAR.width - HALF, gapbarX(boxSide)));
    gapbarBox.setAttribute("transform", `translate(${fmt(x, 2)} 0)`);
    gapbarBox.classList.toggle("is-locked", boxLocked);
  }
  function updateGapBar(p, _B, g, mode, assessment, precision) {
    const info = gapbarSetup(p, state.liveN);
    // **`met` is a claim about the n the bar describes.** The centre and angle gaps are measured
    // against the targets of the n the step is heading INTO, so they mean nothing while the bar is
    // describing the previous packing through the dwell -- where the arrangement is that packing's
    // own record, exactly, and the side test is the whole of what can be asked. The same is true of
    // a blind run, which has no correspondence to the record's labelling at all.
    const describesTarget = info.n === p.n + 1;
    const valid = assessment.valid;
    const withinSide = g.side <= info.record * (1 + GAP_MET.side);
    // A hit is a claim about a packing, so only a valid arrangement can make it.
    const met =
      valid &&
      (mode === "blind" || !describesTarget
        ? withinSide
        : g.centre <= GAP_MET.centre && g.angle <= GAP_MET.angle && withinSide);
    // On a hit the hand locks to the record's tick rather than hovering a pixel off it.
    // The hand is a 20-unit triangle centred on the value, so at a record sitting hard against an
    // end -- which is every perfect square, whose record IS the area bound -- half of it hung off
    // the bar. Kept inside by its own half-width: the tick is the mark, the hand only points at it.
    const HALF = 10;
    const x = Math.max(
      HALF,
      Math.min(GAPBAR.width - HALF, met ? gapbarX(info.record) : gapbarX(g.side)),
    );
    // **And the hand is drawn only where the arrangement IS a packing,** under the one validity
    // contract every other part of the workbench uses: unit squares, pair and wall penetration
    // within 1e-9, and the rest of `PACKING_VALIDITY`. A bounding box will happily report a smaller
    // side for squares that are inside each other, or shrunk, so a side is a claim only then. A
    // retained record drawn exactly as stored is assessed at the catalogue's declared stored
    // precision instead, and says so in `precision`: rounding the witness to six places reads as
    // up to 3.9e-6 of penetration on frames that do not overlap.
    const excess = valid ? (g.side / info.record - 1) * 100 : null;
    gapbarHand.setAttribute("x1", fmt(x, 2));
    gapbarHand.setAttribute("x2", fmt(x, 2));
    gapbarHand.setAttribute("opacity", valid ? "1" : "0");
    // The hand turns green on a hit; the head row that said "on the record" beside a tick box is
    // gone, because the bar is always measuring the same thing and a label saying so on every frame
    // was a caption rather than a reading. `excess` survives in the readout below the stage and in
    // `gapBar()`, which is where a number belongs.
    gapbar.classList.toggle("is-met", met);
    gapbarOut.n = info.n;
    gapbarOut.record = info.record;
    gapbarOut.lower = info.lower;
    gapbarOut.lo = info.lo;
    gapbarOut.hi = info.hi;
    gapbarOut.side = g.side;
    gapbarOut.x = x / GAPBAR.width;
    gapbarOut.excess = excess;
    gapbarOut.met = met;
    gapbarOut.valid = valid;
    gapbarOut.reason = assessment.reason;
    gapbarOut.overlap = Math.max(assessment.maxPairOverlap, assessment.maxWallOverlap);
    gapbarOut.tolerance = assessment.tolerance;
    gapbarOut.precision = precision;
  }
  // `still` is true where the picture is not in motion: through the dwell, and from the instant the
  // settle ends. Those are the frames the bar is allowed to move on, along with the ones something
  // has marked dirty (a step boundary, a setting, a pause, a seek, a drop, or `refreshGap()`).
  //
  // **The bar measures the squares the frame shows, and only those.** Through the dwell the arriving
  // square is already in the pose buffers, at its starting pose and drawn at opacity zero, while
  // the bar describes the n before it (`state.liveN`). Counting it put an invisible square inside
  // n's record: the step into 17 read a side of 4.67553 for n = 16, whose record is 4, and called
  // the record itself no packing, which hid the hand through every dwell.
  function updateGap(p, _A, B, mode, still) {
    const shown = Math.min(poseX.length, state.liveN);
    const g = gapOf(poseX, poseY, poseA, shown, paintOut.size);
    if (gapBarDirty || still) {
      const radians = new Float64Array(shown);
      for (let i = 0; i < shown; i++) {
        radians[i] = poseA[i] * DEG;
      }
      const snapshot = packingSnapshot(
        poseX.subarray(0, shown),
        poseY.subarray(0, shown),
        radians,
        paintOut.size,
        { originX: 0, originY: 0, side: paintOut.side },
      );
      const stored = drawsStoredRecord(p, shown);
      const assessment = stored
        ? assessCataloguePrecisionFrame(snapshot, shown)
        : assessPackingSnapshot(snapshot, shown);
      updateGapBar(p, B, g, mode, assessment, stored ? "catalogue-precision" : "packing");
      gapBarDirty = false;
    }
  }
  // Whether the frame draws a retained record as the catalogue stores it: n's poses through the
  // dwell, or n + 1's once the step has landed, each square where the record puts it. Compared to
  // a billionth rather than exactly, since a tween that has landed reaches its target through a
  // rotation that rounds, and angles as a square's, a quarter turn being the same square. A hand's run picked up from the record is still the record until a
  // square moves, and not after.
  function drawsStoredRecord(p, shown) {
    // Within the contract's own tolerance: a frame that close to the stored one is the stored frame,
    // and nothing further from it may be assessed at the catalogue's precision.
    const near = (/** @type {number} */ a, /** @type {number} */ b) =>
      Math.abs(a - b) <= PACKING_VALIDITY.penetrationTolerance;
    for (let i = 0; i < shown; i++) {
      const at =
        shown === p.n ? motion[i]?.a : [tgtX[i] ?? Number.NaN, tgtY[i] ?? Number.NaN, tgtA[i]];
      if (
        at === undefined ||
        !near(poseX[i], at[0]) ||
        !near(poseY[i], at[1]) ||
        !near(angleDelta(at[2] ?? Number.NaN, poseA[i]), 0)
      ) {
        return false;
      }
    }
    return shown === p.n || shown === p.n + 1;
  }
  // Where the two numbers come from at this instant, or the empty string when nothing is simulating.
  function _lawReadout() {
    let pen = null,
      near = null;
    if (state.optimizing && opt !== null) {
      pen = Number.isFinite(opt.pen) ? opt.pen : null;
      near = opt.near;
    } else if (currentTrajectory !== null) {
      const tr = currentTrajectory;
      const u = clamp01(lastMoveU);
      const f = u * tr.steps;
      let s0 = Math.floor(f);
      if (s0 >= tr.steps) {
        s0 = tr.steps;
      }
      pen = tr.pens[s0];
      near = tr.nears[s0];
    }
    // Revision 12: the target graph's own report — how much of it is in contact, out of how much,
    // and the container side the arrangement is in — is written whether or not anything is
    // simulating, because it is a measurement of the picture rather than of a run. The five rows
    // are 28 px on a 694 px panel, which is about fifty characters, so this row is kept inside it.
    if (relKind === "contact") {
      // The honest measure of whether biasing toward a contact graph does anything: how much of
      // the target graph the picture has actually realised.
      const r = relationshipState();
      const parts = [];
      if (pen !== null) {
        parts.push(`overlap ${fmt(pen, 3)}`);
      }
      parts.push(`${r.met} of ${r.edges} contacts`);
      parts.push(`side ${fmt(r.side, 3)}`);
      return parts.join(" · ");
    }
    if (pen === null) {
      return "";
    }
    const tail = !lawAttracts()
      ? "no attraction"
      : near +
        " pair" +
        (near === 1 ? "" : "s") +
        " pulling" +
        (relKind === "groups" ? " inside a block" : ` within ${fmt(LAW.range, 2)}`);
    return `deepest overlap ${fmt(pen, 3)} · ${tail}`;
  }

  // ---------------------------------------------------------------- initial conditions and Optimize (revision 9)
  // The cached simulator above answers one question: what does the step from n - 1 to n look like?
  // Optimize answers a different one: from some arrangement of n squares, how small a box can this
  // physics get them into, given as long as you like? That is an open-ended run, so it cannot be a
  // precomputed span: state advances, in chunks sized to hold the frame budget, until pause.
  //
  // It is a separate stepper rather than a generalisation of `simulate`. `simulate` is a closed
  // precompute whose output is cached, keyed and byte-compared by four checkers; opening it up to
  // continuation would put every one of those measurements at risk for no gain here. The physics is
  // the same physics — the same constants, the same separating-axis push-apart, the same walls, the
  // same seeded jiggle — with one difference in the clock: the optimizer's time unit is one second
  // of simulated time, where `simulate`'s is one move, so `PHYS`'s per-move constants read directly
  // as per-second ones.
  //
  // Bodies are one per square, always. A block is a fact about one step's correspondence, not about
  // an arrangement being shaken open-endedly, and the random and grid starts have none at all. What
  // the style select does reach is the shake: style C's jiggle is twice style B's, as it is in the
  // step animation.
  // ---------------------------------------------------------------- growth (revision 11)
  // Start the squares small and grow them inside a box that is closing at the same time. This is a
  // real method, not a toy: the repository's strategy catalogue lists billiard and inflation, citing
  // Gensane and Ryckelynck, as a record-producing family, and the inflate-and-contract cycle the
  // optimizer already runs is the contraction half of it.
  //
  // Every square carries the same size, a fraction of a unit side. The number to read is not the box
  // the run is holding but **the box it would need at unit size**: the tight box divided by the
  // current size. That is the figure the record compares with, and it is only a claim about a
  // packing when the size has actually reached one with nothing overlapping — which is why the
  // readout names the size beside it every time.
  //
  // Two rules, both stated per simulated second:
  //   constant  the size climbs at the rate whatever the arrangement is doing.
  //   clean     it climbs only while the deepest overlap is inside `OPT.squeezeTol`, the same
  //             tolerance the walls' own squeeze is gated on, so growth and contraction stall
  //             together rather than fighting each other.
  /** @type {AtlasGrowthRule[]} */
  const GROWTH_RULES = ["constant", "clean"];
  /** @type {Pick<AtlasGrowth, "on" | "size" | "rate" | "rule">} */
  const GROWTH_DEFAULT = { on: false, size: 1, rate: 0.05, rule: "constant" };
  /** @type {AtlasGrowth["bounds"]} */
  const GROWTH_BOUNDS = { size: [0.3, 1], rate: [0.005, 0.3] };
  const GROWTH = Object.assign({}, GROWTH_DEFAULT);
  const growKey = () =>
    GROWTH.on ? `${GROWTH.size}:${GROWTH.rate}:${GROWTH.rule}` : `s${GROWTH.size}`;

  // The starting arrangements. `record` is last because it is the least common: you do not
  // usually start from the answer. Its use is diagnostic, and it is the sharpest test of a force
  // law there is -- put a known optimum on the stage, press play, and see whether the law holds
  // it. A law that slides off a packing nobody can beat is telling you about itself, not about
  // the packing. (The two-sided form, which distinguishes a rigid record from one with rattlers,
  // is think-dpmt; this is the button that makes it a thing you can do by hand.)
  /** @type {AtlasInitial[]} */
  const INITIALS = ["previous", "random", "grid", "record"];
  const OPT = {
    stepsPerSecond: 120, // the simulated rate, the same dt the cached simulator integrates at
    budgetMs: 9, // the wall clock one frame's chunk of steps may take
    maxChunk: 400,
    minChunk: 1,
    // The walls close while the packing is not jamming and ease back out when it is, which is the
    // inflate-and-contract cycle revision 7's annealing survey said the side actually responds to.
    squeezeRate: 0.03, // fraction of the side taken per simulated second while nothing overlaps
    relaxRate: 0.03, // and given back while something overlaps by more than jamTol
    // The squeeze runs only while the arrangement is essentially clean and gives room back once it
    // is properly jammed, so the equilibrium the cycle settles at is an overlap of a few
    // thousandths rather than of the tolerance itself. Revision 6's blind run gated on 0.08 and its
    // packings sat at 0.08 for that reason: a squeeze allowed up to a tolerance will use all of it.
    squeezeTol: 0.004,
    jamTol: 0.06,
    minSide: 0.5,
    // The shake anneals down to a floor rather than to nothing: the run never ends, so it must not
    // go dead either.
    tau: 2.0,
    floor: 0.15,
    randomInflate: 1.25, // the random start's box, comfortably larger than the record
    // The deepest overlap an arrangement may have and still be worth recording as the smallest box
    // the run reached. The shake never dies — it anneals to a floor — so with soft contacts the
    // squares keep nudging into each other by a thousandth or two for as long as the run goes, and
    // there is no instant at which the overlap is exactly nothing. Which is why the readout prints
    // the overlap *beside* the box rather than calling the box a packing: a box below the record
    // with an overlap in it is not a record, and the two numbers together say so.
    feasible: 0.008,
  };
  // Two names each: the button's, which has room to say what the start is, and the stage's, which
  // has one 28 px row of the panel and has to leave space for the clock, the step count and the
  // hand-edited mark on the same line.
  const _initialLabel = {
    previous: "previous packing",
    random: "random",
    grid: "ordered fill",
    record: "best known",
  };
  // The run's seed folded into a generator's own base. The multiplier is the odd 32-bit
  // constant from the same family as the LCG's, so successive seeds land far apart rather
  // than in neighbouring streams; at `state.seed === 0` it adds nothing, which is what keeps
  // the default bit-identical to every run recorded before seeds existed.
  const withSeed = (base) => mixUint32Seed(base, state.seed);
  // Build the open-ended Pack adapter's start and optional record target from the retained
  // corpus. The simulation itself is package code and does not know about transition pairs.
  function frameSnapshot(frame, squareSide) {
    return {
      squareSide,
      container: { originX: 0, originY: 0, side: frame.side },
      poses: frame.squares.map((square) => ({
        x: square[0],
        y: square[1],
        angle: square[2] * DEG,
      })),
    };
  }

  function initialArrangement(kind, p, A, B, springs) {
    const N = p.n + 1;
    if (kind === "grid") {
      return { ...createGridPackStart(N), squareSide: GROWTH.size };
    }
    if (kind === "random") {
      return {
        ...createRandomPackStart(N, B.side * OPT.randomInflate, withSeed(N)),
        squareSide: GROWTH.size,
      };
    }
    if (kind === "record") {
      return frameSnapshot(B, GROWTH.size);
    }
    if (!springs) {
      return {
        ...createAppendPackStart(frameSnapshot(A, 1), B.side * BLIND.inflate, {
          gridStep: BLIND.gridStep,
        }),
        squareSide: GROWTH.size,
      };
    }
    const poses = A.squares.map((square) => ({
      x: square[0],
      y: square[1],
      angle: square[2] * DEG,
    }));
    const arriving = B.squares[p.new];
    poses.push({ x: arriving[0], y: arriving[1], angle: arriving[2] * DEG });
    return {
      squareSide: GROWTH.size,
      container: { originX: 0, originY: 0, side: B.side },
      poses,
    };
  }

  function optimizerTargets(p, A, B, springs) {
    if (!springs) {
      return null;
    }
    const targets = [];
    for (let i = 0; i < p.n; i++) {
      const a = A.squares[i];
      const b = B.squares[p.map[i]];
      targets.push({
        x: b[0],
        y: b[1],
        angle: (a[2] + angleDelta(a[2], b[2])) * DEG,
      });
    }
    const arriving = B.squares[p.new];
    targets.push({ x: arriving[0], y: arriving[1], angle: arriving[2] * DEG });
    return targets;
  }

  /** @type {import("./simulation/pack.js").PackRun | null} */
  let opt = null;

  // Target springs only where there is a target: the previous packing with the blind box off.
  function optSprings(kind) {
    return kind === "previous" && !state.blind;
  }

  function newOptimizer(kind, startOverride) {
    const p = PAIRS[state.pair];
    const A = FRAMES[String(p.n)];
    const B = FRAMES[String(p.n + 1)];
    const N = p.n + 1;
    const springs = optSprings(kind);
    const start =
      startOverride === undefined
        ? initialArrangement(kind, p, A, B, springs)
        : packingSnapshot(startOverride.X, startOverride.Y, startOverride.TH, GROWTH.size, {
            originX: 0,
            originY: 0,
            side: startOverride.side,
          });
    return createPackRun({
      n: N,
      seed: state.seed,
      effectiveSeed: withSeed(N + INITIALS.indexOf(kind) * 7919),
      startKind: kind,
      start,
      targets: optimizerTargets(p, A, B, springs),
      reference: { pairIndex: state.pair, recordSide: B.side },
      pairLaw: LAW,
      wallLaw: WALLLAW,
      relatedMask: maskFor(state.pair),
      physics: {
        stepsPerSecond: OPT.stepsPerSecond,
        omega: PHYS.omega,
        zeta: PHYS.zeta,
        contactDamping: PHYS.contactDamping,
        contactTorque: PHYS.contactTorque,
        jiggle: state.style === "bodies" ? BODIES.jiggle : PHYS.jiggle,
        jiggleTorque: state.style === "bodies" ? BODIES.jiggleTorque : PHYS.jiggleTorque,
        jiggleHz: [PHYS.jiggleHz[0], PHYS.jiggleHz[1]],
        maxSpeed: PHYS.maxSpeed,
        maxSpin: PHYS.maxSpin,
        cell: PHYS.cell,
      },
      anneal: {
        amplitude: ANNEAL.amplitude(state.anneal),
        decayPower: ANNEAL.decayPower(state.anneal),
        tau: OPT.tau,
        floor: OPT.floor,
      },
      growth: { on: GROWTH.on, rate: GROWTH.rate, rule: GROWTH.rule },
      container: {
        squeezeRate: OPT.squeezeRate,
        relaxRate: OPT.relaxRate,
        squeezeTolerance: OPT.squeezeTol,
        jamTolerance: OPT.jamTol,
        minimumSide: OPT.minSide,
      },
      stationarity: {
        linearSpeed: 0,
        angularSpeed: 0,
        forcingScale: 0,
        window: 1,
        stop: false,
      },
    });
  }

  function measureOptimizer(o) {
    return measurePackRun(o).requiredSide;
  }

  function optAdvance(o, steps) {
    const rigidStyle = state.style === "bodies";
    updatePackRun(o, {
      pairLaw: LAW,
      wallLaw: WALLLAW,
      relatedMask: maskFor(state.pair),
      physics: {
        jiggle: rigidStyle ? BODIES.jiggle : PHYS.jiggle,
        jiggleTorque: rigidStyle ? BODIES.jiggleTorque : PHYS.jiggleTorque,
      },
      anneal: {
        amplitude: ANNEAL.amplitude(state.anneal),
        decayPower: ANNEAL.decayPower(state.anneal),
      },
      growth: { on: GROWTH.on, rate: GROWTH.rate, rule: GROWTH.rule },
    });
    advancePackRun(o, steps);
  }

  // One frame of the open-ended run: as many fixed steps as the wall clock asked for, capped so a
  // chunk holds the frame budget. The state after k steps is exact and repeatable; how many steps a
  // second of wall clock buys is not, and that is the whole difference between this and `seek`.
  //: The cost of a step, in milliseconds, assumed before any step has been timed, so the first chunk
  //: is a finite number of steps; a wall-clock floor, unrelated to validity.
  const MIN_MS_PER_STEP = 1e-4;
  function optimizeAdvance(dtSim) {
    const o = opt;
    if (o === null) {
      return;
    }
    const cap = Math.max(
      OPT.minChunk,
      Math.min(OPT.maxChunk, Math.round(OPT.budgetMs / Math.max(o.msPerStep, MIN_MS_PER_STEP))),
    );
    const want = Math.max(OPT.minChunk, Math.min(cap, Math.round(dtSim * OPT.stepsPerSecond)));
    const t0 = performance.now();
    optAdvance(o, want);
    const ms = performance.now() - t0;
    o.msPerStep = o.msPerStep * 0.7 + (ms / want) * 0.3;
    render();
  }

  // The chooser, the run, and what it is doing.
  // One rule: the previous packing *is* the timeline's own start, so choosing it shows the step
  // animation again; a random or grid start has nothing to do with the step, so it is put on the
  // stage at once, paused, and Optimize is what sets it going. Optimize runs from whichever of the
  // three is chosen, the previous packing included.
  function setInitial(kind) {
    const next = INITIALS.includes(kind) ? kind : INITIALS[0];
    state.initial = next;
    pause();
    if (next === "previous") {
      state.optimizing = false;
      opt = null;
      // Revision 13: below full size the previous packing is staged as an arrangement rather than
      // as the timeline, so that the chosen size is on the stage the moment the start is chosen —
      // the same rule `setGrowth` applies from the other side.
      stagePack();
    } else {
      state.optimizing = true;
      opt = newOptimizer(next);
    }
    markGapBar();
    updateSegments();
    render();
    return state.initial;
  }
  function optimize(on) {
    if (on === false) {
      pause();
      state.optimizing = false;
      opt = null;
      // Pack always has its n squares on the stage, so stopping a run there goes back to the
      // starting arrangement rather than to the step animation underneath it.
      stagePack();
      markGapBar();
      updateSegments();
      render();
      return optimizeState();
    }
    pause();
    state.optimizing = true;
    opt = newOptimizer(state.initial);
    markGapBar();
    updateSegments();
    render();
    play();
    return optimizeState();
  }
  // For measurement and for tests: advance the run by an exact number of steps, with no clock in it.
  function optimizeStep(steps) {
    if (opt === null) {
      return optimizeState();
    }
    optAdvance(opt, Math.max(1, Math.round(Number(steps) || 1)));
    render();
    return optimizeState();
  }
  // ---------------------------------------------------------------- the hand (revision 9)
  // Press picks the topmost square under the cursor, drag moves it, shift rotates it about its own
  // centre, release drops it. While it is held it is pinned: the run writes the cursor's pose into
  // it every step and gives it no force at all, so its neighbours are pushed aside by it instead of
  // it being pushed aside by them. On release it rejoins with zero velocity.
  //
  // A drag needs a live simulation to push anything, so grabbing a square while the timeline is
  // playing or scrubbing hands the picture to an open-ended run seeded from the poses on the stage —
  // no jump, and the run carries on from there. A run that has been touched is no longer a function
  // of its seed, so it is marked, and the mark is on the stage: `hand-edited`.
  function seedOptimizerFromScene() {
    const p = PAIRS[state.pair];
    const N = p.n + 1;
    const X = new Float64Array(N),
      Y = new Float64Array(N),
      TH = new Float64Array(N);
    for (let i = 0; i < N; i++) {
      X[i] = poseX[i];
      Y[i] = poseY[i];
      TH[i] = poseA[i] * DEG;
    }
    const side = sceneSide > 0 ? sceneSide : FRAMES[String(p.n + 1)].side;
    return newOptimizer(state.initial, { X, Y, TH, side });
  }
  // The topmost square whose own frame contains the world point, or -1. Drawing order is birth
  // order, so the last match is the one on top.
  function pickAt(wx, wy) {
    if (poseX === null) {
      return -1;
    }
    let found = -1;
    for (let i = 0; i < poseX.length; i++) {
      const c = Math.cos(poseA[i] * DEG),
        sn = Math.sin(poseA[i] * DEG);
      const dx = wx - poseX[i],
        dy = wy - poseY[i];
      const u = dx * c + dy * sn,
        v = -dx * sn + dy * c;
      const h = (opt === null ? 1 : opt.size) / 2;
      if (Math.abs(u) <= h && Math.abs(v) <= h) {
        found = i;
      }
    }
    return found;
  }
  let grabOffX = 0,
    grabOffY = 0,
    grabAngle = 0,
    grabTH = 0,
    grabRotating = false;
  function grab(index, wx, wy) {
    const i = Math.round(Number(index));
    if (!Number.isFinite(i) || i < 0 || poseX === null || i >= poseX.length) {
      return -1;
    }
    if (!(state.optimizing && opt !== null)) {
      const was = state.playing;
      pause();
      state.optimizing = true;
      opt = seedOptimizerFromScene();
      if (was) {
        play();
      }
    }
    const o = opt;
    o.held = i;
    o.edited = true;
    o.heldX = o.X[i];
    o.heldY = o.Y[i];
    o.heldTH = o.TH[i];
    const px = wx === undefined ? o.X[i] : Number(wx);
    const py = wy === undefined ? o.Y[i] : Number(wy);
    grabOffX = px - o.X[i];
    grabOffY = py - o.Y[i];
    grabAngle = Math.atan2(py - o.Y[i], px - o.X[i]);
    grabTH = o.TH[i];
    grabRotating = false;
    // A new hold takes its own view, whatever an earlier hold that never let go left behind.
    heldView = null;
    updateSegments();
    render();
    return i;
  }
  // Where the cursor is now. `rotating` swaps translation for a turn about the square's own centre,
  // re-anchored the moment the modifier changes so the square never jumps as shift goes down.
  function dragTo(wx, wy, rotating) {
    const o = opt;
    if (o === null || o.held < 0) {
      return null;
    }
    const i = o.held;
    const px = Number(wx),
      py = Number(wy);
    if (!Number.isFinite(px) || !Number.isFinite(py)) {
      return null;
    }
    const turning = !!rotating;
    if (turning !== grabRotating) {
      grabRotating = turning;
      grabOffX = px - o.X[i];
      grabOffY = py - o.Y[i];
      grabAngle = Math.atan2(py - o.Y[i], px - o.X[i]);
      grabTH = o.TH[i];
    }
    if (turning) {
      o.heldTH = grabTH + (Math.atan2(py - o.Y[i], px - o.X[i]) - grabAngle);
    } else {
      o.heldX = px - grabOffX;
      o.heldY = py - grabOffY;
    }
    // Written straight into the arrangement as well as held for the next step, so a drag with the
    // run paused still moves the square and still moves the readout under it.
    o.X[i] = o.heldX;
    o.Y[i] = o.heldY;
    o.TH[i] = o.heldTH;
    o.VX[i] = 0;
    o.VY[i] = 0;
    o.W[i] = 0;
    measureOptimizer(o);
    render();
    return { index: i, x: o.X[i], y: o.Y[i], angle: o.TH[i] / DEG };
  }
  function release() {
    if (opt === null || opt.held < 0) {
      return -1;
    }
    const i = opt.held;
    opt.held = -1;
    // The drop is a settled moment: the bar is allowed to move again.
    markGapBar();
    render();
    return i;
  }
  function adjustSquareFromKeyboard(index, command) {
    if (poseX === null || poseY === null || poseA === null) {
      return;
    }
    const x = poseX[index],
      y = poseY[index];
    if (x === undefined || y === undefined || grab(index, x, y) < 0 || opt === null) {
      return;
    }
    keyboardSquare = index;
    if (command.kind === "move-square") {
      dragTo(x + command.dx, y + command.dy, false);
    } else if (command.kind === "rotate-square") {
      opt.heldTH = opt.TH[index] + command.degrees * DEG;
      opt.TH[index] = opt.heldTH;
      opt.W[index] = 0;
      measureOptimizer(opt);
    }
    release();
  }
  function hand() {
    return {
      held: opt === null ? -1 : opt.held,
      edited: opt?.edited,
      rotating: grabRotating,
    };
  }
  function optimizeState() {
    if (opt === null) {
      return { on: false, initial: state.initial, edited: false };
    }
    const bestPacking =
      opt.bestPacking === null
        ? null
        : {
            seed: opt.seed,
            at: opt.bestPacking.at,
            required: opt.bestPacking.requiredSide,
            squareSide: opt.bestPacking.squareSide,
            container: { ...opt.bestPacking.container },
            poses: opt.bestPacking.poses.map(
              (pose) =>
                /** @type {[number, number, number]} */ ([pose.x, pose.y, pose.angle / DEG]),
            ),
            maxPairOverlap: opt.bestPacking.maxPairOverlap,
            maxWallOverlap: opt.bestPacking.maxWallOverlap,
          };
    return {
      on: state.optimizing,
      running: state.playing,
      initial: /** @type {AtlasInitial} */ (opt.kind),
      springs: opt.springs,
      seed: opt.seed,
      n: opt.n,
      ...(opt.pair === null ? {} : { pair: opt.pair }),
      time: opt.time,
      steps: opt.steps,
      side: opt.side,
      required: opt.required,
      size: opt.size,
      best: opt.best === Infinity ? null : opt.best,
      bestAt: opt.bestAt,
      bestPenetration: opt.best === Infinity ? null : opt.bestPen,
      bestWallPenetration: opt.best === Infinity ? null : opt.bestWallPen,
      bestPacking,
      feasible: OPT.feasible,
      // The excess over the record is a claim about a packing, so it is reported only for one.
      ...(opt.record === null
        ? {}
        : {
            record: opt.record,
            excess: opt.packingValid ? (opt.required / opt.record - 1) * 100 : null,
          }),
      penetration: Number.isFinite(opt.pen) ? opt.pen : null,
      exactPenetration: Number.isFinite(opt.exactPen) ? opt.exactPen : null,
      wallPenetration: Number.isFinite(opt.wallPen) ? opt.wallPen : null,
      packing: opt.packingValid,
      invalidReason: opt.invalidReason,
      near: opt.near,
      edited: opt.edited,
      held: opt.held,
      msPerStep: opt.msPerStep,
    };
  }

  // ---------------------------------------------------------- the graph on the stage (revision 12)
  // Two different pictures share one group of lines, and they answer two different questions.
  //
  //   **The target contact graph**, whenever a contact relationship is in force, and *without*
  //   needing the correspondence overlay: it is what the run is being asked to realise, so it is
  //   drawn whenever it is doing anything. Every edge of it is drawn, and the two classes are drawn
  //   differently, because the difference is the measurement: an edge whose two squares share a
  //   whole side right now is a solid white line lying across the pair, and one that is only wanted
  //   is a dashed dark line, usually long, crossing paper. The count in the readout is exactly the
  //   number of solid ones.
  //
  //   **The blocks' cliques** under the groups relationship, which is revision 11's picture and
  //   keeps revision 11's rule: it rides the correspondence overlay, and it draws only the pairs
  //   the attraction is actually reaching, because a completely connected block is thousands of
  //   pairs and drawing them all would say every one of them was doing something.
  //
  // A general relationship draws nothing, there being no mask to show. Drawing mode draws whatever
  // has been drawn so far even where the relationship is not reading it, because a drawing you
  // cannot see is not a drawing.
  const maskLines = [];
  function stageGraph() {
    if (relKind === "contact") {
      return { edges: targetGraphFor(state.pair), classed: true, reach: false };
    }
    if (state.drawing) {
      const flat = drawnFor(state.pair);
      return flat.length ? { edges: flat, classed: true, reach: false } : null;
    }
    if (state.links && relKind === "groups") {
      return { edges: relationshipFor(state.pair).edges, classed: false, reach: true };
    }
    return null;
  }
  function drawMaskLinks(N) {
    const want = stageGraph();
    maskGroup.style.display = want === null ? "none" : "";
    // The lines are pooled and reused, so hiding the group is not enough: a line left over from the
    // last graph would still read as drawn to anything counting them off the DOM.
    if (want === null) {
      for (let k = 0; k < maskLines.length; k++) {
        maskLines[k].style.display = "none";
      }
      return;
    }
    const edges = want.edges;
    const reach = 1.41422 * (opt === null ? 1 : opt.size) + (lawAttracts() ? LAW.range : 0);
    let drawn = 0;
    for (let e = 0; e + 1 < edges.length; e += 2) {
      const a = edges[e],
        b = edges[e + 1];
      if (a >= N || b >= N) {
        continue;
      }
      const dx = poseX[b] - poseX[a],
        dy = poseY[b] - poseY[a];
      if (want.reach && dx * dx + dy * dy >= reach * reach) {
        continue;
      }
      let line = maskLines[drawn];
      if (line === undefined) {
        line = el("line", { "stroke-linecap": "round", "vector-effect": "non-scaling-stroke" });
        maskGroup.appendChild(line);
        maskLines.push(line);
      }
      line.setAttribute("x1", poseX[a]);
      line.setAttribute("y1", poseY[a]);
      line.setAttribute("x2", poseX[b]);
      line.setAttribute("y2", poseY[b]);
      line.setAttribute(
        "class",
        !want.classed ? "" : paintTouching.has(a < b ? a * N + b : b * N + a) ? "met" : "unmet",
      );
      line.style.display = "";
      drawn++;
    }
    for (let k = drawn; k < maskLines.length; k++) {
      maskLines[k].style.display = "none";
    }
    maskGroup.setAttribute("opacity", "1");
  }

  // ------------------------------------------------- drawing an edge with the pointer (revision 12)
  // Press on a square, release on another, and the edge between them is added; the same gesture
  // where the edge already exists takes it away. The pending edge follows the cursor so the gesture
  // says what it is doing while it is being made.
  //
  // It is behind the `draw links` toggle rather than beside the square drag, because both gestures
  // are press-drag-release on the same square: with the toggle off a press picks a square up, as it
  // always has; with it on, no square is ever picked up. Nothing about the drag code changes, and
  // `hand()` still reports what it always did.
  let linkFrom = -1;
  function linkStart(index) {
    const i = Math.round(Number(index));
    if (!Number.isFinite(i) || i < 0 || poseX === null || i >= poseX.length) {
      return -1;
    }
    linkFrom = i;
    drawLine.setAttribute("x1", poseX[i]);
    drawLine.setAttribute("y1", poseY[i]);
    drawLine.setAttribute("x2", poseX[i]);
    drawLine.setAttribute("y2", poseY[i]);
    drawLine.style.display = "";
    return i;
  }
  function linkMove(wx, wy) {
    if (linkFrom < 0) {
      return null;
    }
    const x = Number(wx),
      y = Number(wy);
    if (!Number.isFinite(x) || !Number.isFinite(y)) {
      return null;
    }
    drawLine.setAttribute("x2", String(x));
    drawLine.setAttribute("y2", String(y));
    return { from: linkFrom, x, y };
  }
  function linkCancel() {
    linkFrom = -1;
    drawLine.style.display = "none";
  }
  // The release. `index` is the square under the cursor, or -1 for empty paper, which cancels.
  function linkEnd(index) {
    const from = linkFrom;
    linkCancel();
    const to = Math.round(Number(index));
    if (from < 0 || !Number.isFinite(to) || to < 0 || to === from) {
      return { added: false, edges: drawnEdges() };
    }
    const added = toggleEdge(from, to);
    return { added, from, to, edges: drawnEdges() };
  }
  function setDrawing(on) {
    state.drawing = !!on;
    linkCancel();
    // Turning drawing on points the target at the drawn graph. Otherwise the edges would go into a
    // store nothing reads, and the first drag would appear to do nothing at all.
    if (state.drawing) {
      targetSource = "drawn";
      targetEdges = null;
    }
    document.body.classList.toggle("drawing", state.drawing);
    graphChanged();
    return state.drawing;
  }

  // ---------------------------------------------------------------- the painter (revision 11)
  // Every scene writes its poses into poseX / poseY / poseA and then calls this. The fill of a
  // square is a function of the angle it is drawn at and of how many of its sides lie whole against
  // a neighbour or a wall on the stage, and of nothing else — not of which frame it belongs to, not
  // of what else the frame holds, and not of a setting. `drain` is revision 6's desaturation;
  // `tint` is how far the arriving square still leans toward scarlet, which is the one square whose
  // colour this map does not have the last word on.
  const paintEdges = []; // the frame's own contact graph, as index pairs
  /** @type {ReadonlySet<number>} */
  let paintTouching = new Set(); // the same, as i * N + j keys, for the relationship's evidence
  const paintOut = {
    classes: 0,
    centres: [],
    sizes: [],
    slots: [],
    contacts: [],
    /** @type {AtlasPaintScheme} */
    scheme: "identity",
    // The frame's own answer to "is this a packing": the summed penetration in unit sides, the
    // deepest single one, and how many pairs are inside each other. Zero on a valid packing.
    overlap: 0,
    deepestOverlap: 0,
    overlapPairs: 0,
    // The container side and square size the frame was measured at, so a later measurement of
    // part of the frame uses the same geometry.
    side: 0,
    size: 1,
  };
  function paintSquares(p, side, drain, tint, size, resting, homeward) {
    const N = poseA.length;
    const geometry = measureFrameGeometry(poseX, poseY, poseA, side, size ?? 1, {
      gap: CONTACT.gap,
      angleToleranceDegrees: ANGLE_TOL,
    });
    paintEdges.splice(0, paintEdges.length, ...geometry.contactEdges);
    if (standardizing() && clamp01(Number(resting) || 0) < 1) {
      if (state.optimizing && opt !== null) {
        assignRunGroups(N, state.t);
      } else {
        assignGroups(N, state.t);
      }
    }
    /** @type {import("./view/scene-types.js").SceneFrame} */
    const scene = {
      pairIndex: state.pair,
      n: N,
      containerSide: side,
      viewBox: { x: 0, y: 0, size: side },
      squares: Array.from({ length: N }, (_, index) => ({
        index,
        identity: index < motion.length ? motion[index].ident : p.n + 1,
        x: poseX[index],
        y: poseY[index],
        angleDegrees: poseA[index],
        opacity: 1,
        scale: size ?? 1,
      })),
      presentation: {
        drain,
        newTint: tint,
        resting: clamp01(Number(resting) || 0),
        homeward,
        mark: null,
        linksOpacity: 0,
        ghostOpacity: 0,
      },
      motion:
        state.mode === "pack"
          ? "packing-snapshot"
          : state.style === "tween"
            ? "direct-illustration"
            : "physical-illustration",
    };
    const painted = COLOUR.paintScene(scene, geometry, {
      scheme: colorScheme,
      mode: state.mode,
      animateStandardize: ANIMATE.standardize,
      stageChroma,
      desaturationFloor: desatFloor,
      scarlet: SCARLET,
      tintChroma: TINT_CHROMA,
      restSource,
      restTarget,
      holdsColour,
      movingSlots: groupSlot,
    });
    paintTouching = painted.touching;
    paintOut.side = side;
    paintOut.size = size ?? 1;
    drawMaskLinks(N);
    for (let i = 0; i < motion.length; i++) {
      motion[i].rect.setAttribute("fill", painted.fills[i]);
    }
    newRect.setAttribute("fill", painted.fills[p.n]);
    paintOut.overlap = painted.overlap;
    paintOut.deepestOverlap = painted.deepestOverlap;
    paintOut.overlapPairs = painted.overlapPairs;
    paintOut.scheme = painted.scheme;
    paintOut.classes = painted.classes;
    paintOut.centres = painted.centres;
    paintOut.sizes = painted.sizes;
    paintOut.slots = painted.slots;
    paintOut.contacts = painted.contacts;
    return painted;
  }
  // What the painter last did, for the checkers: how many angle classes the frame held, where their
  // centres are, which palette slot each took, and the contact count of every square drawn.
  function colourState() {
    return {
      overlap: paintOut.overlap,
      deepestOverlap: paintOut.deepestOverlap,
      overlapPairs: paintOut.overlapPairs,
      // Revision 12: which scheme is chosen, and which one this frame was actually painted in —
      // they differ only where Animate's standardising has repainted a resting frame.
      scheme: colorScheme,
      painted: paintOut.scheme,
      schemes: COLOR_SCHEMES.slice(),
      greens: GREENS.slice(),
      greenStride: GREEN_STRIDE,
      animateStandardize: ANIMATE.standardize,
      classes: paintOut.classes,
      centres: paintOut.centres.slice(),
      sizes: paintOut.sizes.slice(),
      slots: paintOut.slots.slice(),
      contacts: paintOut.contacts.slice(),
      tolerance: ANGLE_TOL,
      contactGap: CONTACT.gap,
      palette: PALETTE.slice(),
      shades: SHADES.map((f) => f.slice()),
      fills: /** @type {SVGGElement[]} */ (
        Array.from(document.querySelectorAll("#squares g[data-identity]"))
      )
        .filter((g) => g.style.display !== "none")
        .map((g) => g.firstElementChild.getAttribute("fill")),
    };
  }

  // What an open-ended run looks like on the stage: the squares where the run has them, the box the
  // walls are at, and the view sized to hold whichever of the box and the record is wider so the
  // picture does not breathe as the walls close. The fills are the pair's own, drained while the run
  // is going and locked back in on pause, as they are for the step animation.
  //: The view a held square is dragged in, taken when it is picked up; null while nothing is held.
  /** @type {{x: number, y: number, size: number} | null} */
  let heldView = null;
  function renderOptimizeScene(p, _A, B) {
    const o = opt;
    const side = o.side;
    // The view covers the walls and the squares both, so a square let go outside the box stays on
    // the stage instead of vanishing off the edge of it.
    const lox = Math.min(0, o.bx0),
      hix = Math.max(side, o.bx1);
    const loy = Math.min(0, o.by0),
      hiy = Math.max(side, o.by1);
    const span = Math.max(hix - lox, hiy - loy, B.side);
    const size = span * (1 + 2 * PAD);
    const midX = (lox + hix) / 2,
      midY = (loy + hiy) / 2;
    let view = { x: midX - size / 2, y: -midY - size / 2, size };
    // **While a square is held, the view holds still** (#125 F6). Re-fitted on every frame, it moved
    // under the cursor: the pointer is mapped through the view just drawn, a square past a wall
    // widens that view, the same pixel then maps further out, and the square ran away from the
    // hand -- a 65 px drag took it from x 4.5 to 29, and ten one-pixel jiggles to 124. So the view is
    // taken when the square is picked up and kept until it is let go, when it catches up.
    if (o.held >= 0) {
      heldView ??= view;
      view = heldView;
    } else {
      heldView = null;
    }
    svg.setAttribute("viewBox", `${view.x} ${view.y} ${view.size} ${view.size}`);
    containerRect.setAttribute("width", String(side));
    containerRect.setAttribute("height", String(side));
    sceneSide = side;
    const drain = state.desaturate && state.playing ? 1 : 0;
    // Revision 11: the squares carry the run's own size, which is one unless growth is on. It is a
    // scale on the drawn rect, so the pose the readout measures and the picture on the stage are
    // the same numbers at any size.
    const grow = o.size === 1 ? "" : ` scale(${o.size})`;
    for (let i = 0; i < motion.length; i++) {
      const m = motion[i];
      const ang = o.TH[i] / DEG;
      poseX[i] = o.X[i];
      poseY[i] = o.Y[i];
      poseA[i] = ang;
      m.node.setAttribute("transform", `translate(${o.X[i]} ${o.Y[i]}) rotate(${ang})${grow}`);
    }
    const ang = o.TH[p.n] / DEG;
    poseX[p.n] = o.X[p.n];
    poseY[p.n] = o.Y[p.n];
    poseA[p.n] = ang;
    newNode.setAttribute("opacity", 1);
    newNode.setAttribute("transform", `translate(${o.X[p.n]} ${o.Y[p.n]}) rotate(${ang})${grow}`);
    // An open-ended run is at rest exactly when it is not playing; Animate's standardising does not
    // reach it anyway, an optimisation being Pack's own playback.
    paintSquares(p, side, drain, 0, o.size, state.playing ? 0 : 1, true);
    mark.setAttribute("opacity", "0");
    linksGroup.setAttribute("opacity", "0");
    ghost.setAttribute("opacity", "0");
  }

  // Styles B and C. The world-to-stage scale is held at n's through the move, so the container
  // visibly grows and no square changes size (the picture shrinks only where n + 1's container
  // would not fit at that scale, which happens on the tiny pairs); over the settle the whole
  // picture eases down to n + 1's fit. The new square inflates in place from the start of the
  // move, tinted scarlet as in A. Every square is the pool's element for its identity.
  // The simulation's own progress at wall-clock `t`. Piecewise linear with its knee at
  // `PHYS.tightenFrom`, which is where the landing begins: the reader spends `move` seconds on
  // the run's first 68 per cent and `correct` seconds on its last 32, so the two phases have
  // independent durations while the run they play is the same one. Lengthening the search no
  // longer lengthens the landing with it, which was the whole complaint.
  // The run waits out the box's BOX_FIRST of the move, like every other motion on a step.
  function moveProgress(sc, t) {
    const tm = timing();
    const start = sc.moveStart + (sc.moveEnd - sc.moveStart) * BOX_FIRST;
    const span = sc.moveEnd - start;
    const total = tm.move + tm.correct;
    if (span <= 0 || total <= 0) {
      return ramp(t, start, sc.moveEnd);
    }
    const knee = start + span * (tm.move / total);
    return t < knee
      ? ramp(t, start, knee) * PHYS.tightenFrom
      : PHYS.tightenFrom + ramp(t, knee, sc.moveEnd) * (1 - PHYS.tightenFrom);
  }
  // Where the physical styles put every square at `t`, written into the three pose buffers, and
  // the container around them. The stage draws this answer and the moving palette's checkpoints
  // read it, so a run's colours are measured on the same poses the stage shows.
  function physicsFrame(p, A, B, sc, t, xs, ys, as) {
    const u = moveProgress(sc, t);
    const moving = u > 0 && u < 1;
    // With the snap off the simulation's own final state is what the pair comes to rest at, so the
    // trajectory is read through the settle as well, not only while the squares are on the move.
    const mode = simMode();
    const blind = mode === "blind";
    const tr =
      moving || (mode !== "snap" && u > 0) ? ensureTrajectory(state.pair, state.style, mode) : null;
    // A blind run opens its container before it begins: over the first BLIND.open of the move the
    // picture eases from the record of n to the run's own first state, the box inflated and the
    // packing recentred inside it. After that the move is the simulation's own clock.
    const oe = blind ? easeInOut(clamp01(u / BLIND.open)) : 1;
    const su = blind ? clamp01((u - BLIND.open) / (1 - BLIND.open)) : Math.min(u, 1);
    let side, fit;
    if (blind && tr !== null) {
      side = oe < 1 ? lerp(A.side, tr.sides[0], oe) : sampleSide(tr, su);
      fit = Math.max(B.side, tr.miss.side);
    } else {
      side = u >= 1 ? B.side : containerSide(A.side, B.side, u);
      fit = B.side;
    }
    for (let i = 0; i < motion.length; i++) {
      const m = motion[i];
      let x, y, ang;
      if (u <= 0) {
        x = m.a[0];
        y = m.a[1];
        ang = m.a[2];
      } else if (tr === null) {
        x = m.b[0];
        y = m.b[1];
        ang = m.b[2];
      } else if (blind && oe < 1) {
        const pose = samplePose(tr, 0, i);
        x = lerp(m.a[0], pose[0], oe);
        y = lerp(m.a[1], pose[1], oe);
        ang = lerp(m.a[2], pose[2], oe);
      } else {
        const pose = samplePose(tr, su, i);
        x = pose[0];
        y = pose[1];
        ang = pose[2];
      }
      xs[i] = x;
      ys[i] = y;
      as[i] = ang;
    }
    // The new square, identity n + 1: it fades and inflates in over the first part of the move
    // where the simulation puts it.
    const nb = newPose;
    const appear = u <= 0 ? 0 : easeOut(clamp01(su / PHYS.appear));
    let scale = 1;
    if (appear > 0 && tr !== null) {
      const pose = samplePose(tr, su, p.n);
      xs[p.n] = pose[0];
      ys[p.n] = pose[1];
      as[p.n] = pose[2];
      scale = lerp(PHYS.inflateFrom, 1, clamp01(su / PHYS.appear));
    } else {
      xs[p.n] = nb[0];
      ys[p.n] = nb[1];
      as[p.n] = nb[2];
    }
    return { u, moving, blind, tr, su, side, fit, appear, scale };
  }
  function renderPhysicsScene(p, A, B, _tm, sc, t) {
    const { u, moving, blind, tr, su, side, fit, appear, scale } = physicsFrame(
      p,
      A,
      B,
      sc,
      t,
      poseX,
      poseY,
      poseA,
    );
    const settled = easeOut(ramp(t, sc.moveEnd, sc.end));
    const e = easeInOut(u);
    // The held view has to cover the widest the container ever gets, which for a blind run is its
    // inflated start; that is a pure function of the record, so the view never jumps when the
    // trajectory arrives.
    const widest = blind ? B.side * BLIND.inflate : side;
    const held = Math.max(A.side * (1 + 2 * PAD), widest * (1 + 2 * PAD_MIN));
    const refit = easeInOut(ramp(t, sc.moveEnd, sc.end));
    const view = u < 1 ? held : lerp(held, fit * (1 + 2 * PAD), refit);
    svg.setAttribute("viewBox", `${side / 2 - view / 2} ${-side / 2 - view / 2} ${view} ${view}`);
    containerRect.setAttribute("width", String(side));
    containerRect.setAttribute("height", String(side));
    sceneSide = side;

    currentTrajectory = tr;
    lastMoveU = su;
    const drain = desatLevel(sc, t);
    for (let i = 0; i < motion.length; i++) {
      motion[i].node.setAttribute(
        "transform",
        `translate(${poseX[i]} ${poseY[i]}) rotate(${poseA[i]})`,
      );
    }
    // The new square's fill leans toward scarlet until the settle ends.
    const [x, y, ang] = [poseX[p.n], poseY[p.n], poseA[p.n]];
    if (appear > 0) {
      newNode.setAttribute("opacity", appear);
      newNode.setAttribute("transform", `translate(${x} ${y}) rotate(${ang}) scale(${scale})`);
    } else {
      newNode.setAttribute("opacity", 0);
      newNode.setAttribute("transform", `translate(${x} ${y}) rotate(${ang})`);
    }
    // At rest through the dwell and from the instant the settle ends, which are the two frames a
    // Animate leaves a viewer looking at.
    paintSquares(
      p,
      side,
      drain,
      appear > 0 ? TINT * (1 - settled) : 0,
      undefined,
      hueLevel(sc, t),
      t >= sc.moveEnd,
    );
    mark.setAttribute("opacity", "0");
    if (state.links) {
      linksGroup.setAttribute("opacity", String(u <= 0 ? 0.35 : 1 - e));
      ghost.setAttribute("opacity", String(moving ? 1 - e : 0));
    }
  }

  function render() {
    if (searchPanel?.visible()) {
      searchPanel.redraw();
      return;
    }
    if (packPanel?.visible()) {
      packPanel.redraw();
      return;
    }
    if (animationPanel?.state().active) {
      animationPanel.redraw();
      return;
    }
    const p = PAIRS[state.pair];
    const A = FRAMES[String(p.n)];
    const B = FRAMES[String(p.n + 1)];
    const tm = timing();
    const sc = schedule();
    const t = state.t;
    const mode = simMode();
    const optimizing = state.optimizing && opt !== null;
    // **Which n the stage is showing, decided before anything reads it.** The panel rolls from n to
    // n + 1 half way through the roll, and the bar has to be keyed to the same answer -- it is the
    // n whose packing is on the stage, and a bar keyed to the other one measures a true number
    // against the wrong record. It used to be assigned in the roll block below, which runs AFTER
    // `updateGap`, so the bar read the previous frame's answer and lagged a step behind the panel.
    state.liveN = rollingN(p, sc, t, optimizing);
    if (optimizing) {
      renderOptimizeScene(p, A, B);
    }
    // **A static append is never simulated, whatever the style says.** On a prefix or
    // shared-picture step every existing square's target IS where it already stands, so there is
    // nothing for a simulation to find -- but handing it to one anyway gives the jiggle a
    // rearrangement's worth of energy and no rearrangement to spend it on, and the packing is
    // thrown. Measured, worst distance a square reached from where it ends up, in unit sides:
    // n = 324 went 2.46, n = 100 2.26, n = 16 1.31, against 0.04 to 0.10 for the same steps drawn
    // by the tween. The short move these steps were given so the new square can be seen arriving
    // is what exposed it -- 0.4 s of move is a compressed clock for the same shake.
    else if (isPhysical(state.style) && !isStillPair()) {
      renderPhysicsScene(p, A, B, tm, sc, t);
    } else {
      renderTweenScene(p, A, B, tm, sc, t);
    }
    drawBounds(p, sc, t, optimizing);
    pointAtBox(p);
    // The live gap, from the poses the scene just drew. Style A never runs blind or free, so it is
    // always measured against the record's own labelling. A run from a random or grid start, or a
    // blind one, has no correspondence to that labelling, so only the box comparison means anything.
    updateGap(
      p,
      A,
      B,
      optimizing ? (opt.springs ? "snap" : "blind") : isPhysical(state.style) ? mode : "snap",
      optimizing ? !state.playing : t <= sc.moveStart || t >= sc.end - ROUNDING,
    );

    // The panel hands over to the next n only where it changes. It used to fade both layers whole
    // -- the n layer out, a blank beat, then the n + 1 layer in -- so "Proven", the badges and
    // every line that reads the same for both n blinked away and came back. The owner asked for
    // that to stop. A slot drawn identically in both layers now swaps at the midpoint, which
    // cannot be seen. A slot that differs crossfades over the middle half of the handover, 0.2 s
    // at the most: the two opacities always sum to one, so the text never dims through a blank
    // beat, and the eased curve keeps the moment both are half-visible short.
    // The number under the packing is always a changing slot, and it crossfades in place: it used
    // to drift as it faded, which stacked the two numbers into a ghost for the length of the fade.
    const q = optimizing
      ? 1
      : sc.roll > 0
        ? clamp01((t - sc.arrive) / sc.roll)
        : t >= sc.arrive
          ? 1
          : 0;
    const enter = easeInOut(clamp01((q - 0.25) / 0.5));
    const leave = 1 - enter;
    const heldA = q < 0.5 ? "1" : "0";
    const heldB = q < 0.5 ? "0" : "1";
    const slotsA = factsA.children;
    const slotsB = factsB.children;
    const fadeTo = (/** @type {Element[]} */ els, /** @type {string} */ value) => {
      for (const el of els) {
        /** @type {HTMLElement | SVGElement} */ (el).style.opacity = value;
      }
    };
    for (let i = 0; i < factsSame.length; i++) {
      const a = /** @type {HTMLElement | undefined} */ (slotsA[i]);
      const b = /** @type {HTMLElement | undefined} */ (slotsB[i]);
      const parts = factsParts[i];
      if (parts) {
        // A changing slot: the slot itself stays up and its parts do the work.
        if (a !== undefined) {
          a.style.opacity = "1";
        }
        if (b !== undefined) {
          b.style.opacity = "1";
        }
        fadeTo(parts.heldA, heldA);
        fadeTo(parts.heldB, heldB);
        fadeTo(parts.fadeA, String(leave));
        fadeTo(parts.fadeB, String(enter));
        continue;
      }
      if (a !== undefined) {
        a.style.opacity = factsSame[i] ? heldA : String(leave);
      }
      if (b !== undefined) {
        b.style.opacity = factsSame[i] ? heldB : String(enter);
      }
    }
    numeralSlotA.style.opacity = String(leave);
    numeralSlotB.style.opacity = String(enter);
    if (live.textContent !== `n = ${state.liveN}`) {
      live.textContent = `n = ${state.liveN}`;
    }

    syncStageAccessibility();
    updateChrome();
  }

  // The box, as the owner asked on 2026-09-13: a bold square at the side the step is using, black
  // while it is on its way and green once it locks at the best known side, and a thin black trace
  // of where it just was, so every change of size is seen from both ends.
  //   dwell   green rests at n's best known side; the trace the last step left outside it clears
  //           over the dwell's last BOUND_CLEAR.
  //   grow    over the first BOUND_GROW of the move green opens up and to the right to the room
  //           n + 1 can always use -- ceil(sqrt(n + 1)), the grid, or the best known side where that
  //           is wider -- riding out further wherever the moving container breathes past it. The
  //           trace stays inside at n's side.
  //   clear   the inner trace fades over the next BOUND_FADE, leaving room for the new square,
  //           which the schedule holds back, with every other motion, until BOX_FIRST.
  //   settle  green contracts to n + 1's best known side and the trace stays outside it, where the
  //           box was, until the next step clears it.
  // Where the grid is the best known packing the box never changes size and stays green. An
  // open-ended run has walls rather than a step: its box is drawn on the walls, black, with no
  // trace.
  function openSide(n) {
    return Math.max(Math.ceil(Math.sqrt(n)), FRAMES[String(n)].side);
  }
  // Each scene fits its view to its own container, which the box and its trace can lie outside of,
  // so the view is widened, never narrowed, to hold them with the same breathing room.
  function holdInView(side) {
    const view = (svg.getAttribute("viewBox") ?? "").split(/\s+/).map(Number);
    const x = view[0] ?? 0;
    const y = view[1] ?? 0;
    const size = view[2] ?? 0;
    const pad = side * PAD;
    const left = Math.min(x, -pad);
    const right = Math.max(x + size, side + pad);
    const top = Math.min(y, -side - pad);
    const bottom = Math.max(y + size, pad);
    const span = Math.max(right - left, bottom - top);
    if (left === x && top === y && span === size) {
      return;
    }
    const cx = (left + right) / 2;
    const cy = (top + bottom) / 2;
    svg.setAttribute("viewBox", `${cx - span / 2} ${cy - span / 2} ${span} ${span}`);
  }
  function drawBounds(p, sc, t, optimizing) {
    const from = FRAMES[String(p.n)].side;
    const to = FRAMES[String(p.n + 1)].side;
    const open = openSide(p.n + 1);
    let box = sceneSide;
    let trace = sceneSide;
    let seen = 0;
    // The side the view holds through the whole step, so the picture does not zoom as the trace
    // comes and goes: n's open side through the dwell, n + 1's once the box has grown.
    let held = sceneSide;
    if (!optimizing && t <= sc.moveStart) {
      box = from;
      trace = openSide(p.n);
      seen = 1 - ramp(t, sc.moveStart * (1 - BOUND_CLEAR), sc.moveStart);
      held = trace;
    } else if (!optimizing && t < sc.moveEnd) {
      const span = sc.moveEnd - sc.moveStart;
      const grown = sc.moveStart + span * BOUND_GROW;
      const opening = easeInOut(ramp(t, sc.moveStart, grown));
      box = Math.max(sceneSide, lerp(from, open, opening));
      trace = from;
      seen = 1 - ramp(t, grown, grown + span * BOUND_FADE);
      held = Math.max(box, lerp(openSide(p.n), open, opening));
    } else if (!optimizing) {
      trace = Math.max(sceneSide, open);
      box = Math.max(sceneSide, lerp(trace, to, easeInOut(ramp(t, sc.moveEnd, sc.end))));
      seen = 1;
      held = trace;
    }
    if (!optimizing) {
      holdInView(held);
    }
    traceRect.setAttribute("opacity", String(seen));
    traceRect.setAttribute("width", String(trace));
    traceRect.setAttribute("height", String(trace));
    boxRect.setAttribute("width", String(box));
    boxRect.setAttribute("height", String(box));
    boxSide = box;
    // **Locked means at rest at the best known side of the n on show.** The n on show is
    // `state.liveN`, the one the panel and the gap bar describe. Through a move the box is on its
    // way to the room n + 1 needs, and where that room is n + 1's own best known side the box
    // reaches it a fifth of the way in, while the squares still move and the bar still shows n:
    // keyed to n + 1 from the move's start, 16 steps turned green there (#171 R2), and under
    // physics 5 -> 6 flickered as the container breathed past it. So through a move the box locks
    // only on a step whose box does not change size, a grid fill, where it rests from end to end.
    const best = FRAMES[String(state.liveN)].side;
    const resting = t <= sc.moveStart || t >= sc.moveEnd || (from === to && open === to);
    boxLocked =
      !optimizing && resting && Math.abs(box - best) <= PACKING_VALIDITY.penetrationTolerance;
    boxRect.setAttribute("stroke", boxLocked ? MET : "#000000");
  }

  // Style A, the block tween of revision 5: poses tween between the two frames, a block's members
  // riding its rigid transform, the container and the view with them.
  // Where style A puts every square at `t`: the illustration's frame, which the stage draws and the
  // moving palette's checkpoints read.
  function tweenFrame(p, A, B, tm, sc, t) {
    return illustrationFrame({
      pairIndex: state.pair,
      n: state.liveN,
      fromSide: A.side,
      toSide: B.side,
      tracks: motion,
      arriving: { identity: p.n + 1, pose: newPose },
      previousIndex: prevIndex < 0 ? null : prevIndex,
      phase: state.phase,
      schedule: sc,
      seconds: t,
      moveSeconds: tm.move,
      padding: PAD,
      drain: clamp01(desatLevel(sc, t)),
      resting: clamp01(hueLevel(sc, t)),
      links: state.links,
      tint: TINT,
      mark: { wide: MARK_WIDE, thin: MARK_THIN, fade: MARK_FADE },
    });
  }
  function renderTweenScene(p, A, B, tm, sc, t) {
    const scene = tweenFrame(p, A, B, tm, sc, t);
    sceneSide = scene.containerSide;
    for (const square of scene.squares) {
      poseX[square.index] = square.x;
      poseY[square.index] = square.y;
      poseA[square.index] = square.angleDegrees;
    }
    currentTrajectory = null;
    const painted = paintSquares(
      p,
      scene.containerSide,
      scene.presentation.drain,
      scene.presentation.newTint,
      1,
      scene.presentation.resting,
      scene.presentation.homeward,
    );
    renderStage(
      {
        svg,
        containerRect,
        squares: new Map(
          Array.from(pool, ([identity, node]) => [
            identity,
            { node, shape: node.firstElementChild },
          ]),
        ),
        mark,
        markShape: markRect,
        links: linksGroup,
        ghost,
      },
      { scene, fills: painted.fills },
    );
  }

  // ---------------------------------------------------------------- chrome
  const playButton = htmlNode("play");
  const clock = htmlNode("clock");
  const stageWrap = htmlNode("stage-wrap");
  const controls = htmlNode("controls");
  const continuousInfo = htmlNode("continuous-info");
  const optimizeButton = htmlNode("optimize");

  function squareNodeAt(index) {
    return index < motion.length ? motion[index]?.node : index === motion.length ? newNode : null;
  }
  function syncStageAccessibility() {
    const count = poseX === null ? 0 : poseX.length;
    const interactive = state.mode === "pack" && !state.capture && count > 0;
    keyboardSquare = Math.max(0, Math.min(count - 1, keyboardSquare));
    for (let index = 0; index < count; index++) {
      const node = squareNodeAt(index);
      if (node === null || node === undefined) {
        continue;
      }
      if (interactive) {
        node.setAttribute("role", "button");
        node.setAttribute("tabindex", index === keyboardSquare ? "0" : "-1");
        node.setAttribute(
          "aria-label",
          `Square ${index + 1} of ${count}; use arrow keys to move and Q or E to rotate`,
        );
      } else {
        node.removeAttribute("role");
        node.removeAttribute("tabindex");
        node.removeAttribute("aria-label");
      }
    }
    if (!interactive && document.activeElement?.classList.contains("sq")) {
      stage.focus();
    }
    const shownN = state.liveN === null ? stepN() : state.liveN;
    const description = stageDescription({
      aspect: state.mode,
      n: shownN,
      squareCount: shownN,
      containerSide: sceneSide,
      playing: state.playing,
      edited: opt?.edited === true,
    });
    if (stageDescriptionNode.textContent !== description) {
      stageDescriptionNode.textContent = description;
    }
    svg.setAttribute("aria-label", `${shownN} packing squares`);
  }

  // Revision 10: the timeline scrubber is gone. It drew an open-ended optimisation as if it had a
  // fixed length, which is exactly what it has not got. What replaces it is a counter: in Pack the
  // simulated seconds the run has covered with its step count beside them, because those are the
  // only two numbers a run with no end has; in Animate the step's own clock, the position across the
  // range being on the progress bar and in the panel already. `seek(t)` is untouched — it is still
  // a pure function of its argument, and every capture goes through it.
  // Revision 11: the two panel lines that report a *running* number — what the relationship graph
  // has realised and where growth has got to — are redrawn every frame rather than only when a
  // control is touched. They were stale otherwise: a still of a settled contact run showed the
  // fraction the grid start had at step zero.
  function updateLive() {
    if (state.capture) {
      return;
    }
    const rel = relationshipState();
    htmlNode("rel-info").textContent =
      relKind === "general"
        ? `every pair attracts${rel.attracting ? "" : " \u00b7 no pull set"}`
        : relKind === "groups"
          ? `${rel.maskEdges} pairs inside ${PAIRS[state.pair].blocks.length} blocks`
          : rel.met +
            " of " +
            rel.edges +
            " " +
            rel.target +
            " contacts" +
            (rel.attracting ? "" : " \u00b7 no pull");
    const g = growthState();
    htmlNode("grow-info").textContent = !GROWTH.on
      ? "off: every square is a unit side"
      : g.unitSide === null
        ? `starts at ${fmt(g.size, 2)} of a side`
        : "size " +
          fmt(g.size, 2) +
          " " +
          (g.done ? "full" : g.growing ? "growing" : g.stalled ? "stalled" : "held") +
          " · unit " +
          fmt(g.unitSide, 3) +
          // A side is compared with the record only when the arrangement is a packing.
          (g.packing ? ` vs ${fmt(g.record, 3)}` : ", not a packing");
  }
  function updateChrome() {
    if (state.capture) {
      return;
    }
    updateLive();
    if (state.mode === "pack" || (state.optimizing && opt !== null)) {
      const o = state.optimizing && opt !== null ? opt : null;
      clock.textContent = `${fmt(o === null ? 0 : o.time, 2)} s · ${o === null ? 0 : o.steps} steps`;
      return;
    }
    clock.textContent = `${fmt(state.t, 3)} / ${fmt(duration(), 3)} s`;
  }
  // The sliders are built from the table, not written out. A container says which law it is for
  // and the rows follow, which is why there is no list of slider ids anywhere: the ids are a
  // function of the table, so they cannot disagree with it.
  document.querySelectorAll(".law-rows").forEach((host) => {
    const spec = lawSpec(/** @type {HTMLElement} */ (host).dataset.law);
    host.innerHTML = LAW_PARAMS.map((d) => {
      const id = `${spec.prefix}-${d.key}`;
      return (
        '<div class="law-row"><span>' +
        d.label +
        "</span>" +
        '<input type="range" id="' +
        id +
        '" aria-label="' +
        d.says +
        '">' +
        '<span class="law-val" id="' +
        id +
        '-val"></span></div>'
      );
    }).join("");
    host.querySelectorAll("input[type=range]").forEach((el) => {
      const key = el.id.slice(spec.prefix.length + 1);
      el.addEventListener("input", (ev) =>
        setLawOf(spec.name, { [key]: /** @type {HTMLInputElement} */ (ev.target).value }),
      );
    });
  });
  // And syncing them is the same walk: every law, every parameter, no enumeration by hand.
  function syncLawRows() {
    for (const name of Object.keys(LAWS)) {
      const spec = LAWS[name];
      for (const d of LAW_PARAMS) {
        const el = /** @type {HTMLInputElement} */ (
          document.getElementById(`${spec.prefix}-${d.key}`)
        );
        if (!el) {
          continue;
        }
        const [lo, hi] = spec.bounds[d.key];
        el.min = String(lo);
        el.max = String(hi);
        el.step = String(d.step);
        if (document.activeElement !== el) {
          el.value = String(spec.law[d.key]);
        }
        document.getElementById(`${spec.prefix}-${d.key}-val`).textContent = d.decimals
          ? fmt(spec.law[d.key], d.decimals)
          : String(Math.round(spec.law[d.key]));
      }
    }
  }
  const styleSelect = /** @type {HTMLSelectElement} */ (selectNode("style-select"));
  function updateSegments() {
    const searching = searchPanel?.visible() ?? false;
    animationPanel?.setVisible(!searching && state.mode === "animate");
    packPanel?.setVisible(!searching && state.mode === "pack");
    // Revision 14: which solver runs is strategy, so the select sits with the law and the graph —
    // and Pack offers two of the three, the tween being an interpolation toward an answer Pack has
    // not got. The option is taken out of the list rather than left selectable and inert.
    const offered = solversFor(state.mode);
    // The select is the one place the value is written, so it is the one place the invariant is
    // kept: a style this mode does not offer is coerced here rather than only on the transition
    // that could have introduced it. The transition path missed the case that matters most --
    // the page opens in Pack with the tween already selected as the first style, so no mode
    // change ever ran and the chooser showed A while offering only B and C.
    if (!offered.includes(state.style)) {
      state.style = offered.includes("physics") ? "physics" : offered[0];
      solverNote = TWEEN_NOTE;
    }
    Array.from(styleSelect.options).forEach((o) => {
      const ok = isAtlasStyle(o.value) && offered.includes(o.value);
      o.hidden = !ok;
      o.disabled = !ok;
    });
    styleSelect.value = state.style;
    htmlNode("solver-note").textContent = solverNote;
    // The timing and the phasing describe a step. Pack has none, so the group goes — in place, so
    // that nothing else on the panel moves and the stage keeps its size (see the stylesheet).
    htmlNode("step-anim-box").classList.toggle("is-off", state.mode === "pack");
    // The mode sub-panel. Two buttons drawn as tabs: the pressed one names the aspect on show.
    document.querySelectorAll("#mode-tabs button").forEach((b) => {
      const on =
        /** @type {HTMLElement} */ (b).dataset.mode === (searching ? "search" : state.mode);
      b.classList.toggle("on", on);
      b.setAttribute("aria-pressed", on ? "true" : "false");
    });
    document.querySelectorAll("#phase-seg button").forEach((b) => {
      b.classList.toggle("on", /** @type {HTMLElement} */ (b).dataset.phase === state.phase);
    });
    /** @type {HTMLInputElement} */ (inputNode("desat-toggle")).checked = state.desaturate;
    /** @type {HTMLInputElement} */ (inputNode("desat-floor")).value = String(desatFloor);
    htmlNode("desat-floor-val").textContent = fmt(desatFloor, 2);
    /** @type {HTMLInputElement} */ (inputNode("blind-toggle")).checked = state.blind;
    document.querySelectorAll("#initial-seg button").forEach((b) => {
      b.classList.toggle("on", /** @type {HTMLElement} */ (b).dataset.initial === state.initial);
    });
    optimizeButton.textContent = state.optimizing ? "Restart optimize" : "Optimize";
    /** @type {HTMLInputElement} */ (inputNode("blind-inflate")).value = String(BLIND.inflate);
    /** @type {HTMLInputElement} */ (inputNode("anneal")).value = String(state.anneal);
    const an = annealState();
    htmlNode("anneal-info").textContent =
      state.anneal +
      " \u00b7 shake \u00d7" +
      fmt(an.amplitude, 2) +
      ", decay ^" +
      fmt(an.decayPower, 2) +
      ", " +
      fmt(an.span, 2) +
      " move" +
      (isPhysical(state.style) ? "" : " (styles B and C only)");
    syncLawRows();
    document.querySelectorAll("#law-preset-seg button").forEach((b) => {
      const preset = LAW_PRESETS[/** @type {HTMLElement} */ (b).dataset.law];
      b.classList.toggle(
        "on",
        preset !== undefined &&
          ["rigidity", "repulsion", "attraction", "range"].every(
            (k) => Math.abs(preset[k] - LAW[k]) < ROUNDING,
          ),
      );
    });
    // Revision 12: every live readout is written to fit its slot, a slot that overruns clipping
    // rather than pushing what is next to it. This one is at most 44 characters.
    htmlNode("law-info").textContent =
      "knee " +
      Math.round(LAW.repulsion * LAW.rigidity) +
      " · slope ×" +
      fmt(1 + lawSteep(), 1) +
      " past" +
      (lawAttracts()
        ? ` · pull ${Math.round(LAW.attraction)} to ${fmt(LAW.range, 2)}`
        : " · no pull");
    drawLawPlot();
    // The relationship graph, and the two chart options. They are two claims, not one setting: the
    // snap ends on the record by construction and says nothing about the physics; the contact bias
    // only tells the settle which pairs should touch and leaves it to find the geometry.
    document.querySelectorAll("#rel-seg button").forEach((b) => {
      b.classList.toggle("on", /** @type {HTMLElement} */ (b).dataset.rel === relKind);
    });
    /** @type {HTMLInputElement} */ (inputNode("snap-toggle")).checked = state.snap;
    /** @type {HTMLInputElement} */ (inputNode("bias-toggle")).checked = relKind === "contact";
    // Growth.
    const gs = /** @type {HTMLInputElement} */ (inputNode("grow-size")),
      gr = /** @type {HTMLInputElement} */ (inputNode("grow-rate"));
    gs.min = String(GROWTH_BOUNDS.size[0]);
    gs.max = String(GROWTH_BOUNDS.size[1]);
    gs.step = "0.01";
    gr.min = String(GROWTH_BOUNDS.rate[0]);
    gr.max = String(GROWTH_BOUNDS.rate[1]);
    gr.step = "0.005";
    if (document.activeElement !== gs) {
      gs.value = String(GROWTH.size);
    }
    if (document.activeElement !== gr) {
      gr.value = String(GROWTH.rate);
    }
    htmlNode("grow-size-val").textContent = fmt(GROWTH.size, 2);
    htmlNode("grow-rate-val").textContent = `${fmt(GROWTH.rate, 3)}/s`;
    /** @type {HTMLInputElement} */ (inputNode("grow-toggle")).checked = GROWTH.on;
    document.querySelectorAll("#grow-rule-seg button").forEach((b) => {
      b.classList.toggle("on", /** @type {HTMLElement} */ (b).dataset.growRule === GROWTH.rule);
    });
    updateLive();
    /** @type {HTMLInputElement} */ (inputNode("speed")).value = String(speedToSlider(state.speed));
    htmlNode("speed-info").textContent = `\u00d7${state.speed.toFixed(2)}`;
    /** @type {HTMLInputElement} */ (inputNode("links-toggle")).checked = state.links;
    /** @type {HTMLInputElement} */ (inputNode("capture-toggle")).checked = state.capture;
    // Revision 12: the colour scheme, and Animate's own standardising. The standardising box is
    // disabled rather than hidden outside Animate, and disabled under either angle scheme, where it
    // would have nothing to do: a control that vanishes is a control that moves its neighbours.
    document.querySelectorAll("#colour-seg button").forEach((b) => {
      b.classList.toggle("on", /** @type {HTMLElement} */ (b).dataset.scheme === colorScheme);
    });
    // Revision 12: which graph the contact relationship reads, and the drawing mode.
    document.querySelectorAll("#target-seg button").forEach((b) => {
      b.classList.toggle("on", /** @type {HTMLElement} */ (b).dataset.target === targetFrom());
    });
    /** @type {HTMLInputElement} */ (inputNode("draw-toggle")).checked = state.drawing;
    /** @type {HTMLButtonElement} */ (htmlNode("clear-edges")).disabled =
      drawnFor(state.pair).length === 0;
    const animateBox = /** @type {HTMLInputElement} */ (inputNode("animate-standard-toggle"));
    animateBox.checked = ANIMATE.standardize;
    animateBox.disabled = state.mode !== "animate" || colorScheme !== "identity";

    // Under continuous play the sequence's own beat governs, so the three boxes are inert.
    // The four inputs drive whichever beat is in force: `state.timing` for a single step, and
    // CONTINUOUS while a range is playing. They used to be DISABLED under continuous play, on the
    // reasoning that they had no effect there -- which was true, and made them uneditable exactly
    // where the owner was watching. Editing the beat that is running is the whole point of them.
    ["dwell", "move", "correct", "settle"].forEach((key) => {
      const input = /** @type {HTMLInputElement} */ (document.getElementById(`t-${key}`));
      input.disabled = false;
      input.value = state.continuous.on ? CONTINUOUS[key] : state.timing[key];
    });
    /** @type {HTMLInputElement} */ (inputNode("fullbeat-toggle")).checked =
      state.continuous.fullBeat;
    /** @type {HTMLInputElement} */ (inputNode("fastsimple-toggle")).checked =
      state.continuous.fastSimple;
    updateStepChooser();
    updateRangeControls();
    const c = continuousState();
    continuousInfo.textContent =
      (c.on ? "continuous: " : "continuous beat would be ") +
      fmt(c.dwell, 1) +
      " + " +
      fmt(c.move, 1) +
      " + " +
      fmt(c.settle, 1) +
      " s, static appends " +
      (c.fullBeat ? "the same" : `${fmt(c.staticDwell, 1)} s and no move`) +
      " (" +
      c.staticPairs +
      " of " +
      c.pairs +
      " pairs); " +
      c.simplePairs +
      (c.fastSimple ? " simple grid fills at double speed" : " simple grid fills at full length") +
      "; this pair " +
      fmt(duration(), 2) +
      " s, " +
      fmt(c.remaining, 0) +
      " s left of " +
      fmt(c.total, 0) +
      " s";
    // The transport keeps its two glyphs in the markup and swaps which is drawn; its accessible name
    // is set here, because the button carries no text of its own.
    playButton.classList.toggle("is-playing", state.playing);
    playButton.setAttribute(
      "aria-label",
      reduceMotion
        ? state.mode === "pack"
          ? "Advance the packing strategy by one second"
          : "Advance one packing transition"
        : state.playing
          ? "Pause"
          : "Play",
    );
    // The second button does two different things and should say which. Paused, it skips back to
    // the start, so it draws the skip-to-start bar. Running, what it actually does is restart the
    // run, so it draws a circling arrow. Same button, same action, honest glyph.
    const restartButton = htmlNode("restart");
    restartButton.classList.toggle("is-playing", state.playing);
    restartButton.setAttribute(
      "aria-label",
      state.playing ? "Restart the run" : "Back to the start",
    );
  }
  // ---------------------------------------------------------------- the chooser for n (revision 9)
  // One spine: a `from` and a `to`, both stated as the n being stepped *into*, so choosing 17 shows
  // 16 -> 17 and 17 to 17 is one step. The interesting cases are sparse, so a row of chips carries
  // the ones worth opening the page for, and a chip sets both ends at once.
  const DEFAULT_STEP_N = 17;
  const STEP_CHIPS = [5, 10, 11, 17, 26, 29, 100, 110, 272];
  // One line, for the n that has something to say about why it is worth playing with. 17 is the
  // default for exactly this reason.
  const STEP_NOTES = {
    17:
      "n = 17: the search engine here returned exactly the trivial 5 x 5 grid until a " +
      "whole-configuration move was added, so this is the natural step to play the physics on.",
  };
  const stepLabel = htmlNode("step-label");
  const stepNote = htmlNode("step-note");
  const stepChips = htmlNode("step-chips");
  const stepN = () => PAIRS[state.pair].n + 1;
  // The pair that arrives at n, or the nearest one this page carries (the 25-pair demo build carries
  // 25 of the 323 steps, so a chip there lands on the closest step it has).
  function pairForStepN(n) {
    return nearestSupportedIndex(SUPPORTED_STEP_NS, n);
  }
  // Choosing one n is the range collapsed onto it: the old Single step tab, with nothing else to it.
  function setStepN(n) {
    const want = Math.round(Number(n));
    if (!Number.isFinite(want)) {
      return stepN();
    }
    setRange(want, want);
    return stepN();
  }
  for (const v of STEP_CHIPS) {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.dataset.n = String(v);
    chip.textContent = String(v);
    chip.title = `the step ${v - 1} → ${v}`;
    chip.addEventListener("click", () => setStepN(v));
    stepChips.appendChild(chip);
  }
  function updateStepChooser() {
    const n = stepN();
    // Pack is a size, Animate is a step: the label says which is being shown rather than always
    // naming the step, and the quick picks are Pack's, each one being a single n.
    stepLabel.textContent =
      state.mode === "pack" ? `packing n = ${n}` : `showing the step ${n - 1} → ${n}`;
    stepNote.textContent = STEP_NOTES[n] || "";
    const single = state.range.from === state.range.to;
    for (const chip of stepChips.children) {
      chip.classList.toggle(
        "on",
        single && Number(/** @type {HTMLElement} */ (chip).dataset.n) === n,
      );
    }
    stepChips.hidden = state.mode !== "pack";
  }

  // ---------------------------------------------------------------- the range controls
  // The two range boxes, the run's length in wall-clock seconds before it is started, and where the
  // run stands inside it. The length is the honest one: it prices every pair in the range at the
  // beat it will actually play at, static appends and the annealing dial included.
  const rangeFrom = /** @type {HTMLInputElement} */ (inputNode("range-from"));
  const rangeTo = /** @type {HTMLInputElement} */ (inputNode("range-to"));
  const rangeDurationOut = htmlNode("range-duration");
  const rangePosition = htmlNode("range-position");
  const rangeAllButton = htmlNode("range-all");
  const rangeSep = htmlNode("range-sep");
  rangeFrom.min = rangeTo.min = String(RANGE_MIN);
  rangeFrom.max = rangeTo.max = String(RANGE_MAX);
  rangeAllButton.textContent = `whole corpus (${RANGE_MIN} → ${RANGE_MAX})`;
  function clockText(seconds) {
    const s = Math.round(seconds);
    if (s < 90) {
      return `${s} s`;
    }
    return `${Math.floor(s / 60)} min ${String(s % 60).padStart(2, "0")} s`;
  }
  function updateRangeControls() {
    const r = rangeState();
    // Pack's chooser is one number with its minus and plus: the second box, the word between them
    // and the corpus button are Animate's, and so are the two figures, which price a run of a fixed
    // length. Everything stays in the DOM — only its visibility is per-mode.
    const packing = state.mode === "pack";
    rangeSep.hidden = packing;
    rangeTo.hidden = packing;
    rangeAllButton.hidden = packing;
    rangeDurationOut.hidden = packing;
    rangePosition.hidden = packing;
    rangeFrom.setAttribute(
      "aria-label",
      packing ? "the packing size n" : "the first value of n to step into",
    );
    if (document.activeElement !== rangeFrom) {
      rangeFrom.value = String(r.from);
    }
    if (document.activeElement !== rangeTo) {
      rangeTo.value = String(r.to);
    }
    // One step is priced at the controls' own beat, a range at the sequence beat it will play at.
    rangeDurationOut.textContent =
      r.steps === 1
        ? `1 step, ${fmt(duration(), 2)} s`
        : `${r.steps} steps, ${clockText(r.duration)} at this beat`;
    rangePosition.textContent =
      r.steps === 1
        ? ""
        : r.inside
          ? "step " +
            r.step +
            " of " +
            r.steps +
            " · n = " +
            PAIRS[state.pair].n +
            " → " +
            (PAIRS[state.pair].n + 1)
          : `outside the range (n = ${PAIRS[state.pair].n})`;
  }

  // The last height the controls actually had. A hidden document is not laid out, so
  // `offsetHeight` reads zero while the tab is in the background; the stage then scaled to the
  // whole viewport and covered the controls, which came back only on a reload. Keep the last real
  // measurement and never lay out from a hidden one.
  // The tallest the controls have been since the window last changed size -- not the height they
  // happen to have now.
  //
  // The difference matters because the panel's content is not a constant: the two modes offer
  // different controls, and a group that is meaningless in one is taken out of the list rather
  // than left inert. Scaling the stage from the CURRENT height means the picture grows and
  // shrinks as the reader switches modes, which the page's own gate calls "the mode moved the
  // stage" -- and it is right to. Scaling from the tallest the panel has been keeps the stage a
  // fact about the window, and leaves the mode with fewer controls some empty space instead.
  //
  // Reset on a window resize, because a narrower window wraps the panel differently and last
  // window's peak says nothing about this one's.
  let controlsHeight = 0;
  // The largest share of the window height the controls may take before they start scrolling
  // instead of pushing the stage out. Without a cap the two effects compound: the panel WRAPS
  // as the window narrows, so it grows exactly when there is least height to share, and it is
  // subtracted first. Measured before this cap existed: 1920x1080 gave the stage a scale of
  // 0.448, 1512x982 gave 0.256, and 1280x800 gave 0.061 -- a packing drawn at six per cent.
  // Browser zoom changes the CSS viewport the same way a smaller window does, which is how it
  // was noticed. 0.58 is chosen to leave 1920x1080 exactly as it was: the panel is 596 px
  // there, which is 0.552 of the height, so it still fits under the cap and nothing moves.
  const CONTROLS_SHARE = 0.58;
  // The separator between the stage and the controls (owner, 2026-09-14). Dragging it, or
  // moving it with the keyboard, fixes the share of the window height the stage may take;
  // the share is remembered across reloads and re-clamped whenever the window changes, and
  // the controls take the rest and scroll inside it. A double-click forgets the share and
  // returns to the automatic layout below. The stage keeps STAGE_MIN px however high the
  // separator goes, and the controls keep CONTROLS_MIN px, enough for the mode tabs.
  const STAGE_SHARE_KEY = "squares.workbench.stageShare";
  const STAGE_MIN = 120;
  const CONTROLS_MIN = 56;
  let stageShare = readStageShare();
  let stageHandle = null;
  function readStageShare() {
    try {
      const share = Number(window.localStorage.getItem(STAGE_SHARE_KEY));
      return share > 0 && share < 1 ? share : null;
    } catch {
      return null;
    }
  }
  function writeStageShare(share) {
    try {
      if (share === null) {
        window.localStorage.removeItem(STAGE_SHARE_KEY);
      } else {
        window.localStorage.setItem(STAGE_SHARE_KEY, String(share));
      }
    } catch {
      // Storage can be unavailable (a private window, a blocked origin); the share still
      // holds for this page.
    }
  }
  function stageBounds() {
    return { min: STAGE_MIN, max: window.innerHeight - CONTROLS_MIN };
  }
  function layout() {
    if (document.hidden) {
      return;
    }
    const vw = window.innerWidth,
      vh = window.innerHeight;
    const sized =
      stageShare !== null && !state.capture && !document.body.classList.contains("search-active");
    if (sized) {
      const height = clampSeparator(stageShare * vh, stageBounds());
      const scale = Math.min(vw / 1920, height / 1080);
      stage.style.transform = `scale(${scale})`;
      stageWrap.style.width = `${1920 * scale}px`;
      stageWrap.style.height = `${1080 * scale}px`;
      controls.style.height = `${vh - 1080 * scale}px`;
      controls.style.maxHeight = "none";
      stageHandle?.sync();
      return;
    }
    controls.style.height = "";
    controls.style.maxHeight = "";
    let ch = state.capture ? 0 : controls.offsetHeight;
    if (!state.capture) {
      // A hidden document is not laid out, so `offsetHeight` reads zero in a background tab;
      // the stage then scaled to the whole viewport and covered the controls until a reload.
      if (ch > controlsHeight) {
        controlsHeight = ch;
      }
      ch = Math.min(controlsHeight, vh * CONTROLS_SHARE);
    }
    const s = Math.min(vw / 1920, (vh - ch) / 1080);
    stage.style.transform = `scale(${s})`;
    stageWrap.style.width = `${1920 * s}px`;
    stageWrap.style.height = `${1080 * s}px`;
    stageHandle?.sync();
  }

  // ---------------------------------------------------------------- clock (rAF deltas only)
  let rafHandle = null;
  let lastStamp = null;
  function tick(stamp) {
    // The frame this loop asked for has arrived, so it holds no pending request until it makes one.
    rafHandle = null;
    if (!state.playing) {
      return;
    }
    if (lastStamp !== null) {
      let dt = (stamp - lastStamp) / 1000;
      if (dt > 0.1) {
        dt = 0.1;
      }
      if (dt < 0) {
        dt = 0;
      }
      // The speed multiplies the wall-clock delta, so it stretches or compresses playback without
      // touching what any instant looks like. An open-ended run reads it as simulated seconds.
      if (state.optimizing && opt !== null) {
        optimizeAdvance(dt * state.speed);
      } else {
        advance(dt * state.speed);
      }
    }
    lastStamp = stamp;
    // Only a clock still playing asks for the next frame, and only when nothing inside this one
    // already has: a step that ends here pauses, and a play pressed before the next frame starts
    // its own loop. Asking unconditionally ran two loops at twice the frame rate.
    if (state.playing && rafHandle === null) {
      rafHandle = requestAnimationFrame(tick);
    }
  }
  // The next pair is simulated during this pair's dwell, so the cost of a precompute falls where
  // nothing is moving rather than on the first frame of the next move.
  let preparedFor = -1;
  function maybePrefetch() {
    if (!state.playing || !state.continuous.on || !state.continuous.prefetch) {
      return;
    }
    if (!isPhysical(state.style)) {
      return;
    }
    const next = state.pair + 1;
    if (next >= PAIRS.length || preparedFor >= next) {
      return;
    }
    const sc = schedule();
    if (state.t < Math.min(0.1, sc.moveStart * 0.3) || state.t >= sc.moveStart) {
      return;
    }
    preparedFor = next;
    if (timing(next).move > 0) {
      ensureTrajectory(next, state.style);
    }
  }
  function advance(dt) {
    const t = state.t + dt;
    const d = duration();
    if (t >= d) {
      const next = state.pair + 1;
      // Continuous play runs the pairs back to back whether or not they are consecutive; the
      // auto-advance of a single pair only carries on where the sequence itself does.
      const carry =
        next <= scopeBounds().last &&
        (state.continuous.on || (state.autoAdvance && PAIRS[next].n === PAIRS[state.pair].n + 1));
      if (carry) {
        select(next);
        state.t = Math.min(t - d, duration());
        render();
        return;
      }
      state.t = d;
      render();
      pause();
      return;
    }
    state.t = t;
    render();
    maybePrefetch();
  }
  function play() {
    if (state.playing) {
      return;
    }
    if (!state.optimizing && state.t >= duration()) {
      const next = state.pair + 1;
      if (
        state.autoAdvance &&
        next <= scopeBounds().last &&
        PAIRS[next].n === PAIRS[state.pair].n + 1
      ) {
        select(next);
      } else {
        state.t = 0;
      }
    }
    state.playing = true;
    lastStamp = null;
    updateSegments();
    rafHandle = requestAnimationFrame(tick);
  }
  // End an open-ended run. The clock stops with it: a run is what an optimising clock advances, so
  // leaving the clock running after the run is gone plays whatever the timeline holds instead.
  function endRun() {
    if (state.optimizing || opt !== null) {
      pause();
      state.optimizing = false;
      opt = null;
    }
  }
  function pause() {
    state.playing = false;
    markGapBar();
    if (rafHandle !== null) {
      cancelAnimationFrame(rafHandle);
      rafHandle = null;
    }
    lastStamp = null;
    updateSegments();
  }
  function seek(seconds) {
    // Seeking is the timeline's own operation, so it is also how an open-ended run is left.
    if (state.optimizing) {
      pause();
      state.optimizing = false;
      opt = null;
      updateSegments();
    }
    const d = duration();
    state.t = Math.max(0, Math.min(d, Number(seconds) || 0));
    // Revision 14: Pack has no timeline to seek along, so a seek there drops whatever run was going
    // and puts the starting arrangement back rather than uncovering the step animation underneath.
    stagePack();
    markGapBar();
    render();
  }
  function select(index) {
    index = Math.max(0, Math.min(PAIRS.length - 1, index | 0));
    // A run belongs to one n; choosing another ends it, and the clock with it.
    endRun();
    state.pair = index;
    state.t = 0;
    markGapBar();
    buildPair();
    // Revision 13: the run the new n gets is the new n's own, but the size the stage draws at is a
    // setting rather than a run, so it survives the change of n.
    stagePack();
    updateSegments();
    render();
  }
  // The beat, whichever one is running. Under continuous play this edits CONTINUOUS, which is what
  // a range is actually paced by; otherwise it edits the single-step timing. Both are clamped the
  // same way, and a move of zero is refused in both -- a move has to have a duration for anything
  // to be seen happening in it.
  function setTiming(timing) {
    timing = timing || {};
    const frac = duration() > 0 ? state.t / duration() : 0;
    const beat = state.continuous.on ? CONTINUOUS : state.timing;
    if (timing.dwell !== undefined) {
      beat.dwell = Math.max(0, Number(timing.dwell) || 0);
    }
    if (timing.move !== undefined) {
      beat.move = Math.max(0.05, Number(timing.move) || 0.05);
    }
    if (timing.correct !== undefined) {
      beat.correct = Math.max(0.05, Number(timing.correct) || 0.05);
    }
    if (timing.settle !== undefined) {
      beat.settle = Math.max(0, Number(timing.settle) || 0);
    }
    state.t = frac * duration();
    updateSegments();
    render();
  }
  // Revision 12: three schemes, identity the default. Revision 11's `setColorRule` stays as a
  // no-op alias that reports the scheme in force and changes nothing, because four checkers and
  // the capture pipeline call it.
  function setColorScheme(scheme) {
    const next = COLOR_SCHEMES.includes(scheme) ? scheme : COLOR_SCHEMES[0];
    if (next === colorScheme) {
      updateSegments();
      return colorScheme;
    }
    colorScheme = next;
    markGapBar();
    updateSegments();
    render();
    return colorScheme;
  }
  // Animate's own presentation choice: repaint the resting frame in the standard angle map so what a
  // viewer is left looking at matches the atlas, while the motion stays identity-coloured. It does
  // nothing in Pack, and nothing under either angle scheme.
  function setAnimateStandardize(on) {
    ANIMATE.standardize = !!on;
    markGapBar();
    updateSegments();
    render();
    return ANIMATE.standardize;
  }
  function setColorRule() {
    return colorScheme;
  }
  function setPhase(phase) {
    markGapBar();
    state.phase = PHASES.includes(phase) ? phase : PHASES[0];
    updateSegments();
    render();
  }
  // Revision 14: **the tween is not a solver.** Style A interpolates toward a known answer, which
  // is something only a step between two records has; Pack has no answer to interpolate toward, so
  // the tween is not among its choices. It is removed from them rather than left selectable and
  // inert, and a page that arrives in Pack carrying it falls back to the physics and says so in the
  // readout under the select — once, until the next thing the owner chooses.
  const TWEEN_NOTE = "tween is Animate’s: using physics";
  let solverNote = "";
  const solversFor = availableStyles;
  function setStyle(style) {
    markGapBar();
    let next = STYLES.includes(style) ? style : STYLES[0];
    if (state.mode === "pack" && next === "tween") {
      next = "physics";
      solverNote = TWEEN_NOTE;
    } else {
      solverNote = "";
    }
    if (next !== state.style) {
      // Each style drives the new square and the mark from scratch; drop what the other left on
      // the mark's hidden node, so a style's frame does not depend on which style ran before it.
      mark.removeAttribute("transform");
    }
    state.style = next;
    if (isPhysical(state.style)) {
      ensureTrajectory(state.pair, state.style);
    }
    updateSegments();
    render();
  }
  // For verification: the cached trajectory's size, cost and final poses (degrees) for one pair
  // under a style (the current physical style by default; B when the tween is showing).
  function physics(index, style, mode) {
    index = Math.max(0, Math.min(PAIRS.length - 1, index | 0));
    style = isPhysical(style) ? style : isPhysical(state.style) ? state.style : "physics";
    const tr = ensureTrajectory(index, style, mode);
    const N = tr.n + 1;
    const o = tr.steps * N * 3;
    /** @type {[number, number, number][]} */
    const final = [];
    for (let i = 0; i < N; i++) {
      final.push([tr.states[o + i * 3], tr.states[o + i * 3 + 1], tr.states[o + i * 3 + 2] / DEG]);
    }
    let maxSpeed = 0;
    for (let s = 1; s <= tr.steps; s++) {
      for (let i = 0; i < N; i++) {
        const a = ((s - 1) * N + i) * 3,
          b = (s * N + i) * 3;
        const d =
          Math.hypot(tr.states[b] - tr.states[a], tr.states[b + 1] - tr.states[a + 1]) * tr.steps;
        if (d > maxSpeed) {
          maxSpeed = d;
        }
      }
    }
    return {
      pair: index,
      n: tr.n,
      style: tr.style,
      mode: tr.mode,
      bodies: tr.bodies,
      steps: tr.steps,
      ms: tr.ms,
      bytes: tr.states.byteLength,
      maxSpeedPerMove: maxSpeed,
      maxPenetration: tr.maxPenetration,
      maxPenetrationLate: tr.maxPenetrationLate,
      anneal: tr.anneal,
      annealSpan: tr.annealSpan,
      annealAmplitude: tr.annealAmplitude,
      miss: Object.assign({}, tr.miss),
      final,
    };
  }
  function setDesaturate(on) {
    markGapBar();
    state.desaturate = !!on;
    updateSegments();
    render();
  }
  // With the snap off, styles B and C run to the end of the move with no blend and no snap, and the
  // pair comes to rest wherever the physics left it. Style A is unaffected.
  function setSnap(on) {
    markGapBar();
    state.snap = !!on;
    if (isPhysical(state.style)) {
      ensureTrajectory(state.pair, state.style);
    }
    updateSegments();
    render();
  }
  // The blind run: the simulation is told nothing about where the squares belong. It overrides the
  // snap, there being nothing to snap to.
  function setBlind(on) {
    markGapBar();
    state.blind = !!on;
    if (isPhysical(state.style)) {
      ensureTrajectory(state.pair, state.style);
    }
    updateSegments();
    render();
  }
  // The annealing dial. A level is a whole number 0..20; it scales the jiggle, stretches its decay
  // and lengthens the run, so the trajectory cache is keyed by it and the clock has to be rescaled
  // where the move's length changes under a playing pair.
  function setAnneal(level) {
    markGapBar();
    const v = Math.round(Number(level));
    const next = Math.max(ANNEAL.min, Math.min(ANNEAL.max, Number.isFinite(v) ? v : state.anneal));
    if (next === state.anneal) {
      return annealState();
    }
    const d = duration();
    const frac = d > 0 ? state.t / d : 0;
    state.anneal = next;
    state.t = frac * duration();
    if (isPhysical(state.style)) {
      ensureTrajectory(state.pair, state.style);
    }
    updateSegments();
    render();
    return annealState();
  }
  function annealState() {
    return {
      level: state.anneal,
      min: ANNEAL.min,
      max: ANNEAL.max,
      dflt: ANNEAL.dflt,
      amplitude: ANNEAL.amplitude(state.anneal),
      decayPower: ANNEAL.decayPower(state.anneal),
      span: ANNEAL.span(state.anneal),
      // The whole moving span the run is drawn over on the clock. `move` alone stopped being
      // that when the correction got its own time. `steps` counts the base span's work, which a
      // simple transition's speed-up does not shorten.
      move: timing().move + timing().correct,
      steps: physicsSteps(state.pair, state.style),
    };
  }
  // The run's seed. An integer; anything else is ignored rather than silently turned into
  // NaN, which would make every generator produce the same degenerate stream.
  function setSeed(value) {
    const k = parseUint32Seed(value);
    if (k === null) {
      return state.seed;
    }
    state.seed = k;
    // A new seed is a new run: the staged arrangement and any open-ended run belong to the old one.
    // The run is ended through `endRun`, so the clock stops with it rather than playing on with no
    // run behind it; a Pack run starts again from its own start under the new seed. Trajectories
    // are keyed by the seed, so the next frame reads the new seed's.
    const running = state.optimizing && opt !== null;
    endRun();
    if (running && state.mode === "pack") {
      state.optimizing = true;
      opt = newOptimizer(state.initial);
    }
    markGapBar();
    stagePack();
    updateSegments();
    render();
    return state.seed;
  }
  function setBlindInflate(factor) {
    markGapBar();
    const v = Number(factor);
    BLIND.inflate = Math.max(1, Math.min(2, Number.isFinite(v) ? v : BLIND.inflate));
    if (state.blind && isPhysical(state.style)) {
      ensureTrajectory(state.pair, state.style);
    }
    updateSegments();
    render();
  }
  function setOverlay(on) {
    const was = state.links;
    state.links = !!on;
    if (state.links && !was) {
      buildPair(); // the lines are only built when they are wanted
    }
    linksGroup.style.display = state.links ? "" : "none";
    ghost.style.display = state.links ? "" : "none";
    updateSegments();
    render();
  }
  function setCapture(on) {
    state.capture = !!on;
    document.body.classList.toggle("capture", state.capture);
    updateSegments();
    layout();
    render();
  }
  // The playback speed. It is clamped to the slider's ends and rounded to two places, so the value
  // the readout shows is exactly the value in use.
  function setSpeed(multiplier) {
    const v = Number(multiplier);
    const clamped = Math.max(SPEED.min, Math.min(SPEED.max, Number.isFinite(v) ? v : state.speed));
    state.speed = Math.round(clamped * 100) / 100;
    updateSegments();
    return state.speed;
  }
  function setAutoAdvance(on) {
    state.autoAdvance = !!on;
    updateSegments();
  }
  // The whole run, pair by pair: under continuous play the pairs do not all last the same time, so
  // both of these walk the sequence rather than multiplying.
  function sequenceDuration() {
    return timelineSequenceDuration(timelineConfiguration(), state.style);
  }
  function seekSequence(seconds) {
    const position = timelineSeekSequence(
      timelineConfiguration(),
      state.style,
      Number(seconds) || 0,
    );
    if (position.index !== state.pair) {
      select(position.index);
    }
    const held = keepStageInRange();
    seek(held === null ? position.time : held === "first" ? 0 : duration());
  }
  // Continuous play: every pair from here to the last, back to back, keeping the style, the colour
  // rule, the snap, the blind run and the desaturation, on the sequence's own beat.
  function playAll() {
    endRun();
    keepStageInRange();
    state.continuous.on = true;
    preparedFor = -1;
    state.t = 0;
    buildPair();
    updateSegments();
    render();
    play();
    return continuousState();
  }
  function stopAll() {
    pause();
    state.continuous.on = false;
    state.t = Math.min(state.t, duration());
    updateSegments();
    render();
    return continuousState();
  }
  function setContinuous(options) {
    const o = options || {};
    // A change of speed keeps the playhead at the same point of the pair rather than of the clock.
    const frac = duration() > 0 ? state.t / duration() : 0;
    if (o.fullBeat !== undefined) {
      state.continuous.fullBeat = !!o.fullBeat;
    }
    if (o.fastSimple !== undefined && !!o.fastSimple !== state.continuous.fastSimple) {
      state.continuous.fastSimple = !!o.fastSimple;
      state.t = frac * duration();
    }
    if (o.prefetch !== undefined) {
      state.continuous.prefetch = !!o.prefetch;
    }
    if (o.on !== undefined) {
      if (o.on) {
        return playAll();
      }
      return stopAll();
    }
    state.t = Math.min(state.t, duration());
    updateSegments();
    render();
    return continuousState();
  }
  function continuousState() {
    let remaining = 0;
    for (let i = state.pair; i < PAIRS.length; i++) {
      remaining += duration(i);
    }
    let still = 0;
    for (const p of PAIRS) {
      if (p.kind === "prefix" || p.kind === "shared-picture") {
        still++;
      }
    }
    return {
      on: state.continuous.on,
      fullBeat: state.continuous.fullBeat,
      fastSimple: state.continuous.fastSimple,
      prefetch: state.continuous.prefetch,
      dwell: CONTINUOUS.dwell,
      move: CONTINUOUS.move,
      settle: CONTINUOUS.settle,
      staticDwell: CONTINUOUS.staticDwell,
      pair: state.pair,
      pairs: PAIRS.length,
      staticPairs: still,
      simplePairs: SIMPLE.filter(Boolean).length,
      timing: Object.assign({}, timing()),
      total: sequenceDuration(),
      remaining,
    };
  }
  // ---------------------------------------------------------------- the range (revision 9: the spine)
  // The range is stated in the values of n it steps *into*: 17 to 17 is the one step 16 -> 17, and 2
  // to 324 is the whole corpus. It is clamped to what the page carries and to from <= to, and it
  // scopes four things — which pairs a run may play, how long the run is, what the progress bar's
  // scale spans, and which step the stage is on when the current one falls outside it.
  function setRange(from, to) {
    const normalized = normalizeRange(SUPPORTED_STEP_NS, state.range, from, to);
    const { from: lo, to: hi, collapsed, forcedAspect } = normalized;
    state.range.from = lo;
    state.range.to = hi;
    // Revision 10: the range and the mode are the same fact seen twice, so setting one sets the
    // other where they would otherwise disagree. A range wider than one step is something Pack
    // cannot show, so it puts the page in Animate; a collapsed range is legal in both and never
    // forces a mode, since `setRange(17, 17)` in Animate is how one step animation is played.
    if (forcedAspect !== null && forcedAspect !== state.mode) {
      enterAspect(
        planAspectTransition({
          currentAspect: state.mode,
          currentRange: { from: lo, to: hi },
          currentStepN: stepN(),
          rememberedPackN: state.packN,
          rememberedAnimateRange: state.animate,
          supportedSteps: SUPPORTED_STEP_NS,
          target: forcedAspect,
        }),
      );
    }
    // A one-step range is not a continuous run: the three timing boxes govern again.
    if (collapsed && state.continuous.on) {
      pause();
      state.continuous.on = false;
    }
    const b = rangeBounds();
    if (collapsed || state.pair < b.first || state.pair > b.last) {
      if (!state.continuous.on) {
        pause();
      }
      select(collapsed ? pairForStepN(lo) : b.first);
    }
    updateSegments();
    render();
    return rangeState();
  }
  // How long the range takes at the current settings: the sequence's own beat, pair by pair, since
  // a static append is shorter than a matched pair and the annealing dial lengthens the move.
  function rangeDuration() {
    return timelineRangeDuration(timelineConfiguration(), state.range, state.style);
  }
  function rangeState() {
    const b = rangeBounds();
    const inside = state.pair >= b.first && state.pair <= b.last;
    return {
      from: state.range.from,
      to: state.range.to,
      first: b.first,
      last: b.last,
      steps: b.last - b.first + 1,
      span: state.range.to - state.range.from,
      step: inside ? state.pair - b.first + 1 : 0,
      inside,
      duration: rangeDuration(),
      min: RANGE_MIN,
      max: RANGE_MAX,
    };
  }
  // The whole range, end to end: go to its first step and let continuous play carry it to the last.
  function playRange() {
    select(rangeBounds().first);
    return playAll();
  }
  // Revision 10: the two aspects of the one view. Pack is a single fixed n and its playback is the
  // open-ended optimisation — press play and the chosen strategy, from the chosen start, runs until
  // pause. Animate is a range and its playback is the range end to end. Both keep every shared
  // setting: the style, the colour, the annealing, the speed, the start, the timings and the
  // desaturation live in `state` and a switch does not touch one of them.
  //
  // Underneath there is still one spine, the range. Pack is the range with its ends equal, which is
  // why `setStepN` is `setRange(n, n)` and why `setRange` is unchanged: the only new rule is that a
  // range wider than one step names Animate, because Pack has no way to show it. Entering Pack
  // collapses the range onto the n the stage is on, so what you were watching is what you get;
  // entering Animate restores the range Animate was last left on, or opens on the whole corpus, which
  // leaves the stage where it stands and puts its n on the bar's scale.
  //
  // Revision 14 renames it. It was Sweep, and the name had to go before Calibrate arrives, which is
  // the mode that actually sweeps — over parameters. Two modes called Sweep beside each other would
  // have guaranteed a permanent "which sweep?", so the rename went through the internals as well as
  // the label: the mode value is `'animate'`, and nothing reads `sweep` behind a button saying
  // Animate. **`setMode('sweep')` is still accepted**, as a deprecated alias, so anything that
  // still calls it keeps working; it is the one place the old name survives.
  //
  // **Revision 15: switching is a reset, and each mode keeps its own n.** It used to carry whatever
  // was on the stage across, on the reasoning that a run is work and work is not thrown away. What
  // that produced was a page describing one thing and drawing another: leaving Pack mid-run put the
  // optimiser's arrangement under Animate's header, so the panel read `showing the step 10 -> 11`
  // over a stage holding eleven squares that had been pushed around for 110 steps, with the run's
  // clock still counting; and entering Animate re-keyed the bar to the pair's first n while the
  // stage still held the second's, which is a total overlap of 1.0 and a packing the page itself
  // calls invalid. Neither is recoverable by looking at it. So the switch now ends the run, puts
  // the clock at zero and rebuilds the stage from the mode it is entering.
  //
  // Each mode remembering its own n is what keeps that from being lossy: Pack's n and Animate's
  // range are stored on the way out and restored on the way in, so Pack(17) -> Animate -> Pack is
  // Pack(17) again, and Animate always opens at the first step of its range rather than wherever
  // Pack happened to leave the stage.
  function setMode(next) {
    if (next === "search") {
      if (searchPanel === null) {
        throw new Error("Search panel has not mounted");
      }
      if (!searchPanel.visible()) {
        pause();
        state.optimizing = false;
        opt = null;
        searchPanel.setVisible(true);
        animationPanel?.leave();
        packPanel?.setVisible(false);
        document.body.classList.add("search-active");
      }
      updateSegments();
      layout();
      return "search";
    }
    if (searchPanel?.visible()) {
      searchPanel.setVisible(false);
      document.body.classList.remove("search-active");
    }
    if (next !== "pack") {
      packPanel?.setVisible(false);
    }
    if (next === "pack" && animationPanel?.state().active) {
      animationPanel.leave();
    }
    const transition = planAspectTransition({
      currentAspect: state.mode,
      currentRange: state.range,
      currentStepN: stepN(),
      rememberedPackN: state.packN,
      rememberedAnimateRange: state.animate,
      supportedSteps: SUPPORTED_STEP_NS,
      target: next,
    });
    if (!transition.changed) {
      updateSegments();
      return state.mode;
    } // updateSegments coerces the style
    enterAspect(transition);
    if (transition.aspect === "pack") {
      // Revision 13: Pack is where the starting size lives. Revision 14: and where all n squares are
      // on the stage from the first frame, so entering Pack always stages the arrangement --
      // `setRange` collapsed onto one n selects that pair, which is what stages it.
      setRange(transition.range.from, transition.range.to);
      stagePack();
    } else {
      setRange(transition.range.from, transition.range.to);
      // Animate opens at the first step of its range, so the header, the bar and the stage are all
      // describing the same n from the first frame.
      select(transition.pairIndex);
    }
    updateSegments();
    render();
    return state.mode;
  }
  // **Entering an aspect is a reset, wherever the entry comes from** (#125 F12): the mode tabs, or a
  // range too wide for Pack. Nothing that belonged to the aspect being left survives into the one
  // being entered: `opt` is the open-ended run, `state.t` the animation clock, and each aspect's
  // remembered n or range is stored on the way out.
  function enterAspect(transition) {
    controlsHeight = 0;
    state.animate = transition.rememberedAnimateRange;
    state.packN = transition.rememberedPackN;
    state.mode = transition.aspect;
    endRun();
    pause();
    state.t = 0;
    // Revision 14: the tween is Animate's, so entering Pack with it selected falls back to the
    // physics and leaves the reason under the select; leaving Pack clears the note, the choice
    // being available again.
    if (transition.aspect === "pack" && state.style === "tween") {
      state.style = "physics";
      solverNote = TWEEN_NOTE;
    }
    if (transition.aspect === "animate") {
      solverNote = "";
    }
  }
  // **The one place the stage is put back inside the range** (#125 F12). Every call that moves the
  // stage to another step ends here: a one-step range follows the stage, as the step buttons carry
  // it, and a wider range holds the stage at its nearer end. Answers which end it held at, if any.
  function keepStageInRange() {
    const b = rangeBounds();
    if (state.pair >= b.first && state.pair <= b.last) {
      return null;
    }
    if (state.range.from === state.range.to) {
      const n = PAIRS[state.pair].n + 1;
      state.range.from = n;
      state.range.to = n;
      updateSegments();
      return null;
    }
    const end = state.pair < b.first ? "first" : "last";
    select(end === "first" ? b.first : b.last);
    return end;
  }
  function advanceReducedMotion() {
    const b = rangeBounds();
    const action = reducedMotionAction({
      aspect: state.mode,
      optimizing: state.optimizing && opt !== null,
      pairIndex: state.pair,
      firstPairIndex: b.first,
      lastPairIndex: b.last,
      atPairEnd: state.t >= duration(),
    });
    pause();
    state.continuous.on = false;
    switch (action) {
      case "initialize-pack":
        optimize(true);
        pause();
        optimizeStep(OPT.stepsPerSecond);
        live.textContent = "Reduced-motion mode advanced the packing strategy by one second.";
        return;
      case "step-pack":
        optimizeStep(OPT.stepsPerSecond);
        live.textContent = "Reduced-motion mode advanced the packing strategy by one second.";
        return;
      case "finish-pair":
        seek(duration());
        live.textContent = `Reduced-motion mode advanced to n = ${state.liveN}.`;
        return;
      case "finish-next-pair":
        select(state.pair + 1);
        seek(duration());
        live.textContent = `Reduced-motion mode advanced to n = ${state.liveN}.`;
        return;
      case "restart-and-finish":
        select(b.first);
        seek(duration());
        live.textContent = `Reduced-motion mode restarted at n = ${state.liveN}.`;
        return;
    }
  }
  // Revision 9: one transport button for one view. Revision 10: what it plays is the mode's own
  // playback — the open-ended run in Pack, the range in Animate — and pause stops it where it stands.
  // A range run that has reached its end starts again from the top.
  function transport() {
    if (animationPanel?.state().active) {
      animationPanel.togglePlayback();
      return;
    }
    if (reduceMotion) {
      advanceReducedMotion();
      return;
    }
    const b = rangeBounds();
    const action = transportIntent({
      aspect: state.mode,
      playing: state.playing,
      optimizing: state.optimizing && opt !== null,
      continuous: state.continuous.on,
      pairIndex: state.pair,
      firstPairIndex: b.first,
      lastPairIndex: b.last,
      atEnd: state.t >= duration(),
    });
    switch (action) {
      case "pause":
        pause();
        return;
      case "start-pack":
        optimize(true);
        return;
      case "start-range":
        playRange();
        return;
      case "resume-pack":
      case "resume-animation":
        play();
        return;
    }
  }
  // Revision 14: **restart is return to the beginning of whatever play would play.** The owner
  // asked for it beside play and pause, and then for the thought behind it: "perhaps the restart
  // makes more sense for Pack than for Animate." It does, and that is the reason to define it once
  // rather than twice — in Pack the beginning is the starting arrangement with every setting kept,
  // in Animate it is the first step of the range, and the transport keeps its shape across both.
  //
  // It is not the `reset physics` button beside the growth box, and the two are worth telling
  // apart: reset puts every *parameter* back to its default and leaves the picture where it stands;
  // restart puts the *picture* back to the beginning and leaves every parameter where it stands.
  // A run that was playing keeps playing, from the top, which is what a transport control does.
  function restart() {
    if (animationPanel?.state().active) {
      const trace = animationPanel.seek(0);
      return { mode: state.mode, n: trace.n ?? state.liveN, playing: false, t: 0, steps: 0 };
    }
    const was = state.playing;
    pause();
    if (state.mode === "pack") {
      state.optimizing = false;
      opt = null;
      // The previous packing is staged rather than run from, so it goes back through the one path
      // that stages it; every other start is its own arrangement, built fresh from the same seed.
      if (state.initial === "previous") {
        stagePack();
      } else {
        state.optimizing = true;
        opt = newOptimizer(state.initial);
      }
    } else {
      const b = rangeBounds();
      if (state.pair !== b.first) {
        select(b.first);
      }
      state.t = 0;
      preparedFor = -1;
    }
    markGapBar();
    updateSegments();
    render();
    if (was) {
      play();
    }
    return {
      mode: state.mode,
      n: stepN(),
      playing: state.playing,
      t: state.t,
      steps: opt === null ? 0 : opt.steps,
    };
  }
  // Revision 9: the range is the only span, so the tabs are gone from the page. These stay on the
  // API as no-ops for anything that still calls them.
  /** @returns {"single"} */
  function setTab() {
    return "single";
  }
  // Redraw the gap bar against whatever is on the stage right now, whether or not it is moving.
  function refreshGap() {
    markGapBar();
    render();
    return Object.assign({}, gapbarOut);
  }
  // The pair that starts at n, or the nearest one this page carries.
  function goTo(n) {
    const want = Math.round(Number(n));
    if (!Number.isFinite(want)) {
      return PAIRS[state.pair].n;
    }
    let best = 0,
      dist = Infinity;
    for (let i = 0; i < PAIRS.length; i++) {
      const d = Math.abs(PAIRS[i].n - want);
      if (d < dist) {
        dist = d;
        best = i;
      }
    }
    if (!state.continuous.on) {
      pause();
    }
    select(best);
    keepStageInRange();
    return PAIRS[state.pair].n;
  }

  // The workbench's API, hung on the page's own global: one handle for the probes, the capture
  // script and the console. The type library's `Window` knows nothing of `atlasTransitions`, so the
  // property is named here, once, rather than at each of the two places that touch it.
  /** @typedef {Window & typeof globalThis & { atlasTransitions: WorkbenchApi, packWorkbench: import("./api/pack-api.js").PackWorkbenchApi, searchWorkbench: import("./app/search-panel.js").SearchPanel }} PageWindow */
  const win = /** @type {PageWindow} */ (window);
  /** @type {WorkbenchApi} */
  const atlasTransitions = {
    importAnimation: (text, legacy) => requireAnimationPanel().load(text, legacy),
    animationState: () => requireAnimationPanel().state(),
    seekAnimation: (time) => requireAnimationPanel().seek(time),
    exportAnimation: () => requireAnimationPanel().export(),
    exportAnimationSvg: () => requireAnimationPanel().svg(),
    leaveAnimation: () => requireAnimationPanel().leave(),
    // Revision 9: the tabs are gone; these are no-ops kept so nothing that called them breaks.
    setTab,
    tab: () => "single",
    // The chooser for n, which is the range collapsed onto one value.
    setStepN,
    stepN,
    // The range — the single spine — and the run that plays it end to end.
    setRange,
    range: rangeState,
    playRange,
    transport,
    // Revision 14: back to the beginning of whatever play would play — Pack's starting arrangement
    // or Animate's first step — with every setting kept. Distinct from `reset`, which puts the
    // parameters back and leaves the picture alone.
    restart,
    // Revision 10: which aspect the page is showing. Pack is the range collapsed onto one n and
    // played as the open-ended run; Animate is the range played end to end.
    setMode,
    mode: () => (searchPanel?.visible() ? "search" : state.mode),
    // Revision 8, feature 4: what the gap bar is showing. Revision 9: and the call that redraws it
    // on demand, the bar having stopped following every frame of the motion.
    gapBar: () => Object.assign({}, gapbarOut),
    refreshGap,
    seek,
    duration,
    play,
    pause,
    select,
    setTiming,
    // Revision 11: the colouring is one map and is always on, so `setColorRule` is a no-op kept for
    // callers. `colour()` is what the frame was painted from — the angle classes, their palette
    // slots, and every square's full-side contact count — and `fillsFor` is the map as a pure
    // function of angles and contacts, testable with nothing on the stage at all.
    setColorRule,
    colour: colourState,
    fillsFor: angleFills,
    atlasFillsFor: atlasFills,
    // Revision 12: colour is the square's identity by default, and the two angle maps are options.
    // `identityFills(k)` is the greens as a pure function of the identity, needing nothing on the
    // stage; the Animate standardising is an Animate-mode presentation setting and nothing else.
    setColorScheme,
    colorScheme: () => colorScheme,
    colorSchemes: () => COLOR_SCHEMES.slice(),
    // How far a moving square is drained, as the chroma it keeps. Clamped to [0, 1]: past 1 a
    // "drained" square would be more saturated than a settled one, which would invert what the
    // drain is for.
    setDesatFloor: (v) => {
      const k = Number(v);
      desatFloor = Math.max(0, Math.min(1, Number.isFinite(k) ? k : desatFloor));
      markGapBar();
      render();
      return desatFloor;
    },
    desatFloor: () => desatFloor,
    // The stage's area compensation. 1 is the atlas's own chroma, which is what a check that
    // compares the stage with a rendering sets before it looks.
    setStageChroma: (v) => {
      const k = Number(v);
      stageChroma = Math.max(0.3, Math.min(1, Number.isFinite(k) ? k : stageChroma));
      render();
      return stageChroma;
    },
    stageChroma: () => stageChroma,
    identityFills,
    setAnimateStandardize,
    animateStandardize: () => ANIMATE.standardize,
    setPhase,
    setStyle,
    setOverlay,
    setCapture,
    setAutoAdvance,
    setDesaturate,
    setSnap,
    setBlind,
    setBlindInflate,
    setSeed,
    seed: () => state.seed,
    // Revision 9: how fast the clock runs while playing. Playback only: seek(t) is unchanged.
    setSpeed,
    speed: () => state.speed,
    // Revision 9: what an open-ended run starts from, the run itself, and what it has reached.
    setInitial,
    initial: () => state.initial,
    initials: () => INITIALS.slice(),
    optimize,
    optimizeStep,
    optimizeState,
    // Revision 9: the hand. `pickAt` takes world coordinates, which is what the drag handlers turn
    // client coordinates into, so a test can drive a drag without a mouse. Revision 12 adds the
    // other direction, `poseOf`: where the frame actually drew square i, so a test can turn a
    // square into the screen point a real pointer gesture has to start from.
    pickAt,
    grab,
    dragTo,
    release,
    hand,
    poseOf: (i) => {
      const k = Math.round(Number(i));
      return poseX === null || !Number.isFinite(k) || k < 0 || k >= poseX.length
        ? null
        : [poseX[k], poseY[k], poseA[k]];
    },
    // Revision 7, feature 2: the annealing dial.
    setAnneal,
    anneal: annealState,
    // Revision 11: the one force law, its presets, its sampled shape, and the two draggable control
    // points of the plot driven without a pointer.
    setLaw,
    law: lawState,
    setLawPreset,
    lawPresets: () => Object.keys(LAW_PRESETS),
    lawCurve,
    lawForce,
    dragLaw,
    // Revision 15: the walls' own law, the same shape for the other relationship a square has.
    setWallLaw,
    wallLaw: () => Object.assign({}, WALLLAW),
    wallForce,
    // The table itself, so a caller (or a check) can ask what parameters and laws exist
    // rather than keeping its own copy of the answer.
    lawNames: () => Object.keys(LAWS),
    lawParams: () => LAW_KEYS.slice(),
    lawPrefix: (n) => lawSpec(n).prefix,
    setLawOf,
    // Revision 11: who attracts whom. Orthogonal to the law: repulsion is never masked.
    setRelationship,
    relationship: relationshipState,
    relationships: () => RELATIONSHIPS.slice(),
    setTargetGraph,
    targetGraph: () => targetGraphFor(state.pair).slice(),
    // Revision 12: the hand-drawn contact graph. It is the same object the record-derived graph is
    // — it reaches the mask through `targetGraphFor` and nothing else — so a random or enumerated
    // graph handed to `setEdges` drives a run without touching the physics. `linkStart` /
    // `linkMove` / `linkEnd` are the pointer gesture, drivable from a test with no pointer.
    edges: drawnEdges,
    setEdges,
    clearEdges,
    toggleEdge,
    setTargetSource,
    targetSource: targetFrom,
    targetSources: () => TARGET_SOURCES.slice(),
    setDrawing,
    drawing: () => state.drawing,
    linkStart,
    linkMove,
    linkEnd,
    linkCancel,
    // Revision 11: start small and grow, and put every physics parameter back where it started.
    setGrowth,
    growth: growthState,
    growthRules: () => GROWTH_RULES.slice(),
    reset: resetPhysics,
    contactGraph: () =>
      poseA === null
        ? []
        : Array.from(paintTouching).map((k) => [Math.floor(k / poseA.length), k % poseA.length]),
    sequenceDuration,
    seekSequence,
    physics,
    // Revision 6, feature 4: the whole sequence back to back, and the jump to a given n.
    playAll,
    stopAll,
    setContinuous,
    goTo,
    continuous: continuousState,
    styles: () => STYLES.slice(),
    // Revision 14: which of them the mode on show actually offers. Pack offers two: the tween is an
    // interpolation toward a known answer, and Pack has no answer to interpolate toward.
    solvers: () => solversFor(state.mode),
    progress: () => ({ position: progress(), n: state.liveN }),
    schedule: () => Object.assign({}, schedule()),
    pairs: () => PAIRS.map((p, i) => ({ index: i, n: p.n, kind: p.kind, stats: p.stats })),
    // Revision 5: the motion modes, the current pair's blocks, the identity arrays of its two
    // frames, and the new square with the rule that chose it.
    phases: () => PHASES.slice(),
    blocks: () =>
      PAIRS[state.pair].blocks.map((b) =>
        Object.assign({}, b, { members: b.members.slice(), riders: b.riders.slice() }),
      ),
    blockOf: () => PAIRS[state.pair].block_of.slice(),
    identities: () => ({
      from: FRAMES[String(PAIRS[state.pair].n)].ident.slice(),
      to: FRAMES[String(PAIRS[state.pair].n + 1)].ident.slice(),
    }),
    newSquare: () => ({
      index: PAIRS[state.pair].new,
      identity: PAIRS[state.pair].n + 1,
      rule: PAIRS[state.pair].new_rule,
      tied: PAIRS[state.pair].new_tied,
    }),
    state: () => ({
      // `mode` has meant the simulation mode (snap / free / blind) since revision 6 and still does;
      // revision 10's Pack-or-Animate aspect is `aspect` here and `mode()` on the API. They were both
      // called `mode` in this object for one revision, and the later key silently won.
      tab: "single",
      aspect: state.mode,
      pair: state.pair,
      n: PAIRS[state.pair].n,
      t: state.t,
      duration: duration(),
      playing: state.playing,
      // `rule` is revision 12's colour scheme; it was the constant 'angle' for one revision.
      rule: colorScheme,
      phase: state.phase,
      style: state.style,
      links: state.links,
      capture: state.capture,
      timing: Object.assign({}, state.timing),
      desaturate: state.desaturate,
      snap: state.snap,
      blind: state.blind,
      blindInflate: BLIND.inflate,
      mode: simMode(),
      anneal: state.anneal,
      speed: state.speed,
      initial: state.initial,
      optimizing: state.optimizing,
      seed: state.seed,
      shownN: state.liveN,
    }),
  };
  win.atlasTransitions = new Proxy(atlasTransitions, {
    get(target, property, receiver) {
      const member = Reflect.get(target, property, receiver);
      if (
        !catalogueOwnsPage() &&
        typeof member === "function" &&
        property !== "setMode" &&
        property !== "mode"
      ) {
        return () => {
          throw new Error(
            "atlasTransitions controls catalogue animation; use packWorkbench or searchWorkbench for the active view",
          );
        };
      }
      return member;
    },
  });

  // ---------------------------------------------------------------- wiring
  // Previous and next move the step the stage is on. Where the range is one step they carry it with
  // them, so the pair and the range never disagree; inside a wider range they stay inside it.
  function nudgeStep(delta) {
    if (state.mode === "pack" || state.range.from === state.range.to) {
      // The next step the page carries, across any gap: `stepN() + delta` rounded back to the
      // nearest carried step, which on a sparse page is the step already showing.
      setStepN(adjacentSupportedStep(SUPPORTED_STEP_NS, stepN(), delta));
      return;
    }
    const b = rangeBounds();
    pause();
    select(Math.max(b.first, Math.min(b.last, state.pair + delta)));
  }
  htmlNode("prev").addEventListener("click", () => nudgeStep(-1));
  htmlNode("next").addEventListener("click", () => nudgeStep(1));
  rangeAllButton.addEventListener("click", () => setRange(RANGE_MIN, RANGE_MAX));
  htmlNode("refresh-gap").addEventListener("click", () => refreshGap());
  playButton.addEventListener("click", () => transport());
  htmlNode("restart").addEventListener("click", () => restart());
  document.querySelectorAll("#mode-tabs button").forEach((b) => {
    b.addEventListener("click", () => setMode(/** @type {HTMLElement} */ (b).dataset.mode));
  });
  document.querySelectorAll("#phase-seg button").forEach((b) => {
    b.addEventListener("click", () => setPhase(/** @type {HTMLElement} */ (b).dataset.phase));
  });
  styleSelect.addEventListener("change", () => setStyle(styleSelect.value));
  document
    .getElementById("desat-toggle")
    .addEventListener("change", (ev) =>
      setDesaturate(/** @type {HTMLInputElement} */ (ev.target).checked),
    );
  document
    .getElementById("blind-toggle")
    .addEventListener("change", (ev) =>
      setBlind(/** @type {HTMLInputElement} */ (ev.target).checked),
    );
  document
    .getElementById("blind-inflate")
    .addEventListener("change", (ev) =>
      setBlindInflate(/** @type {HTMLInputElement} */ (ev.target).value),
    );
  document
    .getElementById("anneal")
    .addEventListener("input", (ev) =>
      setAnneal(/** @type {HTMLInputElement} */ (ev.target).value),
    );
  document.querySelectorAll("#law-preset-seg button").forEach((b) => {
    b.addEventListener("click", () => setLawPreset(/** @type {HTMLElement} */ (b).dataset.law));
  });
  document.querySelectorAll("#rel-seg button").forEach((b) => {
    b.addEventListener("click", () => setRelationship(/** @type {HTMLElement} */ (b).dataset.rel));
  });
  inputNode("desat-floor").addEventListener("input", (ev) => {
    win.atlasTransitions.setDesatFloor(/** @type {HTMLInputElement} */ (ev.target).value);
    updateChrome();
  });
  document
    .getElementById("grow-size")
    .addEventListener("input", (ev) =>
      setGrowth({ size: /** @type {HTMLInputElement} */ (ev.target).value }),
    );
  document
    .getElementById("grow-rate")
    .addEventListener("input", (ev) =>
      setGrowth({ rate: /** @type {HTMLInputElement} */ (ev.target).value }),
    );
  document
    .getElementById("grow-toggle")
    .addEventListener("change", (ev) =>
      setGrowth({ on: /** @type {HTMLInputElement} */ (ev.target).checked }),
    );
  document.querySelectorAll("#grow-rule-seg button").forEach((b) => {
    b.addEventListener("click", () =>
      setGrowth({ rule: /** @type {HTMLElement} */ (b).dataset.growRule }),
    );
  });
  htmlNode("reset-physics").addEventListener("click", () => resetPhysics());
  document
    .getElementById("snap-toggle")
    .addEventListener("change", (ev) =>
      setSnap(/** @type {HTMLInputElement} */ (ev.target).checked),
    );
  // Turning the bias on with no attraction set would mask a force that is not there, so it brings
  // the sticky preset's pull with it. That is a convenience of the control, not of the physics:
  // `setRelationship('contact')` on the API changes the graph and nothing else.
  inputNode("bias-toggle").addEventListener("change", (ev) => {
    // The wanted state is read once, before anything is set. `setLaw` runs `updateSegments`, which
    // writes this box's checked state back from a relationship that has not been changed yet, so
    // re-reading `ev.target.checked` on the next line saw the box untick itself and turned the bias
    // straight off again — the first click did nothing but bring the pull in.
    const want = /** @type {HTMLInputElement} */ (ev.target).checked;
    if (want && !lawAttracts()) {
      setLaw({ attraction: LAW_PRESETS.sticky.attraction, range: LAW_PRESETS.sticky.range });
    }
    setRelationship(want ? "contact" : "general");
  });
  lawPlotWiring();
  document.querySelectorAll("#initial-seg button").forEach((b) => {
    b.addEventListener("click", () => setInitial(/** @type {HTMLElement} */ (b).dataset.initial));
  });
  optimizeButton.addEventListener("click", () => optimize(true));
  document
    .getElementById("speed")
    .addEventListener("input", (ev) =>
      setSpeed(sliderToSpeed(Number(/** @type {HTMLInputElement} */ (ev.target).value))),
    );
  document.querySelectorAll("#colour-seg button").forEach((b) => {
    b.addEventListener("click", () =>
      setColorScheme(/** @type {HTMLElement} */ (b).dataset.scheme),
    );
  });
  document
    .getElementById("animate-standard-toggle")
    .addEventListener("change", (ev) =>
      setAnimateStandardize(/** @type {HTMLInputElement} */ (ev.target).checked),
    );
  document
    .getElementById("links-toggle")
    .addEventListener("change", (ev) =>
      setOverlay(/** @type {HTMLInputElement} */ (ev.target).checked),
    );
  document
    .getElementById("draw-toggle")
    .addEventListener("change", (ev) =>
      setDrawing(/** @type {HTMLInputElement} */ (ev.target).checked),
    );
  document.querySelectorAll("#target-seg button").forEach((b) => {
    b.addEventListener("click", () =>
      setTargetSource(/** @type {HTMLElement} */ (b).dataset.target),
    );
  });
  htmlNode("clear-edges").addEventListener("click", () => clearEdges());
  document
    .getElementById("capture-toggle")
    .addEventListener("change", (ev) =>
      setCapture(/** @type {HTMLInputElement} */ (ev.target).checked),
    );
  ["dwell", "move", "correct", "settle"].forEach((key) => {
    document.getElementById(`t-${key}`).addEventListener("change", (ev) => {
      const o = {};
      o[key] = /** @type {HTMLInputElement} */ (ev.target).value;
      setTiming(o);
    });
  });
  document
    .getElementById("fullbeat-toggle")
    .addEventListener("change", (ev) =>
      setContinuous({ fullBeat: /** @type {HTMLInputElement} */ (ev.target).checked }),
    );
  document
    .getElementById("fastsimple-toggle")
    .addEventListener("change", (ev) =>
      setContinuous({ fastSimple: /** @type {HTMLInputElement} */ (ev.target).checked }),
    );
  // Typing in `from` alone drags `to` with it while the two are equal, so a one-step range stays one
  // step rather than silently widening.
  rangeFrom.addEventListener("change", () => {
    const single = state.mode === "pack" || state.range.from === state.range.to;
    setRange(rangeFrom.value, single ? rangeFrom.value : state.range.to);
  });
  rangeTo.addEventListener("change", () => setRange(state.range.from, rangeTo.value));
  // The hand. Client coordinates go through the world group's own matrix, so the y flip, the
  // viewBox and the stage's CSS scale are all accounted for in one step. Pointer capture keeps the
  // drag alive when the cursor leaves the square, or the stage.
  // The SVG group the stage is drawn in, so it carries a screen matrix. `getElementById` is typed
  // as returning an HTML element whatever it finds, which is why the SVG type is named through
  // `Element` here.
  const worldGroup = /** @type {SVGGElement} */ (/** @type {Element} */ (svgNode("world")));
  function worldPoint(ev) {
    const m = worldGroup.getScreenCTM();
    if (m === null) {
      return null;
    }
    const inv = m.inverse();
    const pt = new DOMPoint(ev.clientX, ev.clientY).matrixTransform(inv);
    return [pt.x, pt.y];
  }
  stage.addEventListener("keydown", (ev) => {
    if (ev.metaKey || ev.ctrlKey || ev.altKey || !catalogueOwnsPage()) {
      return;
    }
    const target = ev.target instanceof Element ? ev.target : null;
    const rawIndex = target?.getAttribute("data-square-index");
    const squareIndex = rawIndex === null || rawIndex === undefined ? -1 : Number(rawIndex);
    const squareFocused = Number.isInteger(squareIndex) && squareIndex >= 0;
    const command = stageKeyCommand(ev.key, ev.shiftKey, squareFocused);
    if (command === null) {
      return;
    }
    ev.preventDefault();
    ev.stopPropagation();
    if (command.kind === "focus-square") {
      if (state.mode !== "pack") {
        live.textContent = "Square editing is available in Pack mode.";
        return;
      }
      squareNodeAt(keyboardSquare)?.focus();
      return;
    }
    if (command.kind === "leave-square") {
      stage.focus();
      live.textContent = "Returned to the packing stage.";
      return;
    }
    keyboardSquare = squareIndex;
    adjustSquareFromKeyboard(squareIndex, command);
    squareNodeAt(squareIndex)?.focus();
    live.textContent =
      command.kind === "move-square"
        ? `Square ${squareIndex + 1} moved by keyboard.`
        : `Square ${squareIndex + 1} rotated by keyboard.`;
  });
  // Revision 12: the two gestures on the stage are the same press, drag and release, so the toggle
  // decides which of them a press starts and nothing is ever ambiguous. With `draw links` on no
  // square is picked up at all; with it off the drawing code is never entered.
  svg.addEventListener("pointerdown", (ev) => {
    if (animationPanel?.state().active || !catalogueOwnsPage()) {
      return;
    }
    if (ev.button !== 0) {
      return;
    }
    const w = worldPoint(ev);
    if (w === null) {
      return;
    }
    const i = pickAt(w[0], w[1]);
    if (i < 0) {
      return;
    }
    ev.preventDefault();
    keyboardSquare = i;
    svg.setPointerCapture(ev.pointerId);
    if (state.drawing) {
      linkStart(i);
      linkMove(w[0], w[1]);
      return;
    }
    document.body.classList.add("dragging");
    grab(i, w[0], w[1]);
  });
  svg.addEventListener("pointermove", (ev) => {
    const w = worldPoint(ev);
    if (w === null) {
      return;
    }
    if (linkFrom >= 0) {
      ev.preventDefault();
      linkMove(w[0], w[1]);
      return;
    }
    if (opt === null || opt.held < 0) {
      return;
    }
    ev.preventDefault();
    dragTo(w[0], w[1], ev.shiftKey);
  });
  const endDrag = (ev) => {
    // Whatever ended the gesture, the drag is over: a key that ends the run mid-drag has already
    // dropped the hand, and the early return below would otherwise leave the class behind.
    document.body.classList.remove("dragging");
    if (linkFrom >= 0) {
      if (svg.hasPointerCapture(ev.pointerId)) {
        svg.releasePointerCapture(ev.pointerId);
      }
      const w = worldPoint(ev);
      linkEnd(w === null ? -1 : pickAt(w[0], w[1]));
      return;
    }
    if (opt === null || opt.held < 0) {
      return;
    }
    if (svg.hasPointerCapture(ev.pointerId)) {
      svg.releasePointerCapture(ev.pointerId);
    }
    release();
  };
  svg.addEventListener("pointerup", endDrag);
  svg.addEventListener("pointercancel", endDrag);

  window.addEventListener("keydown", (ev) => {
    // A shortcut is a bare key. With Cmd, Ctrl or Alt held the key belongs to the browser or the
    // system: Cmd+C is a copy, not capture mode, and taking it made the controls vanish.
    if (ev.metaKey || ev.ctrlKey || ev.altKey) {
      return;
    }
    // Pack and Search own their keys: their fields take Space and the arrows, their buttons
    // take Space, and a letter typed there is text, not a shortcut for the hidden catalogue.
    if (!catalogueOwnsPage()) {
      return;
    }
    // What has the focus, read as an element once: the guard is about typing into a control, and
    // the three questions below are all about the same one.
    const focused = /** @type {HTMLElement} */ (ev.target);
    if (focused?.closest("#animation-editor") || focused?.tagName === "TEXTAREA") {
      return;
    }
    if (
      animationPanel?.state().active &&
      ["ArrowLeft", "ArrowRight", "Home", "End"].includes(ev.key)
    ) {
      ev.preventDefault();
      const time = animationPanel.state().time;
      animationPanel.seek(
        ev.key === "Home"
          ? 0
          : ev.key === "End"
            ? 1
            : time + (ev.key === "ArrowRight" ? 0.01 : -0.01),
      );
      return;
    }
    if (
      focused &&
      (focused.tagName === "INPUT" || focused.tagName === "SELECT") &&
      ev.key !== "Escape"
    ) {
      if (ev.key === " " || ev.key === "ArrowLeft" || ev.key === "ArrowRight") {
        focused.blur();
      } else {
        return;
      }
    }
    switch (ev.key) {
      case " ":
        ev.preventDefault();
        transport();
        break;
      case "ArrowLeft":
        ev.preventDefault();
        nudgeStep(-1);
        break;
      case "ArrowRight":
        ev.preventDefault();
        nudgeStep(1);
        break;
      case "Home":
        ev.preventDefault();
        seek(0);
        break;
      case "End":
        ev.preventDefault();
        seek(duration());
        break;
      case "p":
        setStyle(STYLES[(STYLES.indexOf(state.style) + 1) % STYLES.length]);
        break;
      case "m":
        setPhase(PHASES[(PHASES.indexOf(state.phase) + 1) % PHASES.length]);
        break;
      case "d":
        setDesaturate(!state.desaturate);
        break;
      case "s":
        setSnap(!state.snap);
        break;
      case "b":
        setBlind(!state.blind);
        break;
      case "a":
        ev.preventDefault();
        state.continuous.on && state.playing ? stopAll() : playAll();
        break;
      case "l":
        setOverlay(!state.links);
        break;
      case "c":
      case "Escape":
        setCapture(ev.key === "c" ? !state.capture : false);
        break;
      default:
        return;
    }
  });
  window.addEventListener("resize", () => {
    // A new window size is a new question: how the panel wraps changes with it, so the tallest
    // it was at the old size is not evidence about this one.
    controlsHeight = 0;
    layout();
  });
  // The panel's height is not a constant of the window: it changes when a webfont lands, when
  // a control appears or is taken out of the list, and when a row wraps. `layout` used to run
  // only at startup and on resize, so whichever height happened to be current at that instant
  // was the one the stage was scaled from, and a later reflow left it stale. Observing the
  // panel is what makes the layout converge instead of depending on timing.
  if (typeof ResizeObserver === "function") {
    let lastSeen = 0;
    new ResizeObserver(() => {
      const now = controls.offsetHeight;
      // Only on a real change, and never on the sub-pixel echo of our own resize: `layout`
      // resizes the stage, which can change how the panel wraps, which would call us again.
      if (now > 0 && Math.abs(now - lastSeen) >= 1) {
        lastSeen = now;
        layout();
      }
    }).observe(controls);
  }
  // Coming back to the tab is exactly when the stale zero would have been applied.
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) {
      layout();
    }
  });

  // The workbench opens on the one-step range into DEFAULT_STEP_N where the page carries that exact
  // step; the 25-pair demo build does not carry 16 -> 17, so its range clamps to the nearest step
  // it has and it opens there.
  function requireAnimationPanel() {
    if (animationPanel === null) {
      throw new Error("animation editor has not mounted");
    }
    return animationPanel;
  }
  animationPanel = workbenchBundle.animationPanel.mountAnimationPanel({
    document,
    colours: COLOUR,
    enter: () => {
      pause();
      state.optimizing = false;
      opt = null;
      setMode("animate");
    },
    restore: () => {
      select(state.pair);
    },
    reducedMotion: () => reduceMotion,
  });
  packPanel = workbenchBundle.packPanel.mountPackPanel({
    document,
    colours: COLOUR,
    reducedMotion: () => reduceMotion,
    onChange: () => requestAnimationFrame(layout),
  });
  win.packWorkbench = Object.freeze({
    configure: (options) => packPanel.configure(options),
    play: () => packPanel.play(),
    pause: () => packPanel.pause(),
    playing: () => packPanel.playing(),
    step: (count) => packPanel.step(count),
    restart: () => packPanel.restart(),
    resolve: () => packPanel.resolve(),
    load: (text) => packPanel.load(text),
    state: () => packPanel.state(),
    exportSnapshot: () => packPanel.exportSnapshot(),
  });
  searchPanel = workbenchBundle.searchPanel.mountSearchPanel({
    document,
    onChange: () => requestAnimationFrame(layout),
  });
  win.searchWorkbench = searchPanel;
  stageHandle = mountResizeHandle({
    document,
    handle: htmlNode("stage-resize"),
    position: () => stageWrap.getBoundingClientRect().height,
    bounds: stageBounds,
    place: (height) => {
      stageShare = height === null ? null : height / window.innerHeight;
      writeStageShare(stageShare);
      // Back to the automatic layout, the tallest-controls measurement starts again: the
      // height the controls were held at is not evidence about their own.
      if (stageShare === null) {
        controlsHeight = 0;
      }
      layout();
    },
    describe: (height) =>
      `stage ${Math.round((100 * height) / window.innerHeight)} percent of the window height`,
  });
  setRange(DEFAULT_STEP_N, DEFAULT_STEP_N);
  // The page opens on Animate, the aspect the owner uses most (2026-09-14), through the same
  // transition a click on its tab takes, so Pack still remembers the n it was set up on.
  setMode("animate");
  layout();
  // The scale's figure width is measured from the drawn numerals, so it has to be taken again once
  // the faces are in; re-rendering afterwards is a no-op on everything but the suppression.
  // The bar's two ends, set once: they are the same expression at every n.
  htmlNode("gapbar-area").innerHTML = METRICS.bound_html.area;
  htmlNode("gapbar-grid").innerHTML = METRICS.bound_html.grid;
  measureDigit();
  measureHeadline();
  if ("fonts" in document) {
    // `layout()` again, not only `measureDigit()`: the panel's height is what the stage's scale is
    // computed from, and with revision 11's six control boxes the faces landing changes how much the
    // rows wrap. Measured before this line: a fresh load left the controls 45 px taller than the
    // scale had allowed for and `overflow: hidden` clipped the bottom row until the window resized.
    void document.fonts.ready.then(() => {
      measureDigit();
      measureHeadline();
      layout();
      render();
    });
  }
})();
