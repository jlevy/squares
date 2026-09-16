import type { GeometrySnapshot } from "../core/geometry.ts";

const DEFAULT_GRID_STEP = 0.1;
const MAX_APPEND_CANDIDATES = 1_000_000;

function finite(value: number, label: string): void {
  if (!Number.isFinite(value)) {
    throw new RangeError(`${label} must be finite`);
  }
}

function positive(value: number, label: string): void {
  finite(value, label);
  if (value <= 0) {
    throw new RangeError(`${label} must be positive`);
  }
}

function validatePrevious(previous: GeometrySnapshot, containerSide: number): void {
  positive(previous.squareSide, "previous square side");
  positive(previous.container.side, "previous container side");
  finite(previous.container.originX, "previous container origin x");
  finite(previous.container.originY, "previous container origin y");
  positive(containerSide, "append container side");
  if (previous.poses.length === 0) {
    throw new RangeError("append proposal needs a nonempty previous packing");
  }
  if (containerSide < previous.container.side || containerSide < previous.squareSide) {
    throw new RangeError("append container cannot be smaller than the previous packing");
  }
  for (const [index, pose] of previous.poses.entries()) {
    finite(pose.x, `previous pose ${index} x`);
    finite(pose.y, `previous pose ${index} y`);
    finite(pose.angle, `previous pose ${index} angle`);
  }
}

function gridCells(containerSide: number, squareSide: number, gridStep: number): number {
  positive(gridStep, "append grid step");
  const span = containerSide - squareSide;
  const cells = Math.max(1, Math.round(span / gridStep));
  if (!Number.isSafeInteger(cells) || (cells + 1) ** 2 > MAX_APPEND_CANDIDATES) {
    throw new RangeError(`append proposal is limited to ${MAX_APPEND_CANDIDATES} candidates`);
  }
  return cells;
}

/** Number of deterministic coarse-grid points inspected by an append proposal. */
export function appendPackStartCandidateCount(
  containerSide: number,
  squareSide = 1,
  gridStep = DEFAULT_GRID_STEP,
): number {
  positive(containerSide, "append container side");
  positive(squareSide, "append square side");
  if (containerSide < squareSide) {
    throw new RangeError("append container cannot be smaller than one square");
  }
  const cells = gridCells(containerSide, squareSide, gridStep);
  return (cells + 1) ** 2;
}

/**
 * Center a previous packing and append one axis-aligned square at the legacy
 * coarse-grid point with maximum nearest-center clearance.
 */
export function createAppendPackStart(
  previous: GeometrySnapshot,
  containerSide: number,
  options: { gridStep?: number } = {},
): GeometrySnapshot {
  validatePrevious(previous, containerSide);
  const gridStep = options.gridStep ?? DEFAULT_GRID_STEP;
  const cells = gridCells(containerSide, previous.squareSide, gridStep);
  const shiftX = (containerSide - previous.container.side) / 2 - previous.container.originX;
  const shiftY = (containerSide - previous.container.side) / 2 - previous.container.originY;
  const poses = previous.poses.map((pose) => ({
    x: pose.x + shiftX,
    y: pose.y + shiftY,
    angle: pose.angle,
  }));
  const low = previous.squareSide / 2;
  const high = containerSide - low;
  let resultX = low;
  let resultY = low;
  let best = -1;
  for (let xIndex = 0; xIndex <= cells; xIndex += 1) {
    const x = low + ((high - low) * xIndex) / cells;
    for (let yIndex = 0; yIndex <= cells; yIndex += 1) {
      const y = low + ((high - low) * yIndex) / cells;
      let nearest = Number.POSITIVE_INFINITY;
      for (const pose of poses) {
        nearest = Math.min(nearest, (pose.x - x) ** 2 + (pose.y - y) ** 2);
      }
      if (nearest > best) {
        best = nearest;
        resultX = x;
        resultY = y;
      }
    }
  }
  poses.push({ x: resultX, y: resultY, angle: 0 });
  return {
    squareSide: previous.squareSide,
    container: { originX: 0, originY: 0, side: containerSide },
    poses,
  };
}
