import { type PackWorkbenchApi, parsePackSnapshot } from "../api/pack-api.ts";
import type { GeometrySnapshot } from "../core/geometry.ts";
import {
  assessPackingSnapshot,
  type PackingAssessment,
  parseUint32Seed,
} from "../core/runtime-contracts.ts";
import { packKeyCommand } from "../view/accessibility.ts";
import type { ColourSystem } from "../view/colour.ts";
import { paintPack } from "../view/pack-scene.ts";
import { renderStage, type StageTargets } from "../view/stage-renderer.ts";
import { PackController } from "./pack-controller.ts";

const SVG_NS = "http://www.w3.org/2000/svg";
const MIN_COUNT = 1;
const MAX_COUNT = 400;
const MAX_STEPS_PER_FRAME = 8;
const RESOLVE_ITERATIONS = 100;

export interface PackPanel extends PackWorkbenchApi {
  setVisible(visible: boolean): void;
  visible(): boolean;
  redraw(): void;
}

export interface PackPanelOptions {
  document: Document;
  colours: ColourSystem;
  reducedMotion(): boolean;
  onChange(): void;
}

function element<T extends Element>(
  document: Document,
  id: string,
  type: new (...args: never[]) => T,
): T {
  const found = document.getElementById(id);
  if (!(found instanceof type)) {
    throw new Error(`Pack panel needs #${id}`);
  }
  return found;
}

function cloneSnapshot(snapshot: GeometrySnapshot): GeometrySnapshot {
  return {
    squareSide: snapshot.squareSide,
    container: { ...snapshot.container },
    poses: snapshot.poses.map((pose) => ({ ...pose })),
  };
}

/** Two snapshots place every square identically, so committing one over the other changes nothing. */
function samePlacement(left: GeometrySnapshot, right: GeometrySnapshot): boolean {
  return (
    left.poses.length === right.poses.length &&
    left.poses.every((pose, index) => {
      const other = right.poses[index];
      return (
        other !== undefined &&
        pose.x === other.x &&
        pose.y === other.y &&
        pose.angle === other.angle
      );
    })
  );
}

export interface PackValidityText {
  valid: boolean;
  /** The side, named for what it is: a packing's required side, or only a bounding box's. */
  side: string;
  /** The validity clause for the status line. */
  status: string;
  /** The validity line for the stage facts. */
  fact: string;
}

/**
 * What the Pack readouts say about an assessment. Every word comes from the one validity
 * contract: the arrangement is a packing only where `assessment.valid`, and otherwise its side is
 * a bounding box's and the first failing clause says why (#160 R12: the stage facts printed
 * "Required side" and a bare overlap for arrangements that were not packings).
 */
export function describePackValidity(assessment: PackingAssessment): PackValidityText {
  const side = Number.isFinite(assessment.requiredSide)
    ? assessment.requiredSide.toFixed(6)
    : "unavailable";
  if (assessment.valid) {
    return {
      valid: true,
      side: `required side ${side}`,
      status: "valid unit packing",
      fact: "Valid unit packing",
    };
  }
  const detail =
    assessment.reason === "unit-size"
      ? `not unit squares (side ${assessment.snapshot.squareSide.toFixed(4)})`
      : assessment.reason === "pair-overlap"
        ? `pair overlap ${assessment.maxPairOverlap.toExponential(2)}`
        : assessment.reason === "wall-overlap"
          ? `wall overlap ${assessment.maxWallOverlap.toExponential(2)}`
          : `${assessment.reason ?? "unchecked"}`;
  return {
    valid: false,
    side: `bounding side ${side}`,
    status: assessment.reason === "unit-size" ? detail : `not a valid packing (${detail})`,
    fact: `Not a packing: ${detail}`,
  };
}

/** Write text only when it differs, so an unchanged frame is no DOM mutation at all. */
function show(node: HTMLElement, text: string): void {
  if (node.textContent !== text) {
    node.textContent = text;
  }
}

function download(document: Document, name: string, content: string): void {
  const url = URL.createObjectURL(new Blob([content], { type: "application/json" }));
  const link = document.createElement("a");
  link.href = url;
  link.download = name;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

/** One DOM owner for Pack; the numerical controller and painter remain browser-free. */
export function mountPackPanel(options: PackPanelOptions): PackPanel {
  const { document, colours } = options;
  const root = element(document, "pack-workspace", HTMLElement);
  const status = element(document, "pack-status", HTMLOutputElement);
  const repairStatus = element(document, "pack-repair-status", HTMLOutputElement);
  const stageFacts = element(document, "pack-stage-facts", HTMLElement);
  const announcement = element(document, "pack-announcement", HTMLElement);
  const stageDescription = element(document, "stage-accessible-description", HTMLElement);
  const count = element(document, "pack-count", HTMLInputElement);
  const seed = element(document, "pack-seed", HTMLInputElement);
  const start = element(document, "pack-start", HTMLSelectElement);
  const shake = element(document, "pack-shake", HTMLInputElement);
  const shakeValue = element(document, "pack-shake-value", HTMLOutputElement);
  const json = element(document, "pack-json", HTMLTextAreaElement);
  const stage = element(document, "stage", HTMLElement);
  const svg = element(document, "packing-svg", SVGSVGElement);
  const world = element(document, "world", SVGGElement);
  const catalogueSquares = element(document, "squares", SVGGElement);
  const packSquares = document.createElementNS(SVG_NS, "g");
  packSquares.id = "pack-squares";
  packSquares.style.display = "none";
  world.append(packSquares);
  const squareNodes = new Map<number, { node: SVGGElement; shape: SVGRectElement }>();
  const targets: StageTargets = {
    svg,
    containerRect: element(document, "container", SVGRectElement),
    squares: squareNodes,
    mark: element(document, "mark", SVGGElement),
    markShape:
      element(document, "mark", SVGGElement).querySelector("rect") ??
      document.createElementNS(SVG_NS, "rect"),
    links: element(document, "links", SVGGElement),
    ghost: element(document, "ghost", SVGGElement),
  };
  const controller = new PackController();
  let active = false;
  let playing = false;
  let frameHandle: number | null = null;
  let generation = 0;
  let lastFrame: number | null = null;
  let focusedIndex = 0;
  let preview: GeometrySnapshot | null = null;
  let drag: {
    index: number;
    x: number;
    y: number;
    pose: GeometrySnapshot["poses"][number];
  } | null = null;

  function nodeFor(index: number): void {
    const identity = index + 1;
    if (squareNodes.has(identity)) {
      return;
    }
    const node = document.createElementNS(SVG_NS, "g");
    node.classList.add("pack-sq");
    node.dataset.packIndex = String(index);
    node.dataset.identity = String(identity);
    node.setAttribute("role", "button");
    const shape = document.createElementNS(SVG_NS, "rect");
    for (const [key, value] of Object.entries({
      x: "-0.5",
      y: "-0.5",
      width: "1",
      height: "1",
      stroke: "#000000",
      "stroke-width": "1.5",
      "stroke-linejoin": "round",
      "vector-effect": "non-scaling-stroke",
    })) {
      shape.setAttribute(key, value);
    }
    node.append(shape);
    packSquares.append(node);
    squareNodes.set(identity, { node, shape });
  }

  function redraw(): void {
    if (!active) {
      return;
    }
    const current = controller.state();
    const snapshot = preview ?? current.snapshot;
    for (const [identity, { node }] of squareNodes) {
      if (identity > snapshot.poses.length) {
        node.remove();
        squareNodes.delete(identity);
      }
    }
    for (let index = 0; index < snapshot.poses.length; index += 1) {
      nodeFor(index);
    }
    renderStage(targets, paintPack(snapshot, colours));
    focusedIndex = Math.min(focusedIndex, snapshot.poses.length - 1);
    for (const [identity, { node }] of squareNodes) {
      const index = identity - 1;
      node.setAttribute("tabindex", index === focusedIndex ? "0" : "-1");
      node.setAttribute(
        "aria-label",
        `Square ${identity} of ${snapshot.poses.length}; Page Up and Page Down select squares, arrow keys move, Q and E rotate`,
      );
    }
    const assessment =
      preview === null ? current.assessment : assessPackingSnapshot(preview, preview.poses.length);
    const readout = describePackValidity(assessment);
    const steps = current.latest?.work.baseSteps ?? 0;
    show(
      status,
      `n = ${current.configuration.n} · seed ${current.configuration.seed} · ${steps} steps · ${readout.side} · ${readout.status} · ${preview === null ? (playing ? "running" : "paused") : "drag preview"}`,
    );
    const repair = current.repair;
    show(
      repairStatus,
      repair === null
        ? ""
        : `Resolve ${repair.termination.reason}: raw side ${repair.raw.requiredSide.toFixed(6)}, repaired side ${repair.repaired?.requiredSide.toFixed(6) ?? "unavailable"}; ${repair.termination.resolved ? "checked repair shown" : "raw arrangement retained"}`,
    );
    show(
      stageFacts,
      `n = ${current.configuration.n}\n${readout.side.charAt(0).toUpperCase()}${readout.side.slice(1)}\n${readout.fact}\n${steps} steps · ${preview === null ? (playing ? "running" : "paused") : "drag preview"}`,
    );
    show(stageDescription, status.value);
    svg.setAttribute("aria-label", `${current.configuration.n} packing squares`);
  }

  /**
   * Say what changed, once. The status lines and the stage facts are redrawn on every
   * animation frame, so they are not live regions (#160 R16); `#pack-announcement` is, and
   * it is written only here -- on Run, Pause, a step, Restart, Resolve, an import, a
   * settings change, an edit or an error -- never from a frame.
   */
  function announce(): void {
    if (!active) {
      return;
    }
    show(
      announcement,
      [status.value, repairStatus.value].filter((part) => part.length > 0).join(". "),
    );
  }

  /** Stop the frame loop. */
  function halt(): void {
    playing = false;
    generation += 1;
    lastFrame = null;
    if (frameHandle !== null) {
      cancelAnimationFrame(frameHandle);
      frameHandle = null;
    }
  }

  /** Stop and redraw without announcing, for an operation that announces once it is done. */
  function stop(): void {
    halt();
    redraw();
  }

  function pause(): void {
    stop();
    announce();
  }

  function tick(timestamp: number, expectedGeneration: number): void {
    if (!active || !playing || expectedGeneration !== generation) {
      return;
    }
    const elapsed =
      lastFrame === null ? 1 / 60 : Math.max(0, Math.min(0.1, (timestamp - lastFrame) / 1000));
    lastFrame = timestamp;
    const wanted = Math.max(
      1,
      Math.round(elapsed * controller.state().configuration.physics.stepsPerSecond),
    );
    try {
      controller.step(Math.min(MAX_STEPS_PER_FRAME, wanted));
      redraw();
    } catch (error) {
      stop();
      show(status, error instanceof Error ? error.message : String(error));
      announce();
      return;
    }
    frameHandle = requestAnimationFrame((next) => tick(next, expectedGeneration));
  }

  function play(): void {
    if (!active || playing) {
      return;
    }
    if (options.reducedMotion()) {
      controller.step(1);
      redraw();
      announce();
      return;
    }
    playing = true;
    generation += 1;
    frameHandle = requestAnimationFrame((timestamp) => tick(timestamp, generation));
    redraw();
    announce();
  }

  function point(event: PointerEvent): { x: number; y: number } | null {
    const matrix = world.getScreenCTM();
    if (matrix === null) {
      return null;
    }
    const transformed = new DOMPoint(event.clientX, event.clientY).matrixTransform(
      matrix.inverse(),
    );
    return { x: transformed.x, y: transformed.y };
  }

  /**
   * End a pointer gesture. Only a gesture that moved a square is an edit: a press that
   * moved nothing (a click, say, to focus the square) keeps the run -- its time, anneal,
   * retained best and seeded start -- instead of reloading an identical arrangement.
   */
  function commitPreview(): void {
    if (preview === null) {
      return;
    }
    const edited = preview;
    preview = null;
    try {
      if (!samePlacement(edited, controller.export())) {
        controller.load(edited);
        start.value = "given";
      }
    } finally {
      redraw();
    }
    announce();
  }

  const panel: PackPanel = {
    setVisible(visible) {
      if (active === visible) {
        return;
      }
      if (!visible) {
        stop();
        preview = null;
        drag = null;
      }
      active = visible;
      root.hidden = !visible;
      stageFacts.hidden = !visible;
      catalogueSquares.style.display = visible ? "none" : "";
      packSquares.style.display = visible ? "" : "none";
      document.body.classList.toggle("pack-independent", visible);
      if (visible) {
        redraw();
      }
      options.onChange();
    },
    visible: () => active,
    playing: () => playing,
    play,
    pause,
    configure(settings) {
      if (settings.n !== undefined && (settings.n < MIN_COUNT || settings.n > MAX_COUNT)) {
        throw new RangeError(`Pack count must be ${MIN_COUNT}–${MAX_COUNT}`);
      }
      stop();
      const next = controller.configure(settings);
      count.value = String(next.configuration.n);
      seed.value = String(next.configuration.seed);
      start.value = next.configuration.startKind;
      shake.value = String(
        Math.max(0, Math.min(10, Math.round(next.configuration.anneal.amplitude * 3))),
      );
      shakeValue.value = shake.value;
      redraw();
      announce();
      return next;
    },
    step(count) {
      stop();
      controller.step(count);
      redraw();
      announce();
      return controller.state();
    },
    restart() {
      stop();
      controller.restart();
      redraw();
      announce();
      return controller.state();
    },
    resolve() {
      stop();
      const receipt = controller.resolve(RESOLVE_ITERATIONS);
      if (receipt.termination.resolved) {
        start.value = "given";
      }
      redraw();
      announce();
      return receipt;
    },
    load(text) {
      const value: unknown = JSON.parse(text);
      const snapshot = parsePackSnapshot(value);
      if (snapshot.poses.length > MAX_COUNT) {
        throw new RangeError(`Pack supports at most ${MAX_COUNT} squares in this browser`);
      }
      stop();
      controller.load(snapshot);
      start.value = "given";
      count.value = String(snapshot.poses.length);
      redraw();
      announce();
      return controller.state();
    },
    state: () => controller.state(),
    exportSnapshot: () => controller.export(),
    redraw,
  };

  function guarded(action: () => void): void {
    try {
      action();
    } catch (error) {
      show(status, error instanceof Error ? error.message : String(error));
      announce();
    }
  }

  element(document, "pack-run", HTMLButtonElement).addEventListener("click", () => panel.play());
  element(document, "pack-pause", HTMLButtonElement).addEventListener("click", () => panel.pause());
  element(document, "pack-restart", HTMLButtonElement).addEventListener("click", () =>
    panel.restart(),
  );
  element(document, "pack-resolve", HTMLButtonElement).addEventListener("click", () =>
    guarded(() => {
      panel.resolve();
    }),
  );
  element(document, "pack-apply", HTMLButtonElement).addEventListener("click", () =>
    guarded(() => {
      const n = Number(count.value);
      const requestedSeed = seed.value.trim() === "" ? null : parseUint32Seed(Number(seed.value));
      if (!Number.isSafeInteger(n) || n < MIN_COUNT || n > MAX_COUNT) {
        throw new RangeError(`Pack count must be ${MIN_COUNT}–${MAX_COUNT}`);
      }
      if (requestedSeed === null) {
        throw new RangeError("Pack seed must be an unsigned 32-bit integer");
      }
      if (start.value !== "grid" && start.value !== "random") {
        throw new RangeError("select a supported Pack start");
      }
      stop();
      controller.configure({
        n,
        seed: requestedSeed,
        startKind: start.value,
        anneal: { amplitude: Number(shake.value) / 3 },
      });
      redraw();
      announce();
    }),
  );
  element(document, "pack-reset", HTMLButtonElement).addEventListener("click", () => {
    stop();
    count.value = "17";
    seed.value = "1";
    start.value = "grid";
    shake.value = "3";
    shakeValue.value = "3";
    controller.configure({ n: 17, seed: 1, startKind: "grid", anneal: { amplitude: 1 } });
    redraw();
    announce();
  });
  shake.addEventListener("input", () => {
    shakeValue.value = shake.value;
  });
  element(document, "pack-load", HTMLButtonElement).addEventListener("click", () =>
    guarded(() => {
      panel.load(json.value);
    }),
  );
  element(document, "pack-export", HTMLButtonElement).addEventListener("click", () =>
    guarded(() => {
      download(
        document,
        `packing-n${controller.state().configuration.n}.json`,
        JSON.stringify(controller.export(), null, 2),
      );
    }),
  );

  packSquares.addEventListener("pointerdown", (event) => {
    if (!active || !(event.target instanceof Element)) {
      return;
    }
    const square = event.target.closest("g[data-pack-index]");
    const index = Number(square?.getAttribute("data-pack-index"));
    const at = point(event);
    const pose = controller.state().snapshot.poses[index];
    if (square === null || at === null || pose === undefined) {
      return;
    }
    event.preventDefault();
    stop();
    focusedIndex = index;
    drag = { index, x: at.x, y: at.y, pose: { ...pose } };
    preview = cloneSnapshot(controller.export());
    packSquares.setPointerCapture(event.pointerId);
    event.stopPropagation();
    redraw();
  });
  packSquares.addEventListener("pointermove", (event) => {
    if (drag === null || preview === null) {
      return;
    }
    const at = point(event);
    const pose = preview.poses[drag.index];
    if (at === null || pose === undefined) {
      return;
    }
    if (event.shiftKey) {
      pose.angle = drag.pose.angle + (at.x - drag.x) * 0.03;
    } else {
      pose.x = drag.pose.x + at.x - drag.x;
      pose.y = drag.pose.y + at.y - drag.y;
    }
    redraw();
  });
  packSquares.addEventListener("pointerup", (event) => {
    if (drag === null) {
      return;
    }
    if (packSquares.hasPointerCapture(event.pointerId)) {
      packSquares.releasePointerCapture(event.pointerId);
    }
    drag = null;
    guarded(commitPreview);
  });
  packSquares.addEventListener("pointercancel", () => {
    preview = null;
    drag = null;
    redraw();
    announce();
  });
  packSquares.addEventListener("keydown", (event) => {
    if (!(event.target instanceof Element)) {
      return;
    }
    const square = event.target.closest("g[data-pack-index]");
    const index = Number(square?.getAttribute("data-pack-index"));
    if (square === null || !Number.isSafeInteger(index)) {
      return;
    }
    const command = packKeyCommand(event, true);
    if (command === null) {
      return;
    }
    const snapshot = cloneSnapshot(controller.export());
    const pose = snapshot.poses[index];
    if (pose === undefined) {
      return;
    }
    switch (command.kind) {
      case "move-square":
        pose.x += command.dx;
        pose.y += command.dy;
        break;
      case "rotate-square":
        pose.angle += command.radians;
        break;
      case "cycle-square":
        event.preventDefault();
        event.stopPropagation();
        focusedIndex = (index + command.offset + snapshot.poses.length) % snapshot.poses.length;
        redraw();
        squareNodes.get(focusedIndex + 1)?.node.focus();
        return;
      case "leave-square":
        stage.focus();
        event.stopPropagation();
        return;
      default:
        return;
    }
    event.preventDefault();
    event.stopPropagation();
    stop();
    focusedIndex = index;
    guarded(() => {
      controller.load(snapshot);
      start.value = "given";
      redraw();
      announce();
    });
  });
  stage.addEventListener(
    "keydown",
    (event) => {
      if (!active || event.target !== stage) {
        return;
      }
      const command = packKeyCommand(event, false);
      if (command?.kind === "focus-square") {
        event.preventDefault();
        event.stopPropagation();
        squareNodes.get(focusedIndex + 1)?.node.focus();
      } else if (command?.kind === "toggle-playback") {
        event.preventDefault();
        event.stopPropagation();
        if (playing) {
          pause();
        } else {
          play();
        }
      }
    },
    { capture: true },
  );
  return panel;
}
