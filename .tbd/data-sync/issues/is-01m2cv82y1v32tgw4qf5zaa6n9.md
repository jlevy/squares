---
type: is
id: is-01m2cv82y1v32tgw4qf5zaa6n9
title: "PR #157 review READ-02 (High): additive weighted record lets older readers erase counts"
kind: bug
status: open
priority: 1
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:28.673Z
updated_at: 2026-09-13T07:38:28.673Z
---
packing/src/sqpack/fractional/threshold.py:259-271 preserves all old required fields and only adds keys, so the actual base revision decoder silently returns the lighter atom. packing/cases/n11_threshold_certificate/verify_claim.py:179-201 also ignores the new fields. Fix per the review repair format: weighted atoms become structurally incompatible with the legacy points shape. Preserve all-ones legacy output; retain explicit refusals at current admission/publication readers; test the historical decoding shape and the current standalone parser.
