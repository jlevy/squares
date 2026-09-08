---
title: H-133 — is the exactly-eleven plateau at 191/50 a site artefact?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-133
  kind: open_question
  claim: >-
    Is the restricted covering value of exactly 11.000000 that two site sets reached at
    side 191/50 an artefact of Trump-shaped B-cores overlapping only in site-free strips
    of width about 0.0124, so that adding sites in those strips or refining the net
    yields a certificate below eleven at 191/50; and if not, does the plateau close as
    an exact cover of the atoms by eleven mass-one cells?
  lane: proof
  derived_from: [X-021]
  strategy_refs: ['proof:9', 'proof:15']
  instrument: >-
    Thirty-minute artefact test: regenerate the grid site set at 191/50 and test whether
    the eleven B-cores of Trump's packing scaled by 382/387.7 overlap only in site-free
    regions. Then either add sites in the strips and re-run, or refine the net toward
    1800 directions with B = 99977/100000, or read the tight-cell census and run the
    exact cover with atom-based branching.
  instrument_ready: true
  regime: >-
    n = 11, side 191/50, the retained shrink and net for the artefact test and the
    plateau certificate; a finer net and shrink for the tax measurement
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: one session of four hours; the artefact test alone is thirty minutes
  prereqs: [the 3.82 grid site sets, T-018 atoms scaled by 382/381]
  replication: true
  registered: '2026-09-08'
  notes: >-
    Lane C's cheapest question in X-021 and the one that changes the ladder's status at
    3.82 immediately if the answer is yes; the n = 21 grid artefact is the precedent. The
    exact-cover route is the weighted form of Stromquist's ownership argument and the only
    one that works on a plateau at exactly eleven. Answered in session-103 (lane F,
    2026-09-08): the Trump-strip mechanism is refuted exactly, 45 grid-seed sites and 822
    of BC-200's retained sites lie in two or more of the scaled cores; the general
    site-invisible-overlap mechanism holds; adding strip sites left the value at 11.07
    with the generator stopping on its 32-row pricing cap; the census exceeds one million
    near-tight cells with no clustering on Trump's cores. Whether the true value at
    191/50 is below eleven stays open.
---
# H-133 — The Plateau’s Cheapest Test

At `3.82` two independent site sets stopped at a restricted covering value of exactly
eleven, and the record warns against reading that round number as the true value.
[X-021](../explorations/X-021-what-can-be-proved-about-eleven-squares.md) offers a
mechanism: Trump’s eleven cores scaled to `3.82` overlap only in strips a grid of pitch
`0.047` never samples, which is how the `n = 21` artefact arose.

If the test confirms the mechanism, the ladder at `3.82` is an instrument question; if
it refutes it, the plateau is geometric and the exact-cover certificate is the only
route left. [Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md) owns
both halves in BC-297.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
