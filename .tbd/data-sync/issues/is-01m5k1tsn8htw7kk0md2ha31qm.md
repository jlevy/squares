---
type: is
id: is-01m5k1tsn8htw7kk0md2ha31qm
title: Align breadcrumbs with header logo text across the site
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-width-audit
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T00:16:05.282Z
updated_at: 2026-10-23T00:29:49.427Z
started_at: 2026-10-23T00:16:13.825Z
---
Latest user direction supersedes prose-column breadcrumb alignment: left-align every displayed breadcrumb below the header logo text. Use shared header/layout geometry responsively rather than a per-page fixed offset. Preserve plain category/current labels and linked real parents; standalone pages remain without breadcrumbs. Verify desktop and narrow layouts and document the revised design rule.

## Notes

Implemented explicit latest-user exception: present breadcrumbs align first-label text with header logo text, independent of630px prose. Replaced original conflicting prose-track breadcrumb sizing using shared --site-nav-track70rem content width, --site-nav-gutter, --site-nav-link-inset, --site-nav-name-outset tokens and explicit consistent box sizing; no per-page offsets/specificity patch. Header original content track and responsive hit-area inset retained. New existing-shell geometry assertion failed245px before CSS repair and passes4shell×5widths4.82s after; actual generated105page/viewport audit reports0px logo/trail error at every applicable family/width (all4paperHTML included), Overview/News absent. Current producer17family×5width regression passes84.20s. Components received docs wording and updated breadcrumb paragraph separately. News dropdown block untouched. Root owns final preview rebuild/acceptance; source checkpoint complete, leave open until integrated artifact verified.
