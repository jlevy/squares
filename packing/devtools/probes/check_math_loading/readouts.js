// The readouts after release, judged against the frozen early-input targets rather than the
// mutable DOM inputs: each slider's value, its output's TeX source in the active saved-font
// variant, whether that output is set in the sans math face, and the accessible direction
// state. `math` is `math/library.js`.
/**
 * @param {{ targets: ReadonlyArray<{ id: string, value: string }>, math: SquaresMathProbes }} o
 */
({ targets, math }) => {
  const { activeVariant } = math;
  return targets.map((target) => {
    const slider = /** @type {HTMLInputElement | null} */ (document.getElementById(target.id));
    const angle = target.id.startsWith("phi-");
    const direction = target.id.startsWith("kslider-");
    const output = document.getElementById(
      angle ? `s-${target.id}` : target.id.replace(/^kslider-/, "kval-"),
    );
    const annotation = [
      ...(output?.querySelectorAll('annotation[encoding="application/x-tex"]') || []),
    ].find(activeVariant);
    const maths = [...(output?.querySelectorAll(".katex") || [])].filter(activeVariant);
    return {
      id: target.id,
      expected_value: target.value,
      actual_value: slider?.value ?? null,
      expected_source: angle
        ? `${(Number(target.value) / 10).toFixed(3)}^{\\circ}`
        : `k = ${target.value}`,
      source: annotation?.textContent || "",
      sans:
        maths.length > 0 && maths.every((node) => !!node.closest('[data-kpress-math-face="sans"]')),
      state_matches:
        !direction ||
        (slider?.getAttribute("aria-valuetext") || "").startsWith(`Direction ${target.value} of `),
      supported: angle || direction,
    };
  });
};
