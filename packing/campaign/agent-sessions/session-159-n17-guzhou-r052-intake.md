---
title: "Session 159 — Intake of Guzhou0806's R052 certificate for s(17) > 231001/50000"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-159
  title: Intake of Guzhou0806's R052 Certificate for s(17) > 231001/50000
  date: '2026-09-25'
  started_at: '2026-09-25T08:00:00Z'
  deadline_at: '2026-09-25T16:00:00Z'
  branch: claude/n17-guzhou-r052-intake
  primary_bead: think-ju2h
  status: stopped
  certification_pending: think-tdfj
  ended_at: '2026-09-25T09:25:00Z'
  goal: >-
    Decide whether Guzhou0806's R052 certificate for s(17) > 231001/50000 is correct,
    retain it at its pinned commit with its credits, fact-check the public n = 17 record
    it claims to lead (Kleddamag's public 461300/99853, the unpublished 4.62001 the source
    mentions, and the R042, R043 and R050 certificates and ahyangyi/17squares not yet in
    the record), and register the result at the level epistemics.md derives.
  workflow_phases:
  - workflow: factual-review
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      Retain the source at its pinned commit, replay R052 with its own verifier and with
      this repository's independent route, review its proof with Fable max, and record
      the other public n = 17 claims it is compared against.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 360
    started_at: '2026-09-25T08:00:00Z'
    deadline_at: '2026-09-25T14:00:00Z'
    expected_output: >-
      A retained source packet with receipts, a dated review, a register decision derived
      from epistemics.md, and n-017.md, README and SYNOPSIS updated with credits.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: A replay fails or the review finds a gap the certificate does not close.
    fallback: Record R052 as reported but unverified, with the finding, and stop.
    outcome: >-
      All four of R052's replay modes passed here, both full sweeps reproducing the
      source's row ledgers exactly, and a Fable max review found no mathematical defect.
      The native interval route accepts every exact premise but refuses coverage at its
      engine ceilings, so R052 is the verified n = 17 lower bound at V4/C3, as Kleddamag's
      was. R042, R043 and R050 are retained as publication records and ahyangyi/17squares
      is recorded as a reported source; the source's unpublished-4.62001 report is not a
      rung.
    evidence:
    - docs/project/reviews/review-2026-09-25-n17-guzhou-r052.md
    - packing/resources/web/n17-guzhou-r052-2026-09-25/README.md
    - packing/frontier/n-017.md
    stop_reason: R052 is registered with its credits and every source replay passed.
    next_action: Run the planning block the owner asked for after the integration.
  - workflow: review-planning-oversight
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: >-
      BC-385: decide what R052 and the closed rung 0 make possible at n = 11 and n = 17,
      from two Fable max assessments, and select bounded next work.
    status: stopped
    entered_by: user_request
    switch_reason: >-
      The owner asked for an extra planning session on further improvements given the
      new n = 11 and n = 17 results.
    budget_minutes: 150
    started_at: '2026-09-25T08:50:00Z'
    deadline_at: '2026-09-25T11:20:00Z'
    expected_output: >-
      A plan document, registered H-items, agenda-042 items with beads, idea-board rows
      and one selected next entry.
    validation_command: >-
      cd packing && uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The assessments find nothing worth a bounded commitment.
    fallback: Record the assessment and keep BC-384 as the next entry.
    outcome: >-
      Two Fable max assessments were reconciled into a plan. At n = 17 R052's certificate
      is nearly saturated, so a first-party increment is not worth building, and an
      unreviewed capacity-one lemma makes the architecture's ceiling a cheap search; at
      n = 11 the separating-axis LP reaches any target until about twenty pairs are
      fixed, so the per-node bound must be a counting bound. BC-386 to BC-391 and H-243
      to H-247 are registered, BC-384 is blocked on BC-388 and BC-389, and BC-386 leads
      the next session's order of work.
    evidence:
    - docs/project/specs/active/plan-2026-09-25-after-r052-planning.md
    - packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md
    stop_reason: The planning records are landed and the next entry is selected.
    next_action: >-
      Close the session with certification pending on one hosted gate.
  budget:
    wall_minutes: 480
    slice_minutes: 240
    finalization_minutes: 90
  stop_conditions:
  - The owner ends the run; a self-declared budget is not a stop condition (OR-8).
  - No register entry without the Fable max review and an epistemics.md derivation.
  - Archived source material is retained byte-for-byte and never edited.
  progress:
    metric: R052 verdict, register decision and the public n = 17 record fact-checked.
    before: >-
      The verified n = 17 lower bound is Kleddamag's 461300/99853, at V4/C3 by source
      replay; R042, R043, R050, R052 and ahyangyi/17squares are not in the record.
    after: >-
      R052's s(17) > 231001/50000 is the verified n = 17 lower bound at V4/C3 with its
      credits; the public n = 17 record is fact-checked; and a planning block has
      selected six bounded commitments for n = 11, n = 12, n = 17 and n = 21.
  resource_rollups:
  - packing/campaign/resource-usage/e8d698c4-206a-4921-bcc4-4f7e12fa474f.yaml
  - packing/campaign/resource-usage/agent-a14838e74b93e7722.yaml
  - packing/campaign/resource-usage/agent-a5b2f63f330c0def9.yaml
  - packing/campaign/resource-usage/agent-a990900e039ea518c.yaml
  - packing/campaign/resource-usage/agent-a4228d717a68a4701.yaml
  - packing/campaign/resource-usage/agent-a567ff1432f455da2.yaml
  - packing/campaign/resource-usage/agent-a86c3b35a080e2b9f.yaml
  delegations: []
  outputs:
  - docs/project/reviews/review-2026-09-25-n17-guzhou-r052.md
  - packing/resources/web/n17-guzhou-r052-2026-09-25/README.md
  - packing/devtools/verify_guzhou_r052_native.py
  - packing/frontier/n-017.md
  - packing/frontier/evidence.yaml
  - docs/project/specs/active/plan-2026-09-25-after-r052-planning.md
  - packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md
  checks:
  - All four R052 source replay modes passed (records, containment, Python full, Node/BigInt full).
  - The native R052 tool's 19 tests pass; its coverage engine refuses at the frozen ceilings.
  - check_results passes all 36 registered results.
  - packing-validate --records passed on the closed records.
  stop_reason: >-
    The owner's two requests reached their exits: R052 is integrated with its credits
    and fact-check, and the planning block selected the next work. One hosted full gate
    remains.
  next_action: >-
    BC-386 (think-amx8): lift the native coverage ceilings and decide R052 natively, the
    first lane of the after-R052 order, with the n11 tilt-profile census and the ceiling
    search beside it; think-tdfj certifies this head with one hosted full gate.
---
# Intake of Guzhou0806’s R052 Certificate

On 2026-09-25 Guzhou0806 published R052, a strict lower-bound certificate for
$s(17) > 231001/50000 = 4.62002$ that extends Kleddamag’s public mixed-certificate
architecture. The owner asked for it to be integrated with its credits after a
fact-checking pass. This session retains the source, replays the certificate twice, has
Fable max review the argument, and registers whatever the evidence supports.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
