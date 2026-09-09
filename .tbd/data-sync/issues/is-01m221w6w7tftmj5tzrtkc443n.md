---
type: is
id: is-01m221w6w7tftmj5tzrtkc443n
title: Remove bold condition labels from figure captions
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-09T03:02:40.774Z
updated_at: 2026-09-09T03:57:45.483Z
closed_at: 2026-09-09T03:57:45.483Z
close_reason: "Implemented in Squares PR #140 (head d6f1cce6): semantic apparatus frames, prefix-only caption emphasis, and print inline-code decoration removal with renderer and live typography regressions."
resolution: null
duplicate_of: null
---
In figure captions, keep the Figure N. prefix bold but render following Condition/Conditions labels at normal caption weight. Apply consistently across HTML and PDF without altering caption sans weight 410, math sizing, baseline, or figure label emphasis. Add a focused regression against representative captions.
