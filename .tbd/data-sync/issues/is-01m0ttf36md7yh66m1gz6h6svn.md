---
type: is
id: is-01m0ttf36md7yh66m1gz6h6svn
title: Migrate packing uniformly to Python 3.14 only
kind: task
status: open
priority: 1
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
  - python
dependencies:
  - type: blocks
    target: is-01m0ttfczkhxs9fqa6kwphy8rx
  - type: blocks
    target: is-01m0ttfx53tjv841cn2v2anyf2
  - type: blocks
    target: is-01m0ttgkhcyks8na3prg20kk8c
  - type: blocks
    target: is-01m0tth2dgvwnagwh2975ac6k3
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T21:22:48.130Z
updated_at: 2026-08-24T21:23:52.879Z
---
Make Python 3.14 the sole supported runtime across the packing project before later refactors rely on its language and standard-library behavior. Align project.requires-python, the uv lock and environment, Ruff target, BasedPyright target, CI, executable commands, scripts, and documentation; remove compatibility branches for Python 3.11-3.13 unless a named external consumer requires one. Acceptance: metadata expresses one uniform policy, all Python checks and the complete packing gate run under 3.14, and development.md documents the supported runtime and setup.
