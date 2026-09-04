# BC-153 — Independent review of the H-060 proof (Goebel `n = 5`, fixed-side local rigidity)

## Provenance and installation

This document is the review deliverable of BC-153, the independent review of the H-060
proof packet, written on 2026-09-03 in the agenda-016 ten-hour run.
Its author wrote only to `scratchpad/bc153/` -- a container-local directory outside the
repository, which does not survive the session -- and modified no repository file.
It is installed here so that the evidence the records cite outlives that directory.

The source was `588` lines with SHA-256
`ea9af1b76bbc08931dc72962fce99a2df5bbb9e54d2c3d37af72f5bfb5487d1c`, and that hash names
the scratchpad source rather than this file.
The installation added this preface and the closing guidelines footer, and reformatted
the body to house Markdown conventions; it altered no classification, verdict, finding,
number, citation, recommendation or claim boundary, and none may be altered here.
References of the form `scratchpad/...` in the body below are the reviewer’s own record
of what was read and where it was written at review time, and are left as written.

* * *

- **Reviewer:** independent reviewer for BC-153 (agenda 016). Authored none of the
  packet, X-012, exp-058, the instrument, or the three supporting reviews.
- **Date:** 2026-09-03. Reading and mathematics 08:46Z onward; replay after the
  08:58Z–09:58Z quiet lease.
  Inside the window the only processes I started were clock checks: `date -u` at 09:02Z,
  09:05Z and 09:07Z, and from about 09:13Z one
  `until [ $(date -u +%H%M%S) -ge 095830 ]; do sleep 30; done` loop that reads the clock
  every thirty seconds.
  None touches the repository or uses CPU. The coordinator reported the H-052 writer
  finished early and released the lease at 09:36:29Z; the clock-watch was stopped and
  the replay ran 09:40:19Z–09:41:30Z. No replay, test, interpreter or git process ran
  while the lease was held.
- **Write scope honoured:** only `scratchpad/bc153/`. No repository file was modified,
  staged, or committed.
- **Reviewed against:** the frozen packet `scratchpad/bc152/h060-chart-and-proof.md`
  (926 lines including the trailing newline count; SHA-256 checked in §6), its replay
  scripts, X-012 as installed, exp-058, H-060’s frozen criterion, and the three
  supporting reviews (instrument readiness, curve-selection source check, prior-art
  survey). The supporting reviews were used as evidence, not as authority: every
  mathematical step below was re-derived by me.

## Classification: PASS

Earned on the mathematics (§2–§4) *and* on the replay (§6, run 09:40Z–09:41Z after the
lease was released at 09:36Z): the reviewer’s from-scratch reconstruction passes every
check, the packet’s own scripts pass with digests equal to the exp-058 record, and the
instrument reproduces from clean temporary roots under normal and `-O` Python with all
eight controls rejecting.

The argument closes.
Every step of the registered route — chart, complete constraint accounting,
neighbourhood reduction, curve selection on the punctured set, and the order-`2m`
coefficient induction — is correct as written, and every exact quantity it consumes
reproduces from an implementation of mine that shares no code with the packet, with
`sqpack`, or with the instrument.
H-060’s three acceptance clauses are met as registered; no clause was weakened.
The gaps I name in §5 are all either disclosed by the authors, non-load-bearing, or
both; none is a condition on the pass.

The scope at which the theorem may be claimed is stated exactly in §7.

* * *

## 1. What was reviewed, pinned

| item | identity |
| --- | --- |
| proof packet | `scratchpad/bc152/h060-chart-and-proof.md`, SHA-256 `28343b74…40b6b` (verified §6) |
| installed record | `packing/campaign/explorations/X-012-…md` (citation apparatus rewritten after freeze, mathematics unchanged — checked by reading both) |
| round record | `exp-058-h-060-n5-chart-and-proof.md`, verdict `unresolved`, `needs_review: true` |
| criterion | `H-060-n5-local-rigidity.md`, frozen; `instrument_ready: true` at 743fd18a |
| certificates | `bc-049-n5-rigidity-certificates.json` (T-012), read-only |
| supporting reviews | instrument readiness (PASS), curve-selection source check (YES), prior-art survey |

* * *

## 2. Does the argument close? Step by step

Notation as in the packet: `r = √2`, `s = 2 + r/2`, chart `z = (dx_i, dy_i, t_i)`,
`θ_i = θ_i^0 + 2 arctan t_i`, `J = diag(1,1,2)^{⊕5}`, rows `g̃_0..g̃_19`, `A = A_chart`,
`q = q_chart`, `C = {x : A x ≥ 0}`, `e = e_{t4}`.

### 2.1 The chart (Lemmas 1–3) — correct

- `t ↦ θ^0 + 2 arctan t` is a real-analytic bijection `R → (θ^0 − π, θ^0 + π)`; the
  product with the identity on centres is a homeomorphism of `R^15` onto the open set
  `U`. Nothing smaller than `R^15` is needed.
  Correct.
- Denominators `1 + t_i^2 ≥ 1`; clearing them preserves every sign on all of `R^15`.
  Correct, and it is what lets the 400 sign conditions be stated on polynomials.
- 2-jet transfer: `2 arctan t = 2t − (2/3)t^3 + O(t^5)` has no `t^2` term, so
  `Φ(z) = P^0 + Jz + O(|z|^3)` and `Hess Φ(0) = 0`; with `D(0) = 1`, `∇D(0) = 0`,
  `G(P^0) = 0`, the product rule gives `∇G̃(0) = J^T ∇G`, `Hess G̃(0) = J^T Hess G J`. I
  re-derived the product-rule expansion; the two cross terms and the `G · Hess D` term
  vanish for the stated reasons.
  Correct.

I recomputed rows 0, 1, 3, 7, 9, 12 by hand from the corner and normal formulas and they
match the packet’s §2.5 table; §6 records the machine check of all twenty.

### 2.2 The full system (Lemma 4, §3.2) — correct

Lemma 4 (separating axes, closed squares, disjoint interiors ⟺ some `(owner, e)` branch
has all four corners of the other square on the closed outer side): the ⇐ direction is
the half-plane separation; the ⇒ direction goes through the Minkowski difference `K`,
using `int(A + B) = int A + int B` for convex bodies and the fact that the edge normals
of a Minkowski sum of polygons are edge normals of the summands.
Both facts are standard and the packet proves the first.
The count `2 × 4 × 4 = 32` per pair, `320` total, plus `4 × 20 = 80` wall–corner
functions, is right, and `F` is therefore a finite Boolean combination of polynomial
inequalities — semialgebraic without Tarski–Seidenberg, and closed.
`F = Φ^{-1}(Feas(s) ∩ U)` exactly, because containment of a convex square in the convex
container is corner containment and Lemma 4 is an equivalence.
Correct.

### 2.3 The neighbourhood reduction (Proposition 5) — valid in both directions, and no boundary behaviour is consumed

- `N` is cut out by 128 strict polynomial inequalities, all strict at `0` by the exact
  base margins, hence open and containing `0`.
- (i) `F ∩ N ⊂ {g̃_j ≥ 0}`: for each touching pair `(c, 4)`, membership in `F` says some
  branch holds; membership in `N` says the other seven each have a strictly negative
  corner; so the holding branch is `b_c` and its active corner inequality — the pair row
  — holds. The wall rows are among the 80 that `F` imposes.
  Uses only the 28 negative witnesses.
  Correct.
- (ii) the converse: on `N` the 64 inactive walls, the 24 corners of the non-touching
  witness branches and the 12 non-active corners of the separating branches are strictly
  positive; adding the 20 rows makes every wall inequality and every pair’s `OR` true.
  Correct. This is the clause “accounts for the entire local feasible set”.

**On the instrument’s interior-only audit.** The proof does not need it and does not
need anything at or near `∂N`. `N` is defined by sign persistence, not by a radius; the
proof consumes exactly three facts — `N` is open, `0 ∈ N`, and the 28 witnesses are
negative *on* `N`, which is true by definition.
The isolation argument (Corollary 4.3) enters `N` by continuity of the arc at `s = 0`
and never leaves a small `(0, ε)`. The instrument’s sampled audit corroborates the
instrument’s *implementation* of the same definition; its limitation (no samples near
`∂N`, disclosed) is a limitation of that corroboration and does not touch the proof.
Consistently with H-060’s rules, a lone feasible point at positive distance could show
only that it lies outside `N`, never that Proposition 5 fails.

I spot-checked the witness table for pair `(0, 4)` by hand: branches `(0,1)` and `(0,2)`
fail at square 4’s extreme corners by exactly `−r/4`; `(0,0)`, `(0,3)` by `−1 − 3r/4`;
`(4,0)`, `(4,2)` by `−1/2 − r/2`; `(4,1)` by `−1 − r`; and the separating branch `(4,3)`
has the other three corners at `r, r/2, r/2`. All agree with the packet’s table.
§6 records the machine check of all 320.

### 2.4 Curve selection (§4) — hypotheses reduced; the punctured set is essential; provenance judged sufficient

- `A := F \ {0}` is semialgebraic (difference of two semialgebraic sets) and locally
  closed (`F` closed, `{0}` closed).
  Not used by BCR 8.1.13, but true.
- `0 ∈ Cl(A)` ⟺ `P^0` not isolated in `Feas(s)`, via the homeomorphism onto the open
  `U`. Correct.
- The lemma returns a Nash (real-analytic, semialgebraic) `γ : (−1,1) → R^15`,
  `γ(0) = 0`, `γ((0,1)) ⊂ A`. Because `0 ∉ A`, `γ(s) ≠ 0` for `s ∈ (0,1)`; by the
  identity theorem the Taylor series at `0` is not identically zero, giving a least
  `m ≥ 1` with `a_m ≠ 0`. This is the whole role of puncturing: applied to `F` itself
  the lemma is satisfied by the constant arc and the induction has no `a_m`. The packet
  says this explicitly and applies the lemma to the punctured set.
  Correct and load-bearing, as the source check also found.
- Analyticity is load-bearing (a `C^∞` arc could be flat; a merely continuous
  semialgebraic arc has a Puiseux expansion and needs `s = u^N` first).
  The packet takes the Nash version and so needs neither.
  Correct.

**Provenance judgment.** The printed page of BCR Proposition 8.1.13 was not reached by
the packet lane, by the source-verification lane, or by me.
What stands behind the citation: BCR’s own printed table of contents locating the
proposition in §8.1; the statement in the words of Coste, an author of BCR, in his own
notes (self-described provisional, “without giving a complete proof”); four verbatim
applications of `[BCR, Prop. 8.1.13]` by one author group, one of them to a set
difference; and, for the continuous version, the complete primary text of
Basu–Pollack–Roy (Theorem 3.19 in the 2006 print, 3.22 in the posted revision).

I independently accept the statement, for a reason that does not depend on the unopened
page: the Nash version follows from the primary-text continuous version by a standard
two-line argument. A continuous semialgebraic arc `γ : [0, ε) → R^n` has, near `0`,
components given by convergent Puiseux series in `s^{1/N}` (the one-variable structure
theorem for semialgebraic functions — germs of continuous semialgebraic functions of one
variable are algebraic Puiseux series, the fact Coste’s notes state in the two
paragraphs before his Theorem 1.15); substituting `s = u^N` turns them into convergent
power series in `u`, so `γ̃(u) = γ(u^N)` is real-analytic at `0`, still semialgebraic,
with `γ̃(0) = 0` and `γ̃((0, ε^{1/N})) ⊂ A`. That is the statement the packet uses.
The Milnor route with the packet’s finite-union reduction (§4.1) is a third derivation;
I checked that reduction (the `8^10` branch choices, the `2^M` sign patterns, the
puncture as `{|z|^2 > 0}`, `N` itself being strict) and it is correct.
Three derivations reach the same needed statement; the only thing not confirmed against
print is the numbering and wording in BCR. That is a citation-provenance limitation,
disclosed by the authors, and not a gap in the mathematics.
It is listed in §5 and is not a condition on the pass.

**Quotations verified first-hand** (from the text extractions in
`scratchpad/bc152-curveselection/src/` and `scratchpad/bc152-novelty/`, not from the
lanes’ summaries): BPR Theorem 3.22 reads verbatim “Let `S ⊂ R^k` be a semi-algebraic
set. Let `x ∈ S̄`. Then there exists a continuous semi-algebraic mapping
`γ : [0,1) → R^k` such that `γ(0) = x` and `γ((0,1)) ⊂ S`” (primary text).
Coste’s Theorem 1.14 reads verbatim as the source check quotes it, with
`x ∈ clos(S), x ∉ S`; and the lines immediately preceding his Theorem 1.15 state the
very bridge above — “The change of variable `t = u^p` that we used above shows the
following: if `f : [0,1) → R` is a continuous semialgebraic function, there is a
positive integer `p` … From this fact we easily deduce an improved curve selection
lemma.
Theorem 1.15 (Analytic curve selection) For `A` and `x` as in theorem 1.14, …”. So
the derivation I give is the one an author of BCR gives.
Derdzinski–Gal §4 defines Milnor’s “semi-algebraic” as algebraic ∩ finitely many strict
inequalities and states Theorem 4.1 with a real-analytic curve, verbatim as the source
check reports; X-007’s own text also already carries the `s = u^N` route.
The [CW96] paragraph before Theorem 4.3.1 ("the first derivative of the analytic flex
may be trivial … the first nonvanishing derivative … has the correct sign") is as the
survey quotes it. The Goebel extraction has no occurrence of “rigid” or “uniqu”
(case-insensitive) and does carry Proposition 1 at `S(2 + ½√2 − ε)`.

### 2.5 The T-012 transfer (Proposition 6) — correct, and the sign is intrinsic

- `A e = 0` because `t4` appears in no gradient row.
  Geometrically: `∂/∂θ_4` of each pair gap is `(p − c_4) · n^⊥`, which vanishes exactly
  when the contact corner is the foot of the perpendicular from `c_4`, i.e. the edge
  midpoint — computed to be so for all four contacts (along-edge parameter exactly
  `1/2`). Correct.
- `C = R e`: the packet cites T-012’s 28 Farkas certificates through `S` and `J`. I
  derived the cone by hand from the row inequalities without any certificate, and §6
  records both an exact rational LP and 28 certificates of my own construction:
  `dx0 ≥ |t0|`, `dy0 ≥ |t0|` (rows 0,4,1,2); `dx4 + dy4 ≥ dx0 + dy0` (row 3);
  `−(dx4 + dy4) ≥ −(dx3 + dy3) ≥ 2|t3|` (rows 15,16,17,18,19); hence `dx4 + dy4 = 0`,
  `dx0 = dy0 = t0 = 0`, `dx3 = dy3 = t3 = 0`; then rows 9 and 11 give `dy4 − dx4 ≥ 0`
  and `dx4 − dy4 ≥ 0`, so `dx4 = dy4 = 0`, and squares 1, 2 are pinned the same way.
  Every coordinate but `t4` is forced to zero; `t4` is free.
  Correct.
- Self-stress: `w = (1/2, 1/2, r/2, 1/2, r/2, 1/2)` on rows `5, 8, 9, 10, 11, 12` — I
  summed the six gradient rows by hand: `(dy1 − t1) + (−dx1 + t1) + (dx1 − dy1 − dx4 +
  dy4)
  + (dx2 + t2) + (−dx2 + dy2 + dx4 − dy4) + (−dy2 − t2) = 0`. `w · q = 2 · (r/2)(−2) =
    −2r`. Correct.
- **Normalization.** The sign of the obstruction is intrinsic and no factor is absorbed.
  Let `Φ := Σ w_j g̃_j`. Since `w^T A = 0`, `∇Φ(0) = 0`, so `Hess Φ(0)` is a
  well-defined quadratic form independent of coordinates (the second-derivative
  correction `Σ ∂_kΦ · Hess ψ_k` vanishes under any `C^2` change `ψ`), and
  `w · q = e^T Hess Φ(0) e` is its value on the flex line.
  Under a positive row rescaling `g_j → σ_j g_j` the self-stress rescales
  `w_j → w_j/σ_j` and `Φ` is unchanged.
  Under the chart, `e_{t4}` corresponds to `J e_{t4} = 2 e_{w4}`, so
  `q_chart = q(2e_{w4}) = 4 q_geo` — a quadratic scaling of the direction, sign
  preserved. The packet pairs `w = S w̃` (weights for the *unscaled* rows) with `q_chart`
  of the *unscaled* cleared polynomials, which is the consistent pairing.
  `w · q_chart = −2√2` and `w · q_geo = −√2/2` are one fact.
  Confirmed by §6 (`Φ` restricted to the flex line is exactly `−√2 · t4^2`).

### 2.6 The induction (Lemmas 7–8, Theorem 9) — genuinely covers every `m ≥ 1`, no division, no hidden nonvanishing

Lemma 7: if `f(s) = Σ_{k≥K} f_k s^k` converges and `f ≥ 0` on `(0, ε)` then `f_K ≥ 0`.
Correct whether or not `f_K` is the true leading coefficient (if `f_K < 0`, `f < 0` for
small `s > 0`).

Lemma 8: for `γ(s) = Σ_{k≥m} a_k s^k`, `a_m ≠ 0`, and polynomial `g` with `g(0) = 0`:
orders `m ≤ k < 2m` receive only the linear part `a · a_k`; order `2m` receives
`a · a_{2m} + (1/2) a_m^T H a_m` (the only split `k + l = 2m` with `k, l ≥ m` is
`(m, m)`); cubic and higher parts start at `3m > 2m`. Correct for every `m ≥ 1`,
including `m = 1` where `3m = 3 > 2`. §6 records a machine check on random arcs with
`m = 2, 3`.

Theorem 9, checked line by line:

- *Base `k = m`.* Orders `< m` vanish (their `a_k` are zero; the quadratic part starts
  at `2m > m − 1`); the order-`m` coefficient is `a_j · a_m`; Lemma 7 gives `A a_m ≥ 0`,
  so `a_m ∈ C = R e`, `a_m = λ e` with `λ ≠ 0` by definition of `m`, and `A a_m = 0`.
- *Step `m < k ≤ 2m − 1`.* All coefficients of order `< k` are `a_j · a_{k'}` with
  `k' < 2m` (Lemma 8’s first formula applies), and each is `0` because
  `a_{k'} ∈ C ⊂ ker A`. So order `k` is leading, Lemma 7 gives `A a_k ≥ 0`, `a_k ∈ C`,
  `A a_k = 0`. The step needs `k < 2m` to stay in Lemma 8’s linear regime, and it does.
- *Order `2m`.* Every coefficient below `2m` vanishes; the order-`2m` coefficient is
  `a_j · a_{2m} + (λ^2/2) q_j`; Lemma 7 gives `A a_{2m} ≥ −(λ^2/2) q` componentwise.
  Multiply by `w ≥ 0` and sum: `0 = w^T A a_{2m} ≥ −(λ^2/2)(w · q) = λ^2 √2 > 0`.
  Contradiction. `λ ≠ 0` enters only as `λ^2 > 0`; nothing is divided by `λ`; nothing is
  assumed about `a_{2m}` (the identity `w^T(A a_{2m} + (λ^2/2) q) = −√2 λ^2` holds for
  every `a_{2m}`, §6).

Two things the induction relies on, and both hold exactly: `C ⊂ ker A` (so the lower
coefficients vanish *exactly*, not merely nonnegatively — otherwise a positive
coefficient at some order `k' < 2m` in some row would end that row’s constraints and the
order-`2m` inequality would be lost for it), and `w · q < 0` on rows a nonnegative
self-stress combines to zero.
The induction stops at `2m` and uses only the first- and second-order jets; it claims
nothing about higher-order rigidity, so the Connelly–Servatius warning does not apply.
With `m = 1` it is T-012’s own order-2 inequality.

### 2.7 Theorem 10 and the equivalent formulations — correct

Not isolated ⟹ Corollary 4.3 ⟹ analytic nonconstant arc satisfying (4.1) ⟹ contradicts
Theorem 9. The rejection clause of H-060 (a nonconstant feasible arc, or an exact
convergent sequence of distinct feasible poses) is exactly the negation of isolation, so
the theorem excludes both.
One prose nit in §1.3 (i): “a nonconstant continuous path leaves every neighbourhood’s
singleton” needs the one-line argument that if a path in `Feas(s)` is constant on
`[0, t*]` and not beyond, then `P^0` is a limit of distinct feasible points; the
conclusion is right.
The lift from unlabeled placed squares to `(c, θ)` is a covering-space lift and is
correct, so isolation implies Kingbird’s fixed-side rigidity.

### 2.8 Where the argument is weakest, and what it does not cover

Weakest, in my judgment: (a) the citation provenance of §2.4, which I have judged
non-blocking for the reasons given there; (b) the dependence on exactly computed
quantities — 400 base margins, 20 gradient rows, the restricted Hessian, the
certificates — which is why I rebuilt them from scratch (§6). Nothing else is soft.

Cases it does not cover, all correctly excluded from the claim: container side free (the
cone opens, X-007); relabelled or symmetry-image poses (at positive chart distance;
isolation of the labeled pose does not see them and need not); other `n = 5` optimal
packings, if any; global uniqueness; a numerical isolation radius.

* * *

## 3. The second, corroborating route (§5.7, Theorem 11) — independent and valid; the multiplier subtlety is not a problem

Theorem 11’s normalized-sequence proof: `z_k → 0` in `G \ {0}`, `d_k = z_k/|z_k| → d`;
first order gives `A d ≥ 0` so `d = ±e`; second order, after `w` kills the linear terms
*exactly* (not just in the limit), gives `d^T H_w d ≥ 0`, but `e^T H_w e = w · q < 0`.
Correct. It shares with the primary route only Proposition 5(i) and Proposition 6, uses
`C^2` rather than semialgebraicity, and needs no curve selection or induction.
It is a genuinely independent second derivation of isolation from strictly weaker
hypotheses.

The multiplier scaling: in the SOSC packaging with objective `−|z|^2`, the Lagrangian
Hessian along `e` is `−2 − μ (w · q)`, positive iff `μ > 2/(−w · q)`; `μ = 1` clears the
chart normalization (`−w·q = 2√2`) and fails the `(c, θ)` one (`−w·q = √2/2`). This is
only the freedom to scale a KKT multiplier when `∇f = 0`; the primary argument has no
objective, no multiplier, and consumes only the sign of `w · q`, which §2.5 shows is
intrinsic. It indicates no problem in the primary argument.
The packet labels this route non-acceptance and it discharges no obligation of the
registered route; I agree with both.

* * *

## 4. Novelty — S3 as scoped, independently accepted

Basis checked by me from the archived sources, not from the survey’s summary:

- `packing/resources/web/kingbird-squares-in-squares.md` line 44: the `n = 5` entry is
  marked “Rigid.” with a link and no argument; the definition (from the live rigid page,
  fetched by two other lanes on 2026-09-03) is fixed-side and coincides with isolation
  through the lifting remark.
  Asserted, not proved.
- `packing/resources/papers/friedman-ds7-…md`: rigidity is remarked only for `n = 40`
  (line 59) and Trump’s `n = 11` (line 71); Theorem 2 (line 225) proves
  `s(5) = 2 + 1/√2` by an unavoidable four-point set and says nothing about uniqueness
  or rigidity.
- Goebel 1979: the survey’s and the packet’s extractions (0 hits for "rigid"/"unique")
  agree; the instrument reviewer partially corroborated.
  Not re-extracted by me.
- No published uniqueness theorem for the `n = 5` optimum was found by the survey; none
  is known to me. An unavoidable-set proof does not analyse its equality case, so
  “uniqueness ⟹ rigidity” is not available as a prior route.
- The closing principle (first-order cone a line plus a nonnegative self-stress with
  `w · q < 0` ⟹ isolation) is the classical second-order sufficient optimality condition
  and the energy principle of Connelly–Whiteley; the analytic-flex induction to order
  `2m` is the shape of [CW96] Theorem 4.3.1. Neither is new and the packet claims
  neither.

I accept: **first exact proof that Goebel’s `n = 5` optimum is locally rigid at fixed
side — a property asserted without proof by Kingbird and not stated by Goebel or
Friedman.** Score S3 (a case result), not S4. Two qualifications, both already in the
record: “first” is relative to the literature searched (Connelly 2008 was not read in
print; Kingbird’s method is unknown); and, relative to the repository’s own prior state,
T-012’s certificates plus the classical SOSC already implied the result once the local
reduction is granted, so the packet’s genuinely new content is Proposition 5 — the exact
accounting of all 400 functions and the 128-condition neighbourhood — together with the
closing, proved directly for corner-on-line and corner-on-wall inequalities.

**The Kingbird list discrepancy** (X-012 §7.3: thirteen rigid `n` on the live rigid page
versus four “Rigid.”
annotations at `n ≤ 100` on the archived main page) is real and unresolved, and it is
not load-bearing: `n = 5` is on both lists, and only `n = 5` is used.
The two lists are reconcilable if the rigid page also lists rigid-but-inoptimal
packings, which its preamble allows.
Recommendation (not a condition): archive the rigid page under `packing/resources/` so
the tension can be checked from the repository.

* * *

## 5. Gaps, all named

Disclosed by the authors, checked accurate:

1. **BCR Proposition 8.1.13 unread in print** — see §2.4. Non-blocking: the needed
   statement is attested by a BCR author and derivable from the primary-text continuous
   version, and the Milnor route is a third derivation.
   What is unconfirmed is the proposition’s number and wording in the printed book.
2. **SOSC theorem numbering from memory** (Nocedal–Wright 12.6, McCormick 1967,
   Fiacco–McCormick 1968) — on the non-acceptance route only; Theorem 11 is proved in
   full.
3. **Prior-art scoping adopted from the coordinator’s survey** ([CW96] Thm 4.3.1 shape
   match, disk-jamming sign requirement, Donev 2007 deferral) — unverified against
   primary texts by the packet lane; carried outside the claim in X-012 §7.4/§8.5, which
   is the right place. I read the survey’s verbatim quotations and they support the
   scoping.
4. **Instrument binds the restricted second jet along `e_{u4}` only** — sufficient:
   Lemma 8 at order `2m` and Theorem 11 both consume only `e^T H_j e`. The packet’s own
   `verify_chart.py` checks the full `J^T H J` on all 20 rows.
5. **Instrument’s reduction audit samples only inside `N`** — irrelevant to the proof
   (§2.3).
6. **No numerical isolation radius** — not claimed, not required by H-060.
7. **Kingbird thirteen-versus-four list tension** — non-load-bearing (§4).

Found by this review, none load-bearing:

8. §1.3 (i), “a nonconstant continuous path leaves every neighbourhood’s singleton”, is
   terse: a path can be constant on an initial segment; take the supremum of the
   constant initial interval.
   One sentence; the conclusion holds.
9. X-012’s status line and §8.4 still say `instrument_ready: false` and “the review has
   not passed”, which was true at installation and is now stale relative to H-060 and
   exp-058 (`instrument_ready: true` at 743fd18a). A documentation-pass item.
10. The packet’s §4.1 cites arXiv:2301.00128 for the Nash lemma with a Milnor
    attribution that the source check found to be an over-attribution; X-012 withdrew
    it. The frozen packet still carries it (it is frozen); the installed record is
    correct.
11. The one-variable Puiseux structure theorem that bridges BPR’s continuous lemma to
    the analytic one (§2.4) is not cited by the packet, which takes the Nash lemma
    directly. Adding it as the fallback derivation would make §4 independent of the
    unopened page.

Nothing found that makes an infeasible direction look feasible, that weakens the frozen
criterion, or that changes any exact quantity.

* * *

## 6. Replay (after 09:58Z)

Three layers, from most to least independent of the authors’ code:

1. **Reviewer’s reconstruction** (`independent_check.py`, sympy only, no shared code):
   pose and chart rebuilt from §1.1; all 400 elementary polynomials evaluated and
   classified by exact sign in `Q(√2)`; the 20 rows’ gradients, the `t4` column, the
   restriction of each pair row to the flex line, the packet’s displayed `g̃_3`, the
   midpoint property, `q_geo = −1/2`; the cone by exact rational LP *and* by 28
   certificates the reviewer derived by hand from the row inequalities; the self-stress
   and `w · q`; T-012’s 28 stored certificates and self-stress replayed against the
   reviewer’s own `S A_chart`; Lemma 8 on random arcs with `m = 2, 3`; the order-`2m`
   identity; a numerical sphere search; the packet SHA-256.
2. **The packet’s own scripts** (`verify_chart.py`, `sosc_check.py`,
   `midpoint_check.py`, `margins.py`, `print_polys.py`), run read-only from `bc152/`,
   with their digests compared to the exp-058 record.
3. **The instrument** (`sqpack.local_rigidity` via the author’s `build_receipt.py`),
   from clean temporary roots under normal and `-O` Python: readiness, all eight
   controls, counts, binding, neighbourhood, provenance.

### 6.1 Reviewer’s reconstruction — `independent_check.py`, exit 0, “ALL REVIEWER CHECKS PASSED”

Python 3.14.7, sympy 1.14.0, `packing/.venv/bin/python3`. Output in
`independent_check.out`. Everything below was computed from the pose of §1.1 with no
import from the packet, `sqpack`, `devtools` or the instrument (the one repository file
read is T-012’s JSON, in §5 of the script).

| claim | reviewer’s result |
| --- | --- |
| chart identities, `2 atan t = 2t − (2/3)t^3 + O(t^5)` | exact |
| 80 wall–corner functions | 16 zero, 64 strictly positive, 0 negative; multiset `1 ×16, 1 + r/2 ×16, 2 + r/2 ×16, 1 + r/4 ×8, 1 − r/4 ×4, 1 + 3r/4 ×4`; minimum `1 − r/4` |
| 320 pair functions | 4 touching pairs `(0,4),(1,4),(2,4),(3,4)`, each with exactly one satisfied branch `(4,3),(4,0),(4,2),(4,1)` and exactly one zero corner `2,3,1,0`; 6 non-touching pairs each with a strictly positive branch |
| 28 negative witnesses | one per violated branch; values equal the packet’s table row for row; least negative `−r/4` |
| strict conditions of `N` | `64 + 24 + 12 + 28 = 128` |
| the 20 rows | exactly the 16 vanishing wall margins and the 4 zero pair corners, in T-012’s `contacts.detail` order; all vanish at the pose |
| gradients | all 20 rows equal the packet’s §2.5 table; column `t4` identically zero |
| `q_chart` | `−2` on rows 3, 9, 11, 15; `0` elsewhere; each pair row restricted to `z = t4 e_{t4}` is exactly `−t4^2`; each wall row restricted is `0` |
| packet’s displayed `g̃_3` | equals the reviewer’s row 3 as a polynomial |
| geometric rotation gap | `(cos δ − 1)/2`, `q_geo = −1/2`, so `q_chart = 4 q_geo` |
| midpoint property | along-edge parameter exactly `1/2` for all four contacts |
| `S A_chart` | rational |
| first-order cone | **28 reviewer-built Farkas certificates** (derived by hand from the row inequalities, §2.5 of this review) verify `w ≥ 0`, `w^T (S A) = ±e_k` for all 14 pinned coordinates. (sympy’s simplex raised `InfeasibleLPError: Oscillating system` on the box-bounded LP; the LP was therefore not used and the cone rests on the certificates, which need no LP.) |
| self-stress | `w = (1/2, 1/2, r/2, 1/2, r/2, 1/2)` on rows 5, 8, 9, 10, 11, 12: `w ≥ 0`, `w^T A_chart = 0`, `w · q_chart = −2√2`, `w · q_geo = −√2/2`; `Φ = Σ w_j g̃_j` has zero gradient and restricts to `−√2 · t4^2` on the flex line |
| T-012 record | row order equals `contacts.detail`; cone recorded one-dimensional with `w4` free; **all 28 stored certificates replay** on the reviewer’s `S A_chart` with targets `±J_kk e_k`; the stored self-stress `w̃` is nonnegative with `w̃^T S A_chart = 0` and `S w̃` equals the packet’s `w` exactly |
| Lemma 8 | on random rational arcs with `m = 2` and `m = 3`: orders `< m` vanish, orders `m..2m−1` equal `a_j · a_k`, order `2m` equals `a_j · a_{2m} + (1/2) a_m^T H_j a_m`, for all 20 rows |
| order-`2m` identity | `w^T (A a_{2m} + (λ^2/2) q) = −√2 λ^2` identically in `a_{2m}`; the pure flex arc `t4 = s^2/3` has order-4 coefficient `−1/9` on every pair row |
| numerical sanity (not proof) | best `min_j g̃_j` over sampled spheres: `−1.20e−2` at `ρ = 0.1`, `−8.02e−4` at `ρ = 0.01`, `−6.25e−5` at `ρ = 0.001`; along the flex line exactly `−ρ^2` |
| packet digest | `28343b743e689fc99968d589a542d9022d061de8ec3ae5100bf4ef4930e40b6b`, 925 lines — equals the frozen hash in X-012 and exp-058 |

### 6.2 The packet’s scripts — all pass, digests equal the record

Run read-only from `bc152/` with `PYTHONPATH=packing`: `verify_chart.py` → “ALL CHECKS
PASSED” (pose corner-for-corner from `cases.gobel5`; 16/64 and 4/6; `A_chart = A_geo J`;
`H_chart = J^T H_geo J` on all 20 rows; `q_chart = 4 q_geo`; `−t4^2`; the 28
certificates and self-stress on `S A_chart`); `sosc_check.py` → “SOSC numbers replay”
(`−√2/2`, `−2√2`, the `μ = 1` signs, the threshold); `midpoint_check.py` → all four
exact midpoints; `margins.py` → the multiset; `print_polys.py` → the §2.5 table.
All seven script files in `bc152/` hash to the digests retained in
`exp-058-h-060-n5-chart-and-proof.json` (`937f5f4d…`, `e551cb34…`, `9331844d…`,
`14f98cc5…`, `0ca24178…`, `234c14bd…`, `8743b1ff…`).

### 6.3 The instrument — replayed build stated exactly

Replayed with the author’s `build_receipt.py` (`bc152-instrument/build_receipt.py`,
copied) from clean roots `bc153/replay/instrument/{normal,optimized}`, `cd packing`,
`PYTHONPATH=packing`, under `python3` and `python3 -O`:

- payload digest `2ffd1222263b32cd2a2da2d724134544a595354030bad1355f7b761893004bd0`,
  identical under both interpreters; certificate and receipt byte-identical across
  interpreters (`bcc6381a…`, `4281af75…`).
- `ready True`, `controls_all_reject True`, `count_disagreements {}`, refusals `[]`;
  `isolation_decided False` (unconditional, as designed).
- counts: 80 wall (16/64), 10 pairs (4/6), 80 branches, 320 corner inequalities, active
  total 20; expected cardinality equals actual.
- neighbourhood: 128 strict conditions — 64 `inactive-wall-stays-slack`, 24
  `noncontact-pair-stays-separated`, 12 `active-branch-nontouching-feature-stays-slack`
  (positive), 28 `competing-branch-stays-refuted` (negative); `valid True`. These are
  the packet’s `N` exactly, by role and by count.
- binding: 20 rows, `gradient_matches` all true, `second_jet_matches` all true
  (restricted jet along `e_{u4}/2`), free variables correspond (`u4` ↔ `w4`), transform
  `diag(1,1,2)` per square, `holds True`.
- probe: 180 axis points, no feasible neighbour.
  Reduction audit: 304 points, 252 inside `U`, 252 agreements, 0 counterexamples
  (corroboration only, as §2.3 says).
- controls: `changed_feature`, `zero_margin`, `omitted_constraint`, `invented_contact`,
  `side_release`, `wrong_chart`, `certificate_drift`, `exp034_angle_and_slide` — all
  eight `rejected True`.
- provenance: `source_digest ad32062e5a01…`, `tree_matches True`, `paths_differing []`,
  observed commit `ceff4400` (repository HEAD at replay time).

**Which build this is.** It is the *current* build — `source_digest ad32062e…`, the one
H-060 and exp-058 record as `bd450cb6…` and describe as “not itself claimed to be
reviewed” — not the reviewed build `743fd18a…`. My leaf-diff of my certificate against
the author’s current certificate (`bc152-instrument/normal/`, digest `bd450cb6…`) shows
**exactly one differing leaf**, `/claim_boundary/provenance/pinned_commit` (`15ebfa98` →
`ceff4400`): an unrelated commit landed in between, and the record’s documented
sensitivity of the observed-commit mechanism is all that moved.
My leaf-diff against the instrument reviewer’s replay of the reviewed build
(`bc152-review/replay4/`, digest `eccf0e1e…` at `fe8bccde`, `source_digest 9382bae1…`)
shows differences only under `/claim_boundary/provenance` — `note`, `pinned_commit`,
`source_digest`, and three added `source_files` entries (`sqpack/field.py`,
`cases/gobel5/packing.py`, `devtools/assess_n5_rigidity.py`) — and in no margin, count,
row, jet, control verdict or determination leaf.
That confirms, independently of the record’s own statement, that the current build
differs from the reviewed one in provenance metadata only.
So the H-060 readiness PASS at `743fd18a…` carries over to what I replayed, and I
replayed it myself.

### 6.4 Provenance widening attempted after the lease (negative result, recorded)

I tried to find citations of `[BCR, Prop. 8.1.13]` from author groups other than
Fernando’s. Web search surfaced only that group and papers that cite BCR elsewhere: Savi
(arXiv:2302.04673) and Carbone (arXiv:2507.17387, citing BCR 8.1.6 and 8.1.8 —
consistent numbering for §8.1, but not the lemma); Carbone–Fernando (arXiv:2306.00401)
is the same group. Kollár’s Bull.
AMS 2017 survey and Hrushovski–Pillay (arXiv:1105.2660), both fetched and text-extracted
(`bc153/prov/`), cite BCR but not a curve-selection lemma.
Aizenbud–Gourevitch’s Weizmann PDF answered 503/52 on three attempts.
So the “one author group” status of the *verbatim uses* stands; what carries the
citation is Coste’s own statement and derivation (§2.4), verified first-hand.

### 6.5 The BPR-to-Nash bridge, written out so it can be checked without re-derivation

Two cited facts, then the derivation.
Only (F1) is on a page that was read; (F2) is stated with a proof sketch by Coste in the
same notes and is the classical Newton–Puiseux fact for one-variable semialgebraic
functions.

- **(F1)** Basu–Pollack–Roy, *Algorithms in Real Algebraic Geometry*, Theorem 3.22
  (posted 2016 revision; Theorem 3.19 in the 2006 print), verbatim from the authors’
  posted text: for a semialgebraic `S ⊂ R^k` and `x ∈ S̄` there is a *continuous
  semialgebraic* `γ : [0,1) → R^k` with `γ(0) = x` and `γ((0,1)) ⊂ S`.
- **(F2)** (Coste, *Real Algebraic Sets*, §1.5, the paragraph before Theorem 1.15; BCR
  §8.1 is where it is proved) For a continuous semialgebraic `f : [0,1) → R` there are a
  positive integer `p` and a Nash function `f̃ : (−ε, ε) → R` with `f̃(u) = f(u^p)` for
  `u ∈ [0, ε)`. Sketch, as Coste gives it: the graph of `f` on a small `(0, ε)` is a
  branch of a real algebraic curve `P(t, y) = 0`, parametrised by a real Puiseux series
  `y = φ(t^{1/p})` (Newton–Puiseux), with no negative powers because `f` extends
  continuously to `0`; an algebraic Puiseux series converges; so `f(u^p) = e(u)` with
  `e` an ordinary convergent series satisfying `P(u^p, e(u)) = 0`, i.e. a Nash germ.

*Derivation.* Suppose `P^0` is not isolated.
Then `0 ∈ Cl(A)` for `A = F \ {0}` (§2.4). By (F1) with `S = A`, `x = 0`, take
`γ = (γ_1, …, γ_15) : [0,1) → R^15` continuous semialgebraic, `γ(0) = 0`,
`γ((0,1)) ⊂ A`. Each `γ_i` is continuous semialgebraic on `[0,1)`, so by (F2) there are
`p_i` and Nash `γ̃_i` on `(−ε_i, ε_i)` with `γ̃_i(u) = γ_i(u^{p_i})` on `[0, ε_i)`. Put
`P = lcm(p_1, …, p_15)` and `Γ_i(u) := γ̃_i(u^{P/p_i})`, a Nash function on a symmetric
interval about `0` (a Nash function composed with the polynomial `u ↦ u^{P/p_i}`), with
`Γ_i(u) = γ_i(u^P)` for `0 ≤ u < ε_i^{p_i/P}`. With `ε := min_i ε_i^{p_i/P} > 0`,
`Γ := (Γ_1, …, Γ_15)` is Nash — in particular real-analytic — on `(−ε, ε)`,
`Γ(0) = γ(0) = 0`, and `Γ((0, ε)) = γ((0, ε^P)) ⊂ A`. That is precisely the arc
Corollary 4.3 consumes; since `0 ∉ A`, `Γ(u) ≠ 0` for `u ∈ (0, ε)`, so `Γ` is
nonconstant and the identity theorem gives the least `m ≥ 1` with `a_m ≠ 0`. Nothing
about `Γ` beyond real-analyticity at `0` and the inclusion on `(0, ε)` is used
afterwards. □

The dependence on the unopened page of BCR Proposition 8.1.13 is thereby replaced by
(F1), read in primary text, plus (F2), a classical one-variable fact attested with a
proof sketch by an author of BCR; the Milnor route with the packet’s finite-union
reduction is a third, independent derivation.
That is the footing on which I call the provenance caveat non-blocking.

* * *

## 7. Exact scope at which the theorem may be claimed

**Theorem (fixed-side local rigidity of Goebel’s `n = 5` pose).** Let `s = 2 + √2/2` and
let `P^0` be Goebel’s labeled pose: squares `0..3` axis-aligned with centres
`(1/2, 1/2)`, `(s − 1/2, 1/2)`, `(1/2, s − 1/2)`, `(s − 1/2, s − 1/2)` and square `4`
with centre `(s/2, s/2)` at angle `π/4`, corners ordered counter-clockwise as in
`cases/gobel5`. In the labeled configuration space `C = (R^2 × S^1)^5`, `P^0` is an
isolated point of `Feas(s)`, the set of configurations in which every closed unit square
lies in the closed container `[0, s]^2` and the squares have pairwise disjoint
interiors.
Equivalently: there is no nonconstant continuous path in `Feas(s)` starting at
`P^0`, and no sequence of points of `Feas(s) \ {P^0}` converges to `P^0`. Consequently
the unlabeled packing is rigid in Kingbird’s fixed-side sense.

Established exactly over `Q(√2)`, by the registered route (chart, complete 400-function
accounting, curve selection on the punctured set, order-`2m` coefficient induction),
corroborated by an independent second route (second-order sufficiency, `C^2` hypotheses
only).

**Not claimed, and not to be claimed on this review:** a numerical isolation radius;
rigidity when the container side is a variable (false, X-007); global uniqueness of the
`n = 5` optimum; rigidity of any other optimal `n = 5` packing; applicability of the
Connelly–Whiteley tensegrity theorems as stated (their hypotheses are distance members;
none was invoked); novelty of the closing principle, the curve-selection proof shape,
the half-angle rationalization, the separating-axis accounting or Farkas certification.
Novelty: S3 as worded in §4, `apparently-novel` in the repository’s sense.

* * *

## 8. Recommendations (none is a condition of the pass)

1. In the installed record, add the one-sentence bridge of §2.4 (continuous curve
   selection from primary text + one-variable Puiseux + `s = u^N`) as the fallback
   derivation of the analytic lemma, so §4 no longer rests on an unopened page.
2. Fix the stale `instrument_ready: false` in X-012’s status line and §8.4.
3. Add the supremum sentence to §1.3 (i).
4. Archive Kingbird’s rigid page under `packing/resources/` and resolve or record the
   thirteen-versus-four tension there.
5. Carry the prior-art scoping exactly as X-012 §7.4 now does — outside the claim.

## 9. Reviewer artifacts (all under `scratchpad/bc153/`)

- `h060-proof-review.md` — this document.
- `independent_check.py`, `independent_check.out` — the reviewer’s from-scratch
  reconstruction and checks (sections 0–8 listed in its docstring).
- `run_replay.sh`, `run_replay.log` — the replay runner and its transcript
  (09:40:19Z–09:41:30Z).
- `replay/packet/*.out` — outputs of the packet’s `verify_chart.py`, `sosc_check.py`,
  `midpoint_check.py`, `margins.py`, `print_polys.py`.
- `replay/instrument/{normal,optimized}/` — the instrument’s certificate, receipt and
  copied sources from clean roots under both interpreters; `normal.out`,
  `optimized.out`.
- `prov/` — the two PDFs fetched for the provenance-widening attempt and their text
  extractions (negative result, §6.4).

Timing: reading and mathematics from 08:46Z; no replay, test, interpreter or git process
before the coordinator released the lease (09:36:29Z); replay 09:40Z–09:41Z; document
finalised after. No repository file modified, staged or committed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
