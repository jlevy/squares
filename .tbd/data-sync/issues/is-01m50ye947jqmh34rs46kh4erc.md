---
type: is
id: is-01m50ye947jqmh34rs46kh4erc
title: "PR #616 A8 (https://github.com/jlevy/squares/pull/616#issuecomment-6189327252): the beyond-horizon measurements live in a packet's review/ directory with no tier check"
kind: bug
status: open
priority: 2
version: 3
delegate: ecstatic-edison-address-627
labels: []
dependencies: []
parent_id: is-01m50gnwbxd5kxbynyx9nd162p
hold: null
hold_until: null
created_at: 2026-10-15T23:30:29.639Z
updated_at: 2026-10-15T23:58:26.873Z
started_at: 2026-10-15T23:30:53.812Z
---
Nit. #616 review A (https://github.com/jlevy/squares/pull/616#issuecomment-6189327252), carried by PR #627 B1. compare_beyond_horizon.py and goebel_beyond_horizon.py run by hand (OR-1). Fix: a bead to move them into devtools with --check.

## Notes

Deferred from #616's review A (A8), carried by PR #627 B1. compare_beyond_horizon.py and goebel_beyond_horizon.py in packing/resources/web/couzo-verified-bounds-2026-10-14/review/ decide which 487b058 rows are recorded and which 42 are left out, run by hand, and no tier re-checks their outputs (OR-1). Move them into devtools with a --check (the Goebel half needs no source bytes). Same class as think-z161 (#612 A12, compare_lineage.py). Waits on a tooling slice; not this PR's scope.
