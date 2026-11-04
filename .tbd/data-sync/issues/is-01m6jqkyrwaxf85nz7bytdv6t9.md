---
type: is
id: is-01m6jqkyrwaxf85nz7bytdv6t9
title: "T-262 to V3/C3: rerun mixed_n94_L9965's whole-net control under think-4uun's enclosure rule, enter the replay evidence, adopt 1993/200 in n-094's verified lane (#890, intake lane L37)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: bold-ritchie-l37
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-04T07:33:17.211Z
updated_at: 2026-11-04T10:27:08.348Z
started_at: 2026-11-04T07:33:23.700Z
---
Intake lane L37 (bold-ritchie-l37). #892 (merged 0bc5a08c5, think-4uun) replaced AXIS_ROUNDING with axis_captures_agree. Rerun sqverify_fast_census --family mixed --control --only mixed_n94_L9965; enter E-ozden-890-n94-9965-sqverify-fast-replay with the 3 November stage 4 review as its audit_record; T-262's rung as check_results derives it; n-094's verified lower lane to 1993/200, T-091 superseded at n = 94; #890's result-requests entry no longer blocked on think-4uun; generated views; DATA_REVISION re-pinned. Also the nits of #892's confirming review (sqverify_fast_axis docstring and pins, the fine-net auditor's derived_from refusal, the n68 complete-indices mismatch, the packet README, float(bound)). One draft PR; the coordinator posts #890's reply.

## Notes

2026-11-04 (bold-ritchie-l37): PR #898 (draft, labels intake and S2), branch claude/bold-ritchie-xo28us-l37, head 1118ab04e.

- Control: `sqverify_fast_census --family mixed --binary sqverify_fast/target/release/sqverify-fast --out benchmarks/measure-verifier/census-mixed --control --threads 2 --only mixed_n94_L9965` (binary 567a0fd5, source d97758bb, 07:35:14Z to 07:37:44Z, nice -n 19): CONTROLS_REFUSED r=277; 99/100 mutant refused at 600 of 600; near-threshold refused; axis capture in [0.9930860126842824, 0.9930860149308234]. Receipt mixed_n94_L9965.control.json, sha256 be73798aca4a369f195b3d2ec1d7754aae2bebc57cc2bf0d537a265fab813616 (commit 103bf530c).
- Records (d2924a31e): E-ozden-890-n94-9965-sqverify-fast-replay; T-262 V3/C3 (check_results derives it); n-094 verified lower 1993/200; #890 s94-dilation validation dropped (think-4uun no longer named).
- Nits of #892's confirming review: (a) 714788ded, s(94) pinned to an instrumented scratch build (original upper 1.0031171867987096); (b) 7aa242739, auditor admits derived_from and --candidate, full n94 run PASS 37.5 s; (c) filed think-swu4; (d) READMEs refreshed (records commit and 6ddb9047b); (e) 714788ded.
- Release: no-public-change record 3f08f6455 (four papers byte-identical, 69 files x3); DATA_REVISION re-pinned to d2924a31 (1118ab04e).
- Local validation: --records --jobs 2 55/55; --edit --jobs 2 70/71 with the type floor passing through uv run (0 errors).


The revised think-2agl notes staged here on 4 November were applied to think-2agl by the coordinator, who now holds that bead.

2026-11-04 (bold-ritchie-l37): addressing pass for #898's senior review (accept-with-fixes), head f75479351ea6f91e38663a235f4e73221122a2e6.
- F1 dbed7ccb8 + f75479351: PacketProvenance/PACKET_PROVENANCE in sqverify_fast_census; clean-room sentence dropped for same-implementation; certificate path from the report; independence.coverage; --control-date; n94's entry is the generator's output, golden test test_the_890_replay_entry_is_what_the_census_prints.
- F2 f2b776f3d: packing/tests/fixtures/sqverify-fast-axis-instrument/ (patch + README), context test.
- F3 dbed7ccb8: bool refused, (TypeError, ValueError) caught.
- F4 a2f87086e: CLI --candidate test, missing-field admission test (mutations fail them).
- F5 f2b776f3d; F6 9fb3b37e2.
- Release record re-rendered (c98f58606); DATA_REVISION re-pinned to dbed7ccb (013c93137).
- Local: --records 55/55 at 013c93137; --edit 71/71 at f75479351; touched tests 332 passed.
- Hosted at f75479351: Packing validation 41811757040 success; Certificate page 41811756970 success; Branch mergeability 41811740451 success; Deferred checkpoint 41811757068 skipped.
Remaining: coordinator's merge; #890 reply from main; close think-4uun from main.
