---
type: is
id: is-01m4fdxysyxrsz86wnrpzt6sr4
title: Resolve survey URL history registrations and T-129 superseded expected set
kind: task
status: closed
priority: 1
version: 4
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
hold: null
hold_until: null
created_at: 2026-10-09T04:14:52.222Z
updated_at: 2026-10-09T04:48:13.099Z
started_at: 2026-10-09T04:20:34.722Z
closed_at: 2026-10-09T04:48:13.098Z
close_reason: "T-129 expectation fixed at owning layer #463; survey URL failures resolved by main integration; #459-#463 hosted green"
resolution: null
duplicate_of: null
---
#459/#460/#466 validate refuse three missing historical registrations for papers/square-packing-methods-survey.{html,md,pdf}; #463/#466 suite A test_superseded_is_marked_on_a_bound_and_where_a_later_result_is_declared excludes T-129. Audit semantically and fix at the owning layer.

## Notes

T-129 (#463 78fdc830e, V0/C0 three dated source-only Daniel #375 reports n105/130/292) derives SUPERSEDED by T-117 (main), T-125 (#442), T-127 (#448/#459); each source side strictly larger than the verified side; records correct, no frontier change. Test expectation fixed on #463 0f1e2d193 (one sorted literal). Survey URL-history refusal (devtools.site_urls check_history vs origin/main) was a pre-integration symptom; 0 failures at #459 31a7397e1, #460 791f304e3, #463 0f1e2d193 locally and in hosted validate. Hosted Packing+Pages green on #459, #460, #463. Coordinator merged #463 into #466 as fa6b4308a.
