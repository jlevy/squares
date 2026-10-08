---
type: is
id: is-01m4cyb0xzaz61xxn1yep9gph5
title: Inline prepared math assets without losing provenance or idempotence
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-06-site-urls-seo-performance.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m49ph0abvy6j16zcq4jse39y
hold: null
hold_until: null
created_at: 2026-10-08T05:03:54.302Z
updated_at: 2026-10-08T05:10:32.563Z
started_at: 2026-10-08T05:10:32.562Z
---
Independent Astra review found that the shared-asset inliner does not recognize the new data-site-math-styles link attribute. Self-contained exports keep an external metric stylesheet. Inline that exact shared stylesheet, preserve its marker and the separately checked renderer provenance, and keep re-preparation idempotent; retain rejection of undeclared/traversal/remote assets.
