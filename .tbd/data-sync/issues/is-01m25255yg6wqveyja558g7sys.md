---
type: is
id: is-01m25255yg6wqveyja558g7sys
title: Handle exact zero-charge floor atoms without NumPy conversion overflow
kind: bug
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: a6_dual_replay_admission
labels: []
dependencies:
  - type: blocks
    target: is-01m23fkwbxxcyeknacny62nhhf
parent_id: is-01m23fkwbxxcyeknacny62nhhf
created_at: 2026-09-10T07:05:18.018Z
updated_at: 2026-10-06T08:38:40.818Z
closed_at: 2026-10-06T08:38:40.818Z
close_reason: "Superseded by T-060: s(11) equals Trump's side, registered 2026-09-29 at V3/C3 and on main since PR #246 (merged 2026-09-30). This n = 11 lower-bound certificate work has no target left; the owner's 2026-09-14 strategy reset had already paused it, and the post-optimality plan (plan-2026-10-01) uses n = 11 only as a control. The candidate lived only in /private/tmp/n11-floor-atom-prep and was never adopted on main."
resolution: canceled
duplicate_of: null
---
Astra xhigh independently reproduced valid floor atoms with total multiplicity 1 and divisor 2, weight 2**63, or divisor 2**63 and weight 1: exact charge and budget are zero and existing parsing/headroom checks pass, but both event and interval readers raise OverflowError when converting NumPy scalars. Repair zero-contribution handling or explicit representation refusal consistently, preserve exact charge/budget semantics, add the concrete controls, and obtain correction review before prototype adoption. Candidate: /private/tmp/n11-floor-atom-prep/. This is a robustness defect with no false acceptance or target result demonstrated.

## Notes

Private Sol correction and independent Astra xhigh correction review PASS. Thirty controls passed, with additional exact unequal-net and extreme inert-atom controls. Root also applies the independently recommended test fixture middle half-tangent 1/5 instead of 1/4. Review: /private/tmp/n11-floor-atom-correction-review.md; candidate and correction report: /private/tmp/n11-floor-atom-prep/. Production adoption and integration remain pending on the post-merge branch; no scientific target ran.
