---
type: is
id: is-01m4fkxqcgp6xcf3e98azvvqj7
title: Add a near-boundary shrink control to the evand arrangement kernel
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
created_at: 2026-10-09T05:59:36.080Z
updated_at: 2026-10-09T05:59:36.080Z
---
#469 review A4: controls are gross failures (gap -1, wall ~-3) that a float checker would also refuse; shrinking the side by 1e-19 is refused by both exact routes while float(side)==float(side-1e-19). Add that control so the 1e-20 margins are exercised.
