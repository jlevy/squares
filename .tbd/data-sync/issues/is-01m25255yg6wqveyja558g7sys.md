---
type: is
id: is-01m25255yg6wqveyja558g7sys
title: Handle exact zero-charge floor atoms without NumPy conversion overflow
kind: bug
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-overnight-three-blocks.md
delegate: a6_dual_replay_admission
labels: []
dependencies:
  - type: blocks
    target: is-01m23fkwbxxcyeknacny62nhhf
parent_id: is-01m23fkwbxxcyeknacny62nhhf
created_at: 2026-09-10T07:05:18.018Z
updated_at: 2026-09-10T07:39:04.229Z
---
Astra xhigh independently reproduced valid floor atoms with total multiplicity 1 and divisor 2, weight 2**63, or divisor 2**63 and weight 1: exact charge and budget are zero and existing parsing/headroom checks pass, but both event and interval readers raise OverflowError when converting NumPy scalars. Repair zero-contribution handling or explicit representation refusal consistently, preserve exact charge/budget semantics, add the concrete controls, and obtain correction review before prototype adoption. Candidate: /private/tmp/n11-floor-atom-prep/. This is a robustness defect with no false acceptance or target result demonstrated.

## Notes

Private Sol correction and independent Astra xhigh correction review PASS. Thirty controls passed, with additional exact unequal-net and extreme inert-atom controls. Root also applies the independently recommended test fixture middle half-tangent 1/5 instead of 1/4. Review: /private/tmp/n11-floor-atom-correction-review.md; candidate and correction report: /private/tmp/n11-floor-atom-prep/. Production adoption and integration remain pending on the post-merge branch; no scientific target ran.
