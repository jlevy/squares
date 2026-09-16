import type { GeometrySnapshot } from "../core/geometry.ts";
import type { PackingAssessment } from "../core/runtime-contracts.ts";
import type {
  PackAnnealConfiguration,
  PackConfiguration,
  PackContainerConfiguration,
  PackPhysicsConfiguration,
  PackReceipt,
  PackStationarityConfiguration,
} from "../simulation/pack.ts";
import type { ResolveReceipt } from "../simulation/resolve.ts";
import type { AtlasLaw } from "./workbench-api.ts";

export interface PackControllerOptions {
  n?: number;
  seed?: number;
  startKind?: "grid" | "random" | "given";
  snapshot?: GeometrySnapshot;
  physics?: Partial<PackPhysicsConfiguration>;
  anneal?: Partial<PackAnnealConfiguration>;
  container?: Partial<PackContainerConfiguration>;
  stationarity?: Partial<PackStationarityConfiguration>;
  pairLaw?: AtlasLaw;
  wallLaw?: AtlasLaw;
}

export interface PackControllerState {
  configuration: PackConfiguration;
  snapshot: GeometrySnapshot;
  latest: PackReceipt | null;
  repair: ResolveReceipt | null;
  assessment: PackingAssessment;
}

/** Public handle for the currently displayed Pack session. */
export interface PackWorkbenchApi {
  configure(options: PackControllerOptions): PackControllerState;
  play(): void;
  pause(): void;
  playing(): boolean;
  step(count: number): PackControllerState;
  restart(): PackControllerState;
  resolve(): ResolveReceipt;
  load(text: string): PackControllerState;
  state(): PackControllerState;
  exportSnapshot(): GeometrySnapshot;
}

function object(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function finite(value: unknown, label: string): number {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    throw new TypeError(`${label} must be a finite number`);
  }
  return value;
}

/** Grid sides of room a snapshot's container may have, beyond the plain grid's own side. */
const CONTAINER_GRID_SIDES = 4;
/** Square sides added to that, so a small n is not held to a cramped container. */
const CONTAINER_MARGIN_SQUARES = 4;

/**
 * The largest container side a snapshot of `n` squares of side `squareSide` may declare.
 *
 * `ceil(sqrt(n))` squares to a row is the plain grid, which holds any n squares with no
 * search at all, so no packing ever needs a container wider than that. Four times it is
 * sixteen times the area, room for any loose hand-made start, and four more squares keep
 * n = 1 (a side of 8) usable. Every start Pack makes for itself is inside the bound. A
 * wider container is only empty space, and the simulation's broad phase and the stage both
 * grow with it: side 1e4 cost 33 ms a step and side 1e6 killed the page (#160 R15).
 */
export function maximumPackContainerSide(n: number, squareSide: number): number {
  return (CONTAINER_GRID_SIDES * Math.ceil(Math.sqrt(n)) + CONTAINER_MARGIN_SQUARES) * squareSide;
}

/** Parse geometry only. A snapshot does not contain velocities or resume a trajectory. */
export function parsePackSnapshot(value: unknown): GeometrySnapshot {
  if (!object(value) || !object(value.container) || !Array.isArray(value.poses)) {
    throw new TypeError("Pack snapshot requires squareSide, container, and poses");
  }
  const squareSide = finite(value.squareSide, "squareSide");
  const side = finite(value.container.side, "container side");
  if (squareSide <= 0 || side <= 0 || value.poses.length === 0) {
    throw new RangeError("Pack snapshot requires positive dimensions and at least one pose");
  }
  const widest = maximumPackContainerSide(value.poses.length, squareSide);
  if (side > widest) {
    throw new RangeError(
      `Pack snapshot container side ${side} is too large for n = ${value.poses.length} squares of side ${squareSide}; the most accepted is ${widest}`,
    );
  }
  return {
    squareSide,
    container: {
      originX: finite(value.container.originX, "container originX"),
      originY: finite(value.container.originY, "container originY"),
      side,
    },
    poses: value.poses.map((pose: unknown, index: number) => {
      if (!object(pose)) {
        throw new TypeError(`pose ${index} must be an object`);
      }
      return {
        x: finite(pose.x, `pose ${index} x`),
        y: finite(pose.y, `pose ${index} y`),
        angle: finite(pose.angle, `pose ${index} angle`),
      };
    }),
  };
}
