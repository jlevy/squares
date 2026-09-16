import type { AnimationSample } from "../animation/trace.js";
import { sampleAnimation } from "../animation/trace.ts";
import type { AnimationPanelState } from "../api/animation-api.js";
import {
  ANIMATION_CONTRACT,
  type AnimationDocument,
  decodeAnimationPose,
} from "../data/animation.ts";
import { paintAnimation } from "../view/animation-scene.ts";
import type { ColourSystem } from "../view/colour.js";
import { renderStage, sceneSvg } from "../view/stage-renderer.ts";
import { AnimationEditor, AnimationPlayback } from "./animation-editor.ts";
import { captureIllustration } from "./capture.ts";

const MAX_IMPORT_BYTES = 8 * 1024 * 1024;
const SVG_NS = "http://www.w3.org/2000/svg";

export interface AnimationPanel {
  setVisible(visible: boolean): void;
  load(text: string, legacy?: boolean): AnimationPanelState;
  seek(time: number): AnimationPanelState;
  togglePlayback(): void;
  leave(): void;
  redraw(): void;
  state(): AnimationPanelState;
  export(): string;
  svg(): string;
}

export interface AnimationPanelOptions {
  document: Document;
  colours: ColourSystem;
  enter(): void;
  restore(): void;
  reducedMotion(): boolean;
}

function element<T extends Element>(
  document: Document,
  id: string,
  type: new (...args: never[]) => T,
): T {
  const found = document.getElementById(id);
  if (!(found instanceof type)) {
    throw new Error(`animation editor needs ${id}`);
  }
  return found;
}

function download(document: Document, name: string, text: string, mime: string): void {
  const url = URL.createObjectURL(new Blob([text], { type: mime }));
  const link = document.createElement("a");
  link.href = url;
  link.download = name;
  link.click();
  // The click starts asynchronously in WebKit; retain the URL until the browser has consumed it.
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

/** DOM ownership is confined to this adapter. The editor, clock and renderer also run in Node. */
export function mountAnimationPanel(options: AnimationPanelOptions): AnimationPanel {
  const { document, colours } = options;
  const root = element(document, "animation-editor", HTMLElement);
  const status = element(document, "animation-status", HTMLOutputElement);
  const input = element(document, "animation-json", HTMLTextAreaElement);
  const legacy = element(document, "animation-legacy", HTMLInputElement);
  const file = element(document, "animation-file", HTMLInputElement);
  const time = element(document, "animation-time", HTMLInputElement);
  const frames = element(document, "animation-frame", HTMLSelectElement);
  const frameTime = element(document, "animation-frame-time", HTMLInputElement);
  const frameSide = element(document, "animation-frame-side", HTMLInputElement);
  const frameLabel = element(document, "animation-frame-label", HTMLInputElement);
  const poses = element(document, "animation-poses", HTMLTextAreaElement);
  const duration = element(document, "animation-duration", HTMLInputElement);
  const play = element(document, "animation-play", HTMLButtonElement);
  const stage = element(document, "packing-svg", SVGSVGElement);
  const world = element(document, "world", SVGGElement);
  const catalogueSquares = element(document, "squares", SVGGElement);
  const traceSquares = document.createElementNS(SVG_NS, "g");
  traceSquares.id = "animation-squares";
  traceSquares.style.display = "none";
  world.append(traceSquares);
  const squareNodes = new Map<number, { node: SVGGElement; shape: SVGRectElement }>();
  const targets = {
    svg: stage,
    containerRect: element(document, "container", SVGRectElement),
    squares: squareNodes,
    mark: element(document, "mark", SVGGElement),
    markShape:
      element(document, "mark", SVGGElement).querySelector("rect") ??
      document.createElementNS(SVG_NS, "rect"),
    links: element(document, "links", SVGGElement),
    ghost: element(document, "ghost", SVGGElement),
  };
  const editor = new AnimationEditor();
  let current: AnimationDocument | null = null;
  let active = false;
  let importGeneration = 0;
  let lastSample: AnimationSample | null = null;
  let captureGeneration = 0;

  function draw(sample: AnimationSample): void {
    if (!active || current === null) {
      return;
    }
    for (const identity of sample.squareIds) {
      if (!squareNodes.has(identity)) {
        const node = document.createElementNS(SVG_NS, "g");
        node.dataset.identity = String(identity);
        const shape = document.createElementNS(SVG_NS, "rect");
        for (const [key, value] of Object.entries({
          x: "-0.5",
          y: "-0.5",
          width: "1",
          height: "1",
          stroke: "#000000",
          "stroke-width": "1.5",
          "vector-effect": "non-scaling-stroke",
        })) {
          shape.setAttribute(key, value);
        }
        node.append(shape);
        traceSquares.append(node);
        squareNodes.set(identity, { node, shape });
      }
    }
    renderStage(targets, paintAnimation(sample, current, colours));
    lastSample = sample;
    time.value = String(editor.logicalTime);
    status.value = `${current.name} · n = ${sample.n} · ${sample.guided ? "guided history" : "no recorded guidance"} · ${sample.interpolated ? "interpolated illustration" : sample.assessment?.valid === true ? "geometry passes numerical checks" : "invalid packing geometry"}${sample.label === null ? "" : ` · ${sample.label}`}`;
    element(document, "stage-accessible-description", HTMLElement).textContent = status.value;
  }
  const playback = new AnimationPlayback(
    editor,
    {
      now: () => performance.now(),
      request: (callback) => requestAnimationFrame(callback),
      cancel: (handle) => cancelAnimationFrame(handle),
    },
    draw,
    (playing) => {
      play.textContent = playing ? "Pause trace" : "Play trace";
      play.setAttribute("aria-pressed", String(playing));
    },
  );

  function selectedFrame(): number {
    const index = Number(frames.value);
    if (!Number.isSafeInteger(index) || current?.frames[index] === undefined) {
      throw new RangeError("select an animation frame");
    }
    return index;
  }

  function showFrame(): void {
    const frame = current?.frames[selectedFrame()];
    if (frame === undefined) {
      return;
    }
    frameTime.value = String(frame.t);
    frameSide.value = String(frame.side);
    frameLabel.value = frame.label ?? "";
    poses.value = JSON.stringify(
      frame.squares.map((pose) => [pose.x, pose.y, pose.angle]),
      null,
      2,
    );
  }

  function refresh(): void {
    current = editor.document();
    const selected = Math.min(Number(frames.value) || 0, current.frames.length - 1);
    frames.replaceChildren(
      ...current.frames.map((frame, index) => {
        const option = document.createElement("option");
        option.value = String(index);
        option.textContent = `${index + 1} · t = ${frame.t}${frame.label === null ? "" : ` · ${frame.label}`}`;
        return option;
      }),
    );
    frames.value = String(selected);
    duration.value = String(current.durationSeconds ?? 5);
    element(document, "animation-loaded", HTMLFieldSetElement).disabled = false;
    showFrame();
    draw(editor.sample());
  }

  function guarded(action: () => void): void {
    try {
      action();
    } catch (error) {
      status.value = error instanceof Error ? error.message : String(error);
    }
  }

  const controller: AnimationPanel = {
    setVisible(visible) {
      root.hidden = !visible;
      if (!visible && active) {
        controller.leave();
      }
    },
    load(text, allowLegacy = false) {
      if (new TextEncoder().encode(text).length > MAX_IMPORT_BYTES) {
        throw new RangeError("animation import is limited to 8 MiB");
      }
      // Validate before changing the scene. A rejected import leaves the last animation intact.
      editor.load(text, allowLegacy);
      importGeneration++;
      captureGeneration++;
      playback.pause();
      options.enter();
      current = editor.document();
      active = true;
      catalogueSquares.style.display = "none";
      traceSquares.style.display = "";
      document.body.classList.add("trace-active");
      refresh();
      return controller.state();
    },
    seek(value) {
      playback.pause();
      draw(editor.seek(value));
      return controller.state();
    },
    togglePlayback() {
      if (playback.playing) {
        playback.pause();
      } else {
        playback.play(options.reducedMotion());
      }
    },
    leave() {
      importGeneration++;
      captureGeneration++;
      playback.pause();
      active = false;
      traceSquares.style.display = "none";
      catalogueSquares.style.display = "";
      document.body.classList.remove("trace-active");
      options.restore();
    },
    redraw() {
      if (active) {
        draw(editor.sample());
      }
    },
    state() {
      return {
        active,
        loaded: editor.loaded,
        playing: playback.playing,
        time: editor.logicalTime,
        durationSeconds: current === null ? null : (current.durationSeconds ?? 5),
        revision: editor.revision,
        n: current?.n ?? null,
        guided: lastSample?.guided ?? null,
        interpolated: lastSample?.interpolated ?? null,
        valid: lastSample?.assessment?.valid ?? null,
      };
    },
    export: () => editor.export(),
    svg() {
      if (current === null) {
        throw new Error("load an animation before exporting it");
      }
      return sceneSvg(paintAnimation(editor.sample(), current, colours));
    },
  };

  async function exportFrames(): Promise<void> {
    const generation = ++captureGeneration;
    const snapshot = editor.document();
    const serialized = editor.export();
    const sourceCommit = document
      .querySelector('meta[name="squares-workbench-revision"]')
      ?.getAttribute("content");
    if (sourceCommit === null || sourceCommit === undefined) {
      throw new Error("Frame capture requires a site build with source identity");
    }
    const dirty =
      document.querySelector('meta[name="squares-workbench-dirty"]')?.getAttribute("content") !==
      "false";
    const buffer = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(serialized));
    const digest = [...new Uint8Array(buffer)]
      .map((value) => value.toString(16).padStart(2, "0"))
      .join("");
    const seconds = snapshot.durationSeconds ?? 5;
    const revision = editor.revision;
    const receipt = await captureIllustration({
      source: {
        commit: sourceCommit,
        inputId: `sha256:${digest}`,
        configurationId: "svg-24fps-endpoint-v1",
      },
      timing: {
        startSeconds: 0,
        durationSeconds: seconds,
        framesPerSecond: 24,
        includeEndpoint: true,
        maxFrames: 300,
      },
      seek: (time) => paintAnimation(sampleAnimation(snapshot, time / seconds), snapshot, colours),
      cancelled: () => generation !== captureGeneration || revision !== editor.revision,
      writeFrame: async (frame) => {
        status.value = `Captured ${frame.index + 1} SVG frames`;
        // Yield for cancellation and navigation; drawing itself remains independent of rAF.
        await new Promise<void>((resolve) => setTimeout(resolve, 0));
      },
    });
    download(
      document,
      "packing-animation-frames.json",
      JSON.stringify(
        {
          schema: "squares.workbench.animation-capture/v1",
          sourceDirty: dirty,
          animation: JSON.parse(serialized) as unknown,
          receipt,
        },
        null,
        2,
      ),
      "application/json",
    );
    if (generation === captureGeneration) {
      status.value = `${receipt.status}: ${receipt.frames.length} of ${receipt.scheduledFrames} frames captured${receipt.error === null ? "" : ` · ${receipt.error}`}`;
    }
  }
  element(document, "animation-frames-export", HTMLButtonElement).addEventListener("click", () => {
    void exportFrames().catch((error: unknown) => {
      status.value = error instanceof Error ? error.message : String(error);
    });
  });
  element(document, "animation-cancel-capture", HTMLButtonElement).addEventListener("click", () => {
    captureGeneration++;
    status.value = "Capture cancelled; the completed frames will be exported.";
  });

  const actions: Record<string, () => void> = {
    "animation-load": () => {
      controller.load(input.value, legacy.checked);
    },
    "animation-example": () => {
      controller.load(
        JSON.stringify({
          contract: ANIMATION_CONTRACT,
          name: "Two-square illustration",
          n: 2,
          duration_seconds: 4,
          palette: { hue: "identity", shade: "evidence" },
          frames: [
            {
              t: 0,
              side: 2,
              squares: [
                [0.5, 0.5, 0],
                [1.5, 1.5, 0],
              ],
              square_ids: [1, 2],
            },
            {
              t: 1,
              side: 2,
              squares: [
                [0.5, 1.5, 0],
                [1.5, 0.5, Math.PI * 2],
              ],
              square_ids: [1, 2],
            },
          ],
        }),
      );
    },
    "animation-catalogue": () => controller.leave(),
    "animation-play": () => controller.togglePlayback(),
    "animation-export": () =>
      download(document, "packing-animation.json", controller.export(), "application/json"),
    "animation-svg": () =>
      download(document, "packing-frame.svg", controller.svg(), "image/svg+xml"),
    "animation-save-frame": () => {
      playback.pause();
      const index = selectedFrame();
      const parsed: unknown = JSON.parse(poses.value);
      if (!Array.isArray(parsed)) {
        throw new TypeError("square poses must be an array");
      }
      editor.editFrame(index, {
        t: Number(frameTime.value),
        side: Number(frameSide.value),
        label: frameLabel.value,
        squares: parsed.map((value: unknown) => decodeAnimationPose(value)),
      });
      refresh();
      controller.seek(Number(frameTime.value));
    },
    "animation-duplicate": () => {
      playback.pause();
      const index = selectedFrame();
      const t = current?.frames[index]?.t;
      if (t === undefined) {
        throw new RangeError("select a frame");
      }
      editor.duplicateFrame(index, t);
      refresh();
    },
    "animation-remove": () => {
      playback.pause();
      editor.removeFrame(selectedFrame());
      refresh();
    },
  };
  for (const [id, action] of Object.entries(actions)) {
    element(document, id, HTMLButtonElement).addEventListener("click", () => guarded(action));
  }
  time.addEventListener("input", () =>
    guarded(() => {
      controller.seek(Number(time.value));
    }),
  );
  frames.addEventListener("change", () =>
    guarded(() => {
      showFrame();
      controller.seek(Number(frameTime.value));
    }),
  );
  duration.addEventListener("change", () =>
    guarded(() => {
      playback.pause();
      editor.setDuration(Number(duration.value));
      refresh();
    }),
  );
  file.addEventListener("change", () => {
    const selected = file.files?.[0];
    if (selected === undefined) {
      return;
    }
    const generation = ++importGeneration;
    if (selected.size > MAX_IMPORT_BYTES) {
      status.value = "animation import is limited to 8 MiB";
      return;
    }
    void selected
      .text()
      .then((text) => {
        if (generation === importGeneration) {
          guarded(() => {
            controller.load(text, legacy.checked);
          });
        }
      })
      .catch((error: unknown) => {
        if (generation === importGeneration) {
          status.value = error instanceof Error ? error.message : String(error);
        }
      });
  });
  return controller;
}
