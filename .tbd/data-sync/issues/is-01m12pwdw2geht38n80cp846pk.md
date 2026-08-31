---
type: is
id: is-01m12pwdw2geht38n80cp846pk
title: Automated PDF export of the known-best composite
kind: feature
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-08-27T22:54:06.209Z
updated_at: 2026-08-27T22:54:06.209Z
---
Add a devtools pipeline that renders atlas/known-best/known-best-1-100.svg to a clean PDF with correct page sizing (the artwork is 2400 wide, so the page box must match the aspect rather than scaling into Letter/A4 with silent margins). Wire it into the atlas build and a packing-validate check so the PDF cannot go stale.
