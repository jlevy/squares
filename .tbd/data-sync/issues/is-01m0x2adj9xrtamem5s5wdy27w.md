---
type: is
id: is-01m0x2adj9xrtamem5s5wdy27w
title: "PR #39 review R1: preserve exact forms in formal frontier display"
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels: []
dependencies: []
parent_id: is-01m0x29vkahkr6ht4zx2cahh2x
created_at: 2026-08-25T18:18:32.392Z
updated_at: 2026-08-25T18:38:29.419Z
closed_at: 2026-08-25T18:38:29.406Z
close_reason: Fixed in be35a70; focused regressions, full 32-surface validation, deep-golden replay, and both required CI jobs pass.
resolution: null
duplicate_of: null
---
Formal review R1 at explorations/packing/devtools/render_research_tables.py:133. compact_bound discards exact_form when longer than 28 characters and emits an unmarked rounded value in verified columns; some formal lower-bound displays round upward. Render an exact expression, add regression coverage, and regenerate frontier/STATUS.md. PR #39 review: https://github.com/jlevy/thinking-scratchpad/pull/39#pullrequestreview-5022399787
