---
type: is
id: is-01m4qafvvrkvvc884100g1ch9t
title: "check_requests --github: hold each recorded reply's ids to the posted comment's text"
kind: task
status: open
priority: 3
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
created_at: 2026-10-12T05:48:40.184Z
updated_at: 2026-10-12T07:55:20.424Z
---
From #519 review A5: --github compares replies by URL and date; it should also check that every id recorded under a reply's reported appears in the comment body, so a record cannot claim a reply stated an id it did not.

## Notes

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): https://github.com/jlevy/squares/issues/541 (label enhancement). Tracker https://github.com/jlevy/squares/issues/544.
