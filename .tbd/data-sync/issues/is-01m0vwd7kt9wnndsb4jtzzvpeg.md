---
type: is
id: is-01m0vwd7kt9wnndsb4jtzzvpeg
title: Fix downward-rounded certified Trump bound in SVG captions
kind: bug
status: open
priority: 0
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels:
  - packing
  - soundness
dependencies: []
parent_id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
created_at: 2026-08-25T07:15:58.713Z
updated_at: 2026-08-25T07:15:58.713Z
---
PR 25 formats Trump's exact side 3.877083590022814... to 3.87708359 and prints it after <=, which asserts a smaller false upper bound. Preserve the evidence label but use approximation semantics or rigorously outward rounding; add a regression that rejects inward rounding. Found during pre-session-010 upstream review; PR 25 must not land until fixed.
