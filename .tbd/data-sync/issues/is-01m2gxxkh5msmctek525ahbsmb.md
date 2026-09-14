---
type: is
id: is-01m2gxxkh5msmctek525ahbsmb
title: The snap control behind the 1e-5 tolerance was never code; build it as a retained control
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
parent_id: is-01m29kqwefbzzpt7bngm68pq6p
created_at: 2026-09-14T21:42:08.671Z
updated_at: 2026-09-14T21:42:31.609Z
---
The benchmark's validity tolerance (1e-5 of a side, deepest pair) is justified everywhere by a control: a snapped run ends on the record's poses and scores 5.5e-7 to 1.0e-6. **That control was never runnable code.** BASE `packing/devtools/bench_annealing.py` TRIAL_JS calls `A.physics(index, o.style, "blind")` with the mode hard-coded (verified 2026-09-14), so exp-210's recorded command cannot produce its snap row. On PR #160 the probe also hard-codes blind (`packages/workbench/probes/bench-annealing.ts:250`) and admission refuses any other mode (`workbench_tools/trial_records.py:565`), and `trial_records.py:27` now says only "Matches the retained catalogue precision" (audit 2026-09-14).

Build it as a retained control:
- a control run of the snapped (and free) modes that reports the deepest final overlap per n, recorded with the trials and never admitted to ranking;
- the tolerance's comment and the runbook cite that control's output;
- a test fails if the snapped control scores above the tolerance, or if a known overlapping arrangement scores below it.

Until then X-029 and exp-210 say the control is recorded, not reproducible (done in the 2026-09-14 rewrite).
