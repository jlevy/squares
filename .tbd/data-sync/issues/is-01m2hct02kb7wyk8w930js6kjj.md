---
type: is
id: is-01m2hct02kb7wyk8w930js6kjj
title: "PR #125 review D25: projection search feasibility asserted by its own screen; NaN passes; in-process 'out of process' check"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb401yy3ph99cfn5mhpcv4
created_at: 2026-09-15T02:02:19.090Z
updated_at: 2026-09-15T02:13:46.663Z
closed_at: 2026-09-15T02:13:46.662Z
close_reason: "Fixed in 471781af: violation returns inf for non-finite input; solved-run test asks sqpack.verify; verified_out_of_process runs in a child interpreter with count and finiteness guards."
resolution: null
duplicate_of: null
---
Review source: PR #125 review F24 (Medium); triage row D25. The recover_records consumer is fixed in #160 at f9099096 (WT/recover_records.py:198-200).

The projection search's feasibility is asserted only by its own screen: packing/tests/test_divide_and_concur.py :104-119 asserts violation(...) <= 1e-9, the same predicate solve uses; packing/devtools/divide_and_concur.py :264 violation returns 0.0 for a NaN pose; packing/devtools/map_optimum_stability.py :120 trusts it; packing/devtools/run_projection_ratchet.py :457-472 `verified_out_of_process` calls verify_packing in the parent process with no finiteness guard.
