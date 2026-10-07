---
type: is
id: is-01m40534rntkem2mt8qgh88fe2
title: "Remove environment sealing: retained results bound to Git revision, not to pyproject/uv.lock; determinism by small tests, never by re-running (lane E1)"
kind: task
status: open
priority: 0
version: 2
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-03T05:51:48.500Z
updated_at: 2026-10-05T05:37:35.846Z
---
Owner direction 2026-10-03: 'It should never cost hours of verification time for
internal bookkeeping … we are not validating across a trust boundary.
We’re worrying about correctness.'
and ‘We need determinism for sure, but determinism should not cost rerunning code.’
Trigger: adding gmpy2 failed audit_kleddamag_n11_native (PROOF_INPUTS freezes
packing/pyproject.toml and uv.lock to blobs at c183cc9a, so any dependency change
demanded re-running the 6,197 s n11 native run).
Same pattern in fixed_core_packet, calibrate/verify/read fixed-core calibration tools.
E1 inventories and removes these gates (drift becomes informational), keeps genuine
trust-boundary checks, keeps determinism as fast small-instance tests, records the rule
in development.md. Then gmpy2 returns as a plain dependency (F2 fixing mpmath
gmpy-backend leak sites such as promote/interval.py Decimal(mpz)).

## Notes

2026-10-05 (PR 347 status survey).
The OR-16 amendment, the integrity-ceremony audit review and
devtools.check_integrity_ceremony all ship in PR 347. Close or narrow this once #347
merges; slice 6 waits on the owner (think-gzju).
