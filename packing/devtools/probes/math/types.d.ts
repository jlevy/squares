// What `math/library.js` returns: the explainer's math helpers that more than one checker
// needs, written once. A probe given the library through its argument declares it as
// `SquaresMathProbes`; an init script reads the copy the library installs as
// `__squaresMathProbes`.

/** One declared face, as `document.fonts` reports it. */
interface SquaresFontFaceSummary {
  family: string;
  style: string;
  weight: string;
  unicodeRange: string;
  status: FontFaceLoadStatus;
}

/** What the font-load observer has seen of one `document.fonts.load` request. */
interface SquaresFontObservation {
  outcome: "pending" | "resolved" | "rejected";
  faces: SquaresFontFaceSummary[];
  error?: string;
  ready: boolean;
}

/** One CSS family's glyph run inside a formula, and whether its faces are ready. */
interface SquaresFontRequirement extends SquaresFontObservation {
  spec: string;
  text: string;
}

/** Observes one request per distinct description and text, and reports it as it stands. */
type SquaresFontObserver = (spec: string, text: string) => SquaresFontObservation;

/** What a font load resolves to: the faces it matched. */
type SquaresFontLoad = (
  spec: string,
  text: string,
) => Iterable<FontFace> | PromiseLike<Iterable<FontFace>>;

interface SquaresMathProbes {
  /** Whether a node belongs to the saved-font variant the root attributes select. */
  activeVariant(node: Element): boolean;
  /** Whether a node has readable geometry after ancestor clipping and scrolling. */
  exposed(node: Element): boolean;
  /** Every glyph run a formula draws, grouped by CSS family, with its readiness. */
  requiredFonts(math: Element, observe: SquaresFontObserver): SquaresFontRequirement[];
  /** A readiness oracle over `load` that does not trust `document.fonts.check`. */
  fontLoadObserver(load: SquaresFontLoad): SquaresFontObserver;
  /** The formulas a batch of mutations can have changed; every formula without records. */
  mutatedMath(records?: readonly MutationRecord[]): Iterable<Element>;
}

/** The library as `math/library.js` installs it for the init scripts that follow it. */
declare var __squaresMathProbes: SquaresMathProbes | undefined;
