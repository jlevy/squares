---
type: is
id: is-01m3w446qmzxptdghpen35k717
title: "Results tables: a wider n column that wraps, and a narrower Result column that wraps cleanly"
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T16:17:56.961Z
updated_at: 2026-10-01T19:05:19.325Z
closed_at: 2026-10-01T19:05:19.317Z
close_reason: "70366bb27, 457a0d94d, merged into jlevy/squares#276: n values wrap inline in a wider column (T-056 15 lines to 6 at 1280), long quotients break so Result's floor is 288 px, both tables fit at 1024 with the kind chip's 180 px Rungs column (14 px slack), 242 px scroll at 768."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'the results table still has issues with column width. the n column should be wider and wrap so values like T-056 with many n values don't take up a ton of vertical space. the result column could be narrower and wrap cleanly to make room'. The n cell of a result covering many cases (T-056, T-044, T-007) is one value per line today; it should set its values inline, wrapping within a wider column (ranges collapsed where consecutive). The Result column gives up the width: it is held to 411 px by four unbreakable formulas, so those must break cleanly (at relation and operator boundaries, or scroll inside the cell). This also answers think-b245 (tables scrolling sideways at 1024 and 768). Measure with measure_site_pages columns before and after; test_site_result_columns pins it.

## Notes

Done: 70366bb27 on claude/site-polish-4-columns, merged into claude/site-polish-4. n values are nowrap spans in a 24ch column (T-056: 15 lines to 6 at 1280; row 386 to 165 px); long quotients may break after the solidus, so Result's floor is 288 px (was 411); both tables fit at 1024 (were 63 px over) and scroll 221 px at 768 (was 319). The n column is now left-aligned. Results-page table is taller overall (+476 px at 1280). Slack: about 36 px at 1024 before a wider Rungs column fails the fit test.
