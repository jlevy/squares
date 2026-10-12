---
title: H-252 — a zero-margin weighted closed cover of [0,7]^2 with mass below 45 exists, so s(45) = 7
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-252
  kind: hypothesis
  claim: >-
    A D4-invariant weighted point set in [0,7]^2 with rational weights and total mass
    strictly below 45 exists such that every closed unit square contained in [0,7]^2,
    at any position and angle, contains points of total weight at least 1, a point on
    the square's boundary counting. By Daniel's scaling argument (a packing at side
    s < 7 scales to 45 pairwise disjoint closed unit squares in [0,7]^2), it follows
    that s(45) >= 7, and the 7 x 7 grid gives s(45) = 7: the k = 7 member of the
    k^2 - 4 family after Daniel's s(32) = 6.
  lane: proof
  derived_from: [X-039]
  criterion:
    shape: determination
    metric: >-
      A cover in Daniel's plain certificate format whose D4 invariance and exact total
      mass below 45 are recomputed here, certified at margin zero over the whole reduced
      pose region (centres in [0, 7/2]^2, half-tangent in [0, 1/2]) by zeromargin.py
      with zero uncertified boxes, and independently by the Rust zmcheck, on the
      published bytes
    direction: >-
      Confirm only on both checkers' complete censuses re-run here and an accepting
      review of the method (the intake lane's review of Daniel's s(32) certificate is
      the entry). A cover search that stalls with mass at or above 45 is a bounded
      negative about the search at k = 7, as Daniel's own record pins the k = 4 LP at
      exactly 12.000; it says nothing about s(45). A register row waits for a Fable
      max W2 review.
    threshold: 45
  instrument: >-
    evand/square-packing at 167d842: the cover search under s12/search and
    s12/search/zeromargin.py, with verify2/zmcheck, run at k = 7 if the tools take k as
    a parameter; otherwise the adaptation is BC-396's build
  instrument_ready: false
  regime: >-
    n=45; closed unit squares, closed containment, D4-invariant point covers checked at
    margin zero by exact subdivision of pose space; the k^2 - 4 family
  instance: {axis: n, point: 45}
  priority: 1
  cost_estimate: >-
    Fable extra-high one to two hours on the method beside the intake review; Opus
    extra-high half a day if the search must be adapted; the k = 6 check cost 2.8 CPU-h
    over 7,200 roots, so about 4 CPU-h per cover at k = 7
  prereqs: [think-0g4t]
  replication: false
  registered: '2026-09-27'
  notes: >-
    From the 2026-09-27 planning block
    (docs/project/specs/archive/plan-2026-09-27-after-4640020-overnight.md), on the
    coordinator's discovery of evand/square-packing (s(32) = 6, s(12) >= 15680/3951,
    s(21) >= 5000/1001). The method reached the endpoint at k = 6 and fell short at
    k = 5 (4.995) and k = 4 (3.968616, with the pure cover LP pinned at 12.000), so the
    transfer is upward in k: n = 45 (wand125 holds 6.955 against 7), then n = 60, 77
    and 96. Another lane reviews and registers Daniel's own results; nothing here
    replays them.
---
# H-252: The Next Member of the k² − 4 Family

Daniel’s s(32) = 6 is a weighted closed cover of $[0,6]^2$ of mass $31.71 < 32$ in which
every closed unit square captures at least 1, checked at margin zero.
The same construction fell short at $k = 5$ and $k = 4$, where the endpoint LP sits at
exactly $12$, so the next case to try is upward: $n = 45$ at side $7$, where wand125’s
rectangle certificate holds $6.955$.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
