// Play the whole sequence from one n, with a probe on requestAnimationFrame recording every
// frame as [timestamp, pair, t, the pair's move start] in `window.__frames`, and return the pair
// it started on. Takes {startN, style, prefetch}.
/** @param {{startN: number, style: string, prefetch: boolean}} o */
(o) => {
  const A = window.atlasTransitions;
  const holder = /** @type {Window & {__frames?: number[][], __token?: number}} */ (window);
  A.stopAll();
  A.setStyle(o.style);
  A.goTo(o.startN);
  A.setContinuous({ prefetch: o.prefetch });
  holder.__frames = [];
  holder.__token = (holder.__token || 0) + 1;
  const token = holder.__token;
  /** @param {number} ts */
  const probe = (ts) => {
    if (holder.__token !== token) {
      return; // one probe per run: an earlier loop stops here
    }
    const s = A.state();
    // Set above, before the first frame could run.
    /** @type {number[][]} */ (holder.__frames).push([ts, s.pair, s.t, A.schedule().moveStart]);
    requestAnimationFrame(probe);
  };
  requestAnimationFrame(probe);
  A.playAll();
  return A.state().pair;
};
