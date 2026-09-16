// Grades the move of the pair on the stage on both halves (see `grade_motion.py`). It reads
// every square's pose at the end, at the start of the move, at `samples` instants across it
// and at `lockAt` of the way through, where the lock-in takes over. Outcome: the worst and
// mean distance, and the worst angle, of the lock-in poses from the end. Motion: the worst
// distance a square strays from its straight line, and its worst single-frame step. Beside
// them, the deepest overlap and the cost the page reports for the run. Leaves the clock at the
// end. Takes {samples, lockAt, style}.
/** @param {{samples: number, lockAt: number, style: import("../../../../../../../../packages/workbench/src/api/workbench-api.js").AtlasStyle}} o */
(o) => {
  const api = window.atlasTransitions;
  const d = api.duration(),
    sc = api.schedule();
  const read = () => {
    /** @type {[number, number, number][]} */
    const poses = [];
    for (let i = 0; ; i++) {
      const q = api.poseOf(i);
      if (!q) {
        break;
      }
      // A copy of a pose is the same three numbers.
      poses.push(/** @type {[number, number, number]} */ (q.slice()));
    }
    return poses;
  };
  /** @param {number} u */
  const at = (u) => {
    api.seek(sc.moveStart + (sc.moveEnd - sc.moveStart) * u);
    return read();
  };
  api.seek(d);
  const end = read();
  const start = at(0);
  const path = [];
  for (let s = 1; s <= o.samples; s++) {
    path.push(at(s / o.samples));
  }
  const lock = at(o.lockAt);

  // Outcome: where the free run had got to when the lock-in took over.
  let residual = 0,
    turn = 0,
    sum = 0,
    count = 0;
  for (let i = 0; i < end.length; i++) {
    const lockPose = lock[i];
    if (!lockPose) {
      continue;
    }
    // `i` is inside `end`, so its pose is there.
    const endPose = /** @type {[number, number, number]} */ (end[i]);
    const r = Math.hypot(lockPose[0] - endPose[0], lockPose[1] - endPose[1]);
    if (r > residual) {
      residual = r;
    }
    sum += r;
    count++;
    let da = Math.abs(lockPose[2] - endPose[2]) % 90;
    if (da > 45) {
      da = 90 - da;
    }
    if (da > turn) {
      turn = da;
    }
  }

  // Motion: how the journey went.
  let wander = 0,
    jerk = 0;
  for (let i = 0; i < end.length; i++) {
    const startPose = start[i];
    if (!startPose) {
      continue;
    }
    // `i` is inside `end`, so its pose is there.
    const endPose = /** @type {[number, number, number]} */ (end[i]);
    const vx = endPose[0] - startPose[0],
      vy = endPose[1] - startPose[1];
    const len2 = vx * vx + vy * vy;
    let prev = startPose;
    for (const frame of path) {
      const q = frame[i];
      if (!q) {
        continue;
      }
      const px = q[0] - startPose[0],
        py = q[1] - startPose[1];
      const u = len2 > 1e-12 ? Math.max(0, Math.min(1, (px * vx + py * vy) / len2)) : 0;
      const off = Math.hypot(px - vx * u, py - vy * u);
      if (off > wander) {
        wander = off;
      }
      const step = Math.hypot(q[0] - prev[0], q[1] - prev[1]);
      if (step > jerk) {
        jerk = step;
      }
      prev = q;
    }
  }
  // The deepest overlap the run reached, which the page measures for its own readout.
  const built = api.physics(api.state().pair, o.style);
  api.seek(d);
  return {
    squares: end.length,
    residual: residual,
    mean: count ? sum / count : 0,
    turn: turn,
    wander: wander,
    jerk: jerk,
    overlap: built.maxPenetration === undefined ? 0 : built.maxPenetration,
    ms: built.ms === undefined ? 0 : built.ms,
  };
};
