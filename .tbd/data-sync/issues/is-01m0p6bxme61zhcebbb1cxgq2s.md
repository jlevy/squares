---
type: is
id: is-01m0p6bxme61zhcebbb1cxgq2s
title: "PR #5 review F-4: renumber residue: broken links, dead output path, wrong claim"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m0p6bwcyve6zdv41ezr08e3g
created_at: 2026-08-23T02:14:34.893Z
updated_at: 2026-08-23T02:30:05.004Z
closed_at: 2026-08-23T02:30:05.003Z
close_reason: "FIXED. All five stale references corrected plus a sixth the review did not catch (miscounted ../ depth). Compensating controls added: a relative-link checker in ledger.py, and a rule that a reserved id may be named but not linked. Both negative-controlled."
---
From series-001 -> series-000 and H-00x -> H-01x. Three broken links, run_baseline.sh writing to the dead directory, exp-001 method.record stale, traps.md linked with five ../ where six are needed, and the board asserting a reserved id H-004 is registered. Structural note: ledger.py's reserved-ids exemption MASKS the H-004 case by design, so a relative-link checker is the compensating control, plus a rule that a reserved id may not be a link target.
