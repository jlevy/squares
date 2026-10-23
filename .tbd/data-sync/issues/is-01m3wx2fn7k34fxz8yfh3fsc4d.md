---
type: is
id: is-01m3wx2fn7k34fxz8yfh3fsc4d
title: Hold a register entry scope to the scopes of its cited evidence, and extend the register coverage gate to upper bounds by others
kind: task
status: closed
priority: 2
version: 4
delegate: c-gates-1023
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3nrt5zy2g6dpegq1fbczpzg
hold: null
hold_until: null
created_at: 2026-10-01T23:33:54.982Z
updated_at: 2026-10-23T09:08:21.606Z
started_at: 2026-10-23T06:19:04.544Z
closed_at: 2026-10-23T09:08:21.606Z
close_reason: "Delivered: check_results.scope_problems holds a scope to its evidence, and the register coverage gate reads upper bounds (7bb6f63f5); T-045's n = 32 evidence was already on main. PR #748 head 417ba331b, CI green (Packing validation run 39927824318, Certificate page 39927824335)."
resolution: null
duplicate_of: null
---
W7. check_results does not compare a result scope with its evidence scopes: T-045 claims s(32) >= 119/20 and cites one entry whose scope is 27, 28, 31. The coverage gate reads lower bounds only, so T-056, T-057 and T-065 are registered by convention. Add both checks with negative controls, and add the n = 32 evidence entry for T-045 from the retained replay receipt.

## Notes

2026-10-23 c-gates-1023 (PR #748): check_results.scope_problems refuses an entry whose scope holds a count no cited evidence covers, and the register coverage gate (coverage_problems) now reads case upper bounds as well as lower; epistemics.md and the runbook say so. Both pass on main with no record change: T-045's n = 32 evidence is already on main (E-wand125-rectangle-source-replay's scope holds 32), and T-056, T-057, T-065 and every other recent upper bound have their entries. Commit 7bb6f63f5; tests test_a_scope_its_evidence_does_not_cover_is_refused and test_a_recent_case_upper_bound_is_covered_as_a_lower_bound_is.
