---
type: is
id: is-01m1r4a7xke7n75dz675ezt32t
title: Decide whether the rendered explainer HTML is checked in
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1qgrj2q8kmrbqrgvkaksn87
created_at: 2026-09-05T06:32:53.427Z
updated_at: 2026-09-05T07:01:04.201Z
closed_at: 2026-09-05T07:01:04.201Z
close_reason: "Decided in 80c74f18: the rendered HTML stays out of git. It is a deterministic function of files that are in git (two renders byte-identical), a checked-in copy would be a second thing to keep in step, and the Pages workflow now renders twice and compares (render_certificate_page --check) so a non-reproducing render fails the build instead of publishing."
resolution: null
duplicate_of: null
---
Owner's question: with deterministic Markdown-to-HTML, should packing/site/index.html be committed? Assess against deploy simplicity to GitHub Pages end to end from this branch; record the disposition and any determinism check the workflow gains.
