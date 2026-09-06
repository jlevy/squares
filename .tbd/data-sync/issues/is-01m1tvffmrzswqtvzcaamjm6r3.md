---
type: is
id: is-01m1tvffmrzswqtvzcaamjm6r3
title: "PR #93 review R2: expose forkserver CPU measurements as incomplete lower bounds"
kind: bug
status: in_progress
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1tve7ex9akeg5842fnbfesr
created_at: 2026-09-06T07:56:11.287Z
updated_at: 2026-09-06T07:56:52.870Z
---
Review R2 https://github.com/jlevy/squares/pull/93#issuecomment-5557862664; packing/devtools/cpu_durations.py:89-91. RUSAGE_CHILDREN misses forkserver grandchildren. Keep diagnostic plugin unwired, clearly mark incomplete lower-bound accounting, and add end-to-end forkserver regression before any threshold use.
