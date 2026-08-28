---
type: is
id: is-01m12vwrn7p99ehaxxasqkh9c5
title: check_source_coverage never reparses Kingbird exact forms, so transcription misses are invisible
kind: bug
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T00:21:40.120Z
updated_at: 2026-08-28T01:26:19.010Z
---
exact_form, algebraic_degree and minimal_polynomial in frontier/n-NNN.md are hand-transcribed from resources/web/kingbird-squares-in-squares.html and never machine-reconciled against it. devtools/check_source_coverage.py:41-46 extracts only the decimal and the integer side form, so nothing can detect a missed radical.

This produced a live error: n=54. Kingbird prints s = 7 - (1/2)sqrt(2) + sqrt(1+sqrt(2)) at kingbird-squares-in-squares.md:292, but the frontier recorded exact_form: null. Verified independently: the closed form matches the witness side to its full 29 digits (diff 1.7e-30) and its minimal polynomial is 4s^4 - 112s^3 + 1164s^2 - 5304s + 8897, degree 4. Cause: n=54 is the ONLY n<=100 entry Kingbird renders with a multi-line begin{aligned} block rather than the single-line pattern the transcriber handled.

The miss reached a published figure: the composite badged n=54 'only known numerically'. Fixed now, counts moved 94/6 -> 95/5.

Done when check_source_coverage reparses the exact-form and degree lock annotations for every n and fails on divergence.
