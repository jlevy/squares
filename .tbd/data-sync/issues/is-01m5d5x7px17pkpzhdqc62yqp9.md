---
type: is
id: is-01m5d5x7px17pkpzhdqc62yqp9
title: "Import #686 (gfppoy): 100 certified beyond-horizon packings, 328-998"
kind: task
status: in_progress
priority: 2
version: 5
delegate: c-lane-686
labels: []
dependencies: []
parent_id: is-01m5c0fwsxga70rszkjy1zbp2f
hold: null
hold_until: null
created_at: 2026-10-20T17:31:52.924Z
updated_at: 2026-10-23T02:26:19.127Z
started_at: 2026-10-21T01:19:39.108Z
---
Triage 2026-10-20 (c-lane-686; scratchpad/replies-new/686-triage.md). Evidence: zip attached to the issue (sha256 6b711d6e...a874, matches issue), 100 Evan-Daniel-format certificates, no commit pin, no licence. All counts 328-998 (none in 1..324); all 100 below every earlier value checked (68 main rows, 32 grid starts; smallest margin 6.33e-8 at 810); 5/5 sampled (328, 381, 464, 810, 998) pass sqpack.verify and check_rational_witness_independent, with controls refused at 328. Policy: dated beyond_horizon_claims rows in source-coverage.yaml (no register entry), per #584/#586 and #506. Work: requests-record entry + intake label + intake-ledger run; custody packet (acquire_source cannot take a zip: W7 tool change or SQUISH-facts route); ~7.5 CPU-h replay (300 jobs, max ~184 s) + evidence entries; source entry, 100 rows, 68 superseded; sequencing vs think-3m10/f28n/2vjc/pvav/xu4d/yfoo; stage-7 replies. Owner to confirm: an issue attachment with a digest (no commit/DOI) as the pin (precedent SQUISH #401), and keeping derived facts rather than the zip's bytes absent a licence.

## Notes

2026-10-22 c-triage-1022b (read-only; coordinator scratchpad triage-1022b/couzo-residue-plan.md).

**What the Couzo history records PR (after #719's) changes for #686.**

- At 9 counts, #686's rows become superseded first by Francisco Couzo's `5a299b4`
  certificates, not by #719: 453, 649, 810, 812, 933, 934, 990, 991 and 997.
  `5a299b4` was pushed 2026-10-21T22:56:37Z, before #719, and lies 1.3e-12 to 3.2e-11
  below #686's rows with a different 12-place print.
- 16 of `4e4c8ce`'s new history rows are superseded by #686's rows, which changes nothing
  for #686.
- **A follow-up on #686 is owed** only if #719's reply there names #719 as what
  supersedes those 9 rows.

2026-10-22 coord-intake-1021b: #686 follow-up posted 2026-10-22T20:04:02Z: #719 (#722) superseded 42 of #686's rows; https://github.com/jlevy/squares/issues/686#issuecomment-6350116497.

2026-10-23 (c-lane-couzo-residue-1022): #730 merged at 02:10Z on 23 October 2026 as fcf2f96a5. At 453, 649, 810, 812, 933, 934, 990, 991 and 997, #686's rows are now superseded_by couzo-reconcile-2026-10-20 (5a299b4, by 1.28e-12 to 3.20e-11; the source credits the nine to Muglich), with #719 superseding those in turn. Our follow-up of 22 October (6350116497) said #719 superseded them, so the correction is posted: https://github.com/jlevy/squares/issues/686#issuecomment-6355894548 (to be recorded under #686's replies by the next records PR). This bead stays open: it is #686's answer_bead and owns the queued credit ask in result-requests.yaml on main, still the owner's decision.
