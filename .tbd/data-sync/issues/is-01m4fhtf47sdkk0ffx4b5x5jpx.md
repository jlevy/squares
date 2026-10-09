---
type: is
id: is-01m4fhtf47sdkk0ffx4b5x5jpx
title: Unadopted better results render as superseded (T-128, T-130)
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
created_at: 2026-10-09T05:22:52.167Z
updated_at: 2026-10-09T05:22:52.167Z
---
render_recent_results.standing marks any result no case lane rests on as SUPERSEDED, so T-128 (#460) reads 'recorded, superseded by T-098, T-115, T-125 and T-127' and T-130 (#469) 'superseded by T-119 and T-125' although their reported sides are strictly smaller than the held bounds. Correct status should say reported/pending adoption. Fix at #460, the lowest layer where it manifests.
