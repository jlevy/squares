---
type: is
id: is-01m0wz3nx8ggn5gs6zqkdrhtxs
title: SYNOPSIS registry rounds column drifted from the ledger with no check
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m0wy9s97fwegw5kqrge2p8sy
created_at: 2026-08-25T17:22:25.831Z
updated_at: 2026-08-25T17:49:31.483Z
closed_at: 2026-08-25T17:49:31.483Z
close_reason: Fixed on the PR 33 branch; see review-2026-08-25-tutorial-soundness-iteration-2.md and defects D-320..D-328. Full gate green.
resolution: null
duplicate_of: null
---
The hypothesis-registry table's Rounds/Effort columns were hand-maintained under no consistent rule: H-023 lagged exp-039 (5 vs 6 rounds), H-002 showed 4 vs ledger 5, H-021 showed 0 vs ledger 14. check_synopsis compared only the status column. Fixed: rows aligned to the ledger's per-hypothesis totals, the counting rule stated in the section intro, check_synopsis extended to compare the rounds column row by row, and a negative control added rehearsing one stale row.
