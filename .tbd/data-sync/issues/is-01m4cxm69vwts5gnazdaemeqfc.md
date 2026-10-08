---
type: is
id: is-01m4cxm69vwts5gnazdaemeqfc
title: Preserve offline case alias navigation through the real static page
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-06-site-urls-seo-performance.md
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m49ph0abvy6j16zcq4jse39y
hold: null
hold_until: null
created_at: 2026-10-08T04:51:26.138Z
updated_at: 2026-10-08T11:19:54.978Z
started_at: 2026-10-08T04:52:44.246Z
---
PR #395 old cases.html forwarder sends file:// readers to cases/ directory listing after the move to canonical directory URLs. Preserve registered HTTP canonical identity cases/, provide an actual cases/index.html fallback for offline and no-script readers, verify actual case content rather than directory arrival, and preserve supported query/fragment selectors without weakening invalid-selector handling.
