// One change of the atlas's layout, timed. `press` is the selector of the control that
// makes it, a view tab or the expander. The control is pressed once two frames have
// passed, and the report is made once every tile and container move has finished and two frames
// more have passed. It gives: how long the press's own handler ran, which is the whole
// of the script's work (both reads of every box, the change and starting the moves);
// how many tiles moved; how long the move lasted from the press; the animation frames
// the page was given in that time, the longest and the mean interval between two, and
// how many intervals were over one and a half frames of the display's rate, which is a
// frame the main thread missed; and every long task, over 50 ms, with its length. An
// animation frame is an opportunity to paint on the main thread, not a presented frame:
// the moves themselves are transforms the compositor draws without it.
//
// Asking for an animation frame makes the main thread produce one, and with it restyle
// every tile in a move, which it otherwise leaves to the compositor. So with `frames`
// false no frame is asked for while the tiles move, and the browser's own counters over
// the change (`measure_atlas_views.timed`) show what the main thread does when nothing
// is watching it; the frame numbers are then all zero.
async (/** @type {{press: string, frames: boolean}} */ { press, frames: watch }) => {
  /** @param {number} value */
  const round = (value) => Math.round(value * 100) / 100;
  const frame = () => new Promise((resolve) => requestAnimationFrame(resolve));
  const control = document.querySelector(press);
  if (!(control instanceof HTMLElement)) {
    return null;
  }
  /** @type {number[]} */
  const frames = [];
  /** @type {{start: number, duration: number}[]} */
  const tasks = [];
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      tasks.push({ start: round(entry.startTime), duration: round(entry.duration) });
    }
  });
  observer.observe({ entryTypes: ["longtask"] });
  let watching = watch;
  /** @param {number} time */
  const tick = (time) => {
    frames.push(time);
    if (watching) {
      requestAnimationFrame(tick);
    }
  };
  if (watch) {
    requestAnimationFrame(tick);
  }
  await frame();
  await frame();
  const start = performance.now();
  control.click();
  const handled = performance.now() - start;
  const moves = document
    .getAnimations()
    .filter(
      (animation) =>
        !(animation instanceof CSSTransition) &&
        animation.effect instanceof KeyframeEffect &&
        animation.effect.target?.matches(".site-atlas-cell, .site-atlas-cells") === true,
    );
  await Promise.allSettled(moves.map((animation) => animation.finished));
  const end = performance.now();
  if (watch) {
    await frame();
    await frame();
  }
  watching = false;
  observer.disconnect();
  const during = frames.filter((time) => time >= start && time <= end + 34);
  const gaps = during.slice(1).map((time, index) => time - (during[index] ?? time));
  const ordered = [...gaps].sort((a, b) => a - b);
  const usual = ordered[Math.floor(ordered.length / 2)] ?? 0;
  return {
    handler_ms: round(handled),
    moved: moves.filter(
      (animation) =>
        animation.effect instanceof KeyframeEffect &&
        animation.effect.target?.matches(".site-atlas-cell") === true,
    ).length,
    lasted_ms: round(end - start),
    frames: during.length,
    frame_ms: round(usual),
    longest_frame_ms: round(Math.max(0, ...gaps)),
    mean_frame_ms: round(gaps.reduce((sum, gap) => sum + gap, 0) / Math.max(1, gaps.length)),
    missed_frames: gaps.filter((gap) => gap > usual * 1.5).length,
    long_tasks: tasks.filter((task) => task.start + task.duration >= start),
  };
};
