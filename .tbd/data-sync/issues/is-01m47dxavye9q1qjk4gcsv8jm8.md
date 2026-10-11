---
type: is
id: is-01m47dxavye9q1qjk4gcsv8jm8
title: "Decide the reported-lane witness at T-098's 48 counts: the known-best pose does not attain S' (EX-9)"
kind: task
status: open
priority: 3
version: 1
labels:
  - result-import
dependencies: []
created_at: 2026-10-06T01:40:36.349Z
updated_at: 2026-10-06T01:40:36.349Z
---
At the 48 counts of T-098 (Evan Daniel's exact optima, #375) each case record's
reported_upper_bound.value is the certificate's side S', but its `witnesses` list still
names W-known-best-nNNN, the finder's binary64 pose at the finder's larger printed side,
which does not attain S'. The atlas (devtools/build_known_best_atlas.py,
_frontier_with_witness) writes that witness into every count's reported lane, and the lane
kept the finder's pose as the pictured witness on purpose (pictured_source_key), so the
48 known-best witnesses were not rewritten. Each record's body says which pose the witness
is.

Raised as EX-9 by docs/project/reviews/review-2026-10-06-evand-exact-optima.md and judged
partly resolved by its fix check. Decide one of: register each certificate as a rational
witness and list it in the reported lane (the T-088 route at n = 69, 48 new witness
files), let the atlas list the known-best witness only where it attains the reported
value, or record that the reported lane's witness is the pictured pose by convention.
Non-blocking; nothing in the bound depends on it.
