---
type: is
id: is-01m4ywtq6ntygqch1zraeay361
title: "PR #612 B7: #550 and #554 show reply due"
kind: bug
status: open
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
created_at: 2026-10-15T04:23:51.253Z
updated_at: 2026-10-15T05:12:33.846Z
---
Nit. result-requests.yaml #550 and #554 have replies: []; check_requests reports an acknowledgement due. Review: https://github.com/jlevy/squares/pull/612#issuecomment-6184319016

## Notes

Deferred from PR #612 (review B7). #550 and #554 are the project's own issues (author jlevy, the record's owner); they report no result and owe no acknowledgement, and their entries' notes say so (6f1f09634). check_requests still reports 'reply due' because neither the schema nor the tool has a state for an owner-opened issue. Needed: either check_requests treating an issue whose author is the record's owner as owing no acknowledgement (this also clears #532-#545), or an entry field such as acknowledgement: not-owed with a reason. check_requests.py is reserved for squares-a5's code-only PR, so this waits on that.
