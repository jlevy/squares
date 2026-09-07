# exp-115: Independent Pair-Certificate Review

Disposition: **reject H-105**. The single independent file replay returned exit 0 and
`no-pair-obstruction`: all 134 eligible pairs have checked separating axes.
This is a negative result for the predicted pair obstruction, not acceptance of the
density candidate. H-099 and the candidate’s full a.e. feasibility remain unresolved.

This is `think-hql2`, W6 research-loop, commissioned for 2026-09-06, 22:02:20–22:16:00
UTC. The
[prospective exp-115 record](../../experiments/exp-115-h-105-fixed-candidate-pair-obstruction.md)
was committed at `a40b40d36760708d422facb803c8eefc1d23aa21` before target execution.
It fixed the source, weights, 134-pair inventory, stopping rule, and separate 30-second
producer and replay caps.
The reviewer found no static protocol blocker and did not invoke target binding or
geometry before the coordinator’s explicit packet dispatch.

## Checked Result and Scope

The [producer packet](packet.json) names `exp-113-candidate-v1`, reports 134 eligible
pairs and 134 separation records, and has `witness: null`. Its first and last canonical
pairs are `[0,2]` and `[57,59]`. The [independent replay](replay.json) reconstructed and
bound the exact source geometry and fixed weights against the frozen accepted parent,
enumerated eligible pairs independently, and required one correctly ordered separation
record for every pair.

For each pair, the reader checked that the supplied axis has exact unit length and that
every vertex of the first square projects on or below every vertex of the second.
Linearity extends those inequalities to the whole squares.
Their interiors are therefore disjoint; boundary contact is permitted.
Missing, repeated, or reordered records could not have produced the no-pair verdict.
All 134 eligible pairs were checked; there was no unverified remainder within that
finite pair inventory.

The candidate’s unchanged eight per-member weights are $(1,0,2/5,1/10,0,1/10,3/10,0)$ on
the retained 60-placement D4 support.
Pairs outside the eligible inventory have weight sum at most one.
This result excludes only an overweight pair obstruction.
Three or more squares may still produce excess depth without any eligible overlapping
pair, as demonstrated by the predeclared triple control in the
[instrument review](../agenda-026/bc-254-pair-separator-independent-review.md).

Thus the result applies the frozen
[H-105 criterion](../../../../hypotheses/H-105-exp113-overweight-pair-obstruction.md)
against its prediction.
It neither accepts nor refutes H-099, changes the retained $[11,56/5]$ supremum bracket,
nor establishes a packing bound.
No new LP row, changed weight, support extension, or higher-order geometric check
follows from this replay.

## Frozen Execution and Cost

The coordinator dispatched one successful producer run, with actual exit 0, from clean
source revision `cf299e6c7516c2ad41ba05c8e4ac8bb3ca16b5c6`. The reviewer ran the
ordinary outer checker once from the same frozen checkout,
`/private/tmp/squares-pair-check.tQXUTv/packing`, using that checkout’s parent packet.
The reviewer’s observed start and finish were **22:08:08–22:08:09 UTC**.

```bash
/usr/bin/time -p env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3 -m devtools.check_full_size_density_pair_separator /Users/levy/wrk/github/squares/packing/campaign/series/series-000-smoke-and-calibration/results/exp-115-h-105-fixed-candidate-pair-obstruction/packet.json --parent campaign/series/series-000-smoke-and-calibration/results/exp-113-h-099-trump-support-screen/packet.json --timeout-seconds 30
```

Stdout is retained verbatim in [replay.json](replay.json).
Worker timing and process-timer stderr are retained verbatim in
[replay.log](replay.log).
The process used **0.75 seconds wall and 0.73 seconds CPU** (`user 0.70`, `sys 0.03`).
Its worker reported 0.6037460420047864 seconds wall and 0.600491 seconds CPU. The cap
did not expire and no guard refused the input.
There was no second replay.

For comparison of accounting scopes, the separately owned [producer log](run.log)
reports 1.05 seconds process wall and 1.03 seconds CPU (`user 0.99`, `sys 0.04`), with
worker times 0.8997154590906575 seconds wall and 0.8931140000000001 seconds CPU. These
are costs of the single producer and checker, not benchmark estimates or total agent
time.

The checker independently verifies candidate-pair certificates, while sharing the exact
number field, single-square validation, canonical geometry key, and accepted original
source validation described in the instrument review.
It does not repeat the parent LP proof or independently attest Git state and process
history. The accepted parent and coordinator-recorded clean source/protocol provenance
supply those prerequisites.

Only `replay.json`, `replay.log`, and this review were written.
The reviewer did not run the producer, repeat the checker, or change source, registries,
Git, or beads.
Any next full positive-area-face verification requires a separate decision
and budget. Experiment-loop governed the frozen criterion and one-shot accounting; tbd
review guidance kept certificate validity separate from provenance.
Practical Prose and Flowmark guided the report.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
