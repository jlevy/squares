---
type: is
id: is-01m5jr2d9y616b6b95kt3dpmry
title: "headroom.js: skip the root scroll-padding write when the measured value already matches"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-kind-mccarthy
labels: []
dependencies: []
parent_id: is-01m5jr2cr74kbbn71j05pqsgkd
hold: null
hold_until: null
created_at: 2026-10-22T21:25:29.022Z
updated_at: 2026-10-22T21:25:36.536Z
started_at: 2026-10-22T21:25:36.536Z
---
headroom.js sets root.style.scrollPaddingBlockStart on <html> after first layout on every page. Any change to the root's computed style makes Chromium restyle the whole document: ~350 ms on results and atlas, ~136 ms on the index (trace, UpdateLayoutTree after headroom measure). Tested alternatives that do NOT help: a <style> textContent rewrite, a CSSOM :root rule edit; an unrelated root inline property (outline-offset) costs the same. Fix: declare the expected padding in site-nav.css (61.19px at >=660px wide, 81.59px below) and write only when the measurement differs by more than 1px. Measured index->results click-to-settled ~1,240 -> ~800 ms.
