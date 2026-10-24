---
type: is
id: is-01m5nz4xsf7m33aj93e6nhyxgf
title: "Fix check_rung_figures: '√2/2' read as the fraction 2/2"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T03:26:54.767Z
updated_at: 2026-10-24T03:26:54.767Z
---
PR #750 review A8 (https://github.com/jlevy/squares/pull/750#issuecomment-6379115396): devtools/check_rung_figures.py reads "√2/2 = 2.707…" as the fraction 2/2 equals a decimal, because the lookbehind of `_FRACTION_EQUALS_DECIMAL` (packing/devtools/check_rung_figures.py:120) does not exclude `√`. PR #750 had to rewrite T-237's value as 2 + 1/√2 to pass, which is how Friedman writes it, but the next lane may have to rewrite a source's own form.

Fix: exclude `√` (and other operators that bind the numerator, such as `^`) in the lookbehind, with a test: a negative control first, "2 + √2/2 = 2.70710678" must not be read as 2/2, and "2/2 = 1.0" still must be.
