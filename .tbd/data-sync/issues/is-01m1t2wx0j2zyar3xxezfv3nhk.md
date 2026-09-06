---
type: is
id: is-01m1t2wx0j2zyar3xxezfv3nhk
title: Seed the cutting driver from a certificate and pre-register a scalar 61/16 probe
kind: task
status: closed
priority: 1
version: 2
labels:
  - research
dependencies: []
parent_id: is-01m1t2sgqmantgyx59knjxqheg
created_at: 2026-09-06T00:46:36.561Z
updated_at: 2026-09-06T01:02:19.736Z
closed_at: 2026-09-06T01:02:19.736Z
close_reason: "Implemented on PR 89 in commit c0db25cf: devtools.freeze_cutting_primal (bridge with tests), run_fractional_cutting --seed-certificate/--seed-map with tests, and cases/n12_fractional_certificate/replay_independent.py with the evidence replay repointed and tested; agenda-025 pre-registers the scalar 61/16 probe for the coordinator to allocate or decline at T+0."
resolution: null
duplicate_of: null
---
No side between 3.81 and 3.82 has ever been attempted with the existing single-B theorem: the covering-values register holds n=11 reports only at 3.82 and 3.85. The retained 3.81 certificate carries 434547/40000 = 10.863675, 0.136 below eleven, and the 3.82 vertex-seeded restricted optimum is 11.055617, 0.056 above it; a straight interpolation puts the current instrument's wall near 3.817, so 61/16 = 3.8125 and 763/200 = 3.815 are plausibly reachable with no new theorem. Agenda-025 only reaches 61/16 through BC-234 after the adaptive theorem (BC-230) and verifier (BC-231). Add --seed-certificate/--seed-map to devtools.run_fractional_cutting so a fresh side can start from the 3.81 atoms plus the grid (warm starts only move upward), and record the scalar probe as a pre-registered first-block option in agenda-025 for the coordinator to allocate at T+0.
