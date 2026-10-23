---
type: is
id: is-01m5mstqh92zpt3w1tk0xt4vdb
title: "PR #754 A8: the withdrawn files still render as recorded (suggestion)"
kind: bug
status: open
priority: 2
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m5mstad6tr1k9t825pe62ptr
created_at: 2026-10-23T16:34:43.369Z
updated_at: 2026-10-23T17:01:42.023Z
---
Review A of PR #754 (https://github.com/jlevy/squares/pull/754#issuecomment-6369572454); see the review for file:line references and the suggested fix.

## Notes

2026-10-23 c-answers-1023: deferred from #754 (review A, A8), per coord-intake-1023's call. This is presentation only: a rerun without the 1851c2c files changes no verdict, and `beyond_horizon_replay.Held.answer` already keeps them out of the record. Rendering a settled withdrawn step as "not a report (think-8m4k)", or leaving such files out of the walk's entries, would change intake_ledger's step contract (a new verdict or an excluded-publication list), its render, and the #732 walk's ledger.json and README. That is a ledger format change better made on its own, with a test that older ledgers render byte-identically.
