---
type: is
id: is-01m1sdq9qd23r47dsa666qn2zb
title: test_known_best_composite_png_is_derived_from_current_svg fails only inside the full suite
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T18:36:32.877Z
updated_at: 2026-09-05T20:46:54.804Z
closed_at: 2026-09-05T20:46:54.804Z
close_reason: "Not reproducible on a settled tree; the confounder was the cause. Reproduction attempted three ways: the receipt test alone (2 passed), the test file together with every other file that imports the builder or clears its caches in one process (51 passed, 150s), and main's complete integration surface on 5ebeb62a, which runs the whole 2000-test behavioural suite alongside the known-best atlas step and reported ALL CHECKS PASSED. The original observation came from a --fast run that overlapped this session regenerating the atlas at 18:09-18:11, which changes the committed SVG under a running test and produces exactly the reported symptom: a receipt hash mismatch that passes standalone. No global-state leakage exists to fix."
resolution: null
duplicate_of: null
---
Reported by a sub-agent running packing-validate --fast: the PNG-vs-SVG receipt hash mismatches in the 2016-test suite but passes standalone and under -k composite_png, suggesting global-state leakage from an earlier test through the builder's memo. Confounder to rule out first: that run overlapped this session regenerating the atlas, which would produce the same symptom. Re-run on a settled tree before treating it as a real order dependence.
