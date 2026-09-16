// The page global `check_math_faces`'s probes read beyond the shared explainer API: KPress's
// KaTeX text metric tables.

/** KPress's KaTeX metric tables by context, font and code point; index 4 is the advance. */
interface KpressKatexTextMetrics {
  sans?: Record<string, Record<number, number[]>>;
}

declare var kpressKatexTextMetrics: KpressKatexTextMetrics | undefined;
