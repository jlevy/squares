---
type: is
id: is-01m4qfk7nzmgrwxdj50b3h3k5w
title: Label every issue; intake label in the runbook and sweep
kind: task
status: in_progress
priority: 2
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T07:17:53.470Z
updated_at: 2026-10-12T07:30:32.390Z
started_at: 2026-10-12T07:18:01.788Z
---

## Notes

## Labels, 2026-10-12

Owner's ask (2026-10-12): every issue tagged, `intake` on reports of new items.
Inventory: 68 issues on jlevy/squares (pull requests excluded), 53 in
packing/campaign/result-requests.yaml, 15 not (#500, #501, #503 to #506, #521 to #529).
Before: 57 issues had no label; #308, #358, #367, #375, #400, #411, #413, #419, #445
and #472 had `n-17`; #405 had `n-17` and `tracker`. No issue had `intake`. Every
existing label was set by jlevy.

Classes:

- Intake reports, 64: the 45 register `result-report` entries; #295 and #308
  (`defect-report`, but they offer counterexamples, replacement results or a refutation
  the record took in); #358 (`other`, certificates for two n17 classes offered for
  admission); #367 (`other`, the B2 branching method offered for the repository); and
  the 15 unregistered issues, each of which offers results (#523 is also a compute
  request).
- Trackers, 2: #317 (owner's n = 11 umbrella), #405 (n17 tracker).
- Notice, 1: #411 (repositories moved).
- Bug, 1: #445 (verifier memory, fixed by PR452).

Added: `intake` to 64 issues, `n-17` to #494, #495 and #523, and `tracker` to #317. That
is 68 labels on 65 issues. Every label was added after re-reading the issue's live labels.
None was removed. #405, #411 and #445 were left as they were. After the edits, a fresh
listing shows all 68 issues labelled and every planned label present.

Doubtful: #358 and #367 are `other` in the register, but each offers an item for the
record. #367 in particular is a method report. #411's `n-17` is arguable, since the
notice covers ten repositories, two of them n17, but the owner set it. No label looks
wrong.

Change table (scratch copy:
/tmp/claude-0/-home-user-squares/387dc0a2-0a91-51c6-bf71-f69e33945398/scratchpad/labels/changes.md):

| issue | register kind | labels before | added | reason |
| ---: | --- | --- | --- | --- |
| #170 | result-report | none | intake | register kind result-report |
| #227 | result-report | none | intake | register kind result-report |
| #238 | result-report | none | intake | register kind result-report |
| #247 | result-report | none | intake | register kind result-report |
| #256 | result-report | none | intake | register kind result-report |
| #279 | result-report | none | intake | register kind result-report |
| #280 | result-report | none | intake | register kind result-report |
| #281 | result-report | none | intake | register kind result-report |
| #282 | result-report | none | intake | register kind result-report |
| #294 | result-report | none | intake | register kind result-report |
| #295 | defect-report | none | intake | defect report offering counterexamples and replacement results (T-083..T-086) |
| #296 | result-report | none | intake | register kind result-report |
| #308 | defect-report | n-17 | intake | defect report offering a refutation of DS7 Theorem 9's argument |
| #309 | result-report | none | intake | register kind result-report |
| #316 | result-report | none | intake | register kind result-report |
| #317 | correction | none | tracker | owner's umbrella for the n = 11 proof |
| #358 | other | n-17 | intake | certificates for two n17 classes offered for admission |
| #363 | result-report | none | intake | register kind result-report |
| #366 | result-report | none | intake | register kind result-report |
| #367 | other | n-17 | intake | the B2 branching method offered for the repository |
| #368 | result-report | none | intake | register kind result-report |
| #375 | result-report | n-17 | intake | register kind result-report |
| #399 | result-report | none | intake | register kind result-report |
| #400 | result-report | n-17 | intake | register kind result-report |
| #401 | result-report | none | intake | register kind result-report |
| #413 | result-report | n-17 | intake | register kind result-report |
| #414 | result-report | none | intake | register kind result-report |
| #419 | result-report | n-17 | intake | register kind result-report |
| #420 | result-report | none | intake | register kind result-report |
| #422 | result-report | none | intake | register kind result-report |
| #425 | result-report | none | intake | register kind result-report |
| #428 | result-report | none | intake | register kind result-report |
| #432 | result-report | none | intake | register kind result-report |
| #438 | result-report | none | intake | register kind result-report |
| #446 | result-report | none | intake | register kind result-report |
| #451 | result-report | none | intake | register kind result-report |
| #465 | result-report | none | intake | register kind result-report |
| #470 | result-report | none | intake | register kind result-report |
| #471 | result-report | none | intake | register kind result-report |
| #472 | result-report | n-17 | intake | register kind result-report |
| #476 | result-report | none | intake | register kind result-report |
| #481 | result-report | none | intake | register kind result-report |
| #483 | result-report | none | intake | register kind result-report |
| #484 | result-report | none | intake | register kind result-report |
| #485 | result-report | none | intake | register kind result-report |
| #486 | result-report | none | intake | register kind result-report |
| #488 | result-report | none | intake | register kind result-report |
| #489 | result-report | none | intake | register kind result-report |
| #494 | result-report | none | intake,n-17 | register kind result-report |
| #495 | result-report | none | intake,n-17 | register kind result-report |
| #500 | unregistered | none | intake | not in the register; body offers results |
| #501 | unregistered | none | intake | not in the register; body offers results |
| #503 | unregistered | none | intake | not in the register; body offers results |
| #504 | unregistered | none | intake | not in the register; body offers results |
| #505 | unregistered | none | intake | not in the register; body offers results |
| #506 | unregistered | none | intake | not in the register; body offers results |
| #521 | unregistered | none | intake | not in the register; body offers results |
| #522 | unregistered | none | intake | not in the register; body offers results |
| #523 | unregistered | none | intake,n-17 | not in the register; body offers results |
| #524 | unregistered | none | intake | not in the register; body offers results |
| #525 | unregistered | none | intake | not in the register; body offers results |
| #526 | unregistered | none | intake | not in the register; body offers results |
| #527 | unregistered | none | intake | not in the register; body offers results |
| #528 | unregistered | none | intake | not in the register; body offers results |
| #529 | unregistered | none | intake | not in the register; body offers results |
