import assert from "node:assert/strict";
import { test } from "node:test";
import {
  type KeyChord,
  type PackKeyCommand,
  packKeyCommand,
  reducedMotionAction,
  stageDescription,
  stageKeyCommand,
} from "../src/view/accessibility.ts";

test("the stage description states the current mode, packing, and activity", () => {
  assert.equal(
    stageDescription({
      aspect: "pack",
      n: 17,
      squareCount: 17,
      containerSide: 4.675,
      playing: false,
      edited: true,
    }),
    "Pack mode shows n = 17. 17 squares are inside a container of side 4.6750. Playback is paused. The arrangement has been edited by hand.",
  );
  assert.match(
    stageDescription({
      aspect: "animate",
      n: 29,
      squareCount: 29,
      containerSide: 5.8,
      playing: true,
      edited: false,
    }),
    /Animate mode.*transition is playing/,
  );
});

test("stage keys enter the square layer and move or rotate the focused square", () => {
  assert.deepEqual(stageKeyCommand("Enter", false, false), { kind: "focus-square" });
  assert.deepEqual(stageKeyCommand("ArrowLeft", false, true), {
    kind: "move-square",
    dx: -0.05,
    dy: 0,
  });
  assert.deepEqual(stageKeyCommand("ArrowUp", true, true), {
    kind: "move-square",
    dx: 0,
    dy: 0.2,
  });
  assert.deepEqual(stageKeyCommand("q", false, true), {
    kind: "rotate-square",
    degrees: -15,
  });
  assert.deepEqual(stageKeyCommand("Escape", false, true), { kind: "leave-square" });
  assert.equal(stageKeyCommand("ArrowRight", false, false), null);
});

test("reduced motion turns transport into one discrete visible result", () => {
  assert.equal(
    reducedMotionAction({
      aspect: "pack",
      optimizing: false,
      pairIndex: 16,
      firstPairIndex: 16,
      lastPairIndex: 16,
      atPairEnd: false,
    }),
    "initialize-pack",
  );
  assert.equal(
    reducedMotionAction({
      aspect: "pack",
      optimizing: true,
      pairIndex: 16,
      firstPairIndex: 16,
      lastPairIndex: 16,
      atPairEnd: false,
    }),
    "step-pack",
  );
  assert.equal(
    reducedMotionAction({
      aspect: "animate",
      optimizing: false,
      pairIndex: 15,
      firstPairIndex: 15,
      lastPairIndex: 17,
      atPairEnd: false,
    }),
    "finish-pair",
  );
  assert.equal(
    reducedMotionAction({
      aspect: "animate",
      optimizing: false,
      pairIndex: 15,
      firstPairIndex: 15,
      lastPairIndex: 17,
      atPairEnd: true,
    }),
    "finish-next-pair",
  );
  assert.equal(
    reducedMotionAction({
      aspect: "animate",
      optimizing: false,
      pairIndex: 17,
      firstPairIndex: 15,
      lastPairIndex: 17,
      atPairEnd: true,
    }),
    "restart-and-finish",
  );
});

function chord(key: string, modifiers: Partial<Omit<KeyChord, "key">> = {}): KeyChord {
  return { key, shiftKey: false, ctrlKey: false, metaKey: false, altKey: false, ...modifiers };
}

test("the Pack square keys move, rotate, cycle and leave with Pack's own strides", () => {
  // Five degrees, written the way the panel has always applied it.
  const rotation = Math.PI / 36;
  const expected: [string, PackKeyCommand][] = [
    ["ArrowLeft", { kind: "move-square", dx: -0.05, dy: 0 }],
    ["ArrowRight", { kind: "move-square", dx: 0.05, dy: 0 }],
    ["ArrowUp", { kind: "move-square", dx: 0, dy: 0.05 }],
    ["ArrowDown", { kind: "move-square", dx: 0, dy: -0.05 }],
    ["q", { kind: "rotate-square", radians: -rotation }],
    ["Q", { kind: "rotate-square", radians: -rotation }],
    ["e", { kind: "rotate-square", radians: rotation }],
    ["E", { kind: "rotate-square", radians: rotation }],
    ["PageDown", { kind: "cycle-square", offset: 1 }],
    ["]", { kind: "cycle-square", offset: 1 }],
    ["PageUp", { kind: "cycle-square", offset: -1 }],
    ["[", { kind: "cycle-square", offset: -1 }],
    ["Escape", { kind: "leave-square" }],
  ];
  for (const [key, command] of expected) {
    assert.deepEqual(packKeyCommand(chord(key), true), command, key);
  }
  for (const key of ["Enter", " ", "x", "Tab", "Home"]) {
    assert.equal(packKeyCommand(chord(key), true), null, key);
  }
});

test("Shift selects the coarse Pack stride and leaves every other square key alone", () => {
  assert.deepEqual(packKeyCommand(chord("ArrowLeft", { shiftKey: true }), true), {
    kind: "move-square",
    dx: -0.25,
    dy: 0,
  });
  assert.deepEqual(packKeyCommand(chord("ArrowRight", { shiftKey: true }), true), {
    kind: "move-square",
    dx: 0.25,
    dy: 0,
  });
  assert.deepEqual(packKeyCommand(chord("ArrowUp", { shiftKey: true }), true), {
    kind: "move-square",
    dx: 0,
    dy: 0.25,
  });
  assert.deepEqual(packKeyCommand(chord("ArrowDown", { shiftKey: true }), true), {
    kind: "move-square",
    dx: 0,
    dy: -0.25,
  });
  // Shift+Q arrives as "Q": the aria-label promises Q and E rotate, so both cases do.
  for (const key of ["q", "Q", "e", "E", "PageDown", "PageUp", "]", "[", "Escape"]) {
    assert.deepEqual(
      packKeyCommand(chord(key, { shiftKey: true }), true),
      packKeyCommand(chord(key), true),
      key,
    );
  }
});

test("the Pack stage keys enter the square layer and toggle playback", () => {
  assert.deepEqual(packKeyCommand(chord("Enter"), false), { kind: "focus-square" });
  assert.deepEqual(packKeyCommand(chord(" "), false), { kind: "toggle-playback" });
  for (const key of ["ArrowLeft", "q", "PageDown", "]", "Escape", "x"]) {
    assert.equal(packKeyCommand(chord(key), false), null, key);
  }
});

test("a Pack shortcut is a bare key: Ctrl, Meta and Alt chords belong to the browser", () => {
  const squareKeys = ["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "q", "Q", "e", "E"];
  squareKeys.push("PageDown", "PageUp", "]", "[", "Escape");
  const modifiers: Partial<Omit<KeyChord, "key">>[] = [
    { ctrlKey: true },
    { metaKey: true },
    { altKey: true },
    { ctrlKey: true, shiftKey: true },
    { metaKey: true, shiftKey: true },
    { altKey: true, shiftKey: true },
    { ctrlKey: true, altKey: true },
  ];
  for (const modifier of modifiers) {
    for (const key of squareKeys) {
      assert.equal(
        packKeyCommand(chord(key, modifier), true),
        null,
        `${key} ${JSON.stringify(modifier)}`,
      );
    }
    for (const key of ["Enter", " "]) {
      assert.equal(
        packKeyCommand(chord(key, modifier), false),
        null,
        `${key} ${JSON.stringify(modifier)}`,
      );
    }
  }
});
