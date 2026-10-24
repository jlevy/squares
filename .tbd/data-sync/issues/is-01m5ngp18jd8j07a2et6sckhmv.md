---
type: is
id: is-01m5ngp18jd8j07a2et6sckhmv
title: "check_requests: a recorded-reservation hold still reads 'pending the owner's confirmation' after the owner stated no preference"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T23:14:06.738Z
updated_at: 2026-10-23T23:14:06.738Z
---
Found by c-land-753-1023 (think-uhgf) on 23 October 2026 while recording the four hold notes on PR #753 (commit 695a07431). The owner, asked in conversation on 23 October which of #557, #565, #570 and #574 should stay reserved, stated no preference, so the holds stand with basis recorded-reservation (think-5ip2's notes). The notes in packing/campaign/result-requests.yaml now say so, but packing/devtools/check_requests.py hold_text() derives ', pending the owner's confirmation' from basis alone, so --report, the closeable blockers and intake_sweep still print it, and the schema's basis description (packing/campaign/schemas/result-requests.schema.yaml) says a recorded-reservation hold 'awaits the owner's confirmation'. tests/test_check_requests.py (hold_text and the live-record invariant) and tests/test_intake_sweep.py pin that wording. Decide whether the derived text should change (for example a basis or field for a reservation the owner was asked about and left standing), or whether 'pending' is still accurate since the owner did not confirm; the coordinator's or owner's call, not a records lane's.
