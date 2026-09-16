import type { PaintedSceneFrame, SceneFrame, SceneMark, SceneSquare } from "./scene-types.js";

/** The small browser adapter also makes attribute behavior testable without a DOM emulator. */
export interface AttributeTarget {
  setAttribute(name: string, value: string): void;
}

export interface StageTargets {
  svg: AttributeTarget;
  containerRect: AttributeTarget;
  squares: ReadonlyMap<number, { node: AttributeTarget; shape: AttributeTarget }>;
  mark: AttributeTarget;
  markShape: AttributeTarget;
  links: AttributeTarget;
  ghost: AttributeTarget;
}

function finite(value: number, name: string): void {
  if (!Number.isFinite(value)) {
    throw new RangeError(`${name} must be finite`);
  }
}

function fraction(value: number, name: string): void {
  finite(value, name);
  if (value < 0 || value > 1) {
    throw new RangeError(`${name} must be between zero and one`);
  }
}

function positive(value: number, name: string): void {
  finite(value, name);
  if (value <= 0) {
    throw new RangeError(`${name} must be positive`);
  }
}

function colour(value: string): void {
  if (!/^#[0-9a-f]{6}$/i.test(value)) {
    throw new TypeError("a painted square must have an opaque six-digit hex colour");
  }
}

function checkPose(square: SceneSquare | SceneMark): void {
  finite(square.x, "square x");
  finite(square.y, "square y");
  finite(square.angleDegrees, "square angle in degrees");
  positive(square.scale, "square scale");
  fraction(square.opacity, "square opacity");
}

/** Check the entire frame before mutating any DOM node or producing SVG. */
export function validatePaintedScene(frame: PaintedSceneFrame): void {
  const { scene, fills } = frame;
  positive(scene.containerSide, "container side");
  positive(scene.viewBox.size, "view size");
  finite(scene.viewBox.x, "view x");
  finite(scene.viewBox.y, "view y");
  if (!Number.isSafeInteger(scene.n) || scene.n < 1) {
    throw new RangeError("scene n must be a positive integer");
  }
  if (scene.squares.length !== fills.length) {
    throw new RangeError("paint colours must cover every scene square");
  }
  const identities = new Set<number>();
  for (const [index, square] of scene.squares.entries()) {
    if (square.index !== index || !Number.isSafeInteger(square.identity) || square.identity < 1) {
      throw new RangeError("scene squares must have ordered indices and positive identities");
    }
    if (identities.has(square.identity)) {
      throw new RangeError("scene square identities must be unique");
    }
    identities.add(square.identity);
    checkPose(square);
  }
  for (const fill of fills) {
    colour(fill);
  }
  const presentation = scene.presentation;
  fraction(presentation.drain, "drain");
  fraction(presentation.newTint, "new tint");
  fraction(presentation.resting, "resting");
  fraction(presentation.linksOpacity, "links opacity");
  fraction(presentation.ghostOpacity, "ghost opacity");
  if (presentation.mark !== null) {
    checkPose(presentation.mark);
    positive(presentation.mark.strokeWidth, "mark stroke width");
  }
}

export function squareTransform(square: SceneSquare | SceneMark): string {
  const growth = square.scale === 1 ? "" : ` scale(${square.scale})`;
  return `translate(${square.x} ${square.y}) rotate(${square.angleDegrees})${growth}`;
}

function viewBox(scene: SceneFrame): string {
  const view = scene.viewBox;
  return `${view.x} ${view.y} ${view.size} ${view.size}`;
}

/** Painting has no geometry, simulation, timeline, API, or controller dependency. */
export function renderStage(targets: StageTargets, frame: PaintedSceneFrame): void {
  validatePaintedScene(frame);
  const prepared = frame.scene.squares.map((square, index) => {
    const target = targets.squares.get(square.identity);
    const fill = frame.fills[index];
    if (target === undefined || fill === undefined) {
      throw new RangeError(`stage has no target or colour for identity ${square.identity}`);
    }
    return { square, target, fill };
  });
  targets.svg.setAttribute("viewBox", viewBox(frame.scene));
  targets.containerRect.setAttribute("width", String(frame.scene.containerSide));
  targets.containerRect.setAttribute("height", String(frame.scene.containerSide));
  const visible = new Set(prepared.map(({ square }) => square.identity));
  for (const [identity, target] of targets.squares) {
    target.node.setAttribute("display", visible.has(identity) ? "inline" : "none");
  }
  for (const { square, target, fill } of prepared) {
    target.node.setAttribute("transform", squareTransform(square));
    target.node.setAttribute("opacity", String(square.opacity));
    target.shape.setAttribute("fill", fill);
  }
  const presentation = frame.scene.presentation;
  if (presentation.mark === null) {
    targets.mark.setAttribute("opacity", "0");
  } else {
    targets.mark.setAttribute("opacity", String(presentation.mark.opacity));
    targets.mark.setAttribute("transform", squareTransform(presentation.mark));
    targets.markShape.setAttribute("stroke-width", String(presentation.mark.strokeWidth));
  }
  targets.links.setAttribute("opacity", String(presentation.linksOpacity));
  targets.ghost.setAttribute("opacity", String(presentation.ghostOpacity));
}

/** A portable illustration uses the same view and square transforms as the live stage. */
export function sceneSvg(frame: PaintedSceneFrame): string {
  validatePaintedScene(frame);
  const rectangles = frame.scene.squares.map(
    (square, index) =>
      `<g data-identity="${square.identity}" transform="${squareTransform(square)}" opacity="${square.opacity}"><rect x="-.5" y="-.5" width="1" height="1" fill="${frame.fills[index]}"/></g>`,
  );
  const mark = frame.scene.presentation.mark;
  const outline =
    mark === null
      ? ""
      : `<g transform="${squareTransform(mark)}" opacity="${mark.opacity}"><rect x="-.5" y="-.5" width="1" height="1" fill="none" stroke="#cc3344" stroke-width="${mark.strokeWidth}"/></g>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${viewBox(frame.scene)}" role="img" aria-label="Packing illustration for n = ${frame.scene.n}"><g transform="scale(1 -1)"><rect width="${frame.scene.containerSide}" height="${frame.scene.containerSide}" fill="none" stroke="#444444" stroke-width=".01"/>${rectangles.join("")}${outline}</g></svg>`;
}
