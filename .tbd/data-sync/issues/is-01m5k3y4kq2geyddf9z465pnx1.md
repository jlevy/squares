---
type: is
id: is-01m5k3y4kq2geyddf9z465pnx1
title: test_upper_bound_packets::test_the_records_are_what_the_apply_tool_writes runs at about two-thirds of the 45 s per-test limit on hosted runners (46.94 s once, in shard C)
kind: bug
status: open
priority: 2
version: 1
labels:
  - performance
dependencies: []
created_at: 2026-10-23T00:52:51.959Z
updated_at: 2026-10-23T00:52:51.959Z
---
From #406's lane (23 Oct): the test takes 16.3 s alone locally and 29.5-33.0 s on hosted runners; on #406 at 738fa07f0 it hit 46.94 s against the hard 45 s per-test limit when the suite-file cost record reshuffled it into shard C beside test_negative_controls (100 s) and test_confirm_gupta_records (90 s), with the shard at 2.93x its record. It imports none of #406's modules. Make it fast (OR-14) rather than raise the limit: profile where the 16 s goes (likely re-running the apply tool over every packet) and cut or split it.
