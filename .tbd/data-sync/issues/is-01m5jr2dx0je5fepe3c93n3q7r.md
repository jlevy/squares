---
type: is
id: is-01m5jr2dx0je5fepe3c93n3q7r
title: Prerender same-site pages on hover with speculation rules
kind: feature
status: in_progress
priority: 1
version: 2
delegate: claude-kind-mccarthy
labels: []
dependencies: []
parent_id: is-01m5jr2cr74kbbn71j05pqsgkd
hold: null
hold_until: null
created_at: 2026-10-22T21:25:29.631Z
updated_at: 2026-10-22T21:25:36.932Z
started_at: 2026-10-22T21:25:36.932Z
---
Add a <script type=speculationrules> with prerender, eagerness moderate (hover ~200 ms or pointerdown) to every site page head. Chromium (Chrome, Edge) builds the page in the background so the click swaps it in; other browsers ignore the tag. Measured with no DevTools attached (DevTools disables prerendering): index->results ~110 ms, results->atlas ~117 ms, atlas->index ~25 ms click-to-settled with the headroom fix. Static site, no analytics, no unload handlers, so prerendering has no side effects.
