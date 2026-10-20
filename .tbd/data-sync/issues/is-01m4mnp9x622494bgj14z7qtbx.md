---
type: is
id: is-01m4mnp9x622494bgj14z7qtbx
title: "PR #496 G5: does check_math_markup --check read vendor/kpress?"
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
created_at: 2026-10-11T05:06:42.212Z
updated_at: 2026-10-12T23:39:08.660Z
started_at: 2026-10-11T05:07:03.214Z
closed_at: 2026-10-12T23:39:08.659Z
close_reason: "PR #496 review item G5 fixed in PR #507 (merged 2026-10-12 as e96e9ea95)."
resolution: null
duplicate_of: null
---
Suggestion, unverified. A vendor/kpress pointer change selects only X-027. 'migrated Markdown writes its math as LaTeX' runs check_math_markup -> migrate_math -> lazy check_katex (migrate_math.py:1645) -> kpress_static(). Settle: run check_math_markup --check with vendor/kpress unreadable. If it reads it, claim vendor/kpress and test it; else defer under think-ht59. PR #496, review G: https://github.com/jlevy/squares/pull/496#pullrequestreview-5481975880
