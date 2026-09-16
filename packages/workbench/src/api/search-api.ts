import { PACKING_VALIDITY, parseUint32Seed } from "../core/runtime-contracts.ts";
import type { JsonObject, SearchPlan } from "../search/contracts.ts";
import {
  PACK_SEARCH_CONFIGURATION_CONTRACT,
  validatePackSearchPlan,
} from "../search/pack-runner.ts";
import { decodeSearchPlan } from "../search/registry.ts";

/** The source the page was built from, as its build stamped it. */
export interface BrowserSearchSource {
  commit: string;
  dirty: boolean;
}

export interface BrowserSearchInputs {
  n: number;
  seeds: readonly number[];
  physicsSteps: number;
  proposal: "grid" | "random";
  repair: boolean;
  /** Recorded in the plan; without it the plan says `unknown` and dirty. */
  source?: BrowserSearchSource;
}

/**
 * Read the source from the page's `squares-workbench-revision` and `squares-workbench-dirty`
 * meta contents. A missing or empty revision is `unknown`; a dirty flag that is not exactly
 * `false` counts as dirty, so a page never claims a clean source it cannot show.
 */
export function browserSearchSource(
  revision: string | null,
  dirty: string | null,
): BrowserSearchSource {
  const commit = revision === null || revision === "" ? "unknown" : revision;
  // Without a revision nothing ties the plan to a source, so it can never read as clean.
  return { commit, dirty: commit === "unknown" || dirty !== "false" };
}

/** A bounded, reproducible exploratory plan. It makes no research acceptance claim. */
export function createBrowserSearchPlan(inputs: BrowserSearchInputs): SearchPlan {
  if (!Number.isSafeInteger(inputs.n) || inputs.n < 1 || inputs.n > 32) {
    throw new RangeError("Search n must be an integer from 1 to 32");
  }
  if (
    inputs.seeds.length < 1 ||
    inputs.seeds.length > 8 ||
    new Set(inputs.seeds).size !== inputs.seeds.length ||
    inputs.seeds.some((seed) => parseUint32Seed(seed) === null)
  ) {
    throw new RangeError("Search needs 1 to 8 unique unsigned 32-bit seeds");
  }
  if (
    !Number.isSafeInteger(inputs.physicsSteps) ||
    inputs.physicsSteps < 1 ||
    inputs.physicsSteps > 5_000
  ) {
    throw new RangeError("Search physics steps must be an integer from 1 to 5000");
  }
  if (inputs.proposal !== "grid" && inputs.proposal !== "random") {
    throw new RangeError("Search proposal must be grid or random");
  }
  const configuration: JsonObject = {
    contract: PACK_SEARCH_CONFIGURATION_CONTRACT,
    seed_base: 0,
    proposal:
      inputs.proposal === "grid"
        ? { kind: "grid" }
        : { kind: "random", container_side: Math.ceil(Math.sqrt(inputs.n)) * 1.5 },
    reference: "none",
    targets: "none",
    pair_law: { rigidity: 0.15, repulsion: 2500, attraction: 0, range: 0 },
    wall_law: { rigidity: 0.25, repulsion: 2500, attraction: 0, range: 0 },
    related_mask: null,
    physics: {
      steps_per_second: 120,
      omega: 10,
      zeta: 0.85,
      contact_damping: 20,
      contact_torque: 0.15,
      jiggle: 0,
      jiggle_torque: 0,
      jiggle_hz: [2.5, 4],
      max_speed: 40,
      max_spin: 20,
      cell: 1.5,
    },
    anneal: { amplitude: 0, decay_power: 1.5, tau: 2, floor: 0 },
    growth: { on: false, rate: 0.05, rule: "constant" },
    container: {
      squeeze_rate: 0.03,
      relax_rate: 0.15,
      squeeze_tolerance: 0.004,
      jam_tolerance: 0.06,
      minimum_side: 0.5,
    },
    stationarity: {
      linear_speed: 1e-6,
      angular_speed: 1e-6,
      forcing_scale: 1e-6,
      window: 20,
      stop: false,
    },
    repair: inputs.repair
      ? { kind: "resolve", tolerance: PACKING_VALIDITY.penetrationTolerance }
      : { kind: "none" },
    // With Resolve requested the table ranks what Resolve returned, not the best raw sample.
    objective: {
      kind: "absolute-side",
      state: inputs.repair ? "repaired" : "best-observed",
      require_stationary: false,
    },
  };
  const plan = decodeSearchPlan({
    contract: "packing.squares:SearchPlan/v1",
    id: `browser-n${inputs.n}-${inputs.proposal}-${inputs.repair ? "repair" : "raw"}-${inputs.physicsSteps}-${inputs.seeds.join("-")}`,
    source: {
      commit: inputs.source?.commit ?? "unknown",
      dirty: inputs.source?.dirty ?? true,
      runtime: "browser",
      engine: "pack/v1",
    },
    configurations: [{ id: "browser-control", configuration }],
    cohorts: [
      {
        id: "exploratory-browser",
        configuration_id: "browser-control",
        partition: "exploratory",
        n: inputs.n,
        seeds: [...inputs.seeds],
        block_size: Math.min(5, inputs.seeds.length),
        work_budget: {
          proposal_attempts: 1,
          physics_steps: inputs.physicsSteps,
          repair_iterations: inputs.repair ? 100 : 0,
        },
      },
    ],
  });
  validatePackSearchPlan(plan);
  return plan;
}

export function parseBrowserSearchSeeds(text: string): number[] {
  const tokens = text.split(",").map((token) => token.trim());
  if (tokens.some((token) => token.length === 0)) {
    throw new RangeError("Enter comma-separated seeds without empty values");
  }
  const seeds = tokens.map((token) => {
    if (!/^\d+$/.test(token)) {
      throw new RangeError("Each seed must be an unsigned integer");
    }
    const seed = Number(token);
    if (parseUint32Seed(seed) === null) {
      throw new RangeError("Each seed must be an unsigned 32-bit integer");
    }
    return seed;
  });
  return seeds;
}
