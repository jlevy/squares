---
type: is
id: is-01m6ym5fed6w0da4254hkwv4yk
title: "Credit refresh for T-274 (unnir s(12) >= 9929/2500): credit-attributions.json sources/results rows, unnir contributor entry, Ryu's current-lower-bound role, curation note"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-11-08T22:23:50.221Z
updated_at: 2026-11-08T22:23:50.221Z
---
From the senior review of PR #925 (N2). Only the n = 12 case-group row was updated. Missing: sources row for [unnir s12 2026-11-08], results row for T-274, contributor entry for unnir; Ryu (line ~351) still listed as current lower-bound source author; curation note. Posters' 'Lower bounds due to' line derives from that role (atlas_credit_attributions.py:115), so do this before the next poster redraw (think-wvsa). Precedent: 9bc7c94f6, 08c7c1576.
