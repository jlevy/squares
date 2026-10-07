---
type: is
id: is-01m4055fqdnsc95js0egq5sc1t
title: Repo-wide integrity-ceremony audit and removal plan (lane R7)
kind: task
status: open
priority: 0
version: 3
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-03T05:53:05.260Z
updated_at: 2026-10-05T05:37:32.243Z
---
Owner direction 2026-10-03: ‘needless ceremony around things like this is a constant tax
on all development and progress’; ‘we are not validating across a trust boundary …
worrying about correctness’; ‘determinism should not cost rerunning code’.
R7 inventories every hash/digest comparison of repository-owned files,
frozen-blob/frozen-copy comparison, digest-gated refusal (checkpoints, receipts,
caches), forced re-run and internal signing; verdict KEEP (named trust boundary) /
REPLACE (Git revision, small determinism test, semantic comparison) / REMOVE; ranked
implementable slices; proposed OR-16 amendment.
Known n17 instances: MODULE_SHA256, digest-named certificates with name checks, ledger
verifier digests and receipt_sha256, tool/kernel_sha256, capture load_checkpoint
refusing after a byte-identical kernel speedup (forced a 256-row restart).
Deliverable: docs/project/reviews/review-2026-10-03-integrity-ceremony-audit.md.

## Notes

Audit committed 28e48fb0a: 42 mechanisms, 20 KEEP / 13 REPLACE / 6 REMOVE / 2 FROZEN / 1
recording-only. Slices dispatched 2026-10-03 ~06:30 UTC: 1 environment sealing (E1, in
flight) then 6 n11 chain + think-gzju (E1); 2 n17 checkpoint/ledger/verifiers (P2); 3
library round trips + 4 frozen-blob audits (E2); 7 OR-16 amendment + development.md +
growth ratchet check_integrity_ceremony.py (R7); 5 CI history (17 jobs full clone, 174 s
vs 7 s sparse) after 1 and 4.

2026-10-05 (PR 347 status survey).
The OR-16 amendment, the integrity-ceremony audit review and
devtools.check_integrity_ceremony all ship in PR 347. Close or narrow this once #347
merges; slice 6 waits on the owner (think-gzju).
