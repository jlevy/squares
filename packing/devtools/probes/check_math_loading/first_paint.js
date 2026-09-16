// Installed before parsing: samples animation frames, so hidden staging nodes do not count as
// a paint, and records the first frame each formula is exposed, whether its glyph runs' faces
// were ready then, any math exposed while `hold_fonts` still holds the loads, and any exposed
// semantic MathML. Mutations discover glyph runs early, so already-ready font promises can
// settle before first exposure.
//
// An init script takes no argument, so the shared helpers come from `__squaresMathProbes`,
// which `math/library.js` installs when an earlier init script applies it with
// `{install: true}`.
() => {
  const library = globalThis.__squaresMathProbes;
  if (!library) {
    throw new Error("check_math_loading/first_paint needs math/library installed before it");
  }
  globalThis.__mathFirstPaint = null;
  /** @type {SquaresMathLoadingState} */
  const state = {
    frames: 0,
    mathFontChecks: 0,
    unreadyMath: [],
    earlyMath: null,
    fallback: null,
    stop: false,
  };
  globalThis.__mathLoadingState = state;
  const { exposed, activeVariant, requiredFonts } = library;
  const observe = library.fontLoadObserver((...args) =>
    globalThis.__mathLoadControl?.nativeLoad
      ? globalThis.__mathLoadControl.nativeLoad(...args)
      : document.fonts.load(...args),
  );
  const affectedMath = library.mutatedMath;
  /** @param {MutationRecord[]} [records] */
  const discover = (records) => {
    if (state.stop) {
      return;
    }
    for (const math of affectedMath(records)) {
      if (activeVariant(math)) {
        requiredFonts(math, observe);
      }
    }
  };
  const mutations = new MutationObserver(discover);
  mutations.observe(document, {
    subtree: true,
    childList: true,
    characterData: true,
    attributes: true,
    attributeFilter: [
      "class",
      "style",
      "hidden",
      "data-kpress-math-face",
      "data-kpress-math-prepared",
      "data-squares-math-ready",
    ],
  });
  discover();
  /** @type {WeakSet<Element>} */
  const observed = new WeakSet();
  /** @param {Element} node */
  const label = (node) =>
    /** @type {string} */ (node.textContent).trim().replace(/\s+/g, " ").slice(0, 100);
  const sample = () => {
    state.frames++;
    const maths = [...document.querySelectorAll(".katex")].filter(activeVariant).filter(exposed);
    for (const math of maths) {
      if (observed.has(math)) {
        continue;
      }
      observed.add(math);
      const required = requiredFonts(math, observe);
      state.mathFontChecks += required.length;
      const late = required.filter((face) => !face.ready);
      if (!required.length) {
        state.unreadyMath.push(`${label(math)}: no observed glyph closure`);
      }
      if (late.length) {
        state.unreadyMath.push(
          label(math) +
            ": " +
            late
              .map(
                (face) =>
                  `${face.spec} [${face.text}] (${face.outcome || "error"}; ` +
                  face.faces.map((match) => `${match.family}: ${match.status}`).join(", ") +
                  (face.error ? `; ${face.error}` : "") +
                  ")",
              )
              .join(", "),
        );
      }
      if (!globalThis.__mathFirstPaint) {
        const faces = [...document.fonts].map((face) => ({
          family: face.family,
          style: face.style,
          weight: face.weight,
          unicodeRange: face.unicodeRange,
          status: face.status,
        }));
        globalThis.__mathFirstPaint = { at: performance.now(), faces, required };
      }
    }
    const control = globalThis.__mathLoadControl;
    if (maths.length && control && !control.released && !state.earlyMath) {
      state.earlyMath = label(/** @type {Element} */ (maths[0]));
    }
    const fallback = [...document.querySelectorAll(".kpress-math-semantic")]
      .filter(activeVariant)
      .find(exposed);
    if (fallback && !state.fallback) {
      state.fallback = label(fallback);
    }
    if (!state.stop) {
      requestAnimationFrame(sample);
    } else {
      mutations.disconnect();
    }
  };
  requestAnimationFrame(sample);
};
