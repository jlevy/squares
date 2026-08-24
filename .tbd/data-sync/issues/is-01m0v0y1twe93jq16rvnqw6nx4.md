---
type: is
id: is-01m0v0y1twe93jq16rvnqw6nx4
title: Define rendering model and exact numeric projection
kind: task
status: open
priority: 1
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels:
  - packing
  - visualization
  - tdd
dependencies:
  - type: blocks
    target: is-01m0v0yf3ffe0tg78dss3cdx77
  - type: blocks
    target: is-01m0v0yfcmzrkj40qhph74gk1n
  - type: blocks
    target: is-01m0v0ypqc2shhf313140pqsmk
parent_id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
created_at: 2026-08-24T23:15:49.724Z
updated_at: 2026-08-24T23:16:11.115Z
---
Files: sqpack/render/__init__.py, model.py, numbers.py, and the first model/number sections of tools/check_svg_rendering.py. Implement the stable enums and frozen dataclasses, source-preserving scalar constructors, Decimal projection, visible-label formatting, and validation named in the spec. Work test-first through the repository checker: reject non-finite or ambiguous scalars, duplicate or unstable square IDs, invalid evidence combinations, negative zero, locale-sensitive formatting, and precision drift. Done when focused Ruff/BasedPyright checks pass and fresh-process number/model controls are green without a new runtime dependency.
