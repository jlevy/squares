---
type: is
id: is-01m2gxxkh5msmctek525ahbsmb
title: The snap control behind the 1e-5 tolerance was never code; build it as a retained control
kind: bug
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
parent_id: is-01m29kqwefbzzpt7bngm68pq6p
created_at: 2026-09-14T21:42:08.671Z
updated_at: 2026-09-15T03:43:40.359Z
closed_at: 2026-09-15T03:43:40.358Z
close_reason: "Superseded rather than built: no looser tolerance remains. Benchmark admission uses the 1e-9 contract (ec0a0604), the repair and blind gates assert no control (fbc74c0e), and the runbook cites the contract as the tolerance in use (2db57cae). Record wording is lane B's D29."
resolution: null
duplicate_of: null
---
The benchmark's validity tolerance (1e-5 of a side, deepest pair) is justified everywhere by a control: a snapped run ends on the record's poses and scores 5.5e-7 to 1.0e-6. **That control was never runnable code.** BASE `packing/devtools/bench_annealing.py` TRIAL_JS calls `A.physics(index, o.style, "blind")` with the mode hard-coded (verified 2026-09-14), so exp-210's recorded command cannot produce its snap row. On PR #160 the probe also hard-codes blind (`packages/workbench/probes/bench-annealing.ts:250`) and admission refuses any other mode (`workbench_tools/trial_records.py:565`), and `trial_records.py:27` now says only "Matches the retained catalogue precision" (audit 2026-09-14).

Build it as a retained control:
- a control run of the snapped (and free) modes that reports the deepest final overlap per n, recorded with the trials and never admitted to ranking;
- the tolerance's comment and the runbook cite that control's output;
- a test fails if the snapped control scores above the tolerance, or if a known overlapping arrangement scores below it.

Until then X-029 and exp-210 say the control is recorded, not reproducible (done in the 2026-09-14 rewrite).

## Notes

2026-09-14, PR #155 review lane B (D29, think-iusp): the record half is done on #155. exp-207, exp-208 and exp-210 record the tolerance as chosen and name the unretained snapped observation, exp-210's control reads "none retained", H-210's regime follows, and X-034 and exp-210 give the table's ratios instead of "two orders of magnitude". The retained control, the tolerance comment and the runbook citation remain with this bead and PR #160's review item D10.

2026-09-14, PR #160 review lane C (D10, #160 R5; #155 R5 harness items): the benchmark no longer uses a looser tolerance, so no snap control is needed to justify one. The 1e-5 constant and its justification are gone and admission checks raw and repaired geometry at the shared 1e-9 contract (ec0a0604); the repair gate is documented and refuses a non-converged repair, and the blind-mode gate says no snapped control is admitted or needed (fbc74c0e). Remaining before closure: the annealing runbook's citation of this, after lane B's #155 record merges up. Record wording is D29 on #155.

2026-09-15, lane C: the runbook citation landed in 2db57cae. The annealing runbook states that the package benchmark admits under the 1e-9 validity contract, chosen and pinned by the shared fixture, that no retained control justifies it and none is needed, and that the historical 1e-5 applies to those records only.
