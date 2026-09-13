---
type: is
id: is-01m2ece63feqsj8psvetpk477b
title: Make the BC303 T2 adversarial reference complete over feasible strata
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - bc303
dependencies:
  - type: blocks
    target: is-01m2e9etf82fvg7xz4xg6dn4zc
parent_id: is-01m2e6e4j1ee5nre22gp7fyyrc
created_at: 2026-09-13T21:58:08.750Z
updated_at: 2026-09-13T22:17:06.648Z
closed_at: 2026-09-13T22:17:06.648Z
close_reason: Repairs committed at 0f20fdcdd5bac7e0734b29cd0b0efef4ffea3699 with 20 target-free focused controls passing and edit tier 45/74 selected steps passing; fresh independent admission think-ncn8 remains open before exp-158
resolution: null
duplicate_of: null
---
Admission review think-ncn8 found a false result in packing/tests/test_bc303_t2_charge_sweep.py:52-63. direct_all_strata_minima silently skips a feasible open cell when its 64 dyadic witness attempts do not enter a narrow wall-feasible sliver; its event/midpoint samples do not repair that loss. Target-free regression /private/tmp/test_bc303_t2_charge_reader_admission_2026_09_13.py constructs rational synthetic ray (4/5,3/5), source lower tangent 3/4 (extent 7/10), a cell with maximum clearance 7/10 + 2^-100, and two unit-weight synthetic atoms. The optimized sweep and an explicit rational centre certify minimum 0, but the reference returns 1. Replace finite search-as-absence with complete exact stratum feasibility plus guaranteed rational witness construction, or fail explicitly on unresolved construction. Include edges/vertices and rational equality with each endpoint inclusion policy. Promote the retained regression. Also add a genuine interior coincident end/start fixture: existing cases have no interior negative x events, and all their ends at x=h are never processed. Retained local control passes with C=20, S=24, closed event=31 using synthetic atoms. No target source charges were evaluated; fresh independent reader admission is required before exp-158.

## Notes

The direct reference enumerates point/open-interval products and decides wall feasibility exactly, including equality and endpoint attainment. Feasible representatives are constructed or raise an explicit unresolved error after the bound; no stratum is silently skipped. Maintained target-free controls cover 2^-100 narrow feasibility, 2^-300 unresolved refusal, rational wall equality, and a genuine interior coincident x-end/start with C=20, S=24, closed event=31. Clean local repair commit 0f20fdcdd5bac7e0734b29cd0b0efef4ffea3699 on codex/bc303-t2-charge-reader-repair (base cdf854e240aa0068b0a4554f6c20d09385aa02d8). Focused geometry, charge, and original target-free admission controls: 20 passed. Ruff and BasedPyright: zero findings. Documentation check passes. packing-validate --edit: 45/74 selected steps passed. Historical REFUSE and original failing log retained in repo. No BC293 target charge, H-160/exp-158 edit, target invocation, push, or PR. Fresh independent admission of this exact clean head remains pending.
