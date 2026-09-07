---
type: is
id: is-01m1yyke6nzgwh6afvamwsrep6
title: "PR #114 review S114-R1: --metrics-patch variants route glyphs in CSS differently from their metric plans"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1yyjv6z0kahq242mm8ndvj7
created_at: 2026-09-07T22:07:44.321Z
updated_at: 2026-09-07T22:29:26.865Z
closed_at: 2026-09-07T22:29:26.828Z
close_reason: fixed on claude/kpress-pt-serif-fonts-1ec7e6
resolution: null
duplicate_of: null
---
packing/devtools/compare_math_fonts.py: several built-in routes' CSS and swaps/scales disagreed. digits left unclassed operator letters (\sin) on stock KaTeX while patching Latin Main-Regular rows; sizeadj scaled the whole Math-Italic face in CSS and only Latin in metrics; ops moved five operators with no operator metric entries; greek let the first composite's KaTeX fallback range claim upright Greek, shadowing KaTeX_MainGreek. From the senior review of PR #114.
