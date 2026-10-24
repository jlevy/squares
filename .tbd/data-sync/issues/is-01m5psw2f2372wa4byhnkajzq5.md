---
type: is
id: is-01m5psw2f2372wa4byhnkajzq5
title: "Markdown math: a gate for control characters in math spans (a TAB eats the t of \\times, \\tan), and fix main's three in docs/project/reviews/review-2026-10-03-sqverify-fast-soundness.md (lines 357, 378, 402)"
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T11:13:56.194Z
updated_at: 2026-10-24T11:14:18.785Z
---

## Notes

2026-10-24 coord-intake-1024: from #790 review A (A1, A6). On main the file holds four, not three: lines 357, 378, 402 and 404 (a TAB before 'an'). #790 fixes its own two in the #672 packet README. A gate: refuse a control character (other than newline) inside $...$ or $$...$$ in tracked Markdown, with a negative control; the math-span tooling (devtools.check_math_spans) is the natural home.
