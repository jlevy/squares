---
type: is
id: is-01m1sdq9qd23r47dsa666qn2zb
title: test_known_best_composite_png_is_derived_from_current_svg fails only inside the full suite
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-05T18:36:32.877Z
updated_at: 2026-09-05T18:36:32.877Z
---
Reported by a sub-agent running packing-validate --fast: the PNG-vs-SVG receipt hash mismatches in the 2016-test suite but passes standalone and under -k composite_png, suggesting global-state leakage from an earlier test through the builder's memo. Confounder to rule out first: that run overlapped this session regenerating the atlas, which would produce the same symptom. Re-run on a settled tree before treating it as a real order dependence.
