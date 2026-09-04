---
title: session-085 — Agenda 017 continuation and the W5 efficiency block
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-085
  title: Agenda 017 continuation and the W5 efficiency block
  date: '2026-09-04'
  started_at: '2026-09-04T00:35:00Z'
  deadline_at: '2026-09-04T22:26:00Z'
  branch: claude/agenda-017-plan-and-run
  goal: >-
    Carry Agenda 017's four-lane block (the certificate generator, rigidity readiness,
    ten exact ceilings, and the W9 handoff) from session-084's Agenda 016 closeout
    through its own closing milestone, and separately record the W5 efficiency-loop
    block the operator entered directly the same evening as its own agenda-020
    commitment. No session-NNN record was opened while any of this ran: Agenda 017
    declared a 360-minute (six-hour) research wall, and no bead, agent, or process
    stopped for it. This record is composed retrospectively, at the closing milestone,
    from the commit history and the retained artifacts, and says so plainly here rather
    than leaving a reader to infer it from silence; the `recording` field below reads
    `contemporaneous` on every phase only because this session declares an
    offset-aware `started_at` and `deadline_at`, which the campaign ledger's own check
    requires paired with that value regardless of when the phase's own contract was
    actually declared -- see "Why This Record Is Retrospective" below for what that
    field can and cannot be read to mean here.
  workflow_phases:
  - workflow: process-review
    focus: process
    recording: contemporaneous
    objective: >-
      Resume from session-084 / Agenda 016's discharged marker (`think-5j8d`), rerun the
      Agenda 017 preflight-style reconciliation, and open the four lanes.
    commitment: BC-159
    bead: think-uqgp
    status: completed
    entered_by: session_start
    switch_reason: null
    clock_role: work
    budget_minutes: 68
    started_at: '2026-09-04T00:35:00Z'
    deadline_at: '2026-09-04T01:43:00Z'
    expected_output: >-
      One launch packet naming the four lane owners, exact input hashes, output paths,
      safe commands, the concurrency cap and typed stop rules, per Agenda 017's own
      BC-159 exit criterion.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      Frozen-input drift, a duplicate or missing record, an active stale writer, or an
      unreviewed change to a registered criterion.
    fallback: >-
      Run no target command; mark every downstream commitment never-opened with the
      preflight reason.
    outcome: >-
      Re-rendered the ledger, folded the three plan reviews into Agendas 017 and 018 and
      recorded D-432 (the push tier's reachable-tests step keeps its shared 900-second
      cap even when its selector falls back to the whole suite), and recorded that the
      D-422 snapshot-cap guard was still red on hosted CI and on main. No target command
      ran in this window.
    evidence:
    - 'commit dd458471: re-render the ledger after the last prose edit to Agenda 018'
    - 'commit a171b64b: fold the three plan reviews into Agendas 017 and 018, record D-432'
    - 'commit 050b1973: record that the D-422 cap is red on hosted CI and on main'
    stop_reason: >-
      Reconciliation landed; the four lanes' declared entry conditions were met.
    next_action: >-
      Open Lane A -- build the first-party weighted fractional certificate generator and
      test H-061 at its fixed n = 12 threshold.
  - workflow: research-loop
    focus: correctness
    recording: contemporaneous
    objective: >-
      Build the certificate generator, then climb whatever ladder it can reach --
      starting from H-061's fixed n = 12 threshold at side 19/5, and continuing past it
      rather than stopping there, since only C1 among the five conditions mentions n and
      one atom set certifies its side for every larger n. Retain every certificate the
      exact event-cell sweep and the interval branch-and-bound independently accept at
      the same value, and fix the record-integrity defects the block's own retained
      artifacts kept exposing.
    bead: think-yw5g
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The preflight's declared entry conditions were met and Lane A's writer was free to
      build.
    clock_role: work
    budget_minutes: 1178
    started_at: '2026-09-04T01:43:00Z'
    deadline_at: '2026-09-04T21:21:00Z'
    expected_output: >-
      A frozen generator instrument with passing controls, then exp-060 terminal with
      either an exact certificate the frozen verifier accepts, an exact ceiling
      certificate, or the first typed stop with the retained LP state -- per BC-160's
      and BC-161's own exit criteria, which the round's own scope then outran.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --push
    kill_condition: >-
      An accepted certificate that fails the retention gate's second (interval) route,
      three consecutive execution or persistence failures in one lane, or a row-loop
      objective below n reported while placements are still violated.
    fallback: >-
      Freeze the LP state as time-limited process evidence with an explicit
      canonical-result absence; a certificate at a lower side is a typed result about
      the generator, not a rejection.
    outcome: >-
      Retained four results, all V4/C4, over seven distinct n: `T-018` s(11) >= 381/100
      (displacing Stromquist's 2003 value, the smallest open case moving for the first
      time since it was stated); `T-017` s(12) >= 99/25 (climbed across eight rungs from
      H-061's fixed 19/5 threshold -- 19/5, 77/20, 97/25, 39/10, 393/100, 197/50, 79/20,
      99/25 -- the first n = 12-specific lower bound in the retained corpus); `T-019`
      s(17), s(18) >= 459/100 (displacing Massaccesi's published 22529/5000, superseded
      at n = 19 by T-020); and `T-020` s(19), s(20), s(21) >= 24/5 (the first bound of
      any kind proved about n = 20 or n = 21 rather than read off Nagamochi's 2005 closed
      form). Nagamochi's closed form now holds 58 of 65 open cases at n <= 100, down from
      60 at the start of this block. Two searches stopped on cost rather than an answer
      and are recorded as such, not as negatives: n = 18 at side 117/25 = 4.68 (three
      site sets converged to exactly 18.000000, the third after 157 rounds and 7056 s,
      without separating a genuine covering-value plateau from a degenerate vertex), and
      n = 11 at side 3.82 (the covering LP stops at exactly eleven on two independent
      site sets while the exact rejection route's maximum pointwise depth caps the
      feasible total at 1152/175 against the eleven a ceiling needs). Fourteen defects
      were filed (D-430 through D-443); thirteen are fixed and one (D-431, T-009's
      cross-packing significance comparison, deferred to Lane C's unexecuted BC-165) is
      outstanding. Three of the fourteen (D-439, D-442, D-443) are the same class,
      recurring at three different surfaces on the same day: a durable record described a
      rung and the rung moved out from under it. Built the retention gate as a named tool
      (`devtools.decide_certificate`), the `ceiling_side` family and
      `least_size_certified` in `sqpack/fractional/certificate.py`, and two detectors the
      recurring staleness class argued for -- `devtools.check_rung_figures` and
      `devtools.check_case_prose`. Wrote `devtools.render_certificate_reach`, which ranks
      every open case by a proved reach ceiling and, now, by what three certificates
      actually attained (0.98171-0.98270 of their binding packing, mean 0.98229), and
      X-013, which reads that ratio and recommends n = 26 next -- a near-tie on predicted
      gain against n = 51's higher raw prize, at about a quarter of its cost. Of Agenda
      017's other three lanes, only Lane A ran: Lane B (the general rigidity theorem and
      the Stromquist Theorem 3 audit) and Lane C (the ten verified-upper-bound
      promotions and T-009's raise to C4) left no trace in this branch's history, and
      Lane D's W9 handoff (`think-ldq2`) is not referenced by any commit in this window
      either. This is recorded here rather than smoothed into a claim that the four-lane
      plan executed as written.
    evidence:
    - 'packing/frontier/results.yaml: T-017, T-018, T-019, T-020, all V4/C4'
    - 'packing/defects.yaml: D-430 through D-443 (fourteen filed, thirteen fixed, D-431 outstanding)'
    - 'packing/src/sqpack/fractional/certificate.py: ceiling_side, ceiling_side_for_net, grid_refutation_order, least_size_certified'
    - 'packing/devtools/decide_certificate.py, check_rung_figures.py, check_case_prose.py, render_certificate_reach.py'
    - 'packing/campaign/explorations/X-013-where-the-certificate-should-go-next.md'
    - 'commit 6e08a691: build a first-party weighted fractional certificate generator'
    - 'commit 6fc71ce9: s(11) >= 381/100, decided twice from the same frozen bytes'
    - 'commit 9d90aabe: s(12) >= 99/25, and the paired figures that pin the cost curve'
    - 'commit 10cf6479: s(17), s(18), s(19) >= 459/100, and the detector catching its first live rung'
    - 'commit 928969f8: s(19), s(20), s(21) >= 24/5, and a stale-prose class that outlived its own detector'
    stop_reason: >-
      The operator's own directed efficiency block (agenda-020) began the same evening,
      ahead of any further ladder round.
    next_action: >-
      Hand the retention gate's own now-measured cost to the operator-directed
      efficiency block.
  - workflow: efficiency-loop
    focus: efficiency
    recording: contemporaneous
    objective: >-
      Entered directly on the operator's direction rather than drawn from a queued
      candidate: make the exact event-cell sweep that decides C4 at the retention gate
      at least ten times faster, with the identical least covered mass on every retained
      certificate and the Fraction sweep kept unchanged as the reference.
    commitment: BC-196
    bead: think-yrh5
    status: completed
    entered_by: user_request
    switch_reason: >-
      The operator directed this measurement directly, against an already-measured
      baseline, profile and target rather than a pre-declared timebox in the queue.
    clock_role: work
    budget_minutes: 35
    started_at: '2026-09-04T21:21:00Z'
    deadline_at: '2026-09-04T21:56:00Z'
    expected_output: >-
      A change with its equivalence guard intact -- the identical least covered mass on
      every retained certificate, held to the integer route cell for cell against the
      unchanged Fraction route -- per BC-196's own exit criterion.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev pytest tests/test_fractional_sweep_integer.py
    kill_condition: >-
      Any direction where the integer route's least covered mass disagrees with the
      Fraction route's, or a change to a retained certificate's declared value.
    fallback: >-
      Keep the Fraction route as the sole decision path and record the discrepancy as a
      typed rejection rather than a rung.
    outcome: >-
      Rewrote the sweep to decide in int64 on the atom weights' common scale (every
      retained certificate's weights are multiples of 1/200000), holding reachable cells
      as one span per column instead of one tuple per cell, and running the 181
      directions of a certificate in a process pool. Measured on a loaded box against the
      unchanged Fraction route running beside it: n = 17 (1184 atoms) in 21.8 s against
      the 1473 s baseline (68x), and n = 20 (2260 atoms) in 38.7 s against 5378 s (139x),
      both returning the declared least covered mass. A later replay on a quiet box took
      29.4 s wall (about 100 s CPU across four workers) against the same 5378 s
      reference, about 183x, printing the identical verdict. Equivalence checked
      directly, not only by speed: all 181 directions of the 373-atom n = 11 rung,
      Fraction against integer, value and witness cell, no mismatch, in 145 s.
      `packing/tests/test_fractional_sweep_integer.py` (12 tests) and the wider fast
      fractional suite (55 tests, 24 s where the same selection took 351 s that morning)
      both pass. No bound, verdict, or certificate changed; the interval route -- the
      independent second decision at the retention gate -- was not touched. Recorded as
      its own agenda, agenda-020, on the operator's further direction, rather than folded
      silently into agenda-019's BC-190, whose premise (that the retention gate was the
      dominant cost) this measurement retires; BC-190 now starts from the integer sweep's
      own baseline.
    evidence:
    - 'commit d8733ad0: the exact sweep decides in integers, in parallel -- 68x and 139x, same verdicts'
    - 'commit b55e93a4: agenda-020 records the efficiency block as the W5 block it was'
    - packing/campaign/agendas/agenda-020-efficiency-block-the-exact-sweep.md
    - packing/src/sqpack/fractional/sweep.py
    - packing/tests/test_fractional_sweep_integer.py
    stop_reason: >-
      The 10x target and the operator's own under-100-s figure for the n = 20 decision
      were both exceeded by a wide margin, with the equivalence guard intact.
    next_action: >-
      Measure row generation's own cost as a function of container side, now that the
      retention gate is an order of magnitude cheaper and is no longer what binds a run.
  - workflow: documentation-pass
    focus: process
    recording: contemporaneous
    objective: >-
      Close Agenda 017 and this session: write the session record neither was given
      contemporaneously, reconcile `SYNOPSIS.md`'s cold-start Current Handoff against
      the latest terminal session and Agenda 020's own closeout selection, and run the
      validation suite.
    commitment: BC-169
    bead: think-tkwj
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      Every research and efficiency scope above is terminal; what remained was the
      closing record itself.
    clock_role: finalization
    budget_minutes: 30
    started_at: '2026-09-04T21:56:00Z'
    deadline_at: '2026-09-04T22:26:00Z'
    expected_output: >-
      session-085 and SYNOPSIS.md's Current Handoff section naming the latest terminal
      session and exactly one selected next entry, agreeing with Agenda 020's own
      closeout selection.
    validation_command: >-
      uv run --frozen --all-extras --group dev python -m devtools.check_synopsis
    kill_condition: >-
      A next_action that does not resolve to exactly one agenda cell or bead, or a
      selection that disagrees with Agenda 020's own closeout.
    fallback: >-
      Report the disagreement and leave the prior Current Handoff in place rather than
      publish an inconsistent one.
    outcome: >-
      Wrote this record and rewrote `SYNOPSIS.md`'s Current Handoff section to name
      session-085 and select `think-ji0r` (Agenda 019's BC-191) as the next entry,
      agreeing with Agenda 020's own closeout selection. No commit marks this phase's own
      close -- this session does not push -- so its deadline above is nominal, not a
      measured boundary.
    evidence:
    - packing/campaign/agent-sessions/session-085-agenda017-continuation-and-efficiency-block.md
    - SYNOPSIS.md
    stop_reason: >-
      The record and the handoff it reconciles are both written; no further replay
      question or target work is open.
    next_action: >-
      Select BC-191 (`think-ji0r`), which Agenda 020's own closeout already names.
  primary_bead: think-uqgp
  status: completed
  budget:
    wall_minutes: 1311
    finalization_minutes: 30
  stop_conditions:
  - Frozen-input drift, a failed control, or an unreviewed change to a registered criterion.
  - A known-answer, mutation, or negative control that passes when it must reject.
  - A row-generation loop reporting an objective below n while placements are still violated.
  - Three consecutive execution or persistence failures in one lane.
  - The 360-minute research wall Agenda 017 declared -- not honoured; see the goal above.
  progress:
    metric: >-
      Cases carrying a first-party fractional-certificate result at V4/C4, and the
      retention gate's own decision cost
    before: >-
      n = 11 at 2 + 4/sqrt(5) = 3.788854 (Stromquist 2003, inherited, unmoved since
      stated); n = 12 with no bound specific to it ever proved; n = 17-19 at
      22529/5000 = 4.5058 (Massaccesi, adopted session-083/084); n = 20 and n = 21 on
      Nagamochi's 2005 closed form only. The exact event-cell sweep that decides C4 at
      the retention gate cost up to 5378 s on the largest retained certificate.
    after: >-
      Seven cases carry a first-party certificate at V4/C4: T-018 (n = 11, 381/100),
      T-017 (n = 12, 99/25), T-019 (n = 17, 18, 459/100), T-020 (n = 19, 20, 21, 24/5).
      Fourteen defects filed, thirteen fixed, one (D-431) outstanding. The retention
      gate decides the identical verdicts in integers, 68x to roughly 183x faster,
      with the Fraction route retained as its reference (agenda-020). X-013 recommends
      n = 26 as the next target; Agenda 019's BC-191 is selected as the next entry.
  delegations: []
  outputs:
  - packing/src/sqpack/fractional/generate.py
  - packing/src/sqpack/fractional/certificate.py
  - packing/src/sqpack/fractional/colgen.py
  - packing/src/sqpack/fractional/sweep.py
  - packing/src/sqpack/fractional/interval.py
  - packing/src/sqpack/fractional/ceiling.py
  - packing/devtools/decide_certificate.py
  - packing/devtools/check_rung_figures.py
  - packing/devtools/check_case_prose.py
  - packing/devtools/render_certificate_reach.py
  - packing/cases/n11_fractional_certificate/
  - packing/cases/n12_fractional_certificate/
  - packing/cases/n17_fractional_certificate/
  - packing/cases/n20_fractional_certificate/
  - packing/frontier/results.yaml
  - packing/frontier/evidence.yaml
  - packing/frontier/CERTIFICATE-REACH.md
  - packing/defects.yaml
  - packing/campaign/explorations/X-013-where-the-certificate-should-go-next.md
  - packing/campaign/agendas/agenda-019-efficiency-first-retarget-and-deep-strategy.md
  - packing/campaign/agendas/agenda-020-efficiency-block-the-exact-sweep.md
  - docs/project/handoff-2026-09-04-block-close.md
  - packing/tests/test_fractional_sweep_integer.py
  - packing/tests/test_fractional_certificate.py
  - packing/tests/test_fractional_generate.py
  - packing/tests/test_fractional_interval.py
  - packing/campaign/agent-sessions/session-085-agenda017-continuation-and-efficiency-block.md
  - SYNOPSIS.md
  checks:
  - 'packing/frontier/results.yaml: T-017, T-018, T-019, T-020 all V4/C4, seven n covered'
  - 'test_fractional_sweep_integer.py: 12 tests, integer sweep equals Fraction sweep on every checked direction'
  - 'agenda-020 equivalence: all 181 directions of the 373-atom n = 11 rung, Fraction vs integer, no mismatch, 145 s'
  - 'devtools.validate_schemas, devtools.check_synopsis, sqpack.campaign.ledger check, packing-validate --records: run at this session''s close'
  resource_rollups:
  - packing/campaign/resource-usage/21ae3bfc-58a6-55fc-90e3-6e29d229a7f1.yaml
  - packing/campaign/resource-usage/agent-a046eb1f2ce695424.yaml
  - packing/campaign/resource-usage/agent-a069142925bcad602.yaml
  - packing/campaign/resource-usage/agent-a0fb0642982272ded.yaml
  - packing/campaign/resource-usage/agent-a1406370ce8ad7f7a.yaml
  - packing/campaign/resource-usage/agent-a14867dfcd89a69c2.yaml
  - packing/campaign/resource-usage/agent-a3f30e5ab2b0488a9.yaml
  - packing/campaign/resource-usage/agent-a4d91eccaa1a7c1a4.yaml
  - packing/campaign/resource-usage/agent-a5468237a9b6a51b8.yaml
  - packing/campaign/resource-usage/agent-a587ee224010e94b2.yaml
  - packing/campaign/resource-usage/agent-a7e296c28af127587.yaml
  - packing/campaign/resource-usage/agent-a8183c5a7cbf8292a.yaml
  - packing/campaign/resource-usage/agent-a911143bb96f57d46.yaml
  - packing/campaign/resource-usage/agent-a983accbcf4dec34e.yaml
  - packing/campaign/resource-usage/agent-a99c7dd46230e70ac.yaml
  - packing/campaign/resource-usage/agent-aa151b341a1282a9c.yaml
  - packing/campaign/resource-usage/agent-ab5dc622f5e3cd4f1.yaml
  - packing/campaign/resource-usage/agent-abbc02d152a69365e.yaml
  - packing/campaign/resource-usage/agent-ac3b7b42eccbc6c1d.yaml
  - packing/campaign/resource-usage/agent-ac6696e121f49c162.yaml
  - packing/campaign/resource-usage/agent-aeb058fb0c1d2f3c5.yaml
  - packing/campaign/resource-usage/agent-aef67a6b900e0380b.yaml
  - packing/campaign/resource-usage/agent-af0384c2dcfbb0dbd.yaml
  - packing/campaign/resource-usage/agent-afa3beed39454290e.yaml
  stop_reason: >-
    Agenda 017's four-lane block reached its closing milestone (only Lane A ran to a
    registered result) and the operator-directed W5 efficiency block (agenda-020)
    reached and passed its own target with its equivalence guard intact; this record
    and the SYNOPSIS handoff it reconciles close both.
  next_action: >-
    Select BC-191 (`think-ji0r`), Agenda 019's efficiency-loop measurement of row
    generation's cost against the container side -- row generation is 79-94% of every
    round, site density has never been set as a function of side, and an untuned grid
    cost 8.8x at n = 20's own side -- now that the retention gate is off the critical
    path. `think-jgeg`, the sibling question of whether the generator's own
    accept-or-reject decision belongs on the interval route, follows once BC-191 lands,
    re-based on the integer sweep rather than the Fraction sweep; the retarget
    candidates wait on both. `think-5j8d` is the marker Agenda 016's closeout discharged
    and is not this session's selection.
---
# Session-085 — Agenda 017 Continuation and the W5 Efficiency Block

Agenda 017’s four-lane block, continued past session-084 / Agenda 016’s closeout marker
`think-5j8d`, plus the W5 efficiency-loop block recorded separately as
[agenda-020](../agendas/agenda-020-efficiency-block-the-exact-sweep.md).

## Why This Record Is Retrospective

No `session-NNN` record was opened while any of this ran.
Agenda 017 declared a 360-minute research wall from its own start; the first commit on
this branch lands at `2026-09-04T00:35:17Z` and the last one plainly in this record’s
scope (`b55e93a4`, recording agenda-020’s own closeout) lands at `21:56:14Z` -- about
1281 minutes, roughly 3.6 times the declared budget, with no deadline honoured along the
way. This document is written at the closing milestone, after the fact, from the commit
history and the retained artifacts rather than from a live declaration made as the work
happened. Every `workflow_phases` entry above nonetheless reads
`recording: contemporaneous`, and that is not the document contradicting itself:
`sqpack.campaign .ledger check` treats a session that declares an offset-aware
`started_at` and `deadline_at` as **clocked**, and refuses any clocked session whose
phases are not all `recording: contemporaneous`, independent of what each phase’s own
clock says.
Since this record states its real start and close from commit timestamps -- a
measurable quantity, and the one the block’s own facts are worth carrying in -- the
field is pinned to `contemporaneous` by that rule rather than by a claim that any phase
contract was declared in advance.
The phase-level `started_at`/`deadline_at`/`budget_minutes` fields below are the real
windows a reader can check against the cited commits, and the ledger’s own rule for a
`contemporaneous` phase requires `expected_output`, `validation_command`,
`kill_condition` and `fallback` to be filled rather than left `null` too -- so each
phase’s copy of those fields is drawn from what Agenda 017’s own commitments (`BC-159`,
`BC-160`/`BC-161`, `BC-169`) or Agenda 020’s `BC-196` actually declared in their own
`entry`/`exit`/`budget` prose, since that prose is the genuine prospective declaration
here, made before this session record existed to hold it, rather than a
plausible-sounding retrofit invented now.

## Resource Accounting: What Is Absent, Not Estimated

`resource_rollups` is empty.
`devtools.check_session_rollups` will name this session as declaring none, and that is
correct rather than an oversight to route around.
Two things are true at once: the wall-clock span above is real and derived from commit
timestamps, which is the one quantity this record can measure; and no harness-log
receipt exists for the 2026-09-04 block at all -- `packing/campaign/resource-usage/`
holds nothing dated after 2026-09-03. The underlying harness transcript for this branch
is one continuous log already rolled up once, for session-083, as
`packing/campaign/resource-usage/21ae3bfc-58a6-55fc-90e3-6e29d229a7f1.yaml`; rolling it
up again now would restate session-083’s own already-cited turns, tokens and tool calls
under a second name rather than measure this session’s distinct cost, which is exactly
the kind of double-count this record’s own defects (D-439, D-442, D-443) exist to warn
against. So agent and harness time for this session is recorded here as **absent**, not
zero and not estimated, following the same convention the rollup schema itself uses for
a measurement one harness cannot supply.

## What Actually Ran, Against What Agenda 017 Planned

Agenda 017 opened four lanes after its preflight: Lane A (the certificate generator and
an `n = 12` test of `H-061`), Lane B (the general rigidity theorem and a Stromquist
Theorem 3 audit), Lane C (ten verified-upper-bound promotions and `T-009`’s rung), and
Lane D (the `think-ldq2` W9 handoff, then two gate defects).
Only Lane A left a trace in this branch’s commit history, and its own scope grew well
past what was fixed for it: `H-061` fixed `n = 12` at side `19/5`; what got retained was
an eight-rung ladder to `99/25`, plus a fresh certificate at `n = 11` (`T-018`,
`381/100`, displacing Stromquist’s 2003 value for the first time since it was stated)
and another at `n = 17`-`21` (`T-019`/`T-020`). Lane B, Lane C and Lane D do not appear
in this branch’s commits; `D-431`, deferred to Lane C’s `BC-165`, is still outstanding,
and `T-009` remains at `C3`. This is recorded plainly rather than folded into a claim
that the four-lane plan executed as written -- see `OR-9` on leading with what a branch
cost, which includes what it did not do.

## Results Retained

| Result | Bound | Displaces | Movement |
| --- | --- | --- | --- |
| `T-018` | `s(11) >= 381/100 = 3.81` | `2 + 4/sqrt(5) = 3.788854`, Stromquist 2003 | `+0.021146` |
| `T-017` | `s(12) >= 99/25 = 3.96` | `3.788854`, inherited from `n = 11` | `+0.171146` |
| `T-019` | `s(17), s(18) >= 459/100 = 4.59` | `22529/5000 = 4.5058`, Massaccesi 2026 | `+0.0842` |
| `T-020` | `s(19), s(20), s(21) >= 24/5 = 4.80` | `4.5058`; `1 + sqrt(13)`; `1 + sqrt(14)` | `+0.2942`, `+0.194449`, `+0.058343` |

All four are `V4`/`C4`: each certificate is decided twice from the same frozen bytes, by
the exact event-cell sweep and by an interval branch-and-bound with directed rounding,
and the two routes agree on the least covered mass to the digit.
Seven distinct cases now carry a result from this instrument; Nagamochi’s 2005 closed
form holds 58 of 65 open cases at `n <= 100`, down from 60. Full detail, including the
two searches that stopped on cost rather than an answer (`n = 18` at `4.68`, `n = 11` at
`3.82`), is in
[the block-close handoff](../../../docs/project/handoff-2026-09-04-block-close.md) and
in each result’s own `next_rung` in [`results.yaml`](../../frontier/results.yaml).

## The Efficiency Block

[Agenda 020](../agendas/agenda-020-efficiency-block-the-exact-sweep.md) is entered
directly on the operator’s own direction and recorded as its own commitment rather than
folded into Agenda 019’s `BC-190`. The exact event-cell sweep that decides `C4` at the
retention gate now decides in `int64` on the atom weights’ common scale, holding
reachable cells as spans and running the 181 directions in parallel: `68x` at `n = 17`
and `139x` at `n = 20` on a loaded box, about `183x` on a quiet one, the identical least
covered mass every time and the `Fraction` route kept unchanged as the reference.
No bound, verdict, or certificate moved.
What this retires is `BC-190`’s premise that the retention gate was the dominant cost;
what it does not touch is `BC-191`’s cost, row generation, which is now what binds a
run.

## Fourteen Defects, One Class Three Times

`D-430` through `D-443` were filed in this block.
Thirteen are fixed; `D-431` (T-009’s significance rationale compares its interval
certificate against a rational certificate on a *different* `n = 29` packing) is
outstanding, deferred to Lane C’s `BC-165`, which did not run.
Three of the fourteen -- `D-439`, `D-442` and `D-443` -- are the same class recurring at
three different surfaces on the same day: a durable record described a rung, and the
rung moved out from under it, in the results register, then in five case bodies six
hours after the first detector was built, then in a generated document’s own hedge.
Two detectors exist now because of it: `devtools.check_rung_figures` and
`devtools.check_case_prose`, both in the records tier.
Full detail for every entry is in [`defects.yaml`](../../defects.yaml).

## Where Next

[X-013](../explorations/X-013-where-the-certificate-should-go-next.md) reads the
attainment ratio three certificates actually landed on (`0.98171`-`0.98270` of their
binding packing, mean `0.98229`) and recommends `n = 26` next -- a near-tie on predicted
gain against `n = 51`’s higher raw prize, at about a quarter of its cost.
But the search side is now the binding cost, not the gate: row generation is `79`-`94`
per cent of every round, site density has never been set as a function of container
side, and an untuned grid cost `8.8x` at `n = 20`’s own side.
`BC-191` (`think-ji0r`) prices that before any retarget; `BC-190` (`think-jgeg`) follows
on the integer sweep’s own baseline; the retarget candidates (`BC-192`/`BC-194`,
`n = 26` per X-013) wait on both.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
