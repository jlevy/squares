---
type: is
id: is-01m32dwews9ybk6snx8ctzt5tv
title: one-spare-inventory n21 and n22 artifacts not re-emitted after orientation_margins (PR 205)
kind: task
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m32dvmtc77znp14556p7c5w2
created_at: 2026-09-21T16:48:13.721Z
updated_at: 2026-10-06T08:47:44.153Z
closed_at: 2026-10-06T08:47:44.153Z
close_reason: "Duplicate of think-6apc (older): both ask to re-emit the n21 and n22-check one-spare inventory artifacts after orientation_margins; none of the three agenda-040 artifacts carries it on origin/main."
resolution: duplicate
duplicate_of: is-01m31gq9n9btr1s9ywpjq84xqb
---
run()'s payload gained an orientation_margins block; the n=32 artifact was regenerated and these two were not. Diffing every shared key of the n=21 record gives 'differing shared keys: []', so no count is wrong -- but the three artifacts are now inconsistent in shape.
