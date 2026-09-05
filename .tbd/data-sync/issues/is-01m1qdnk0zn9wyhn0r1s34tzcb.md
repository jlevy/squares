---
type: is
id: is-01m1qdnk0zn9wyhn0r1s34tzcb
title: "Certificate page: display fractions clipped at the top"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1q0p63s2evef5mhkyn16e41
created_at: 2026-09-04T23:57:07.998Z
updated_at: 2026-09-05T00:04:06.836Z
closed_at: 2026-09-05T00:04:06.834Z
close_reason: Commit 387c3508, verified in the browser.
resolution: null
duplicate_of: null
---
Review feedback on PR #79: μ(Q) = 50003/50000 lost the top of its numerator. .tex-d scrolls sideways with overflow-x: auto, which also clips vertically, and the KaTeX display margin is zeroed, so a fraction had no headroom; the block now has vertical padding.
