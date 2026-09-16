// True once the settlement `start_settlement` began has resolved or rejected.
() =>
  /** @type {SquaresMathStartupState} */ (globalThis.__mathStartup).settlement_state !== "pending";
