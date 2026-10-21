---
type: is
id: is-01m5b9b3wxyv0ajw2346p3vq65
title: "Simplify _pair_best_gap's loop and share the composite-number filter (PR #691 B5/B6)"
kind: task
status: open
priority: 4
version: 1
labels: []
dependencies: []
created_at: 2026-10-19T23:53:24.636Z
updated_at: 2026-10-19T23:53:24.636Z
---
Preference suggestions from PR #691 Review B. B5: expected_composite (build_known_best_atlas.py ~:4046) restates _cards' filter (~:4030) and measure_release_assets._atlas_composites (:108) has a third copy; one helper returning a composite's numbers in corpus order. B6: _pair_best_gap (sqpack/witness.py ~:445-474) range(4)/index<2 dispatch and packed tuple args; two loops over zip(axes, shadows) and a small NamedTuple would read like the definition. Any change to _pair_best_gap must keep Review A's equivalence (test_margin_summary_matches_the_exhaustive_definition) and get a correctness re-review.
