// The explainer page's globals, as the probes under `packing/devtools/probes` and
// `packing/tests/probes` read them. Two kinds live here: the page's own API (kpress's math
// runtime and the host adapter `render_explainer` inlines), and the instrumentation globals
// that `check_math_loading`'s init scripts install and other checkers read.
//
// A probe group's own instrumentation globals belong in a `.d.ts` in that group's
// directory. Extend an interface declared here by merging, in your own file; never declare a
// `var` a second time.

/** The host adapter `render_explainer`'s `host_math_init` installs as `squaresMath`. */
interface SquaresMathHost {
  render(el: Element, source: string, display?: boolean): Promise<boolean>;
  reserve(): () => void;
  batch(jobs: ReadonlyArray<() => unknown>): Promise<void>;
  submitted(): Promise<void>;
  settled(): Promise<void>;
  context: { isSansContext(node: Node): boolean };
}

/** kpress's math runtime, `katex/katex-math-runtime.js`. */
interface KpressMathText {
  ready(nodes?: Iterable<Element>, options?: object): Promise<unknown>;
  render(tex: string, node: Element, katexOptions?: object, options?: object): Promise<unknown>;
  hydrate(tex: string, node: Element, katexOptions?: object, options?: object): Promise<unknown>;
  installTablesFor(node: Element, options?: object): unknown;
  restore(): void;
  complete(): void;
}

/** `check_math_loading/hold_fonts`: holds font loads until released. */
interface SquaresMathLoadControl {
  heldLoads: number;
  released: boolean;
  release(): void;
  nativeLoad: FontFaceSet["load"];
}

/** `check_math_loading/first_paint`: what the frame sampler has seen. */
interface SquaresMathLoadingState {
  frames: number;
  mathFontChecks: number;
  unreadyMath: string[];
  earlyMath: string | null;
  fallback: string | null;
  stop: boolean;
}

/** `check_math_loading/first_paint`: the fonts at the first frame a formula was exposed. */
interface SquaresMathFirstPaint {
  at: number;
  faces: SquaresFontFaceSummary[];
  required: SquaresFontRequirement[];
}

/**
 * The KaTeX build the page inlines: its public `render`, which `check_math_faces` re-typesets
 * with and the startup fixture stands in for, and the internal `__renderToDomTree`, whose box
 * tree `compare_math_fonts` sums (`compare_math_fonts/types.d.ts` has that tree's shape).
 */
interface SquaresKatex {
  render(expression: string, element: Element, options?: object): void;
  __renderToDomTree(
    expression: string,
    options: { throwOnError: boolean; displayMode: boolean },
  ): CompareMathFontsKatexTree;
}

declare var katex: SquaresKatex;
declare var squaresMath: SquaresMathHost | undefined;
declare var kpressMathText: KpressMathText | undefined;
declare var __mathLoadControl: SquaresMathLoadControl | undefined;
declare var __mathLoadingState: SquaresMathLoadingState | undefined;
declare var __mathFirstPaint: SquaresMathFirstPaint | null | undefined;
