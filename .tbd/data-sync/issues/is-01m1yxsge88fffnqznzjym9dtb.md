---
type: is
id: is-01m1yxsge88fffnqznzjym9dtb
title: "Font provenance guard: every embedded PDF font and on-screen run comes from a shipped face"
kind: feature
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - explainer
  - pdf
dependencies: []
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
created_at: 2026-09-07T21:53:34.659Z
updated_at: 2026-09-08T06:55:47.032Z
closed_at: 2026-09-08T06:55:47.032Z
close_reason: "Shipped: squares#119 merged to main on 2026-09-08 after a senior review (approve) and its fixes"
resolution: null
duplicate_of: null
---
Extend render_explainer_pdf --check's font scan (think-988s adds the Type3 guard) with an allow-list of BaseFont families: PTSerif, SourceSans3, SourceCodePro (once kpress ships it), KaTeX_*, and Helvetica documented as the atlas figure's exception; any other family (Menlo, Georgia, Times, Arial, .SF) fails the check with the family named. Add the on-screen equivalent to inspect_explainer_typography: a Playwright probe over every text node outside the atlas figure asserting via CSS.getPlatformFontsForNode that each resolves to a custom (shipped) font, in screen and print media. Route the one glyph the page currently takes from the reader's machine, U+2265 in .rel (the template comment near line 267 explains the earlier choice of a system sans over KaTeX_Main), to a shipped face: KaTeX_Main's relation, or a Source Sans 3 symbols subset if one can be vendored; re-run the three-way comparison the comment describes and record the choice. Until kpress ships the mono and the marker fix, the guard's expected failures (Menlo, Georgia) are the evidence for those beads; land it so it fails, then bump the gitlink.
