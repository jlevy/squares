---
type: is
id: is-01m59trfn0cvcm8r52m0bnghdh
title: "PR #578 F1: detach cached articles from response shells locally"
kind: task
status: in_progress
priority: 3
version: 2
delegate: codex-578-f1-fix-20261019
labels: []
dependencies: []
parent_id: is-01m59tb83e779xjn19g896fa78
hold: null
hold_until: null
created_at: 2026-10-19T10:19:19.582Z
updated_at: 2026-10-19T10:19:51.500Z
started_at: 2026-10-19T10:19:51.499Z
---
Address published Review F F1 (Low) at PR578 head b76a24fd29bdab28b5c946adeff88313fd28eb47, review5570079896. Sole committer in existing full checkout intake-review-20261018, new local branch codex/578-cache-fix-20261019; preserve all existing branches and never touch the external owner checkout. Detach article only after awaited math-style discovery. Add a red-green ownership regression for detached cached article, distinct clones and one fetch while preserving style discovery/promise caching/ID scope. Run focused existing Node/article-loader tests and changed-file floor, normal-hook local commit only. No push, comments, PR edits, CI dispatch, prospective671 merge, downloads, environments or broader performance/research/build work. Root coordinates actual671main, final integration/review/CI/publication.
