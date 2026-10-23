---
type: is
id: is-01m3wx2g3x57fh5njgjj4ryht5
title: Read the AI-assistance statement from the bibliography and run the check in packing-validate
kind: task
status: closed
priority: 3
version: 4
delegate: c-gates-1023
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3nrt5zy2g6dpegq1fbczpzg
hold: null
hold_until: null
created_at: 2026-10-01T23:33:55.452Z
updated_at: 2026-10-23T09:08:24.024Z
started_at: 2026-10-23T06:19:05.311Z
closed_at: 2026-10-23T09:08:24.024Z
close_reason: "Delivered: AI-assistance statements are typed ai_assistance in the bibliography, the four missing keys added, --check runs in packing-validate's case-prose step, n-011 states its owed sentence (4fa365516). PR #748 head 417ba331b, CI green (Packing validation run 39927824318, Certificate page 39927824335)."
resolution: null
duplicate_of: null
---
W7. state_ai_assistance.STATEMENTS is a hard-coded key list outside packing-validate; four cited keys are absent from it ([evand square-packing 2026-10-01], [franciscouzo square-packing 2026-09-27], [wand125 tools 2026], [Queuingtheorydotcom n11 optimality 2026]) and their case records carry the statement by hand.

## Notes

2026-10-23 c-gates-1023 (PR #748): the statements are a typed ai_assistance (sentence, marker, anchor, optional counts) on bibliography sources, read by state_ai_assistance.load_statements; --check also refuses a bad anchor or a sentence lacking its marker, and runs in packing-validate inside the records step "case prose agrees with its own front matter" (about 1.3 s). The 21 keys of the old list moved; the four named keys joined ([Queuingtheorydotcom n11 optimality 2026] is now [Ahmed n11 optimality 2026]); Couzo's statement is limited to n = 102 and 103; n-011 gained the one sentence it owed. Commit 4fa365516; three new tests in test_state_ai_assistance.py.
