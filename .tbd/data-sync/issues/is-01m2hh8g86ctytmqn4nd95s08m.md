---
type: is
id: is-01m2hh8g86ctytmqn4nd95s08m
title: "PR #160 review D48: mode, range and staging invariants are re-implemented per mutator"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T03:20:08.705Z
updated_at: 2026-09-15T03:32:51.173Z
closed_at: 2026-09-15T03:32:51.172Z
close_reason: "Fixed on PR #160 in fa53f158: enterAspect is the one aspect reset (setMode and a range forcing Animate), keepStageInRange the one range rule for goTo, seekSequence and playAll, endRun ends a run with its clock; item (a) is hidden by the Pack panel since f08bee5c. Follow-up fc8079df (think-z9gm) makes the capture baseline enter Animate first. Checked in check_animate_view's scope section."
resolution: null
duplicate_of: null
---
Canonical defect D48 from the 2026-09-14 stack triage (Medium). Source: #125 F12 ((a) no longer visible since f08bee5c; (b) present).

Mode, range and staging invariants were re-implemented per mutator: `setRange` forced Animate without `setMode`'s reset; `goTo`, `seekSequence` and the `a` key ignored the range (and `a` started continuous play over a running hand run); legacy `stagePack` staged only "previous" (hidden behind the Pack panel since f08bee5c).

Files: `packages/workbench/src/application.js` (~:1966, ~:4999-5025, ~:4909, ~:5306, ~:5934 @bb3f7c99). Related: think-8cti (Pack and Animate split), think-z9gm (capture prepare, a follow-up).
