---
type: is
id: is-01m51jedsrc6wryy5h462eqkry
title: "PR #641 (merge): regularize every re-housed count during intake"
kind: task
status: in_progress
priority: 1
version: 7
delegate: user-eb
labels: []
dependencies: []
parent_id: is-01m51hy396vnjkxe4726egs8x5
hold: null
hold_until: null
created_at: 2026-10-16T05:20:05.943Z
updated_at: 2026-10-16T13:00:55.481Z
started_at: 2026-10-16T05:20:51.337Z
---
Pin 09ba0c143 against main e2e018f32, obtain independent senior review and any required dedicated review, verify exact-source fast plus deferred checkpoint evidence, address findings, merge by merge commit under user regularization completion authorization, and verify main/deployment. No drawing change is claimed for this process PR.

## Notes

PR641 remains unmerged at09ba0c143/e2e018f32. Ordinary CI and full Deferred checkpoint38855304323 passed at exact merge def5d1ca6f51f215607a2c87eb121e3cb8d4b7fe, but trusted reviews A5543468367 and B5543563103 contain unresolved findings. Independent recovery review confirmed A1 deferred-regression disclosure, B1 missing persisted historical lapse blocks, B2 colliding printed run IDs, and A2 deferral regeneration ordering; all other findings/suggestions need dispositions. Existing source owner retains fixes. Public handoff https://github.com/jlevy/squares/pull/641#issuecomment-6209136044 links separate data batch PR644. A future fix invalidates current gate evidence; no final clean review or merge performed.

2026-10-16 ~10:40Z coordinator user-eb: PR #641 MERGE-READY at 7aa4775ea: senior Reviews A and B (round 1), follow-up + correctness Review C (round 2) all addressed (C2 gate hardening deferred to think-k6rj as a design call; moot once the 14 lapsed counts are decided), CI green incl. the deferred checkpoint (38883825029). Waits for the owner's word. Merge FIRST in the regularization-process pair; then retarget #650 to main (think-bb70) and merge it.

2026-10-16 ~13:00Z coordinator: CORRECTION to the 10:40Z merge-ready note: #657's review B4 found #641's --compare predicate misses strong-view losses whose replacement is the axis tool's view (flags 0 of 7 at #657). Tracked as a bug bead under think-g3q7 (title 'default_drawings --compare misses strong-view losses...'). #641 is merge-ready only with that gap accepted as a follow-up; better: fix it in #641 before merge.
