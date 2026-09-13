---
type: is
id: is-01m2b884a8xfyybgtpfr4rdwgv
title: Build and admit the source-distinct calibration receipt reader
kind: task
status: in_progress
priority: 1
version: 22
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Astra Max mathematical contract; Sol implementation
labels:
  - n11
  - calibration
  - review
dependencies:
  - type: blocks
    target: is-01m2b884n0ms50xp93q6aaps1g
  - type: blocks
    target: is-01m2appm2nx1m700ky98ytzv4z
parent_id: is-01m2appm2nx1m700ky98ytzv4z
child_order_hints:
  - is-01m2dz5hs247ey3ncymhvd0d05
  - is-01m2dz5j7vkkz99ssnz99c0rtc
  - is-01m2dz5jn4r6dyknxanbvcf5zb
  - is-01m2dz5k4wf297ycgbyerrmgjy
  - is-01m2dz5kk5hnnkhx8dqjxc7w1n
  - is-01m2dz5kzv8k9e1yq06017ngah
  - is-01m2e0e3jvze66t76m0p44a69z
  - is-01m2e19mwtk6gne1hxvwpap4bk
  - is-01m2e19ncq107301gs2q7rg8b6
  - is-01m2e19nqwvrfv91ak14mra1hj
  - is-01m2e19p36hn9ks8b2er46jw3m
  - is-01m2e23g7whep3daw5rnryg8by
created_at: 2026-09-12T16:47:12.711Z
updated_at: 2026-09-13T19:27:41.094Z
---
Run-sheet review F-4 and the existing think-1mma obligation. Add a maintained reader that is source-distinct from the calibration producer and checks every retained row and digest, independently derives the exact fixture geometry, normalization and dilation answers, reconstructs resources and route counts, enforces schema separation, and includes coherent-tampering controls. Bind both reader revision and execution revision; provide a literal per-profile command whose stdout, stderr and exit status are retained. Independently admit the reader before it is used to admit profiles. Do not run BC329.

## Notes

Independent Astra Max review at 212e0dfc refused six reader classes; 7e4d2487 repair and rereview accepted F1-F5 but refused F6/F7. First F6/F7 repair 95830f9e passed ordinary controls but exact-head Astra review found finite phase-sum overflow. Follow-up a5701e73 fixed that boundary. Independent exact-head Sol max review at a5701e73 ACCEPTED F6/F7 at the specific reader and source blobs: 23/23 full real-binder controls, 111 maintained reader tests passed with one intentional source-writing test excluded. Durable report docs/project/reviews/review-2026-09-13-n11-bc329-reader-f6f7-final.md. Later PR-head integration, running-reader source closure, run-sheet operational admission, and positive-profile readback remain; no positive profile/BC329 target.
