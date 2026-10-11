---
type: is
id: is-01m45eykfctkcn3vxwx3dxmn7f
title: "Stack 357 CI: wall-time budget verdicts fail every layer (suite-c 167.4 s vs 154 s, suite-d 131.5 s vs 131 s on #347)"
kind: bug
status: open
priority: 1
version: 4
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
delegate: null
labels: []
dependencies: []
parent_id: is-01m45ex3dssa31jvkkz9bzpc6e
child_order_hints:
  - is-01m45m6x68t479v0ssh5azqrrw
hold: null
hold_until: null
created_at: 2026-10-05T07:20:17.643Z
updated_at: 2026-10-05T08:52:12.616Z
started_at: 2026-10-05T07:29:22.934Z
---
Review B CI status on jlevy/squares#347 (https://github.com/jlevy/squares/pull/347#pullrequestreview-5411026138) and every stack layer (#354, #355, #356, #360) and #350. Per the stack coordinator on 2026-10-05: every layer's failures are wall-time budget verdicts only, with all tests passing. On #347 (run 37274037862 at 9d2f05582): suite-c 167.4 s against its 154 s ceiling (recorded cost 132 s) and suite-d 131.5 s against 131 s, so packing-required fails 'Hold the pull request's wall to its budget'. Latest runs at the reviewed heads: #355 (37274352597) suite-a and suite-c fail; #356 (37274445972) suite-a and validate fail; #354 (37274257279), #360 (37274530812) and #350 (37275173288) were cancelled. #347's lane is root-causing suite-c and suite-d; the upper layers inherit the fix when they merge #347's head. Related: think-skka (suite-file-costs.json re-record; shard 4 at the 10% unrecorded threshold). Closes when the hosted packing-required run is green on #347 and each layer.

## Notes

2026-10-05 07:45 UTC (bead bookkeeper). Related standing beads: think-t7k5 (behavioral shards at their ceilings since 1 October; fourth shard added in #287; remaining was re-taking ceilings from a four-shard cohort and rebuilding the cost record) and think-skka (main's shard 4 at the 10% unrecorded threshold). #347's body says its shard record is #333's, recorded from hosted run 37186951080 on #307's tree (3.1 to 4.5% of each shard unrecorded). This bead is the stack-357 blocker; the general fix may land under either related bead.
