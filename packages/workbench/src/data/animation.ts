import {
  assessPackingSnapshot,
  type PackingAssessment,
  type SquarePose,
} from "../core/runtime-contracts.ts";

export const ANIMATION_CONTRACT = "packing.squares:PackingAnimation/v1";
export const MAX_ANIMATION_SQUARES = 324;
export const MAX_ANIMATION_FRAMES = 10_000;
export const MAX_ANIMATION_PAIR_CHECKS = 5_000_000;
export type JsonValue =
  | null
  | boolean
  | number
  | string
  | JsonValue[]
  | { [key: string]: JsonValue };
type JsonObject = { [key: string]: JsonValue };

export interface AnimationFrame {
  t: number;
  side: number;
  squares: SquarePose[];
  squareIds: number[];
  locked: boolean[] | null;
  record: number | null;
  phase: string;
  label: string | null;
  /** Imported flags are claims. Admission is recomputed from geometry. */
  claimedFeasible: boolean | null;
  claimedGuided: boolean;
  guided: boolean;
  assessment: PackingAssessment;
}

export interface AnimationDocument {
  contract: typeof ANIMATION_CONTRACT;
  name: string;
  n: number;
  guided: boolean;
  source: {
    strategy: string | null;
    records: number[];
    commit: string | null;
    seed: number | null;
    configuration: JsonObject | null;
  } | null;
  durationSeconds: number | null;
  palette: {
    hue: "identity" | "angle-class" | "uniform" | null;
    shade: "none" | "full-side-contact" | "evidence" | null;
  } | null;
  reference: { bestKnown: number | null; provedLowerBound: number | null } | null;
  fairReach: FairReach[];
  frames: AnimationFrame[];
}

/**
 * What an ascent step's unguided settle reached. `fairSide` and `excessPct` are null
 * exactly when `packingValid` is false; `packingValid` is null only for a row written
 * before validity was recorded, whose side is unchecked.
 */
export interface FairReach {
  n: number;
  fairSide: number | null;
  record: number;
  excessPct: number | null;
  packingValid: boolean | null;
}

function object(
  value: unknown,
  allowed: readonly string[],
  label: string,
): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new TypeError(`${label} must be an object`);
  }
  const result: Record<string, unknown> = {};
  for (const [key, field] of Object.entries(value)) {
    if (!allowed.includes(key)) {
      throw new TypeError(`${label} has unsupported field ${key}`);
    }
    result[key] = field;
  }
  return result;
}

function array(value: unknown, label: string): unknown[] {
  if (!Array.isArray(value)) {
    throw new TypeError(`${label} must be an array`);
  }
  return value;
}

function number(value: unknown, label: string): number {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    throw new TypeError(`${label} must be finite`);
  }
  return value;
}

function positive(value: unknown, label: string): number {
  const result = number(value, label);
  if (result <= 0) {
    throw new RangeError(`${label} must be positive`);
  }
  return result;
}

function integer(value: unknown, label: string, minimum = 1): number {
  const result = number(value, label);
  if (!Number.isSafeInteger(result) || result < minimum) {
    throw new RangeError(`${label} must be an integer >= ${minimum}`);
  }
  return result;
}

function text(value: unknown, label: string): string {
  if (typeof value !== "string") {
    throw new TypeError(`${label} must be a string`);
  }
  return value;
}

function identifier(value: unknown, label: string): string {
  const result = text(value, label);
  if (result.trim().length === 0) {
    throw new TypeError(`${label} must not be empty`);
  }
  return result;
}

function boolean(value: unknown, label: string): boolean {
  if (typeof value !== "boolean") {
    throw new TypeError(`${label} must be a boolean`);
  }
  return value;
}

function jsonValue(value: unknown, depth = 0): JsonValue {
  if (depth > 32) {
    throw new RangeError("animation configuration nesting exceeds 32 levels");
  }
  if (value === null) {
    return null;
  }
  if (typeof value === "string" || typeof value === "boolean") {
    return value;
  }
  if (typeof value === "number") {
    return number(value, "configuration number");
  }
  if (Array.isArray(value)) {
    return value.map((item: unknown) => jsonValue(item, depth + 1));
  }
  if (typeof value !== "object") {
    throw new TypeError("animation configuration must be JSON");
  }
  return Object.fromEntries(
    Object.entries(value).map(([key, field]) => [key, jsonValue(field, depth + 1)]),
  );
}

function configuration(value: unknown): JsonObject {
  const result = jsonValue(value);
  if (result === null || typeof result !== "object" || Array.isArray(result)) {
    throw new TypeError("animation configuration must be a JSON object");
  }
  return result;
}

function source(value: unknown): NonNullable<AnimationDocument["source"]> {
  const row = object(value, ["strategy", "records", "commit", "seed", "configuration"], "source");
  const records =
    row.records === undefined ? [] : array(row.records, "records").map((n) => integer(n, "record"));
  if (new Set(records).size !== records.length) {
    throw new RangeError("source records must be unique");
  }
  const seed = row.seed === undefined ? null : integer(row.seed, "seed", 0);
  if (seed !== null && seed > 0xffff_ffff) {
    throw new RangeError("source seed must fit uint32");
  }
  return {
    strategy: row.strategy === undefined ? null : identifier(row.strategy, "strategy"),
    records,
    commit: row.commit === undefined ? null : identifier(row.commit, "commit"),
    seed,
    configuration: row.configuration === undefined ? null : configuration(row.configuration),
  };
}

export function decodeAnimationPose(value: unknown): SquarePose {
  const coordinates = array(value, "square pose");
  if (coordinates.length !== 3) {
    throw new RangeError("square poses require x, y and angle in radians");
  }
  return {
    x: number(coordinates[0], "square x"),
    y: number(coordinates[1], "square y"),
    angle: number(coordinates[2], "square angle in radians"),
  };
}

function frame(value: unknown, n: number, inheritedGuidance: boolean): AnimationFrame {
  const row = object(
    value,
    [
      "t",
      "side",
      "squares",
      "square_ids",
      "record",
      "locked",
      "phase",
      "guided",
      "label",
      "feasible",
    ],
    "frame",
  );
  const t = number(row.t, "logical time");
  if (t < 0 || t > 1) {
    throw new RangeError("logical time must be between zero and one");
  }
  const side = positive(row.side, "container side");
  const squares = array(row.squares, "squares").map(decodeAnimationPose);
  const squareIds =
    row.square_ids === undefined
      ? Array.from({ length: n }, (_unused, index) => index + 1)
      : array(row.square_ids, "square IDs").map((id) => integer(id, "square ID"));
  const locked =
    row.locked === undefined
      ? null
      : array(row.locked, "locked flags").map((flag) => boolean(flag, "locked flag"));
  if (
    squares.length !== n ||
    squareIds.length !== n ||
    new Set(squareIds).size !== n ||
    (locked !== null && locked.length !== n)
  ) {
    throw new RangeError("every frame must preserve n squares, unique IDs and locked flags");
  }
  const claimedGuided = row.guided === undefined ? false : boolean(row.guided, "guided");
  return {
    t,
    side,
    squares,
    squareIds,
    locked,
    record: row.record === undefined ? null : integer(row.record, "record"),
    phase: row.phase === undefined ? "frame" : identifier(row.phase, "phase"),
    label: row.label === undefined ? null : text(row.label, "label"),
    claimedFeasible: row.feasible === undefined ? null : boolean(row.feasible, "feasible"),
    claimedGuided,
    guided: inheritedGuidance || claimedGuided,
    assessment: assessPackingSnapshot(
      { squareSide: 1, container: { originX: 0, originY: 0, side }, poses: squares },
      n,
    ),
  };
}

function palette(value: unknown): NonNullable<AnimationDocument["palette"]> {
  const row = object(value, ["hue", "shade"], "palette");
  return { hue: hueScheme(row.hue), shade: shadeScheme(row.shade) };
}

function hueScheme(value: unknown): NonNullable<AnimationDocument["palette"]>["hue"] {
  if (value === undefined) {
    return null;
  }
  if (value === "identity" || value === "angle-class" || value === "uniform") {
    return value;
  }
  throw new TypeError("unsupported animation hue scheme; use scheme names when present");
}

function shadeScheme(value: unknown): NonNullable<AnimationDocument["palette"]>["shade"] {
  if (value === undefined) {
    return null;
  }
  if (value === "none" || value === "full-side-contact" || value === "evidence") {
    return value;
  }
  throw new TypeError("unsupported animation shade scheme; use scheme names when present");
}

function reference(value: unknown): NonNullable<AnimationDocument["reference"]> {
  const row = object(value, ["best_known", "proved_lower_bound"], "reference");
  return {
    bestKnown: row.best_known === undefined ? null : positive(row.best_known, "best known side"),
    provedLowerBound:
      row.proved_lower_bound === undefined ? null : positive(row.proved_lower_bound, "lower bound"),
  };
}

/** Decode the Python/browser interchange contract and independently assess every frame. */
export function decodeAnimation(value: unknown): AnimationDocument {
  const row = object(
    value,
    [
      "contract",
      "name",
      "n",
      "guided",
      "source",
      "duration_seconds",
      "palette",
      "reference",
      "fair_reach",
      "frames",
    ],
    "animation",
  );
  if (row.contract !== ANIMATION_CONTRACT) {
    throw new TypeError(
      "unsupported animation contract; use the explicit legacy adapter for unversioned input",
    );
  }
  const name = text(row.name, "animation name");
  if (!name.length) {
    throw new RangeError("animation name must be nonempty");
  }
  const n = integer(row.n, "animation n");
  if (n > MAX_ANIMATION_SQUARES) {
    throw new RangeError(`browser animations support at most ${MAX_ANIMATION_SQUARES} squares`);
  }
  const guided = row.guided === undefined ? false : boolean(row.guided, "guided");
  const ancestry = row.source === undefined ? null : source(row.source);
  let inheritedGuidance = guided || (ancestry !== null && ancestry.records.length > 0);
  let previousTime = -1;
  let stableIds: readonly number[] | null = null;
  const rawFrames = array(row.frames, "frames");
  if (rawFrames.length > MAX_ANIMATION_FRAMES) {
    throw new RangeError(`browser animations support at most ${MAX_ANIMATION_FRAMES} frames`);
  }
  if ((rawFrames.length * n * (n - 1)) / 2 > MAX_ANIMATION_PAIR_CHECKS) {
    throw new RangeError("animation exceeds the browser geometry-check budget; reduce its frames");
  }
  const frames = rawFrames.map((value) => {
    const next = frame(value, n, inheritedGuidance);
    if (next.t < previousTime) {
      throw new RangeError("animation times must be nondecreasing");
    }
    if (stableIds?.some((id, index) => id !== next.squareIds[index])) {
      throw new RangeError("animation square identities must remain stable");
    }
    previousTime = next.t;
    stableIds = next.squareIds;
    inheritedGuidance = next.guided;
    return next;
  });
  if (frames.length === 0) {
    throw new RangeError("animation needs at least one frame");
  }
  const fairReach =
    row.fair_reach === undefined
      ? []
      : array(row.fair_reach, "fair reach").map((value): FairReach => {
          const item = object(
            value,
            ["n", "fair_side", "record", "excess_pct", "packing_valid"],
            "fair reach",
          );
          const packingValid =
            item.packing_valid === undefined ? null : boolean(item.packing_valid, "fair validity");
          const reach = {
            n: integer(item.n, "fair reach n"),
            record: positive(item.record, "fair reference"),
            packingValid,
          };
          if (packingValid === false) {
            if (item.fair_side !== null || item.excess_pct !== null) {
              throw new TypeError("a fair-reach settle that is not a packing reached no side");
            }
            return { ...reach, fairSide: null, excessPct: null };
          }
          return {
            ...reach,
            fairSide: positive(item.fair_side, "fair side"),
            excessPct: number(item.excess_pct, "fair excess"),
          };
        });
  return {
    contract: ANIMATION_CONTRACT,
    name,
    n,
    guided,
    source: ancestry,
    durationSeconds:
      row.duration_seconds === undefined ? null : positive(row.duration_seconds, "duration"),
    palette: row.palette === undefined ? null : palette(row.palette),
    reference: row.reference === undefined ? null : reference(row.reference),
    fairReach,
    frames,
  };
}

export function decodeLegacyAnimation(value: unknown): AnimationDocument {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new TypeError("legacy animation must be an object");
  }
  return decodeAnimation({ contract: ANIMATION_CONTRACT, ...value });
}

function sourceValue(value: NonNullable<AnimationDocument["source"]>): JsonObject {
  return {
    records: value.records,
    ...(value.strategy === null ? {} : { strategy: value.strategy }),
    ...(value.commit === null ? {} : { commit: value.commit }),
    ...(value.seed === null ? {} : { seed: value.seed }),
    ...(value.configuration === null ? {} : { configuration: value.configuration }),
  };
}

/** Export preserves effective ancestry even when an editor removes an earlier guide frame. */
export function encodeAnimation(document: AnimationDocument): string {
  const row: JsonObject = {
    contract: ANIMATION_CONTRACT,
    name: document.name,
    n: document.n,
    guided: document.guided,
    frames: document.frames.map((frame) => ({
      t: frame.t,
      side: frame.side,
      squares: frame.squares.map(({ x, y, angle }) => [x, y, angle]),
      square_ids: frame.squareIds,
      phase: frame.phase,
      guided: frame.guided,
      ...(frame.claimedFeasible === null ? {} : { feasible: frame.claimedFeasible }),
      ...(frame.record === null ? {} : { record: frame.record }),
      ...(frame.locked === null ? {} : { locked: frame.locked }),
      ...(frame.label === null ? {} : { label: frame.label }),
    })),
    ...(document.source === null ? {} : { source: sourceValue(document.source) }),
    ...(document.durationSeconds === null ? {} : { duration_seconds: document.durationSeconds }),
    ...(document.palette === null
      ? {}
      : {
          palette: {
            ...(document.palette.hue === null ? {} : { hue: document.palette.hue }),
            ...(document.palette.shade === null ? {} : { shade: document.palette.shade }),
          },
        }),
    ...(document.reference === null
      ? {}
      : {
          reference: {
            ...(document.reference.bestKnown === null
              ? {}
              : { best_known: document.reference.bestKnown }),
            ...(document.reference.provedLowerBound === null
              ? {}
              : { proved_lower_bound: document.reference.provedLowerBound }),
          },
        }),
    ...(document.fairReach.length === 0
      ? {}
      : {
          fair_reach: document.fairReach.map((item) => ({
            n: item.n,
            fair_side: item.fairSide,
            record: item.record,
            excess_pct: item.excessPct,
            ...(item.packingValid === null ? {} : { packing_valid: item.packingValid }),
          })),
        }),
  };
  // Validate before JSON.stringify could silently turn a nonfinite edited value into null.
  decodeAnimation(row);
  return `${JSON.stringify(row, null, 2)}\n`;
}
