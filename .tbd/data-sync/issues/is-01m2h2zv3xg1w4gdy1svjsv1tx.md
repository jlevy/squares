---
type: is
id: is-01m2h2zv3xg1w4gdy1svjsv1tx
title: "Consolidate the workbench stack: #155 into #160 into #171"
kind: task
status: in_progress
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-14T23:10:44.859Z
updated_at: 2026-09-14T23:10:49.148Z
---
Owner, 2026-09-14: "Can you review and consolidate if we have duplicate work on other branches? Check https://github.com/jlevy/squares/pull/171" and "Let's review carefully and see what the best strategy here is to merge everything together."

The stack: #125 (spike workbench, to main) <- #155 (annealing record, strategy plan, page fixes on the spike) <- #160 (draft; package consolidation, by Codex) <- #171 (owner interface revisions on the package, by another Claude session).

Overlap found:
- No feature is implemented twice. But the same page lives in two trees: #155's six page fixes were made in the spike, which #160 deletes, and #171's five revisions in the package.
- #160 carried annotated copies of X-029, the runbook and exp-208, which conflict with #155's cleaned record.
- The two sessions tracked owner UI feedback in separate beads that interact: the box size against #171's thicker, box-first box.

Done locally in `.claude/worktrees/consolidate-stack`, nothing pushed:
- `consolidate/160-with-155` (6094ae5a): #155 merged into #160, with the page fixes ported into packages/workbench and the record resolved toward #155.
- `consolidate/171-with-all` (26d44ee5): that merged into #171 with no textual conflicts, plus a retune for #171's box (drawing 949 px, headline 21 px: 56/55 px, at least 4.6 px of moving clearance).
- Both pushes would be fast-forwards.
- Checks pass on the combined tree: npm run check (117), package pytest (124), Biome, tsc, check_probes (186), build_site, check_frontend, ledger, synopsis. check_workbench stops where it did on #160 (think-7sw8).

Recommendation: push both merges, fold #171 into #160, then land #125, #155 and #160 in order. From now on, page work happens only in packages/workbench on the tip.
