import type { AtlasLaw } from "../api/workbench-api.js";
import type { GeometrySnapshot } from "../core/geometry.js";
import { parseUint32Seed, seededRandom } from "../core/runtime-contracts.ts";
import { forceAtGap, forceLawAttracts } from "./force-law.ts";

const SQUARE_INERTIA = 1 / 6;
const QUARTER_TURN = Math.PI / 2;
const QUARTER_TURN_TIE = Math.PI / 4 + 1e-9;
/**
 * A separating-axis penetration this small is float rounding between touching squares and applies
 * no force. A solver threshold: validity is assessed separately, under `PACKING_VALIDITY`.
 */
const CONTACT_EPSILON = 1e-9;
/** Widens a broad-phase cell past the interaction reach, so a pair at the reach is never lost. */
const CELL_MARGIN = 1e-9;
/** The widest broad-phase grid, in cells; `core/geometry.ts` caps its own grid the same. */
export const MAX_BROAD_PHASE_DIMENSION = 512;

/** Typed arrays are dense inside their allocated bounds; every index is validated on admission. */
interface DenseFloat64Array extends Iterable<number> {
  [index: number]: number;
  readonly length: number;
  fill(value: number): this;
}

interface DenseInt32Array extends Iterable<number> {
  [index: number]: number;
  readonly length: number;
  fill(value: number): this;
  some(predicate: (value: number, index: number) => boolean): boolean;
}

function floatBuffer(length: number): DenseFloat64Array {
  return new Float64Array(length) as DenseFloat64Array;
}

function integerBuffer(length: number): DenseInt32Array {
  return new Int32Array(length) as DenseInt32Array;
}

function read(values: ArrayLike<number>, index: number): number {
  const value = values[index];
  if (value === undefined) {
    throw new RangeError(`numeric buffer has no item at index ${index}`);
  }
  return value;
}

export interface SimulationPose {
  x: number;
  y: number;
  angle: number;
  size: number;
}

export interface SimulationTarget {
  x: number;
  y: number;
  angle: number;
}

export interface SimulationBodyDefinition {
  members: readonly number[];
  /** Initial body angle in radians. Square offsets are derived in this frame. */
  angle: number;
  target: SimulationTarget;
  /** Fraction of contact torque applied to this body. */
  torqueFactor: number;
}

export interface SimulationDefinition {
  squares: readonly SimulationPose[];
  bodies: readonly SimulationBodyDefinition[];
  container: { originX: number; originY: number; side: number };
  seed: number;
  frequencyRange: readonly [number, number];
}

export interface SimulationSpring {
  stiffness: number;
  damping: number;
  /** A singleton square treats quarter turns as the same orientation. */
  quarterTurn: boolean;
}

export interface SimulationForcing {
  linear: number;
  angular: number;
  /** Phase clock in the same units as the stored oscillator frequencies. */
  time: number;
}

export interface SimulationPin {
  body: number;
  x: number;
  y: number;
  angle: number;
}

export interface SimulationStep {
  timestep: number;
  container: { originX: number; originY: number; side: number };
  pairLaw: AtlasLaw;
  wallLaw: AtlasLaw;
  /** Row-major n × n mask. Null or omitted means every pair may attract. */
  relatedMask?: Uint8Array | null;
  baseCell: number;
  contactDamping: number;
  contactScale: number;
  spring: SimulationSpring;
  forcing: SimulationForcing;
  maxSpeed: number;
  maxSpin: number;
  pinned?: SimulationPin;
}

export interface SimulationWork {
  steps: number;
  pairCandidates: number;
  pairForces: number;
  wallForces: number;
}

export interface SimulationStepReceipt {
  deepestPairPenetration: number;
  deepestFullSizePairPenetration: number;
  nearPairs: number;
  maxLinearSpeed: number;
  maxAngularSpeed: number;
  work: SimulationWork;
}

export interface SimulationBuffers {
  x: Float64Array;
  y: Float64Array;
  angle: Float64Array;
  velocityX: Float64Array;
  velocityY: Float64Array;
  angularVelocity: Float64Array;
}

/** Mutable numerical state. It has no DOM, clock or presentation dependency. */
export interface SimulationState {
  readonly seed: number;
  readonly squareCount: number;
  readonly bodyCount: number;
  readonly bodyOf: DenseInt32Array;
  readonly offsetX: DenseFloat64Array;
  readonly offsetY: DenseFloat64Array;
  readonly offsetAngle: DenseFloat64Array;
  readonly squareX: DenseFloat64Array;
  readonly squareY: DenseFloat64Array;
  readonly squareAngle: DenseFloat64Array;
  readonly squareVelocityX: DenseFloat64Array;
  readonly squareVelocityY: DenseFloat64Array;
  readonly squareSize: DenseFloat64Array;
  readonly bodyX: DenseFloat64Array;
  readonly bodyY: DenseFloat64Array;
  readonly bodyAngle: DenseFloat64Array;
  readonly bodyVelocityX: DenseFloat64Array;
  readonly bodyVelocityY: DenseFloat64Array;
  readonly bodyAngularVelocity: DenseFloat64Array;
  readonly bodyMass: DenseFloat64Array;
  readonly bodyInertia: DenseFloat64Array;
  readonly bodyTorqueFactor: DenseFloat64Array;
  readonly targetX: DenseFloat64Array;
  readonly targetY: DenseFloat64Array;
  readonly targetAngle: DenseFloat64Array;
  readonly frequencyX: DenseFloat64Array;
  readonly frequencyY: DenseFloat64Array;
  readonly frequencyAngle: DenseFloat64Array;
  readonly phaseX: DenseFloat64Array;
  readonly phaseY: DenseFloat64Array;
  readonly phaseAngle: DenseFloat64Array;
  readonly cosine: DenseFloat64Array;
  readonly sine: DenseFloat64Array;
  readonly forceX: DenseFloat64Array;
  readonly forceY: DenseFloat64Array;
  readonly torque: DenseFloat64Array;
  container: { originX: number; originY: number; side: number };
  simulatedTime: number;
  steps: number;
  gridDimension: number;
  gridHead: DenseInt32Array;
  gridNext: DenseInt32Array;
}

function finite(value: number, label: string): void {
  if (!Number.isFinite(value)) {
    throw new RangeError(`${label} must be finite`);
  }
}

function nonnegative(value: number, label: string): void {
  finite(value, label);
  if (value < 0) {
    throw new RangeError(`${label} must be nonnegative`);
  }
}

function positive(value: number, label: string): void {
  finite(value, label);
  if (value <= 0) {
    throw new RangeError(`${label} must be positive`);
  }
}

function validateLaw(law: AtlasLaw, label: string): void {
  positive(law.rigidity, `${label} rigidity`);
  nonnegative(law.repulsion, `${label} repulsion`);
  nonnegative(law.attraction, `${label} attraction`);
  nonnegative(law.range, `${label} range`);
}

function validateContainer(
  container: { originX: number; originY: number; side: number },
  label: string,
): void {
  finite(container.originX, `${label} origin x`);
  finite(container.originY, `${label} origin y`);
  positive(container.side, `${label} side`);
}

function validateStep(state: SimulationState, step: SimulationStep): void {
  positive(step.timestep, "timestep");
  validateContainer(step.container, "container");
  validateLaw(step.pairLaw, "pair law");
  validateLaw(step.wallLaw, "wall law");
  positive(step.baseCell, "base cell");
  nonnegative(step.contactDamping, "contact damping");
  nonnegative(step.contactScale, "contact scale");
  nonnegative(step.spring.stiffness, "spring stiffness");
  nonnegative(step.spring.damping, "spring damping");
  nonnegative(step.forcing.linear, "linear forcing");
  nonnegative(step.forcing.angular, "angular forcing");
  finite(step.forcing.time, "forcing time");
  positive(step.maxSpeed, "maximum speed");
  positive(step.maxSpin, "maximum spin");
  if (step.relatedMask !== undefined && step.relatedMask !== null) {
    if (step.relatedMask.length !== state.squareCount * state.squareCount) {
      throw new RangeError("relationship mask must be n by n");
    }
  }
  if (step.pinned !== undefined) {
    if (
      !Number.isSafeInteger(step.pinned.body) ||
      step.pinned.body < 0 ||
      step.pinned.body >= state.bodyCount
    ) {
      throw new RangeError("pinned body is outside the simulation");
    }
    finite(step.pinned.x, "pinned x");
    finite(step.pinned.y, "pinned y");
    finite(step.pinned.angle, "pinned angle");
  }
}

function recomputeBodyInertia(state: SimulationState, body: number): void {
  let inertia = 0;
  for (let index = 0; index < state.squareCount; index++) {
    if (read(state.bodyOf, index) !== body) {
      continue;
    }
    inertia +=
      SQUARE_INERTIA * read(state.squareSize, index) ** 2 +
      read(state.offsetX, index) ** 2 +
      read(state.offsetY, index) ** 2;
  }
  state.bodyInertia[body] = inertia;
}

function updateWorldPoses(state: SimulationState): void {
  for (let index = 0; index < state.squareCount; index++) {
    const body = read(state.bodyOf, index);
    if (body === undefined) {
      throw new RangeError("square has no body");
    }
    const cosine = Math.cos(read(state.bodyAngle, body));
    const sine = Math.sin(read(state.bodyAngle, body));
    const relativeX = cosine * read(state.offsetX, index) - sine * read(state.offsetY, index);
    const relativeY = sine * read(state.offsetX, index) + cosine * read(state.offsetY, index);
    state.squareX[index] = read(state.bodyX, body) + relativeX;
    state.squareY[index] = read(state.bodyY, body) + relativeY;
    state.squareAngle[index] = read(state.bodyAngle, body) + read(state.offsetAngle, index);
    state.squareVelocityX[index] =
      read(state.bodyVelocityX, body) - read(state.bodyAngularVelocity, body) * relativeY;
    state.squareVelocityY[index] =
      read(state.bodyVelocityY, body) + read(state.bodyAngularVelocity, body) * relativeX;
  }
}

/** Build one state used by cached trajectories and live Pack runs. */
export function createSimulationState(definition: SimulationDefinition): SimulationState {
  const seed = parseUint32Seed(definition.seed);
  if (seed === null) {
    throw new RangeError("simulation seed must be an unsigned 32-bit integer");
  }
  validateContainer(definition.container, "initial container");
  const [frequencyLow, frequencyHigh] = definition.frequencyRange;
  positive(frequencyLow, "minimum forcing frequency");
  positive(frequencyHigh, "maximum forcing frequency");
  if (frequencyHigh < frequencyLow) {
    throw new RangeError("forcing frequency range is reversed");
  }
  const squareCount = definition.squares.length;
  const bodyCount = definition.bodies.length;
  if (squareCount === 0 || bodyCount === 0) {
    throw new RangeError("simulation requires squares and bodies");
  }

  const bodyOf = integerBuffer(squareCount);
  bodyOf.fill(-1);
  const squareX = floatBuffer(squareCount);
  const squareY = floatBuffer(squareCount);
  const squareAngle = floatBuffer(squareCount);
  const squareVelocityX = floatBuffer(squareCount);
  const squareVelocityY = floatBuffer(squareCount);
  const squareSize = floatBuffer(squareCount);
  const offsetX = floatBuffer(squareCount);
  const offsetY = floatBuffer(squareCount);
  const offsetAngle = floatBuffer(squareCount);
  const singletonIdentity =
    bodyCount === squareCount &&
    definition.bodies.every(
      (body, index) =>
        body.members.length === 1 &&
        body.members[0] === index &&
        body.angle === definition.squares[index]?.angle,
    );
  for (let index = 0; index < squareCount; index++) {
    const square = definition.squares[index];
    if (square === undefined) {
      throw new RangeError("square definition is missing");
    }
    finite(square.x, `square ${index} x`);
    finite(square.y, `square ${index} y`);
    finite(square.angle, `square ${index} angle`);
    positive(square.size, `square ${index} size`);
    squareX[index] = square.x;
    squareY[index] = square.y;
    squareAngle[index] = square.angle;
    squareSize[index] = square.size;
  }

  const bodyX = singletonIdentity ? squareX : floatBuffer(bodyCount);
  const bodyY = singletonIdentity ? squareY : floatBuffer(bodyCount);
  const bodyAngle = singletonIdentity ? squareAngle : floatBuffer(bodyCount);
  const bodyVelocityX = singletonIdentity ? squareVelocityX : floatBuffer(bodyCount);
  const bodyVelocityY = singletonIdentity ? squareVelocityY : floatBuffer(bodyCount);
  const bodyAngularVelocity = singletonIdentity ? floatBuffer(squareCount) : floatBuffer(bodyCount);
  const bodyMass = floatBuffer(bodyCount);
  const bodyInertia = floatBuffer(bodyCount);
  const bodyTorqueFactor = floatBuffer(bodyCount);
  const targetX = floatBuffer(bodyCount);
  const targetY = floatBuffer(bodyCount);
  const targetAngle = floatBuffer(bodyCount);
  for (let body = 0; body < bodyCount; body++) {
    const source = definition.bodies[body];
    if (source === undefined || source.members.length === 0) {
      throw new RangeError(`body ${body} must have members`);
    }
    finite(source.angle, `body ${body} angle`);
    finite(source.target.x, `body ${body} target x`);
    finite(source.target.y, `body ${body} target y`);
    finite(source.target.angle, `body ${body} target angle`);
    nonnegative(source.torqueFactor, `body ${body} torque factor`);
    let centreX = 0;
    let centreY = 0;
    for (const index of source.members) {
      if (!Number.isSafeInteger(index) || index < 0 || index >= squareCount) {
        throw new RangeError(`body ${body} has an invalid member`);
      }
      if (bodyOf[index] !== -1) {
        throw new RangeError(`square ${index} belongs to more than one body`);
      }
      bodyOf[index] = body;
      centreX += read(squareX, index);
      centreY += read(squareY, index);
    }
    centreX /= source.members.length;
    centreY /= source.members.length;
    bodyX[body] = centreX;
    bodyY[body] = centreY;
    bodyAngle[body] = source.angle;
    bodyMass[body] = source.members.length;
    bodyTorqueFactor[body] = source.torqueFactor;
    targetX[body] = source.target.x;
    targetY[body] = source.target.y;
    targetAngle[body] = source.target.angle;
    const cosine = Math.cos(source.angle);
    const sine = Math.sin(source.angle);
    for (const index of source.members) {
      const differenceX = read(squareX, index) - centreX;
      const differenceY = read(squareY, index) - centreY;
      offsetX[index] = cosine * differenceX + sine * differenceY;
      offsetY[index] = -sine * differenceX + cosine * differenceY;
      offsetAngle[index] = read(squareAngle, index) - source.angle;
    }
  }
  if (bodyOf.some((body) => body < 0)) {
    throw new RangeError("every square must belong to exactly one body");
  }

  const random = seededRandom(seed);
  const frequencyX = floatBuffer(bodyCount);
  const frequencyY = floatBuffer(bodyCount);
  const frequencyAngle = floatBuffer(bodyCount);
  const phaseX = floatBuffer(bodyCount);
  const phaseY = floatBuffer(bodyCount);
  const phaseAngle = floatBuffer(bodyCount);
  const frequencySpan = frequencyHigh - frequencyLow;
  for (let body = 0; body < bodyCount; body++) {
    frequencyX[body] = 2 * Math.PI * (frequencyLow + frequencySpan * random());
    phaseX[body] = 2 * Math.PI * random();
    frequencyY[body] = 2 * Math.PI * (frequencyLow + frequencySpan * random());
    phaseY[body] = 2 * Math.PI * random();
    frequencyAngle[body] = 2 * Math.PI * (frequencyLow + frequencySpan * random());
    phaseAngle[body] = 2 * Math.PI * random();
  }

  const state: SimulationState = {
    seed,
    squareCount,
    bodyCount,
    bodyOf,
    offsetX,
    offsetY,
    offsetAngle,
    squareX,
    squareY,
    squareAngle,
    squareVelocityX,
    squareVelocityY,
    squareSize,
    bodyX,
    bodyY,
    bodyAngle,
    bodyVelocityX,
    bodyVelocityY,
    bodyAngularVelocity,
    bodyMass,
    bodyInertia,
    bodyTorqueFactor,
    targetX,
    targetY,
    targetAngle,
    frequencyX,
    frequencyY,
    frequencyAngle,
    phaseX,
    phaseY,
    phaseAngle,
    cosine: floatBuffer(squareCount),
    sine: floatBuffer(squareCount),
    forceX: floatBuffer(bodyCount),
    forceY: floatBuffer(bodyCount),
    torque: floatBuffer(bodyCount),
    container: { ...definition.container },
    simulatedTime: 0,
    steps: 0,
    gridDimension: 0,
    gridHead: integerBuffer(0),
    gridNext: integerBuffer(squareCount),
  };
  for (let body = 0; body < bodyCount; body++) {
    recomputeBodyInertia(state, body);
  }
  updateWorldPoses(state);
  return state;
}

/** Change one square's side and keep the body's rotational inertia consistent. */
export function setSimulationSquareSize(state: SimulationState, index: number, size: number): void {
  if (!Number.isSafeInteger(index) || index < 0 || index >= state.squareCount) {
    throw new RangeError("square index is outside the simulation");
  }
  positive(size, "square size");
  state.squareSize[index] = size;
  const body = read(state.bodyOf, index);
  if (body === undefined) {
    throw new RangeError("square has no body");
  }
  recomputeBodyInertia(state, body);
}

/** Change every square side, recalculating each body once. */
export function setUniformSimulationSquareSize(state: SimulationState, size: number): void {
  positive(size, "square size");
  state.squareSize.fill(size);
  for (let body = 0; body < state.bodyCount; body++) {
    recomputeBodyInertia(state, body);
  }
}

/** Native buffers for a one-square-per-body Pack adapter. */
export function simulationBuffers(state: SimulationState): SimulationBuffers {
  if (state.squareCount !== state.bodyCount) {
    throw new RangeError("direct simulation buffers require one body per square");
  }
  return {
    x: state.squareX as Float64Array,
    y: state.squareY as Float64Array,
    angle: state.squareAngle as Float64Array,
    velocityX: state.squareVelocityX as Float64Array,
    velocityY: state.squareVelocityY as Float64Array,
    angularVelocity: state.bodyAngularVelocity as Float64Array,
  };
}

/** Translate every body, preserving velocities and relative geometry. */
export function translateSimulation(state: SimulationState, x: number, y: number): void {
  finite(x, "simulation x shift");
  finite(y, "simulation y shift");
  for (let body = 0; body < state.bodyCount; body++) {
    state.bodyX[body] = read(state.bodyX, body) + x;
    state.bodyY[body] = read(state.bodyY, body) + y;
  }
  updateWorldPoses(state);
}

function addForce(
  state: SimulationState,
  square: number,
  pointX: number,
  pointY: number,
  forceX: number,
  forceY: number,
): void {
  const body = read(state.bodyOf, square);
  if (body === undefined) {
    throw new RangeError("square has no body");
  }
  state.forceX[body] = read(state.forceX, body) + forceX;
  state.forceY[body] = read(state.forceY, body) + forceY;
  const torqueFactor = read(state.bodyTorqueFactor, body);
  state.torque[body] =
    read(state.torque, body) +
    torqueFactor *
      ((pointX - read(state.bodyX, body)) * forceY - (pointY - read(state.bodyY, body)) * forceX);
}

function supportPoint(
  state: SimulationState,
  index: number,
  normalX: number,
  normalY: number,
): readonly [number, number] {
  const half = read(state.squareSize, index) / 2;
  const cosine = read(state.cosine, index);
  const sine = read(state.sine, index);
  const sign1 = normalX * cosine + normalY * sine >= 0 ? 1 : -1;
  const sign2 = -normalX * sine + normalY * cosine >= 0 ? 1 : -1;
  return [
    read(state.squareX, index) + half * (sign1 * cosine - sign2 * sine),
    read(state.squareY, index) + half * (sign1 * sine + sign2 * cosine),
  ];
}

function applyPairForce(
  state: SimulationState,
  step: SimulationStep,
  first: number,
  second: number,
  attractionReach: number,
): { penetration: number; near: boolean; applied: boolean } {
  if (state.bodyOf[first] === read(state.bodyOf, second)) {
    return { penetration: 0, near: false, applied: false };
  }
  const differenceX = read(state.squareX, second) - read(state.squareX, first);
  const differenceY = read(state.squareY, second) - read(state.squareY, first);
  const relation = step.relatedMask;
  const pull =
    attractionReach > 0 &&
    (relation === undefined ||
      relation === null ||
      relation[first * state.squareCount + second] !== 0)
      ? attractionReach
      : 0;
  const reach =
    Math.SQRT1_2 * (read(state.squareSize, first) + read(state.squareSize, second)) + pull;
  if (differenceX ** 2 + differenceY ** 2 >= reach ** 2) {
    return { penetration: 0, near: false, applied: false };
  }
  let best = Infinity;
  let normalX = 0;
  let normalY = 0;
  let owner = -1;
  for (let axisIndex = 0; axisIndex < 4; axisIndex++) {
    const own = axisIndex < 2 ? first : second;
    const cosine = read(state.cosine, own);
    const sine = read(state.sine, own);
    const axisX = (axisIndex & 1) !== 0 ? -sine : cosine;
    const axisY = (axisIndex & 1) !== 0 ? cosine : sine;
    const radiusFirst =
      (read(state.squareSize, first) *
        (Math.abs(axisX * read(state.cosine, first) + axisY * read(state.sine, first)) +
          Math.abs(-axisX * read(state.sine, first) + axisY * read(state.cosine, first)))) /
      2;
    const radiusSecond =
      (read(state.squareSize, second) *
        (Math.abs(axisX * read(state.cosine, second) + axisY * read(state.sine, second)) +
          Math.abs(-axisX * read(state.sine, second) + axisY * read(state.cosine, second)))) /
      2;
    const separation = differenceX * axisX + differenceY * axisY;
    const penetration = radiusFirst + radiusSecond - Math.abs(separation);
    if (penetration <= CONTACT_EPSILON && pull === 0) {
      return { penetration: 0, near: false, applied: false };
    }
    if (penetration < best) {
      best = penetration;
      normalX = separation < 0 ? -axisX : axisX;
      normalY = separation < 0 ? -axisY : axisY;
      owner = own;
    }
  }
  const gap = -best;
  if (gap > 0 && gap >= pull) {
    return { penetration: 0, near: false, applied: false };
  }
  const [pointX, pointY] =
    owner === first
      ? supportPoint(state, second, -normalX, -normalY)
      : supportPoint(state, first, normalX, normalY);
  const normalVelocity =
    (read(state.squareVelocityX, second) - read(state.squareVelocityX, first)) * normalX +
    (read(state.squareVelocityY, second) - read(state.squareVelocityY, first)) * normalY;
  const damping = best > 0 && normalVelocity < 0 ? -step.contactDamping * normalVelocity : 0;
  const force = step.contactScale * (forceAtGap(step.pairLaw, -best) + damping);
  const forceX = force * normalX;
  const forceY = force * normalY;
  addForce(state, second, pointX, pointY, forceX, forceY);
  addForce(state, first, pointX, pointY, -forceX, -forceY);
  return { penetration: best > 0 ? best : 0, near: gap > 0, applied: true };
}

function applyWallForces(state: SimulationState, step: SimulationStep): number {
  const { originX, originY, side } = step.container;
  const maximumX = originX + side;
  const maximumY = originY + side;
  const reach = forceLawAttracts(step.wallLaw) ? step.wallLaw.range : 0;
  let applications = 0;
  for (let index = 0; index < state.squareCount; index++) {
    const half = read(state.squareSize, index) / 2;
    const cosine = read(state.cosine, index);
    const sine = read(state.sine, index);
    for (let corner = 0; corner < 4; corner++) {
      const sign1 = (corner & 1) !== 0 ? -1 : 1;
      const sign2 = (corner & 2) !== 0 ? -1 : 1;
      const vertexX = read(state.squareX, index) + half * (sign1 * cosine - sign2 * sine);
      const vertexY = read(state.squareY, index) + half * (sign1 * sine + sign2 * cosine);
      const leftGap = vertexX - originX;
      if (leftGap < reach) {
        const damping =
          leftGap < 0 && read(state.squareVelocityX, index) < 0
            ? -step.contactDamping * read(state.squareVelocityX, index)
            : 0;
        addForce(state, index, vertexX, vertexY, forceAtGap(step.wallLaw, leftGap) + damping, 0);
        applications++;
      }
      const rightGap = maximumX - vertexX;
      if (rightGap < reach) {
        const damping =
          rightGap < 0 && read(state.squareVelocityX, index) > 0
            ? step.contactDamping * read(state.squareVelocityX, index)
            : 0;
        addForce(
          state,
          index,
          vertexX,
          vertexY,
          -(forceAtGap(step.wallLaw, rightGap) + damping),
          0,
        );
        applications++;
      }
      const bottomGap = vertexY - originY;
      if (bottomGap < reach) {
        const damping =
          bottomGap < 0 && read(state.squareVelocityY, index) < 0
            ? -step.contactDamping * read(state.squareVelocityY, index)
            : 0;
        addForce(state, index, vertexX, vertexY, 0, forceAtGap(step.wallLaw, bottomGap) + damping);
        applications++;
      }
      const topGap = maximumY - vertexY;
      if (topGap < reach) {
        const damping =
          topGap < 0 && read(state.squareVelocityY, index) > 0
            ? step.contactDamping * read(state.squareVelocityY, index)
            : 0;
        addForce(state, index, vertexX, vertexY, 0, -(forceAtGap(step.wallLaw, topGap) + damping));
        applications++;
      }
    }
  }
  return applications;
}

function wrappedTargetDelta(current: number, target: number): number {
  let difference = (((current - target) % QUARTER_TURN) + QUARTER_TURN) % QUARTER_TURN;
  if (difference > QUARTER_TURN_TIE) {
    difference -= QUARTER_TURN;
  }
  return -difference;
}

function pinBody(state: SimulationState, pin: SimulationPin): void {
  state.bodyX[pin.body] = pin.x;
  state.bodyY[pin.body] = pin.y;
  state.bodyAngle[pin.body] = pin.angle;
  state.bodyVelocityX[pin.body] = 0;
  state.bodyVelocityY[pin.body] = 0;
  state.bodyAngularVelocity[pin.body] = 0;
}

/**
 * The broad-phase grid for a container: how many cells wide, and how wide each cell is.
 *
 * The grid covers the container and two units beyond each wall in cells at least
 * `minimumCell` wide, so a pair close enough to interact is never more than one cell apart.
 * Left alone it grows with the square of the side: a 1e6 container asked for a grid that
 * cannot be allocated (#160 R15). Past `MAX_BROAD_PHASE_DIMENSION` the grid stops growing
 * and its cells grow instead. The neighbour search stays exact, because every cell is still
 * at least `minimumCell` wide and the kernel's clamped mapping is monotone, so two points
 * less than a cell apart still land in the same or adjacent cells; only more candidates
 * share a cell. Below the cap this is the grid the kernel always built, cell for cell, so
 * ordinary runs are bit-for-bit what they were.
 */
export function broadPhaseGrid(
  containerSide: number,
  minimumCell: number,
): { dimension: number; cell: number } {
  const dimension = Math.max(2, Math.ceil((containerSide + 4) / minimumCell) + 1);
  if (dimension <= MAX_BROAD_PHASE_DIMENSION) {
    return { dimension, cell: minimumCell };
  }
  return {
    dimension: MAX_BROAD_PHASE_DIMENSION,
    cell: Math.max(minimumCell, (containerSide + 4) / (MAX_BROAD_PHASE_DIMENSION - 1)),
  };
}

/** Advance one deterministic semi-implicit Euler step. */
export function advanceSimulation(
  state: SimulationState,
  step: SimulationStep,
): SimulationStepReceipt {
  validateStep(state, step);
  if (step.pinned !== undefined) {
    pinBody(state, step.pinned);
  }
  state.container = { ...step.container };
  updateWorldPoses(state);
  state.forceX.fill(0);
  state.forceY.fill(0);
  state.torque.fill(0);
  for (let index = 0; index < state.squareCount; index++) {
    state.cosine[index] = Math.cos(read(state.squareAngle, index));
    state.sine[index] = Math.sin(read(state.squareAngle, index));
  }

  const wallForces = applyWallForces(state, step);
  const attractionReach = forceLawAttracts(step.pairLaw) ? step.pairLaw.range : 0;
  let maximumSize = 0;
  for (const size of state.squareSize) {
    maximumSize = Math.max(maximumSize, size);
  }
  const { dimension, cell } = broadPhaseGrid(
    step.container.side,
    Math.max(step.baseCell, Math.SQRT2 * maximumSize + attractionReach + CELL_MARGIN),
  );
  if (state.gridDimension !== dimension) {
    state.gridDimension = dimension;
    state.gridHead = integerBuffer(dimension * dimension);
  }
  state.gridHead.fill(-1);
  const cellX = (value: number): number =>
    Math.max(0, Math.min(dimension - 1, Math.floor((value - step.container.originX + 2) / cell)));
  const cellY = (value: number): number =>
    Math.max(0, Math.min(dimension - 1, Math.floor((value - step.container.originY + 2) / cell)));
  for (let index = 0; index < state.squareCount; index++) {
    const cellIndex =
      cellX(read(state.squareX, index)) + cellY(read(state.squareY, index)) * dimension;
    state.gridNext[index] = read(state.gridHead, cellIndex);
    state.gridHead[cellIndex] = index;
  }
  let pairCandidates = 0;
  let pairForces = 0;
  let deepestPairPenetration = 0;
  let deepestFullSizePairPenetration = 0;
  let nearPairs = 0;
  for (let first = 0; first < state.squareCount; first++) {
    const centreX = cellX(read(state.squareX, first));
    const centreY = cellY(read(state.squareY, first));
    for (let offsetY = -1; offsetY <= 1; offsetY++) {
      const y = centreY + offsetY;
      if (y < 0 || y >= dimension) {
        continue;
      }
      for (let offsetX = -1; offsetX <= 1; offsetX++) {
        const x = centreX + offsetX;
        if (x < 0 || x >= dimension) {
          continue;
        }
        for (
          let second = read(state.gridHead, x + y * dimension);
          second !== -1;
          second = read(state.gridNext, second)
        ) {
          if (second <= first || state.bodyOf[first] === read(state.bodyOf, second)) {
            continue;
          }
          pairCandidates++;
          const collision = applyPairForce(state, step, first, second, attractionReach);
          if (collision.applied) {
            pairForces++;
          }
          if (collision.near) {
            nearPairs++;
          }
          deepestPairPenetration = Math.max(deepestPairPenetration, collision.penetration);
          if (read(state.squareSize, first) === 1 && read(state.squareSize, second) === 1) {
            deepestFullSizePairPenetration = Math.max(
              deepestFullSizePairPenetration,
              collision.penetration,
            );
          }
        }
      }
    }
  }

  let maxLinearSpeed = 0;
  let maxAngularSpeed = 0;
  for (let body = 0; body < state.bodyCount; body++) {
    if (step.pinned?.body === body) {
      pinBody(state, step.pinned);
      continue;
    }
    const accelerationX =
      read(state.forceX, body) / read(state.bodyMass, body) -
      step.spring.stiffness * (read(state.bodyX, body) - read(state.targetX, body)) -
      step.spring.damping * read(state.bodyVelocityX, body) +
      step.forcing.linear *
        Math.cos(read(state.frequencyX, body) * step.forcing.time + read(state.phaseX, body));
    const accelerationY =
      read(state.forceY, body) / read(state.bodyMass, body) -
      step.spring.stiffness * (read(state.bodyY, body) - read(state.targetY, body)) -
      step.spring.damping * read(state.bodyVelocityY, body) +
      step.forcing.linear *
        Math.cos(read(state.frequencyY, body) * step.forcing.time + read(state.phaseY, body));
    state.bodyVelocityX[body] = read(state.bodyVelocityX, body) + accelerationX * step.timestep;
    state.bodyVelocityY[body] = read(state.bodyVelocityY, body) + accelerationY * step.timestep;
    const speed = Math.hypot(read(state.bodyVelocityX, body), read(state.bodyVelocityY, body));
    if (speed > step.maxSpeed) {
      state.bodyVelocityX[body] = read(state.bodyVelocityX, body) * (step.maxSpeed / speed);
      state.bodyVelocityY[body] = read(state.bodyVelocityY, body) * (step.maxSpeed / speed);
    }
    state.bodyX[body] = read(state.bodyX, body) + read(state.bodyVelocityX, body) * step.timestep;
    state.bodyY[body] = read(state.bodyY, body) + read(state.bodyVelocityY, body) * step.timestep;
    const angularDifference = step.spring.quarterTurn
      ? wrappedTargetDelta(read(state.bodyAngle, body), read(state.targetAngle, body))
      : read(state.targetAngle, body) - read(state.bodyAngle, body);
    const angularAcceleration =
      read(state.torque, body) / read(state.bodyInertia, body) +
      step.spring.stiffness * angularDifference -
      step.spring.damping * read(state.bodyAngularVelocity, body) +
      step.forcing.angular *
        Math.cos(
          read(state.frequencyAngle, body) * step.forcing.time + read(state.phaseAngle, body),
        );
    state.bodyAngularVelocity[body] =
      read(state.bodyAngularVelocity, body) + angularAcceleration * step.timestep;
    state.bodyAngularVelocity[body] = Math.max(
      -step.maxSpin,
      Math.min(step.maxSpin, read(state.bodyAngularVelocity, body)),
    );
    state.bodyAngle[body] =
      read(state.bodyAngle, body) + read(state.bodyAngularVelocity, body) * step.timestep;
    maxLinearSpeed = Math.max(
      maxLinearSpeed,
      Math.hypot(read(state.bodyVelocityX, body), read(state.bodyVelocityY, body)),
    );
    maxAngularSpeed = Math.max(maxAngularSpeed, Math.abs(read(state.bodyAngularVelocity, body)));
  }
  updateWorldPoses(state);
  state.steps++;
  state.simulatedTime += step.timestep;
  return {
    deepestPairPenetration,
    deepestFullSizePairPenetration,
    nearPairs,
    maxLinearSpeed,
    maxAngularSpeed,
    work: { steps: 1, pairCandidates, pairForces, wallForces },
  };
}

/** Copy the exact returned pose for validation, storage and browser/Node receipts. */
export function simulationSnapshot(state: SimulationState): GeometrySnapshot {
  return {
    squareSide: read(state.squareSize, 0) ?? 1,
    container: { ...state.container },
    poses: Array.from({ length: state.squareCount }, (_, index) => ({
      x: read(state.squareX, index),
      y: read(state.squareY, index),
      angle: read(state.squareAngle, index),
    })),
  };
}

export const simulationKernel = Object.freeze({
  createSimulationState,
  setSimulationSquareSize,
  setUniformSimulationSquareSize,
  simulationBuffers,
  translateSimulation,
  advanceSimulation,
  simulationSnapshot,
});

export type SimulationKernelModule = typeof simulationKernel;
