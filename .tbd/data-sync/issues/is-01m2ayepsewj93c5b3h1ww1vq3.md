---
type: is
id: is-01m2ayepsewj93c5b3h1ww1vq3
title: Use literal Git pathspecs for BC329 result-directory exclusions
kind: bug
status: closed
priority: 1
version: 6
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
updated_at: 2026-09-12T15:11:12.827Z
closed_at: 2026-09-12T15:11:12.826Z
close_reason: "Repair commit 1a5a8565 passed source-distinct reproduction at each stated boundary: literal Git pathspec and tracked-output overlap are fail closed; the post-Popen deadline uses recomputed remaining time and kills a late process group; real SIGTERM and launch-window SIGHUP kill and reap workers before signal redelivery. The 98-test focused suite, Ruff, BasedPyright, edit tier, and diff check passed. Adjacent findings remain separately blocked; no BC329 target ran."
resolution: null
duplicate_of: null
---
Independent review of c516a592 reproduced a clean-tree bypass: when the result directory is literally named *, source_manifest builds non-literal :(exclude,top) pathspecs and excludes unrelated untracked files. Replace every user-derived Git exclusion with literal pathspec semantics, reject any result directory that overlaps a path tracked at the bound HEAD, and add adversarial controls for metacharacter names, tracked deletion or replacement, untracked files outside the true result tree, scientific readback, and normal nested result directories. Re-run focused tests, Ruff, BasedPyright, formatting, and source-distinct review. No BC329 target may run before closure.

## Notes

Repair committed as 1a5a8565eb7d8a4ed5c8dfc1979a2d3af5c034fe. source_manifest now uses a top-level literal Git exclusion and rejects result-directory ancestor, equality, or descendant overlap with paths tracked at the frozen revision. Target-free controls cover normal and nested paths, a literal * directory, unrelated untracked state, tracked deletion or replacement, and scientific readback. Validation: 98 fixed-core tests passed in 11.40 s; repository Ruff and BasedPyright reported zero findings; packing-validate --edit passed in 55.66 s on the final tree. Keep open pending source-distinct review. BC329 was not registered or run.
