---
type: is
id: is-01m1xc4yz870dda76wbx9aqkq0
title: Honor original row order in exact simplex Bland pivots
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1wz3p3zhgbd8qzv8sw6es9g
created_at: 2026-09-07T07:26:01.191Z
updated_at: 2026-09-07T07:28:07.162Z
closed_at: 2026-09-07T07:28:07.161Z
close_reason: Corrected leaving selection to the lowest original row index; independent reviewer accepted the fix and the reversed-basis triangle regression. Fifteen producer controls passed after the change.
resolution: null
duplicate_of: null
---
Independent BC261 review found that solve() chooses the first negative multiplier by basis position, contradicting its documented lowest-original-row Bland rule when the basis is permuted. Correct the choice and retain a degenerate optimal-face control demonstrating start-order independence. This is a termination/determinism issue; independently checked Farkas receipts remain sound.
