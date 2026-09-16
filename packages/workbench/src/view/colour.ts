import type { AtlasAspect, AtlasPaintScheme, AtlasScheme } from "../api/workbench-api.js";
import type { GeometryReceipt } from "../core/geometry.js";
import type { CorpusColour } from "../data/corpus.js";
import type { SceneFrame } from "./scene-types.js";

const QUARTER_TURN_DEGREES = 90;
const GREEN_BAND = [109.4, 174.6] as const;
const GREEN_ROWS = [
  [0.54, 0.106, 5],
  [0.586, 0.118, 5],
  [0.632, 0.126, 5],
  [0.678, 0.13, 5],
  [0.724, 0.13, 5],
  [0.77, 0.128, 5],
  [0.816, 0.12, 5],
  [0.862, 0.104, 4],
  [0.906, 0.08, 3],
] as const;
const RAMP_ENDS = [
  [0.662, 0.1189, 174.6],
  [0.799, 0.1244, 109.4],
] as const;
const GREEN_STRIDE = 29;
const MOVING_SHADE = 2;
const COLOUR_SCHEMES: readonly AtlasScheme[] = ["identity", "angle-stable", "angle-continuous"];

type Lab = readonly [number, number, number];

export interface AngleMap {
  classes: number;
  centres: number[];
  slots: number[];
  sizes: number[];
  slotOf(angleDegrees: number): number;
}

export interface ColourReferenceFrame {
  anglesDegrees: readonly number[];
  contacts: readonly number[];
}

export interface SceneColourState {
  scheme: AtlasScheme;
  mode: AtlasAspect;
  animateStandardize: boolean;
  stageChroma: number;
  desaturationFloor: number;
  scarlet: string;
  tintChroma: number;
  restSource: ColourReferenceFrame | null;
  restTarget: ColourReferenceFrame | null;
  holdsColour: ArrayLike<number> | null;
  movingSlots: ArrayLike<number> | null;
}

export interface SceneColourReceipt {
  fills: string[];
  scheme: AtlasPaintScheme;
  classes: number;
  centres: number[];
  sizes: number[];
  slots: number[];
  contacts: number[];
  overlap: number;
  deepestOverlap: number;
  overlapPairs: number;
  /** Flat index pairs copied from the geometry receipt. */
  contactEdges: number[];
  /** Pair keys encoded as `low * squareCount + high`. */
  touching: ReadonlySet<number>;
}

export interface ColourSystem {
  readonly palette: readonly string[];
  readonly shades: readonly (readonly string[])[];
  readonly angleToleranceDegrees: number;
  readonly greens: readonly string[];
  readonly greenStride: number;
  readonly schemes: readonly AtlasScheme[];
  foldAngle(angleDegrees: number): number;
  angleGap(leftDegrees: number, rightDegrees: number): number;
  slotForAngle(angleDegrees: number): number;
  buildAngleMap(anglesDegrees: readonly number[]): AngleMap;
  buildAtlasMap(anglesDegrees: readonly number[]): AngleMap;
  angleFills(anglesDegrees: readonly number[], contacts?: readonly number[]): string[];
  atlasFills(anglesDegrees: readonly number[], contacts?: readonly number[]): string[];
  identityFill(identity: number): string;
  identityFills(count?: number): string[];
  mix(left: string, right: string, progress: number): string;
  desaturate(hex: string, level: number, floor: number): string;
  trim(hex: string, chroma: number): string;
  schemeFor(
    scheme: AtlasScheme,
    mode: AtlasAspect,
    animateStandardize: boolean,
    restProgress: number,
  ): AtlasPaintScheme;
  paintScene(
    scene: SceneFrame,
    geometry: GeometryReceipt,
    state: SceneColourState,
  ): SceneColourReceipt;
}

function itemAt<T>(items: ArrayLike<T>, index: number, name: string): T {
  const item = items[index];
  if (item === undefined) {
    throw new RangeError(`${name} has no item at index ${index}`);
  }
  return item;
}

function finite(value: number, name: string): void {
  if (!Number.isFinite(value)) {
    throw new RangeError(`${name} must be finite`);
  }
}

function fraction(value: number, name: string): void {
  finite(value, name);
  if (value < 0 || value > 1) {
    throw new RangeError(`${name} must be between zero and one`);
  }
}

function checkedHex(value: string): string {
  if (!/^#[0-9a-f]{6}$/i.test(value)) {
    throw new TypeError(`invalid six-digit colour: ${value}`);
  }
  return value.toLowerCase();
}

function clamp01(value: number): number {
  return Math.max(0, Math.min(1, value));
}

function lerp(left: number, right: number, progress: number): number {
  return left + (right - left) * progress;
}

function foldAngle(angleDegrees: number): number {
  finite(angleDegrees, "angle");
  return ((angleDegrees % QUARTER_TURN_DEGREES) + QUARTER_TURN_DEGREES) % QUARTER_TURN_DEGREES;
}

function angleGap(leftDegrees: number, rightDegrees: number): number {
  const distance = Math.abs(foldAngle(leftDegrees) - foldAngle(rightDegrees));
  return Math.min(distance, QUARTER_TURN_DEGREES - distance);
}

function linearToSrgb(value: number): number {
  return value <= 0.003_130_8 ? 12.92 * value : 1.055 * value ** (1 / 2.4) - 0.055;
}

function srgbToLinear(value: number): number {
  return value <= 0.040_45 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
}

function labToLinear(lightness: number, a: number, b: number): Lab {
  const long = (lightness + 0.396_337_777_4 * a + 0.215_803_757_3 * b) ** 3;
  const medium = (lightness - 0.105_561_345_8 * a - 0.063_854_172_8 * b) ** 3;
  const short = (lightness - 0.089_484_177_5 * a - 1.291_485_548 * b) ** 3;
  return [
    4.076_741_662_1 * long - 3.307_711_591_3 * medium + 0.230_969_929_2 * short,
    -1.268_438_004_6 * long + 2.609_757_401_1 * medium - 0.341_319_396_5 * short,
    -0.004_196_086_3 * long - 0.703_418_614_7 * medium + 1.707_614_701 * short,
  ];
}

function hexChannel(value: number): string {
  const encoded = Math.max(
    0,
    Math.min(255, Math.round(linearToSrgb(Math.max(0, Math.min(1, value))) * 255)),
  );
  return encoded.toString(16).padStart(2, "0");
}

function labToHex(lightness: number, a: number, b: number): string {
  const rgb = labToLinear(lightness, a, b);
  return `#${hexChannel(rgb[0])}${hexChannel(rgb[1])}${hexChannel(rgb[2])}`;
}

function inGamut(lightness: number, chroma: number, hue: number): boolean {
  const rgb = labToLinear(lightness, chroma * Math.cos(hue), chroma * Math.sin(hue));
  return rgb.every((value) => value >= -0.0001 && value <= 1.0001);
}

function oklchHex(lightness: number, chromaValue: number, hueDegrees: number): string {
  const hue = (hueDegrees * Math.PI) / 180;
  let chroma = chromaValue;
  if (!inGamut(lightness, chroma, hue)) {
    let low = 0;
    let high = chroma;
    for (let iteration = 0; iteration < 14; iteration += 1) {
      const middle = (low + high) / 2;
      if (inGamut(lightness, middle, hue)) {
        low = middle;
      } else {
        high = middle;
      }
    }
    chroma = low;
  }
  return labToHex(lightness, chroma * Math.cos(hue), chroma * Math.sin(hue));
}

function hexToLab(hexValue: string): Lab {
  const hex = checkedHex(hexValue);
  const red = srgbToLinear(Number.parseInt(hex.slice(1, 3), 16) / 255);
  const green = srgbToLinear(Number.parseInt(hex.slice(3, 5), 16) / 255);
  const blue = srgbToLinear(Number.parseInt(hex.slice(5, 7), 16) / 255);
  const long = Math.cbrt(0.412_221_470_8 * red + 0.536_332_536_3 * green + 0.051_445_992_9 * blue);
  const medium = Math.cbrt(
    0.211_903_498_2 * red + 0.680_699_545_1 * green + 0.107_396_956_6 * blue,
  );
  const short = Math.cbrt(0.088_302_461_9 * red + 0.281_718_837_6 * green + 0.629_978_700_5 * blue);
  return [
    0.210_454_255_3 * long + 0.793_617_785 * medium - 0.004_072_046_8 * short,
    1.977_998_495_1 * long - 2.428_592_205 * medium + 0.450_593_709_9 * short,
    0.025_904_037_1 * long + 0.782_771_766_2 * medium - 0.808_675_766 * short,
  ];
}

function paletteCopy(config: CorpusColour): {
  palette: string[];
  shades: string[][];
  angleToleranceDegrees: number;
} {
  if (config.palette.length < 3) {
    throw new RangeError("the colour palette needs two pinned families and one free family");
  }
  finite(config.angleToleranceDegrees, "angle tolerance");
  if (config.angleToleranceDegrees < 0 || config.angleToleranceDegrees >= 45) {
    throw new RangeError("angle tolerance must be between zero and 45 degrees");
  }
  const palette = config.palette.map(checkedHex);
  if (config.shades.length !== palette.length) {
    throw new RangeError("every palette family needs one shade family");
  }
  const shades = config.shades.map((family) => {
    if (family.length !== 5) {
      throw new RangeError("each palette family must contain five contact shades");
    }
    return family.map(checkedHex);
  });
  return { palette, shades, angleToleranceDegrees: config.angleToleranceDegrees };
}

/** Build immutable colour behavior from the palette emitted with the corpus. */
export function createColourSystem(config: CorpusColour): ColourSystem {
  const copied = paletteCopy(config);
  const { palette, shades, angleToleranceDegrees } = copied;
  const labCache = new Map<string, Lab>();
  const toLab = (hex: string): Lab => {
    const normalized = checkedHex(hex);
    const cached = labCache.get(normalized);
    if (cached !== undefined) {
      return cached;
    }
    const converted = hexToLab(normalized);
    labCache.set(normalized, converted);
    return converted;
  };
  const mix = (left: string, right: string, progressValue: number): string => {
    const progress = clamp01(progressValue);
    if (progress <= 0) {
      return checkedHex(left);
    }
    if (progress >= 1) {
      return checkedHex(right);
    }
    const from = toLab(left);
    const to = toLab(right);
    return labToHex(
      lerp(from[0], to[0], progress),
      lerp(from[1], to[1], progress),
      lerp(from[2], to[2], progress),
    );
  };
  const desaturate = (hex: string, levelValue: number, floor: number): string => {
    const level = clamp01(levelValue);
    fraction(floor, "desaturation floor");
    if (level <= 0) {
      return checkedHex(hex);
    }
    const lab = toLab(hex);
    const chroma = 1 - (1 - floor) * level;
    return labToHex(lab[0], lab[1] * chroma, lab[2] * chroma);
  };
  const trim = (hex: string, chroma: number): string => {
    fraction(chroma, "stage chroma");
    if (chroma >= 1) {
      return checkedHex(hex);
    }
    const lab = toLab(hex);
    return labToHex(lab[0], lab[1] * chroma, lab[2] * chroma);
  };
  const freeSlots = palette.length - 2;
  const slotBand = QUARTER_TURN_DEGREES / freeSlots;
  const slotForAngle = (angleDegrees: number): number => {
    const angle = foldAngle(angleDegrees);
    if (angleGap(angle, 0) <= angleToleranceDegrees) {
      return 0;
    }
    if (angleGap(angle, 45) <= angleToleranceDegrees) {
      return 1;
    }
    const band = Math.floor(angle / slotBand);
    return 2 + Math.max(0, Math.min(freeSlots - 1, band));
  };
  const buildAngleMap = (anglesDegrees: readonly number[]): AngleMap => {
    const representatives: number[] = [];
    const sums: number[] = [];
    const counts: number[] = [];
    for (const rawAngle of anglesDegrees) {
      const angle = foldAngle(rawAngle);
      let match = -1;
      for (let index = 0; index < representatives.length; index += 1) {
        if (
          angleGap(angle, itemAt(representatives, index, "angle representatives")) <=
          angleToleranceDegrees
        ) {
          match = index;
          break;
        }
      }
      if (match < 0) {
        representatives.push(angle);
        sums.push(0);
        counts.push(1);
        continue;
      }
      const representative = itemAt(representatives, match, "angle representatives");
      let difference = angle - representative;
      if (difference > 45) {
        difference -= 90;
      } else if (difference < -45) {
        difference += 90;
      }
      sums[match] = itemAt(sums, match, "angle sums") + difference;
      counts[match] = itemAt(counts, match, "angle counts") + 1;
    }
    const centres = representatives.map((representative, index) =>
      foldAngle(
        representative + itemAt(sums, index, "angle sums") / itemAt(counts, index, "angle counts"),
      ),
    );
    const slots = centres.map(slotForAngle);
    const slotOf = (rawAngle: number): number => {
      const angle = foldAngle(rawAngle);
      for (let index = 0; index < centres.length; index += 1) {
        if (angleGap(angle, itemAt(centres, index, "angle centres")) <= angleToleranceDegrees) {
          return itemAt(slots, index, "angle slots");
        }
      }
      return slotForAngle(angle);
    };
    return {
      classes: centres.length,
      centres,
      slots,
      sizes: [...counts],
      slotOf,
    };
  };
  const buildAtlasMap = (anglesDegrees: readonly number[]): AngleMap => {
    const base = buildAngleMap(anglesDegrees);
    const unpinned: number[] = [];
    const slots: number[] = base.centres.map((centre, index) => {
      if (angleGap(centre, 0) <= angleToleranceDegrees) {
        return 0;
      }
      if (angleGap(centre, 45) <= angleToleranceDegrees) {
        return 1;
      }
      unpinned.push(index);
      return -1;
    });
    unpinned.sort(
      (left, right) =>
        itemAt(base.sizes, right, "angle sizes") - itemAt(base.sizes, left, "angle sizes") ||
        left - right,
    );
    for (const [position, index] of unpinned.entries()) {
      slots[index] = 2 + (position % freeSlots);
    }
    const slotOf = (rawAngle: number): number => {
      const angle = foldAngle(rawAngle);
      for (let index = 0; index < base.centres.length; index += 1) {
        if (
          angleGap(angle, itemAt(base.centres, index, "angle centres")) <= angleToleranceDegrees
        ) {
          return itemAt(slots, index, "atlas slots");
        }
      }
      return slotForAngle(angle);
    };
    return { ...base, slots, slotOf };
  };
  const shadeForContacts = (contacts: number): number => {
    const count = Math.round(Number.isFinite(contacts) ? contacts : 0);
    return count <= 0 ? 4 : count >= 4 ? 0 : 4 - count;
  };
  const fillFor = (slot: number, contacts: number): string => {
    const familyIndex = ((slot % shades.length) + shades.length) % shades.length;
    return itemAt(
      itemAt(shades, familyIndex, "shade families"),
      shadeForContacts(contacts),
      "shades",
    );
  };
  const mappedFills = (
    anglesDegrees: readonly number[],
    contacts: readonly number[],
    map: AngleMap,
  ): string[] =>
    anglesDegrees.map((angle, index) =>
      fillFor(map.slotOf(angle), contacts[index] === undefined ? 0 : contacts[index]),
    );
  const angleFills = (
    anglesDegrees: readonly number[],
    contacts: readonly number[] = [],
  ): string[] => mappedFills(anglesDegrees, contacts, buildAngleMap(anglesDegrees));
  const atlasFills = (
    anglesDegrees: readonly number[],
    contacts: readonly number[] = [],
  ): string[] => mappedFills(anglesDegrees, contacts, buildAtlasMap(anglesDegrees));
  const greens: string[] = [];
  for (const [rowIndex, row] of GREEN_ROWS.entries()) {
    const [lightness, chroma, slots] = row;
    const step = (GREEN_BAND[1] - GREEN_BAND[0]) / slots;
    for (let slot = 0; slot < slots; slot += 1) {
      const hue = GREEN_BAND[0] + step * (slot + 0.5) + (rowIndex % 2 === 1 ? step / 2 : 0);
      greens.push(oklchHex(lightness, chroma, Math.min(GREEN_BAND[1], hue)));
    }
  }
  const identityFill = (identity: number): string => {
    finite(identity, "square identity");
    const index = Math.round(identity || 0) - 1;
    const wrapped = (((index * GREEN_STRIDE) % greens.length) + greens.length) % greens.length;
    return itemAt(greens, wrapped, "identity greens");
  };
  const identityFills = (countValue = greens.length): string[] => {
    const count = Math.max(1, Math.round(Number.isFinite(countValue) ? countValue : greens.length));
    return Array.from({ length: count }, (_unused, index) => identityFill(index + 1));
  };
  const rampFill = (angleDegrees: number): string => {
    const angle = foldAngle(angleDegrees);
    const progress = angle <= 45 ? angle / 45 : (90 - angle) / 45;
    const from = RAMP_ENDS[0];
    const to = RAMP_ENDS[1];
    return oklchHex(
      lerp(from[0], to[0], progress),
      lerp(from[1], to[1], progress),
      lerp(from[2], to[2], progress),
    );
  };
  const fillOf = (
    scheme: AtlasPaintScheme,
    map: AngleMap,
    identity: number,
    angleDegrees: number,
    contacts: number,
  ): string => {
    if (scheme === "identity") {
      return identityFill(identity);
    }
    if (scheme === "angle-continuous") {
      return rampFill(angleDegrees);
    }
    return fillFor(map.slotOf(angleDegrees), contacts);
  };
  const schemeFor = (
    scheme: AtlasScheme,
    mode: AtlasAspect,
    animateStandardize: boolean,
    restProgress: number,
  ): AtlasPaintScheme => {
    if (scheme !== "identity") {
      return scheme;
    }
    return mode === "animate" && animateStandardize && restProgress >= 1 - 1e-9
      ? "angle-atlas"
      : "identity";
  };
  const referenceFill = (reference: ColourReferenceFrame, map: AngleMap, index: number): string => {
    const angle = itemAt(reference.anglesDegrees, index, "reference angles");
    const contacts = itemAt(reference.contacts, index, "reference contacts");
    return fillFor(map.slotOf(angle), contacts);
  };
  const paintScene = (
    scene: SceneFrame,
    geometry: GeometryReceipt,
    state: SceneColourState,
  ): SceneColourReceipt => {
    if (scene.squares.length !== geometry.contacts.length) {
      throw new RangeError("colour geometry must cover every scene square");
    }
    fraction(scene.presentation.drain, "scene drain");
    fraction(scene.presentation.newTint, "scene tint");
    fraction(scene.presentation.resting, "scene rest progress");
    fraction(state.stageChroma, "stage chroma");
    fraction(state.desaturationFloor, "desaturation floor");
    fraction(state.tintChroma, "tint chroma");
    const angles = scene.squares.map((square) => square.angleDegrees);
    const liveMap = buildAngleMap(angles);
    const standardizing =
      state.scheme === "identity" && state.mode === "animate" && state.animateStandardize;
    const standard = standardizing ? scene.presentation.resting : 0;
    const currentAtlasMap = standardizing ? buildAtlasMap(angles) : null;
    const sourceMap =
      state.restSource === null ? null : buildAtlasMap(state.restSource.anglesDegrees);
    const targetMap =
      state.restTarget === null ? null : buildAtlasMap(state.restTarget.anglesDegrees);
    const scarletLab = toLab(state.scarlet);
    const scarletFill = labToHex(
      scarletLab[0],
      scarletLab[1] * state.tintChroma,
      scarletLab[2] * state.tintChroma,
    );
    const fills = scene.squares.map((square, index) => {
      const contacts = itemAt(geometry.contacts, index, "geometry contacts");
      let fill: string;
      if (!standardizing) {
        fill = desaturate(
          trim(
            fillOf(state.scheme, liveMap, square.identity, square.angleDegrees, contacts),
            state.stageChroma,
          ),
          scene.presentation.drain,
          state.desaturationFloor,
        );
      } else {
        const source = state.restSource;
        const target = state.restTarget;
        const settled =
          source === null || target === null || sourceMap === null || targetMap === null
            ? fillFor((currentAtlasMap ?? liveMap).slotOf(square.angleDegrees), contacts)
            : scene.presentation.homeward
              ? mix(
                  referenceFill(source, sourceMap, index),
                  referenceFill(target, targetMap, index),
                  standard,
                )
              : referenceFill(source, sourceMap, index);
        const holds =
          state.holdsColour !== null && index < state.holdsColour.length
            ? Boolean(itemAt(state.holdsColour, index, "held-colour flags"))
            : false;
        if (holds) {
          fill = trim(settled, state.stageChroma);
        } else {
          const movingSlot =
            state.movingSlots === null || index >= state.movingSlots.length
              ? 1
              : itemAt(state.movingSlots, index, "moving colour slots");
          const moving = fillFor(movingSlot, MOVING_SHADE);
          const chosen =
            standard >= 1 ? settled : standard <= 0 ? moving : mix(moving, settled, standard);
          fill = desaturate(
            trim(chosen, state.stageChroma),
            scene.presentation.drain,
            state.desaturationFloor,
          );
        }
      }
      if (index === scene.squares.length - 1 && scene.presentation.newTint > 0) {
        return mix(fill, scarletFill, scene.presentation.newTint);
      }
      return fill;
    });
    const count = scene.squares.length;
    const touching = new Set<number>();
    for (let index = 0; index < geometry.contactEdges.length; index += 2) {
      const left = itemAt(geometry.contactEdges, index, "contact edges");
      const right = itemAt(geometry.contactEdges, index + 1, "contact edges");
      touching.add(left < right ? left * count + right : right * count + left);
    }
    return {
      fills,
      scheme: schemeFor(
        state.scheme,
        state.mode,
        state.animateStandardize,
        scene.presentation.resting,
      ),
      classes: liveMap.classes,
      centres: [...liveMap.centres],
      sizes: [...liveMap.sizes],
      slots: [...liveMap.slots],
      contacts: [...geometry.contacts],
      overlap: geometry.totalOverlap,
      deepestOverlap: geometry.deepestOverlap,
      overlapPairs: geometry.overlapPairs,
      contactEdges: [...geometry.contactEdges],
      touching,
    };
  };

  return Object.freeze({
    palette: Object.freeze([...palette]),
    shades: Object.freeze(shades.map((family) => Object.freeze([...family]))),
    angleToleranceDegrees,
    greens: Object.freeze(greens),
    greenStride: GREEN_STRIDE,
    schemes: COLOUR_SCHEMES,
    foldAngle,
    angleGap,
    slotForAngle,
    buildAngleMap,
    buildAtlasMap,
    angleFills,
    atlasFills,
    identityFill,
    identityFills,
    mix,
    desaturate,
    trim,
    schemeFor,
    paintScene,
  });
}

export const colour = Object.freeze({ createColourSystem });
