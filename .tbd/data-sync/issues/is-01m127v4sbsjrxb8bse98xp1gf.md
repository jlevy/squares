---
type: is
id: is-01m127v4sbsjrxb8bse98xp1gf
title: Merge main into the packing agenda branch and take PR 48 out of draft
kind: task
status: open
priority: 1
version: 1
labels:
  - packing
dependencies: []
created_at: 2026-08-27T18:31:15.498Z
updated_at: 2026-08-27T18:31:15.498Z
---
PR 48 (codex/packing-ten-hour-research-agenda -> main) carries sessions 027, 028 and 029 plus the guard repairs. It is still a draft and is behind origin/main by 6 commits as of 2026-08-27.

Deliberately not done inside session 029: merging main rewrites files underneath the measurements that session recorded (the exhaustive_exact profile, the full-gate timings, and the negative-control anchor), so it belongs in its own slice where the gate can be re-run against the merged tree rather than the pre-merge one.

Scope:
  - merge origin/main into the branch and resolve conflicts
  - re-run the full packing-validate against the merged tree, not --fast
  - if the round count or any generated aggregate moved in the merge, re-check devtools/controls.yaml anchors, which is the exact rot that killed the round-aggregate negative control
  - re-render ledger.md and defects.md and confirm the synopsis handoff still points at the latest session
  - take PR 48 out of draft only once that gate is green

Sequencing: run this after think-cja6 lands, so the guard repairs are in the tree that gets merge-tested rather than being merged on top of an unguarded one.
