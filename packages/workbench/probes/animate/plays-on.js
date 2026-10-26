// Whether play carries on from one step into the next: the range o.from..o.to is played from its
// start until the stage has shown o.steps values of n, play has stopped, or o.seconds of real
// time have passed, and the probe reports every n the stage showed, whether it is still playing,
// any error a frame threw, and the clock it ran on: the frames drawn, the real time they took,
// the slowest of them, and the seconds of the page's own clock they advanced. A seek draws one
// instant and cannot see play stop between steps, which is how a regression that halted playback
// after the first step (the owner, 2026-09-21) passed every check. The page's clock advances at
// most 0.1 s a frame, so on a host too loaded to draw ten frames a second it falls behind real
// time; the clock it reports is what tells that from a stop (#538). Pauses and puts the range back.
/** @param {{from: number, to: number, steps: number, seconds: number}} o */
async (o) => {
  const api = window.atlasTransitions;
  const chosen = api.range();
  /** @type {Set<number>} */
  const seen = new Set();
  /** @type {string[]} */
  const errors = [];
  /** @param {ErrorEvent} event */
  const record = (event) => {
    errors.push(String(event.message));
  };
  window.addEventListener("error", record);
  try {
    api.pause();
    api.setRange(o.from, o.to);
    api.playRange();
    const started = performance.now();
    let last = started;
    let frames = 0;
    let slowest = 0;
    let clock = 0;
    let before = api.state();
    let playing = before.playing;
    while (performance.now() - started < o.seconds * 1000) {
      await new Promise((resolve) => window.requestAnimationFrame(resolve));
      const now = performance.now();
      frames += 1;
      slowest = Math.max(slowest, now - last);
      last = now;
      const state = api.state();
      // A step's remaining time, then the next step's elapsed time, when the stage moved on.
      clock +=
        state.pair === before.pair ? state.t - before.t : before.duration - before.t + state.t;
      before = state;
      playing = state.playing;
      if (state.n !== null) {
        seen.add(state.n);
      }
      if (seen.size >= o.steps || !playing) {
        break;
      }
    }
    return {
      playing,
      seen: [...seen].sort((a, b) => a - b),
      errors,
      frames,
      seconds: (performance.now() - started) / 1000,
      slowest: slowest / 1000,
      clock,
    };
  } finally {
    window.removeEventListener("error", record);
    api.pause();
    api.setRange(chosen.from, chosen.to);
  }
};
