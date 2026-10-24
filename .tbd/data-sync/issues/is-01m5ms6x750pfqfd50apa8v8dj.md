---
type: is
id: is-01m5ms6x750pfqfd50apa8v8dj
title: "Stage 4 mathematical review of T-238: Amund Kristiansen's s(303) <= 17.909762327476 (#755)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: c-review-t238-math
labels:
  - result-import
  - validation
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T16:23:53.828Z
updated_at: 2026-10-24T01:47:12.332Z
started_at: 2026-10-23T16:23:55.732Z
---

## Notes

Stage 4 mathematical review of T-238 (#755), lane c-review-t238-math, 23 October 2026. Review written; outputs in this lane's scratch, for the records lane (c-lane-755-1023) to commit on claude/intake-2026-10-23-755. This lane committed, pushed and posted nothing.

Verdict: accepted, finite feasibility only. s(303) <= S = 223872029093440709529093216833/12500000000000000000000000000 = 17.90976232747525676232745734664 (17.909762327476 at 12 places, rounded up). Least wall clearance 6.020000000001029e-13 (square 3, top); least pair gap 60250000000010249/(5*10^28) = 1.205e-12 at six pairs; none touching. 9.889799071009889799071e-6 below T-230; below every report at 303 (Kingbird included) and every bound at 304-320.

Checker: review_t238_check.py (SHA-256 ba967921...8480), clean room, two routes (Z integers, separating axes, every pair; E Fraction, discs plus edge/vertex tests with exact distances). Both accept; 116/116 shared numbers equal with both maintained routes, the records lane's receipt and its derived fact; 21 controls (sharp at 1e-30, 3 walls and 5 pairs, gross, mirror, reader) as expected on all four deciders; self-test 15 + 13 + 2,000 pairs; second run identical.

Findings (none blocking): RF-1 minor, the issue's verify_cert.py wall clearance 8.2e-13 is not this file's (6.020e-13); RF-2 the long decimal is the binary64 print; RF-3 the certificate is dilate_cert.py's output from the input (side and centres exact, 267 tangents, 36 one ulp of tan apart); RF-4 T-230's arrangement rearranged (one to one, row order, 12 beyond 0.1, 5 newly tilted, 47 contacts changed); RF-5 significance S2, not draft S3; RF-6 not rigid (5 free squares, >= 4.67e-3); RF-7 maintained replay shared-components; RF-8 custody (no licence); RF-9 retain and register programs. Three questions for the author.

Rungs once entered: V3/C3, confirmed, independently re-implemented (Claude, a system family the producer also used). Then adopt at 303 and regularize; T-230 stays as history.

Outputs (scratchpad/review-t238/): docs/project/reviews/review-2026-10-23-amundsk-n303.md; packing/resources/web/amundsk-n303-2026-10-23/review/review-2026-10-23/ (README, programs/, outputs/); record-changes.md (evidence, verifiers, results, document-map, significance, News note, reply draft).

2026-10-24 c-land-757-1024 (coordinator coord-intake-1023): the entry this review covers was renumbered from T-238 to T-239 on PR #757, before it merged, when the owner gave T-237 and T-238 to #750 (think-4o9c). Every "T-238" in this bead's title and notes above means T-239. The review document and its packet README each gained one dated sentence naming the old id (commit 045497b6a); the review's programs keep "T-238" in their docstrings and `t238` in their names, and the receipts are untouched, since outputs/program-digests.sha256 binds them. The register entry's notes record the renumbering.
