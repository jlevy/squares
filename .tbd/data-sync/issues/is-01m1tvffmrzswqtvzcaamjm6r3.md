---
type: is
id: is-01m1tvffmrzswqtvzcaamjm6r3
title: "PR #93 review R2: expose forkserver CPU measurements as incomplete lower bounds"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1tve7ex9akeg5842fnbfesr
created_at: 2026-09-06T07:56:11.287Z
updated_at: 2026-09-06T08:56:29.230Z
closed_at: 2026-09-06T08:56:29.229Z
close_reason: "Fixed via review-approved diagnostic-contract option in c610d308: incomplete CPU lower bounds labelled in terminal and serialized output, real forkserver regression, plugin remains unwired. Final head89ee68c8 CI green. Complete accounting remains on existing think-fckk."
resolution: null
duplicate_of: null
---
Review R2 https://github.com/jlevy/squares/pull/93#issuecomment-5557862664; packing/devtools/cpu_durations.py:89-91. RUSAGE_CHILDREN misses forkserver grandchildren. Keep diagnostic plugin unwired, clearly mark incomplete lower-bound accounting, and add end-to-end forkserver regression before any threshold use.
