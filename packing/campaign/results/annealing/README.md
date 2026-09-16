# The annealing benchmark’s runbook

The campaign asks which declared packing strategies improve the distribution of valid
outcomes under equal work on cases not used for tuning.
The
[workbench plan](../../../../docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md)
governs implementation; the
[annealing plan](../../../../docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md)
defines the experimental comparison.

## What is retained

`summaries.json` holds one entry per run file: the median `closed` and the best of the
first k runs, per cell.
The package summariser,
[`summarize_annealing.py`](../../../../packages/workbench/tools/workbench_tools/summarize_annealing.py),
wrote it from the per-trial rows, and rebuilds it from them.

- **Cells marked `resolved: true`** were scored on runs repaired to packings.
  They are the only cells any finding may cite.
  The flag means the rows carry the repaired side; the summariser counts every row and
  refuses none.
- **Cells marked `resolved: false`** were scored before any validity check, on
  arrangements with overlapping squares.
  They are void.
- **Best-of-k is a prefix of one seed stream**, not a distribution, and several files
  replay the same seeds.

**The per-trial rows are not retained.** The 185 MB of JSONL was removed from the branch
at `6e191a35`, `.gitignore` keeps new rows out, and no copy is published.
Nothing in the repository alone re-checks a cell or splits it into disjoint blocks.

**The rows can be regenerated, at each round’s recorded commit.** The historical rows
came from `devtools.bench_annealing`, which #160 deletes, run on a page built from the
round’s engine commit (the `engine_commit` in its experiment record).
Every run is seeded, so that command, run at that commit, should write the same rows
again; rows written by the package benchmark, or after the page’s physics changed, will
not match. That has been checked for one file: on 2026-09-14 the recorded command below,
run on #155’s branch where the harness still exists (recorded in `8a0f9a61`),
regenerated all 30,000 rows of `resolved-5k-a6.jsonl` in 82 seconds, and every cell
matched `summaries.json` apart from the median milliseconds.

From the repository root, check out that commit in its own worktree.
From the worktree’s `packing/`, build the page as that commit’s harness documents, then
run the round’s recorded command, naming the file as its `summaries.json` entry does:

```bash
git worktree add ../annealing-rows <engine-commit>
uv run --frozen --all-extras --group dev python -m devtools.bench_annealing \
    --n 5 10 11 17 26 29 --seeds 5000 --anneal 6 --budget 3600 \
    --out campaign/results/annealing/resolved-5k-a6.jsonl
```

Then, from this checkout’s `packing/`, compare the regenerated rows with the committed
summaries:

```bash
uv run --frozen --all-extras --group dev squares-workbench-summarize-annealing \
    --rows ../../annealing-rows/packing/campaign/results/annealing --check
uv run --frozen --all-extras --group dev squares-workbench-summarize-annealing \
    --rows ../../annealing-rows/packing/campaign/results/annealing --overlaps
```

`--check` compares each run file present with its committed entry and says how many it
compared. `--overlaps` reports the overlap figures X-034 cites, over the files whose
every cell is resolved.

What those cells show is written up in
[X-034](../../explorations/X-034-the-workbench-physics-as-a-search.md).
`workbench_tools.historical_summary_audit` lists every cell with its flags, from
`packing/`:

```bash
uv run --frozen --all-extras --group dev python -m workbench_tools.historical_summary_audit \
    campaign/results/annealing/summaries.json --out ../attic/annealing-summary-audit.json
```

## New comparisons

New rounds use the package benchmark, never the historical harness, and follow the steps
under [One round](#one-round).
From `packing/`:

```bash
uv run --frozen --all-extras --group dev squares-workbench-benchmark \
    --n 5 10 11 17 26 29 --seeds 2000 --anneal 6
uv run --frozen --all-extras --group dev squares-workbench-benchmark \
    --replay ../attic/retained-trials.jsonl
```

**The tolerance in use, and its control.** The package benchmark admits a trial only if
its raw and repaired arrangements pass the workbench’s one validity contract: every pair
and wall penetration at most 1e-9 of a unit side, the count, finiteness, unit size, an
area lower bound and a coordinate limit.
That is the tolerance Pack, Resolve and Search use, shared by `PACKING_VALIDITY` in
`packages/workbench/src/core/runtime-contracts.ts` and
`packages/workbench/tools/workbench_tools/packing_contracts.py` and pinned by
`packages/workbench/tests/fixtures/packing-validity.json`, which both test runners read
(#160, `ec0a0604`). It is chosen, not measured, and no retained control justifies it:
none is needed, because nothing is admitted at a looser value.
The 1e-5 threshold the historical rounds used, and that `--overlaps` still reports
against, came from a snapped control that was run once and never kept (`think-2ngs`),
and applies to those records only.

Historical campaign records retain their original instrument paths at their source
commits. New comparative conclusions use the package command and its admission receipts.

## One round

1. Choose a registered hypothesis, control, candidate, held-out cases, seed blocks and
   work budget before running.
   Declare the accept rule and stop condition.

2. Run the instrument’s guards, including finite geometry, exact square count, positive
   container side, pair and wall checks.
   Record source revision, dirty state, configuration version, effective seed,
   environment and measured elapsed time.

3. Retain the raw trial receipt and displayed geometry, with separate raw and repaired
   checks. Repair may stall or exhaust its budget; it is not guaranteed to produce a
   packing. Invalid or incomplete outcomes never enter ranking.

4. Replay the retained receipt through the same admission contract.
   Group equal-work trials into disjoint seed blocks and report best-of-k median, range,
   valid/refused counts, leftover trials and cost.
   One prefix best-of-k is one observation.

5. Write the experiment artifact, preserving negative results and the original
   criterion. Record the raw artifact location; if too large for Git, retain an
   accessible immutable artifact reference and manifest rather than deleting the only
   inputs to the report.

6. Regenerate and validate the record immediately, from `packing/`:

   ```bash
   uv run --frozen --all-extras --group dev packing-ledger render
   uv run --frozen --all-extras --group dev packing-ledger check
   uv run --frozen --all-extras --group dev packing-validate --records
   ```

## Metrics and acceptance

`closed = (grid - side) / (grid - record)` is the fraction of the record-to-grid gap
closed by a checked arrangement.
One is the record, zero is the grid and a negative value is worse than the grid.
Cases where the denominator is zero need an absolute side metric instead.
A numerically checked improvement is not a proved new bound.

Compare control and candidate distributions at equal declared work and report their
spread. Keep tuning and held-out cases separate.
A better median, a single lucky seed, or a visually flat tail does not by itself
establish the registered claim.

Continue from the open hypotheses
[H-207 through H-211](../../ideas.md#workbench-physics-as-a-search), the
[ledger](../../ledger.md), and the governing plan.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
