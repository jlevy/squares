---
type: is
id: is-01m6d7e190sgv3s1h6zwdmpd31
title: "Guard: a '|' inside a Markdown table cell is silently split by flowmark-rs 0.4.0 at commit, losing cells (review of #879 lost nine rows' Verdict text)"
kind: task
status: closed
priority: 2
version: 3
delegate: bold-ritchie-l24
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-02T04:14:13.792Z
updated_at: 2026-11-02T07:48:41.129Z
started_at: 2026-11-02T04:53:22.799Z
closed_at: 2026-11-02T07:48:41.129Z
close_reason: Fixed in https://github.com/jlevy/squares/pull/882 (merged 6062867b1) after review A addressed; hosted CI green.
resolution: null
duplicate_of: null
---
Review A of #879 (pullrequestreview-5732014839, finding 1): absolute-value bars inside table cells in docs/project/reviews/review-2026-11-02-ryu-quarter-cube-strongest-tier.md were read as column separators and the pinned flowmark-rs==0.4.0 commit hook dropped the extra cells, silently, in the first commit. An escaped \| survives. Add a pre-format check (devtools or the hook) that refuses an unescaped | inside math or code within a table row, or measure flowmark's behaviour and report it upstream; red-first test. OR-1.
