---
title: agenda-041 — a deep low-n review, an efficiency block, and the first-party n = 17 question
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-041
  title: A Deep Low-n Review, an Efficiency Block, and the First-Party n = 17 Question
  updated: '2026-09-22'
  status: active
  objective: >-
    Spend one four-hour run on three blocks in sequence, overlapped so that no gate is
    waited on idle. A deep mathematical review on Fable asks whether anything
    significant is left at n = 11, n = 17 or another low n now that the five-value
    n = 17 ladder and the T-031 and T-032 registrations have merged; it runs as four
    disjoint lanes and lands as X-042. An efficiency block runs beside it, because
    OR-12 is seventeen terminal blocks overdue and because a fresh clone of this
    repository turned out not to run the research loop at all. The remaining time is an
    Opus research block on what the review ranks, with Fable taking the mathematics. The
    flagship is X-041's A2 cell: whether the external n = 17 measure also verifies
    unrestricted, in this repository's own language and its own gate, which is the one
    available move that would turn a retained external artifact into a first-party bound.
  items:
  - id: BC-368
    purpose: tool_validation
    owner_focus: efficiency
    instances: [11, 17]
    state: complete
    priority: 0
    question: >-
      Does the research loop actually run in a fresh remote-session clone, and if not,
      what is missing and where should the answer live so the next session does not
      rediscover it?
    budget: >-
      About forty minutes inside the efficiency block, overlapped with the review lanes.
      Repair first, then a guarded check, then the documentation, then one --edit tier to
      prove the repair.
    entry: >-
      A fresh clone on a remote session, with no venv and no node modules.
    exit: >-
      packing-validate --edit exits 0 from a clean clone after a documented sequence, and
      a guarded check reports each missing precondition with its remedy rather than
      leaving the next agent to read a build error.
    bead: think-zmos
    depends_on: []
    next_evidence: >-
      The bootstrap receipt under results/agenda-041 and the new devtools check.
    workflows: [efficiency-loop]
    program: n11-strategy-reset
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-041/bootstrap-receipt.md
    - packing/devtools/check_bootstrap.py
    parallel_group: efficiency
    note: >-
      Unplanned. It was found by running the loop rather than by reasoning about it, which
      is the whole argument for opening a block by measuring it.
    outcomes:
    - scope: Five preconditions no document named, found by running the edit tier on a fresh clone.
      classification: achieved
      result: >-
        The image ships uv 0.8.17, whose interpreter index ends at cpython-3.14.0rc2, so
        the pinned 3.14.7 cannot install and uv sync fails; uv self update does not fix it
        because it hits a GitHub API rate limit, and a direct install of 0.12.17 does. The
        clone is shallow, which fails the provenance step. The vendor/kpress submodule is
        absent, which fails uv sync. npm ci has not run, which fails the browser floor.
        After all five, the edit tier passes at 124.4 s of wall against its 240 s ceiling.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-041/bootstrap-receipt.md
      disposition: retire-success
      follow_up: null
  - id: BC-369
    purpose: tool_validation
    owner_focus: efficiency
    instances: [11, 17]
    state: in_progress
    priority: 1
    question: >-
      The deep gate costs about 45 minutes of wall and its exhaustive tier runs at 1.376x
      its own declared price, and no drift rule clocks a CI job at all. What does it cost
      to put the four CI jobs under the same register that already clocks the local tiers?
    budget: >-
      About an hour, analysis and configuration only. The deep gate is not run: the
      measurement it would take already exists on think-zmos from two complete runs of
      PR 208 at one tree.
    entry: >-
      think-zmos carries the measurement, and OR-17 has given every routine gate a wall
      ceiling to be measured against.
    exit: >-
      The four deep-gate jobs are clocked by a stated band with its reasoning in the
      register's own comments, or the lane says why a hosted runner's wall cannot carry
      the local rule.
    bead: think-zmos
    depends_on: [BC-368]
    next_evidence: >-
      The CI-budget receipt under results/agenda-041.
    workflows: [efficiency-loop]
    program: n11-strategy-reset
    parallel_group: efficiency
    note: >-
      OR-12 is overdue by the record's own count: the last session declaring
      workflow efficiency-loop is Session 131 on 2026-09-14, and seventeen terminal blocks
      have closed since against a ceiling of eight.
  - id: BC-370
    purpose: research
    owner_focus: insight
    instances: [11, 17, 18]
    state: in_progress
    priority: 0
    question: >-
      With the n = 17 ladder merged and T-031 and T-032 registered, is there a
      significant improvement still available at n = 11, n = 17 or another low n, and
      which mechanism carries it?
    budget: >-
      Four Fable lanes with disjoint deliverables, about fifty minutes, read-only against
      the record. One lane per question: the n = 11 one-body ceiling and what provably
      escapes it; the n = 17 measure and where the remaining gap lives; the cross-n
      integer plateaus and the integer-endpoint argument; and the upper-bound and search
      side, which no lower-bound lane covers.
    entry: >-
      X-040 and X-041 are retained, the five-value ladder is decomposed, and main carries
      T-032.
    exit: >-
      X-042 states a ranked slate with each item's mechanism, instrument, first
      discriminator and kill rule, and registers the falsifiable hypotheses the research
      block then runs. Arithmetic that does not reproduce is reported as a finding.
    bead: think-gvlg
    depends_on: []
    next_evidence: >-
      packing/campaign/explorations/X-042 and the hypotheses it registers.
    workflows: [insight-iteration, factual-review]
    program: n11-strategy-reset
    artifacts:
    - packing/campaign/explorations/X-041-after-the-n17-certified-bound.md
    - packing/campaign/explorations/X-040-lower-bound-mechanisms-beyond-the-one-body-ceiling.md
    parallel_group: review
    note: >-
      The mathematics is on Fable by OR-2. Each lane is asked for its own arithmetic
      recomputation of the numbers it relies on, because a review that only reads the
      record inherits the record's errors.
  - id: BC-371
    purpose: research
    owner_focus: insight
    instances: [17]
    state: in_progress
    priority: 0
    question: >-
      Does the external n = 17 measure, which is stated in a restricted parent-centre
      language this repository does not implement, also verify unrestricted as a plain
      threshold certificate in this repository's schema and its own two-route gate?
    budget: >-
      The research block's flagship lane. A guarded translator, then its controls, then
      the quick interval route, and the full two-route decision only if the quick route
      does not reject.
    entry: >-
      The artifact is retained under packing/resources/web with a byte-level manifest and
      a proof review, and its global-certificate.json carries 1134 point orbits, 253
      threshold orbits and 7853 rows in readable exact form.
    exit: >-
      Either a first-party threshold certificate that both routes accept, which would be
      an s(17) movement of about +0.0067 over T-032, or a refusal with its least charge
      and binding direction, which measures what the parent-centre restriction carries.
      A translation that cannot reproduce the artifact's own stated minimum decides
      nothing and is reported as a failed control, not as a bound.
    bead: think-xdoh
    depends_on: []
    next_evidence: >-
      exp-221 under results/agenda-041 and the translator under devtools.
    workflows: [research-loop]
    program: n11-strategy-reset
    artifacts:
    - packing/resources/web/n17-kleddamag-certified-bound-2026-09-21/kleddamag-17-squares-certified-bound/global-certificate.json
    parallel_group: research
    note: >-
      X-041 ranks this A2 and states the control that makes a negative trustworthy: the
      artifact's own minimum of 1000020517 units must be reproduced from the translated
      sites before any unrestricted verdict is believed. A clean negative is a full
      result for this cell.
  - id: BC-372
    purpose: research
    owner_focus: insight
    instances: [17]
    state: in_progress
    priority: 2
    question: >-
      Can this repository's own site sets cover at the external side L = 4613/1000 at all,
      and at which shrink do they stop?
    budget: >-
      A background sweep in a spare CPU slot, three shrinks on the 181-direction net at
      60 rounds and a 1200 s deadline each, seeded from the retained n = 17 certificate
      with a five-per-window lattice.
    entry: >-
      The stock column generator runs, verified by a 47 s smoke at 12 rounds.
    exit: >-
      Each shrink reports converged below 17, locked, or round-limited, with its least
      covered mass; the series says whether our support reaches the external side.
    bead: think-xdoh
    depends_on: []
    next_evidence: >-
      The sweep receipt under results/agenda-041.
    workflows: [research-loop]
    program: n11-strategy-reset
    parallel_group: research
    note: >-
      This is X-041's A1 cell run on our own support rather than the artifact's, which is
      the part of it that needs no translation. The register records our sites reaching
      only 17.195968 unconverged at 461/100, so a negative here is expected and its
      margin is the number wanted.
  - id: BC-373
    purpose: research
    owner_focus: insight
    instances: [11]
    state: complete
    priority: 2
    question: >-
      Does T-026's threshold family still decide at the 2880-step net, and what does the
      finer net buy over the 1440-step record?
    budget: >-
      A background rung in a spare CPU slot on two workers, nets 1440 and 2880 so the
      coarser net's failing shrink brackets the finer one's bisection.
    entry: >-
      The 1440-step record is retained and the refinement instrument runs.
    exit: >-
      A least charge at the 2880-step net against M/11, and either a bound movement or a
      statement of how much of the series' remaining 0.0011 the net buys.
    bead: think-gvlg
    depends_on: []
    next_evidence: >-
      The refinement work file and its receipt under results/agenda-041.
    workflows: [research-loop]
    program: n11-strategy-reset
    parallel_group: research
    note: >-
      X-041 calls this a rung rather than a mechanism and says to run it in an idle CPU
      slot and never as a block. That is exactly how it is run here.
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-041/exp-226-n11-net2880-receipt.md
    - packing/frontier/results.yaml
    - packing/frontier/evidence.yaml
    outcomes:
    - scope: T-026 threshold refinement from the retained 1440-step net to 2880 steps.
      classification: achieved
      result: >-
        The 2880-step certificate is retained as T-033 at the exact value
        3.826997548829543624. It improves the first-party fixed-core rung but remains
        below the independently verified strict external bound s(11) > 31/8; the
        unchanged fixed-core family has ceiling 955000/249507, so finer net refinement
        alone cannot recover that gap.
      evidence:
      - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-041/exp-226-n11-net2880-receipt.md
      - packing/frontier/results.yaml
      disposition: retire-success
      follow_up: think-vx26
---
# agenda-041: A Deep Low-n Review, an Efficiency Block, and the First-Party `n = 17` Question

The entry point is **W3 insight-iteration**, because the input is a merged record and an
open question about what is left in it, and the exit is a ranked slate with registered
hypotheses. It moves to **W5 efficiency-loop** for `BC-368` and `BC-369`, which run
beside the review rather than after it, and to **W6 research-loop** for the cells the
review ranks.

## Why these three blocks, in this order

`OR-12` is overdue and the record says by how much: the last session declaring
`workflow: efficiency-loop` is Session 131 on 2026-09-14, and seventeen terminal blocks
have closed since, against a ceiling of eight.
`think-zmos` was selected as the next entry by Session 150 and not run.

The review is first because the last one predates two registrations.
`X-041` ranked its slate against `main` at `9fe9999d`; `T-031`, `T-032` and the
Kleddamag retention have landed since, and the ladder it decomposed has a fifth value on
it.

The research block is last because its dispatch depends on the review, with one
exception.
`X-041`’s Tier A is already reviewed, so `BC-371`, `BC-372` and `BC-373` start
during the review rather than after it.
`OR-3` is the rule: never wait on a gate with nothing else in flight.

## What the efficiency block found by running rather than reasoning

`BC-368` was not planned.
It exists because the first command of the session was the edit tier and the edit tier
failed three steps, and because none of the five causes is written down anywhere a next
agent would look. The full sequence is in the receipt; the short version is that a fresh
remote-session clone has an interpreter it cannot install, a history it cannot read, a
submodule it does not have and a node tree it has not built.

The measurement that matters for `OR-14` is the one after the repair: **124.4 s of wall
against a 240 s ceiling**, which is 52% of the tier’s budget and inside its band.

## The flagship, and what would make its negative worth as much as its positive

`BC-371` is the one cell on the slate that could convert a retained external artifact
into a first-party bound.
The registered value is `T-032`’s `461300/99999 = 4.613046`; the artifact claims
`461300/99853 = 4.619791` in a restricted parent-centre language this repository does
not implement, which is why it is retained at `V4/C3` and registered by nothing.

The cell is worth running in both directions, and `X-041` says why.
An unrestricted covering below 17 implies a restricted one, so a pass hands over a
first-party certificate in this repository’s own gate.
A fail measures, by its least charge, what the restriction carries — which is the number
nobody has.

What makes the negative trustworthy is the control, and it is stated before the run
rather than after it: the translated sites must reproduce the artifact’s own stated
minimum of `1,000,020,517` units over its own 7,853 restricted rows, exactly.
A translation that cannot do that decides nothing, and a bound read off it would be an
artifact of the translation rather than of the measure.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
