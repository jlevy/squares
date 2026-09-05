---
type: is
id: is-01m1r3mqpgpxp2cg3maw3cvv1c
title: GitHub Pages deploy path proven end to end for the explainer
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1qgrj2q8kmrbqrgvkaksn87
created_at: 2026-09-05T06:21:08.688Z
updated_at: 2026-09-05T06:25:17.899Z
closed_at: 2026-09-05T06:25:17.899Z
close_reason: Landed in eff24a5e (plain-HTML template, convention in conventions.md, zero-regression pixel comparison), 91c85b25 (Pages enabled with Actions as source; workflow states the prerequisite; subpath test) and 3fde37f5 (formatter notes describe the pinned 0.4.0 only).
resolution: null
duplicate_of: null
---
Pages was not enabled on jlevy/squares and no github-pages environment existed. Enabled Pages with build_type=workflow via the API (https://jlevy.github.io/squares/); configure-pages enablement rejected because it needs a non-workflow token, stated in pages.yml; artifact served under /squares/ in Chromium with the composite image and PDF resolving; deploy itself runs on the first push to main.
