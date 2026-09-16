---
type: is
id: is-01m2mg6d6n3b5b93qrm2nxkae8
title: "PR #181 integration: scope extracted explainer scripts as render inputs"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m2m6xx00sabcq5zqkrneavd0
created_at: 2026-09-16T06:59:14.770Z
updated_at: 2026-09-16T06:59:14.770Z
---
The branch moves inline explainer JavaScript into packing/devtools/explainer/, but render_explainer.RENDER_INPUTS does not name that directory and the Pages push filter does not include it. A change to page.js/certificate.js/etc. could therefore skip both PR page checks (pages_scope) and the main push workflow. Add the directory to the builder-owned input declaration, let Pages scope derive it, retain a matching push filter, and add/retain contract coverage.
