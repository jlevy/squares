---
type: is
id: is-01m46g4z163zz1r4edv4er01ns
title: "Import squarepacker #363: s(12) >= 7943/2000 (v1.1 at 98ffe37/7a96bec), replay and review to the verified lane"
kind: task
status: closed
priority: 1
version: 7
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m46g4yac7ewc22drc7twjhy5
hold: null
hold_until: null
created_at: 2026-10-05T17:00:29.093Z
updated_at: 2026-10-06T02:41:30.796Z
started_at: 2026-10-05T17:06:28.130Z
closed_at: 2026-10-06T02:41:30.792Z
close_reason: Done in jlevy/squares#369 (merged 34e87a86b); verdict replies posted 2026-10-06
resolution: null
duplicate_of: null
---

## Notes

2026-10-05 17:30Z, lane A (think-3kd9), stage 1-3 done on branch claude/ecstatic-pascal-pothtx-s12.

Claim map (#363, issue body; no comments): one claim, s(12) >= 7943/2000 = 3.9715, certificate
s12_lower_3.9715.txt (SHA-256 e2f326b2...), squarepacker/s12-lower-bound v1.1 (98ffe37 adds it,
7a96bec = tag v1.1 adds .zenodo.json). New entry, provisional T-095 (a later release than T-078's).
Notes, not claims: "why it stops near here" (560/141 sigma_0, LP 12.0052 at 3.97155) and the
#309 clarification (31360/7900 rejection is a net artefact at the reported pose); neither changes T-078.

Retained: packing/resources/web/squarepacker-s12-lower-bound-2026-10-05/ at 7a96bec (commit 3ae63093a),
devtools.audit_s12_v11_certificate (21 exact checks PASS), native case s12-v11 at N = 96000.
Registered: T-095 V0/C0 draft S3 (commit 037f78f15), E-n012-squarepacker-7943-2000-report.

Stage 4 plan (2 threads, nice 10): Daniel's verify (7d6f46d, overflow checks) at N = 96000
(running since 17:09Z), native parent-core all 39,765 rows (pilot 0.4 s/row, ~4.4 CPU-h),
indep_check N = 96000 (+192000), controls on all three, separately prompted review (claude -p,
running since 17:21Z in /home/user/squares-lanes/s12-review).

2026-10-05 18:30Z, lane A (think-3kd9), stage 4 in progress.

- Daniel's verify (7d6f46d blobs, overflow checks, binary 60279b2c) at N = 96000: VERIFIED,
  least 10000050/10^7 at k = 0, every line = source log; 4,671 s wall, 3,439 CPU-s (commit bb2bd87d5).
- Controls: verify single bins 0/30000 and native rows 0/30000 refuse both (receipts committed).
- Review: separately prompted (claude -p --agent tbd-strong --model claude-opus-5-5), stored byte for
  byte at docs/project/reviews/review-2026-10-05-s12-v11-certificate.md (commit 075ac4ad3); no blocking
  finding; it computed nothing (tool permissions refused execution, its F1). T-095 at V0/C1.
- Native parent-core --case s12-v11 --all --workers 2 started 18:27Z at 3ddd47d3a (pid 16828); at the
  current load ~1.8 rows/s, about 6 h wall, ~5 CPU-h. indep_check N = 96000/192000 and its two
  controls follow it (2-thread cap). The verified-lane move waits for the native decision.

2026-10-05 23:55Z, lane A (think-3kd9), stage 4 exit committed (547cae278; pin f7f424e21).
- Native parent-core --case s12-v11 --all --workers 2 at 3ddd47d3: PASS_COMPLETE, 39,765/39,765 rows,
  340,090,115 boxes, 0 stalled/exhausted/refuted; 16,344 s wall, 12,980 CPU-s.
- indep_check N = 96000 and 192000: VERIFIED, least 10000050/10^7, outputs = source logs (305, 608 CPU-s);
  controls refused (9999850, 6737611), outputs = source's.
- Zenodo 10.5281/zenodo.23157015 retained (record, files list, per-file digests): its zip's 68 files equal
  the pinned tree byte for byte (cbee0a83a).
- T-095 at V3/C3, S3 kept by the review; T-079 superseded, true as stated; n = 12 verified lower
  bound 7943/2000. Review F1 (no computation) in notes and next_rung.
- Open: V4/C4 needs a second distinct review (ideally one that executes its own exact checks) and a
  human oversight record; replies are lane E's.
