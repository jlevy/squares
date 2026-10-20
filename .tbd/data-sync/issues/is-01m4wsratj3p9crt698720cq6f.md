---
type: is
id: is-01m4wsratj3p9crt698720cq6f
title: "intake_ledger: a tool that orders every open upper-bound report by when it reached the record and decides, per count, which to record"
kind: task
status: closed
priority: 1
version: 4
delegate: serene-hopper
labels:
  - result-import
dependencies:
  - type: blocks
    target: is-01m4wsrcd61weyq0xjpyk4xbqv
parent_id: is-01m4wsqt2sjrksybyz375sarb3
hold: null
hold_until: null
created_at: 2026-10-14T08:51:38.450Z
updated_at: 2026-10-14T11:29:19.917Z
started_at: 2026-10-14T08:51:46.983Z
closed_at: 2026-10-14T11:29:19.917Z
close_reason: "Done on claude/serene-hopper-xxh80m (jlevy/squares#601): devtools.intake_ledger with 21 tests, and packing/campaign/issue-intake/upper-bounds-20261014/ (sources, issue snapshot, frozen starts, ledger.yaml/json, README). Fable review docs/project/reviews/review-2026-10-14-intake-ledger.md: 305/306 steps agree on recomputation, no blocking finding; its majors fixed in 19b7d0303. PR #574 re-render on its lane's final head stays with think-a30g."
resolution: null
duplicate_of: null
---
packing/devtools/intake_ledger.py and packing/tests/test_intake_ledger.py (OR-1). Rule: at each count, walk the reports by reported_at; a report is recorded where its side is decidably below the standing side (the case record's reported lane, or a register entry pending adoption, or the current beyond-horizon row, or the grid) and below every earlier report; an equal or larger side is not recorded and its verdict names the earlier report that holds it; an undecided comparison (print precision) is reported, never guessed. Reuses upper_bound_reports.printed_span/relation.
