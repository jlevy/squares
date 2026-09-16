import {
  type PackControllerOptions,
  type PackControllerState,
  parsePackSnapshot,
} from "../api/pack-api.ts";
import type { GeometrySnapshot } from "../core/geometry.ts";
import { assessPackingSnapshot, PACKING_VALIDITY } from "../core/runtime-contracts.ts";
import {
  advancePackRun,
  createGridPackStart,
  createPackRun,
  createRandomPackStart,
  type PackConfiguration,
  type PackReceipt,
  type PackRun,
} from "../simulation/pack.ts";
import { type ResolveReceipt, resolvePacking } from "../simulation/resolve.ts";

export type { PackControllerOptions, PackControllerState } from "../api/pack-api.ts";

function configuration(options: PackControllerOptions): PackConfiguration {
  const n = options.n ?? 17;
  const seed = options.seed ?? 1;
  const startKind = options.startKind ?? "grid";
  const grid = createGridPackStart(n);
  const start =
    startKind === "given"
      ? options.snapshot === undefined
        ? (() => {
            throw new TypeError("given start requires a snapshot");
          })()
        : parsePackSnapshot(options.snapshot)
      : startKind === "random"
        ? createRandomPackStart(n, grid.container.side, seed)
        : grid;
  const law = { rigidity: 0.15, repulsion: 2500, attraction: 0, range: 0 };
  return {
    n,
    seed,
    effectiveSeed: seed,
    startKind,
    start,
    targets: null,
    reference: null,
    relatedMask: null,
    pairLaw: options.pairLaw ?? law,
    wallLaw: options.wallLaw ?? law,
    physics: {
      stepsPerSecond: 120,
      omega: 10,
      zeta: 0.85,
      contactDamping: 20,
      contactTorque: 0.15,
      jiggle: 20,
      jiggleTorque: 12,
      jiggleHz: [2.5, 4],
      maxSpeed: 40,
      maxSpin: 20,
      cell: 1.5,
      ...options.physics,
    },
    anneal: { amplitude: 1, decayPower: 1.5, tau: 2, floor: 0.15, ...options.anneal },
    growth: { on: false, rate: 0.05, rule: "constant" },
    container: {
      squeezeRate: 0.03,
      relaxRate: 0.03,
      squeezeTolerance: 0.004,
      jamTolerance: 0.06,
      minimumSide: 0.5,
      ...options.container,
    },
    stationarity: {
      linearSpeed: 1e-6,
      angularSpeed: 1e-6,
      forcingScale: 1e-6,
      window: 8,
      stop: false,
      ...options.stationarity,
    },
  };
}

/** An independent, DOM-free Pack session. Every configuration change begins a new run. */
export class PackController {
  private run: PackRun;
  private latest: PackReceipt | null = null;
  private repair: ResolveReceipt | null = null;

  constructor(options: PackControllerOptions = {}) {
    this.run = createPackRun(configuration(options));
  }

  configure(options: PackControllerOptions): PackControllerState {
    const current = this.run.configuration;
    const candidate = configuration({
      n: current.n,
      seed: current.seed,
      startKind:
        current.startKind === "random"
          ? "random"
          : current.startKind === "given"
            ? "given"
            : "grid",
      snapshot: current.start,
      pairLaw: current.pairLaw,
      wallLaw: current.wallLaw,
      ...options,
      physics: { ...current.physics, ...options.physics },
      anneal: { ...current.anneal, ...options.anneal },
      container: { ...current.container, ...options.container },
      stationarity: { ...current.stationarity, ...options.stationarity },
    });
    this.run = createPackRun(candidate);
    this.latest = null;
    this.repair = null;
    return this.state();
  }

  step(count: number): PackReceipt {
    this.latest = advancePackRun(this.run, count);
    this.repair = null;
    return structuredClone(this.latest);
  }

  restart(): PackControllerState {
    this.run = createPackRun(this.run.configuration);
    this.latest = null;
    this.repair = null;
    return this.state();
  }

  resolve(iterationLimit = 100): ResolveReceipt {
    this.repair = resolvePacking(this.export(), {
      expectedCount: this.run.n,
      iterationLimit,
      // Resolve reports success only for an arrangement the contract calls a packing.
      tolerance: PACKING_VALIDITY.penetrationTolerance,
    });
    if (this.repair.termination.resolved && this.repair.repaired !== null) {
      this.run = createPackRun({
        ...this.run.configuration,
        startKind: "given",
        start: this.repair.repaired.snapshot,
      });
      this.latest = null;
    }
    return structuredClone(this.repair);
  }

  load(snapshot: GeometrySnapshot): PackControllerState {
    const parsed = parsePackSnapshot(snapshot);
    return this.configure({ n: parsed.poses.length, startKind: "given", snapshot: parsed });
  }

  state(): PackControllerState {
    const snapshot = this.export();
    return structuredClone({
      configuration: this.run.configuration,
      snapshot,
      latest: this.latest,
      repair: this.repair,
      assessment: assessPackingSnapshot(snapshot, this.run.n),
    });
  }

  export(): GeometrySnapshot {
    return {
      squareSide: this.run.size,
      container: { ...this.run.configuration.start.container, side: this.run.side },
      poses: Array.from(this.run.X, (x, index) => ({
        x,
        y: this.run.Y[index] ?? Number.NaN,
        angle: this.run.TH[index] ?? Number.NaN,
      })),
    };
  }
}
