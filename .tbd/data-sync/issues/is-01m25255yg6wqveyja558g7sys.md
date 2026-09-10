---
type: is
id: is-01m25255yg6wqveyja558g7sys
title: Handle exact zero-charge floor atoms without NumPy conversion overflow
kind: bug
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-overnight-three-blocks.md
delegate: a6_dual_replay_admission
labels: []
dependencies: []
parent_id: is-01m23fkwbxxcyeknacny62nhhf
created_at: 2026-09-10T07:05:18.018Z
updated_at: 2026-09-10T07:09:14.125Z
---
Astra xhigh independently reproduced valid floor atoms with total multiplicity 1 and divisor 2, weight 2**63, or divisor 2**63 and weight 1: exact charge and budget are zero and existing parsing/headroom checks pass, but both event and interval readers raise OverflowError when converting NumPy scalars. Repair zero-contribution handling or explicit representation refusal consistently, preserve exact charge/budget semantics, add the concrete controls, and obtain correction review before prototype adoption. Candidate: /private/tmp/n11-floor-atom-prep/. This is a robustness defect with no false acceptance or target result demonstrated.
