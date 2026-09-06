---
type: is
id: is-01m1ttyk40sg8hjtypfn2x8grb
title: "PR 94: rendering the retained 19/5 certificate alone leaves unbound placeholders"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
created_at: 2026-09-06T07:46:57.791Z
updated_at: 2026-09-06T08:05:14.876Z
closed_at: 2026-09-06T08:05:14.875Z
close_reason: Fixed in PR 94 commit 9c82dc2a. All required CI checks passed in run 34020582886; page build passed in 34020582877. Focused regression tests, final 31-step records gate, both revised negative controls, and n11/n17 package controls passed.
resolution: null
duplicate_of: null
---
render_explainer.py:1993-1999 now requires headline slug in PINNED_SECONDS, which only has 381-100. For certificate-19-5.json alone, claimed=False skips claim_substitutions while introduction uses HEADLINE_N_ATOMS, HEADLINE_N_DIRECTIONS, HEADLINE_PINNED_RUNTIME, PINNED_VERIFIER_LINES outside CLAIM. markdown_source reproduces missing-placeholder refusal. Separate universal facts from optional timed-checker prose and test the single-certificate render.
