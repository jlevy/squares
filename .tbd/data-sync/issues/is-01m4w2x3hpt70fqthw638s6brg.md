---
type: is
id: is-01m4w2x3hpt70fqthw638s6brg
title: Carry credited people as structured data on each regularization generator
kind: task
status: open
priority: 4
version: 1
labels: []
dependencies: []
created_at: 2026-10-14T02:12:17.589Z
updated_at: 2026-10-14T02:12:17.589Z
---
Review A of PR #591, suggestion A9: the posters shorten each regularization credit to surnames with _print_surnames in packing/devtools/build_known_best_atlas.py, which recovers people from prose by matching credit-attributions.json's multi-word name_aliases. A future generator credit naming someone with no alias would print in full, and the test that only 'Diagram by Joshua Levy' appears in full can only see aliased names. Consider a structured field on each generator in the regularized index (who is credited, with a print name), read by the poster credit and its test instead of the prose. Done when the poster credit and its test read the structured field and an unaliased name cannot print in full unnoticed.
