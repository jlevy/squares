const OVERLAP_CELL_SIDES = 1.5;
const CONTACT_CELL_SIDES = 1.2;

export interface GeometryPose {
  x: number;
  y: number;
  /** Counter-clockwise radians. */
  angle: number;
}

export interface GeometryContainer {
  originX: number;
  originY: number;
  side: number;
}

export interface GeometrySnapshot {
  squareSide: number;
  container: GeometryContainer;
  poses: readonly GeometryPose[];
}

export interface GeometryBounds {
  minX: number;
  maxX: number;
  minY: number;
  maxY: number;
}

export interface ContactOptions {
  gap: number;
  angleToleranceRadians: number;
}

export interface LegacyContactOptions {
  gap: number;
  angleToleranceDegrees: number;
}

export interface GeometryReceipt {
  bounds: GeometryBounds;
  requiredSide: number;
  totalOverlap: number;
  deepestOverlap: number;
  overlapPairs: number;
  wallOverlapTotal: number;
  maxPairOverlap: number;
  maxWallOverlap: number;
  contacts: number[];
  /** Flat pairs of pose indices. Walls increment contact counts but have no edge. */
  contactEdges: number[];
}

interface Grid {
  dimension: number;
  head: Int32Array;
  next: Int32Array;
  xIndex(value: number): number;
  yIndex(value: number): number;
}

export function degreesToRadians(degrees: number): number {
  return (degrees * Math.PI) / 180;
}

function finite(value: number, name: string): void {
  if (!Number.isFinite(value)) {
    throw new RangeError(`${name} must be finite`);
  }
}

function positive(value: number, name: string): void {
  finite(value, name);
  if (value <= 0) {
    throw new RangeError(`${name} must be positive`);
  }
}

function itemAt<T>(items: ArrayLike<T>, index: number, name: string): T {
  const item = items[index];
  if (item === undefined) {
    throw new RangeError(`${name} has no item at index ${index}`);
  }
  return item;
}

function checkSnapshot(snapshot: GeometrySnapshot): void {
  positive(snapshot.squareSide, "square side");
  positive(snapshot.container.side, "container side");
  finite(snapshot.container.originX, "container x origin");
  finite(snapshot.container.originY, "container y origin");
  if (snapshot.poses.length < 1) {
    throw new RangeError("a geometry snapshot must contain at least one square");
  }
  for (const pose of snapshot.poses) {
    finite(pose.x, "square x");
    finite(pose.y, "square y");
    finite(pose.angle, "square angle");
  }
}

function angleGap(left: number, right: number): number {
  const quarterTurn = Math.PI / 2;
  const distance = Math.abs(left - right) % quarterTurn;
  return Math.min(distance, quarterTurn - distance);
}

function foldAngle(angle: number): number {
  const quarterTurn = Math.PI / 2;
  return ((angle % quarterTurn) + quarterTurn) % quarterTurn;
}

function squareRadiusOnAxis(
  axisX: number,
  axisY: number,
  cosine: number,
  sine: number,
  halfSide: number,
): number {
  return (
    halfSide * (Math.abs(axisX * cosine + axisY * sine) + Math.abs(-axisX * sine + axisY * cosine))
  );
}

export interface PairSeparation {
  /** The smallest face-normal overlap, or zero when some face normal separates the squares. */
  penetration: number;
  /** The unit face normal of that overlap, oriented from `left` towards `right`; zero when separated. */
  normalX: number;
  normalY: number;
}

/** Separating-axis penetration for two equal squares, or zero when an axis separates them. */
export function pairPenetration(
  left: GeometryPose,
  right: GeometryPose,
  squareSide: number,
): number {
  return pairSeparation(left, right, squareSide).penetration;
}

/** `pairPenetration` with the face normal a repair would push the two squares apart along. */
export function pairSeparation(
  left: GeometryPose,
  right: GeometryPose,
  squareSide: number,
): PairSeparation {
  positive(squareSide, "square side");
  for (const [value, name] of [
    [left.x, "left x"],
    [left.y, "left y"],
    [left.angle, "left angle"],
    [right.x, "right x"],
    [right.y, "right y"],
    [right.angle, "right angle"],
  ] as const) {
    finite(value, name);
  }
  const dx = right.x - left.x;
  const dy = right.y - left.y;
  const leftCosine = Math.cos(left.angle);
  const leftSine = Math.sin(left.angle);
  const rightCosine = Math.cos(right.angle);
  const rightSine = Math.sin(right.angle);
  const axes: readonly (readonly [number, number])[] = [
    [leftCosine, leftSine],
    [-leftSine, leftCosine],
    [rightCosine, rightSine],
    [-rightSine, rightCosine],
  ];
  const halfSide = squareSide / 2;
  const separated: PairSeparation = { penetration: 0, normalX: 0, normalY: 0 };
  const deepest: PairSeparation = { penetration: Infinity, normalX: 0, normalY: 0 };
  for (const [axisX, axisY] of axes) {
    const projected = dx * axisX + dy * axisY;
    const overlap =
      squareRadiusOnAxis(axisX, axisY, leftCosine, leftSine, halfSide) +
      squareRadiusOnAxis(axisX, axisY, rightCosine, rightSine, halfSide) -
      Math.abs(projected);
    if (overlap <= 0) {
      return separated;
    }
    if (overlap < deepest.penetration) {
      const sign = projected < 0 ? -1 : 1;
      deepest.penetration = overlap;
      deepest.normalX = axisX * sign;
      deepest.normalY = axisY * sign;
    }
  }
  return deepest;
}

export function packingBounds(poses: readonly GeometryPose[], squareSide: number): GeometryBounds {
  positive(squareSide, "square side");
  if (poses.length < 1) {
    throw new RangeError("packing bounds require at least one square");
  }
  let minX = Infinity;
  let maxX = -Infinity;
  let minY = Infinity;
  let maxY = -Infinity;
  const half = squareSide / 2;
  for (const pose of poses) {
    finite(pose.x, "square x");
    finite(pose.y, "square y");
    finite(pose.angle, "square angle");
    const radius = half * (Math.abs(Math.cos(pose.angle)) + Math.abs(Math.sin(pose.angle)));
    minX = Math.min(minX, pose.x - radius);
    maxX = Math.max(maxX, pose.x + radius);
    minY = Math.min(minY, pose.y - radius);
    maxY = Math.max(maxY, pose.y + radius);
  }
  return { minX, maxX, minY, maxY };
}

function spatialGrid(poses: readonly GeometryPose[], cellSize: number): Grid {
  positive(cellSize, "grid cell size");
  let minX = Infinity;
  let maxX = -Infinity;
  let minY = Infinity;
  let maxY = -Infinity;
  for (const pose of poses) {
    minX = Math.min(minX, pose.x);
    maxX = Math.max(maxX, pose.x);
    minY = Math.min(minY, pose.y);
    maxY = Math.max(maxY, pose.y);
  }
  const span = Math.max(maxX - minX, maxY - minY);
  const dimension = Math.max(1, Math.min(512, Math.ceil(span / cellSize) + 1));
  const actualCellSize = dimension === 512 ? Math.max(cellSize, span / 511) : cellSize;
  const index = (value: number, base: number): number =>
    Math.max(0, Math.min(dimension - 1, Math.floor((value - base) / actualCellSize)));
  const head = new Int32Array(dimension * dimension);
  const next = new Int32Array(poses.length);
  head.fill(-1);
  for (let poseIndex = 0; poseIndex < poses.length; poseIndex += 1) {
    const pose = itemAt(poses, poseIndex, "poses");
    const cellIndex = index(pose.x, minX) + index(pose.y, minY) * dimension;
    next[poseIndex] = itemAt(head, cellIndex, "grid head");
    head[cellIndex] = poseIndex;
  }
  return {
    dimension,
    head,
    next,
    xIndex: (value) => index(value, minX),
    yIndex: (value) => index(value, minY),
  };
}

function nearbyPairs(
  poses: readonly GeometryPose[],
  cellSize: number,
  visit: (left: number, right: number) => void,
): void {
  const grid = spatialGrid(poses, cellSize);
  for (let left = 0; left < poses.length; left += 1) {
    const pose = itemAt(poses, left, "poses");
    const gridX = grid.xIndex(pose.x);
    const gridY = grid.yIndex(pose.y);
    for (let offsetY = -1; offsetY <= 1; offsetY += 1) {
      const y = gridY + offsetY;
      if (y < 0 || y >= grid.dimension) {
        continue;
      }
      for (let offsetX = -1; offsetX <= 1; offsetX += 1) {
        const x = gridX + offsetX;
        if (x < 0 || x >= grid.dimension) {
          continue;
        }
        const cellIndex = x + y * grid.dimension;
        for (
          let right = itemAt(grid.head, cellIndex, "grid head");
          right !== -1;
          right = itemAt(grid.next, right, "grid next")
        ) {
          if (right > left) {
            visit(left, right);
          }
        }
      }
    }
  }
}

function wallPenetration(
  pose: GeometryPose,
  squareSide: number,
  container: GeometryContainer,
): number {
  const half = squareSide / 2;
  const radius = half * (Math.abs(Math.cos(pose.angle)) + Math.abs(Math.sin(pose.angle)));
  return Math.max(
    0,
    container.originX - (pose.x - radius),
    pose.x + radius - (container.originX + container.side),
    container.originY - (pose.y - radius),
    pose.y + radius - (container.originY + container.side),
  );
}

function contactFacts(
  snapshot: GeometrySnapshot,
  options: ContactOptions,
): { contacts: number[]; contactEdges: number[] } {
  finite(options.gap, "contact gap");
  finite(options.angleToleranceRadians, "contact angle tolerance");
  if (options.gap < 0 || options.angleToleranceRadians < 0) {
    throw new RangeError("contact tolerances cannot be negative");
  }
  const { poses, squareSide, container } = snapshot;
  const contacts = Array<number>(poses.length).fill(0);
  const contactEdges: number[] = [];
  for (let index = 0; index < poses.length; index += 1) {
    const pose = itemAt(poses, index, "poses");
    if (angleGap(foldAngle(pose.angle), 0) > options.angleToleranceRadians) {
      continue;
    }
    let count = 0;
    if (Math.abs(pose.x - (container.originX + squareSide / 2)) <= options.gap) {
      count += 1;
    }
    if (Math.abs(pose.x - (container.originX + container.side - squareSide / 2)) <= options.gap) {
      count += 1;
    }
    if (Math.abs(pose.y - (container.originY + squareSide / 2)) <= options.gap) {
      count += 1;
    }
    if (Math.abs(pose.y - (container.originY + container.side - squareSide / 2)) <= options.gap) {
      count += 1;
    }
    contacts[index] = count;
  }
  nearbyPairs(poses, CONTACT_CELL_SIDES * squareSide, (left, right) => {
    const first = itemAt(poses, left, "poses");
    const second = itemAt(poses, right, "poses");
    const dx = second.x - first.x;
    const dy = second.y - first.y;
    if (dx * dx + dy * dy > 2.5 * squareSide * squareSide) {
      return;
    }
    if (angleGap(foldAngle(first.angle), foldAngle(second.angle)) > options.angleToleranceRadians) {
      return;
    }
    const cosine = Math.cos(first.angle);
    const sine = Math.sin(first.angle);
    const along = dx * cosine + dy * sine;
    const across = -dx * sine + dy * cosine;
    const sharesSide =
      (Math.abs(Math.abs(along) - squareSide) <= options.gap && Math.abs(across) <= options.gap) ||
      (Math.abs(Math.abs(across) - squareSide) <= options.gap && Math.abs(along) <= options.gap);
    if (!sharesSide) {
      return;
    }
    contacts[left] = Math.min(4, itemAt(contacts, left, "contacts") + 1);
    contacts[right] = Math.min(4, itemAt(contacts, right, "contacts") + 1);
    contactEdges.push(left, right);
  });
  return { contacts, contactEdges };
}

/** Measure every pair/wall overlap and optional full-side contacts from one normalized snapshot. */
export function measurePackingGeometry(
  snapshot: GeometrySnapshot,
  contactOptions?: ContactOptions,
): GeometryReceipt {
  checkSnapshot(snapshot);
  const bounds = packingBounds(snapshot.poses, snapshot.squareSide);
  let totalOverlap = 0;
  let deepestOverlap = 0;
  let overlapPairs = 0;
  let wallOverlapTotal = 0;
  let maxWallOverlap = 0;
  for (const pose of snapshot.poses) {
    const overlap = wallPenetration(pose, snapshot.squareSide, snapshot.container);
    wallOverlapTotal += overlap;
    maxWallOverlap = Math.max(maxWallOverlap, overlap);
    totalOverlap += overlap;
    deepestOverlap = Math.max(deepestOverlap, overlap);
  }
  let maxPairOverlap = 0;
  nearbyPairs(snapshot.poses, OVERLAP_CELL_SIDES * snapshot.squareSide, (left, right) => {
    const first = itemAt(snapshot.poses, left, "poses");
    const second = itemAt(snapshot.poses, right, "poses");
    const dx = second.x - first.x;
    const dy = second.y - first.y;
    if (dx * dx + dy * dy >= 2 * snapshot.squareSide * snapshot.squareSide) {
      return;
    }
    const overlap = pairPenetration(first, second, snapshot.squareSide);
    if (overlap <= 0) {
      return;
    }
    totalOverlap += overlap;
    deepestOverlap = Math.max(deepestOverlap, overlap);
    maxPairOverlap = Math.max(maxPairOverlap, overlap);
    overlapPairs += 1;
  });
  const contacts =
    contactOptions === undefined
      ? { contacts: Array<number>(snapshot.poses.length).fill(0), contactEdges: [] }
      : contactFacts(snapshot, contactOptions);
  return {
    bounds,
    requiredSide: Math.max(bounds.maxX - bounds.minX, bounds.maxY - bounds.minY),
    totalOverlap,
    deepestOverlap,
    overlapPairs,
    wallOverlapTotal,
    maxPairOverlap,
    maxWallOverlap,
    contacts: contacts.contacts,
    contactEdges: contacts.contactEdges,
  };
}

/** Normalize the retained degree buffers and measure them through the shared radian engine. */
export function measureFrameGeometry(
  x: ArrayLike<number>,
  y: ArrayLike<number>,
  anglesDegrees: ArrayLike<number>,
  containerSide: number,
  squareSide: number,
  options: LegacyContactOptions,
): GeometryReceipt {
  if (x.length !== y.length || x.length !== anglesDegrees.length) {
    throw new RangeError("pose buffers must have the same length");
  }
  const poses: GeometryPose[] = [];
  for (let index = 0; index < x.length; index += 1) {
    poses.push({
      x: itemAt(x, index, "x buffer"),
      y: itemAt(y, index, "y buffer"),
      angle: degreesToRadians(itemAt(anglesDegrees, index, "angle buffer")),
    });
  }
  return measurePackingGeometry(
    {
      squareSide,
      container: { originX: 0, originY: 0, side: containerSide },
      poses,
    },
    {
      gap: options.gap,
      angleToleranceRadians: degreesToRadians(options.angleToleranceDegrees),
    },
  );
}

export const geometry = Object.freeze({
  degreesToRadians,
  pairPenetration,
  pairSeparation,
  packingBounds,
  measurePackingGeometry,
  measureFrameGeometry,
});
