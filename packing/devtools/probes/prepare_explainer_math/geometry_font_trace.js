// A head script: the geometry probe's font gate. Every `kpressMathText.render` and `hydrate`
// call is held until the before snapshot is complete and the gate is released, and the first
// math request and every rejection are traced in `__squaresGeometryFontTrace`.
() => {
  /** @type {SquaresGeometryFontTrace} */
  const trace = {
    time_origin_ms: performance.timeOrigin,
    first_math_request_ms: null,
    before_snapshot_complete: false,
    root_watchdog_paused: false,
    queued_calls: 0,
    rejections: [],
  };
  globalThis.__squaresGeometryFontTrace = trace;
  /** @type {(() => void)[]} */
  const waiting = [];
  let released = false;
  // This control delays entry into kpressMathText while it constructs the
  // altered before-state. Pause the independent root fallback or that test
  // setup can expose dynamic prepared formulas before the real runtime gets
  // the synchronous call that hides them. Watchdog expiry has its own control.
  /** @type {ReturnType<typeof setTimeout> | undefined} */
  let rootWatchdog;
  Object.defineProperty(globalThis, "kpressMathPendingTimer", {
    configurable: true,
    get() {
      return rootWatchdog;
    },
    /** @param {ReturnType<typeof setTimeout>} timer */
    set(timer) {
      rootWatchdog = timer;
      clearTimeout(timer);
      trace.root_watchdog_paused = true;
    },
  });
  globalThis.__squaresMarkGeometryBeforeSnapshotComplete = () => {
    trace.before_snapshot_complete = true;
  };
  globalThis.__squaresReleaseGeometryFontGate = () => {
    if (!trace.before_snapshot_complete) {
      throw new Error("geometry font gate released before the before snapshot");
    }
    if (released) {
      return;
    }
    released = true;
    for (const invoke of waiting.splice(0)) {
      invoke();
    }
  };
  /**
   * @param {(...args: unknown[]) => unknown} original
   * @param {unknown} receiver
   * @param {unknown[]} args
   */
  const invoke = (original, receiver, args) => {
    const start = performance.now();
    trace.first_math_request_ms ??= start;
    let result;
    try {
      result = original.apply(receiver, args);
    } catch (error) {
      trace.rejections.push({
        source: String(args[0]),
        elapsed_ms: performance.now() - start,
        reason: String(error),
      });
      throw error;
    }
    Promise.resolve(result).then(undefined, (error) => {
      trace.rejections.push({
        source: String(args[0]),
        elapsed_ms: performance.now() - start,
        reason: String(error),
      });
    });
    return result;
  };
  /** @type {Record<string, (...args: unknown[]) => unknown> | undefined} */
  let runtime;
  Object.defineProperty(globalThis, "kpressMathText", {
    configurable: true,
    get() {
      return runtime;
    },
    /** @param {Record<string, (...args: unknown[]) => unknown>} api */
    set(api) {
      runtime = api;
      for (const name of ["render", "hydrate"]) {
        const original = /** @type {(...args: unknown[]) => unknown} */ (api[name]);
        /**
         * @this {unknown}
         * @param {unknown[]} args
         */
        api[name] = function (...args) {
          // The arrow functions below read this call's `this` as their own.
          if (released) {
            return invoke(original, this, args);
          }
          return new Promise((resolve, reject) => {
            trace.queued_calls++;
            waiting.push(() => {
              try {
                Promise.resolve(invoke(original, this, args)).then(resolve, reject);
              } catch (error) {
                reject(error);
              }
            });
          });
        };
      }
    },
  });
};
