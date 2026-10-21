---
type: is
id: is-01m5d5x7px17pkpzhdqc62yqp9
title: "Import #686 (gfppoy): 100 certified beyond-horizon packings, 328-998"
kind: task
status: in_progress
priority: 2
version: 2
delegate: c-lane-686
labels: []
dependencies: []
parent_id: is-01m5c0fwsxga70rszkjy1zbp2f
hold: null
hold_until: null
created_at: 2026-10-20T17:31:52.924Z
updated_at: 2026-10-21T01:19:39.109Z
started_at: 2026-10-21T01:19:39.108Z
---
Triage 2026-10-20 (c-lane-686; scratchpad/replies-new/686-triage.md). Evidence: zip attached to the issue (sha256 6b711d6e...a874, matches issue), 100 Evan-Daniel-format certificates, no commit pin, no licence. All counts 328-998 (none in 1..324); all 100 below every earlier value checked (68 main rows, 32 grid starts; smallest margin 6.33e-8 at 810); 5/5 sampled (328, 381, 464, 810, 998) pass sqpack.verify and check_rational_witness_independent, with controls refused at 328. Policy: dated beyond_horizon_claims rows in source-coverage.yaml (no register entry), per #584/#586 and #506. Work: requests-record entry + intake label + intake-ledger run; custody packet (acquire_source cannot take a zip: W7 tool change or SQUISH-facts route); ~7.5 CPU-h replay (300 jobs, max ~184 s) + evidence entries; source entry, 100 rows, 68 superseded; sequencing vs think-3m10/f28n/2vjc/pvav/xu4d/yfoo; stage-7 replies. Owner to confirm: an issue attachment with a digest (no commit/DOI) as the pin (precedent SQUISH #401), and keeping derived facts rather than the zip's bytes absent a licence.
