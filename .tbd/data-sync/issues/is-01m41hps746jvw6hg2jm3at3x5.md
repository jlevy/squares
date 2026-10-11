---
type: is
id: is-01m41hps746jvw6hg2jm3at3x5
title: Delete imported replay and transfer branches after checking the beads that cite their commits
kind: task
status: open
priority: 2
version: 4
labels:
  - session-169
  - owner-decision
dependencies: []
parent_id: null
created_at: 2026-10-03T18:51:29.380Z
updated_at: 2026-10-04T01:09:57.793Z
---
Lane D measured 76 session and replay branches without a PR holding 60.6 MB unique (mostly transfer/), which every default clone and full-history CI job fetches. Beads cite 26 of their commits (20 on claude/optimistic-gauss-uzmcl2; one each on four replay branches, result-import-process and nice-fermi-v8fhi2), so those citations need re-pointing or the branches keeping. Deleting remote branches is irreversible from a clone's point of view; owner decision. GitHub storage drops only after GitHub's own maintenance.

## Notes

2026-10-04 01:05 UTC: moved out from under think-gmef to the top level. think-gmef was closed at 00:37 UTC with this bead open, and an open bead under a closed parent fails check_bead_tree (D-025's first invariant) in every pull request's validate job (jlevy/squares#315 at 6c5036895). Kept open as the owner decision it is; re-parent it wherever it belongs.
