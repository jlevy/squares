import assert from "node:assert/strict";
import { test } from "node:test";
import {
  annealSpan,
  continuousTiming,
  displayedCount,
  pairDuration,
  pairSchedule,
  pairTiming,
  phaseProgress,
  ramp,
  rangeDuration,
  rangeProgress,
  seekSequence,
  sequenceDuration,
  type TimelineConfiguration,
} from "../src/animation/timeline.ts";

function configuration(): TimelineConfiguration {
  const timing = { dwell: 0.8, move: 0.55, correct: 0.25, settle: 0.8 };
  return {
    pairs: [
      { n: 1, kind: "prefix" },
      { n: 2, kind: "matched" },
      { n: 16, kind: "shared-picture" },
      { n: 17, kind: "matched" },
    ],
    timing,
    continuous: {
      on: true,
      fullBeat: false,
      beat: timing,
      staticBeat: { dwell: 0.4, move: 0.28, correct: 0.12, settle: 0.35 },
    },
    anneal: 3,
    phase: "add-then-move",
    arrivalFraction: 0.3,
    newFraction: 1 / 3,
    rollMax: 0.4,
  };
}

function near(actual: number, expected: number): void {
  assert.ok(Math.abs(actual - expected) < 1e-12, `${actual} != ${expected}`);
}

test("four-span timing preserves correction in single, continuous and annealed paths", () => {
  const config = configuration();
  near(pairDuration(config, 0, "tween"), 1.15);
  near(pairDuration(config, 1, "physics"), 2.4);
  config.anneal = 8;
  near(pairDuration(config, 1, "physics"), 2.8);
  near(pairDuration(config, 1, "tween"), 2.4);
  near(continuousTiming(config, 0, "bodies").correct, 0.12);
  config.continuous.on = false;
  near(pairTiming(config, 0, "bodies").correct, 0.375);
  config.continuous.on = true;
  config.continuous.fullBeat = true;
  near(pairDuration(config, 0, "physics"), 2.8);
  assert.equal(annealSpan("physics", 0), 1);
  assert.equal(annealSpan("tween", 10), 1);
});

test("staging exposes arrival, free movement, correction and facts-panel count", () => {
  const config = configuration();
  const schedule = pairSchedule(config, 1, "tween");
  near(schedule.moveStart, 0.8);
  near(schedule.arrived, 1.04);
  near(schedule.blocksStart, 1.04);
  near(schedule.moveEnd, 1.6);
  near(schedule.end, 2.4);
  assert.equal(displayedCount(2, schedule, 0.99, false), 2);
  assert.equal(displayedCount(2, schedule, 1.01, false), 3);
  assert.equal(displayedCount(2, schedule, 0, true), 3);
  config.phase = "move-then-add";
  const after = pairSchedule(config, 1, "tween");
  near(after.blocksEnd, 1.36);
  near(after.arrive, 1.36);
  near(after.arrived, 1.6);
  config.phase = "simultaneous";
  near(pairSchedule(config, 1, "tween").arrive, 0.8 + (0.8 * 2) / 3);
});

test("rotation-first and slide-first are distinct pure schedules", () => {
  const rotate = phaseProgress("rotate-first", 0.3);
  const slide = phaseProgress("slide-first", 0.3);
  near(rotate.rot, 0.5);
  assert.equal(rotate.slide, 0);
  near(slide.slide, 0.5);
  assert.equal(slide.rot, 0);
  assert.deepEqual(phaseProgress("simultaneous", 0.5), { rot: 0.5, slide: 0.5, e: 0.5 });
});

test("sequence seeking and sparse ranges share endpoint ownership", () => {
  const config = configuration();
  near(sequenceDuration(config, "tween"), 7.1);
  near(rangeDuration(config, { from: 2, to: 18 }, "tween"), 7.1);
  assert.deepEqual(seekSequence(config, "tween", 1.15), { index: 1, time: 0 });
  const end = seekSequence(config, "tween", 999);
  assert.equal(end.index, 3);
  near(end.time, 2.4);
  assert.deepEqual(seekSequence(config, "tween", -10), { index: 0, time: 0 });
  near(rangeProgress(config, { from: 2, to: 18 }, 1, 1.2, "tween", false), 1.5 / 17);
  near(rangeProgress(config, { from: 2, to: 18 }, 3, 0, "tween", true), 1);
  const samples = [0, 0.7, 1.15, 3.55, 7.1];
  assert.deepEqual(
    samples.map((time) => seekSequence(config, "tween", time)),
    [...samples]
      .reverse()
      .map((time) => seekSequence(config, "tween", time))
      .reverse(),
  );
});

test("zero-duration phases remain deterministic and malformed durations fail early", () => {
  const config = configuration();
  config.continuous.on = false;
  config.timing = { dwell: 0, move: 0, correct: 0, settle: 0 };
  assert.deepEqual(seekSequence(config, "tween", 0), { index: 3, time: 0 });
  assert.equal(pairSchedule(config, 0, "tween").roll, 0);
  assert.equal(ramp(0, 0, 0), 1);
  assert.equal(ramp(-1, 0, 0), 0);
  config.timing.correct = Number.NaN;
  assert.throws(() => pairDuration(config, 0, "tween"), /finite/);
  assert.throws(() => annealSpan("physics", 11), /zero and ten/);
  assert.throws(() => seekSequence(configuration(), "tween", Number.NaN), /finite seconds/);
});
