---
type: is
id: is-01m50p364zjg93qw5e3vt6ggvd
title: Retain test selection reasons and measure unrelated selections
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
created_at: 2026-10-15T21:04:37.534Z
updated_at: 2026-10-15T21:04:37.534Z
---
Astra read-only analysis of PR629 final B1 delta found an exact two-file changed-path receipt, yet step selection uses _RENDERER_HUB=packing/devtools/* and reaches renderer/exact/drawing checks. Behavioral selection includes whole modules merely for glob or dynamic-import evidence, including temporary asset and PDF diagnostic globs. select_tests computes reasons then discards them. First retain each selected module reason in the existing receipt and join it with completed per-test costs; preserve memberships and unknown-input fallbacks. Then select one measured family to narrow with positive/refusal controls. Do not claim per-family elapsed attribution from this static evidence. This continues the existing plan selection-reasons requirement; think-6izq retained these conservative glob cases intentionally. PR629 diagnostics stay frozen and separate.
