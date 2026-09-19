# Session-141 Block 4 W5: `think-g4n9` hosted walls

Harvest at 2026-09-19T10:26Z. Instrument is `packing/devtools/check_pr_wall.py`. The
wall is the workflow run start (`run_started_at`) through the start of
`Hold the pull request's wall to its
budget` inside `packing-required` or `pages-required`. Kind is `stacked` (PR 201 into
`cursor/lb-survey-stacked-f02a`). Budget is 180 s. Both walls stay
`enforcement: advisory` under `think-g4n9`.

Re-enforcement needs five consecutive exact-head hosted runs where **both** Packing and
Pages are ≤180 s and measurable.
One over-budget, failed, or unmeasurable wall resets the streak to zero.
This harvest does not close `think-g4n9`, does not flip enforcement, and does not edit
`gate-budgets.yaml`. Do not paste `--sample` into the register: there is still no
`stacked` kind record, and the regression rule stays unjudged.

PR 201 head at harvest start was `9f3f5479`. Later exact-head pairs `5a5dec22` (n=31
landing) and `f640ffc2` (n=30 landing) may still be running at harvest; they do not
change the streak until both walls are terminal and measurable.

## Consecutive count

**0 of 5.** The latest completed exact-head pair (`9f3f5479`) is 186 s / 186 s.

## Measured heads on PR 201

| Head | Packing | Pages | Counts toward 5? |
| --- | --- | --- | --- |
| `bce66e51` | 176 s, green (run 35429738893) | 38 s, scope-skip (run 35429738890) | yes, then reset later |
| `4557e66c` | 198 s (run 35430685974) | 196 s, full (run 35430685967) | no (both over 180); reset |
| `43957eb2` | unmeasurable: suite-b cost-band 70.5 s vs 124.78 s (0.56×); run 35433763446 failed the wall check; science jobs green | green (run 35433763399) | no (Packing unmeasurable); reset |
| `9f3f5479` | 186 s, advisory over budget (run 35434631390, green) | 186 s, full, advisory over budget (run 35434631388, green) | no (both over 180); reset |

`9f3f5479` was still in progress at 09:25Z. Both aggregators finished by 09:28:14Z.
`check_pr_wall` on those runs, kind `stacked`:

- Packing: 186 s. Pole `frontend` (queue 4 s, setup 59 s, work 112 s, job wall 176 s),
  then the aggregator queued 2 s and prepared 4 s.
- Pages: 186 s. Pole `typography` (queue 2 s, setup 17 s, work 97 s, job wall 117 s),
  then the aggregator queued 2 s and prepared 6 s. Not a scope-skip.

Other exact-head hosted Packing/Pages pairs exist on this branch between `4557e66c` and
`43957eb2` (including `1839d573`, `0580e86c`, `c41d8d68`, and cancellations).
They do not change the streak: the latest completed pair is over budget.

## Disposition

Walls remain advisory.
`think-36n1` is closed.
`think-g4n9` stays open.
n=27 `525/100` was already on the core at 10:26 and finishes.
Resume covering after 11:26Z on the same `rank-queue.yaml` with
`--stop-at 2026-09-19T15:26:00Z`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
