---
type: is
id: is-01m2hh8hjwj7sfydazzkenes78
title: "PR #160 review D59: setSeed in Pack clears optimizing without pause or rebuild; no seed replay check"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T03:20:10.074Z
updated_at: 2026-09-15T03:32:51.741Z
closed_at: 2026-09-15T03:32:51.740Z
close_reason: "Fixed on PR #160 in f1c449b1: setSeed ends the run through endRun (pausing) and a legacy Pack run is rebuilt under the new seed; check_animate_view replays seed 7 exactly, differs under 8, and requires a seed set mid-run to leave the page paused; seed mutations of withSeed and lawKey fail it."
resolution: null
duplicate_of: null
---
Canonical defect D59 from the 2026-09-14 stack triage (Medium). Source: #155 R10 (items c, f). The aliasing, uint32 domain, recorded effective seed and `.d.ts` items are fixed in #160 at f9099096 (think-dq1l, think-gxxc, closed).

`setSeed` cleared `optimizing` without `pause()` or rebuilding the run, leaving `{playing: true, optimizing: false}` during a run; and no page-level check replayed a seed (mutations "seed dropped from lawKey" and "withSeed ignores the seed" passed every checker).

Files: `packages/workbench/src/application.js` (~:4846-4861 @bb3f7c99); a seed probe run by `check_frontend`.
