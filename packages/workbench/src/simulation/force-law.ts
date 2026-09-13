import type { AtlasLaw } from "../api/workbench-api.js";

const LEGACY_RIGIDITY = 0.15;
const MAX_STEEPENING = 8;
const ASSUMED_CONTACTS = 4;
const MAX_SUBSTEPS = 12;

/** Extra slope past the repulsion knee; zero at the shipped law. */
export function forceLawSteep(law: AtlasLaw): number {
  return MAX_STEEPENING * Math.max(0, 1 - law.rigidity / LEGACY_RIGIDITY);
}

/** Whether the law reaches across a positive gap. */
export function forceLawAttracts(law: AtlasLaw): boolean {
  return law.attraction > 0 && law.range > 0;
}

/**
 * Evaluate the shared signed-gap law. Negative gaps are penetration and produce repulsion;
 * positive gaps may produce attraction. The pieces meet at zero and at the attraction range.
 */
export function forceAtGap(law: AtlasLaw, gap: number): number {
  if (gap <= 0) {
    const penetration = -gap;
    return (
      law.repulsion *
      (Math.min(penetration, law.rigidity) +
        forceLawSteep(law) * Math.max(0, penetration - law.rigidity))
    );
  }
  if (!forceLawAttracts(law) || gap >= law.range) {
    return 0;
  }
  const progress = gap / law.range;
  return -law.attraction * 4 * progress * (1 - progress);
}

/** Bound semi-implicit Euler substeps for the law's stiffest reachable slope. */
export function forceLawSubsteps(law: AtlasLaw, timestep: number): number {
  const slope = law.repulsion * Math.max(1, forceLawSteep(law));
  const angularFrequency = Math.sqrt(slope * ASSUMED_CONTACTS);
  const stabilityLimit = 2 / angularFrequency;
  return Math.max(1, Math.min(MAX_SUBSTEPS, Math.ceil(timestep / stabilityLimit)));
}

export const forceLaw = Object.freeze({
  forceLawSteep,
  forceLawAttracts,
  forceAtGap,
  forceLawSubsteps,
});

export type ForceLawModule = typeof forceLaw;
