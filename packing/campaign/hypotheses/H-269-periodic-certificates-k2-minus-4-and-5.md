---
title: H-269 — a periodic measure of Daniel's form with corner deficit above one proves s(k² − 4) = k for all large k, and above five quarters s(k² − 5) = k
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-269
  kind: hypothesis
  claim: >-
    A fixed-profile periodic measure of the form behind T-064 (a corner module in each
    corner, a wall profile of period one, Lebesgue measure on the interior, every
    non-Lebesgue mass on segments of a rational grid) exists at profile width w = 3 with
    exact rational corner deficit D > 1 such that every closed unit square in its base
    box [0, 2w + 3]^2 = [0, 9]^2, at any position and angle, has mass at least 1 with
    boundary mass counting, at margin zero. By the insertion lemma (Daniel, FRIEDMAN.md
    section 2.1, the mechanism of bentz_of_valid7 with the deficit and the box as
    parameters) the family then has total mass k^2 - 4D < k^2 - 4 on [0, k]^2 and proves
    s(k^2 - 4) = k for every k >= k_0, with k_0 = 8 under the source's proposed
    localization and k_0 = 9 under the slab form of the lemma. With the confirmed
    s(21) = 5, s(32) = 6 and s(45) = 7 (T-052, T-051, T-053) and the reported s(60) = 8
    (T-062) that is Friedman's Conjecture 1 at c = 4: s(k^2 - 4) = k for every k >= 5,
    independent of s(12). The second cell is d = 5: a family at width w <= 5 with
    D > 5/4, proving s(k^2 - 5) = k for every k >= k_0(5).
  lane: proof
  derived_from: [X-049]
  strategy_refs: ['proof:12', 'proof:22', 'proof:18']
  criterion:
    shape: determination
    metric: >-
      The exact rational corner deficit D of a candidate family after the density-layer,
      tilt-margin and nonnegativity constraints, recomputed here from the family file by
      an own parser; the base-box cover's zero-margin census (root boxes certified,
      uncertified boxes) from the source's exact checker replayed here in full; and the
      reduction from the base box to every k >= k_0, parametrized by the deficit and the
      box, read or kernel-checked.
    direction: >-
      Confirm the d = 4 cell only when D > 1 exactly, the base-box census is complete
      with zero uncertified boxes under a full replay here, and the reduction is accepted
      in review; the T-064 Valid7 replay under think-4k80 is the entry to that review.
      Reject the d = 4 cell when the exact LP at profile widths w = 3 and w = 4, R = w,
      pitch 1/5, returns D <= 1 after the exactness constraints: a bounded negative
      about this family class that says nothing about s(k^2 - 4). Any verified packing
      of k^2 - 4 unit squares below side k at some k >= 5 refutes the claim outright.
      The d = 5 cell is decided the same way at threshold 5/4 and widths w <= 5. No
      verified bound moves on the source's census alone; a register row for any k waits
      for a W2 review.
    threshold: 1
  instrument: >-
    The source's qx2 pipeline (evand/square-packing at 08e8a5f: search/qx2_exact.py for
    the exact family LP, qx2_zm.py with the zm_mixed and zeromargin primitives for the
    base-box check, qx2_records.py for the run record), run at R = w = 3 with base box 9.
    The checker and the k^2 - 3 family files are retained under
    packing/resources/web/evand-square-packing-2026-10-01/; the LP generator is not and
    must be fetched or rebuilt. A deficit-and-box-parametrized form of bentz_of_valid7
    (Lean) or the insertion lemma on paper closes the reduction. Neither the width-three
    family nor the parametrized reduction exists today.
  instrument_ready: false
  regime: >-
    Proof lane; closed unit squares and closed containment; fixed-profile periodic
    measures with Lebesgue interior and sigma = 0 bands, elements on the 1/5-grid, widths
    w = 3 and 4 for d = 4 and w <= 5 for d = 5; exact rational arithmetic in the LP
    projection and in the checker, floats only to choose which exact test to try; the
    base box 2w + 3 checked over its D4 fundamental domain; a family statement for
    k >= k_0, the finite k below k_0 taken from T-051, T-052, T-053 (confirmed) and
    T-062 (reported)
  instance: {axis: family, point: 'k^2-4'}
  sweep: {axis: family, points: ['k^2-4', 'k^2-5']}
  priority: 2
  cost_estimate: >-
    Source estimates, FRIEDMAN.md section 5: 5 to 10 CPU-hours for the exactness LP at
    R = w = 3, which is the go/no-go; 50 to 80 CPU-hours for the base-box check at box 9,
    a factor of three either way, refinement depth being the unknown; about a day of
    agent time to recover the LP pipeline and parametrize the reduction; d = 5 unpriced
  prereqs:
    - think-4k80
    - the source's qx2 LP at R = w = 3, fetched or rebuilt
    - a deficit-and-box-parametrized reduction from the base box to every k >= k_0
  replication: false
  registered: '2026-10-02'
  notes: >-
    Registers X-049's first candidate and absorbs the idea board's parked X-048 lead "a
    periodic family with deficit four". Premises checked 2026-10-02: T-064 stands at
    V0/C1, reported, its Valid7 premise not replayed here (RESULTS.md); the k^2 - 3
    family has D = 423621306389/500000000000 = 0.847 at w = 2, where the float LP gave
    0.945 before exactness, a price of about 0.1; the source's float LP at w = 3, R = 3,
    pitch 1/5 gives D near 1.154, a margin of 0.154 (FRIEDMAN.md section 5); the band LP
    caps D at 1.755 for w = 3 and at an interim 1.97 for w = 4, so d = 5 (D > 5/4) needs
    w >= 4. H-252's target s(45) = 7 is proved (T-053 replayed here, T-054 by a second
    route), so H-252 is overtaken and this hypothesis is the family successor. Not a
    duplicate of H-037: FRIEDMAN.md section 0 and X-049 both note that Roth-Vaughan's
    bound tends to zero at integer sides and cannot decide whether d_max(k) tends to
    infinity, so a fixed-profile family with growing D(w) is the only route on record to
    that question, and this is its first cell. Update 2026-10-03: Evan Daniel's
    s(k^2 - 4) = k for every k >= 5, registered as T-081 (V0/C1, reported), is the d = 4
    cell as stated here: a family of this form at w = 3 on the base box [0, 9]^2 with
    exact deficit D = 214770225571/200000000000 = 1.07385... > 1, reduced in Lean from
    ValidTilt9 to every k >= 8, with s(21), s(32) and s(45) below that. It settles the
    k^2 - 4 half as the source reports it, so no round of this hypothesis will run for
    d = 4. By this hypothesis's own direction the cell is confirmed here only when the
    full replay of qx2_zm.py on the box-9 cover (think-8hk1) completes with zero
    uncertified boxes; the reduction was built here from the retained bytes on 3 October
    and the claim chain reviewed (T-081's artifacts). The d = 5 cell, D > 5/4 at w <= 5,
    stays open; Daniel's D is below 5/4, so his family does not decide it.
---
# H-269: Periodic Certificates for the k² − 4 and k² − 5 Families

T-064 reports $s(k^2-3)=k$ for every $k\ge 6$ from one measure family: a corner module
in each corner, a wall profile of period one, Lebesgue measure inside, corner deficit
$D=0.847>3/4$, and every closed unit square of mass at least $1$ in the base box
$[0,7]^2$; the insertion lemma carries the box statement to every $k$. The same shape at
profile width three is Daniel’s own proposed route to $d=4$: a float LP gives
$D\approx 1.154$, and the open question is whether $D>1$ survives the exactness
constraints that cost about $0.1$ at width two.
This hypothesis freezes that go/no-go and the base-box check as one determination, with
$d=5$ ($D>5/4$) as the second cell.

A positive at $d=4$ gives $s(k^2-4)=k$ for every $k\ge 5$: the first proof that
$d_{\max}(k)\ge 4$ for all large $k$, Friedman’s Conjecture 1 at $c=4$, and, after
review, the eleven open cases $n=60,77,\dots,320$ of this record moved to proved.
It says nothing about $s(12)$.

A negative is specific.
$D\le 1$ at widths three and four says the fixed-profile class at those widths cannot
reach $d=4$, which also removes the first data point of the $D(w)\to\infty$ route toward
$d_{\max}(k)\to\infty$. A verified packing of $k^2-4$ squares below side $k$ at any
$k\ge 5$ ends both the family statement and Friedman’s conjecture at $c=4$.

**Update, 3 October 2026.** Evan Daniel reports the $d=4$ cell as this hypothesis states
it: $s(k^2-4)=k$ for every $k\ge 5$, from a family of this form at width three on the
base box $[0,9]^2$ with exact corner deficit
$D=214770225571/200000000000\approx 1.0739>1$, its finite premise `ValidTilt9` reduced
in Lean to every $k\ge 8$ ([T-081](../../frontier/RESULTS.md), registered `V0/C1`). That
settles the $k^2-4$ half as the source reports it, so no round here will run for $d=4$;
by the direction above the cell is confirmed here once the full replay of the box-9
cover under `think-8hk1` finishes with no uncertified box.
The $d=5$ cell ($D>5/4$ at width at most five) stays open: Daniel’s deficit is below
$5/4$, so his family does not reach it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
