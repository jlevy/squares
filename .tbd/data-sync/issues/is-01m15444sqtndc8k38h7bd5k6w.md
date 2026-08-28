---
type: is
id: is-01m15444sqtndc8k38h7bd5k6w
title: Run the full gate and merge
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m15219m6eh8fww5pm9sc2sqd
created_at: 2026-08-28T21:23:59.414Z
updated_at: 2026-08-28T21:23:59.414Z
---
Full `packing-validate`, not `--fast`, before the PR merges.

`--fast` runs 16 of 38 steps and skips precisely the surfaces this reorg is most likely
to have broken: the generated views, the negative controls (whose sandbox logic changes
in this epic), the atlas builders, and the provenance replay.

Expected to pass unchanged, and worth confirming rather than assuming:

- Provenance. Engine commits recorded in experiment artifacts stay reachable because
  `git mv` does not rewrite history, but the check reads `PROJECT_ROOT / campaign/series`
  and PROJECT_ROOT has moved.
- Negative controls. `run_negative_controls.py` clones the repo and works in a
  subdirectory `HERE`, a design that exists specifically because one control targets
  `.flowmarkignore` two levels up. After the move that file is one level up instead, so
  `HERE` and the `COPY_SEPARATELY` special case both change, and the sandbox must still
  contain the control's target rather than reaching back into the real working tree.
- `check_bead_tree.py`, which resolves `.git/tbd/data-sync-worktree` from the repo root.

Also run `make check` and `make format-check` at the root, and confirm CI is green on
both the Linux `validate` job and `macos-portability` before merging.
