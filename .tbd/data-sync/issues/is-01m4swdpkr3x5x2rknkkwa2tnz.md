---
type: is
id: is-01m4swdpkr3x5x2rknkkwa2tnz
title: Work down the reconciliation needs_evidence list (3 open after rounds 1-3)
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels: []
dependencies: []
parent_id: is-01m0r7tk07nw6nb8wyzv4v776z
created_at: 2026-10-13T05:40:32.503Z
updated_at: 2026-10-13T05:40:32.503Z
---
Owns every item a bead reconciliation left at needs_evidence that is still open, so the next round does not have to rediscover them (PR #493 review A, A6). Reproduce the list from packing/ with: python -m devtools.reconcile_work SNAPSHOT.json --needs-evidence ../docs/project/reviews/review-2026-10-10-bead-reconciliation-a.json ../docs/project/reviews/review-2026-10-10-bead-reconciliation-b.json ../docs/project/reviews/review-2026-10-12-bead-reconciliation-applied.json ../docs/project/reviews/review-2026-10-13-owner-decisions-applied.json (oldest first; a later round's disposition supersedes). Open on 2026-10-13: think-5jr5 (whether a full checkpoint on a head with #434 and #439 passes the 300 ms no-JS controls and the 0.1 CLS limit), think-e7c8 (worktrees on the owner's Mac, unobservable from a cloud session), and the atlas-expansion-to-324 plan (owner's scope call: stop at 324, or build the caveated 325-400 form; think-vb7g). Done when each is decided or re-homed and the command lists nothing.
