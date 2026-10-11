---
type: is
id: is-01m3v1a4rr2nd2032jnp1td9db
title: "Hosted CI: the tier timing rules fail on runner speed, not on code (checks tier 0.54x on #262, shard C 1.58x on #255)"
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T06:09:31.413Z
updated_at: 2026-10-01T08:00:07.773Z
closed_at: 2026-10-01T08:00:07.757Z
close_reason: "Landed on main in f9a3409f0 via jlevy/squares#255 (2791d7f78, 08555994b, 7a038a732): per-tier drift and stale rules are advisory on pull requests under think-be1s, ceilings stay enforced, checks and shard C re-recorded as bands from 66 hosted readings. Hosted runs after the change: #255 at 158820d9d 27 pass, 0 fail. Follow-ups on think-611a."
resolution: null
duplicate_of: null
---
On 2026-09-30 and 10-01 the pull-request timing rules failed four hosted runs with no failing test: jlevy/squares#255 shard C at 172 s and 140 s twice against a recorded 88.59 s (1.5x fails), on a runner fleet about 2x slow for every branch that evening; jlevy/squares#255 and #262 checks tier at 59.4 s and 62.3 s against a recorded 114.34 s ('stale in the flattering direction', 0.52x and 0.54x), on fast runners. The same code read 59 to 133 s for the checks tier and 84 to 172 s for shard C across the day. The pull-request wall is already advisory under think-g4n9 for 1.6 to 1.8x runner variance; the per-tier drift rules are still enforced and inherit the same variance in both directions. Owner, 2026-10-01: delegate to Fable to fix the failed CI. Fix the rule so a run is judged on its code, with the ratchet's purpose kept (a real slowdown is still caught), using today's hosted measurements as the test set; land it on the website PR's integration line.
