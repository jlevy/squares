# The annealing benchmark’s runbook

The campaign asks which declared packing strategies improve the distribution of valid
outcomes under equal work on cases not used for tuning.
The
[workbench plan](../../../../docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md)
governs implementation; the
[annealing plan](../../../../docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md)
defines the experimental comparison.

## Retained record and current limits

`summaries.json` contains the summaries retained when 185 MB of raw JSONL was removed
from the branch at `6e191a35`. The raw files named inside it are not present in this
checkout. A summary is insufficient to replay exact geometry, reconstruct disjoint
blocks, or recover total elapsed time.
Do not pass it to the raw-trial replay command or treat its `best_of` values as
distributions.

The old divide-and-concur experiment keeps `exp-206`. The colliding blind-run record is
now `exp-210`; `exp-207` through `exp-210` carry dated corrections, reachable source
mappings and explicit unrecorded timing.
Their original accounts remain visible, but their verdicts are unresolved pending
reproducible evidence.
The discarded compaction pass in `exp-209` cannot exclude translation or rotation repair
as an improvement.

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

The current legacy harness can be invoked from `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.bench_annealing \
    --n 5 10 11 17 26 29 --seeds 2000 --anneal 6
uv run --frozen --all-extras --group dev python -m devtools.bench_annealing \
    --replay /path/to/retained-trials.jsonl
```

The Phase 1 admission repair and Phase 3 shared kernel replace this legacy instrument
before new comparative conclusions are accepted.
Existing commands are reproduction routes, not evidence that their known defects are
fixed.

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

Continue from [H-206 through H-211](../../ideas.md#workbench-physics-as-a-search), the
[ledger](../../ledger.md), and the governing plan.
Do not repeat the old monotone difficulty claim or the claim that n=17 was tested only
at shake 6; retained summaries include unresolved n=17 level-8 cells, while the retained
deep level-8 artifact contains n=11 only.
The plan assigns the detailed cohort reconciliation to `think-jdgu`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
