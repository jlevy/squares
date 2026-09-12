---
type: is
id: is-01m2aj7paytrdj85x26njv0jrr
title: Bind the BC329 runtime and enforce a strict result schema
kind: bug
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2aj2ewckram8ww4458w74hr
  - type: blocks
    target: is-01m2aj7q4y8raaw35s0jq3ty2y
  - type: blocks
    target: is-01m2anzgc2aqn6vzx29ps3rpn2
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T10:22:29.714Z
updated_at: 2026-09-12T16:11:31.550Z
closed_at: 2026-09-12T16:11:31.550Z
close_reason: Implemented, integrated, independently reviewed, and published on the clean PR 156 stack by f1e397cd. Their remaining follow-up risks are separately tracked under calibration, parent preflight, partial-direction integration, and admission beads; no BC329 scientific target ran.
resolution: null
duplicate_of: null
---
Extend the source manifest beyond the local Python import closure to bind pyproject.toml, uv.lock, the project Python 3.14 interpreter identity/path, and relevant runtime package versions, including NumPy and strif. Reject dirty or mismatched runtime inputs. Require finite positive scientific, external, and grace durations; serialize strict JSON with allow_nan=false and reject nonstandard NaN/Infinity on read; tighten legal status/outcome/phase/error combinations. Put the raw minimum, published source blob/SHA/revision, and ratio-preserving normalization provenance in candidate.json so it remains traceable outside the result bundle. Add mutation controls for every bound field.
