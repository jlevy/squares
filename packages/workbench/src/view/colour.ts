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
/**
 * A shared centre holds a tilt exactly the tolerance away, whichever way float arithmetic
 * rounds the gap. The build draws centres from four-place angles, 0.0001 apart at the least,
 * and holds such a tilt the same way (`_TIE` in `build_candidate.py`).
 */
const SHARED_TIE = 1e-9;

type Lab = readonly [number, number, number];

export interface AngleMap {
  classes: number;
  centres: number[];
  slots: number[];
  sizes: number[];
  /** The index of the class a tilt belongs to, or -1 for a tilt in none of them. */
  classOf(angleDegrees: number): number;
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
  /** Whether the step rearranges nothing, so no square needs a moving colour. */
  stillPair: boolean;
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
  /** The atlas's shared angle centres, sorted (#554). */
  readonly angleCentres: readonly number[];
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

/**
 * OKLab's rectangular `a`/`b` as polar chroma and hue, hue in degrees.
 *
 * A near-neutral colour has no meaningful hue -- the angle of a point at the origin is noise --
 * so `chroma` is what a caller checks before trusting `hue`.
 */
function labToPolar(lab: Lab): { lightness: number; chroma: number; hue: number } {
  const chroma = Math.hypot(lab[1], lab[2]);
  return {
    lightness: lab[0],
    chroma,
    hue: (Math.atan2(lab[2], lab[1]) * 180) / Math.PI,
  };
}

/** Below this OKLab chroma a colour is neutral and takes the other endpoint's hue. */
const NEUTRAL_CHROMA = 1e-4;

/**
 * The widest hue arc a blend will travel around the wheel, in degrees.
 *
 * Inside it the two ends are the same colour moving a little -- two shades of one family, a
 * moving shade settling into its neighbour -- and travelling between them shows nothing a
 * viewer would call a third colour. Past it the arc starts running through hues neither end
 * has, so the blend goes through neutral instead.
 *
 * Twenty-five, not sixty. At sixty a green at 158 degrees blending to the olive at 109 swept
 * the forty-nine between them, and the middle of that sweep is a yellow-green -- a colour
 * neither end has, which is the whole thing this rule exists to prevent. The angle families are
 * far enough apart that only shades of one family fall inside twenty-five.
 */
const HUE_ARC_LIMIT = 25;

/**
 * The shortest way round from one hue to another, in degrees, signed.
 *
 * Without the fold, a mix from 350 degrees to 10 travels 340 degrees the wrong way through
 * every other hue on the wheel -- the same artifact a chord through the middle produces, just
 * with a different shape.
 */
function hueDelta(from: number, to: number): number {
  return ((((to - from) % 360) + 540) % 360) - 180;
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
  angleCentres: number[];
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
  const angleCentres = [...config.angleCentres];
  for (const [index, centre] of angleCentres.entries()) {
    finite(centre, "shared angle centre");
    if (centre < 0 || centre >= QUARTER_TURN_DEGREES) {
      throw new RangeError("shared angle centres must be folded into a quarter turn");
    }
    if (
      angleGap(centre, 0) <= config.angleToleranceDegrees ||
      angleGap(centre, 45) <= config.angleToleranceDegrees
    ) {
      throw new RangeError("a shared angle centre lies in a pinned class");
    }
    if (
      index > 0 &&
      centre - itemAt(angleCentres, index - 1, "shared angle centres") <=
        config.angleToleranceDegrees
    ) {
      throw new RangeError(
        "shared angle centres must be sorted and further apart than the tolerance",
      );
    }
  }
  return { palette, shades, angleToleranceDegrees: config.angleToleranceDegrees, angleCentres };
}

/** Build immutable colour behavior from the palette emitted with the corpus. */
export function createColourSystem(config: CorpusColour): ColourSystem {
  const copied = paletteCopy(config);
  const { palette, shades, angleToleranceDegrees, angleCentres } = copied;
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
  /**
   * Blend two colours the way the palette was built: polar, in OKLCH.
   *
   * Lerping OKLab's rectangular `a` and `b` walks a CHORD across the a-b plane, and a chord
   * passes nearer the neutral axis than either of its endpoints. The further apart the two
   * hues, the deeper the chroma sags in the middle, and the sag reads as a grey flash. The
   * worst case here is also the most visible one -- a green fill blended toward the new
   * square's scarlet is close to a half turn of hue, so the chord ran almost through grey.
   *
   * Lerping lightness, chroma and hue instead keeps chroma up across the whole blend, and
   * `oklchHex` gamut-maps whatever comes out. This is the same shape `rampFill` already used.
   */
  const mix = (left: string, right: string, progressValue: number): string => {
    const progress = clamp01(progressValue);
    if (progress <= 0) {
      return checkedHex(left);
    }
    if (progress >= 1) {
      return checkedHex(right);
    }
    const from = labToPolar(toLab(left));
    const to = labToPolar(toLab(right));
    // A neutral endpoint has no hue to travel from or to, so it borrows the other's and moves
    // in chroma alone. Reading its noisy angle instead would swing the blend through hues
    // neither colour has.
    const fromHue = from.chroma < NEUTRAL_CHROMA ? to.hue : from.hue;
    const toHue = to.chroma < NEUTRAL_CHROMA ? from.hue : to.hue;
    const lightness = lerp(from.lightness, to.lightness, progress);
    const chroma = lerp(from.chroma, to.chroma, progress);
    const arc = hueDelta(fromHue, toHue);
    if (Math.abs(arc) <= HUE_ARC_LIMIT) {
      // Near hues blend along the short arc at full chroma. Two shades of one family, or a
      // moving shade settling into its neighbour, are the same colour moving a little; taking
      // them through neutral would put a wash in the middle of a change nobody should notice.
      return oklchHex(lightness, chroma, fromHue + arc * progress);
    }
    // Far hues cross through neutral instead of around the wheel. Green to scarlet is close to
    // a half turn, and the short arc between them runs through yellow -- a colour neither end
    // has and the picture never shows, appearing for the length of the blend and reading as a
    // flash. Collapsing chroma to nothing at the crossing and bringing it back on the other
    // side gives green, then something greyer, then scarlet, which is the change itself and
    // nothing else. The hue switches where chroma is zero, so the switch cannot be seen.
    const away = Math.abs(2 * progress - 1);
    return oklchHex(lightness, chroma * away, progress < 0.5 ? fromHue : toHue);
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
  /**
   * The shared class a tilt belongs to, as that class's centre, or null for a tilt no shared
   * class holds. The two pinned classes are 0 and 45 degrees; any other tilt belongs to the
   * nearest of the atlas's shared centres within the tolerance. The centres lie further apart
   * than the tolerance and clear of the pins, so a tilt the atlas carries meets one class, and
   * so one slot, in every frame (#554).
   */
  const sharedCentre = (angleDegrees: number): number | null => {
    const angle = foldAngle(angleDegrees);
    if (angleGap(angle, 0) <= angleToleranceDegrees) {
      return 0;
    }
    if (angleGap(angle, 45) <= angleToleranceDegrees) {
      return 45;
    }
    // The first centre at or above the angle; it and the one below are the only candidates.
    // No centre is within the tolerance of the pins, so none is reached across the seam.
    let low = 0;
    let high = angleCentres.length;
    while (low < high) {
      const middle = Math.floor((low + high) / 2);
      if (itemAt(angleCentres, middle, "shared angle centres") < angle) {
        low = middle + 1;
      } else {
        high = middle;
      }
    }
    let nearest: number | null = null;
    let nearestGap = Number.POSITIVE_INFINITY;
    for (const index of [low - 1, low]) {
      const centre = angleCentres[index];
      if (centre === undefined) {
        continue;
      }
      const gap = angleGap(angle, centre);
      if (gap <= angleToleranceDegrees + SHARED_TIE && gap < nearestGap) {
        nearest = centre;
        nearestGap = gap;
      }
    }
    return nearest;
  };
  /**
   * A tilt's palette slot: the pins, then the five-degree band of its shared class's centre,
   * or of the tilt itself when no shared class holds it. Two classes less than the tolerance
   * apart used to fall either side of a band edge when each frame clustered its own tilts:
   * n = 29's 64.9387 and T-151's 65.2889 at n = 272 were slots 14 and 15 (#553, review C1).
   * The band is now read off a centre every frame shares.
   */
  const slotForAngle = (angleDegrees: number): number => {
    const angle = foldAngle(angleDegrees);
    if (angleGap(angle, 0) <= angleToleranceDegrees) {
      return 0;
    }
    if (angleGap(angle, 45) <= angleToleranceDegrees) {
      return 1;
    }
    const band = Math.floor((sharedCentre(angle) ?? angle) / slotBand);
    return 2 + Math.max(0, Math.min(freeSlots - 1, band));
  };
  /**
   * One frame's angle classes. A tilt a shared class holds joins that class, centred on the
   * shared centre; the rest, which only a frame no atlas witness draws can carry (a Pack or
   * Search run, an import, a square mid-turn), cluster among themselves within the tolerance
   * around the first tilt of each, centred on their mean, as every class once did.
   */
  const buildAngleMap = (anglesDegrees: readonly number[]): AngleMap => {
    const shared: boolean[] = [];
    const representatives: number[] = [];
    const sums: number[] = [];
    const counts: number[] = [];
    const sharedIndex = new Map<number, number>();
    for (const rawAngle of anglesDegrees) {
      const angle = foldAngle(rawAngle);
      const centre = sharedCentre(angle);
      if (centre !== null) {
        const at = sharedIndex.get(centre);
        if (at === undefined) {
          sharedIndex.set(centre, representatives.length);
          shared.push(true);
          representatives.push(centre);
          sums.push(0);
          counts.push(1);
        } else {
          counts[at] = itemAt(counts, at, "angle counts") + 1;
        }
        continue;
      }
      let match = -1;
      for (let index = 0; index < representatives.length; index += 1) {
        if (
          !itemAt(shared, index, "shared classes") &&
          angleGap(angle, itemAt(representatives, index, "angle representatives")) <=
            angleToleranceDegrees
        ) {
          match = index;
          break;
        }
      }
      if (match < 0) {
        shared.push(false);
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
      itemAt(shared, index, "shared classes")
        ? representative
        : foldAngle(
            representative +
              itemAt(sums, index, "angle sums") / itemAt(counts, index, "angle counts"),
          ),
    );
    const slots = centres.map(slotForAngle);
    const classOf = (rawAngle: number): number => {
      const angle = foldAngle(rawAngle);
      const centre = sharedCentre(angle);
      if (centre !== null) {
        return sharedIndex.get(centre) ?? -1;
      }
      for (let index = 0; index < centres.length; index += 1) {
        if (
          !itemAt(shared, index, "shared classes") &&
          angleGap(angle, itemAt(centres, index, "angle centres")) <= angleToleranceDegrees
        ) {
          return index;
        }
      }
      return -1;
    };
    const slotOf = (rawAngle: number): number => {
      const index = classOf(rawAngle);
      return index < 0 ? slotForAngle(rawAngle) : itemAt(slots, index, "angle slots");
    };
    return {
      classes: centres.length,
      centres,
      slots,
      sizes: [...counts],
      classOf,
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
      const index = base.classOf(rawAngle);
      return index < 0 ? slotForAngle(rawAngle) : itemAt(slots, index, "atlas slots");
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
    fraction(scene.presentation.homeward, "scene homeward progress");
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
        // The square a step adds has no place in n's packing: the source reference parks it
        // far off at angle 0 so its neighbors keep n's contacts, which as a color is a pale
        // right-angle green. Turned from that, it crossed from scarlet to the pale green and
        // then dropped a shade when the rest color turned. It takes n + 1's throughout.
        const homeward = index === scene.squares.length - 1 ? 1 : scene.presentation.homeward;
        const settled =
          source === null || target === null || sourceMap === null || targetMap === null
            ? fillFor((currentAtlasMap ?? liveMap).slotOf(square.angleDegrees), contacts)
            : mix(
                referenceFill(source, sourceMap, index),
                referenceFill(target, targetMap, index),
                homeward,
              );
        const holds =
          state.holdsColour !== null && index < state.holdsColour.length
            ? Boolean(itemAt(state.holdsColour, index, "held-colour flags"))
            : false;
        const arriving = index === scene.squares.length - 1 && scene.presentation.newTint > 0;
        if (arriving) {
          // **One blend, not two.** The arriving square used to take the moving-to-settled
          // blend and then be blended again toward scarlet, and each of those crosses through
          // neutral at its own moment. Near the crossings the hue belongs to whichever term
          // happens to dominate, so it thrashed: measured at the step into 51, frames 83 to 86
          // read hue 11, then 154, then 12, then 110 -- red, green, red, olive in four frames,
          // which at speed is the smear the owner sees.
          //
          // It has no moving identity to track anyway: it is not a square being followed from
          // one arrangement to the next, it is a square arriving. So it goes straight from
          // scarlet to the colour it will keep, in one crossing.
          //
          // The drain is applied to the far END of the blend, not to the blend. Draining the
          // result muted the scarlet along with everything else, and on a matched step -- where
          // the drain is deepest exactly while the square arrives -- it took the red out
          // entirely: measured at the step into 51, not one frame of ninety-one carried a
          // saturated red square. The drain says "this square is unsettled and still looking for
          // its place", which the arriving square is not. It is arriving, and its redness is the
          // whole of what that says. So it comes in at full scarlet and crosses to the colour the
          // rest of the packing is wearing at that moment, drained or not.
          fill = mix(
            desaturate(
              trim(settled, state.stageChroma),
              scene.presentation.drain,
              state.desaturationFloor,
            ),
            scarletFill,
            scene.presentation.newTint,
          );
        } else if (holds || state.stillPair) {
          // A still pair rearranges nothing -- a prefix or a shared picture, where the only
          // event is the new square arriving -- so no square needs a moving colour to be
          // tracked by. Giving them one recoloured the whole packing to the moving palette for
          // the length of the step, and with the drain off (there being no motion to mute) it
          // showed at full strength: measured over n = 96..102, 6,735 of 32,676 square-instants
          // came out at `#a3a580`, an olive, on packings whose own colours are greens.
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
      if (!standardizing && index === scene.squares.length - 1 && scene.presentation.newTint > 0) {
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
    angleCentres: Object.freeze([...angleCentres]),
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
