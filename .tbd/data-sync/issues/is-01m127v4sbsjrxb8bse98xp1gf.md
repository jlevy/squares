---
type: is
id: is-01m127v4sbsjrxb8bse98xp1gf
title: Merge main into the packing agenda branch and take PR 48 out of draft
kind: task
status: closed
priority: 1
version: 2
labels:
  - packing
dependencies: []
created_at: 2026-08-27T18:31:15.498Z
updated_at: 2026-08-27T21:12:50.634Z
closed_at: 2026-08-27T21:12:50.624Z
close_reason: Done in session 031 (commits 1efeb8b..313ff18). Merged origin/main; two conflicts resolved toward main on evidence (session-025 kept main's terminalization with the exact pushed SHA and CI run; ledger.md regenerated). The merged tree failed two gate steps the pre-merge tree passed - main's atlas SVG work pushed the negative-control mutation snapshot to 42,441,211 bytes against a 41,943,040 cap. Fixed by pruning atlas/known-best/rendering and contact-overlays, the direct analogue of the already-pruned prospective renderings; snapshot now 37,269,354 with 4.46 MiB headroom, pinned by test assertions. Full gate green on the merged revision, GitHub validate passed in 5m37s, PR 48 out of draft and CLEAN.
resolution: null
duplicate_of: null
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
