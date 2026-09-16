// A head script: holds every `squaresMath.batch` call in `__squaresQueueControl` instead of
// running it, until `release()`.
() => {
  /** @type {SquaresMathHost | undefined} */
  let runtime;
  /** @type {(() => unknown)[]} */
  const posted = [];
  globalThis.__squaresQueueControl = {
    get count() {
      return posted.length;
    },
    release() {
      for (const post of posted.splice(0)) {
        post();
      }
    },
  };
  // Delay the public producer before its first static job. The host must
  // protect every queued wrapper before handing any work to the scheduler.
  Object.defineProperty(globalThis, "squaresMath", {
    configurable: true,
    get() {
      return runtime;
    },
    /** @param {SquaresMathHost} api */
    set(api) {
      runtime = api;
      const batch = api.batch;
      /**
       * @this {SquaresMathHost}
       * @param {ReadonlyArray<() => unknown>} jobs
       */
      api.batch = function (jobs) {
        return new Promise((resolve, reject) => {
          posted.push(() => Promise.resolve(batch.call(this, jobs)).then(resolve, reject));
        });
      };
    },
  });
};
