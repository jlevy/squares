---
type: is
id: is-01m12pwdw2geht38n80cp846pk
title: Automated PDF export of the known-best composite
kind: feature
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-08-27T22:54:06.209Z
updated_at: 2026-10-06T08:42:49.585Z
closed_at: 2026-10-06T08:42:49.585Z
close_reason: "Done: origin/main retains packing/atlas/known-best/known-best-1-100.pdf and known-best-1-324.pdf. build_known_best_atlas --update-composites draws them and --check-composites holds the exports to their records."
resolution: null
duplicate_of: null
---
Add a devtools pipeline that renders atlas/known-best/known-best-1-100.svg to a clean PDF with correct page sizing (the artwork is 2400 wide, so the page box must match the aspect rather than scaling into Letter/A4 with silent margins). Wire it into the atlas build and a packing-validate check so the PDF cannot go stale.
