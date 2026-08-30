---
title: session-047 — four facts about every claim, and the two the register was not recording
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-047
  primary_bead: think-xdly
  status: completed
  title: Make the assurance record say who established what
  date: '2026-08-30'
  started_at: '2026-08-30T16:30:00Z'
  deadline_at: '2026-08-30T21:03:00Z'
  goal: >-
    The register could always answer "is this proved?" and could not answer "is this ours?"
    -- not because the vocabulary was missing but because two of its fields were unused,
    unenforced, or carried a date where they promised a statement. This session was driven
    by the owner rather than by the agenda: five successive questions, each narrowing the
    last, ending at a rubric for `apparently-novel` and an inventory generated from it.
  budget:
    # Measured, not declared in advance: the phases below are timed from the commits they
    # produced, per D-358's rule to read a clock rather than estimate between tool calls.
    # Five work phases across 228 measured minutes, a mean of about 46, timed from the
    # commits they produced rather than estimated. The wall covers those plus the
    # finalization reserve. It is not a stop condition -- OR-8 exists because the previous
    # run invented a budget mid-flight and treated reaching it as permission to stop.
    wall_minutes: 273
    max_cycles: 8
    orientation_minutes: 5
    # The finalization phase is the reserve: recording a session is work, and a run that
    # leaves no time for it produces five phases nobody can reconstruct, which is how this
    # session reached its sixth phase with no record of the first five.
    finalization_minutes: 45
  workflow_phases:
  - workflow: general-improvement
    recording: contemporaneous
    clock_role: work
    focus: process
    commitment: BC-049
    bead: think-xdly
    objective: >-
      Answer why the previous run stopped twelve hours into an open-ended mandate, and make
      the answer structural rather than a resolution.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 50
    started_at: '2026-08-30T16:30:00Z'
    deadline_at: '2026-08-30T17:20:00Z'
    expected_output: >-
      A defect naming the cause, an operating rule, and a continuity device that does not
      depend on the agent choosing to re-arm it.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      A rule without a mechanism is the failure mode being fixed, so the mechanism is the
      deliverable and the rule is the explanation.
    fallback: >-
      The defect alone, if the trigger cannot be made recurring.
    outcome: >-
      `D-395`, a recurrence of `D-358`. The reminders worked: twenty-one self-written pings
      fired without a gap from 03:37Z to 15:21Z. The run then wrote itself one saying "the
      wall budget is spent... do not start new work" and deleted it. `OR-8` says a
      self-declared budget is not a stop condition; the mechanism is an hourly recurring
      trigger that fires whether or not the previous turn thought the work was finished,
      because a one-shot chain is only as long as the first turn that concludes it is done.
    evidence:
    - operating-rules.md
    - packing/defects.yaml
    - packing/devtools/check_session_rollups.py
    - packing/campaign/agent-sessions/README.md
    stop_reason: >-
      The mechanism is armed and does not depend on being re-armed.
    next_action: >-
      Nothing. The rule holds unless the owner ends the run.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-049
    bead: think-xdly
    objective: >-
      Promote the three sizes whose exact certificates were already running in the gate
      while their records declared a mathematics blocker, then close the class rather than
      the instance.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      Focus moves from process to correctness. The continuity work was about how the run
      behaves; this is about what the register says, and the two do not share a kill
      condition -- a wrong promotion is a false claim about the mathematics.
    budget_minutes: 95
    started_at: '2026-08-30T17:20:00Z'
    deadline_at: '2026-08-30T18:55:00Z'
    expected_output: >-
      n = 40, 65 and 89 citing Goebel's construction, and a sweep that runs from
      certificates toward records so the next one cannot land unrecorded.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --edit
    kill_condition: >-
      Feasibility decided exactly is an upper bound and not optimality; the promotion moves
      `verified_upper_bound` and nothing else.
    fallback: >-
      The promotion without the sweep.
    outcome: >-
      `D-398` fixed. The trailing-ceiling count falls 33 to 30.
      `devtools/check_certificate_citations.py` runs the other way and is a records-tier
      step: every `cases/*/verify_exact.py` declares `CERTIFIES` and each size must reach a
      verified evidence record citing that package, with an undeclared module a refusal
      rather than a skip. An adversarial pass then broke both new guards --
      `_check_rigidity_claim` had no catch-all, so a block with no assurance at all passed
      silently; the sweep crashed rather than refused on a non-literal declaration, taking
      every later package with it. Six tests, one per attack that landed.
    evidence:
    - packing/frontier/n-040.md
    - packing/frontier/n-065.md
    - packing/frontier/n-089.md
    - packing/frontier/evidence.yaml
    - packing/devtools/check_certificate_citations.py
    - packing/tests/test_certificate_citations.py
    - packing/src/sqpack/assurance.py
    stop_reason: >-
      The three promotions landed and the class check that would have caught them exists.
    next_action: >-
      The trailing-ceiling count of 30 is a tripwire in a test, not a check; a real one would sweep bounds the way this sweeps certificates.
  - workflow: factual-review
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-049
    bead: think-xdly
    objective: >-
      Test BC-049's typed refusal for n = 28 rather than accepting it.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      A sub-agent proposed closing `BC-049` on the n = 28 refusal. Testing a refusal is a
      different act from building against it, so the workflow moves to factual-review and
      the kill condition becomes what the retained precision can support.
    budget_minutes: 25
    started_at: '2026-08-30T18:55:00Z'
    deadline_at: '2026-08-30T19:20:00Z'
    expected_output: >-
      Either the refusal stands with a reason, or it does not and the route is open.
    validation_command: >-
      uv run --frozen --all-extras --group dev python -m devtools.price_exact_construction --check
    kill_condition: >-
      A measurement taken below the precision the record carries is a measurement of the
      materialisation, not of the pose.
    fallback: >-
      None; this is a question, not a build.
    outcome: >-
      The refusal STANDS, and the attempt to overturn it is `D-402`, direction flattering.
      Extraction appeared to give 32 pair contacts with nothing undecided and 41 decades of
      separation; the witness carries 57 fractional digits and the extraction ran at 200,
      classifying incidences at a floor of 1e-80. That decided the padding.
      `price_exact_construction` already measured this correctly at the witness's own
      digits plus a margin, reports 27, and its own prose warns of "windows on the
      materialisation's padding" -- a description of the mistake written before it was
      made. The calibration settles it: at n = 29, where the truth is known from a
      160-digit provenance artifact (52 and 37), the same route reports 17 and 36. CI
      caught it inside twenty minutes.
    evidence:
    - packing/campaign/agendas/agenda-005-symbolic-promotion-and-identity.md
    - packing/defects.yaml
    - packing/devtools/generate_contact_structures.py
    stop_reason: >-
      The claim was withdrawn as soon as CI showed the pricing artifact disagreeing with it.
    next_action: >-
      `extract_contacts` cannot know a pose was padded to reach the floor it was given; a guard comparing the requested floor against the witness's declared digits does not exist.
  - workflow: general-improvement
    recording: contemporaneous
    clock_role: work
    focus: process
    commitment: BC-049
    bead: think-xdly
    objective: >-
      Answer the owner's question -- what are the criteria, rather than whose judgement --
      for the three decisions this run had put to them.
    status: completed
    entered_by: user_request
    switch_reason: >-
      The owner rejected the framing: "It's not a judgment call for me. It's about what our
      policies are."
    budget_minutes: 25
    started_at: '2026-08-30T19:20:00Z'
    deadline_at: '2026-08-30T19:45:00Z'
    expected_output: >-
      Each decision resolved by an existing rule, or the missing rule written down.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --edit
    kill_condition: >-
      Writing a criterion is not the same as settling the question it rests on, and the
      licensing assessment underneath is the owner's.
    fallback: >-
      The two the contract already decides.
    outcome: >-
      Two of the three were already decided and I had not read the contract. n = 29's bound
      moves onto the interval certificate -- the method table says `interval-certified`
      supports `verified`, and "below exact-algebraic" and "unreviewed" are not criteria,
      independence being a separately recorded fact. The same rule decides the half I had
      backwards: the blocker STAYS, because without a shared `exact_form` the agreement
      rule allows half a unit and the certificate trails the report by 9.19e-15. n = 5
      stays `undetermined` because no method value covers a first-party unpublished prose
      argument. The third was genuinely unwritten: the retention policy is about dependence
      on the source, so a construction recomputed from a published rule is not under it and
      a re-encoded transcription still is -- checkable, since neither Goebel module imports
      a witness.
    evidence:
    - packing/frontier/n-029.md
    - packing/src/sqpack/known_best.py
    - SYNOPSIS.md
    stop_reason: >-
      Each of the three resolved by a rule, or the missing rule written where the policy lives.
    next_action: >-
      The licensing assessment the retention criterion assumes is the owner's and is untouched.
  - workflow: general-improvement
    recording: contemporaneous
    clock_role: work
    focus: process
    commitment: BC-049
    bead: think-xdly
    objective: >-
      Record, for every claim, whether anyone here has read the argument behind it and
      whether the result is ours -- then corroborate the novelty claims rather than
      asserting them.
    status: completed
    entered_by: user_request
    switch_reason: >-
      The owner asked for the four facts to be filled in accurately across the whole
      frontier. That is the same process focus as the previous phase but a wider object --
      the register rather than three decisions.
    budget_minutes: 33
    started_at: '2026-08-30T19:45:00Z'
    deadline_at: '2026-08-30T20:18:00Z'
    expected_output: >-
      The four facts complete across all 31 evidence records, enforced, and generated into
      a view a reader can use.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      `apparently-novel` obliges a documented search. Asserting one not performed is
      `D-402`'s error in a second costume.
    fallback: >-
      The fields and the enforcement, leaving the assessments unfilled and visible.
    outcome: >-
      `external_review` added and set on all six external proofs, all honestly
      `not-reviewed`; an external proof declaring no state is refused. `origin` filled on
      the three numerical records lacking it and is now complete. `novelty_basis` added --
      corpus, what was searched, what exactly is new, and the corpus's known holes --
      because the vocabulary calls this label "a statement about the search performed" and
      every claim carried only a date. Three sub-agents searched the archive: all four
      pre-existing claims are defensible and name the right object, and three rigidity
      findings are newly marked, the corpus asserting rigidity in four places while
      "second-order", "infinitesimal", "Farkas", "self-stress" and "tangent cone" return
      zero files. `frontier/INVENTORY.md` is generated and drift-checked, and measures
      what prose had asserted: `E-nagamochi-lower` carries the verified lower bound for 88
      of the hundred cases against 2 for the next, and is external and unread.
    evidence:
    - packing/frontier/evidence.yaml
    - packing/frontier/frontier-evidence.schema.yaml
    - packing/frontier/INVENTORY.md
    - packing/devtools/render_evidence_inventory.py
    - packing/src/sqpack/assurance.py
    - packing/tests/test_frontier_assurance_contract.py
    - README.md
    - SYNOPSIS.md
    stop_reason: >-
      The four facts are complete and enforced where completeness is honest, and
      visibly absent where it is not.
    next_action: >-
      Three records still make no novelty statement, correctly. The inventory names
      the highest-value unclaimed work: an informal review of `[Nagamochi 2005]`.
  - workflow: general-improvement
    recording: contemporaneous
    clock_role: finalization
    focus: process
    commitment: BC-049
    bead: think-xdly
    objective: >-
      Record this session while it is still running, and account for what it cost.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The clock role changes from work to finalization. Five phases of work had produced no
      session record at all, which the continuity floor surfaced on a check-in rather than
      anyone noticing at the time.
    budget_minutes: 45
    started_at: '2026-08-30T20:18:00Z'
    deadline_at: '2026-08-30T21:03:00Z'
    expected_output: >-
      This record, with phase clocks read from the commits that produced them, and rollups
      for the session log and the twelve sub-agent logs it spawned.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      A session record written after the fact is a reconstruction, and the schema refuses a
      phase that starts later than the record of it -- D-358's guard, which caught this one
      dating a phase into the future on the first attempt.
    fallback: >-
      The rollups alone; they are the part that cannot be reconstructed once the harness
      log is gone.
    outcome: >-
      The rollups are written: the session log at 18330 records, 6106 turns
      and 3416 tool calls over 35.88 hours, and twelve sub-agent logs beside it. One number
      in that rollup is worth reading against OR-1 rather than filing -- 954 of the tool
      calls are one-off code, and 718 are Python heredocs, in a session whose first
      operating rule says never leave a measurement in one-off code.
    evidence:
    - packing/campaign/agent-sessions/session-047-assurance-structure-and-what-is-ours.md
    - packing/campaign/resource-usage/3930e045-47fc-5947-8bf6-0c92155bcd88.yaml
    - SYNOPSIS.md
    stop_reason: >-
      The record exists, the rollups are written, and PR #63's description was rewritten to
      match the branch rather than the half of it that predates this session.
    next_action: >-
      The recognition sweep this record's next_action names.
  stop_conditions:
  - >-
    `apparently-novel` obliges a documented search. No record gets the label on an
    assertion, and a record whose search has not been run keeps saying nothing -- absence
    is a legitimate state and the inventory displays it rather than hiding it.
  - >-
    Adding a field is not the same as filling it honestly. `external_review` on all six
    external proofs reads `not-reviewed`, because that is what is true; the point of the
    field is to make that visible, not to make it look better.
  - >-
    Nothing is pushed without the affected tests run directly. `--edit` does not run them
    (D-381, D-393), and exit status is read from a redirect rather than off the end of a
    pipeline -- a `| tail` reports tail's code, which cost a red push earlier in this run.
  progress:
    metric: >-
      Facts stated per evidence record, across the four that decide whether a claim is
      ours: assurance, method, origin with external_review, and novelty with its basis.
    before: >-
      31 records. `external_review` did not exist, so a transcribed citation and an
      examined argument were indistinguishable. Three records had no `origin`. Six made no
      novelty statement, and the four that did carried a date where the vocabulary promises
      a statement about a search.
    after: >-
      `external_review` and `origin` complete and enforced. Seven records marked
      `apparently-novel`, every one with a corpus, a search, a named novel object and that
      corpus's known holes. Three still say nothing, correctly.
  # Twelve sub-agents ran read-only investigations. They are not tracked delegations:
  # each is a separate harness log with its own rollup below, attributed by span, and what
  # each produced is in the phase outcome it fed. Six produced findings acted on; two
  # repeated the PEP 758 misreading recorded as D-397, and one placed a real quote in the
  # wrong file. Every load-bearing claim was reproduced before use, which is how the
  # misplacement surfaced.
  delegations: []
  outputs: []
  checks: []
  # The session's own log, then the twelve sub-agent logs this block spawned. Sub-agent
  # transcripts are separate logs, so they are separate records rather than folded in.
  resource_rollups:
  - packing/campaign/resource-usage/3930e045-47fc-5947-8bf6-0c92155bcd88.yaml
  - packing/campaign/resource-usage/agent-a235d6deb195e96a2.yaml
  - packing/campaign/resource-usage/agent-a3fd26ebd6591bf06.yaml
  - packing/campaign/resource-usage/agent-a5c087adf65f78ac2.yaml
  - packing/campaign/resource-usage/agent-a73154b1e2f2a487f.yaml
  - packing/campaign/resource-usage/agent-a95a72c7deadc0ffd.yaml
  - packing/campaign/resource-usage/agent-aa4fe4753eb034678.yaml
  - packing/campaign/resource-usage/agent-aabe2b6ddd3e6be41.yaml
  - packing/campaign/resource-usage/agent-aacef4331c8666e1e.yaml
  - packing/campaign/resource-usage/agent-aae611a3917f04561.yaml
  - packing/campaign/resource-usage/agent-ade870588ae0888a1.yaml
  - packing/campaign/resource-usage/agent-aef07d923ca86729c.yaml
  - packing/campaign/resource-usage/agent-af6005e953cb04f35.yaml
  stop_reason: >-
    The block is complete and closed here rather than left open with a rolling deadline: an
    in-progress session whose deadline has passed is a refusable state, and rolling it
    forward to stay inside the gate would be the bookkeeping D-358 records.
  next_action: >-
    `BC-049` stays open and this session did not touch its mathematics. Three evidence
    records still make no novelty statement and should keep making none
    until someone searches: `E-migrated-lower-report`, whose provenance is
    `unknown-historical`, and the two n = 29 numerical checks. The inventory's own
    arithmetic names the highest-value unclaimed work -- an informal review of
    `[Nagamochi 2005]`, which 88 cases rest on and nobody here has read (`think-xdly`).
---
# Session-047 — Four Facts About Every Claim

The register has always been able to say whether something is proved.
It could not say whether it is *ours*, and the reason was not a missing idea.

Two fields already existed to carry that.
One had never been used, so a transcribed citation and an argument someone here had
worked through were the same record.
The other promised “a statement about the search performed” and held a date.

This session filled both, enforced both, and generated a view from them.
It also spent forty-five minutes producing a result that was an artifact of its own
measurement, which is [`D-402`](../../../defects.md) and the reason the last phase
refused to assert a search it had not run.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
