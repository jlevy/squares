import {
  browserSearchSource,
  createBrowserSearchPlan,
  parseBrowserSearchSeeds,
} from "../api/search-api.ts";
import type { SearchOutcome, SearchOutcomes, SearchPlan } from "../search/contracts.ts";
import { selectedSearchState } from "../search/contracts.ts";
import { decodeSearchOutcomes, encodeSearchOutcomes, statusCounts } from "../search/outcomes.ts";
import { createPackSearchRunner } from "../search/pack-runner.ts";
import { runSearchPlan, SearchObserverError } from "../search/scheduler.ts";
import { type SearchCohortSummary, summarizeSearch } from "../search/summary.ts";

export interface SearchPanelOptions {
  document: Document;
  onChange?: () => void;
}

export interface SearchPanelState {
  active: boolean;
  running: boolean;
  plan: SearchPlan | null;
  ledger: SearchOutcomes | null;
  observed: readonly SearchOutcome[];
  message: string;
}

export interface SearchPanel {
  setVisible(visible: boolean): void;
  visible(): boolean;
  redraw(): void;
  start(): Promise<void>;
  cancel(): void;
  state(): SearchPanelState;
}

function required<T extends Element>(document: Document, id: string, kind: { new (): T }): T {
  const element = document.getElementById(id);
  if (!(element instanceof kind)) {
    throw new Error(`Search panel requires #${id}`);
  }
  return element;
}

function outcomeRow(document: Document, outcome: SearchOutcome): HTMLTableRowElement {
  const row = document.createElement("tr");
  const result = outcome.status === "completed" ? outcome.result : null;
  const selected = result === null ? null : selectedSearchState(result);
  const columns = [
    String(outcome.slot.seed),
    outcome.status,
    selected?.valid === true ? "valid" : selected === null ? "—" : "invalid",
    result?.objective === null || result === null ? "—" : result.objective.toFixed(6),
    result?.stationarity.stationary === true ? "yes" : "no",
  ];
  for (const value of columns) {
    const cell = document.createElement("td");
    cell.textContent = value;
    row.append(cell);
  }
  return row;
}

/**
 * One line per cohort of what a finished ledger holds: validity among completed slots,
 * stationarity, rankable slots, the physics and repair work spent, and each block's best objective.
 */
export function formatSearchSummary(summaries: readonly SearchCohortSummary[]): string[] {
  return summaries.map((summary) => {
    const blocks =
      summary.blocks.length === 0
        ? "none"
        : summary.blocks
            .map(
              (block) =>
                `${block.bestObjective === null ? "none" : block.bestObjective.toFixed(6)} (block ${block.block})`,
            )
            .join(", ");
    return (
      `${summary.partition} n = ${summary.n}: ` +
      `${summary.validityRate.numerator} of ${summary.validityRate.denominator} completed valid, ` +
      `${summary.stationary} stationary, ${summary.rankable} rankable; ` +
      `${summary.work.physicsSteps} physics steps, ${summary.work.repairIterations} repair iterations; ` +
      `best objective by block: ${blocks}`
    );
  });
}

/**
 * What the panel keeps when a run rejects. An observer failure still carries a complete ledger of
 * the outcomes collected so far, which stays exportable and resumable; any other error has none.
 */
export function searchRunFailure(error: unknown): {
  ledger: SearchOutcomes | null;
  message: string;
} {
  if (error instanceof SearchObserverError) {
    return {
      ledger: error.outcomes,
      message: `Search stopped: ${error.message}. Export the ledger to keep its finished slots; resuming it runs the rest.`,
    };
  }
  return {
    ledger: null,
    message: `Search could not run: ${error instanceof Error ? error.message : String(error)}`,
  };
}

function ranked(outcomes: readonly SearchOutcome[]): SearchOutcome[] {
  return [...outcomes].sort((a, b) => {
    const aObjective = a.status === "completed" ? a.result.objective : null;
    const bObjective = b.status === "completed" ? b.result.objective : null;
    const aValid = a.status === "completed" && selectedSearchState(a.result)?.valid === true;
    const bValid = b.status === "completed" && selectedSearchState(b.result)?.valid === true;
    const aRank = aValid && aObjective !== null ? aObjective : Infinity;
    const bRank = bValid && bObjective !== null ? bObjective : Infinity;
    return aRank - bRank || a.slot.index - b.slot.index;
  });
}

export function mountSearchPanel(options: SearchPanelOptions): SearchPanel {
  const { document } = options;
  const workspace = required(document, "search-workspace", HTMLElement);
  const nInput = required(document, "search-n", HTMLInputElement);
  const seedsInput = required(document, "search-seeds", HTMLInputElement);
  const stepsInput = required(document, "search-steps", HTMLInputElement);
  const proposalInput = required(document, "search-proposal", HTMLSelectElement);
  const repairInput = required(document, "search-repair", HTMLInputElement);
  const startButton = required(document, "search-start", HTMLButtonElement);
  const cancelButton = required(document, "search-cancel", HTMLButtonElement);
  const exportButton = required(document, "search-export", HTMLButtonElement);
  const importInput = required(document, "search-import", HTMLTextAreaElement);
  const resumeButton = required(document, "search-resume", HTMLButtonElement);
  const status = required(document, "search-status", HTMLOutputElement);
  const progress = required(document, "search-progress", HTMLOutputElement);
  const results = required(document, "search-results", HTMLElement);
  let active = false;
  let running = false;
  let controller: AbortController | null = null;
  let plan: SearchPlan | null = null;
  let ledger: SearchOutcomes | null = null;
  let observed: SearchOutcome[] = [];
  /** Summary lines for `ledger`, empty while a run is producing it. */
  let summaryLines: readonly string[] = [];
  let message =
    "Experimental search. Results are exploratory and have not passed research acceptance.";
  const stamped = (name: string): string | null =>
    document.querySelector(`meta[name="${name}"]`)?.getAttribute("content") ?? null;
  const source = browserSearchSource(
    stamped("squares-workbench-revision"),
    stamped("squares-workbench-dirty"),
  );

  const currentPlan = (): SearchPlan => {
    const proposal = proposalInput.value;
    if (proposal !== "grid" && proposal !== "random") {
      throw new RangeError("Choose grid or random start");
    }
    return createBrowserSearchPlan({
      n: Number(nInput.value),
      seeds: parseBrowserSearchSeeds(seedsInput.value),
      physicsSteps: Number(stepsInput.value),
      proposal,
      repair: repairInput.checked,
      source,
    });
  };

  const redraw = (): void => {
    workspace.hidden = !active;
    for (const input of [nInput, seedsInput, stepsInput, proposalInput, repairInput]) {
      input.disabled = running;
    }
    startButton.disabled = running;
    cancelButton.disabled = !running;
    exportButton.disabled = ledger === null;
    resumeButton.disabled = running;
    importInput.disabled = running;
    status.textContent = message;
    const shown = new Map((ledger?.outcomes ?? []).map((outcome) => [outcome.slot.index, outcome]));
    for (const outcome of observed) {
      shown.set(outcome.slot.index, outcome);
    }
    const visibleOutcomes = [...shown.values()];
    const counts = statusCounts(visibleOutcomes);
    const total = plan?.slots.length ?? 0;
    const done = visibleOutcomes.length - counts.notStarted;
    const line = `${done}/${total} slots; ${counts.completed} completed, ${counts.failed} failed, ${counts.cancelled} cancelled, ${counts.timedOut} timed out, ${total - done} pending`;
    progress.replaceChildren(
      line,
      ...summaryLines.flatMap((text) => [document.createElement("br"), text]),
    );
    results.replaceChildren(
      ...ranked(visibleOutcomes).map((outcome) => outcomeRow(document, outcome)),
    );
  };

  const execute = async (resume?: SearchOutcomes): Promise<void> => {
    if (running) {
      return;
    }
    try {
      const declared = currentPlan();
      if (resume !== undefined) {
        decodeSearchOutcomes(resume, declared);
      }
      plan = declared;
      ledger = resume ?? null;
      observed = [];
      summaryLines = [];
      running = true;
      controller = new AbortController();
      message =
        resume === undefined ? "Experimental search running." : "Resuming exact saved plan.";
      redraw();
      ledger = await runSearchPlan(declared, createPackSearchRunner({ batchSteps: 20 }), {
        concurrency: 1,
        signal: controller.signal,
        ...(resume === undefined ? {} : { resume }),
        onOutcome: (outcome) => {
          observed.push(outcome);
          redraw();
        },
      });
      summaryLines = formatSearchSummary(summarizeSearch(declared, ledger));
      message = controller.signal.aborted
        ? "Experimental search cancelled. Export the ledger to retain completed slots."
        : "Experimental search finished. Inspect valid ranked results and export the ledger.";
    } catch (error: unknown) {
      const failure = searchRunFailure(error);
      message = failure.message;
      if (failure.ledger !== null) {
        ledger = failure.ledger;
        summaryLines = formatSearchSummary(summarizeSearch(ledger.plan, ledger));
      }
    } finally {
      running = false;
      controller = null;
      redraw();
    }
  };

  startButton.addEventListener("click", () => {
    void execute();
  });
  cancelButton.addEventListener("click", () => controller?.abort());
  resumeButton.addEventListener("click", () => {
    try {
      const raw: unknown = JSON.parse(importInput.value);
      const declared = currentPlan();
      const imported = decodeSearchOutcomes(raw, declared);
      void execute(imported);
    } catch (error: unknown) {
      message = `Ledger rejected: ${error instanceof Error ? error.message : String(error)}`;
      redraw();
    }
  });
  exportButton.addEventListener("click", () => {
    if (ledger === null) {
      return;
    }
    const blob = new Blob([encodeSearchOutcomes(ledger)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${ledger.planId}.json`;
    link.click();
    globalThis.setTimeout(() => URL.revokeObjectURL(url), 0);
  });
  redraw();
  return {
    setVisible(visible) {
      if (active === visible) {
        return;
      }
      active = visible;
      if (!visible) {
        // A hidden search would keep spending the page's time with nobody watching it.
        controller?.abort();
      }
      redraw();
      options.onChange?.();
    },
    visible: () => active,
    redraw,
    start: () => execute(),
    cancel: () => controller?.abort(),
    state: () => ({ active, running, plan, ledger, observed: [...observed], message }),
  };
}
