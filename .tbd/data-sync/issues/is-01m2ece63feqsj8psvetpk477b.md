---
type: is
id: is-01m2ece63feqsj8psvetpk477b
title: Make the BC303 T2 adversarial reference complete over feasible strata
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - bc303
dependencies:
  - type: blocks
    target: is-01m2e9etf82fvg7xz4xg6dn4zc
parent_id: is-01m2e6e4j1ee5nre22gp7fyyrc
created_at: 2026-09-13T21:58:08.750Z
updated_at: 2026-09-13T22:02:16.966Z
---
Admission review think-ncn8 found a false result in packing/tests/test_bc303_t2_charge_sweep.py:52-63. direct_all_strata_minima silently skips a feasible open cell when its 64 dyadic witness attempts do not enter a narrow wall-feasible sliver; its event/midpoint samples do not repair that loss. Target-free regression /private/tmp/test_bc303_t2_charge_reader_admission_2026_09_13.py constructs rational synthetic ray (4/5,3/5), source lower tangent 3/4 (extent 7/10), a cell with maximum clearance 7/10 + 2^-100, and two unit-weight synthetic atoms. The optimized sweep and an explicit rational centre certify minimum 0, but the reference returns 1. Replace finite search-as-absence with complete exact stratum feasibility plus guaranteed rational witness construction, or fail explicitly on unresolved construction. Include edges/vertices and rational equality with each endpoint inclusion policy. Promote the retained regression. Also add a genuine interior coincident end/start fixture: existing cases have no interior negative x events, and all their ends at x=h are never processed. Retained local control passes with C=20, S=24, closed event=31 using synthetic atoms. No target source charges were evaluated; fresh independent reader admission is required before exp-158.
