---
type: is
id: is-01m45c13h7edpkm3t1xnacadm4
title: "Intake pass: the 41 evand/square-packing commits inside the 7ff3b21 pin that no packet retains (08e8a5f..7ff3b21)"
kind: task
status: closed
priority: 2
version: 5
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T06:29:13.895Z
updated_at: 2026-10-05T08:45:46.136Z
started_at: 2026-10-05T06:29:42.567Z
closed_at: 2026-10-05T08:45:46.135Z
close_reason: "Merged in jlevy/squares#362 (dee22b882): 41 evand commits dispositioned, evidence updates on T-006, T-051-T-053, T-062, T-064, T-081"
resolution: null
duplicate_of: null
---

## Notes

2026-10-05 intake pass (lane evand2, branch claude/ecstatic-pascal-pothtx-evand2 from 208313ddf).

Sweep item: 41 commits 27dd68a..40e442f inside the 7ff3b211 pin whose changed paths no packet retained. Each read in the scratch clone at 7ff3b21.

Evidence updates (files added to the evand-square-packing-2026-10-04 declaration at the same pin, 44 files; no rung moves):
- T-064: k2m3 README (02629f2, a40e2bc, 2eb1545, 37f2d09, ca6d988), k2m3-review README + 6 REPORT.md (0f55a52), ZMX2_AREA.md + zmx2_area _v2 records + tests/tools (bfbdf04: zmx2 --first-order VERIFIED-D4 4,900 roots and VERIFIED 39,200 roots, 399 CPU-s; source still calls zmx2 partial pending a second reader of 4 mutation-blind refinements, ZMX2_AREA.md sec 13). Sentence on E-k2m3-evand-family-report; T-064 next_rung and notes.
- T-081: k2m4-review README + 3 REPORT.md (0f55a52). Sentence on E-k2m4-evand-family-report.
- T-051/T-052/T-053/T-062: claims audit 6383ad8 (VERIFICATION.md, s21/s32/s45/s60 READMEs) and s12/tasks/s21-finish/ incl. xcheck.md, the zmx2 brief the record said was not public. Sentences on E-n021/E-n032/E-n045/E-n060 reports and E-n032-evand-zmx2-full-sym-replay; T-051 composition sentence updated.
- T-006 / T-086: Lean Attain, Spec, SpecBridge, FCSquarePacking, SpecFC, SpecHeadline, S13Lower (f7b4430, 87726c9, c2ae715). Sentence on E-n013-evand-casefree-cover-lean-kernel; T-086 note.

Nothing to import (read in campaign/intake-watch.yaml through 40e442f): TODO/Completed, briefs, 0f55a52's other working material, research notes/scripts (SOS probe, S2 insertable, seam, qx2 PL/go-no-go, s20 generator tools, 27dd68a doc pointers), literature-s32 and proof-anatomy notes, QUADRANT_EXACT pointer, S3Lower s3_eq_2 (toy), Average.lean (lemma, no bound).

No new claim, so no import bead. Follow-up worth pricing (not done here): replay zmx2 cert L4_k02_box7.txt --full --first-order (~400 CPU-s at the source) with the retained d42cbde2 zmx2.rs, compared root for root with k7_full_first_order_v2.log.xz: an interval-certified method beside T-064's rung, after a second reader of ZMX2_AREA.md sec 13.

Committed 7ff9b5ca7 (not pushed). Validation: packing-validate --records passed 44/44 steps; 15 touched test files 562 passed; reachable_tests --since 208313ddf selected everything (zmx2_tools.py is Python under resources): 11280 passed, 3 failed: test_release pin drift (expected on a data commit; DATA_REVISION re-pin owed at integration) and two fixed_core_packet process-reaping tests that also fail when run alone, with no code changed (PID 1 is process_api; environmental). make intake rerun: the evand item is gone.
