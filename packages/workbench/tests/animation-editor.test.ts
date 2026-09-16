import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import {
  AnimationEditor,
  AnimationPlayback,
  type AnimationPlaybackClock,
} from "../src/app/animation-editor.ts";
import { decodeAnimation } from "../src/data/animation.ts";

const fixture = readFileSync(
  new URL("./fixtures/packing-animation-v1.json", import.meta.url),
  "utf8",
);

test("pose edits discard retained claims, recheck geometry, and preserve guide ancestry", () => {
  const editor = new AnimationEditor();
  editor.load(fixture);
  editor.editFrame(2, {
    squares: [
      { x: 0.5, y: 0.5, angle: 0 },
      { x: 0.5, y: 0.5, angle: 0 },
    ],
  });
  let frame = editor.document().frames[2];
  assert.equal(frame?.assessment.valid, false);
  assert.equal(frame?.claimedFeasible, null);
  assert.equal(frame?.record, null);
  assert.equal(frame?.guided, true);
  editor.removeFrame(1);
  frame = decodeAnimation(JSON.parse(editor.export())).frames[1];
  assert.equal(frame?.guided, true);
});

test("a rejected edit leaves the last checked animation and revision intact", () => {
  const editor = new AnimationEditor();
  editor.load(fixture);
  const before = editor.export();
  const revision = editor.revision;
  assert.throws(() => editor.editFrame(0, { side: Number.NaN }), /finite/);
  assert.throws(() => editor.editFrame(0, { squares: [] }), /preserve n/);
  assert.throws(() => editor.duplicateFrame(0, 0.9), /nondecreasing/);
  assert.equal(editor.export(), before);
  assert.equal(editor.revision, revision);
  const view = editor.document();
  view.frames.length = 0;
  assert.equal(editor.document().frames.length, 3);
});

class Clock implements AnimationPlaybackClock {
  time = 0;
  next = 0;
  readonly callbacks = new Map<number, (milliseconds: number) => void>();
  now(): number {
    return this.time;
  }
  request(callback: (milliseconds: number) => void): number {
    const handle = ++this.next;
    this.callbacks.set(handle, callback);
    return handle;
  }
  cancel(handle: number): void {
    this.callbacks.delete(handle);
  }
  tick(milliseconds: number): void {
    this.time = milliseconds;
    const callbacks = [...this.callbacks.values()];
    this.callbacks.clear();
    for (const callback of callbacks) {
      callback(milliseconds);
    }
  }
}

test("playback uses duration, stops at the endpoint, and honors reduced motion", () => {
  const editor = new AnimationEditor();
  editor.load(fixture);
  const clock = new Clock();
  let draws = 0;
  const player = new AnimationPlayback(
    editor,
    clock,
    () => {
      draws++;
    },
    () => {},
  );
  player.play(false);
  clock.tick(1750);
  assert.equal(editor.logicalTime, 0.5);
  assert.equal(player.playing, true);
  clock.tick(3500);
  assert.equal(editor.logicalTime, 1);
  assert.equal(player.playing, false);
  assert.equal(clock.callbacks.size, 0);
  player.play(true);
  assert.equal(editor.logicalTime, 1);
  assert.equal(draws, 3);
  assert.equal(clock.callbacks.size, 0);
});

test("queued playback cannot overwrite a new import or a restarted clock", () => {
  const editor = new AnimationEditor();
  editor.load(fixture);
  const clock = new Clock();
  let draws = 0;
  const player = new AnimationPlayback(
    editor,
    clock,
    () => {
      draws++;
    },
    () => {},
  );
  player.play(false);
  editor.load(fixture);
  clock.tick(1000);
  assert.equal(draws, 0);
  assert.equal(player.playing, false);
  player.play(false);
  const stale = [...clock.callbacks.values()][0];
  assert.ok(stale !== undefined);
  player.play(false);
  stale(2000);
  assert.equal(draws, 0);
  assert.equal(player.playing, true);
});
