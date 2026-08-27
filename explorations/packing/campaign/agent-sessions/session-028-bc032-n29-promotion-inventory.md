---
title: session-028 — resumed BC-032 n=29 promotion inventory
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-028
  title: Execute the carried-forward BC-032 n=29 promotion inventory
  date: '2026-08-27'
  started_at: '2026-08-27T08:30:00-07:00'
  deadline_at: '2026-08-27T09:30:00-07:00'
  goal: >-
    Reach a terminal disposition on session 027's unexecuted phase 11 contract: either
    preregister one falsifiable exact-or-interval BC-032 promotion question with named
    inputs, checker, and accept rule, or retain the first typed source, contact,
    isolation, or checker blocker that prevents an honest n=29 round.
  workflow_phases:
  - workflow: insight-iteration
    recording: contemporaneous
    clock_role: work
    focus: correctness
    objective: >-
      Select or reject one bounded BC-032 n=29 exact-or-interval promotion slice by
      inventorying the concrete witness, contact system, isolation boxes, certificate
      contract, and independent checker already present in the repository.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-08-27T08:30:00-07:00'
    deadline_at: '2026-08-27T09:00:00-07:00'
    expected_output: >-
      One falsifiable exact or outward-rounded interval question with named inputs,
      checker, and accept rule, or the first typed source/contact/isolation/checker
      blocker that prevents an honest n=29 round.
    validation_command: >-
      uv run --directory explorations/packing --frozen packing-validate --list
    kill_condition: >-
      Stop on higher decimal precision plus tolerance, inferred contacts, unbounded
      generic interval work, record-improvement/rigidity/optimality language, generated
      geometry transfer, n=11 promotion, a long gate, hosted CI poll, or hash ceremony.
    fallback: >-
      Retain the exact missing prerequisite under think-75ll and enter W7 only for a
      source/contact/checker inventory or typed blocker, not a numerical solve.
    outcome: >-
      Rejected the slice as specified and preregistered a different, smaller question.
      The three inventories agree that BC-032's stated n=29 prerequisites do not describe
      the repository: the exact-or-interval promotion boundary has already been crossed by
      a stronger route, recorded and gated as `E-n029-schadt-rational-upper`, so no
      interval round is required for the n=29 upper bound. Of the four named prerequisites
      the independent checker already exists and is gated, and contact equations, isolation
      boxes, and an outward-rounded certificate type are unnecessary for that route rather
      than merely unbuilt. Q-BC032-a is preregistered in their place. No numerical solve,
      promotion run, or certificate generation was performed in this slice.
    evidence:
    - >-
      Inventory A. The n=29 source witness is complete and retained. `witnesses/schadt-n029-2025-decimal.yaml`
      holds 29 center-angle squares at side 5.933885799813025878636..., assurance `reported`,
      method `numerical-multiprecision`, precision 300 digits, tolerance `1e-100`, imported by
      `cases/schadt29/import_witness.py` from the Schadt repository retrieved 2026-08-25. Its
      source values carry about six decimals padded to 105 digits; the padding is presentational
      and carries no information.
    - >-
      Inventory A. The retained record already types the pose as infeasible-as-printed: thirteen
      best pair gaps are negative, the worst about -8.81e-102, and they are admitted only by the
      declared tolerance. Replaying the declared numerical check reports `NUMERIC CHECK PASSED - not
      verification` and states that a 1e-100 tolerance does not establish exact feasibility.
    - >-
      Inventory B. No n=29 contact system exists. `contact_assembly`, `contact_full_cell`,
      `contact_full_cell_execution`, and `contact_realization` are the small-n structural
      enumeration lane and carry no n=29 contact graph, contact equations, or isolation boxes.
      No isolation boxes exist at any n; SYNOPSIS lists the `PoseBox` scalar and the interval
      branch-and-bound hook as deliberately unbuilt.
    - >-
      Inventory C. The independent exact checker exists and is already gated.
      `devtools/check_rational_witness_independent.py` shares no geometry or verification code with
      `sqpack.witness` or `sqpack.verify` by construction, and `packing-validate` runs it on both the
      n=11 control and the n=29 rational witness. Run read-only here it reports VERIFIED over 29
      squares and all 406 pairs in 0.23 seconds.
    - >-
      Inventory C. Exact rational feasibility at n=29 is established, not open. Every one of the 29
      squares has all four edges of exactly unit squared length over Q, the exact minimum pair gap is
      strictly positive at about 9.9998e-12, and the exact side is
      296694289993118242899906513/50000000000000000000000000, about 4.94e-11 above the source decimal
      side. `E-n029-schadt-rational-upper` records this as assurance `verified`, method
      `exact-algebraic`, novelty `apparently-novel`, with a passing replay.
    - >-
      Inventory C. The interval route is separately and honestly blocked: `packing-witness promote
      --strategy interval-existence` raises `_interval_not_built()`, so an interval round could not
      be run today even if it were the right question.
    - >-
      Comparison. `promote_rational` selects the first rung of a hardcoded dilation ladder
      `[1, 1+10^-e ...]` over `e = max(2, rational_digits-5)` descending by two that both verifies and
      stays inside the allowed relaxation. The achieved 4.94e-11 is therefore the first admissible rung
      at the default `rational_digits = 36`, not a measured minimum, which is what makes Q-BC032-a
      falsifiable with the instruments already present.
    stop_reason: >-
      Three read-only inventories converged on the same disposition well inside the
      30-minute ceiling: the declared slice rests on prerequisites that the repository
      does not need, and the smallest genuinely open question is different and cheaper.
      Preregistration, not execution, is this phase's contract.
    next_action: >-
      Register Q-BC032-a as a W6 mini-cycle under think-75ll with its declared
      `rational_digits` set fixed before the first run, and correct BC-032's stale
      `next_evidence` in agenda-003.
  primary_bead: think-75ll
  status: completed
  budget:
    wall_minutes: 60
    slice_minutes: 30
    finalization_minutes: 10
  stop_conditions:
  - The absolute deadline 2026-08-27T09:30:00-07:00 is reached.
  - At 2026-08-27T09:20:00-07:00, stop target work and use only the finalization reserve.
  - No phase may run for more than 30 minutes without terminal evidence and a newly declared slice.
  - No n=29 numerical solve, interval round, or certificate generation begins from this inventory slice.
  - Decimal precision is never treated as a certificate, and no contact is inferred from a figure or a coordinate list.
  - No exp-045 scientific disposition is written by this session; its stale lease is surfaced, not resolved.
  progress:
    metric: BC-032 n=29 promotion readiness reduced to either one preregistered falsifiable question or one typed blocker
    before: >-
      Session 027 declared this contract at 2026-08-27T03:52:00-07:00 and stopped nine
      minutes later on a provider usage limit without executing it. BC-032's registered
      rounds are complete through the n=11 robust-rational control, which validates only
      the already-built exactification path at a relaxed side. No n=29 contact equations,
      isolation boxes, certificate type, or independent checker have been written.
    after: >-
      The slice is terminal and the readiness question is answered in the negative: the
      declared n=29 prerequisites do not describe this repository, and the promotion
      boundary they guard has already been crossed by a stronger, gated route. One
      falsifiable question, Q-BC032-a, is preregistered with named inputs, an existing
      independent checker, an accept rule, and a single-witness falsifier, and BC-032's
      stale `next_evidence` is corrected. No n=29 numerical work was run and no claim
      widened.
  delegations: []
  outputs:
  - campaign/agendas/agenda-003-balanced-ten-hour-research-program.md
  - campaign/agent-sessions/session-028-bc032-n29-promotion-inventory.md
  checks:
  - Session 027 is terminal and its stopped disposition is committed and pushed.
  - The worktree is clean at session start except for the known stale exp-045 lease.
  - Read-only replay of the independent exact checker on the n=29 rational witness returned VERIFIED over 406 pairs.
  - Read-only replay of the declared numerical check on the n=29 decimal witness returned NUMERIC CHECK PASSED - not verification.
  - No promotion run, certificate generation, or witness file write was performed.
  - The exp-045 stale lease is carried out of this session undecided and is recorded below as an open item.
  stop_reason: >-
    The declared inventory reached a terminal disposition inside its slice: the phase
    contract was rejected on evidence and replaced by one preregistered falsifiable
    question, with the stale agenda text corrected. Executing Q-BC032-a belongs to a
    registered W6 mini-cycle, not to this W3 slice.
  next_action: >-
    Under BC-032 and think-75ll, register Q-BC032-a as a W6 mini-cycle with its
    `rational_digits` set declared before the first run and the existing independent
    exact checker as its sole acceptance instrument.
---
# Session 028 — Resumed BC-032 n = 29 Promotion Inventory

This session carries forward the single unexecuted phase of
[session 027](session-027-balanced-research-session-b.md), which stopped on an external
provider usage limit before its BC-032 slice began.
The phase contract is reused verbatim rather than restated, so the declaration remains
the one made before any of this work was seen.

## Bounded Slot Plan

| Slot | Minutes | Workflow | Bead | Intent |
| --- | ---: | --- | --- | --- |
| 8:30–9:00 | 30 | W3 insight-iteration | think-75ll | Three independent read-only inventories over the n=29 witness, contact assets, and interval/checker infrastructure; then one disposition. |
| 9:00–9:20 | 20 | reserve | think-75ll | Record the disposition and any typed blocker. |
| 9:20–9:30 | 10 | finalization | think-75ll | Terminalize, regenerate shared views, run proportional gates, commit and push. |

## Preregistered question Q-BC032-a

**Question.** Is the `4.94e-11` side relaxation in `E-n029-schadt-rational-upper` a
property of the retained Schadt pose, or an artifact of `promote_rational`’s fixed
dilation ladder at the default `rational_digits = 36`?

**Why this and not the agenda’s question.** BC-032 asks for the smallest well-posed
system that can test the next exact-or-interval promotion boundary *without pretending
that more decimal precision is a certificate*. At `n = 29` that boundary is already
crossed: the exact rational upper bound is `verified`, and the interval route is both
unnecessary for it and blocked by a declared unbuilt instrument.
What remains open is not the boundary but the size of the relaxation paid to reach it,
and that is a tool-validation question the existing instruments can decide.

**Inputs.** `witnesses/schadt-n029-2025-decimal.yaml`, unchanged;
`packing-witness promote --strategy robust-rational --rational-digits d` over a finite
set of `d` fixed and recorded before the first run; the existing `--max-side-increase`
bound.

**Checker.** `devtools/check_rational_witness_independent.py`, which shares no geometry
or verification code with the promotion path and is already gated in `packing-validate`.

**Accept rule.** The relaxation is *route-dependent* if at least one declared `d` yields
an independently verified 29-square rational witness whose exact side is strictly less
than `296694289993118242899906513/50000000000000000000000000`. It is *route-independent
on this ladder* if no declared `d` does.

**Falsifier.** A single independently verified witness at a strictly smaller exact side.

**Claim boundary.** Any smaller certified side remains an upper bound on the true
`n = 29` optimum and a weaker bound than the reported record.
No answer certifies the source decimals, improves a record, establishes rigidity, or
proves optimality.
A negative answer is a real result about the promotion tool, not about
the packing.

**Cost.** One sub-second promotion and one 0.23-second independent check per declared
`d`.

## What the n = 29 case measures

The retained records already quantify the campaign’s standing warning about decimal
precision, though no document had yet stated it as one number.
The source pose is admitted only by a `1e-100` tolerance that masks a worst best-pair
gap of about `-8.81e-102`, while genuine exact feasibility requires about `4.94e-11` of
extra container side.
Those two scales differ by roughly ninety-one orders of magnitude, so no amount of added
decimal precision on the source side converts that pose into a certificate.

## Open item carried out of this session

`exp-045` is `in_progress` with a lease that expired at `2026-08-27T03:18:23-07:00`, so
`packing-ledger check` reports it as a stale claim.
This session deliberately did not resolve it.
The two admissible dispositions are to renew the lease under an active slice that is
actually executing the experiment, or to record the `blocked` verdict its own execution
admission section already describes.
Either is a scientific disposition on H-023 and belongs to the runner that owns that
lane, not to an unrelated BC-032 inventory.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
