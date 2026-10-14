# The upper bound AT ŝ: route decision and the attainment lemma (A63, 2026-09-01; §7 A69, 2026-09-01)

> **STATUS UPDATE (A69).** The (c-idl) certificate of §6 has been FOUND and exactly
> verified: `certs/cidl_identity.json` + `certs/verify_cidl.py` (PASS, 0.7 s, stdlib
> rationals). The identity ŝ_A22 = ŝ_octic is now certificate-backed at the same TCB
> tier as the rest of the Python layer; only the Lean replay (named obligation
> CIDL-LEAN, §7.5) keeps `shatA22_eq_shat` an axiom. §7 has the construction. The
> §4 (c-alg) "compositum degree 56" obstacle is VOID — based on spurious A03 minpoly
> data (§7.4): every coordinate of ẑ lies in ℚ(t̂), degree 8.

Target: A62 finding F2 / Lean axioms `zhat`, `trump_packs_at_shat` — the equality claim's UB
half. A62 named two routes: (a) A22's Krawczyk existence + feasibility; (b) closedness of
{s : Fits 11 s} plus a certified sequence of sides ↓ ŝ. This file executes the cheap half —
the attainment/closedness lemma and the EXACT check of what route (b) can and cannot deliver —
and reduces route (a) to one precisely-localised algebraic gap with two closure specs.
Labels: [T] proved, [M] computed exact, [F] finding, [C] open.

## 1 [T] Lemma A (the fits-ray): {s : Fits 11 s} is a closed ray [s(11), ∞), and the infimum
is attained

(i) *Monotone.* If 11 unit squares pack in [0, s]² and s ≤ s′ then the same squares pack in
[0, s′]² (container inclusion). So {s : Fits} is up-closed.

(ii) *Closed.* Let s_n → s∞ with Fits(s_n); WLOG s_n ≤ s∞ + 1 =: S. Represent each packing by
its configuration z_n ∈ K := ([0, S]² × [0, 1])¹¹ (centres, t = tan(θ/2); the `parametrize`
lemma — every unit square in the container is PSq.set of some (c, t), elementary). K is
compact; pass to a convergent subsequence z_n → z∞. Each defining condition survives the limit:
* containment: corner coordinates are continuous in (c, t) and closed inequalities pass to
  limits (s_n → s∞ on the right-hand side);
* pairwise interior-disjointness: overlapping interiors is an OPEN condition on configuration
  pairs (if int Q ∩ int Q′ ∋ x, then squares within ε of (Q, Q′) still overlap near x), so its
  complement is closed;
* unit size and squareness: built into the parametrisation.
So z∞ is a packing at side s∞: Fits(s∞). ∎

(iii) With (i)+(ii): {s : Fits} = [m, ∞) with m = min = sInf = s(11). This is D1 restated on
the set level; it also discharges the PROSE of the Lean axiom `attained` (formalisation of (ii)
is the known cost: closedness of `Fits` — A62 note on `attained` unchanged) and isolates
`parametrize` as its only geometric input.

**Consequence (the honest reduction).** s(11) ≤ s″ for every certified side s″; and
s(11) = the side of ANY feasible configuration that attains the minimum. The UB-at-ŝ question
is EXACTLY: "exhibit a packing at side ŝ" — no compactness argument can manufacture one from
sides > ŝ alone, because nothing forces the minimum DOWN to ŝ except an actual packing there
(the lower-bound machinery only forces it UP to ≥ ŝ).

## 2 [T/F] Route (b) checked exactly: REFUTED as a finite certificate route

* **Single certificate + scaling [F].** Scaling a packing changes the squares' side with the
  container: 11 unit squares in [0, σ]² ⟺ 11 λ-side squares in [0, λσ]². No λ ≠ 1 produces
  UNIT squares at a smaller side; the certified `trump11_tight` packing at
  s₁ = 3.877083591023 yields Fits(s) for s ≥ s₁ (Lemma A(i)) and NOTHING below s₁. The
  "scaling argument" the brief asked to check does not exist.
* **Any finite set of fixed-side certificates.** `checkPacking` requires strictly positive
  margins (A62 F2), so every certified side is a rational STRICTLY above ŝ; a finite set has a
  minimum s_min > ŝ and delivers only s(11) ≤ s_min. A sequence ↓ ŝ needs infinitely many
  certificates — not a finite proof object.
* **Parametric UB certificate (a rational curve of packings z(τ), σ(z(τ)) ↓ ŝ).** On each
  smooth piece σ(z(τ)) is a polynomial in τ with rational coefficients; its limit as τ → 0⁺ is
  its value at 0, a RATIONAL number ≠ ŝ (ŝ is a degree-8 algebraic irrational, T1 certificate).
  So no rational-data curve reaches ŝ in the limit; curve data in ℚ(ŝ) is exactly route (c)
  below, with the same algebraic cost. **Route (b) is closed off, not merely unexecuted.**

## 3 Route (a): what A22 already proves, and the ONE remaining gap

A22 (`attempts/A22-local-rigidity/`, certificate + standalone `recheck.py`) proves, modulo the
mpmath.iv trust item (TCB T3):

* existence + uniqueness of the contact solution ẑ in the box N = box(z0, 5e-4), with
  ‖ẑ − z0‖∞ ≤ 1e-50 (Krawczyk);
* **feasibility: ẑ IS a packing at its own side** (A22 §4 — exact flush/coincidence arguments
  plus interval SAT with min margins 0.0249/0.549);
* strict local optimality: every feasible z ∈ N has s(z) ≥ ŝ_A22 := s(ẑ), equality iff z = ẑ.

So **Fits(ŝ_A22) holds — the UB at the INTRINSIC value ŝ_A22 is already certified**, and with
Lemma A and the lower-bound axioms the composed equality is s(11) = ŝ_A22. What is NOT proved
is the statement-identity ŝ_A22 = ŝ_octic (the octic root the theorem names — A22 §7 gap 2:
PSLQ-found, enclosure-consistent, never derived).

**[M] How tightly the two are now tied** (using T1's isolation certificate):
* z0's s-coordinate = 3.87708359002281417730789706… lies in (a, b) = (3.877083, 3.877084)
  with ≥ 4.1e-7 clearance on both sides; ‖ŝ_A22 − z0_s‖ ≤ 1e-50, so ŝ_A22 ∈ (a, b).
* T1: the octic has exactly ONE root ŝ_octic in (a, b) (and exactly two real roots overall).
* A22 encloses octic(ŝ_A22) ∈ ±3.1e-45; T1's Taylor certificate gives octic′ ≥ 152.37 on
  [a, ∞); by the mean value theorem |ŝ_A22 − ŝ_octic| ≤ 3.1e-45 / 152.37 ≤ 2.1e-47.
* **Equality remains open [C]**: intervals can never prove it; it is an algebraic identity.

## 4 [C] Closure specs for the identification (choose either; both finite)

* **(c-alg) Exact number-field verification.** Verify that an exact algebraic point solves
  A22's 38-row curated system, with the side coordinate a root of the octic. Obstacle recorded
  by A53 L4: at least one coordinate of ẑ (the ε-off square's cy) has minimal polynomial of
  degree 7; since 7 ∤ 8, the coordinate field is NOT ℚ(ŝ_octic) — the verification field is a
  compositum of degree up to 56. Spec: a ~200-line exact checker doing arithmetic in
  ℚ[x]/(m(x)) for the compositum's primitive element (or componentwise in the two fields with
  resultant-certified compatibility), all sign gates via T1-style Sturm isolation + interval
  refinement — same TCB profile as `verify_sturm.py`, stdlib rationals only. Input data (the
  exact coordinates as polynomials in the primitive element) must first be RECOVERED (PSLQ/LLL
  from the 60-digit data, then verified exactly — recovery is untrusted search, verification is
  the certificate). This also upgrades A22 §7 gap 2 for good.
* **(a2-lean) t-reparametrised Krawczyk replay in Lean** (checklist F6, A28 §4) discharges the
  mpmath.iv trust item and formalises existence+feasibility, but does NOT by itself tie ŝ_A22
  to the octic; pair it with (c-alg) for the full statement, or with (S3-fallback) below.
* **(S3-fallback) Restate.** Publish with ŝ := ŝ_A22 (intrinsically defined by A22's
  certificate: "the side of the unique contact solution in N") and the octic as a certified
  remark ("agrees with the second root of […] to within 2.1e-47"). Checklist S3 explicitly
  sanctions this shape. Zero additional mathematics; the Lean `shat` would then be defined
  from the (replayed) Krawczyk certificate instead of the octic.

## 5 Verdict for the composition (state of `zhat` / `trump_packs_at_shat`)

* With ŝ read as ŝ_octic (current `TopLevel.lean`): the axioms remain OPEN; the discharge is
  (a2-lean) + (c-alg). Route (b) cannot discharge them and should be struck from the route
  list.
* With ŝ read as ŝ_A22 (fallback restatement): `trump_packs_at_shat` is certified TODAY
  (Python-interval TCB), and the honest composed theorem is s(11) = ŝ_A22 conditional on the
  lower-bound axioms, with |s(11) − ŝ_octic| ≤ 2.1e-47 unconditionally-on-the-same-axioms.
* Interval-only honest form (no A22 feasibility accepted): ŝ ≤ s(11) ≤ 3.877083591023,
  unchanged from A62.

## 6 [F/C] A64 assessment: can a resultant/interval sign argument beat the compositum?

Asked (A64 brief): does "agreement within 2.1e-47 + an interval enclosure of
octic(ŝ_A22)" support a SIGN argument, entirely in rationals, closing the identity?

**[F] No — and not for lack of precision.** A sign argument certifies strict
inequalities; equality of two algebraic numbers can follow from a finite computation
only via an exact algebraic input that supplies a SEPARATION GAP ("if ŝ_A22 ≠ ŝ_octic
then |ŝ_A22 − ŝ_octic| ≥ γ"), after which |diff| ≤ 2.1e-47 < γ would finish. A
Liouville/resultant gap for ŝ_A22 needs a degree AND height bound for its minimal
polynomial. Degree ≤ 56 is known (compositum), but the height is exactly what we do not
have without doing the elimination: a-priori arithmetic-Bézout height bounds through the
34-variable curated system are doubly exponential in the system size, giving γ far below
any reachable interval precision (tightening 2.1e-47 by re-running A22 at higher
precision changes nothing — the gap estimate loses by orders of magnitude of orders of
magnitude). The pure interval/sign route is closed off, not merely unexecuted; the 2018-
style "verify to 10^-k and wave at PSLQ" shortcut does not exist here.

**[C] (c-idl) — a THIRD closure spec, cheaper than (c-alg).** The identity follows from
a *saturated ideal-membership certificate*: polynomials q_k, r_i, h over ℚ (in the
t-parametrised variables, so every constraint row F_k is polynomial) with

    h · octic(s) = Σ_k q_k · F_k + Σ_i r_i · (c_i² + s_i² − 1),      h(ẑ) ≠ 0.

Evaluating at ẑ (where every F_k and every trig relation vanishes) gives
octic(ŝ_A22) = 0, and T1's isolation converts that to ŝ_A22 = ŝ_octic (ŝ_A22 lies in
the isolating interval by the 1e-50 enclosure). VERIFICATION is pure rational polynomial
identity checking plus ONE interval sign gate h(ẑ) ≠ 0 — same TCB profile as
`verify_sturm.py`, stdlib rationals, no number-field arithmetic, no recovery of exact
coordinates. The saturation factor h is necessary because the global variety of the
curated system has other components on which the octic need not vanish; h kills them.
The SEARCH for (q, r, h) (Gröbner basis / numerically-guided Macaulay linear algebra —
untrusted, only the printed certificate matters) is a bounded compute campaign — a
future attempt, not a today-task. (c-alg) remains valid but strictly costlier in TCB
(compositum arithmetic) and in recovery risk.

**[T] Lean-side execution (the fallback clause, without regressing A63).** Rather than
reverting `shat` to an opaque constant (the literal S3-fallback restatement would undo
A63's `shat_spec` theorem), `TopLevel.lean` now SPLITS the old `trump_packs_at_shat`
axiom into

* `shatA22 : ℝ` + `trump_packs_at_shatA22 : CfgPacking shatA22 zhat` — certified today
  (Python-interval TCB), and
* `shatA22_eq_shat : shatA22 = shat` — THE open identity, isolated as a single named
  axiom carrying the 2.1e-47 pin and the closure specs (c-alg)/(c-idl),

with `trump_packs_at_shat` recovered as a theorem. `#print axioms` on the composed
theorems now separates the certified feasibility from the open identity; discharging
(c-idl) later = replacing one axiom by a theorem, touching nothing else. The published
restatement s(11) = ŝ_A22 (§5) remains available by flipping which constant is primitive.

## 7 [T/M] (c-idl) EXECUTED: the saturated ideal-membership certificate (A69, 2026-09-01)

### 7.1 The reduction (theory; each step certified by A22)

A22's second Krawczyk system F~ (notes.md §3) pins the EXACT structure of ẑ: squares
0–5 axis-parallel with c0=(½,½), c1=(3/2,½), c2=(S−½,½), c3=(½,3/2), c4=(½,y4),
c5=(S−½,S−½), and squares 6–10 sharing exactly one angle θ̂. Substituting this
structure and the Weierstrass parametrisation t = tan(θ/2) (exact at θ̂ since
|θ̂| < π) into the 38 curated rows — ALL of which vanish at ẑ (A22 §3) — and clearing
the positive denominators (1+t²)^k row-wise: 20 rows vanish identically, and the 18
survivors collapse (each flush-tilted pair's two corner rows become rational multiples
of one another once the angles are equal) to **13 distinct generators**
G₀..G₁₂ ∈ ℚ[t, y4, x6..y10, S], each LINEAR in the 12 non-t variables with ℚ[t]
coefficients of degree ≤ 4:

    6 upright–tilted edge rows   E1c2-8e3, E2c3-8e0, E3c2-7e3, E4c1-7e2, E4c2-6e3, E5c0-9e1
    5 flush-tilted rows          E6c1-9e2, E7c1-8e2, E7c2-9e3, E8c2-10e3, E9c1-10e2
    2 tilted wall rows           W6c2[y=s], W10c1[x=s]

Every G_j vanishes at the A22 point P̂ = (t̂, ŷ4, x̂6..ŷ10, ŝ_A22).

### 7.2 The certificate (found by exact linear elimination — no Gröbner basis needed)

Take the 12 rows ≠ E1c2-8e3 as A(t)·x = b(t) (x the 12 unknowns, S last). With
Δ := det A (degree 34) and adjugate cofactors, Cramer gives polynomial identities
Δ·x_m − N_m = Σ_j adj_{mj}·G_j. The left-out row yields the consistency determinant
D(t) := Σ_m a₀_m N_m − Δ·b₀ (degree 35) with D = Δ·G₀ − Σ_j c_j G_j ∈ (G).
Factoring D over ℚ: exactly one irreducible factor vanishes at t̂,

    m(t) = 5t⁸ − 10t⁷ − 2t⁶ + 14t⁵ + 12t⁴ − 6t³ + 2t² + 2t − 1,

i.e. A03's PSLQ tan-half polynomial p(−t) — now DERIVED, not fitted; e := D/m has
degree 27 and gcd(e, m) = gcd(Δ, m) = 1. Setting G_oct := Σ_k a_k N_S^k Δ^{8−k}
(octic = Σ a_k s^k, deg G_oct = 272), exact division gives **m | G_oct** — the heart
of the matter — with g := G_oct/m, and the telescoped assembly

    e·Δ⁸·octic(S) = Σ_{j≠0} [ e·W_tel·adj_{S,j} − g·c_j ]·G_j + [ g·Δ ]·G₀ ,

W_tel the telescoping cofactor of ΔS − N_S in Δ⁸octic(S) − G_oct. Saturation factor
h = e·Δ⁸; cofactors are bivariate in (t, S). Certificate: `certs/cidl_identity.json`
(301 KB); the sizes are tame (no doubly-exponential wall — the §6 height-bound
pessimism applied to a-priori bounds, not to this structured system).

### 7.3 Verification and composition

`certs/verify_cidl.py` (stdlib fractions only) REBUILDS the 13 generators from the
A22 conventions (HALF/NHAT/eval_g), then checks exactly: [O] the octic is canonical;
[I] the polynomial identity above in ℚ[t,y4,x6..y10,S]; [G] Sturm: e and Δ have no
root in [3/10, 2/5]. PASS in 0.7 s; corruption gates qcoeff/e/rowspec/octic all FAIL
loudly. Composition to ŝ_A22 = ŝ_octic:

* G_j(P̂) = 0 (§7.1) and t̂ ∈ [3/10, 2/5] (A22 encloses θ̂ within 1e-50 of A03's
  rational angle, so θ̂/2 ∈ [0.35, 0.36]; x ≤ tan x ≤ x + x³/(3(1−x²)) on [0, 0.36]
  gives t̂ ∈ [0.35, 0.368] ⊂ [3/10, 2/5]);
* evaluating the identity at P̂: e(t̂)·Δ(t̂)⁸·octic(ŝ_A22) = 0, and [G] gives
  e(t̂)Δ(t̂) ≠ 0, so **octic(ŝ_A22) = 0**;
* ŝ_A22 ∈ (3.877083, 3.877084) (A22's 1e-50 enclosure, 4.1e-7 clearance), and the
  octic has exactly ONE root there (T1/`shat_spec`; its other real root lies in
  (−2,−1)), so **ŝ_A22 = ŝ = the octic's second real root**. ∎

TCB: exactly verify_sturm-class (stdlib rationals) for the new checker, PLUS the
already-trusted A22 certificate (mpmath.iv) for "G_j(P̂) = 0, enclosures". No new
trust items.

### 7.4 [F] Correction: the "degree-7 coordinate" does not exist

Since Δ(t̂) ≠ 0, the kept 12×12 system is nonsingular at t̂ and x̂ = A(t̂)⁻¹b(t̂):
**every coordinate of ẑ lies in ℚ(t̂), a degree-8 field.** A53 L4's obstacle (cy4 of
degree 7, hence 7 ∤ 8 and a compositum of degree up to 56 for (c-alg)) came from
A03's per-square `minpoly_cx/cy` JSON fields, which are findpoly ARTIFACTS: the
recorded degree-7 polynomial for cy4 evaluates to −8.0e8 at the true ŷ4 (250 dps) —
not small at all (same for cx2 = S − ½, which must have degree 8, yet carries an
8-coefficient entry). The true minimal polynomial of ŷ4, derived as the factor of
Res_t(m, Δ·Y − N_{y4}) vanishing at ŷ4 (residual 6e-255):

    256Y⁸ − 4608Y⁷ + 37376Y⁶ − 167040Y⁵ + 440352Y⁴ − 674912Y³ + 437376Y² + 327464Y − 599659.

A03's 60-digit coordinate STRINGS are fine (all 13 generators vanish to ≤ 6.7e-60 at
the A03 point); only the minpoly annotations are junk. (c-alg) would have been a
plain ℚ[t]/(m) verification after all — moot now.

### 7.5 [C] Named obligation CIDL-LEAN (the only remaining gap for `shatA22_eq_shat`)

Discharge = (i) reify the 13 generators, the cofactors, e, Δ in Lean and replay [O]/
[I]/[G] by `native_decide` over ℚ (A64's Measure382Check isolation pattern; the
cross-toolchain elaboration recipe applies verbatim); (ii) refine the A22 interface:
replace the opaque `shatA22` axiom pair by axioms asserting exactly A22's certified
content — ∃ (t̂, ŷ4, …, ŝ_A22) with all G_j = 0, t̂ ∈ [3/10, 2/5],
ŝ_A22 ∈ [3.877083, 3.877084], and `CfgPacking shatA22 zhat` — then `shatA22_eq_shat`
becomes a THEOREM via `shat_spec`. Zero new mathematics; pure engineering. Until
then the axiom stands with this certificate as its documented backing.

### 7.6 [T] CIDL-LEAN DISCHARGED (A78 T2, 2026-09-02)

`lean/PackingCertMathlib/PackingCertMathlib/{CidlPoly,CidlGen,CidlData,CidlCheck,CidlBridge}.lean`
(+ `lean/gen_cidl_lean.py`): the 13 generators are REBUILT in Lean from A22's
`HALF`/`NHAT`/`frame`/`row_wall`/`row_edge`/`ROWSPEC` (byte-for-byte the construction of
`verify_cidl.py`), the identity [I] and [O] are `native_decide` facts over ℚ in the isolated
module `CidlCheck.lean` (27 s), and the sign gates are proved STRONGER than [G]: `e < 0` and
`Δ < 0` on all of `[3/10, 2/5]` by a monomial interval bound (no Sturm chain needed in Lean).
`TopLevel.lean`: `shatA22_eq_shat` is a THEOREM; the single new interface axiom
`a22_exact_structure` asserts exactly (i)–(iii) of §7.5 — `t̂ ∈ [3/10, 2/5]`,
`ŝ_A22 ∈ [3.877083, 3.877084]`, the 13 generators vanish at `P̂` built from `zhat`'s coordinates
— i.e. A22's certified content and nothing algebraic. Notes:
`attempts/A78-lean-wave6/notes/t2_cidl.md`.
