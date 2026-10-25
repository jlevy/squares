---
type: is
id: is-01m5qsa1tcazkphxbd029zj58d
title: "Import #798: Amund Kristiansen's 14 upper bounds at 334–504 (gist e4df936 at c9be7b7)"
kind: task
status: in_progress
priority: 2
version: 8
assignee: null
delegate: c-import-798-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5rchxrtvz1ay78s9bqh9hed
hold: null
hold_until: null
created_at: 2026-10-24T20:23:20.140Z
updated_at: 2026-10-25T02:26:21.718Z
started_at: 2026-10-24T20:24:12.673Z
---
New 2026-10-24 issue https://github.com/jlevy/squares/issues/798 (amundsk, 19:03:14Z): fourteen upper bounds at 334, 338, 343, 372, 376, 377, 379, 382, 412, 416, 457, 458, 502, 504, each below #763's 964ee2b side; 12 called new packings found from #763's, 2 refinements (372, 412). Gist amundsk/e4df936fb09c68446598d4c8309d0166 at c9be7b70e2220c2eccb2c5ea746094bc85dda405: s<N>_amund.cert (dilation certificates via Evan Daniel's dilate_cert.py) and s<N>_amund.input.txt. CC0 1.0 per the author's #755 comment of 2026-10-24T19:13:49Z. Report order: after 43f666c (pushed 2026-10-24T06:10:44Z, think-gn29: 108 own-count certificates at 330-997) and the 964ee2b notebook sides (think-lyf9, #795): compare at each count before recording. Stage 0 owner; stage 1 triage read-only first.

## Notes

2026-10-24 c-triage-798-1024 (stage 1 triage, read-only; drafts in /tmp/claude-0/-home-user-squares/d57983cc-21aa-53cd-a24f-c90463a5a3c0/scratchpad/triage-798/). Pin: gist e4df936 at c9be7b70e2220c2eccb2c5ea746094bc85dda405 (tree dd45a26, committed 19:01:54Z, only revision), 29 files 1,104,636 bytes; all 28 issue digests match; CC0 1.0 by issuecomment-6388401978 on #755, so retain all. Sides admitted at 12 places; dilate_cert formulas reproduce every side and centre (tangents differ 1-5 ulp, Apple libm); lineage table vs 964ee2b reproduced exactly by measure_identity. Report order: 43f666c (pushed 06:10:44Z, think-gn29) is below #798 at 372 (+1.91e-11) and 412 (+1.25e-9): not recorded. 12 rows (334 338 343 376 377 379 382 416 457 458 502 504) below every earlier report by 1.24e-5 (457) to 8.75e-3 (334); vs 43f666c at 376/377/416/458/502/504. 382's earlier report is #670's file (same bytes at 964ee2b). Price: certify ~0.25 CPU-h + sharp-controls ~0.8 CPU-h (measured: 504 positive 30.2 s both routes; 334 sharp 160.9 s, 11 controls as expected); checks double it; under the 40 CPU-h item rule. No stage 4 review (beyond-horizon rows); draft S2. Author question (informational): did the 376 search start from 964ee2b's file (packing nearer 43f666c's). Coordinator: walk reads 43f666c as a publication, no need to wait on gn29.


2026-10-25 c-import-798-1024 (stage 2-3 import, PR #802 https://github.com/jlevy/squares/pull/802, branch claude/intake-2026-10-24-issue798, draft, labels intake and S2). Packet amundsk-issue798-2026-10-24 retains all 29 files at c9be7b7 under the CC0 dedication (#755 issuecomment-6388401978). Walk upper-bounds-issue798-20261024 from starts frozen at 2ed0ea740 with 43f666c as an earlier publication: 12 recorded (334 338 343 376 377 379 382 416 457 458 502 504), 372 and 412 not recorded (above 43f666c), 0 undecided, 0 restatements. 12 current beyond-horizon rows, assurance reported, superseding couzo-issue763 (334 343 416 457 458 502), alexchilton (338 504), tymchishin-22-3662 (376), kyleluecke-inos (377), couzo-964ee2b (379), couzo-issue670 (382); requested and replayed list the twelve. Replay: certify 36 jobs 6,028,026 pairs 845.53 route CPU s (669 s wall, 2 workers); check --replay 906 s, 12 certificates and 36 jobs admitted; sharp-controls 132 controls all as expected (3,114 CPU s) and --check all as expected. Identity reproduces the lineage table. Merged main 755ef426b (#794); stamped 2026-10-25; re-pinned 3aa75ff2. When think-gn29 lands 43f666c, whichever PR merges second re-chains 376 377 416 458 502 504. Import reply draft for #798 (stage 7: names no T-NNN; post after merge and verified deploy, coordinator):

@amundsk, thank you for the report, and for the CC0 dedication on #755, which covers this
gist too.

**Received and pinned.** Gist `amundsk/e4df936fb09c68446598d4c8309d0166` at
`c9be7b70e2220c2eccb2c5ea746094bc85dda405`, its only revision. It holds 29 files: the
fourteen certificates, their binary64 inputs and the README. All 28 SHA-256 digests in your
table are the gist's. Under your CC0 1.0 dedication
([#755 comment](https://github.com/jlevy/squares/issues/755#issuecomment-6388401978)),
[the packet](https://github.com/jlevy/squares/blob/main/packing/resources/web/amundsk-issue798-2026-10-24/README.md)
keeps all 29 files.

**Checked.** Each printed side is its certificate's exact side rounded up at 12 places, and
each S′ in your table equals the certificate's header. Both of this repository's exact
routes accept every recorded certificate and refuse its duplicate-square and
outside-container controls, and the sharp controls at exact contact and 1e-30 past it
come out as expected on both. The least wall clearances and pair separations are your
table's figures, to the printed digits. Every side and centre is what `dilate_cert.py`'s
formulas give for its input; where tangents differ, they differ by a few units in the
last place of `tan`, the Apple libm difference you describe. Matched against 964ee2b's
packings, your lineage table is reproduced exactly. Your checkers were not run here.

**Report order.** All fourteen counts lie beyond the case corpus, so each becomes a
beyond-horizon row if it is below every earlier public report at its count. One earlier
report is missing from your comparison: Francisco Couzo's commit
`franciscouzo/square-packing@43f666c`, pushed at 06:10 UTC on 24 October, lowers 8 of these
counts below 964ee2b's sides.

- **372 and 412.** Its sides are below yours by 1.9e-11 and 1.25e-9, so by the rule
  (each report is recorded when it is stronger than everything published before it) those
  two are not recorded.
- **The other twelve.** Yours are below every earlier report, by 1.2e-5 at 457 to
  8.75e-3 at 334. At 376, 377, 416, 458, 502 and 504 the margin is to 43f666c's sides
  rather than 964ee2b's.
- **382.** The earlier certificate is the one Couzo reported in #670, which 964ee2b holds
  unchanged.

**Recorded.** [#802](https://github.com/jlevy/squares/pull/802) records twelve dated beyond-horizon rows, at 334, 338, 343,
376, 377, 379, 382, 416, 457, 458, 502 and 504, each the current row at its count and each
credited to you after the packing it was found from, as your lineage table gives it.
Beyond the corpus they take no register entry. The
[walk](https://github.com/jlevy/squares/blob/main/packing/campaign/issue-intake/upper-bounds-issue798-20261024/README.md)
gives each count's verdict. Nothing you asked for is queued.

**One question, if you have a moment; it holds nothing open.** At 376 your packing lies
nearer Couzo's 43f666c certificate than 964ee2b's: 11 squares beyond 0.1 against 19, at
most 0.24 against 0.79. Did the 376 search start from 964ee2b's
`certificates/best/n376.cert`, as the issue says for all fourteen?

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-25 coord-intake-1024: PR https://github.com/jlevy/squares/pull/802 (draft, intake, S2) at 9a2f6fac3, CI green (40153308419, 40153308552). 12 rows; 372/412 not_registered; #755 answers recorded (think-fc1n). Commit 7c4a50643's message 'on closed #755' is a closing reference to the already-closed #755 (harmless; noted). Senior review A: c-rev-802-1024 (think-dkby). Replies (#798 import reply, #755 follow-up) drafted in think-2l0q/think-fc1n, posted after merge and deploy.
