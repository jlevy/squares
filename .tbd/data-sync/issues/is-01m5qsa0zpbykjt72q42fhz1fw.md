---
type: is
id: is-01m5qsa0zpbykjt72q42fhz1fw
title: "Import #797: Kevin Fang's c*(k) < 4√(2k)+1 for every k ≥ 6 (squarepack-certs theorem-a at b1b3f6b)"
kind: task
status: in_progress
priority: 2
version: 2
delegate: c-triage-797-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T20:23:19.286Z
updated_at: 2026-10-24T20:24:12.105Z
started_at: 2026-10-24T20:24:12.105Z
---
New 2026-10-24 issue https://github.com/jlevy/squares/issues/797 (TheSnakeFang, 18:52:48Z): for every k >= 6, k^2 - ceil(sqrt(32k)) - 1 unit squares fit in a square of side < k, so c*(k) < 4 sqrt(2k) + 1. Ryu's L packing (Theorem 1.3) with filled band ends, b the odd integer nearest sqrt(2k); a 5-page note. Source TheSnakeFang/squarepack-certs@b1b3f6b theorem-a/ (note PDF+TeX, lband.py exact construction, windowed_check.py, certificates k=6..40 and 101, SHA-256 for k=300 and 600 with regenerate.sh). The repository head db1ed62 (3 commits past the last read) adds note v0.2 crediting Evan Daniel's earlier bound (doi:10.5281/zenodo.23624565): read for priority and credit. Bears on the deficiency rows (Ryu's Theorems 1.2-1.4, T-163). Stage 0 owner; stage 1 triage is read-only first. Source claims are unverified.
