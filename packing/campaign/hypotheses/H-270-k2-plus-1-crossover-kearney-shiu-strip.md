---
title: H-270 — Kearney–Shiu's strip construction packs k² + 1 unit squares below the L-step plateau k + 5/√2 − 3 at some k from 18 to 41
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-270
  kind: hypothesis
  claim: >-
    For some integer k with 18 <= k <= 41, the strip construction of Kearney and Shiu
    2002, sections 5 and 6 (a trivially packed rectangle of k(k - m) squares; a strip of
    height m + delta holding K slanted columns of m + 1 squares at the angle theta with
    (m + 1) cos theta + sin theta = m + delta; two end trapezia packed in axis-aligned
    rows) places k^2 + 1 unit squares in a square of side strictly below
    k + 5/sqrt(2) - 3, the side that DS7's L step carries down from the Goebel square at
    n = 65 and that the atlas holds at every k from 8 to 17. Equivalently
    delta_k < 5/sqrt(2) - 3 = 0.5355 at some k below Kearney and Shiu's own k = 42
    (Pell, delta_42 < 0.507) and k = 43 (strip, delta_43 <= 0.4888).
  lane: search
  derived_from: [X-049]
  strategy_refs: ['search:5', 'search:8', 'search:9']
  criterion:
    shape: record
    metric: >-
      The smallest k in 18..41 at which an exactly verified packing from the template has
      side below k + 5/sqrt(2) - 3, together with the template's least delta per k over
      the declared parameter space: m from 1 to k - 1, column height m + 1, K columns,
      symmetric or asymmetric trapezium row packings filled at each row's narrowest
      width.
    direction: >-
      Confirm when at least one k in 18..41 yields a packing whose rational witness side
      S satisfies S < k + 5/sqrt(2) - 3 under an outward-rounded interval comparison,
      the pose verified by sqpack.verify.verify_packing and the independent
      devtools.check_rational_witness_independent. Reject when the exact scan over the
      whole declared parameter space finds no such k: a bounded negative about this
      template that leaves other constructions open and places the crossover between
      the template's reach and k = 42.
    threshold: 'k + 5/sqrt(2) - 3'
  instrument: >-
    A devtool, not yet written (proposed name devtools.scan_kearney_shiu_strip), that
    enumerates (k, m, K) over the declared space, solves theta exactly (the defining
    relation is a quadratic in cos theta once sin theta is eliminated), fills each
    trapezium row by row at the row's narrowest width, counts the squares, searches the
    least delta per (k, m) at which the count reaches k^2 + 1, emits the best pose per k
    as a Witness/v2 file with a rational side rounded up, and hands it to the two
    verifiers; byte-identical replay under --check.
  instrument_ready: false
  regime: >-
    Search lane, upper bounds only; n = k^2 + 1 from 325 to 1682, above the atlas and the
    frontier's case files, which end at 324, and above H-035's 100 <= n <= 324; the
    comparison side is the L-step plateau, an upper bound at every k >= 8 by DS7
    section 2 from the Goebel square (a, b) = (4, 5) at n = 65; the Kearney-Shiu
    template with axis-parallel trapezium rows, the Pell construction excluded because
    its next member is k = 42; verification exact over Q or by outward-rounded intervals
    on the emitted pose
  instance: {axis: n, point: 'k^2+1, k = 18..41'}
  sweep: {axis: k, points: [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]}
  priority: 1
  cost_estimate: >-
    Half a day of agent time to build the scan and its tests; seconds of compute per k;
    seconds of verification per candidate
  prereqs:
    - the scan devtool with a --check replay
  replication: false
  registered: '2026-10-02'
  notes: >-
    Premises checked 2026-10-02 against the archived transcription: section 4, Table 1
    (Pell members n = 2, 8, 42, 240, with delta = 0.5355 at 8 and 0.506 at 42); section
    5, Theorem 2's construction at n = p(t - 1) = 1, 12, 55, where the paper states
    delta_55 < 1/2 and the registrant's evaluation of delta(t) gives about 0.708 at
    n = 12; section 6, n = 43 with m = 15, K = 36, T = T' = 35 and delta_43 <= 0.4888.
    The paper states no construction at 9 <= k <= 41, and its explicit bound (2) exceeds
    0.85 at k = 41, so the candidate rests on the template's free parameters, which the
    paper tuned only at n = 43 and the Table 2 values. The plateau: the family census's
    delta_plateau lists k = 8..17 (X-049). A registrant's hand estimate, not a
    measurement, which the scan replaces: at k = 38, m = 14, K = 31 the template seems
    to leave one spare square per trapezium at the plateau side, and at k = 30 it falls
    a few squares short at every m tried. Relation to H-035: a confirmed k here is above
    H-035's range and scopes it, since even the hand-tuned strip needs k in the thirties
    on this family and the asymptotic primitives are predicted to fail on it at
    n <= 324; a packing found here cannot enter the frontier, which has no case above
    324, and is retained as an experiment result and a witness.
---
# H-270: Where the k² + 1 Plateau Ends

The atlas holds $s(k^2+1)-k=5/\sqrt2-3$ at every $k$ from 8 to 17: the Göbel square at
$n=65$ carried down by L steps, which also makes that side an upper bound at every
$k\ge 8$. Kearney and Shiu beat it at $k=42$ by a Pell solution and at $k=43$ by their
strip, and state no construction between.
The strip has free parameters, the strip height $m$, the column count $K$ and the
packing of the two end trapezia, which they tuned only at $n=43$ and at the Table 2
values. The scan asks for the smallest $k$ at which the template, exactly verified, goes
below the plateau.

A positive names where the asymptotic regime starts on the cleanest family, and scopes
H-035: its primitives are predicted to fail on $k^2+1$ at $n\le 324$ because even the
hand-tuned strip needs a larger $k$. A negative over the whole parameter space says the
plateau survives the only published template below 42, so the crossover needs a
different arrangement, which is what Kearney and Shiu themselves expected for
$\delta\le 1/2$.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
