import { type AnimationSample, sampleAnimation } from "../animation/trace.ts";
import {
  type AnimationDocument,
  type AnimationFrame,
  decodeAnimation,
  decodeLegacyAnimation,
  encodeAnimation,
} from "../data/animation.ts";

export interface FrameEdit {
  t?: number;
  side?: number;
  label?: string | null;
  squares?: AnimationFrame["squares"];
}

/** Editing re-enters the same import boundary; cached assessments cannot survive a pose edit. */
export class AnimationEditor {
  #document: AnimationDocument | null = null;
  #time = 0;
  #revision = 0;

  get revision(): number {
    return this.#revision;
  }

  get logicalTime(): number {
    return this.#time;
  }

  get loaded(): boolean {
    return this.#document !== null;
  }

  document(): AnimationDocument {
    if (this.#document === null) {
      throw new Error("load an animation before editing it");
    }
    // Consumers edit through methods, not by retaining references to checked geometry.
    return decodeAnimation(JSON.parse(encodeAnimation(this.#document)));
  }

  load(text: string, legacy = false): AnimationDocument {
    const value: unknown = JSON.parse(text);
    const decoded = legacy ? decodeLegacyAnimation(value) : decodeAnimation(value);
    this.#document = decoded;
    this.#time = 0;
    this.#revision++;
    return this.document();
  }

  export(): string {
    if (this.#document === null) {
      throw new Error("load an animation before exporting it");
    }
    return encodeAnimation(this.#document);
  }

  seek(logicalTime: number): AnimationSample {
    if (this.#document === null) {
      throw new Error("load an animation before seeking");
    }
    const sampled = sampleAnimation(this.#document, logicalTime);
    this.#time = Math.max(0, Math.min(1, logicalTime));
    return sampled;
  }

  sample(): AnimationSample {
    return this.seek(this.#time);
  }

  #replace(document: AnimationDocument): void {
    const checked = decodeAnimation(JSON.parse(encodeAnimation(document)));
    this.#document = checked;
    this.#revision++;
  }

  editFrame(index: number, edit: FrameEdit): void {
    const document = this.document();
    const original = document.frames[index];
    if (original === undefined) {
      throw new RangeError("selected animation frame does not exist");
    }
    const geometryChanged = edit.side !== undefined || edit.squares !== undefined;
    document.frames[index] = {
      ...original,
      ...edit,
      // A geometric edit creates a candidate; a retained-record tag is no longer accurate.
      claimedFeasible: geometryChanged ? null : original.claimedFeasible,
      record: geometryChanged ? null : original.record,
    };
    this.#replace(document);
  }

  setDuration(seconds: number): void {
    this.#replace({ ...this.document(), durationSeconds: seconds });
  }

  duplicateFrame(index: number, logicalTime: number): void {
    const document = this.document();
    const original = document.frames[index];
    if (original === undefined) {
      throw new RangeError("selected animation frame does not exist");
    }
    document.frames.splice(index + 1, 0, { ...original, t: logicalTime });
    this.#replace(document);
  }

  removeFrame(index: number): void {
    const document = this.document();
    if (!Number.isSafeInteger(index) || index < 0 || index >= document.frames.length) {
      throw new RangeError("selected animation frame does not exist");
    }
    document.frames.splice(index, 1);
    this.#replace(document);
  }
}

export interface AnimationPlaybackClock {
  now(): number;
  request(callback: (milliseconds: number) => void): number;
  cancel(handle: number): void;
}

/** One cancellable clock adapter; revision checks prevent stale playback after import or edit. */
export class AnimationPlayback {
  #handle: number | null = null;
  #generation = 0;
  #playing = false;
  readonly editor: AnimationEditor;
  readonly clock: AnimationPlaybackClock;
  readonly draw: (sample: AnimationSample) => void;
  readonly changed: (playing: boolean) => void;

  constructor(
    editor: AnimationEditor,
    clock: AnimationPlaybackClock,
    draw: (sample: AnimationSample) => void,
    changed: (playing: boolean) => void,
  ) {
    this.editor = editor;
    this.clock = clock;
    this.draw = draw;
    this.changed = changed;
  }

  get playing(): boolean {
    return this.#playing;
  }

  pause(): void {
    this.#generation++;
    this.#playing = false;
    if (this.#handle !== null) {
      this.clock.cancel(this.#handle);
      this.#handle = null;
    }
    this.changed(false);
  }

  play(reducedMotion: boolean): void {
    this.pause();
    const duration = this.editor.document().durationSeconds ?? 5;
    if (reducedMotion) {
      this.draw(this.editor.seek(1));
      return;
    }
    const revision = this.editor.revision;
    const generation = this.#generation;
    const from = this.editor.logicalTime >= 1 ? 0 : this.editor.logicalTime;
    const started = this.clock.now();
    this.#playing = true;
    this.changed(true);
    const tick = (milliseconds: number): void => {
      if (generation !== this.#generation || revision !== this.editor.revision) {
        if (generation === this.#generation) {
          this.pause();
        }
        return;
      }
      const time = Math.min(1, from + (milliseconds - started) / (duration * 1000));
      this.draw(this.editor.seek(time));
      if (time >= 1) {
        this.pause();
      } else {
        this.#handle = this.clock.request(tick);
      }
    };
    this.#handle = this.clock.request(tick);
  }
}
