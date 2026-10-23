---
type: is
id: is-01m5mn0ct9k37pvwdy4dgs11e6
title: "PR #751 (merge): senior review, address, gate"
kind: task
status: closed
priority: 1
version: 4
delegate: c-rev-751-1023
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T15:10:26.121Z
updated_at: 2026-10-23T17:06:11.210Z
started_at: 2026-10-23T15:10:27.170Z
closed_at: 2026-10-23T17:06:11.209Z
close_reason: "PR #751 merged 2026-10-23 as 05e95db36 after review A (https://github.com/jlevy/squares/pull/751#issuecomment-6368595518), dispositions (issuecomment-6369458790), a merge of main and one re-run of two jobs failed outside the PR (bead store; slow runner)."
resolution: null
duplicate_of: null
---

## Notes

**2026-10-23, review A posted (c-rev-751-1023).** Senior engineering review, round 1, PR comment https://github.com/jlevy/squares/pull/751#issuecomment-6368595518 at head 7d0806e1883f89bd0ced14e4c349c012f7304e39, base c1115c0956104e40571d26de439c91917911d554. Verdict: approve with changes; no Blocker or High.

- A1 (Medium): the records take C3 from the review lane's own check_theorem_c.py and say the gradec.py re-run "reaches no rung" (result-requests.yaml:7748, review lines 477-478, PR Limits, think-7scz). Stage 4 needs the source's checker or a first-party one whose soundness was adversarially reviewed. Fix: a correctness review of the checker, or keep the gradec.py re-run (about 10.6 CPU-h) as the C3 route in the backlog.
- A2 (Medium): the key [Daniel exact and local reports 2026-10-12] has lineage independent and no credit, but the source's tasks/exact-minpoly/README.md lines 1, 4, 48 and 161 say it works over this register's records.
- A3 (Low): no source-coverage entry cites E-evand-gradec-local-minima-233-report.
- A4 (Low): check_certificate_citations counts case-record citations only, or a 30-day deferral; a register entry does not cite a certificate for it. Three sentences say otherwise.
- A5 (Low): the 23 October fetch of the 232 forms is not dated in the packet.
- A6 (Low): three statements the receipts do not bear out: the process count, "24 rows" (24 at each), and the timeouts "go away".
- A7 (Low): V-evand-gradec-review-compare and -derivatives have no independence block.

Dedicated review recommended: correctness, of check_theorem_c.py (it would also discharge A1).

Checked: custody of all 233 forms against the upstream tree at 31523f8 (blob ids and sizes); check_added_blobs PASS (1.83 MB); MIT. No rung moves (results.yaml unchanged). Re-ran check_theorem_c.py at 13 counts: identical to the receipts. My own float check at 9 counts agrees with the certificates. Four extra mutations were all refused. packing-validate --records passed, and 347 targeted tests passed.
