---
type: is
id: is-01m2cv9bvcqxck4cafg8yb1qvv
title: "PR #157 review DOC-05: prior PDF comments assert causes their evidence does not establish"
kind: bug
status: open
priority: 2
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:39:10.572Z
updated_at: 2026-09-13T07:39:10.572Z
---
issuecomment-5648592404 and issuecomment-5648627182 attribute unequal normalised bytes to a render race or missing content, from lengths and an import analysis. Those observations do not establish the cause or exact prepared-HTML identity. Fix: APPEND a dated correction retaining the observed comparisons (839866/839866 and 839457/839866), state that byte equality failed and the cause remains unknown under think-ptit, and distinguish PR149's verified artifact/math guards from that unresolved cause. Do NOT rewrite the historical comments. Note: think-r8zn already carries my own correction of the second comment; cross-link rather than duplicate.
