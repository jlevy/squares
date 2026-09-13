---
type: is
id: is-01m2cv82aj4pazmtwwjkwb9vyc
title: "PR #157 review READ-01 (High): orbit admission can accept a violated weighted row"
kind: bug
status: closed
priority: 1
version: 2
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:28.050Z
updated_at: 2026-09-13T08:19:31.542Z
closed_at: 2026-09-13T08:19:31.541Z
close_reason: "Fixed: admit_threshold_atom_orbits.py:256-262 (_orbit_report) now sums multiplicity * cached_membership over zip(image.points, image.multiplicities, strict=True); the module docstring's inequality was also a site inequality (floor(|S|/k), |P and gS|) and now reads in tokens. Review repro verified EXACTLY -- family weight 3/2, unit square centred (1,1) in side-two container, orbit of (1,1)x2 tokens and (1,17/10)x1, k=2, 4 images: BEFORE admitted=True charge 0 budget 4 image_charges ['0','0','0','0']; exact weighted charge 6; AFTER admitted=False charge 6 budget 4 image_charges ['3/2'x4] violated=True. Controls: negative test_a_heavy_site_is_charged_once_per_token_and_not_once_per_site (the repro, refused) and positive test_a_weighted_row_within_its_token_budget_still_admits (same orbit at weight 1: charge 4, budget 4, slack 0, admitted) -- the positive control asserts the CHARGE NUMBER, not just admitted, because the buggy reader also said admitted, at charge 0. False ROW admission only: ceiling_proof.checked stays False, so no global bound rested on it. Retained 2566-atom A6 input still parses and admits unchanged."
resolution: null
duplicate_of: null
---
packing/devtools/admit_threshold_atom_orbits.py:216 sums cached memberships once per site while its budget counts tokens. Repro: unit square centered (1,1) in side-two container, family weight 3/2, four-image orbit of sites (1,1),(1,17/10) with counts (2,1), threshold 2 -> returns admitted=True, charge 0, budget 4; exact weighted charge is 6. Fix: sum multiplicity times cached membership; retain a heavy-site-only negative control plus a valid positive control. This is false ROW admission; K0-K3 remains unchecked so it is not a demonstrated false global bound.
