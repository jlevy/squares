---
type: is
id: is-01m68mknga9mx8s5cgrq3c3j1z
title: "CI: main's slow lane killed at its 1800 s budget (schedule run 41184290497 at c94df7cef); slow-runner draws sit at 1371-1804 s, fast draws trip the 1 s floor"
kind: bug
status: open
priority: 2
version: 5
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-10-31T09:28:17.673Z
updated_at: 2026-10-31T11:15:48.912Z
---
The scheduled Packing validation run 41184290497 (main at c94df7cef, 31 October 2026) failed only in `slow-lane` (job 124487895179) and in `post-merge-required`, which depends on it. No test failed. 297 tests had passed when `packing-validate` killed the step at its 1800 s hard budget: `FAST_SUITE_BUDGET_SECONDS`, the `budget_seconds` of the "slow behavioral tests" Step in `packing/src/sqpack/cli/validate.py`. The step printed "command timed out after 1800 seconds", and the 298th test was still running. Twenty minutes later the push run of the same tree (41184251410, job 124492073199) reported 298 passed in 1696.48 s.

**None of the six PRs merged today (#835, #848, #834, #833, #853, #850) caused it.** The lane has held 298 tests since at least 27 October, and its summed call time is flat: 5268.44 s on 29 October (run 40842297161) and 5312.18 s on 31 October at c94df7cef, up 0.8%. The largest single change is `test_two_strip_checker.py::...[v2]`, which went from 189.66 s to 207.19 s.

**It has been close to the budget for a week.** Main ran the slow lane 54 times from 24 to 31 October, at 808 to 1804 s with a median of 1452 s. The walls split by runner draw. 33 runs took 1300 s or more and 8 took 1700 s or more; before today the five highest were 1778, 1764, 1760, 1750 and 1743 s. The slow class of runners has sat within 1 to 6% of the kill, and today's draw went past it. On one tree the per-test cost differs 1.3x between draws: 4046 s summed (27 October, 1155 s wall) against 5268 s (29 October, 1686 s wall). At four xdist workers the 5268 s should take 1317 s, and the 1686 s wall is about 78% efficient. The tail is set by the four `test_sqverify_fast_census.py` `mixed_*` cases (196 to 277 s each) and `two_strip_checker[v2]` (207 s).

**A second failure mode also turns this job red.** On the fast class of runners (under 1000 s: 10 runs, 8 of them red) the lane fails its 1 s floor. Every red run checked, three of the eight, failed on `tests/test_translation_escape_screen.py::test_an_adopted_house_retains_its_replayed_tolerance_instability`, at 0.90 s (run 40294622148, 26 October), 0.86 s (40656970104, 28 October) and 0.85 s (41026564353, 30 October). The scheduled reds of 28 and 30 October are this failure. A draft PR on `claude/bold-ritchie-xo28us-cifix` deletes the test's marker and registry entry, as the gate prescribes and as think-w3as and think-395o did before. The test measured 1.14 to 2.86 s on other hosted draws and 1.75 s on a shared four-cpu box, inside the quick lane's ceiling.

**For the owner to decide: the 1800 s kill.** Three options, none done here, and no ceiling was raised or test skipped:

1. Split the slow lane across two runners, as `exhaustive-1` to `exhaustive-3` are split. This changes scheduling, not coverage, and `test_the_post_merge_jobs_partition_the_gate` still has to hold.
2. Re-argue the budget from these 54 readings. The Step's own comment says a suite that reaches its ceiling should be re-argued rather than re-padded.
3. Order xdist so that the 200 s and longer census cases start first.

## Notes

Draft PR #855 (https://github.com/jlevy/squares/pull/855, labelled S2) deletes the marker and the registry entry for the test that keeps failing the floor. It was approved with nits in review A, and the nits are addressed at 5680a5daf. Review A found a fourth floor refusal of the same test: push run 40208626081 (job 121214870144, 25 October) at 0.88 s, which makes 4 of the 8 fast-draw reds checked and all four on this test. The comment on the floor in validate.py now records them. The 1800 s kill itself is still waiting on the owner's choice among the three options above.

PR #851 (lane L3), deep-gate deferred-slow-lane readings on 31 October, by job wall (setup included):
- eda45bc, run 41183439403: success, 1772 s.
- d30eeba, run 41185900782: success, 1535 s.
- 50d2332, run 41188373400: success, 1450 s.
- f3f0dc4, run 41191239581 (job 124508391290): killed at the 1800 s step timeout with no test failure shown (about 296 tests had passed). The same push's suite jobs all ran slower than at 50d2332, which points to a slow runner: suite-b 792 s against 652 s, suite-c 733 s against 435 s, suite-a 447 s against 351 s. suite-b also failed the 45 s per-test guard on two atlas tests (56.08 s, 53.15 s), with the shard at 720 s against a recorded 216 s.
- dc8830b (#851 merged with main 49dac4354), run 41193895854 (job 124516184668): success, 1762 s, again within 40 s of the cap; suite walls on that push were a 459 s, b 378 s, c 726 s, d 507 s.
