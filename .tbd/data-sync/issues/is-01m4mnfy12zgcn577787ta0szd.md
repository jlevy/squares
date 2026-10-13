---
type: is
id: is-01m4mnfy12zgcn577787ta0szd
title: "PR #496 E5: verdicts lost when the verify-deployment ceiling fires (suggestion; same root cause as F1)"
kind: bug
status: closed
priority: 3
version: 3
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mneswbxt0m4w1caxy0x320
hold: null
hold_until: null
created_at: 2026-10-11T05:03:13.441Z
updated_at: 2026-10-12T23:39:31.402Z
started_at: 2026-10-11T05:03:45.258Z
closed_at: 2026-10-12T23:39:31.402Z
close_reason: "Completed: PR #496 review finding E5 fixed in PR #507 (merged, e96e9ea95)."
resolution: null
duplicate_of: null
---
Suggestion. .github/workflows/pages.yml:2243-2245, packing/devtools/check_published_site.py:2039-2043. main() prints verdicts only after check() returns, so a job cancelled at the ceiling prints none. Disposed together with F1 (checker wall deadline). E5's premise (longest job 28m22s) is corrected by F4: job 114313930741 ran 58m31s. PR #496, review E: https://github.com/jlevy/squares/pull/496#pullrequestreview-5481683586
