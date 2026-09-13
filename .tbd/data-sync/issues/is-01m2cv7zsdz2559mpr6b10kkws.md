---
type: is
id: is-01m2cv7zsdz2559mpr6b10kkws
title: "PR #157 review MATH-01: direct token-count paint can overflow int64"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:25.452Z
updated_at: 2026-09-13T08:11:08.979Z
closed_at: 2026-09-13T08:11:08.979Z
close_reason: "Fixed: charge_grid_direct now picks its count-grid dtype from the atom's own token total (threshold.py:672-692) -- exact Python integers when token_count >= _INTEGER_MASS_LIMIT, int64 otherwise; the returned MassGrid stays int64 either way. Exact arithmetic chosen over a refusal because the direct route is the oracle the tests hold charge_grid to. Verified: two sites at 2**62 tokens each, k=2**63, core at (5/4,3/2) -> direct grid cell (2,1) was 0, now 1 (true charge 1); heavy grid matches the light 2-of-2 int64 grid cell for cell at two directions. Regression: test_the_direct_count_grid_oracle_does_not_wrap_on_heavy_token_counts. Reachability recorded for the disposition map: public via __all__ but no non-test caller in the repo, and no weighted record can reach the decision CLI (decide_threshold_certificate refuses them)."
resolution: null
duplicate_of: null
---
packing/src/sqpack/fractional/threshold.py:575-589 paints token counts into int64 without bounding them. Repro: two sites carrying 2**62 tokens each, threshold 2**63, weight 1. Charge headroom passes because absolute expansion mass is 1; a reachable core containing both sites then gets direct-grid charge 0 instead of 1. Fix: bound token-count intermediates separately before arithmetic, or use exact arithmetic; retain a compact overflow regression.
