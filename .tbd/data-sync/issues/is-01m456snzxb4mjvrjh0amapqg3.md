---
type: is
id: is-01m456snzxb4mjvrjh0amapqg3
title: Rebuild Guzhou's n17 stack (PRs 325, 333, 351, 352) onto PR 347 without PR 307's dumps and certify it
kind: task
status: closed
priority: 1
version: 8
assignee: claude
delegate: claude-code@vm
labels: []
dependencies: []
child_order_hints:
  - is-01m45f1jvr8mq9q7q1ajveh3g7
  - is-01m45f2ak71t5b3h9evk65mwjt
  - is-01m45f376m2jqsm1t29jteg8q8
  - is-01m45f3gxdbms4wekyer6s1j9e
hold: null
hold_until: null
created_at: 2026-10-05T04:57:47.773Z
updated_at: 2026-10-06T08:11:26.490Z
started_at: 2026-10-05T04:58:02.944Z
closed_at: 2026-10-06T08:11:26.489Z
close_reason: "Done. Stack 357 (#347 -> #354 -> #355 -> #356 -> #360 -> #365) merged into main at 01:12 UTC 2026-10-06 (merge a6279886b); #352 closed 2026-10-05 11:23 UTC, as were #325, #333 and #351 at 07:02 UTC. Review B round 1 dispositions: think-qh0i (#354) closed, all four findings addressed; think-114f (#355), think-a0pu (#356) and think-dm11 (#360 plus stack-level) closed, all findings addressed except the session-record 'independent replay' wording residuals, now follow-ups think-9pvm, think-qm0l and think-oy5v (P2, parent think-tmz6), and #356 B2. Session certification is tracked separately by think-q0z7, which stays open: Sessions 170-172 and 177-179 are certified on main; 174-176 still carry certification_pending."
resolution: null
duplicate_of: null
---
PR 307 was closed and rebuilt as PR 347 without its 112.5 MB of certificate dumps (OR-18). PRs 325, 333, 351 and 352 sit on PR 307's history, so merging any of them would bring the dumps into main. Rebuild each as a claude/ branch by cherry-picking Guzhou's commits (authorship preserved) onto PR 347, re-render the records, verify Guzhou's Review A fixes and finish what is left, open the replacements as a formal stack, drive CI green, then comment on and close the originals as authorized. The rebuilt sessions stay certification_pending on this bead until a hosted fast gate passes on the rebuilt history.

## Notes

2026-10-05 07:30 UTC (bead bookkeeper). State:
- Rebuilt and opened as formal stack 357 (created 05:53 UTC): #347 -> #354 (producer memo, was #325) -> #355 (raw residual supports, was #333) -> #356 (enhanced-core supports, was #351) -> #360 (fixed-witness certificates, was #352). Heads reviewed: f19ab81bd, 018ee13c5, 1a73d1e86, 451154f60. #355, #356 and #360 are drafts and must be marked ready before the merge.
- Originals: #325, #333, #351 closed 07:02 UTC; #361 (duplicate of #350) closed 06:59 UTC; #352 stays open until #360 is green.
- Provenance: tag archive/guzhou-review-a-333 -> 9a1143ab9 preserves every commit #355/#356/#360 cite from guzhou/review-a-backup-333 (21 checked); README lines naming it are being added by the cascade lane (think-mmss, think-owo5, think-3ho2).
- Review B round 1 (2026-10-05 07:04 UTC): think-qh0i (#354), think-114f (#355), think-a0pu (#356), think-dm11 (#360, with the stack-level review). Certification of Sessions 170-172 and 174-179 (each layer's B2): think-q0z7. CI wall-time verdicts on every layer: think-umlx. Stack blocker: #347 B1, think-jhgi.
- Merge: gh stack merge 360 --yes --merge, run by the owner, after #347 B1, green CI on every layer and the session certifications. This bead closes after the stack merges and #352 is closed.
