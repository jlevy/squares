---
type: is
id: is-01m1pnq9tmkqbnfwwmbwpszv36
title: "PR #78: the n=12 bound reads four different values across the record"
kind: bug
status: open
priority: 1
version: 4
labels: []
dependencies: []
parent_id: null
created_at: 2026-09-04T16:58:38.292Z
updated_at: 2026-10-06T08:34:44.029Z
---
Re-checked against PR #78 at `719c2a17`. The register moved from `393/100` to `197/50` to `99/25` and the prose did not follow, so the current head states four values for one bound:

- `packing/frontier/results.yaml` and `SYNOPSIS.md:73`: `99/25 = 3.96`, the register, authoritative
- `packing/frontier/n-012.md:52` YAML: `99/25`, agrees
- `README.md:75`: `79/20 = 3.95`, one rung stale
- `SYNOPSIS.md:3685`: `79/20`, one rung stale
- `SYNOPSIS.md:2619`, the H-061 row: `393/100`, three rungs stale

`SYNOPSIS.md:258` carries `77/20` in the document-map row, but that is the review document's own title and is correct as a title.

The generated blocks track the register; the hand-written prose does not, which is the same class of drift `tests/test_results_headline.py` was built to catch for the synopsis block and does not cover for README prose or hypothesis rows.

## Notes

2026-10-06 bead review: the README instances are gone (origin/main README.md carries none of 79/20, 393/100, 197/50) and n = 12's verified bound is now 7943/2000 (T-095). One instance remains: the SYNOPSIS.md H-061 row still says the method was 'carried well past its own claim to 393/100 (T-017)' while T-017 stands at 99/25. Moved to the top level when its parent think-3od5 closed.
