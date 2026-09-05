---
type: is
id: is-01m1qdh5ez0pghg8m7x64ksje9
title: "Certificate page: every decimal says whether it is exact; rationals where the decimal misleads"
kind: bug
status: closed
priority: 2
version: 3
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1pnpwvpjydts81pffmp1nt7
created_at: 2026-09-04T23:54:43.038Z
updated_at: 2026-09-05T00:41:31.867Z
closed_at: 2026-09-05T00:26:32.929Z
close_reason: Commit 6b639c00, verified on the rendered page.
resolution: null
duplicate_of: null
---
Review feedback on PR #79. decimal() in the renderer rounds to a fixed number of places and does not say whether the result is exact: weights are over 200000 and need six digits, so 'between 0.00233 and 0.1814' at five places can be rounded; 3.788854 and 3.877084 approximate algebraic numbers and need the ellipsis everywhere they appear (number line included); angle readouts (2·atan t) need ≈; Figure 5 shows B at six digits when it is exact at seven, and its product is irrational. Rule: an exact terminating decimal is printed in full; otherwise the rational is printed (TeX fraction) with an approximate decimal marked ≈ or …; never an unmarked rounding.
