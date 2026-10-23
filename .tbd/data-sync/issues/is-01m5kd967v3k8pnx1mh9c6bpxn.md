---
type: is
id: is-01m5kd967v3k8pnx1mh9c6bpxn
title: Reproduce the blank window between page navigations reported in Chrome
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m5jr2cr74kbbn71j05pqsgkd
created_at: 2026-10-23T03:36:11.259Z
updated_at: 2026-10-23T03:36:11.259Z
---
Owner report 2026-10-23: in Chrome/Edge, even in a Guest window, the WHOLE window (nav bar included) goes white/black on EVERY click between site pages. Not reproduced here (all at squaremath.org, deploy 7ce902c6a): headless Chromium 141 screencast, warm/cold/stale caches, wifi/4G/slow, light/dark: no fully blank frame (cold cache only: 0-370 ms nav-bar-only frames from font-display: block). Headed Chromium 141 and Chrome for Testing 156.0.8078.47 on Xvfb (software GL), screen recorded with ffmpeg x11grab at 60 fps, Playwright-launched and plain-launched (no feature flags, bare CDP click): old page held 170-650 ms then the new page in one frame, 0 blank frames on about->results, index->about, results->atlas, atlas->news, also at 6x CPU throttle. Ruled out: CSS hiding html/body before scripts, extensions (Guest). Candidates still open: GPU compositing / OS (macOS or Windows) differences, high-DPI or high-refresh displays, navigation by something other than nav links (back button, cards). Next: a DevTools Performance trace with screenshots from the owner's machine (or a screen recording), OS and Chrome version. Scripts: plainchrome.mjs, headed.mjs, blank.mjs (session scratchpad; see think-15b4 for making them a devtool).
