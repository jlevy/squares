---
type: is
id: is-01m4facph0038y9rzhakyby315
title: Open the hero case popover and navigate to expanded Atlas cases
kind: feature
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10.local
labels:
  - website
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-09T03:13:00.958Z
updated_at: 2026-10-09T03:14:19.709Z
started_at: 2026-10-09T03:14:19.707Z
---
Homepage hero opens the existing case popover with an ordinary case-record link as no-JavaScript fallback. Shared case popover has separate actions for Case Record, the matching Frontier table row and the matching Atlas diagram tile, synchronized when stepping cases. Atlas case-target links fully expand the dedicated grid before scrolling to and highlighting the requested case, including cases beyond the initial100. Preserve valid relative URLs from direct case pages, no-JavaScript behavior and invalid-fragment handling. Verify hero53 plus291/324 and relevant history navigation. Coordinate with shared double-chevron convention tracked by think-hyd6.
