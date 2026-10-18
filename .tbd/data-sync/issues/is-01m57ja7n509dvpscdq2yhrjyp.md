---
type: is
id: is-01m57ja7n509dvpscdq2yhrjyp
title: "PR #665 A1: rerun final-scope custody receipt"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m57j9xsga57szgfah5ex2bcd
hold: null
hold_until: null
created_at: 2026-10-18T13:13:15.172Z
updated_at: 2026-10-18T13:13:25.519Z
started_at: 2026-10-18T13:13:25.519Z
---
High; review A https://github.com/jlevy/squares/pull/665#pullrequestreview-5562201404. packing/devtools/house-custody-2026-10-11.json:14 still attributes n236 to T-174 although final adoption keeps T-146. Rerun bounded custody command, retain actual receipt, verify receipt test.
