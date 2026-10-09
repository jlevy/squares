---
type: is
id: is-01m4hdhajg6838p3qzbme41s30
title: Recognize retained atlas fonts as owned in PDF validation
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h9s465x7mphy1xxkmdyqc9
hold: null
hold_until: null
created_at: 2026-10-09T22:46:27.151Z
updated_at: 2026-10-09T22:46:40.055Z
started_at: 2026-10-09T22:46:40.054Z
---
PR474 at d19d01f18 ships SquaresAtlasPrint-Bold and SquaresAtlasPrint-BoldItalic, but the production PDF font_findings checker rejects both. Register only these exact retained PostScript faces with provenance and preserve owned-font Type3, missing-embedding and unknown/lookalike refusal. Reproduce production check and browser failure; correct the font catalog/classification with narrow negative tests; qualify on macOS and hosted Linux. Root owns source integration, PR publication and final gate; no GitHub merge authorized.
