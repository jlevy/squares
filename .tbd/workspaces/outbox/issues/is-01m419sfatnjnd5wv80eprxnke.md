---
type: is
id: is-01m419sfatnjnd5wv80eprxnke
title: "n17 admission rule: five frictions found admitting SW9 and N1 (exp-250)"
kind: task
status: open
priority: 2
version: 6
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
delegate: claude-code@vm
labels:
  - n17
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
hold: null
hold_until: null
created_at: 2026-10-03T16:33:08.953Z
updated_at: 2026-10-05T05:37:24.517Z
started_at: 2026-10-03T22:34:45.908Z
---
Lane A3, admitting SW9 (flag 3) and N1 in exp-250 (53fe57147), found five frictions in
census_n17_certified’s admission rule.
1. The receipt’s directory must equal the entry’s certificate path exactly, so a
   certificate directory cannot be renamed (both admitted ones are still *-pending)
   without another 6-8 min verification.
   Match on the seed and node content ids instead.
2. A verifier revision is admitted on a YAML comment ('only I/O changed'). Consider
   tying the listing to the verifier test file passing at that revision.
3. evidence is checked for existence only.
   It is a pointer, not a check; say so or drop it.
4. H-267 is scoped to arity <= 7, but the census counts every arity (SW9 is 9, N1 is
   17). Re-scope H-267 or register a census hypothesis.
5. Producer costs (1,521 s, 3,723 s, the 3,767 s check-saved, the stall controls) appear
   in no round’s wall_seconds; exp-250 counts only the verifications.
   Constraint: OR-16 as amended.
   No new digest comparison; the integrity-ceremony ratchet must still pass.

## Notes

6. (2026-10-03, after lane V1, 318c28c42.) Every kernel verifier revision listed before
   318c28c42 accepts an uncovered zero-area row, and those from e0b66f07b on also accept
   an uncovered one-point section.
   Neither branch ran on W7, SW9 or N1, so their admissions stand.
   New admissions should be verified at 318c28c42 or later.
   The census does not enforce that yet: it counts a receipt from any listed revision.
   Decide whether to restrict the older listings to the receipts that already use them.
   7\. The n11 receipts register (upstream 27660cf18) names three verification depths for
   a receipt; consider the same vocabulary for n17 admission.

7. (2026-10-03 evening, 74b9b686f.) Items 1, 3 and 6 are fixed.
   (1) A verification matches its certificate by the content ids in the objects’ file
   names, compared as names with nothing hashed, so an admitted certificate directory
   can be renamed without re-verifying.
   (3) `evidence` is documented as a pointer checked only to exist, and the census
   output says so in `evidence_note`. (6) A verifier listing may carry `admits`:
   556561586 admits W7, 25c1cdef6 admits SW9 and N1, and e0b66f07b and 575795e02 admit
   none. A new entry must be verified at 318c28c42 or a later revision with the same
   file. The census on the committed ledger is unchanged (4 admitted, 126,168 states,
   15,953 orbits); 22 tests.
   Items 2, 4, 5 and 7 are open.
   9\. The streamed kernel verifier (601bbf110, lane M1) is committed but not listed; its
   review is its own bead.

2026-10-05 (PR 347 status survey).
Items 2, 4, 5 and 7 are open.
Item 4 (H-267 is scoped to arity <= 7 while the census counts every arity) has to be
settled before the composed argument.
