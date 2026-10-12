---
title: "exp-251 — Session 182 lane K: the heaviest standing n17 flags under the adaptive-row kernel"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-251
  series: series-000
  title: The arity-7 standing flags with the most census weight, run through the kernel under SW9's adaptive-row
    recipe at cap 1169/250, each closure admitted on the standing verifier's full pass
  date: '2026-10-05'
  hypotheses:
  - H-267
  tier: confirmatory
  subject:
    label: The nine arity-7 standing flags with at least three wall or corner cells and best penetration at
      least 5e-3, in projected-gain order (packing/campaign/explorations/X048-session-182-overnight/kernel-targets.txt),
      on the unique-state 24-cell cover at U = 1169/250.
    engine: devtools.check_n17_subpattern (producer and checker) and devtools.verify_n17_kernel_certificate in
      full mode under the kernel-streamed listing, both from the clean run worktree at the session-182
      registration commit; the verdict's count also rests on W7 and A, admitted in exp-249 and verified
      there under the kernel-review-r3 and bb-review-r4 listings
    assurance: verified
    method: exact-algebraic
    host_system: Linux x86_64 remote session container, project Python 3.14.7, one worker per job at nice 10
    selftest_passed: true
    engine_commit: cebb5d15aaa17d0cc13aa302ecbd750a54bfc57d
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: The endpoint7 pattern (the endpoint's own west-wall cells, feasible at U) under the same recipe at
      a 3,600 s ceiling must not close; it returned PASS_CONTROL_STALLED in 1,244 s (receipts/K/kernel-control-endpoint7.json).
      The endpoint's state must survive every admitted entry, which the census checks. H-267's method
      control, n11's mask-0 field replayed through the same adapter, holds, as tests/test_hull_kernel_mask0.py
      passes 6 of 6 at d0c2417ab, reaching PASS_LIBRARY_REPRODUCES_MASK0, with packing/src/sqpack/hull_kernel/
      unchanged since cebb5d15a (the W2 review, F5).
    candidate: Each frozen target's seed and node, re-proved in full by the standing kernel verifier.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 182; the run operator's lane K queue produced and verified each certificate and
      admitted it in the session checkout
    entry_point: packing/devtools/check_n17_subpattern.py
    command: 'From packing/ of the run worktree: nice -n 10 timeout -k 120 7600 .venv/bin/python3 -m
      devtools.check_n17_subpattern --cells CELLS --bins 64 --max-rounds 24 --hull-limit 16 --producer-share
      0.6 --split-floor 512 --max-rows 1152 --split-patience 1 --max-seconds 7000 --save-objects DIR --output
      FILE; on a closure, nice -n 10 timeout -k 120 4000 .venv/bin/python3 -m devtools.verify_n17_kernel_certificate
      --progress --output CERT/verification.json CERT; then devtools.census_n17_certified in the session
      checkout.'
    budget: 7,000 s per kernel target and 4,000 s per verification on one worker; lane K's kernel budget at most
      17 CPU-hours
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-251-n17-overnight-flag-certification
    dirty: false
    commit: cebb5d15aaa17d0cc13aa302ecbd750a54bfc57d
  results:
  - shape: determination
    role: outcome
    question: Is target 1 (side-S0, side-N0, side-S1, interior-SW, interior-NW, interior-W, interior-S) infeasible
      at U, by a certificate the kernel's checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-k1.json) returns PASS_CERTIFIED_CLOSED in 306 s of wall (276 s
      of process CPU; producer 155 s, checker 149 s) on 27 steps and 1,728 rows in 4 rounds, finest row 1/64,
      closure all_parent_poses_forbidden for interior-W at step 26. The standing verifier at cebb5d15a passes
      it in full mode in 173 s, checking all 1,664 live rows in full and 4,132 collision regions by 23,294,320
      exact facet checks, the closure re-derived. Alone it excludes 116,160 states and 14,590 orbits.
  - shape: determination
    role: outcome
    question: Is target 2 (corner-SW, side-N0, side-W0, side-W1, interior-SW, interior-NW, interior-W)
      excluded within the 7,000 s ceiling?
    outcome: criterion_missed
    checked_by: The run (receipts/K/kernel-k2.json) returns PASS_CERTIFIED_STALL in 3,048 s of wall and 2,330 s
      of process CPU, the producer at its 24-round cap. A non-closure; its node is kept for lane D. This is the
      class the plan's review did not count, at best penetration 0.0050045 on the default receipts.
  - shape: determination
    role: outcome
    question: Is target 3 (corner-NW, side-N0, side-W2, interior-SW, interior-NW, interior-W, interior-S)
      infeasible at U, by a certificate the kernel's checker accepts and the standing verifier re-proves in
      full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-k3.json) returns PASS_CERTIFIED_CLOSED in 195 s of wall (165 s of
      process CPU; producer 95 s, checker 97 s) on 18 steps and 1,198 rows in 3 rounds, finest row 1/128,
      closure all_parent_poses_forbidden for interior-SW at step 17. The standing verifier at cebb5d15a passes
      it in full mode in 124 s, checking all 1,169 live rows in full and 3,128 collision regions by 15,910,980
      exact facet checks. Alone it excludes 124,144 states and 15,580 orbits.
  - shape: determination
    role: outcome
    question: Is target 4 (side-S0, side-S1, side-W2, interior-SW, interior-NW, interior-W, interior-S)
      infeasible at U, by a certificate the kernel's checker accepts and the standing verifier re-proves in
      full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-k4.json) returns PASS_CERTIFIED_CLOSED in 597 s of wall (422 s of
      process CPU; producer 267 s, checker 327 s) on 129 steps and 8,636 rows in 19 rounds, finest row 1/512,
      closure all_parent_poses_forbidden for side-W2 at step 128. The standing verifier at cebb5d15a passes it
      in full mode in 269 s, checking all 3,976 live rows in full and 8,869 collision regions by 30,836,984
      exact facet checks. Alone it excludes 125,904 states and 15,794 orbits.
  - shape: determination
    role: outcome
    question: Is target 5 (side-S0, side-N0, side-W2, interior-SW, interior-NW, interior-W, interior-S)
      infeasible at U, by a certificate the kernel's checker accepts and the standing verifier re-proves in
      full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-k5.json) returns PASS_CERTIFIED_CLOSED in 244 s of wall (149 s of
      process CPU; producer 123 s, checker 119 s) on 25 steps and 1,600 rows in 4 rounds, finest row 1/64,
      closure all_parent_poses_forbidden for interior-SW at step 24. The standing verifier at cebb5d15a passes
      it in full mode in 82 s, checking all 1,534 live rows in full and 3,660 collision regions by 17,886,564
      exact facet checks. Alone it excludes 112,796 states and 14,170 orbits.
  - shape: determination
    role: outcome
    question: Is target 6 (side-S0, side-W0, side-S1, interior-SW, interior-NW, interior-W, interior-S) infeasible at U, by a certificate the kernel's
      checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-k6.json) returns PASS_CERTIFIED_CLOSED in 214 s of wall
      (207 s of process CPU; producer 112 s, checker 101 s) on
      63 steps and 4,059 rows in 9 rounds, finest row 1/128,
      closure all_parent_poses_forbidden for interior-S at step 62. The standing
      verifier at cebb5d15a passes it in full mode in 175 s, checking all 2,209 live rows
      in full and 5,679 collision regions by 23,184,284 exact facet checks. Alone it
      excludes 116,888 states and 14,681 orbits. The container restart at about 10:32 killed
      this target's first launch mid-producer (10:35:54); the counted run is the re-run from
      scratch at 10:36:31.
  - shape: determination
    role: outcome
    question: Is target 7 (side-N0, side-W1, side-W2, interior-SW, interior-NW, interior-W, interior-S) infeasible at U, by a certificate the kernel's
      checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-k7.json) returns PASS_CERTIFIED_CLOSED in 295 s of wall
      (231 s of process CPU; producer 157 s, checker 136 s) on
      19 steps and 1,216 rows in 3 rounds, finest row 1/64,
      closure all_parent_poses_forbidden for interior-NW at step 18. The standing
      verifier at cebb5d15a passes it in full mode in 163 s, checking all 1,154 live rows
      in full and 3,504 collision regions by 19,183,136 exact facet checks. Alone it
      excludes 123,976 states and 15,560 orbits.
  - shape: determination
    role: outcome
    question: Is target 8 (corner-SW, side-W0, side-W1, side-W2, interior-SW, interior-NW, interior-W) infeasible at U, by a certificate the kernel's
      checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-k8.json) returns PASS_CERTIFIED_CLOSED in 118 s of wall
      (113 s of process CPU; producer 62 s, checker 55 s) on
      18 steps and 1,152 rows in 3 rounds, finest row 1/64,
      closure all_parent_poses_forbidden for side-W2 at step 17. The standing
      verifier at cebb5d15a passes it in full mode in 69 s, checking all 1,120 live rows
      in full and 3,172 collision regions by 17,924,700 exact facet checks. Alone it
      excludes 105,128 states and 13,198 orbits.
  - shape: determination
    role: outcome
    question: Is target 9 (side-S0, side-W0, side-W1, side-W2, interior-SW, interior-NW, interior-W) infeasible at U, by a certificate the kernel's
      checker accepts and the standing verifier re-proves in full?
    outcome: criterion_met
    checked_by: The run (receipts/K/kernel-k9.json) returns PASS_CERTIFIED_CLOSED in 1,132 s of wall
      (562 s of process CPU; producer 648 s, checker 482 s) on
      147 steps and 12,759 rows in 21 rounds, finest row 1/512,
      closure all_parent_poses_forbidden for interior-W at step 146. The standing
      verifier at cebb5d15a passes it in full mode in 506 s, checking all 5,894 live rows
      in full and 14,213 collision regions by 43,066,872 exact facet checks. Alone it
      excludes 102,304 states and 12,849 orbits.
  - shape: determination
    role: guard
    question: Do the certified exclusions leave at most 10^4 orbits, H-267's threshold?
    outcome: criterion_met
    checked_by: >-
      On the ledger restricted to the entries of arity at most seven, W7, A, this round's
      s182-k1 and s182-k3 to s182-k9, and s182-bc427-t4 from exp-256, census_n17_certified
      counts 78,824 states and 9,990 orbits, the endpoint surviving: ten orbits under the
      threshold of 10^4 (receipts/K/census-arity7-after-bc427-t4.json, on the derived
      ledger receipts/K/ledger-arity7-after-bc427-t4.yaml, whose header names the command
      that writes it). After s182-k9 the same count was 10,173
      (receipts/K/census-arity7-after-k9.json), down from exp-249's 17,690. Lane K's target
      2, closed under BC-423's settings and held for the user's ruling, is not among the
      entries. The census of record at 488c72d77 counts 38,220 states and 4,874 orbits,
      the endpoint surviving (results/exp-256-n17-third-tranche-flags/census.json).
  verdict:
    decision: accepted
    primary_criterion: The certified residue is at most 10^4 orbits with every certificate independently
      checked; rejected if it exceeds 10^4 at arity seven or a certificate excludes the endpoint state.
    reason: >-
      Every entry of arity at most seven is admitted on a reviewed standing verifier's full
      pass, the endpoint's state survives each, and together they leave 9,990 orbits, ten
      under the threshold of 10^4 (receipts/K/census-arity7-after-bc427-t4.json on its
      derived ledger). Lane K's eight admitted arity-7 flags took the count from 17,690 to
      10,173, and BC-427's target 4 (exp-256) took the last 183. The count includes A,
      certified by the interval branch and bound under exp-249's recorded deviation and
      verified there under bb-review-r4, and is 10,173 without it; W7 likewise rests on
      exp-249's verification under kernel-review-r3, and the other nine are verified at
      cebb5d15a. The count does not depend on lane K's target 2, which is held for the
      user's ruling and would take 1,344 more
      (receipts/K/census-arity7-after-bc427-t4.json). The margin is ten orbits, and every
      one of the eleven entries is individually decisive. Lane K's own list ended at
      10,173 with the criterion unmet; exp-256's admission at 488c72d77 fixed the verdict,
      and its cost is exp-256's. The W2 factual review
      (docs/project/reviews/review-2026-10-05-exp-251-h267.md) confirmed the verdict with
      corrections to these disclosures and two figures, which this record carries.
      Addendum after the review: at 340e92b84, after exp-256's s182-bc427-t6, the line is
      8,191 orbits (receipts/K/census-arity7-after-bc427-t6.json), so the claim no longer
      depends on A (8,302 without it); only W7 is individually decisive (11,496 without
      it).
    needs_review: false
    commit: 488c72d77
  effort:
    timebox: 7,000 s per kernel target and 4,000 s per verification; one worker per job
    wall_seconds: 9285
    stopped_by: criterion
---
# exp-251: Session 182 Lane K, the Heaviest Standing Flags

[H-267](../../../hypotheses/H-267-n17-isolated-sub-pattern-residue.md) asks whether
certified sub-patterns of arity at most seven leave at most $10^4$ orbits on the
unique-state cover. This round is lane K of the
[n17 overnight plan](../../../../../docs/project/specs/done/plan-2026-10-05-n17-overnight.md)
(BC-420): the nine arity-7 standing flags with the most census weight, run through the
kernel with the adaptive-row recipe that closed SW9, which they had never had.

H-267 is accepted.
[The W2 factual review](../../../../../docs/project/reviews/review-2026-10-05-exp-251-h267.md)
confirmed the verdict with corrections, which this record carries.
The entries of arity at most seven leave 9,990 orbits, ten under $10^4$
([census-arity7-after-bc427-t4.json](../../../explorations/X048-session-182-overnight/receipts/K/census-arity7-after-bc427-t4.json)).
The last 183 came from BC-427’s target 4, recorded in
[exp-256](exp-256-h267-n17-third-tranche-flags.md).
The count does not depend on target 2 below, which is held for the user’s ruling and
would take 1,344 more.

Lane K’s own round ended when its list was exhausted, at 10,173 orbits with the
criterion unmet. Its wall, 9,285 s, runs from the endpoint7 control’s start at 08:46:26
UTC to `s182-k9`’s verification at 11:21:11. exp-256’s admission of `s182-bc427-t4` at
`488c72d77` fixed the verdict, and that run’s cost is exp-256’s. Each closure was
admitted after the standing verifier passed it in full from the clean run worktree, the
admission commits following the pass by 1 to 26 minutes.

The count includes A, certified by the interval branch and bound under
[exp-249](exp-249-h267-n17-first-certified-sub-patterns.md)’s recorded deviation, and is
10,173 without it. W7 and A were verified in exp-249, the other nine at `cebb5d15a`.
Every one of the eleven entries is individually decisive at 9,990: the review’s
leave-one-out recount leaves between 10,071 and 14,436 orbits without any one of them.
After exp-256’s `s182-bc427-t6` (`340e92b84`) the line is 8,191 orbits
([census-arity7-after-bc427-t6.json](../../../explorations/X048-session-182-overnight/receipts/K/census-arity7-after-bc427-t6.json)).
It no longer depends on A, which leaves 8,302 without it, and only W7 is individually
decisive, leaving 11,496.

The certificate objects are listed in the hosted-data manifest but not yet uploaded
(`think-jhgi`). The census rests on the committed receipts; re-verifying any entry
outside this container needs the upload.

## Admissions

| Target | Cells | Producer | Verifier | Census after |
| --- | --- | --- | --- | --- |
| 1, `s182-k1` | side-S0, side-N0, side-S1, interior-SW, interior-NW, interior-W, interior-S | closed in 306 s, 27 steps, 1,728 rows | full pass, 173 s | 102,124 states, 12,929 orbits |
| 2 | corner-SW, side-N0, side-W0, side-W1, interior-SW, interior-NW, interior-W | 24-round cap at 3,048 s, not closed | — | — |
| 3, `s182-k3` | corner-NW, side-N0, side-W2, interior-SW, interior-NW, interior-W, interior-S | closed in 195 s, 18 steps, 1,198 rows | full pass, 124 s | 89,456 states, 11,336 orbits (after lane A’s state 5683195 too) |
| 4, `s182-k4` | side-S0, side-S1, side-W2, interior-SW, interior-NW, interior-W, interior-S | closed in 597 s, 129 steps, 8,636 rows | full pass, 269 s | 83,148 states, 10,546 orbits |
| 5, `s182-k5` | side-S0, side-N0, side-W2, interior-SW, interior-NW, interior-W, interior-S | closed in 244 s, 25 steps, 1,600 rows | full pass, 82 s | 81,684 states, 10,360 orbits |
| 6, `s182-k6` | side-S0, side-W0, side-S1, interior-SW, interior-NW, interior-W, interior-S | closed in 214 s, 63 steps, 4,059 rows | full pass, 175 s | 79,872 states, 10,132 orbits |
| 7, `s182-k7` | side-N0, side-W1, side-W2, interior-SW, interior-NW, interior-W, interior-S | closed in 295 s, 19 steps, 1,216 rows | full pass, 163 s | 78,852 states, 10,003 orbits |
| 8, `s182-k8` | corner-SW, side-W0, side-W1, side-W2, interior-SW, interior-NW, interior-W | closed in 118 s, 18 steps, 1,152 rows | full pass, 69 s | 73,236 states, 9,291 orbits |
| 9, `s182-k9` | side-S0, side-W0, side-W1, side-W2, interior-SW, interior-NW, interior-W | closed in 1,132 s, 147 steps, 12,759 rows | full pass, 506 s | 72,296 states, 9,168 orbits |

At the margin of the certified count, in the order admitted: `s182-k1` 24,044 states and
3,024 orbits; `s182-k3` 12,660 states and 1,592 orbits; `s182-k4` 6,308 states and 790
orbits; `s182-k5` 1,464 states and 186 orbits; `s182-k6` 1,812 states and 228 orbits;
`s182-k7` 1,020 states and 129 orbits; `s182-k8` 5,616 states and 712 orbits; `s182-k9`
940 states and 123 orbits.
The first is exactly the census’s projected gain for that flag.

H-267’s threshold is read at arity at most seven, so the guard also counts the ledger
with only those entries: 80,260 states and 10,173 orbits after `s182-k9`, 173 orbits
above $10^4$. That count is
[census-arity7-after-k9.json](../../../explorations/X048-session-182-overnight/receipts/K/census-arity7-after-k9.json),
run on
[ledger-arity7-after-k9.yaml](../../../explorations/X048-session-182-overnight/receipts/K/ledger-arity7-after-k9.yaml),
the ledger of record filtered to entries of at most seven cells by the one-line command
in its header.
Its census, certified and entry blocks are identical to the count taken in
scratch at the 11:21 UTC admission, which this file replaces as the record.
The receipts are under
[receipts/K](../../../explorations/X048-session-182-overnight/receipts/K/), the
certificate’s small files under the X048 certificates folder, and its objects in the
[hosted-data manifest](../../../../hosted/n17-x048-session-168-certificates.yaml).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
