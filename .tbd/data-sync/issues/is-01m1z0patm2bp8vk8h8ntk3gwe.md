---
type: is
id: is-01m1z0patm2bp8vk8h8ntk3gwe
title: Lead the explainer with Trump packing and consolidate problem sections
kind: task
status: in_progress
priority: 2
version: 4
labels: []
dependencies: []
child_order_hints:
  - is-01m1z19m87hvmccrhawtpejwj3
created_at: 2026-09-07T22:44:16.330Z
updated_at: 2026-09-07T22:54:48.570Z
---
W8 documentation edit. Move Trump packing from Figure2 into the opening as Figure1; renumber atlas Figure1 to Figure2 everywhere in the live explainer and supporting references. Rename New Result to A New Bound for Packing 11 Squares. Add a concise Trump1979 best-packing sentence and footnote in the opening; remove standalone Packing11Squares section and merge its remaining content into The Square Packing Problem. Preserve certificate comparisons, T-022 parenthesis, timing footnote, and all verified bounds. Three agents cover cross-reference edits, editorial semantics, and layout assumptions. Rebuild HTML/Markdown/PDF and update or create PR based on current state.

## Notes

Article restructuring and all active Figure1/Figure2 references are edited. Editorial and ordering audits accepted; 43 explainer tests, Ruff, and BasedPyright passed. Fresh 15-page PDF opening, atlas, and merged-section pages inspected; Trump Figure1 fits cleanly on page1. Existing browser layout run had one finding: Figure6 touch (381-100) tap did not turn the square; all other measurements passed. Root is reproducing it once while helper_math audits the touch handler and test. Required pre-push check running. No commit/push until this finding is resolved.
