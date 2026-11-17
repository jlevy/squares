---
type: is
id: is-01m7nsww6cj9tfxxfgbgkr0cqr
title: "PR #1010 A4: #1008 lacks the blocked:author label its record names"
kind: bug
status: closed
priority: 2
version: 5
delegate: w2-credit-1117r
labels: []
dependencies: []
parent_id: is-01m7khyjgjhvyjyzctxqbhxp5a
hold: null
hold_until: null
created_at: 2026-11-17T22:26:31.756Z
updated_at: 2026-11-17T23:26:55.411Z
started_at: 2026-11-17T22:26:39.760Z
closed_at: 2026-11-17T23:26:55.411Z
close_reason: "fixed after #1010 merged (240e3de0c): blocked:author added to #1008 under development.md's Issue and Pull-Request Labels rule (the pass that changes a blocked entry changes the label after its merge), on the coordinator's corrected ruling; the record's blocked: author and the live label now agree."
resolution: null
duplicate_of: null
---
result-requests.yaml:35759; check_requests --github reports the mismatch. Review A (https://github.com/jlevy/squares/pull/1010#issuecomment-6962745009), PR #1010, severity Low.

## Notes

2026-11-17T22:49Z w2-credit-1117r: deferred. Not added: this lane may edit only the intake and case labels on an issue (coordinator ruling, 17 Nov). The record keeps blocked: author; the mismatch is noted on think-dp8t for the coordinator to raise with the owner. Closes when the label is added or the owner rules otherwise.
