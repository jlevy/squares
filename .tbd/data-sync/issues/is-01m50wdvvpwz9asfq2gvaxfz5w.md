---
type: is
id: is-01m50wdvvpwz9asfq2gvaxfz5w
title: "Intake process: add a regularization step to result-import.md stages (on adoption/registration of a new best), with a gate that fails on an unregularized current drawing"
kind: task
status: in_progress
priority: 1
version: 3
delegate: ecstatic-edison-reg-intake
labels:
  - regularization
dependencies: []
parent_id: is-01m50wdrbfnwsq05w150az5z88
hold: null
hold_until: null
created_at: 2026-10-15T22:55:18.902Z
updated_at: 2026-10-16T04:59:20.714Z
started_at: 2026-10-16T04:17:15.710Z
---

## Notes

2026-10-16T04:55Z (ecstatic-edison-reg-intake): branch claude/ecstatic-edison-8en33t-regularization-intake pushed to origin, head 09ba0c143, from origin/main e2e018f32. No PR yet.

Done (3 commits):
- c50444bfe feat(adopt_houses): regularization_owed(), printed after a write and --dry-run: re-housed counts, which are certain to read pending (strong view lapses / earlier lapse), PENDING_ALLOWED and SETTLED entries the new witness bears on, cost 5-15 CPU-min a count, and the "When a Witness Changes" commands (build_known_best_atlas --update, axis --update-atlas --n, default_drawings --update, grid-slack 0.5/1/5, evand run, regularize_select), ending with the --check-state gate. Docstring post-step now the guide's steps. Tests in test_house_adoption.py (2 new) and test_default_drawings.py (adoption replay extended: allowlisted with a bead passes, entry naming no bead fails).
- 8deda0776 docs: result-import.md stage 5 "Adopt a House, Then Regularize It" (cost from run receipts, compute cap, defer to PENDING_ALLOWED with bead in the same PR, gate); Running an Intake Pass step 3, The Prompt step 4, stage table. Guide "When a Witness Changes" and policy sections 5 and 8 cross-linked.
- 09ba0c143 chore(release): ReleaseNoPublicChange for packing/devtools/adopt_houses.py (4 papers + site).

Validated locally: packing-validate --edit pass (68/110, 569 s), --records pass (52/110, 107 s), focused pytest 67 passed, ruff/basedpyright zero on changed files, check_release_impact --baseline-ref origin/main ok, release_pin --check ok (288a1a52022f). packing-validate --push was running at push time.

Left: confirm --push result; open DRAFT PR (labels project + S1; body drafted at scratchpad g3q7_pr_body.md, passes check_pr_description); watch CI to green (#538 animate-view flake may be re-run once); never merge. Close think-g3q7 only after the PR merges.
