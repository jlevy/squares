// What `inspect_explainer_typography`'s probes return, mirroring the `TypedDict`s in
// `inspect_explainer_typography.py`, and the one page global its self-test keeps between
// two probes.

/** `typography.js`: one computed family, weight, style and colour, with sizes and samples. */
interface TypographyFontUse {
  family: string;
  weight: string;
  style: string;
  color: string;
  sizes: number[];
  effective_sizes: number[];
  samples: string[];
}

/** `math_contexts.js`: a formula's outer em against its surrounding text. */
interface TypographyMathContext {
  role: string;
  display_math: boolean;
  source: string | null;
  size: number;
  context_size: number;
  family: string;
  context_family: string;
  weight: string;
  context_weight: string;
  text_rendering: string;
  context_text_rendering: string;
  caption?: string;
  baseline_prepared?: boolean;
  baseline_offset?: number | null;
  unboxed_baseline_offset?: number | null;
}

/** One slot `prepare_explainer_math`'s measurement returns, as the self-test applies it. */
interface TypographyMathFragment {
  key: string;
  html: string;
  attributes: Record<string, string>;
}

/**
 * `render_baseline_fixture.js`: each fixture formula's `.strut` styles as KaTeX first drew
 * them, before preparation, which `restore_original_struts.js` puts back.
 */
declare var baselineOriginalStruts: (string | null)[][] | undefined;
