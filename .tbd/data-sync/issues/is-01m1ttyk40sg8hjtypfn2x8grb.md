---
type: is
id: is-01m1ttyk40sg8hjtypfn2x8grb
title: "PR 94: rendering the retained 19/5 certificate alone leaves unbound placeholders"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-06T07:46:57.791Z
updated_at: 2026-09-06T07:46:57.791Z
---
render_explainer.py:1993-1999 now requires headline slug in PINNED_SECONDS, which only has 381-100. For certificate-19-5.json alone, claimed=False skips claim_substitutions while introduction uses HEADLINE_N_ATOMS, HEADLINE_N_DIRECTIONS, HEADLINE_PINNED_RUNTIME, PINNED_VERIFIER_LINES outside CLAIM. markdown_source reproduces missing-placeholder refusal. Separate universal facts from optional timed-checker prose and test the single-certificate render.
