---
type: is
id: is-01m2h2zv3xg1w4gdy1svjsv1tx
title: "Consolidate the workbench stack: #155 into #160 into #171"
kind: task
status: in_progress
priority: 1
version: 12
labels: []
dependencies: []
child_order_hints:
  - is-01m2h8cc6m0w30p7vd0g5r6161
  - is-01m2hb401yy3ph99cfn5mhpcv4
  - is-01m2hb40g8vbnq8914rkt7p87c
  - is-01m2hb40z4hvrre5f0219zp1m9
  - is-01m2hb41hy7fx18dy67asht84d
  - is-01m2hf4b7raa0yecm3dcepmgb7
created_at: 2026-09-14T23:10:44.859Z
updated_at: 2026-09-15T04:05:13.115Z
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

## Notes

2026-09-14: the #125 review is posted (https://github.com/jlevy/squares/pull/125#pullrequestreview-5204313901): 39 findings (2 Blocker, 8 High, 21 Medium, 8 Low), pinned to 7b06254c, verdict "changes required before merge". Seven are carried from the 2026-09-12 architecture review (R1, R2, R7, R8, R9, R10) and the consumer inventory.

Addressing rule for the stack, decided before any addresser starts: **fix each defect at the lowest PR where its code exists in its final form.**
- Most of #125's page, export, capture and strategy findings live in spike or devtools files that #160 moves into packages/workbench, and some (R1, R10) are already stronger there.
- Those get a disposition on #125 pointing at the #160 (or #171) commit that fixes them, after verification, not a second fix in code the stack deletes.
- Findings in code that persists through the stack (CI, gates, docs, the Rust engine, motion-lab assets, devtools #160 does not move) are fixed on #125 and merged up.

To avoid fixing one defect twice, wait for the #155, #160 and #171 reviews, dedupe findings across the stack into one triage map (finding, PR, final code location, owning lane), then run addressers by lane with address-pr-review, each posting per-finding "Addressed ... in <commit>" replies on the PR whose review raised the finding.

**2026-09-14, review addressing under way.**
- Triage map: `attic/reviews/triage-stack-2026-09-14.md` in the squares-viz-explanations worktree. It reduces the 96 findings to 91 defects; section 5 holds the coordinator's decisions.
- Main #173 was merged up the stack. The new heads are #125 `6f30d5b7`, #155 `c131b76f`, #160 `f3874426`, #171 `fcfd0d7a` and #175 `d723c847`.

Wave 1 lanes, one worktree each:

| Lane | PR | Worktree | Branch |
| --- | --- | --- | --- |
| A | #125 | `stack-125` | `stack/125` |
| B | #155 | `squares-viz-explanations-4ae624` | |
| C | #160 | `consolidate-stack` | `lane/c` |
| D-page | #160 | `nojs-guard` | `lane/d-page` |
| D-tools | #160 | `lane-d-tools` | `lane/d-tools` |

Each PR has a parent bead: `think-6c2j`, `think-xqc3`, `think-jp7o` and `think-kuau`.

Lanes write dispositions to `attic/reviews/dispositions/`; the coordinator posts one reply per PR. Next:
1. Merge A up the stack.
2. Merge B into #160, then send C the `D10` runbook citation, and D-tools `D68` and the `D89` plan line.
3. Send D-page `D11` and the `D12` keyboard case once C's `D07` lands.
4. Merge #160 into #171, then run lane E.
5. Merge #171 into #175.
6. Post the dispositions, update every PR body and watch CI.
