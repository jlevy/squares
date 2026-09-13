---
type: is
id: is-01m2e52mry1qw2v6vkskf1yha7
title: Bind BC329 evidence commit directly to execution revision in run sheet
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: codex@spud10.local
labels:
  - n11
  - calibration
dependencies: []
parent_id: is-01m2e4b5m0xrgxkzqcrxmbb5q0
hold: null
hold_until: null
created_at: 2026-09-13T19:49:30.525Z
updated_at: 2026-09-13T19:58:58.669Z
started_at: 2026-09-13T19:49:58.728Z
closed_at: 2026-09-13T19:58:58.668Z
close_reason: PR156 commit 9c56e901 retains the maintained five-step verifier run sheet, direct evidence-commit parent checks, refusal and acceptance reports, and the exact formatted sheet blob 29517a3f accepted by independent Sol high rereview. Records and edit tiers pass. Operational integrated-head review, remote equality, positive profiles, and evidence admission remain under think-pp3j.
resolution: null
duplicate_of: null
---
Independent exact-diff rereview of the verifier-wired PR156 run sheet REFUSED because source-closure did not require the evidence commit to have EXECUTION_REV as its direct sole parent. Reproduction in /private/tmp/pr156-run-sheet-exact-rereview.md. Add precommit HEAD equality and postcommit single-parent equality, preserve the tree and source checks, independently rereview final bytes, and do not run a positive profile or BC329 target before admission.

## Notes

Independent rereview reproduced that an intervening document-only commit could pass prior staged/committed source-closure assertions. Run sheet now checks HEAD == EXECUTION_REV and tracked worktree clean immediately before evidence commit, then requires rev-list --parents of EVIDENCE_COMMIT to equal EVIDENCE_COMMIT EXECUTION_REV. Target-free Git controls accept direct child and refuse moved head, extra merge parent, and unstaged edit. Independent exact-diff rereviews ACCEPTED the repaired preformat and pinned-Flowmark formatted sheet blob 29517a3f. Awaiting PR156 commit/validation; no positive profile or BC329 target.
