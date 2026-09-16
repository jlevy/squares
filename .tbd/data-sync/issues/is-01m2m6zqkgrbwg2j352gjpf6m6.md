---
type: is
id: is-01m2m6zqkgrbwg2j352gjpf6m6
title: "PR #180 review R3: make motion-lab identity evidence executable"
kind: bug
status: closed
priority: 1
version: 8
labels: []
dependencies: []
parent_id: is-01m2m6y4gw224dgrwf37bgqnhd
created_at: 2026-09-16T04:18:18.863Z
updated_at: 2026-09-16T08:08:30.677Z
closed_at: 2026-09-16T08:08:30.676Z
close_reason: "Paint-level Motion Lab invariant, opacity-zero/transparent-paint negative controls, committed golden, exact-head integration, and installed-Chrome 36+12-state validation are complete on the reviewed PR #180 line."
resolution: null
duplicate_of: null
---
Store and check the deterministic 48-state motion-lab report and add a drawing-level invariant so a hidden canvas or wrong model fails. CI must invoke the report/golden path rather than relying on a one-time local sentence.

## Notes

Fixed on the integrated PR #180 line: 7439c19e adds same-session SVG-stage screenshot differentials for both Motion Lab pages, removes each representative square layer under a file-backed probe, and requires restoration; live ancestor-opacity and transparent-paint mutants are retained as negative controls. After integrating final #181/main, installed Google Chrome drove all 36 exact and 12 general states and passed the committed golden with painted=true for both pages. Focused checker/browser-floor contracts passed, and the branch-owned mutation-snapshot regression from the 280,487-byte golden is fixed in 84ca6cf3 with an executable no-control-reference assertion and change-scope contract.
