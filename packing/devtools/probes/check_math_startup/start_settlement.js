// Evaluate does not honor Playwright's default timeout. Start the real settlement promise
// without awaiting it in this call, recording its outcome on the startup state, so that the
// bounded `wait_for_function` that follows still leaves a broken page with a report.
// `settled` is `render_explainer_pdf/settled.js`'s function, handed in as a handle.
/** @param {{ settled: () => Promise<void> }} o */
({ settled }) => {
  const state = /** @type {SquaresMathStartupState} */ (globalThis.__mathStartup);
  state.settlement_state = "pending";
  settled().then(
    () => {
      state.settlement_state = "resolved";
    },
    (error) => {
      state.errors.push(String(error));
      state.settlement_state = "rejected";
    },
  );
};
