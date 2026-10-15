---
type: is
id: is-01m4yqggay7b6j85jt42qspkmn
title: "Import Francisco Couzo: s(237) <= 15.902603638260 at 4e4c8ce, 2.40e-11 below #607 (no issue)"
kind: task
status: in_progress
priority: 1
version: 2
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-15T02:50:53.662Z
updated_at: 2026-10-15T02:50:59.978Z
started_at: 2026-10-15T02:50:59.973Z
---
Stage 1 triage by the 15 October reads lane (think-mq0k, branch claude/wizardly-meitner-wqn4x3-reads-1015), from the 02:30Z sweep at main 6964362b5.

Source pin: https://github.com/franciscouzo/square-packing at 58a783368d4b7e70bb800f0009ea9ca03e578739 (2026-10-15T01:25:11Z, head of master when read at about 02:45Z). The certificate certificates/n237.cert (blob 788bdc53, SHA-256 e367f769988aaa47ebeb4e5c40d0410c3a0bb23bad50f7478d3d3de452c1da7f, also at certificates/best/n237.cert) was first committed in 4e4c8ce23cb5e87f033021687010992c40575480 ("Update all verified bounds for n < 1024", 2026-10-15T00:31:53Z) and is unchanged at the head. No issue reports it: #607 (filed 2026-10-14T23:18:36Z, not edited since 23:27Z) cites 43ac7d2's submissions/2026-10-14/certificates/n237.cert (blob 3b75c44d), a different file.

Claim: s(237) <= 7951301819129798440089572127137/500000000000000000000000000000 = 15.9026036382595968801791442542740, printed rounded up as 15.902603638260 in certificates/README.md and certificates/best/README.md. certificates/n237.json calls it an "exact optimum" seeded from Mykhailo Polkovskyi's #593 certificate (search job 100230, method fq); the manifest credits Francisco Couzo, construction credit Nate Chaoweeraprasit (itsnaka). So it is the author's precision refinement of his own #607 packing, which itself continues #593.

Report order at 237 (each exact unless printed):
- case T-140 (Chaoweeraprasit, improved by Couzo) 99393435047986448060704927533/6250000000000000000000000000 = 15.90294960767783: the claim is 3.460e-4 below;
- #593 / T-183 (Polkovskyi, 2026-10-14) 15.9027050578664: 1.014e-4 below;
- #607 (Couzo, first committed 43ac7d2 2026-10-14T19:15:09Z) 15.902603638283...: 2.398e-11 below. #607 is the smallest earlier report; its packet is on claude/wizardly-meitner-wqn4x3-intake-607 (think-qik6), not on main, so this packet compares with its print 15.902603638284 (rounded up), which decides it (the claim is at least 2.34e-11 below every number the print may be);
- PR #574 / T-174 15.9029477736582, #561 / T-161, #573, T-136, T-098, T-115, T-127, T-134, #505, #470: all larger. Mishapolk 70a033f has no 237.
Under the per-count rule (a watched-repository publication is a report at its first commit, 2026-10-15T00:31:53Z), the claim is strictly below every earlier report and would be recorded, after #607's 237. It refines #607's own packing, so credit Couzo after Polkovskyi, as #607's.

Nothing else in 4e4c8ce or 58a7833 is a new in-corpus claim: at the other 148 counts n <= 324 the certificates/best/ and certificates/ files are copies of PR #574, #593/70a033f, #606 and the author's own #586 certificates (equal exact sides) or larger, and the Göbel square and strip bounds of 58a7833 are classical closed forms (no discovery claimed). certificates/n211.cert is 487b058's, unchanged (think-nj7h). Beyond 324: 4e4c8ce adds or rewrites several hundred certificates (370 to 1023), think-nj7h's and think-qik6's territory; not triaged here.

Validation, priced: both maintained exact routes through devtools.upper_bound_reports certify, positive plus duplicate-square and outside-container controls; 237 squares, about 28,000 pairs, 30-digit rationals: a few CPU-minutes. No source program runs.
