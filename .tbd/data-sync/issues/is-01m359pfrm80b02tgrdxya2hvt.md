---
type: is
id: is-01m359pfrm80b02tgrdxya2hvt
title: "CI repair: mutation-control snapshot 479 KB over the 160 MiB cap on PR 218"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-22T19:32:46.975Z
updated_at: 2026-09-22T19:32:46.975Z
---
The suite-b job fails test_generator_owned_prospective_outputs_stay_out_of_mutation_snapshots: snapshot_source_bytes() is 168,221,736 against SNAPSHOT_MAX_BYTES = 160 MiB (167,772,160). Answer it by pruning generated output no mutation control reads, per the standing instruction at SNAPSHOT_MAX_BYTES in packing/devtools/run_negative_controls.py, not by raising the cap. Related: think-t1lk.
