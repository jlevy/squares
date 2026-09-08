# PR 127: Research Handoff Review

The stack contains useful, reproducible progress toward `n = 11`, but its original
handoff was not ready to merge.
Eight findings required corrections to proof claims, acceptance rules and continuation
inputs. Those corrections are complete, and the corrected checkpoint is certified by the
component evidence below.
The segment-localization theorem survives independent exact replay.
No certified lower or upper bound changes.

The owner authorized correcting the findings, merging the ready stack, and continuing
the selected research on a new branch.
This is W10 review followed by W9 remediation and BC-304 closeout, tracked by
`think-yx4g` and `think-yrw1`.

## Scope and Integration Order

| Pull request | Reviewed head | Contribution |
| --- | --- | --- |
| [116](https://github.com/jlevy/squares/pull/116) | `1257d533` | Kernel feature pricing, guarded producer and independent reader, unrun H-125 probe |
| [121](https://github.com/jlevy/squares/pull/121) | `8176e389` | Structural restrictions, conditional dot planning and handoff |
| [127](https://github.com/jlevy/squares/pull/127) | `c89c7646` | Agenda 030 lane results, independent replays and selection |

Review covered the cumulative stack, including scientific claims in Markdown fences,
recorded controls, missing artifacts and current CI. Main advanced to `fbc790b3` during
the handoff; its changes integrated cleanly in local merge `883d5ef8`. The intended
merge order is 116, 121, 127, preserving their ancestry.
The corrected integration tree has its own checkpoint evidence below.

## Findings

| Finding | Correction and evidence | Bead |
| --- | --- | --- |
| R1: Rounded-cover and enlargement arguments fail | Lane E’s proposed scaled T-018 measure assigns only `85353/100000` to the closed `3/500` neighborhood of `[0,1]²`. Its source control covers the square with `4001/4000`. Two exact distance calculations agree on all 1,121 atoms. Separated 45-degree squares also refute the stated `1+2δ` enlargement rule. Retract those helper claims; E.4 does not use them. | `think-vf8g` |
| R2: Deep-corner clip can omit a legitimate off-net core | Triangle avoidance belongs to the actual unit square, not an enclosing square at the net angle. A rational off-net counterexample refutes `a+b>d+cos θ_net`; the safe core-avoidance clip uses `d+B cos θ_net`. | `think-d2hz` |
| R3: Ratio obstruction overstates its domain | Mark banking proves the ratio optimum is at most one. The exact dual proves equality on site set A only. Ratio normalization and the `w_f=1` slice have the same exclusion power; slice form may improve numerical resolution. | `think-ll7y` |
| R4: Feasible lower bounds cannot establish the proposed upper bounds | A family below eleven does not confirm H-129. A family at least eleven obstructs the specified one-body certificate, leaving ownership and compatibility open. H-128’s unsuccessful finite support does not refute its continuum support claim. Rejecting a strip explanation does not rule out full-dual pricing. | `think-3r92` |
| R5: Handoff scripts and state are not safely runnable | The BC-303 fence assumes `/proc/loadavg` and returns success on failed decisions. Lane E’s distance helper misses segment crossings. Session 100 references absent scratch state, and its resume fence remaps rows already on the new net. Promote guarded tools, retain source history and name the remaining unavailable state. | `think-7z36` |
| R6: Rounded angles enlarge exact theorem domains | The upper endpoint of cell 39 is approximately `10.38746567°`; cell 117 starts above `30°`. Use rational cell membership as the theorem and degree values only as approximate labels. Positive exact cover transfer is global over that declared angle domain. | `think-2i9v` |
| R7: Retained-net cap has a sign and endpoint error | The cap needs the absolute angular offset and strict separation for closed cores. Its corrected value remains below the Trump upper bound; the old exact endpoint does not follow. Touching closed squares need separation before being used as a depth-one control. | `think-keyj` |
| R8: Closeout overstates completed work | Run 4 of session 109 is partial; run 5 never ran. Remove unfinished prose placeholders, discharge inherited agenda work at its actual scope, carry complements and missing inputs forward, and resolve certification debt with actual qualifying evidence. | `think-pztz` |

Corrections are dated in the retained lane reports.
Historical run scripts and output remain evidence of what ran, rather than being
silently replaced with a new execution.
New tools have source controls and deliberate failure controls.

## Evidence That Survives

The BC-303 segment reader independently verifies ten horizontal segments of length
`1/10` at `q=96/25`, tolerance `3/500`: 24,381 boxes, 10,960 certified leaves, 1,231
discards, no failures, and exact volume `243/128`. Every leaf and discard is re-decided
rationally. The
[replay receipt](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/pr127-segment-replay.json)
and
[rounded-cover counterexample](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/pr127-rounded-counterexample.json)
retain the checked outputs.
The promoted `packing/devtools/segment_cover_replay.py` retains this replay with
portable load reporting and a failing exit status when verification fails.
The corner-pair theorem and exact angle-cell exclusions retain their earlier independent
replays; their scope corrections do not remove those results.

A stronger control was already available in exp-070: scale its retained `B=9977/10000`
family by `10000/9977`. This produces unit squares inside side `38200/9977 < 96/25`
while preserving depth one and total weight `21342289572/2055263195 ≈ 10.3842`. The
[transported control](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/pr127-unit-control.json)
replayed at maximum depth one over 2,702,488 vertices with 19,335 exact tie decisions.
Only the mass-at-least-eleven condition fails, as expected.
This improves the continuation baseline, not the certified packing bracket.

H-125’s biquadratic feature probe has zero scientific invocations.
Its frozen tool and controls are useful, but the family has not been tested: exp-129
stopped at readiness guards and its operational cutoff expired.
Any target attempt needs a fresh prospective allocation, without rewriting that refusal
as a mathematical negative.

## Next Research Slices

1. **Ownership, principal direction.** Use E.4, corner-pair containment and the exact
   angle cells together.
   Sharing a segment does not force touching.
   Instead, for a horizontal segment of length `ℓ` centered at `m`, two
   interior-disjoint squares within distance `δ` admit a separating edge normal `v`
   whose two facing support values lie in the interval centered at `v·m` of radius
   `ℓ|v_x|/2+δ`. The resulting thin pose slabs are a candidate reduction for a guarded
   pair reader. Test compatibility constraints rather than assume unique ownership.
2. **Fractional depth, efficiency direction.** Start from the retained `10.3842`
   control, preserve exact angle identities when transporting or resuming, and measure
   improvement against it.
   Full-dual pricing is the first diagnostic; the historical 32-row cap did not settle
   the plateau. A strict upper certificate or a verified lower family has the specific
   scope stated in corrected H-129.
3. **Corner structure, bounded discriminator.** One corner’s two selected marks can have
   two distinct, separated owners.
   Test whether adjacent corners can each have two owners: an exact quartet falsifier or
   a complete exclusion would change the ownership case split.
   K4 row-outer pricing is another bounded probe; its missing requirement is
   symmetry-aware verification, not a quarter-turn angle net.

The band ladder is reserve work.
Unrun compositions, rectangle bounds, contact witnesses and closing-route cells retain
their prerequisites.
The corner-class and anchor lanes retain their unfinished complementary domains.
None is closed by a one-body obstruction.

Use slices of at most 30 minutes with concrete artifacts and an integration checkpoint
within about four hours.
Sol/Opus handles mechanical work at the effort warranted by its dependencies;
Astra/Fable handles mathematics at extra high/extra, with max for key insights and
adversarial proof review, as specified in `operating-rules.md`.

## Validation and Merge Decision

At original head `c89c7646`, the record tier passed and 143 focused kernel/session tests
passed. Nineteen fractional-ceiling tests also passed.
Nine stopped sessions explicitly retained certification debt; record validity did not
certify their handoffs.
PR 121’s
[deferred checkpoint](https://github.com/jlevy/squares/actions/runs/34273000687) passed
at `8176e389`. These are baseline receipts, not certification of the corrected
integration tree.

The correction checkpoint’s commits and actual outcomes are recorded below.
Merge publication remains pending at this checkpoint.
After merge, the funded continuation starts from updated main on a new `codex/` branch.

The full checkpoint at `ef8a2e72` ran all 69 steps in 1,313.94 seconds.
Its expensive geometry replays passed, including the 324-case atlas and full
translation-escape screen.
Six steps failed: the local Cairo loader path prevented test collection, the mutation
snapshot exceeded its storage guard, and the document-map and handoff views needed
reconciliation. Those failures are retained; this run does not certify the handoff.
The corrected checkpoint reran the failed components and the fast integration surface
while preserving the unchanged geometry receipts.

## Corrected Integration Checkpoint — 2026-09-08

The fast tier at `cbe9fd76` passed all 62 selected steps in 298.34 seconds, including
4,304 fast tests. Separate structured, revision-bound receipts at `cbe9fd76` pass the
three previously failing full-only components: negative controls, slow behavioral tests
and exhaustive exact behavioral tests.
The retained raw stdout from the failed `ef8a2e72` full invocation records passes for
four expensive full-only components: the 324-case atlas rebuild, the full
translation-escape screen, exact rational grid replay and the `n=40` rigidity replay.
The exact reviewed `ef8a2e72..cbe9fd76` path diff changes only handoff records,
generated views, the selected-entry control and the negative- control snapshot guard,
leaving those four component sources and inputs unaffected.

The
[retained checkpoint evidence](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/pr127-checkpoint/README.md)
contains the raw `ef8a2e72` log and revision-bound `cbe9fd76` receipts, composing
coverage of all 69 declared validation steps.
They do not turn the `ef8a2e72` full invocation into a pass, and the fast and component
runs are not described as a new full invocation.
The four successful full-only replays remain historical evidence from `ef8a2e72`; the
repaired checks are evidence from `cbe9fd76`. The packing bracket and every partial,
stopped or never-run scientific task remain unchanged.
Merge publication is still pending.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
