---
type: is
id: is-01m2hh8pjg3amavhy97ycwyat9
title: "PR #160 review D86: the facts handover is per KaTeX span, not per glyph as claimed"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T03:20:15.182Z
updated_at: 2026-09-15T03:32:53.766Z
closed_at: 2026-09-15T03:32:53.765Z
close_reason: "Fixed on PR #160 in e0f67fe7: a probe established KaTeX sets a number as one span, so facts.ts splits typeset numbers into one span per character and a shared digit holds; the handover check requires kept digits of changing numbers (the steps into 18 and 111; 12 -> 13 cannot hold a digit in place because s(13) has no lower bound)."
resolution: null
duplicate_of: null
---
Canonical defect D86 from the 2026-09-14 stack triage (Low). Source: #155 R17.

The facts handover was per KaTeX span, not per glyph as claimed: KaTeX sets a whole number as one span (`4.67553`, `17`), so digits shared between n and n + 1 crossfaded with themselves, lightening by up to 56/255 mid-roll. Coordinator decision: establish by probe whether KaTeX gives each digit a span; if not, split digits so an unchanged digit holds.

Files: `packages/workbench/src/application.js` (~:659-728), `packages/workbench/src/view/facts.ts`, `packages/workbench/probes/facts/handover.js` (:5) @bb3f7c99.
