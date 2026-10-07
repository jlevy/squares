---
type: is
id: is-01m4ajza0v5kmszfe5j6mwtzf8
title: "Senior correctness and security review of squish #401 import"
kind: task
status: closed
priority: 1
version: 7
delegate: squish_senior_review
labels: []
dependencies: []
parent_id: is-01m4ajdxfkfqyr1yj5d4wm5npt
hold: null
hold_until: null
created_at: 2026-10-07T07:06:47.195Z
updated_at: 2026-10-07T11:57:37.142Z
started_at: 2026-10-07T07:07:20.799Z
closed_at: 2026-10-07T09:25:16.521Z
close_reason: |
  Completed and accepted senior review. Semantic v2 receipts, source refresh, motion updates, reader citations/math presentation, and local cost admission findings are closed, including collection-override and setup-only bypasses. Independently replayed all 311 retained motions; final 27 cost tests passed after the initial 24-test acceptance, and five-then-one admission with fresh v3 evidence preserved all 581 historical weights and prior caps/cohorts. Publication and hosted CI remain tracked by the parent and author beads; remote tracker sync is denied, so closure is preserved locally and in the outbox.
resolution: null
duplicate_of: null
---

## Notes

Senior correctness and security review completed and accepted.
Parent authorized closure of this review deliverable; branch publication, hosted CI, and
author communication remain tracked in the parent and author beads.
The frozen review artifact is
docs/project/reviews/review-2026-10-06-squish-import-correctness.md in the confirmation
checkout. No source, records, or review documents changed during closure.

Findings S1-S5 are closed: deterministic control replay, successful-verdict binding,
strict source and checker metadata, consistent verdict diagnostics, and genuine source
refresh with preserved historical verification.
The initial byte-hash binding was superseded under OR16/OR18 by semantic v2 receipts
containing complete deciding inputs.
External raw-source SHA pins remain; generated facts and certificates have no repository
self-pin, integrity exception, or raised baseline.
Selected source adoption rebuilds exact source bounds and safe display ceilings,
regenerates lower-bound content, verifies source ownership and confirmation evidence,
and refuses missing declarations.

Independent geometry and publication evidence: 40 semantic/importer/atlas/supersession
tests passed in 9.89 seconds; 14 final regeneration, ownership, confirmation-display,
and missing-section tests passed in 3.99 seconds; semantic n108 dual replay and both
complete negative controls passed.
The complete semantic fast gate passed.
All 11 confirmed records retain exact source S in both exact_form fields with safe
ceiling displays and open optimality status.
All 11 atlas geometries equal their source-derived geometry.
All 311 retained positive motions were independently replayed against current geometry
in 53.091 seconds, at the recorded numerical tolerance.
Source bytes, external Git tree, and the complete registration roster were independently
checked. Parent evidence includes the full semantic replay in 75.594 seconds, 53 focused
tests in 11.14 seconds, and a complete 324-case motion screen.

Follow-up motion and reader findings are closed.
Targeted motion updates require a complete unique retained roster, current unselected
identities, compatible input and deciding-method settings, preserved unselected records,
and rebuilt aggregates.
Independent selected-screen checks passed 17 tests in 18.14 seconds.
The reader link fix recognizes only strict repository issue/discussion citations while
retaining pinned/non-main/missing-file checks; 18 independent tests passed in 2.39
seconds. Canonical inline-math headline delimiters preserve the exact statements and
fractions while permitting existing quotient line breaks.
The confirmed-adoption fixture fix passed independently in both checkouts.

Cost admission accepted after closing the demonstrated pre-collection override and
setup-only execution gaps.
Effective collection patterns, collection controls, requested whole-module paths, test
counts, filters, deselections, provenance, and shard state now fail closed for local
evidence. The regressions actually omit a failing test through a collection override or
skip its body through setup-only mode, and verify refusal.
Effective setup-only, setup-plan, and collect-only controls must all be false.
Initial independent admission/plugin checks passed 24 tests in 1.05 seconds; the final
execution-control checks passed 27 tests in 1.70 seconds.
Fresh v3 unfiltered reports measured five reported modules (54 tests, 9.514 recorded
seconds) and the separate confirmation receipt module (16 tests, 1.287 recorded
seconds). An independent in-memory five-then-one admission preserved all 581 historical
weights and every existing metadata, cap, and cohort field, preserved the first five
admitted weights on the second admission, and added exactly the intended six modules.
No budgets or thresholds increased.

No correctness or security finding remains open in this review scope.
Final cost data adoption and broader publication gates belong to the parent.
Tracker pull succeeded; remote tracker push remains denied with HTTP 403. Closure state
is saved in the local tracker and outbox for parent publication.
