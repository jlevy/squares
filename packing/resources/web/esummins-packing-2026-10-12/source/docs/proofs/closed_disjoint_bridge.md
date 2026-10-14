# The closed-vs-interior-disjoint bridge (Lemma B, the S4/F9 discharge) — A63, 2026-09-01

The missing lemma A62 finding F9 named: `verify_case.py`'s PASS claim (spec
`docs/specs/case_lp_certificate_v1.md` §1) speaks about families of **pairwise-disjoint closed**
unit squares, while the composition applies kills to packings that are only
**interior-disjoint** (contacts allowed — every minimiser has them; touching squares can share a
μ-atom, which breaks the pigeonhole μ(total) ≥ b). This file states and proves the repair — the
λ-dilation-with-pin-slack lemma — with the exact hypotheses per kill application, quantifies it
against the deployed certificate corpus, and records which certificate uses do NOT go through.

Labels: [T] proved theorem, [M] measured/computed exact, [F] finding.

Conventions. A *packing at side m* is a family of 11 closed unit squares in [0, m]² with pairwise
disjoint interiors. For λ ≥ 1 the **centre dilation** Δ_λ maps a unit square with centre c and
orientation θ to the unit square with centre λc and the same orientation θ (sizes unchanged).
Slot/pin coordinates at side s are affine, k(s) = α + β·s with β ∈ {0,1} and
α ∈ {±1/2, ±3/2, ±5/2} (A56 P1); |α| ≤ 5/2 throughout the census.

## B.0 [T] Three elementary facts about Δ_λ

Let P = (Q_1, …, Q_11) be a packing at side m and λ > 1.

**(a) Strict disjointness.** For any pair (i, j) there is a unit vector u with the projections
of Q_i, Q_j onto u contained in [p_i − w_i, p_i + w_i], [p_j − w_j, p_j + w_j], p = c·u,
w ∈ [1/2, √2/2], and p_j − p_i ≥ w_i + w_j ≥ 1 (separating-axis for convex bodies with disjoint
interiors; the projection half-width of a unit square is ≥ 1/2 on every axis). After Δ_λ the
projection gap along the same u is λ(p_j − p_i) − (w_i + w_j) ≥ (λ − 1)(w_i + w_j) ≥ λ − 1 > 0.
Hence Δ_λQ_i and Δ_λQ_j are disjoint **as closed sets**, with SAT gap ≥ λ − 1. ∎

**(b) Containment.** If Q ⊆ [0, m]² then Δ_λQ ⊆ [0, λm]²: for the extreme x-coordinates,
writing h ∈ [1/2, √2/2] for the corner offset, min-x(Δ_λQ) = λc_x − h = λ(c_x − h) + (λ−1)h ≥ 0
and max-x(Δ_λQ) = λc_x + h = λ(c_x + h) − (λ−1)h ≤ λm; same in y. ∎

**(c) Pin tracking.** If Q is axis-aligned with centre at the side-m slot (α_x + β_x m,
α_y + β_y m), then Δ_λQ is axis-aligned with centre at distance exactly
((λ−1)|α_x|, (λ−1)|α_y|) ≤ (λ−1)·(5/2) (per coordinate) from the side-λm slot
(α_x + β_x·λm, α_y + β_y·λm). Proof: λ(α + βm) − (α + βλm) = (λ−1)α. ∎

## B.1 [T] Lemma B (the bridge)

**Lemma B.** Let C be a `case-lp-certificate-v1` PASS at side s″ with cores K_1 … K_r
(half-side a_j ≥ 0, orientation θ_j, any centres) and **empty `nofams`**, budget b = 11 − r,
Σw < b. Let P be a packing at side m < s″ (interior-disjoint suffices), λ = s″/m, and suppose
there are r distinct squares Q_{i_1}, …, Q_{i_r} of P such that

  (H) for every j: the dilated square Δ_λQ_{i_j} **contains** K_j, and K_j is contained in the
      **open interior** of Δ_λQ_{i_j}.

Then no such P exists.

*Proof.* Suppose P exists and consider the family Δ_λP in [0, s″]² (B.0(b)). Its members are
closed unit squares, pairwise disjoint as closed sets (B.0(a)). Each core K_j is contained in
the family square Δ_λQ_{i_j} (H). Let G be the ≥ 11 − r = b squares of Δ_λP other than the
Δ_λQ_{i_j}. Each Q′ ∈ G:

* is an admissible placement (closed unit square ⊆ [0, s″]²);
* **meets no core**: Q′ is disjoint from Δ_λQ_{i_j} ⊇ K_j, so Q′ ∩ K_j = ∅;
* is not NO-exempt (`nofams` empty).

By the certificate claim (P2), μ(Q′) ≥ 1 for every Q′ ∈ G. The members of G are pairwise
disjoint **closed** sets, so no atom lies in two of them and μ is additive over G:
μ(total) ≥ Σ_{Q′∈G} μ(Q′) ≥ b. This contradicts (P1) Σw < b. ∎

Remarks. (i) The strictness produced by λ > 1 is used exactly twice: atom additivity over G, and
G-vs-pin disjointness (which makes "meets no core" trivial). (ii) At λ = 1 the lemma FAILS in
general — this is the original S4 trap, and it is why every kill application below routes
through a certified side **strictly above** the packing's own side. (iii) Interior containment
in (H) is automatic from strict containment with positive margin; the degenerate case "core
containment tight" (margin 0) is excluded by (H) and must be checked per certificate (B.2).

## B.2 [T+M] Slot instantiation and the corpus margin ρ

**Corollary B′ (slot form).** Let S be a Young class with k pins, C a PASS for S at side s″ with
the k cores centred at slots_S(s″), core half-side a, orientation θ_c, empty nofams. Define the
**containment margin**

  ρ(C) = 1/2 − a·(cos θ_c + sin θ_c)   (per-axis bounding half-width of the tilted core),

and A(C) = max over core coordinates of |α| (≤ 5/2). If P is a packing at side m < s″ containing
axis-aligned unit squares centred at all slots of slots_S(m), and

  (H′)  (s″/m − 1) · A(C)  <  ρ(C),

then no such P exists. *Proof.* By B.0(c) the dilated pin square's centre is within
(λ−1)|α| < ρ(C) of the s″-slot = core centre, both axis-aligned up to the core tilt; the core's
axis-parallel bounding box (half-width a(cosθ_c + sinθ_c) = 1/2 − ρ(C)) then sits inside the
dilated pin square with positive margin, giving (H). Apply Lemma B. ∎

**Corpus numbers [M]** (`a = 16383999967232/32768001953125`, `tm = 1/33554432`, uniform across
all 68 scanned kill certificates — A53 certs_wip 52, A54 4, A55 10, A55/k3_ext 1, A57 base —
all with empty nofams; scan of 2026-09-01):

  ρ = 73787046228886605157/73786980692884783104003906250 ≈ 1.0000009e-9  (> 0 EXACTLY),
  A = 5/2, so (H′) reads  s″/m − 1 < 4.0000e-10,  i.e. s″ − m ≲ 1.55e-9.

**The margin is strictly positive but nine orders of magnitude smaller than the window.**
Consequences, per certificate family:

* **Parametric certificates (A56/A61, `parametric_kill_certificate_v1`).** For every
  m ∈ [3.82, ŝ] in the certified s-cell family, rationals are dense: choose rational
  s″ ∈ (m, m(1 + 4.0e-10)) inside a cell (m < ŝ < s0 = 969271/250000, and the cells cover
  [3.82, s0] with rational endpoints, so such s″ exists whenever the cell coverage reaches
  above m). Specialise the parametric PASS at s″ (A56 P3 soundness theorem) and apply B′.
  **This is the complete, written discharge of the S4 obligation for every full-window
  stratum: `stratum_kill` instances at every m ∈ [3.82, ŝ] for the 38 (+A61 as they land)
  full-window classes.** The verifier-checkable hypotheses are exactly: (i) PASS on cells
  covering (m, m + m·4e-10) for each m in the window — implied by coverage of [3.82, s0];
  (ii) ρ(C) > 0 exact (computed above, once, from the uniform core parameters);
  (iii) `nofams` empty. Nothing else.

* **Fixed-side (s0-only) certificates — A57 k5_11/k5_16 sub-trees, A60 zone-tree leaves, the
  A61 stragglers until their parametric forms land. [F — HEADLINE]** A kill certified at s0
  only can be applied, via B′, exactly to packings at sides m ∈ [s0/(1 + 4.0e-10), s0] — a
  shell of relative width 4e-10 below s0. Since ŝ < s0 with (s0 − ŝ)/ŝ ≈ 1.057e-7 ≫ 4e-10,
  **an s0-only certificate with the library's ε-fat cores instantiates the kill axiom at NO
  side of the window [3.82, ŝ] whatsoever.** "Valid at s0 only" in the A56/A62 ledgers
  overstates what is usable: the certified statement at s0 is about a side the composition
  never visits. (This makes F6's coverage shortfall exact rather than qualitative. It does NOT
  contradict A56's refuted monotone transfer — it is the quantified form of the same fact.)

* **Atlas value certificates (`atlas_value_certificate_v1`).** Off the live tree (depgraph
  X.ATLAS). Lemma B does not apply to them (their PASS bounds σ from below on a box; the
  dilation Δ_λ does not commute with σ for unit squares). If the atlas route is ever revived it
  needs its own bridge; do not cite Lemma B for it.

* **Measure certificates (Theorem 1, `certs/measure_certificate_3.82.json`).** No bridge
  needed: the 3.82 claim is "no 11-family of pairwise-disjoint closed squares", applied to a
  hypothetical packing at side m < 3.82 by dilating with ANY λ = s″/m, s″ = 191/50 — there are
  no cores, so (H) is vacuous and Lemma B applies with r = 0. (This closes the same S4 gap for
  `lb_382`: the published bridge in the verifier header quantifies over disjoint families; a
  packing at m < 3.82 dilates to a strictly-disjoint family at 3.82. One line, previously
  unwritten.)

## B.2′ [T] The general (H) criterion — owner frame, not axis-parallel width

Corollary B′'s formula ρ = 1/2 − a(cos θ_c + sin θ_c) compares a core against an
**axis-aligned** pin square; it is the wrong test for a tilted core hypothesised inside a
same-orientation packing square, where it can go spuriously negative (A60 recorded exactly this
false alarm: ρ ≈ −0.204 on its tilted conditioning cores — a misapplication, not a failure;
`attempts/A60-trump5-campaign/notes/ledger.md` §1). The correct general condition: if the
hypothesis square Q_o (any orientation) contains core K_j with margin ρ_j in **Q_o's body
frame** (for a same-orientation pair, ρ_j = 1/2 − a_j), then (H) survives dilation whenever

  (λ − 1) · |c_o|₂ < ρ_j    (sufficient: body-frame offset ≤ Euclidean centre motion),

and |c_o|₂ ≤ √2·(s″ − 1/2) < 4.78 bounds it certificate-side when the owner's position is not
otherwise localised. For slot pins B′'s per-axis form with A = 5/2 is sharper; use it there.
In every A60 certificate the binding core is the ε-fat PIN core (ρ ≈ 1.0e-9), independently
reproduced by A60 over its 49 leaves; the tilted cores have ρ_tilt = 1/2 − a ∈ [6.4e-4, 0.14]
and never bind.

## B.2″ [T] Lemma B-NO (the `nofams`-aware clause)

Lemma B required empty `nofams`. Four A60 PASS certificates — exactly the CONFINEMENT leaves,
the only viable route for trump5's outer triple (G-A60-2) — carry a NO-family, so they need
their own clause. Recall the semantics: with nonempty nofams the certificate's bridged claim
at its own side s″ is not emptiness but **occupancy**: every disjoint-closed family containing
the cores has some square whose (centre, t) lies in some F_k (otherwise all ≥ b core-free
squares are priced and μ ≥ b > Σw).

**Lemma B-NO.** Same setting and hypotheses (H) as Lemma B, but with NO-families
F_1 … F_m (centre rectangles × t-interval lists). Then P (interior-disjoint, side m = s″/λ)
has a square Q, distinct from the r core-owning squares, with

  (c_Q, t_Q) ∈ λ⁻¹F_k for some k,  where λ⁻¹F_k := ([x0/λ, x1/λ] × [y0/λ, y1/λ]) × (same
  t-intervals — dilation does not change orientation).

*Proof.* Dilate as in Lemma B. If no square of G (the ≥ b non-owners) were NO-exempt, every
member of G would be priced (admissible, meets no core, non-exempt) and μ(total) ≥ b,
contradicting (P1). So some Δ_λQ ∈ G has (λc_Q, t_Q) ∈ F_k; divide the centre by λ. ∎
No side condition on the core owners is needed: the dichotomy only prices the non-owners, so
exempt-or-not status of the owners never enters.

**Composition bookkeeping (the part consumers must not skip).** λ⁻¹F_k is NOT a subset of
F_k — it is F_k contracted toward the origin, so it protrudes below F_k on the near-origin
sides by up to (1 − 1/λ)·x1 ≤ (λ − 1)·x1 per axis. A downstream node that hypothesises "the
confined square lies in F_k" must instead hypothesise the outward widening
F_k^{+ε}, ε = (λ_max − 1)·(max coordinate of F_k):
* within the current fat-pin transfer shell (λ − 1 ≤ 4.0e-10): ε ≤ 1.6e-9 — negligible against
  any real margin, but it must be STATED in the (D)/(K) child hypotheses;
* under the slack-core grid (B.4, λ − 1 ≤ ~4e-4): ε ≈ 1.6e-3 — a real widening that must be
  built into the grid re-emission of every zone consumer, alongside the slackened pin cores.
And the shell caveat is unchanged: with today's ε-fat pin cores the confinement leaves, like
every other A60 leaf, transfer only within the 4e-10 shell — Lemma B-NO removes the
*structural* exclusion of the confinement route from the bridge, not the margin problem.

## B.3 [F] The F6 interaction, made explicit

A56 refuted "kill at s0 × transfer principle" as a factorisation; Lemma B does not resurrect
it. What Lemma B adds is the ε-shell transfer (H′), and the corpus computation shows the shell
is ~4e-10 relative — so the window quantifier in `stratum_kill` is carried by the PARAMETRIC
coverage plus B′, never by s0 certificates alone. Precisely:

* a stratum with full-window parametric coverage → `stratum_kill` instance at every
  m ∈ [3.82, ŝ]: **discharged** (modulo the parametric verifier's own soundness, A56 P3);
* a stratum with partial coverage [3.82, b] ∪ {s0} (k6_07-type) → instances at every m < b
  with (m, m(1+4e-10)) ∩ [3.82, b] ≠ ∅, i.e. every m < b; the band [b, ŝ] stays OPEN;
* an s0-only stratum → **no instance in the window**; the certificate is evidence, not proof.

## B.4 [F] The repair knob for future certificates: slack cores

The ε-fat core (a ≈ 1/2 − 3.1e-8) was an LP economy — it maximises the exempt region. Nothing
in the kill semantics requires it. A certificate re-emitted with core half-side a = 1/2 − δ has
ρ ≈ δ, and B′ then transfers it to all m ∈ [s″/(1 + δ/A), s″]: with δ = 1e-3, a single fixed-s
certificate covers a slab of relative width 4e-4 (~1.55e-3 in s). **A grid of ~37 fixed-side
certificates with δ = 1e-3 cores covers the whole window [3.82, s0] for a stratum, replacing
the 4-D parametric s-axis entirely** — an alternative route for the A61 stragglers and the only
currently-visible route for giving the A57 sub-trees and the A60 zone-tree a window form
without re-architecting them parametrically (re-run the same trees at the grid sides with
slackened pin cores). Named: **the slack-core grid route**.

COST CAVEAT (A60 relay, 2026-09-01): do NOT price the ×37 off A56's 0.5-budget-slack rule.
A60's measured certification law on trump5 is stricter — a node certifies iff η = τ − budget
reaches −1; every fractional-η node (−0.33, −0.50) FAILed (`A60 notes/falsifier.md` §6), i.e.
the 0.5-slack regime is exactly what fails there. Affordability of δ = 1e-3 cores on trump5
is UNMEASURED; A60 is re-emitting one already-PASSing cover leaf at δ = 1e-3 as the decisive
one-LP test. Hold any grid budgeting until that lands. (For zone CONSUMERS in the grid, also
apply the B.2″ widening ε ≈ 1.6e-3.)

Boundary discipline note (S4 checklist item): with Lemma B in place, every kill application in
the composition is at a certified side s″ STRICTLY ABOVE the packing side m, and no lemma is
ever applied to a literal contact-closed packing at the certificate's own side. The remaining
S4 exposure is confined to `trump_residual` (the A60 tree's conclusion is a containment, not an
emptiness — Δ_λ transfers kills, not containment conclusions; the pulled-back basin box shrinks
by λ toward the origin and misses the basin by ~(λ−1)·|ĉ| ≫ rBasin for any λ reaching s0).
That is exactly depgraph node D.SLAB, unchanged by this file.

## B.5 Status

LEAN-PROVED (A68, 2026-09-01): `lean/PackingCertMathlib/PackingCertMathlib/Dilation.lean` —
B.0(a) `scaleC_disjoint`, B.0(b) = A64's `scaleC_subset`, B.0(c) `slot_tracking` (the identity
λ(α+βm) − (α+βλm) = (λ−1)α holds for EVERY β, not only β ∈ {0,1}), `dilation_bridge`
(interior-disjoint packing at m ⟹ strictly-disjoint closed family at λm, `IsStrictFamily`),
`lemma_B`, the pricing pigeonhole `priced_dichotomy` / `hcert_of_priced` ((P1)+(P2) ⟹ the
bridged claim; stated with an abstract `Exempt` predicate, so Lemma B-NO's occupancy dichotomy
is the SAME theorem — empty `nofams` = `Exempt := False`), `bprime_containment` (the (H′)
margin condition ⟹ hypothesis (H), core in the interior of the dilated pin square), and
`pullback_mem_Icc` (the B.2″ outward widening). All axiom-clean (propext/Choice/Quot.sound).
Two findings from the formalisation:
* the SAT citation in B.0(a) is unnecessary — A64's pull-back trick (`scaleC_mem_interior`:
  a common point of the dilates pulls back by 1/λ to a common interior point) proves strict
  disjointness with no separation theorem at all;
* hypothesis (H)'s "open interior" clause is not needed for Lemma B's conclusion — closed
  containment K_j ⊆ Δ_λQ_{i_j} suffices both for "meets no core" (closed-set disjointness)
  and for the pricing step; interior containment matters only if a certificate's own
  exemption semantics requires it (kept in the Lean statements since B′ delivers it free).
NOT Lean: producing (P2) from a concrete PASS file (case-LP verifier soundness, depgraph
V.CASE); the B.2′ owner-frame criterion for tilted cores (prose below stands); and the corpus
margin ρ ≈ 1.0000009e-9, which remains a [M] computation.

Lemma B, Corollary B′, B.2′ (owner-frame criterion), B.2″ (Lemma B-NO), and the corpus margin
computation: proved/computed here (A63; B.2′/B.2″ added after the A60 feedback round —
`attempts/A60-trump5-campaign/notes/ledger.md`). Cross-checks: A60 independently reproduced
ρ = 1.0000009e-9 as the binding margin on all 49 of its leaves; the θ↔t companion lemma
(`theta_t_transfer.md`) caught A60's basin-discharge test running in θ-radians against the
wrong radius (corrected to contain_t vs rBasin = 3/2000; square-1 ladder passes at 1.24×,
squares 2–3 to be re-checked as their ladders close). Uses:
separating-axis for convex polygons (as drain_lemma D3′ and A36 L1 do — cited, standard), the
case-LP PASS claim (P1)/(P2) as frozen in `docs/specs/case_lp_certificate_v1.md`, and the A56
P3 parametric soundness theorem for specialisation. Degenerate case "tight pin containment"
(ρ = 0): does not occur in the corpus (ρ > 0 exact, uniform); any future certificate must have
its ρ checked — add it to the C7 report checklist for new formats.
