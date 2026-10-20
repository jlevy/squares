---
type: is
id: is-01m4wsrbkd61qxbpgxphckpd6v
title: "Ledger input for 2026-10-14: snapshot of the result issues and every reported side, exact where a lane's claims.json holds it"
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
created_at: 2026-10-14T08:51:39.245Z
updated_at: 2026-10-14T11:29:19.924Z
started_at: 2026-10-14T08:51:46.993Z
closed_at: 2026-10-14T11:29:19.924Z
close_reason: "Done on claude/serene-hopper-xxh80m (jlevy/squares#601): devtools.intake_ledger with 21 tests, and packing/campaign/issue-intake/upper-bounds-20261014/ (sources, issue snapshot, frozen starts, ledger.yaml/json, README). Fable review docs/project/reviews/review-2026-10-14-intake-ledger.md: 305/306 steps agree on recomputation, no blocking finding; its majors fixed in 19b7d0303. PR #574 re-render on its lane's final head stays with think-a30g."
resolution: null
duplicate_of: null
---
packing/campaign/issue-intake/upper-bounds-20261014/: github-issues.json (number, author, created_at, title of every result report and the #503/#504 comments and PR #574) and ledger.yaml (each report's claims: n, printed side and rounding as the report prints it, and the exact side where a lane's acquisition/claims.json at a named branch commit holds it).
