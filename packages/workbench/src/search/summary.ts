import type {
  SearchOutcome,
  SearchOutcomes,
  SearchPartition,
  SearchPlan,
  SearchTrialValue,
  SearchWorkReceipt,
} from "./contracts.ts";
import { selectedSearchState } from "./contracts.ts";
import { decodeSearchOutcomes, type SearchStatusCounts, statusCounts } from "./outcomes.ts";

import type { SearchAdmissionOptions } from "./validation.ts";

export interface SearchRate {
  numerator: number;
  denominator: number;
  denominatorKind: "planned" | "completed";
}

export interface SearchBlockSummary {
  block: number;
  planned: number;
  completed: number;
  valid: number;
  rankable: number;
  bestObjective: number | null;
  bestSlotId: string | null;
}

export interface SearchCohortSummary {
  cohortId: string;
  configurationId: string;
  partition: SearchPartition;
  n: number;
  status: SearchStatusCounts;
  valid: number;
  stationary: number;
  rankable: number;
  completionRate: SearchRate;
  validityRate: SearchRate;
  absoluteSides: number[];
  objectives: number[];
  work: SearchWorkReceipt;
  best: { slotId: string; result: SearchTrialValue } | null;
  blocks: SearchBlockSummary[];
}

function emptyWork(): SearchWorkReceipt {
  return {
    proposalAttempts: 0,
    physicsSteps: 0,
    repairIterations: 0,
    pairCandidates: 0,
    pairForces: 0,
    wallForces: 0,
    repairPairTests: 0,
    repairPairTranslations: 0,
    repairFitTranslations: 0,
  };
}

function addWork(total: SearchWorkReceipt, next: SearchWorkReceipt): void {
  total.proposalAttempts += next.proposalAttempts;
  total.physicsSteps += next.physicsSteps;
  total.repairIterations += next.repairIterations;
  total.pairCandidates += next.pairCandidates;
  total.pairForces += next.pairForces;
  total.wallForces += next.wallForces;
  total.repairPairTests += next.repairPairTests;
  total.repairPairTranslations += next.repairPairTranslations;
  total.repairFitTranslations += next.repairFitTranslations;
}

function retainedResult(outcome: SearchOutcome): SearchTrialValue | null {
  if (outcome.status === "completed") {
    return outcome.result;
  }
  if (
    outcome.status === "failed" ||
    outcome.status === "timed-out" ||
    outcome.status === "cancelled"
  ) {
    return outcome.partial;
  }
  return null;
}

/** Summarize each declared cohort independently, including partial disjoint blocks. */
export function summarizeSearch(
  plan: SearchPlan,
  envelope: SearchOutcomes,
  options: SearchAdmissionOptions = {},
): SearchCohortSummary[] {
  const { outcomes } = decodeSearchOutcomes(envelope, plan, options);
  return plan.cohorts.map((cohort) => {
    const selected = outcomes.filter((outcome) => outcome.slot.cohortId === cohort.id);
    const completed = selected.filter((outcome) => outcome.status === "completed");
    const valid = completed.filter(
      (outcome) => selectedSearchState(outcome.result)?.valid === true,
    );
    const rankable = valid.filter((outcome) => outcome.result.objective !== null);
    const stationary = completed.filter((outcome) => outcome.result.stationarity.stationary);
    const work = emptyWork();
    for (const outcome of selected) {
      const result = retainedResult(outcome);
      if (result !== null) {
        addWork(work, result.work);
      }
    }
    const ranked = [...rankable].sort(
      (left, right) => (left.result.objective ?? Infinity) - (right.result.objective ?? Infinity),
    );
    const best = ranked[0];
    const blockCount = Math.ceil(cohort.seeds.length / cohort.blockSize);
    const blocks = Array.from({ length: blockCount }, (_unused, block): SearchBlockSummary => {
      const members = selected.filter((outcome) => outcome.slot.block === block);
      const completeMembers = members.filter((outcome) => outcome.status === "completed");
      const validMembers = completeMembers.filter(
        (outcome) => selectedSearchState(outcome.result)?.valid === true,
      );
      const rankedMembers = validMembers
        .filter((outcome) => outcome.result.objective !== null)
        .sort(
          (left, right) =>
            (left.result.objective ?? Infinity) - (right.result.objective ?? Infinity),
        );
      return {
        block,
        planned: members.length,
        completed: completeMembers.length,
        valid: validMembers.length,
        rankable: rankedMembers.length,
        bestObjective: rankedMembers[0]?.result.objective ?? null,
        bestSlotId: rankedMembers[0]?.slot.id ?? null,
      };
    });
    return {
      cohortId: cohort.id,
      configurationId: cohort.configurationId,
      partition: cohort.partition,
      n: cohort.n,
      status: statusCounts(selected),
      valid: valid.length,
      stationary: stationary.length,
      rankable: rankable.length,
      completionRate: {
        numerator: completed.length,
        denominator: selected.length,
        denominatorKind: "planned",
      },
      validityRate: {
        numerator: valid.length,
        denominator: completed.length,
        denominatorKind: "completed",
      },
      absoluteSides: valid
        .map((outcome) => selectedSearchState(outcome.result)?.absoluteSide ?? null)
        .filter((side) => side !== null),
      objectives: rankable
        .map((outcome) => outcome.result.objective)
        .filter((score) => score !== null),
      work,
      best: best === undefined ? null : { slotId: best.slot.id, result: best.result },
      blocks,
    };
  });
}
