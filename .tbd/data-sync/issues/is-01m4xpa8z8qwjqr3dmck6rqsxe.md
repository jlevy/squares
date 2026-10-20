---
type: is
id: is-01m4xpa8z8qwjqr3dmck6rqsxe
title: Result pages anchor bibliography links by line number, so every added bibliography entry or document-map row forces a site patch release
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
created_at: 2026-10-14T17:10:46.504Z
updated_at: 2026-10-14T17:10:46.504Z
---
Reported by squares-a5 on 2026-10-14 while cutting site v0.6.2 for #601: check_release_impact (#590) treats any change to the bibliography or the SYNOPSIS document map as a site input because result pages link bibliography entries by line-number anchors (#601 re-anchored 386 links on 84 result pages with identical link text). Every intake records PR therefore needs a site successor edition even when no reader-visible text changes. Fix: anchor bibliography links by a stable id (the entry key) instead of a line number, so adding an entry changes no existing page; then such a change can take a reviewed no-public-change record. Acceptance: adding a bibliography entry leaves every existing result page byte-identical, with a test.
