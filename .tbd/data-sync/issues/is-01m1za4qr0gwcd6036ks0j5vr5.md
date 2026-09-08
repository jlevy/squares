---
type: is
id: is-01m1za4qr0gwcd6036ks0j5vr5
title: Refuse stale exact verified bounds in case prose
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-08T01:29:25.502Z
updated_at: 2026-09-08T01:29:25.502Z
---
The n20 and n21 case bodies still call 24/5 = 4.8 the current verified lower bound under frontmatter 97/20 = 4.85. The prose checker discards the exact fraction and accepts the truncated decimal; its named-field matcher misses the s(n) anchor. Preserve exact identities for explicitly named verified fields, keep directional rounding for displays, recognize the new independently-verified generator wording, and repair the case descriptions without changing any verified bound.
