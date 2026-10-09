---
title: H-338 — does a charge specialised to one occupancy state exclude it below S*?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-338
  kind: open_question
  claim: >-
    For a residue state X of the H-266 cover and a cap V < S*, does a weighted counting
    certificate of R068's kind, with its sites, strict cores and parent-centre envelopes
    specialised to X's seventeen cells (each parent's centre confined to its cell, each
    core built for that cell's angle rows), certify that no packing of side at most V
    has state X; and in particular does one exclude the family's own state at V = S* -
    1/100, where the per-state kernel is loss-limited and the branch and bound is
    disjunction-limited?
  lane: proof
  derived_from: [X-051]
  instrument: >-
    Unbuilt: the fractional parent-core tooling (sqpack.fractional.parent_core and the
    exact event-cell sweep) with per-parent centre envelopes restricted to named cells
    and a state-conditioned site dictionary; the exact LP of sqpack.exact_lp for the
    weights; the standing interval route or the source checkers for the coverage
    decision.
  instrument_ready: false
  regime: >-
    n = 17; the H-266 cover in the U frame; one state at a time; cap V below S*; the
    budget rule of capacity-one atoms and R068's threshold features.
  instance: {axis: n, point: 17}
  priority: 3
  cost_estimate: About 20 agent-hours to a first verdict on the family's state; the coverage sweep's cost is R068's scale, hours per interval set.
  prereqs: [H-325]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route G. The 5 October stall classification found three of seven per-state
    stalls consistency-limited: every owner at least 63 per cent supported, so no
    one-partner cut at any row width removes a quarter of any owner. A counting
    certificate is not pairwise; it charges every pose at once. exp-243 showed that
    R068's own charge collapses at the cap because its sites were spaced for larger
    cores; a state-conditioned charge places sites for the cells it must cover. An open
    question because a negative LP value closes only the chosen dictionary.
---
# H-338: A Non-Pairwise Engine for the Tail

**Mechanism.** The kernel reasons one partner at a time and stalls where every pose of
one owner is cleared by some pose of every partner.
A charge assigns every closed unit square a weight and needs only that seventeen
disjoint cores exceed the total mass; it never asks which partner clears which pose.
Specialising the dictionary to one state’s cells makes the parent-centre envelopes
seventeen small polygons instead of the whole centre box, which is where a charge gains
strength.

**First discriminator.** The family’s own state at $V=S^\ast-10^{-2}$: if a
state-conditioned charge excludes it where H-325’s engines stall, the engine exists.

**Expected information.** Whether the consistency-limited tail has any engine at all.

**Limits.** A charge proves a bound at one cap, so the engine serves the cap ladder and
the exclusion stage at $U'$ only where the margin suffices; exp-243’s collapse at the
cap is the risk, and the dictionary search is a search.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
