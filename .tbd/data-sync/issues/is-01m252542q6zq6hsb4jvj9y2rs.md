---
type: is
id: is-01m252542q6zq6hsb4jvj9y2rs
title: Make the private floor certificate serializer and loader round-trip
kind: bug
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-overnight-three-blocks.md
delegate: a6_dual_replay_admission
labels: []
dependencies: []
parent_id: is-01m23fkwbxxcyeknacny62nhhf
created_at: 2026-09-10T07:05:16.115Z
updated_at: 2026-09-10T07:09:14.115Z
---
Astra xhigh independently reproduced that FloorCertificate.to_record emits half_tangents while the private floor loader requires direction_steps and angle_limit, so the reader rejects its own serialized output with missing direction_steps. Repair the private representation/strict loader contract with a meaningful exact round-trip control and independent correction review before adoption. Preserve ordinary threshold semantics and admitted direction requirements. Candidate: /private/tmp/n11-floor-atom-prep/. Controls: /private/tmp/n11-floor-atom-independent-controls.py and .txt. This affects an unadopted prototype; no false acceptance or scientific result was demonstrated.
