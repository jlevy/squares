---
type: is
id: is-01m0n60dqqaxwgh44ravq8qqya
title: Debug tbd session hook Node version failure and file upstream issue
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-08-22T16:49:03.734Z
updated_at: 2026-08-22T16:59:20.682Z
closed_at: 2026-08-22T16:59:20.682Z
close_reason: Root-caused the hook Node-version failure (PATH prepend shadows Node 22, misdiagnosis as format incompatibility, doomed npx fallback); verified all line references against v0.7.1; filed jlevy/tbd#254.
---
The tbd-generated SessionStart hook fails in containers with two Node installs: it prepends /usr/local/bin (Node 20) ahead of the Node 22 already on PATH, then misreports the Node-version failure as a repo format incompatibility, then falls back to npx under the same bad Node.
