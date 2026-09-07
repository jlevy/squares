---
type: is
id: is-01m1yykfykzqk134kvcteajc35
title: "PR #114 review S114-R2: page-overflow culprit scan names clipped semantic MathML"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m1yyjv6z0kahq242mm8ndvj7
created_at: 2026-09-07T22:07:46.121Z
updated_at: 2026-09-07T22:07:46.121Z
---
packing/devtools/check_print_layout.py:286-291: the culprit scan excluded only SVG, so a clipped .katex-mathml math > semantics > mrow subtree could be named as the widest run. From the senior review of PR #114.
