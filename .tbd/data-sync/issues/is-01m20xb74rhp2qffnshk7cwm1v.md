---
type: is
id: is-01m20xb74rhp2qffnshk7cwm1v
title: Keep print emulation active during math-face inspection
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
created_at: 2026-09-08T16:24:15.243Z
updated_at: 2026-09-08T16:46:38.914Z
closed_at: 2026-09-08T16:46:38.914Z
close_reason: "Implemented and independently reviewed in ce3b1ab5 / PR #131. Focused tests, browser controls, both font preferences, PDF reproducibility, and the committed atlas guard pass."
resolution: null
duplicate_of: null
---
Review of PR #128 found that detaching the per-element CDP session resets Chromium print emulation. Later print probes silently inspect screen fonts; serif defaults conceal the error. Keep one attached session through the samples, assert the active medium, and retain regression coverage. Related to the saved sans face correction (think-lghs).
