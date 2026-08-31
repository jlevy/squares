---
type: is
id: is-01m0sy3cf8rxrbcdq99vkrav4q
title: H-041 Lemma 6 replay must guard every squared-inequality sign premise
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/campaign/hypotheses/H-041-repaired-stromquist-point-set.md
labels: []
dependencies: []
parent_id: is-01m0srspsyjecv6bdatrx8r5bx
created_at: 2026-08-24T13:07:04.296Z
updated_at: 2026-08-24T13:18:00.432Z
closed_at: 2026-08-24T13:18:00.431Z
close_reason: The H-041 Lemma 6 replay now guards every domain and sign premise before squaring and retains the exact premise inventory. All 13 mutations plus exact generate/replay pass; D-157 records the correction.
resolution: null
duplicate_of: null
---
Verifier soundness gap found before the scientific run. The first draft checked exact squared polynomial gaps in the Lemma 6 reconstruction but did not executable-assert every domain and positivity premise that makes squaring implication-preserving. Acceptance: assert angle/tangent domains, positivity of both sides before each squaring, tangent-map monotonicity and positive exact gap coefficients; retain those facts in replayed evidence; add a defect record and focused checks.
