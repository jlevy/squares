---
type: is
id: is-01m25zs0ygtqsqfx233fhjrxqf
title: Implement the selected T-025/T-026 explainer update
kind: task
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - explainer
dependencies:
  - type: blocks
    target: is-01m25zs0xky60mnw0q1fvb5bfz
parent_id: is-01m25zrj5np9ywft00t8j8neaz
created_at: 2026-09-10T15:42:56.976Z
updated_at: 2026-09-10T16:32:07.220Z
closed_at: 2026-09-10T16:20:02.155Z
close_reason: "Implemented the incremental explainer architecture at 47a16331: source-derived T-025/T-026 facts and current bracket, preserved point-only figures, updated README/TUTORIAL and Pages inputs, and passed focused render, 70 tests, PDF determinism, print layout, typography, Flowmark, and Ruff checks."
resolution: null
duplicate_of: null
---
Implement the selected explainer architecture after the decision bead closes. Bind all
numbers and links to retained T-025/T-026 sources rather than retyping them where the
renderer can derive them. Preserve the simpler certificate's role and scope if the
incremental design is selected. Explain threshold atoms and the dilation step from
first principles, with enough exact arithmetic for readers to understand why the
packing budget remains below eleven and why the final statement is a weak limit.

Update the Markdown source, renderer data model and focused tests as required. Do not
fold unvalidated A6, parent-domain, owner-routing, floor-atom, or overnight candidate
claims into the article. Apply Practical Prose and Flowmark. Regenerate web and PDF
artifacts through their maintained tools and keep source-derived values consistent.

## Notes

Final implementation commit is d8bd6d9c after CI-driven Ruff, documentation-map, and Linux math-face fixes. Focused source render, 70 tests, PDF determinism, print layout, and exact hosted math-face command pass locally.
