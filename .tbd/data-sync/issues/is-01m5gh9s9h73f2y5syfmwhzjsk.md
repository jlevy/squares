---
type: is
id: is-01m5gh9s9h73f2y5syfmwhzjsk
title: Reconcile shared resource rendering and metadata with upstream adoption merge
kind: task
status: in_progress
priority: 2
version: 2
delegate: about_profiles_implementation
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-22T00:48:41.776Z
updated_at: 2026-10-22T00:48:51.321Z
started_at: 2026-10-22T00:48:51.320Z
---
Resolve only overview_sections.py, suite-file-costs.json and document-map.yaml merge conflicts, preserving the shared profile/resource implementation, exact cost and document entry unions, and incoming Couzo/Joost adoption descriptions via site_resources.py. Run focused checks after the merged release module parses. Stage only owned resolutions; do not commit or push.
