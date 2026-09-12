---
type: is
id: is-01m2ayepsewj93c5b3h1ww1vq3
title: Use literal Git pathspecs for BC329 result-directory exclusions
kind: bug
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2as8hsq3d7dxy1z185zxeah
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
parent_id: is-01m2as8hsq3d7dxy1z185zxeah
created_at: 2026-09-12T13:56:02.468Z
updated_at: 2026-09-12T14:06:28.976Z
---
Independent review of c516a592 reproduced a clean-tree bypass: when the result directory is literally named *, source_manifest builds non-literal :(exclude,top) pathspecs and excludes unrelated untracked files. Replace every user-derived Git exclusion with literal pathspec semantics, reject any result directory that overlaps a path tracked at the bound HEAD, and add adversarial controls for metacharacter names, tracked deletion or replacement, untracked files outside the true result tree, scientific readback, and normal nested result directories. Re-run focused tests, Ruff, BasedPyright, formatting, and source-distinct review. No BC329 target may run before closure.
