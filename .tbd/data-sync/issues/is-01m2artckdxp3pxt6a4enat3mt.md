---
type: is
id: is-01m2artckdxp3pxt6a4enat3mt
title: Read the raw-complete pre-normalization BC329 checkpoint
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2anzgc2aqn6vzx29ps3rpn2
  - type: blocks
    target: is-01m2aj2ewckram8ww4458w74hr
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T12:17:33.793Z
updated_at: 2026-09-12T16:11:31.564Z
closed_at: 2026-09-12T16:11:31.564Z
close_reason: Implemented, integrated, independently reviewed, and published on the clean PR 156 stack by f1e397cd. Their remaining follow-up risks are separately tracked under calibration, parent preflight, partial-direction integration, and admission beads; no BC329 scientific target ran.
resolution: null
duplicate_of: null
---
A process can terminate after execute_packet publishes the complete accepted raw minimum but before candidate normalization is bound into the receipt. The retained receipt is partial/unresolved with normalized null, yet load_result currently requires normalized bytes whenever raw minimum exceeds M/11 and rejects its own last atomic checkpoint. Admit normalized absence only as an unpublished downstream tail for non-complete, non-accepted states with no post-normalization route, after strict raw replay; likewise handle a candidate file written before receipt publication without treating it as evidence. Keep complete/accepted states strict and add injected checkpoint-gap readback controls.
