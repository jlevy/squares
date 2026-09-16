// Settlement. Media changes and ResizeObserver callbacks can start asynchronous math renders:
// let layout dispatch them, then await those renders and the faces they request.
//
// A reference probe: the file returns the settlement function rather than being it, so that
// `page.evaluate_handle` yields a handle another probe can call. `render_explainer_pdf.SETTLED`
// is this applied, which evaluates to the function itself; `observe`, when given, is called
// with each phase's name.
/** @returns {(observe?: ((phase: string) => unknown) | null) => Promise<void>} */
() => async (observe) => {
  observe?.("before-final-frames");
  void document.documentElement.offsetHeight;
  await new Promise((done) =>
    requestAnimationFrame(() => {
      observe?.("final-frame-1");
      requestAnimationFrame(() => {
        observe?.("final-frame-2");
        done(undefined);
      });
    }),
  );
  await globalThis.squaresMath?.settled();
  await document.fonts.ready;
  observe?.("after-fonts");
  await new Promise((done) =>
    requestAnimationFrame(() => {
      observe?.("final-frame-3");
      done(undefined);
    }),
  );
  await globalThis.squaresMath?.settled();
  observe?.("settled");
};
