---
type: is
id: is-01m2b80w08820xxzv5cfgtrhc6
title: The campaign gate fails 15 ways on the overnight round, id collision first
kind: bug
status: open
priority: 0
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
created_at: 2026-09-12T16:43:14.823Z
updated_at: 2026-09-12T16:43:14.823Z
---
`packing-ledger check` fails 15 ways on the overnight annealing work. The campaign has a drift gate and the round was recorded without running it, so four experiments sit in the tree outside the record they claim to be part of.

```
FAIL duplicate experiment id exp-206: exp-206-h210-blind-runs-are-not-packings.md, exp-206-projection-search.md
FAIL ideas.md: does not mention H-206 ... H-211          (6x)
FAIL exp-206..209: numerical experiment requires actual precision, rounding, and tolerance   (4x)
FAIL exp-206..209: terminal round without an effort block                                    (4x)
FAIL ledger.md is stale; run `packing-ledger render`
```

**The id collision is the serious one.** `exp-206` already meant "divide and concur over a bounded container" from 2026-09-09, and that meaning is cited from `ledger.md`, from `X-025`, and from `devtools/sweep_structure_hints.py`. The older artifact keeps the id; the new one moves to the next free number, with its filename, its `id:`, its body heading and the "the guard landed in exp-206" line in exp-207 all moved with it. Ids are the merge surface, and a collision is the one error that leaves both sides internally valid.

The rest are the schema doing its job: a numerical experiment must declare precision, rounding and tolerance, and a terminal round must account for its effort. Both were skipped because nothing ran the gate.

**The process fix is the point, not the fifteen repairs.** The gate exists; the overnight round never called it. It belongs in the runbook's round loop beside `--replay`, so recording an experiment and validating it are one step.
