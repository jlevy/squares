// Stop the startup instrument and return its report.
() =>
  /** @type {() => object} */ (
    /** @type {SquaresMathStartupState} */ (globalThis.__mathStartup).finish
  )();
