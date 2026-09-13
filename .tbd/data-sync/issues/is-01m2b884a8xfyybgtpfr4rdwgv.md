---
type: is
id: is-01m2b884a8xfyybgtpfr4rdwgv
title: Build and admit the source-distinct calibration receipt reader
kind: task
status: in_progress
priority: 1
version: 6
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
created_at: 2026-09-12T16:47:12.711Z
updated_at: 2026-09-13T17:45:44.551Z
---
Run-sheet review F-4 and the existing think-1mma obligation. Add a maintained reader that is source-distinct from the calibration producer and checks every retained row and digest, independently derives the exact fixture geometry, normalization and dilation answers, reconstructs resources and route counts, enforces schema separation, and includes coherent-tampering controls. Bind both reader revision and execution revision; provide a literal per-profile command whose stdout, stderr and exit status are retained. Independently admit the reader before it is used to admit profiles. Do not run BC329.

## Notes

Source-distinct reader merged into local PR156 at 212e0dfc from 2753e53a. Integrated 250 target-free tests passed; Ruff check/format and BasedPyright 0. Astra Max exact-head review is active and identified manifest-closure completeness and strict JSON type/coercion concerns to reproduce and repair before admission. No profile or BC329 ran.
