---
type: is
id: is-01m2dzgknq7k2cj3ea91thkcmj
title: Publish independently accepted BC303 T1 reader as a separate stacked PR
kind: task
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - pr
  - bc303
dependencies: []
parent_id: is-01m2b8watk22ejr9s0zhgrdd17
created_at: 2026-09-13T18:12:16.695Z
updated_at: 2026-09-13T20:29:40.168Z
---
After think-3jsz reaches exact-head acceptance, base a new research branch on the current PR156 head, cherry-pick or port only the T1 source-bound replay, retained review, and narrow research record. Open a separate PR stacked above PR156, measure its unique diff and validation/cost separately, and keep the local counterexample distinct from BC329 calibration. Do not claim T2/global owner routing or a stronger n11 bound.

## Notes

Read-only stack prep retained at /private/tmp/bc303-t1-stack-prep.md. Isolated clean T1 head 74ec773c has two T1-only commits 88d54d85 then 74ec773c touching reader/tests. Final Astra Max exact-head review ACCEPTED 377-atom source-bound literal replay after 17 retained-record and 10 provenance controls, but new branch must replay at its new execution HEAD and retain a fresh receipt. Keep this separately costed draft above final pushed PR156. Candidate retrospective H-159/exp-157 record IDs and agenda cell require schema/ID verification. Claim only rejection of named BL role-C universal T1 inequality; no T2/global routing/new n11 bound. PR publication awaits PR156 final base.

2026-09-13 local stacked draft in progress: new /private/tmp/squares-n11-bc303-t1-pr156-stack branch codex/n11-bc303-t1-pr156-stack starts at settled local PR156 9c56e901 and cherry-picks only T1 commits 88d54d85 then 74ec773c, giving execution HEAD 81898608213774dcab99a16f776000421b9083ac. All 18 frozen sources match proposal/base/execution/worktree bytes and reviewed reader/test blobs. New 108171-byte 377-row CLI receipt is stdout-identical; independent new-head audit passed all rows, 17 mutation refusals, and 10 provenance controls. Pre-registry records gate passed; focused suite 11/11. H-159, exp-157, BC-338 were free and are being recorded retrospectively with only the named local inequality rejection. Publication remains open pending documentation/record validation, local commit, PR156 push-gate completion, T1 push/full gates, branch-cost rollup, and hosted draft PR checks. No T2/global routing/new s(11) bound claimed.

Local milestone committed as a93b57add884640f512af59e6bf099aaefefdfcc on codex/n11-bc303-t1-pr156-stack; worktree clean. The retrospective H-159/exp-157/BC-338 record and independent review are durable above E=81898608213774dcab99a16f776000421b9083ac. Post-registration records gate passed 32/74, edit gate passed 45/74, focused T1 tests passed 11/11, pinned Flowmark format check and git diff --check passed. The historical execution record remains bound to E. Publication is still open: wait for PR156 gate/base, then T1 --push/full, measured branch-cost rollup, draft PR push and hosted checks. No push or PR opening has occurred on this T1 branch.

2026-09-13 publication draft: cost-first body at /private/tmp/bc303-t1-pr-body-draft.md; detailed cost/validation boundary at /private/tmp/bc303-t1-branch-cost-and-validation.md; privacy-safe native live child snapshot at /private/tmp/bc303-t1-stacked-task-tree-snapshot.yaml. Isolated T1 child root 01a09c5a-edb3-75c3-8c97-7eb47c1a8392 has no descendants and is disjoint from the shared coordinator, PR156, prior old-head T1 review, and T2. Snapshot through 20:26:45 UTC is incomplete: 33 tasks, 32 complete, 1531.467 agent-active seconds, 1429.041 active-union seconds. The maintained branch rollup has no declaring AgentSession; no formal branch-attributed token/model cost is claimed. Unique clean diff from PR156 9c56e901 to a93b57ad: 3 commits, 14 files, +7171/-19 lines. T1 --push/full and remote publication remain pending until PR156 is published and T1 gates run; do not close this bead.
