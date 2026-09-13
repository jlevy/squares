import type { AtlasPairKind, AtlasPhase, AtlasTiming } from "../api/workbench-api.js";

export const CORPUS_SCHEMA = "squares.workbench.corpus/v1";
export type CorpusSquare = [number, number, number, string, number];
export interface CorpusFrame {
  side: number;
  /** Catalogue poses are lower-left centred, with angles in degrees. */
  squares: CorpusSquare[];
  ident: number[];
}
export interface CorpusBlock {
  members: number[];
  riders: number[];
  cluster: number;
  turn: number;
  from: [number, number];
  to: [number, number];
  drift_max: number;
}
export interface CorpusPair {
  n: number;
  kind: AtlasPairKind;
  map: number[];
  new: number;
  new_rule: string;
  new_tied: number;
  blocks: CorpusBlock[];
  block_of: number[];
  prev_new: number | null;
  stats: Record<string, number>;
}
export interface CorpusFacts {
  relation: string;
  side: string;
  exact: string | null;
  exact_state: string;
  degree: number | null;
  status: string;
  lower: string | null;
  kind: string;
  badges: { glyph: string; style: string; meaning: string }[];
  star: boolean;
  open: string[];
  html_side: string | null;
  html_lower: string | null;
  html_headline: string | null;
  html_exact: string | null;
}
export interface CorpusMetrics {
  type_scale: number[];
  numeral_px: number;
  numeral_weight: number;
  n_line_px: number;
  headline_gap_px: number;
  bound_html: { area: string; grid: string };
  digit_bearing_px: number;
  n_bearing_px: number;
  badge_baseline: { letter: number; math: number; query: number };
  approx: {
    d: string;
    advance: number;
    y0: number;
    y1: number;
    font_size: number;
    stroke_units: number;
  };
  star_inset: number;
  star_span: number;
}
export interface CorpusColour {
  palette: string[];
  shades: string[][];
  /** Workbench angle clustering, separate from exact rendering's angle tolerance. */
  angleToleranceDegrees: number;
}
export interface Corpus {
  schema: typeof CORPUS_SCHEMA;
  frames: Record<string, CorpusFrame>;
  pairs: CorpusPair[];
  facts: Record<string, CorpusFacts>;
  timing: AtlasTiming;
  arrival_fraction: number;
  motion_phases: AtlasPhase[];
  n_max: number;
  metrics: CorpusMetrics;
  star_points: [number, number][];
  sequence_kinds: Record<string, AtlasPairKind>;
  colour: CorpusColour;
}

function isObject(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}
function object(value: unknown, label: string): Record<string, unknown> {
  if (!isObject(value)) {
    throw new TypeError(`${label} must be an object`);
  }
  return value;
}
function string(value: unknown): string {
  if (typeof value !== "string") {
    throw new TypeError("corpus text must be a string");
  }
  return value;
}
function numeric(value: unknown): number {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    throw new TypeError("corpus numbers must be finite");
  }
  return value;
}
function integer(value: unknown, minimum = 0): number {
  const number = numeric(value);
  if (!Number.isSafeInteger(number) || number < minimum) {
    throw new RangeError(`corpus integer must be >= ${minimum}`);
  }
  return number;
}
function positive(value: unknown): number {
  const number = numeric(value);
  if (number <= 0) {
    throw new RangeError("corpus dimension must be positive");
  }
  return number;
}
function boolean(value: unknown): boolean {
  if (typeof value !== "boolean") {
    throw new TypeError("corpus flags must be explicit booleans");
  }
  return value;
}
function nullable<T>(value: unknown, read: (value: unknown) => T): T | null {
  return value === null ? null : read(value);
}
function array<T>(value: unknown, read: (value: unknown) => T): T[] {
  if (!Array.isArray(value)) {
    throw new TypeError("corpus list must be an array");
  }
  return value.map((item: unknown) => read(item));
}
function record<T>(value: unknown, read: (value: unknown, key: string) => T): Record<string, T> {
  return Object.fromEntries(
    Object.entries(object(value, "record")).map(([key, item]) => [key, read(item, key)]),
  );
}
function point(value: unknown): [number, number] {
  const numbers = array(value, numeric);
  const [x, y] = numbers;
  if (numbers.length !== 2 || x === undefined || y === undefined) {
    throw new RangeError("corpus point must have two coordinates");
  }
  return [x, y];
}
function pairKind(value: unknown): AtlasPairKind {
  if (value === "matched" || value === "prefix" || value === "shared-picture") {
    return value;
  }
  throw new RangeError("unknown corpus transition kind");
}
function phase(value: unknown): AtlasPhase {
  if (
    value === "add-then-move" ||
    value === "move-then-add" ||
    value === "simultaneous" ||
    value === "rotate-first" ||
    value === "slide-first"
  ) {
    return value;
  }
  throw new RangeError("unknown corpus motion phase");
}
function square(value: unknown): CorpusSquare {
  if (!Array.isArray(value) || value.length !== 5) {
    throw new TypeError("catalogue square requires x, y, degrees, fill and contact count");
  }
  return [
    numeric(value[0]),
    numeric(value[1]),
    numeric(value[2]),
    string(value[3]),
    integer(value[4]),
  ];
}
function frame(value: unknown, key: string): CorpusFrame {
  const row = object(value, "frame");
  const count = integer(Number(key), 1);
  const squares = array(row.squares, square);
  const ident = array(row.ident, (value) => integer(value, 1));
  if (
    squares.length !== count ||
    ident.length !== count ||
    new Set(ident).size !== count ||
    ident.some((id) => id > count)
  ) {
    throw new RangeError(`frame ${key} must retain exactly its declared squares and identities`);
  }
  return { side: positive(row.side), squares, ident };
}
function block(value: unknown): CorpusBlock {
  const row = object(value, "block");
  return {
    members: array(row.members, integer),
    riders: array(row.riders, integer),
    cluster: integer(row.cluster),
    turn: numeric(row.turn),
    from: point(row.from),
    to: point(row.to),
    drift_max: numeric(row.drift_max),
  };
}
function pair(value: unknown): CorpusPair {
  const row = object(value, "pair");
  return {
    n: integer(row.n, 1),
    kind: pairKind(row.kind),
    map: array(row.map, integer),
    new: integer(row.new),
    new_rule: string(row.new_rule),
    new_tied: integer(row.new_tied),
    blocks: array(row.blocks, block),
    block_of: array(row.block_of, (value) => integer(value, -1)),
    prev_new: nullable(row.prev_new, integer),
    stats: record(row.stats, numeric),
  };
}
function facts(value: unknown): CorpusFacts {
  const row = object(value, "facts");
  return {
    relation: string(row.relation),
    side: string(row.side),
    exact: nullable(row.exact, string),
    exact_state: string(row.exact_state),
    degree: nullable(row.degree, integer),
    status: string(row.status),
    lower: nullable(row.lower, string),
    kind: string(row.kind),
    badges: array(row.badges, (value) => {
      const badge = object(value, "badge");
      return {
        glyph: string(badge.glyph),
        style: string(badge.style),
        meaning: string(badge.meaning),
      };
    }),
    star: boolean(row.star),
    open: array(row.open, string),
    html_side: nullable(row.html_side, string),
    html_lower: nullable(row.html_lower, string),
    html_headline: nullable(row.html_headline, string),
    html_exact: nullable(row.html_exact, string),
  };
}
function metrics(value: unknown): CorpusMetrics {
  const row = object(value, "metrics");
  const bound = object(row.bound_html, "bound html");
  const badge = object(row.badge_baseline, "badge baselines");
  const approx = object(row.approx, "approximation glyph");
  return {
    type_scale: array(row.type_scale, positive),
    numeral_px: positive(row.numeral_px),
    numeral_weight: positive(row.numeral_weight),
    n_line_px: positive(row.n_line_px),
    headline_gap_px: numeric(row.headline_gap_px),
    bound_html: { area: string(bound.area), grid: string(bound.grid) },
    digit_bearing_px: numeric(row.digit_bearing_px),
    n_bearing_px: numeric(row.n_bearing_px),
    badge_baseline: {
      letter: numeric(badge.letter),
      math: numeric(badge.math),
      query: numeric(badge.query),
    },
    approx: {
      d: string(approx.d),
      advance: positive(approx.advance),
      y0: numeric(approx.y0),
      y1: numeric(approx.y1),
      font_size: positive(approx.font_size),
      stroke_units: numeric(approx.stroke_units),
    },
    star_inset: positive(row.star_inset),
    star_span: positive(row.star_span),
  };
}
function colour(value: unknown): CorpusColour {
  const row = object(value, "colour");
  const palette = array(row.palette, string);
  const shades = array(row.shades, (value) => array(value, string));
  if (
    palette.length < 3 ||
    shades.length !== palette.length ||
    shades.some((family) => family.length !== 5)
  ) {
    throw new RangeError("corpus palette requires matching five-shade families");
  }
  if ([...palette, ...shades.flat()].some((fill) => !/^#[0-9a-f]{6}$/i.test(fill))) {
    throw new RangeError("corpus palette must contain hexadecimal RGB fills");
  }
  return { palette, shades, angleToleranceDegrees: positive(row.angleToleranceDegrees) };
}

/** Decode the build payload once. Geometry/evidence validation remains a separate contract. */
export function decodeCorpus(value: unknown): Corpus {
  const row = object(value, "corpus");
  if (row.schema !== CORPUS_SCHEMA) {
    throw new RangeError(`unsupported corpus schema; expected ${CORPUS_SCHEMA}`);
  }
  const timing = object(row.timing, "timing");
  const corpus: Corpus = {
    schema: CORPUS_SCHEMA,
    frames: record(row.frames, frame),
    pairs: array(row.pairs, pair),
    facts: record(row.facts, facts),
    timing: {
      dwell: numeric(timing.dwell),
      move: numeric(timing.move),
      correct: numeric(timing.correct),
      settle: numeric(timing.settle),
    },
    arrival_fraction: numeric(row.arrival_fraction),
    motion_phases: array(row.motion_phases, phase),
    n_max: integer(row.n_max, 1),
    metrics: metrics(row.metrics),
    star_points: array(row.star_points, point),
    sequence_kinds: record(row.sequence_kinds, pairKind),
    colour: colour(row.colour),
  };
  if (
    Object.values(corpus.timing).some((span) => span < 0) ||
    corpus.arrival_fraction < 0 ||
    corpus.arrival_fraction > 1 ||
    corpus.motion_phases.length === 0
  ) {
    throw new RangeError("corpus timing and arrival intervals must be bounded");
  }
  let previous = 0;
  for (const transition of corpus.pairs) {
    if (transition.n <= previous || transition.n + 1 > corpus.n_max) {
      throw new RangeError("corpus pairs must be ordered, unique, and within n_max");
    }
    previous = transition.n;
    const source = frameAt(corpus, transition.n);
    const target = frameAt(corpus, transition.n + 1);
    if (
      transition.map.length !== transition.n ||
      transition.new > transition.n ||
      new Set([...transition.map, transition.new]).size !== transition.n + 1 ||
      transition.map.some((index) => index > transition.n) ||
      transition.block_of.length !== transition.n
    ) {
      throw new RangeError("corpus transition must map every identity once and add one square");
    }
    if (
      target.ident[transition.new] !== transition.n + 1 ||
      transition.map.some((index, from) => target.ident[index] !== source.ident[from])
    ) {
      throw new RangeError("corpus transition must preserve stable identities");
    }
    if (
      corpus.facts[String(transition.n)] === undefined ||
      corpus.facts[String(transition.n + 1)] === undefined
    ) {
      throw new RangeError("corpus transition facts are incomplete");
    }
    for (const [index, group] of transition.blocks.entries()) {
      const members = [...group.members, ...group.riders];
      if (
        new Set(members).size !== members.length ||
        members.some((member) => member >= transition.n || transition.block_of[member] !== index)
      ) {
        throw new RangeError("corpus block membership must match its source-square index");
      }
    }
    if (transition.block_of.some((index) => index >= transition.blocks.length)) {
      throw new RangeError("corpus block index is outside the declared blocks");
    }
    for (const [square, blockIndex] of transition.block_of.entries()) {
      if (blockIndex < 0) {
        continue;
      }
      const group = transition.blocks[blockIndex];
      if (
        group === undefined ||
        !(group.members.includes(square) || group.riders.includes(square))
      ) {
        throw new RangeError("corpus block index must have a matching member or rider");
      }
    }
    for (const key of ["max_displacement", "rotated", "block_count"]) {
      numeric(transition.stats[key]);
    }
  }
  if (corpus.pairs.length === 0) {
    throw new RangeError("corpus requires at least one transition");
  }
  return corpus;
}

export function frameAt(corpus: Corpus, n: number): CorpusFrame {
  const frame = corpus.frames[String(n)];
  if (frame === undefined) {
    throw new RangeError(`corpus has no frame for n=${n}`);
  }
  return frame;
}
export function pairAt(corpus: Corpus, index: number): CorpusPair {
  const pair = corpus.pairs[index];
  if (pair === undefined) {
    throw new RangeError(`corpus has no transition at index ${index}`);
  }
  return pair;
}

export const corpusData = Object.freeze({ decodeCorpus, frameAt, pairAt });
