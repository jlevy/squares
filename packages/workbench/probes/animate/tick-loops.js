// How many playback loops run after a step ends inside a frame and play is pressed before the
// next one. Every `requestAnimationFrame(tick)` the page makes is counted against the frames
// that pass: one loop asks once a frame, two ask twice. o.n is the step, o.frames how many
// frames to count.
/** @param {{n: number, frames: number}} o */
async (o) => {
  const api = window.atlasTransitions;
  const original = window.requestAnimationFrame;
  let ticks = 0;
  let replayed = false;
  window.requestAnimationFrame = (callback) => {
    if (callback.name !== "tick") {
      return original.call(window, callback);
    }
    ticks += 1;
    return original.call(window, (stamp) => {
      callback(stamp);
      if (!replayed && !api.state().playing) {
        // The step ended inside this frame and paused: press play before the next one.
        replayed = true;
        api.play();
      }
    });
  };
  try {
    api.pause();
    api.setStepN(o.n);
    api.seek(Math.max(0, api.duration() - 1e-3));
    api.play();
    for (let wait = 0; wait < 120 && !replayed; wait++) {
      await new Promise((resolve) => original.call(window, resolve));
    }
    ticks = 0;
    for (let frame = 0; frame < o.frames; frame++) {
      await new Promise((resolve) => original.call(window, resolve));
    }
    return { replayed, ticks, frames: o.frames };
  } finally {
    api.pause();
    api.seek(0);
    window.requestAnimationFrame = original;
  }
};
