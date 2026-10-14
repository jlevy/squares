# The pair-certificate soundness lemma (Lemma P) — A66, 2026-09-02

The certificate family `h10_stuck.md` §8 named as the cheapest formalism that can see what
single-square measures provably cannot: atoms price unordered PAIRS of placements, and the
stuckness revenue is the per-box 2-crowd of CC-2′. Format frozen in
`docs/specs/pair_certificate_v1.md`; this file carries the mathematics: the kill lemma at
drain-v3 rigor, the closed-vs-interior bridge clause for the pair rows, the exact form of the
stuckness hypothesis consumed, the β = 0 emptiness corollary, the death-witness criterion, and
the A34 non-applicability argument. Labels: [T] proved, [S] routine given cited items,
[M] measured exact.

Standing ingredients: Δ_λ dilation facts B.0(a)–(c) and Corollary B′'s margin bookkeeping
(`closed_disjoint_bridge.md`); the teleport-stuck selection chain (`unique_transfer.md` §2);
CC-2′ re-based on teleport-stuckness (A58 §2; re-base per `h10_stuck.md` standing-ingredients
paragraph); the unclipped-box census and its s-stability (A58 occupancy matrix; A53 L2(iv);
exact per-class lists `attempts/A65-low-k-closure/results/h10_boxspec.json`).

## 1 The certificate's claim (from the spec, restated)

A `pair-certificate-v1` PASS at side s″ for class S (k pins, N = 11 − k, m boxes) declares
axis slack cores K_1…K_k (half-side a = 1/2 − δ, δ > 0, centred at slots_S(s″)), widened
boxes B̃_1…B̃_m (closed axis squares, centre = the s″ slot-box centre, half-side 1/2 + ε_box),
β ≥ 0, and an atomic pair measure: atoms ((p_i, p′_i), w_i ≥ 0), W₂ = Σ w_i. It establishes:

> **(P1′)** W₂ < C(N,2) + β·m, and
> **(P2′)** every unordered pair {Q, Q′} of closed unit squares in [0, s″]², each meeting no
> core (closed intersection), with int Q ∩ int Q′ = ∅, satisfies
> μ₂{Q,Q′} := Σ{ w_i : one of p_i, p′_i lies in Q and the other in Q′ } ≥ 1 + β·m₂(Q,Q′),
> where m₂(Q,Q′) = #{ i : int Q ∩ int B̃_i ≠ ∅ and int Q′ ∩ int B̃_i ≠ ∅ }.

## 2 [T] Lemma P (pair kill, with the bridge built in)

**Lemma P.** Let C be a pair-certificate-v1 PASS at side s″ for class S as above, and let

  m̃ ∈ ( s″ / (1 + δ/A), s″ ),  A = 5/2  (the slack-core shell of B.4, OPEN at the bottom:
  at the endpoint the core containment margin degenerates to 0 and (H)-type interior
  containment fails), and
  ε_box ≥ 3·(s″/m̃ − 1)   (satisfied for the whole shell when ε_box ≥ 3·δ/(A − δ) ≥ 3(λ_max−1)).

Then no teleport-stuck packing at side m̃ has skeleton exactly S.

*Proof.* Suppose z* is such a packing: axis pins at slots_S(m̃), free squares q_1 … q_N (in
stratum S the non-pin squares are exactly the non-simple ones). Set λ = s″/m̃ > 1 and dilate.

1. *Bridge.* Δ_λ z* is a family of 11 closed unit squares in [0, s″]² (B.0(b)), pairwise
   disjoint **as closed sets** with SAT gap ≥ λ − 1 (B.0(a)).
2. *Cores are owned.* The dilated pin j is axis-aligned with centre within (λ−1)·A < δ = ρ
   per axis of the s″-slot (B.0(c)); the axis core of half-side 1/2 − δ centred at that slot
   therefore lies in the open interior of the dilated pin (Corollary B′'s computation with
   θ_c = 0). Hence each core is contained in its owner; every dilated free square Δq_a is
   disjoint from the dilated pins (step 1), so it meets no core: **core-free**.
3. *Incidences survive widening.* If x ∈ int q_a ∩ int B_i(m̃) then λx ∈ int Δq_a ∩
   int λB_i(m̃), and λB_i(m̃) ⊆ B̃_i: per coordinate the m̃-box centre is α + β_c·m̃ with
   |α| ≤ 5/2 (A56 P1 slot arithmetic), so |λ(α + β_c m̃) − (α + β_c s″)| = (λ−1)|α| ≤
   (λ−1)·5/2, while the half-width grows from 1/2 to λ/2 = 1/2 + (λ−1)/2; total excursion
   ≤ 1/2 + 3(λ−1) ≤ 1/2 + ε_box. ∎(step)
4. *Stuckness rows consumed.* z* teleport-stuck ⇒ by CC-2′ (re-based: derived from
   teleport-stuckness alone) every unclipped completable box B_i(m̃) of S — the census list is
   s-stable, so it is the s″ list read at m̃ — is met (open interiors) by ≥ 2 distinct free
   squares. **This is the entire stuckness input**: one unordered pair π_i per box, both
   members meeting int B_i(m̃); no CC-3/CC-4/corridor content is encoded. By step 3, both
   members of π_i meet int B̃_i after dilation, so Σ_{a<b} m₂(Δq_a, Δq_b) ≥
   Σ_i #{boxes whose chosen pair is {a,b}} summed = m.
5. *Rows apply.* Each unordered pair {Δq_a, Δq_b} (a < b) is admissible for (P2′): both in
   [0,s″]², core-free (step 2), interiors disjoint (step 1, strictly). Hence
   μ₂{Δq_a, Δq_b} ≥ 1 + β·m₂(Δq_a, Δq_b).
6. *Additivity.* Σ_{a<b} μ₂{Δq_a, Δq_b} ≤ W₂: an atom (p_i, p′_i) is collected by {a,b} only
   if p_i and p′_i lie in the two (distinct) squares; since the Δq are pairwise disjoint
   closed sets, p_i lies in at most one square and p′_i in at most one, so each atom is
   collected by at most one unordered pair.
7. *Chain.* W₂ ≥ Σ_{a<b} (1 + β·m₂) ≥ C(N,2) + β·m > W₂ by (P1′). Contradiction. ∎

Remarks. (i) λ > 1 is used exactly where Lemma B uses it: closed disjointness for atom
additivity (step 6) and owner disjointness (step 2); at m̃ = s″ the lemma is NOT asserted —
the shell is half-open, as everywhere in the composition. (ii) The row quantifier is
interior-disjoint pairs, a superset of the realised (strictly disjoint) pairs — conservative.
(iii) β = 0 needs no boxes and no stuckness; see §3. (iv) Window form: identical status to
every fixed-side kill — the slack-core grid (B.4) covers [3.82, s0] with ~37 sides at
δ = 1e-3, or a parametric re-emission; nothing pair-specific changes the bookkeeping, except
that consumers must carry ε_box ≥ 3(λ_max − 1) per grid slab.

## 3 [T] Corollary P0 (β = 0: EMPTINESS, no stuckness hypothesis)

If the certificate has β = 0 (boxes ignored) and W₂ < C(N,2), then no packing at side
m̃ ∈ (s″/(1+δ/A), s″) contains axis-aligned unit squares at all pins of S **at all** — not
merely no stuck one. *Proof.* Steps 1–2 and 5–7 with the N non-pin squares of an arbitrary
packing containing the pins; stuckness (step 4) is never used. ∎

This is the constructive residue route (a) of `corners4_empty.md` §6: the single-square
analogue is blocked by K1 aliveness (τ* ≥ N), but the pair analogue of aliveness is the
existence of a full N-family of pairwise-disjoint core-free squares — which for corners4 is
exactly what the A65 search could not find. A P0 PASS for corners4 would delete the class
outright on the certified shell(s).

## 4 [T/M] The decision criterion (both directions) and the canary theorem

**Death witness [T].** If N pairwise-disjoint (closed) core-free unit squares exist at s″
with Σ_{a<b} m₂ ≥ m, then every certificate satisfying (P2′) has W₂ ≥ C(N,2) + β·m — sum the
rows over the family's pairs (additivity as in step 6). The pair route is then dead for the
class at every β, decisively.

**Canary theorem [T+M].** Trump's packing supplies such a death witness for its own class:
on trump5 (N = 6, m = 6) his six non-simple squares realise every box with exactly 2 meeters
(A58 §5 canary, re-tallied in `h10_stuck.md` §2). His packing has contacts, so the witness is
its **dilated image**: for any certificate side s″ whose Lemma P shell contains ŝ — i.e.
exactly the certificates that would bind Trump — Δ_{s″/ŝ}(his six free squares) is pairwise
closed-disjoint, core-free (steps 1–2 of Lemma P), and keeps every box incidence (step 3), so
Σ_{a<b} m₂ ≥ 6 = m and every valid pair certificate at such an s″ has
W₂ ≥ C(6,2) + 6β = threshold: **no pair certificate whose shell reaches ŝ can kill trump5.** The design provably spares the canary — the pair threshold is saturated with
equality by the packing every argument must spare, exactly as H10-I is (load 2.00). The
formalism's power is confined to classes where the 2-crowds are NOT jointly realisable.

**Kill hope [M].** k4_08 (N = 7, m = 7): the best exactly-verified family realises
Σ_{a<b} m₂ = 6 < 7 (crowdfam box_coverage (2,2,2,2,2,2,1): six boxes with exactly one
realised pair, the TL(0,0) box deficient — `attempts/A65-low-k-closure/results/crowdfam.json`).
The integral obstruction is short by exactly one pair-incidence; the fractional pair-LP value
τ₂(β) against threshold C(7,2) + 7β = 21 + 7β is the pilot question
(`attempts/A66-corners4-pair/`). corners4 (N = 7, m = 8): no family exists at all; both the
β = 0 emptiness form (threshold 21) and the boosted form (21 + 8β) are structurally open to
certification.

## 5 [T] Why the A34 collapse theorem does NOT apply

The collapse theorem (A34 `notes/verdict.md` §1) caps any sparse moment/SOS relaxation whose
cliques carry ≤ m′ < n squares at s(m′): from an optimal m′-packing it builds locally
consistent clique measures — pair cliques collapse to s(2) = 2. Three reasons it has no grip
here, in decreasing order of importance:

1. **The pair certificate is a pricing dual, not a feasibility relaxation.** Its rows
   quantify over single realised pairs of a hypothetical 11-packing at the fixed side s″ with
   the class pins as cores; no consistency between rows is asserted, no marginal of any
   relaxation variable exists, and there is nothing to glue. The anti-correlated-triangle
   escape (marginal agreement without a global measure) needs a family of local measures
   asked to agree; the certificate asks no such question.
2. **Every row already carries global data.** A row's admissibility condition (containment in
   [0, s″]², core-freeness against all k pins) embeds the full container and skeleton — the
   "square support" of each constraint in A34's sense includes the pins, and the certified
   side is s″ ≈ 3.877, not s(2).
3. **The stuckness revenue couples to the global budget.** The kill compares W₂ against
   C(N,2) + β·m, a count over ALL pairs of the family at once; the additivity step consumes
   pairwise disjointness of the entire 11-square family (an n = 11 fact). No 2-square
   subconfiguration certifies or refutes Σ m₂ ≥ m — precisely the coupling whose absence
   collapses pair-clique relaxations. Conversely: what WOULD reintroduce the collapse is
   replacing the per-pair rows by pair-marginal consistency constraints on a relaxed packing
   measure; the spec's semantics (§1) forbids that reading.

In A34's vocabulary: pair STRUCTURE here means pairs are the priced test objects (the
analogue of single placements in `measure-certificate-v1`), not the support of relaxation
cliques. The certificate's strength lives in the row quantifier (checked by branch-and-bound,
co-NP side), not in any moment matrix.

## 6 [T] Lemma P-B: the basin-exclusion discount (PI's fat-mass row, drain-basin framing)

The ε-parking ghost's home — the Trump-image perturbation families that A65 found to be the
ONLY realisable death-witness material — is an open neighbourhood that the A36 basin deletes
QUANTITATIVELY for exact-form strata. Monetised at pair level it is a row DISCOUNT with a
threshold rebate, and the accounting favours the certificate 21 : 15.

**Setup.** Setting of Lemma P (class S, k pins, N = 11 − k free squares, certified side s″,
slack δ), plus: a rational γ ∈ [0, 1]; a declared set G_S of **compatible Trump images** —
D4 images g of ẑ whose five simple slots contain S's pin slots (any other image has a pin
coordinate ≥ the slot spacing 1 ≫ rBasin from its counterpart, so its basin box cannot meet
the stratum; the compatible set is a per-class pattern computation, e.g. crowdfam's
`trump-sym4` embedding for k4_08); and for each g ∈ G_S, N zone boxes Ẑ_{g,1} … Ẑ_{g,N} in
(c, t)-space at side s″ around the dilated poses of g·ẑ's N non-pin-matching squares (zone
radius r_z, with the mod-π/2 t-branch for near-upright squares as in `theorem_u.md` §3).

**Certificate claim.** (P2″) for every admissible interior-disjoint core-free pair:
μ₂{Q,Q′} ≥ 1 + β·m₂(Q,Q′) − γ·Σ_{g∈G_S} bz_g(Q,Q′), where bz_g = 1 iff Q and Q′ lie in two
distinct zones of g (two disjoint unit squares can never share a zone: zone diameter ≪ 1 ≤
centre distance). (P1″) W₂ < C(N,2) + β·m − γ·C(N−1,2)·|G_S|.

**Lemma P-B.** In addition to Lemma P's hypotheses, suppose

  m̃ ∈ [ŝ − ρ_B, ŝ]  with  r_z + √2·ρ_B + rounding slop ≤ 3/2000  and  ρ_B ≤ 3/2000
  (the pullback bookkeeping per Lemma B-NO/B.2″: a centre coordinate's zone, centred at the
  s″/ŝ-dilated pose but pulled back by λ = s″/m̃, drifts by |ĉ|·(ŝ − m̃)/ŝ ≤ √2·(ŝ − m̃) —
  the DOMINANT slop, an order above the slack-core shell width; t-coordinates do not scale
  under dilation, so tilt zones pull back undrifted. E.g. r_z = 5·10⁻⁴, ρ_B = 5·10⁻⁴ leaves
  ≥ 2.9·10⁻⁴ slack),

and that the stratum hypothesis is EXACT (skeleton exactly S). Then the conclusion of
Lemma P holds with the discounted claim (P1″)/(P2″).

*Proof.* As Lemma P, with one further count. Fix g ∈ G_S and suppose ALL N free squares of
the stuck packing z lie (after Δ_λ dilation) in distinct zones of g. Pull back: every free
square's (c, t) is within r_z + √2·(ŝ − m̃) + slop ≤ 3/2000 of the corresponding non-pin
square of g·ẑ. The pins: z's pins sit exactly at slots(m̃), g·ẑ's matching simple squares exactly at
slots(ŝ), so each pin coordinate deviates by β_c·(ŝ − m̃) ≤ 3/2000 (slot arithmetic; tilt
coordinates 0 = 0 exactly). Hence ALL 33 coordinates of z lie within 3/2000 of g·ẑ: z is in
the A36 basin box of g·ẑ (D4 × S₁₁-covariant). The basin theorem gives σ(z) ≥ ŝ; but
σ(z) ≤ m̃ ≤ ŝ, so σ(z) = ŝ = m̃ and the equality clause forces z = g·ẑ. Now g·ẑ has FIVE
simple squares (a trump5 image), so its skeleton is not exactly S (|S| = k ≤ 4) —
contradicting the exact-stratum hypothesis. Hence for every g at most N − 1 free squares are
in-zone, so Σ_{pairs} bz_g ≤ C(N−1,2), and the additivity chain reads
W₂ ≥ Σ_{a<b}(1 + βm₂ − γΣ_g bz_g) ≥ C(N,2) + βm − γ·C(N−1,2)·|G_S|, contradicting (P1″). ∎

**Where the monotone→exact bridge enters (stated per the PI's bookkeeping demand).** The
skeleton-contradiction step is the ONLY place, and it is load-bearing: a MONOTONE hypothesis
("z contains the pins of S") would NOT contradict z = g·ẑ — the compatible image g·ẑ
*contains* S's pins by definition of compatibility. The basin row is therefore UNSOUND for
monotone pin quantifiers and sound exactly for the InStratum-exact semantics
(`instratum_bridge.md`, H2/F11 definitional layer) that H10-stuck already uses (CC-2′'s "in
stratum S the non-pin squares are exactly the non-simple ones"). The other imported
equality is `basin`'s equality clause (= A36's certified theorem after the X.1/X.3
transfers), consumed exactly as in `theorem_u.md` §4 — none of A60's open D-node content.

**Shell caveat (why this is a near-ŝ weapon).** For m̃ below the ρ_B-shell the pins' own
slot drift (and the √2-weighted zone drift) exceeds the basin radius: z can sit outside the basin box on its PIN coordinates while all N
free squares are in-zone, the count Σbz ≤ C(N−1,2) loses its justification, and the row must
be DROPPED (γ = 0, plain Lemma P). The composition consumes basin-discounted certificates
only on [ŝ − 3/2000, ŝ] — which is exactly where the ghost lives (the attained side) and
where H10-stuck's consumers (the selection chain at the attained minimum, the uniqueness
chain at ŝ) need it. Deep-window kills stay plain.

**The naive accounting, and what the pilot measured [M].** Against a PURE ghost family (all
N free squares in one image's zones — e.g. the crowdfam k4_08 family, a trump-sym4
perturbation at ~10⁻⁷ ≪ r_z) the floor drops by γ·C(N,2) = 21γ while the threshold rebate
is only γ·C(N−1,2) = 15γ: a naive net gain of 6γ. Measured (A66 γ-pilot, k4_08, contained
adequate catalog with zone-perturbation columns at 3·10⁻⁴ (in-zone) and 3·10⁻³ (out),
all cells converged at Lmax = 1.000000, β = 1,
`attempts/A66-corners4-pair/results/pairlp_k4_08_basin_v2.json`):

  γ = 0: value 27.000 vs threshold 28.000 (margin −1.000, ghost-mass fraction 1.00);
  γ = 0.1: 25.100 vs 26.500 (margin −1.400, ghost fraction 0.70);
  γ = 0.3: 24.031 vs 23.500 (margin +0.531: REFUTED, ghost fraction 0.10).

**The mechanism is real but smaller and non-monotone: the discount gains ≈ 4γ near γ = 0
(0.4 at γ = 0.1), then the fractional dual dodges — it re-weights toward out-of-zone
variants displaced 3·10⁻³ that keep almost the full value (A58's meeter margins ~1.6·10⁻²
≫ the 1.5·10⁻³ basin), the value is convex in γ, and beyond γ ≈ 0.245 the unconditional
rebate wins and the certificate is refuted.** Usable window 0 < γ ≲ 0.245, optimum near
γ ≈ 0.1: the basin row widens k4_08's certifiable margin from β to ≈ β + 0.4 at β = 1 — a
reserve, not a lever; PI's dτ/dε ~ 10² is not observed (the ghost's value is robust to the
whole basin radius). Sound at every γ (Lemma P-B), profitable only in that window. What the
basin can still do beyond pricing is disjunctive conditioning (branch on which square
deviates — A60-style), which is not a row. Credit: PI idea (drain-basin/grain framing);
formulation, accounting and the measurement this file + the A66 pilot. (A first γ-run
reported a "+14γ law / dead at every β" — retracted: its perturbation columns had escaped
the containment filter; the exact audit is `results/containment_audit.json`.)

**Measured pair-tier verdicts (A66 pilot; adequacy criterion: the catalog's single-square
fractional packing reproduces the A65 value — k4_08 τ_f = 7.000000 exact; corners4 7.084 vs
7.2545 after 13 column-generation rounds, residual attributed to the δ = 0 core-free
filter; every catalog audited for exact containment).** k4_08: restricted τ₂(β) = 21 + 6β
EXACTLY at β ∈ {0, 1/4, 1} (integral optimum = the crowdfam ghost family; best exact
contained 7-family in any support has Σm₂ = 6, I = 13 — §4's kill-hope paragraph stands),
i.e. margin −β below the threshold 21 + 7β with ZERO fractional excess on the restricted
instance; product witness certifies τ₂(0) ≥ 21 (emptiness dead, as for every class with a
full N-family). **k4_08's boosted pair kill is LIVE at restricted strength** — the first
protected-class pricing object in the lab whose restricted value sits strictly below its
kill threshold — and the residue is the full-quantifier question (emission + exact
verification, or a richer dual). corners4: β = 0 value brackets τ₂(0) ∈ [14.89, 21.32]
(certified product witness; unconverged cutting-plane upper end, trend 22.20 → 21.53 → 21.32
toward 21), straddling 21 — OPEN; the solver (simplex time on a 17k × 10k LP), not the
formulation, is the binder. **Composed-family answer:** (i) corners4: β = 0 emptiness
(Corollary P0), no basin row (G_S = ∅: every trump5 image has a clear corner); (ii) k4_08
and, by the same ghost mechanism, k4_11 (floors one pair-incidence short): pair rows +
stuckness boost β (margin β) + basin discount γ ≈ 0.1 near ŝ (≈ +0.4); (iii) subcritical
classes (floors 2–3 short per crowdfam): plain pair + β with 2β–3β windows, untested.

## 6.5 [T+M] Lemma W (the margin wall) and the A71 emission verdict (2026-09-02)

A71 ran the emission oracle loop (BRIEF T1) against the frozen verifier. Verdict: **no
full-quantifier certificate emitted; the obstruction is a quantified verification wall**,
recorded here because it binds every future emission attempt in v1 semantics.

**Lemma W (margin wall).** Let η > 0 and let Q_1 … Q_K be unit squares in [0, s″]², each
core-free against class S's slack cores, whose η-cores (concentric squares of side 1 − 2η,
same orientation) are pairwise disjoint. Let D = the set of interior-disjoint pairs among
them and V = |D| + β·Σ_{D} m₂. For any atomic pair measure μ write μ₂^η for collection
counting only atoms whose endpoints are ≥ η deep in their squares. Then
Σ_{(i,j)∈D} μ₂^η{Q_i, Q_j} ≤ W₂ (an η-deep endpoint lies in the pairwise-disjoint η-cores,
so each atom serves at most one pair at margin η). Hence if V ≥ C(N,2) + βm, every
P1′-valid certificate carries ≥ V − W₂ units of its coverage of these rows on atoms less
than η deep — and any `verify_pair.py` run must refine the corresponding pair boxes to the
~η scale before COVERED can fire (certain membership over a box is depth against every
placement in it). *Proof: the two sentences above.* ∎

**Measured instantiation (k4_08, β = 1, s″ = s0, δ = 1/1000, ε_box = 1/833) [M exact].**
K = 11 mixed-tilt squares with pairwise-disjoint 0.15-cores, exact rationals, D = 35,
Σm₂ = 4: V = 39 ≥ 28 (`attempts/A71-pair-emission/results/wall_witness2_k4_08.json`,
pure-Fraction verification of every constraint). So every valid certificate rides ≥ 11
units of family coverage on sub-0.15-margin atoms. Fractional probes (η-shrunk membership
LPs) show the adversary value already ≥ 28-trending at η ≈ 0.03–0.10 but did not converge
in budget (`results/etaprobe_*.json`, honest per-η state). Companion negative: k4_08's
pins block the CHEAPEST wall families — an axis-aligned 4-row of shrunk cores needs the
empty y-band [2.499, 2.378] at s0 (`code/wallwit.py`) — the naive (4 − s″)/6 ≈ 0.02 wall
does not apply; the pins protect at the exploit level too.

**Fixed point and demonstration [M/F].** The A71 loop's empirical fixed point: with
adversarial continuum row-hunting + mock-witness feedback the covering LP climbs from the
restricted 27 to W₂ ≈ 30.0 ≥ 28 (P1′ violated) — the wall priced on the covering side; the
rescaled P1′-valid candidate was judged by the FROZEN verifier end to end: FAIL at depth 12
with concrete deficit witnesses (`attempts/A71-pair-emission/certs/pair_k4_08_s0_b1_v1s.report.json`).
corners4 carries the same wall in β = 0 form: exact witness K = 9, D = 22 ≥ 21 at η = 0.15
(`results/wall_witness2_k4_13.json`) — though with the smallest shortfall (1 unit), making
corners4 the natural v2 pilot. **A71 T3 broke the solver wall [M]**: inclusion-maximal
point reduction (265k raw → 1375 maximal patterns) + IPM-no-crossover + row purging turn
A66's stalled 17k×10k simplex into ~8-min converged cut loops; the support-catalog β = 0
value CONVERGED at 20.528144 (viol 0/0, Lmax = 1.000000037) with an exact certified lower
bound 4103377/200000 = 20.516885 (exact Lmax 62499/62500 on cell-representative points,
support exact-audited; completeness caveat recorded in
`attempts/A71-pair-emission/results/k4_13_cert_lower.json`). Dual pricing exposed the
A66 support catalog as NOT pair-adequate (40% of the 1.74M enriched pair columns
under-priced), so the run GROWS the catalog by pricing: grow-0 = 20.528144 converged,
grow-1 (304 placements / 20.4k pairs) = 20.542 at budget (Lmax 1.12), further grows in
flight at session close — every measurement ≥ 0.45 BELOW the line 21 and the value moves
by ~1e-2 per grow: A66's bracket [14.89, 21.32] is effectively [20.52, ~20.6], and the
Corollary P0 emptiness route for corners4 is OPEN at restricted strength (not refuted;
final adequacy-clean value = the A71 T3 artifact set, `results/pairlp_k4_13_a71cg.json`).

**Cost identity [M].** Frozen-verifier throughput at realistic atom counts (3000 atoms,
exact Fractions): 57 pair-boxes/s (17.5 ms/node; A71 `results/calib_verify.json`); the
A71 float mock replays the identical discharge rules at 72k nodes/s (1250×). Leaf-count
geometry ~0.8·((2.877/2r_c)²/(2r_t))²/2 at cell radii (r_c, r_t) ≈ (m/4, m/8) for margin m:
all-margins-0.15 (ruled out by Lemma W) ≈ 6e8 leaves ≈ 125 days single-core; 0.10 ≈ 7e9 ≈ 4 y;
0.05 ≈ 4.5e11 ≈ 250 y — v1 verification is decades-to-centuries at the actually-forced margins. The wall is the verifier's uniform
certain-membership COVERED discharge (spec §5's warning, now priced), NOT the certificate's
existence: restricted τ₂ = 27 < 28 with zero fractional excess on every audited catalog.

**Consequences.** (i) v1 emission for the k4-tier is CLOSED as infeasible-at-scale; the
constructive residue is a v2 design: margin-aware splitting, placement-dependent membership
accounting, a compiled second implementation (wanted for the TCB anyway), and/or an
analytic coverage clause — spec revision to be VERSIONED (pair-certificate-v2), never an
edit of v1. (ii) The measure-existence question (a proof that a W₂ < 28 measure exists,
not an atom list) is the open mathematical half [C]. (iii) Canary: Lemma W is
adversary-side (a lower bound on W₂) — it strengthens nothing against trump5; the A71
run-level canary re-verified the dilated 60-digit Trump family as an exact death witness
under the A71 parameters (min SAT gap = λ − 1 = 1.06e-7 exactly, Σm₂ = 6;
`results/canary_trump.json`).

## 6.6 [T+M] pair-certificate v2, Lemma W′, and the corners4 depth-profile wall (A73, 2026-09-02)

**v2 exists** (`docs/specs/pair_certificate_v2.md`, claim IDENTICAL to v1 — every
consumption path and the canary theorem carry over verbatim): free rational-cut
margin-aware splitting (Lemma S), EXACT quadratic-sign-test membership/exemption
predicates (Lemmas M/E/Q — iff, no interval slop), the analytic handoff clause
COVERED-F (Lemma F, failing-set form), VACUOUS-CONTAIN (the container-boundary sliver
the v1 clip provably cannot discharge), and DEFICIENT-EARLY (exact rational
counterexample rows). Two implementations from the spec: the A73 reference
(`attempts/A73-pair-v2/code/verify_pair2.py`; selftest 0 violations, toys + corruption
gates) and a clean-room compiled Rust build (`code/verify_pair2_rs/`, selftest-clean,
20k–440k nodes/s single-thread by regime, ≥100k with jobs) — checklist C3 for the pair
family. **The v1 THROUGHPUT wall is broken** [M]: the first full-quantifier
atom-bearing (P2′) PASSes exist — synthetic grid-pair certificates at s = 3 verified
end-to-end (5866 nodes at atom margin 0.146; 1098 nodes at margin 0.076; the SMALLER
margin cost FEWER nodes) — and the measured v2 cost law tracks the measure's FRONTIER
STRUCTURE (where coverage hands off between witnesses), not (1/margin)^6.

**Lemma W′ (fractional margin law; Lemma W's quantified successor).** Let z* be any
η-feasible adversary (load of η-deep collection ≤ 1 at every atom position), of value
V = Σ z*(1 + βm₂). Then every P1′-valid certificate satisfies
Σ_i w_i·S_i^η(z*) ≥ V − W₂ > V − (C(N,2) + βm), where S_i^η = the z*-mass of rows
collecting atom i sharply but not η-deep. *Proof:* V ≤ Σ z*μ₂ = Σ_i w_i L_i,
L_i ≤ 1 + S_i^η by η-feasibility at atom i's own position. ∎ The τ₂^η curve therefore
prices the DEPTH PROFILE of every valid certificate.

**Measured corners4 τ₂^η curve (catalog-restricted, A73 `pairlp413e.py` = A71 rig +
η-deep membership + η-shrunk arrangement; brackets = [feasible-scaled, relaxation]):**
sharp η→0: 20.528 CONVERGED (A71); η = 0.01: [18.01, 21.38] unconverged, still
descending ~0.008/round at the IPM wall (plausible asymptote 21.1–21.3, i.e. ABOVE the
line); η = 0.02: [17.77, 22.30]; η = 0.05: [18.31, 26.24]; η = 0.1: scaled ≥ ~34
(relaxation plateau 57.000) — DEAD decisively, and by Lemma W′ ≥ ~13 weighted units of
sub-0.1-margin service are FORCED in every valid corners4 certificate. **The fractional
wall crosses 21 at η* somewhere in (~0.006, ~0.05) — far below Lemma W's integral
0.12–0.15.** Uniform-η emission is dead on that whole range while sharp 20.528 stays
open: any valid corners4 certificate is a MIXED-DEPTH measure (deep coverage of generic
rows + the forced shallow units at the exploit families' own scale), and its
verification cost concentrates near the exploit manifolds — exactly what margin-aware
splitting + hint trees localize.

**The tangency trap [M].** LP-optimal covering primals put atoms ON the membership
boundaries of the squares they serve (arrangement-cell representatives; margins ~1e-6):
the A71 seed is emission-side anti-verifiable — v2's first corners4 survey measured
COVERED firing ZERO times on it. Emitters must solve at η-deep semantics or deepen
post-hoc; η-deep coverage implies true coverage (conservative).

**Status of the corners4 pilot (honest).** No corners4 certificate emitted: the residue
is no longer verifier throughput but the EMISSION problem — produce a mixed-depth,
weight-CONSOLIDATED measure (W₂ < 21 with the Lemma W′-forced shallow structure), for
which the uniform-η LP is only a sufficient-side probe (and its η-runs hit genuine IPM
scaling walls: η-shrunk arrangements yield ~2× denser rows, nnz 4–6M, rounds 30–900 s,
all runs at η ∈ {0.01, 0.02, 0.05} stopped unconverged straddling 21). Constructive
successor, priced: a deepening/consolidation pass on the sharp primal (move each atom to
maximize min serving depth subject to tight rows, consolidate onto a coarse net), the
survey loop (DEFICIENT-EARLY rows) against the compiled verifier, and hint-tree
emission. Canary [M]: the dilated Trump family re-verified SAFE under A73 parameters
(min pair SAT gap = λ − 1 = 1.06e-7 exactly, Σm₂ = 6); all η-probes are
adversary-side. P0 consumption path unchanged and restated in
`attempts/A73-pair-v2/notes/findings.md`.

## 6.7 [M+T] Mixed-depth emission: the first sub-threshold corners4 measures, hint trees, and Lemma W″ (A74, 2026-09-02)

**Machinery** (`attempts/A74-mixed-depth/code/`, emission-side only; the frozen v2
verifiers are untouched and every claim below about the continuum is theirs). The (P2′)
point-pattern rows are offered to the A71/A73 adversary LP at SEVERAL depth levels
η₁ > … > η_L at once (each level's own arrangement of the η-shrunk squares; row (c,d,l)
counts z_ij only when both endpoints are η_l-deep), priced into the adversary as
load ≤ rhs_l = 1 + μ·(η_max − η_l)/(η_max − η_min). By LP duality the row duals y then
minimise the depth-priced covering cost Σ y_r·rhs_r subject to Aᵀy ≥ 1 over EVERY catalog
pair (all pairs are columns, so any HiGHS-optimal dual is a restricted covering measure —
provided no column sits at its bound, which is checked), and the certificate gate is the
UNPRICED mass W₂ = Σ y ≤ priced value. Consolidation drops rows below a rising dual-weight
floor and re-solves, accepted while W₂ < guard. Dual seeding (the binding point pairs of
earlier runs re-membershipped at every level) replaces ~15 cut rounds; the loop solves are
IPM + crossover (exact duals each round; IPM-only iterates time out without a feasible
point above ~10 M nnz, and simplex cold-starts do not finish). Canary per emission SAFE
(`notes/ledger.md`: min gap = λ − 1 = 1.06e-7, Σm₂ = 6).

**[M] Sub-threshold measures exist (restricted).** On the 404-placement A71 colgen catalog
(+ control columns):

| run | menu η | μ | exact W₂ | atoms | mass at 0.05 / 0.02 / 0.008 / 0.002 / 0.0005 |
|---|---|---|---|---|---|
| md5 | 0.05, 0.02, 0.008, 0.002 | 0.01 | **20.98857** | 461 | 0.87 / 7.29 / 7.55 / 5.28 / — |
| md7 | + 0.0005 | 0.01 | **20.95955** | 353 | 0.59 / 6.98 / 7.41 / 5.10 / 0.87 |
| md8 | md7 menu, catalog grown by 65 exact-counterexample placements (469) | 0.01 | **20.95828** | 363 | 0.61 / 6.81 / 7.47 / 5.23 / 0.84 |

Every atom is ≥ its level's η deep in every square its row serves (the A73 tangency trap
is closed by construction; positions rounded to 1e-6 ≪ η). Certificates:
`attempts/A74-mixed-depth/certs/pair_k4_13_s0_b0_md{5,7,8}.json` (+ `_hinted`).

**Lemma W″ (the measured mixed-depth law, restricted form).** Let V(η_min, μ) be the
converged value of the depth-priced adversary LP on a catalog S with menu floor η_min.
By weak duality every covering of S's pairs whose atoms are all ≥ η_min-deep in the
squares they serve has W₂ ≥ V(η_min, μ)/(1 + μ); and the measured values pin the
restricted optimum to the threshold from below: slack 21 − W₂ = 0.011 at floor 0.002,
0.040 at floor 0.0005, against 0.47 at the sharp limit (A71: 20.528 converged). The
forced profile is not "bulk deep + thin shallow stratum": ~70 % of the mass sits at
0.008–0.02, ~25 % at 0.002, 3–4 % at 0.05 — the bulk lives just below the A73 bracket
η* ∈ (0.006, 0.05), as Lemma W′ predicts. Depth and consolidation compete for the same
slack: at μ = 0.3 the dual mass rises ABOVE 21 while rows are added (21.31 → 21.55, run
killed), and consolidation is accepted down to 470 rows (20.9886) and rejected at the
next floor (398 rows, 21.0026) for md5; 355 → 271 rows: 20.9595 → 21.0517 for md7.
Catalog growth by exact counterexample rows costs essentially nothing (md7 → md8:
−0.001 with 65 new placements), so the restricted optimum is not what blocks a
certificate; the verification residue is.

**[M] Verification residue and hint trees.** md5 unhinted (Rust verify_pair2 `--jobs 8`,
depth 34, 2 M nodes, survey): FAIL by cap only — 0 definitive rows, 300 cap witnesses at
depth 34 with certain mass median 0.845 (min 0.68), the verifier's own splitter having
driven factor A to widths 2e-4–7e-4 while factor B's tilt interval stayed UNSPLIT in all
300: the residue is tilt uncertainty in the un-split factor, not the atom margins.
`code/hinttree.py` (spec §4 hint trees: emitter-side float B&B, cut = max-min lookahead
over the six midpoint cuts, COVERED leaves where float-certain mass ≥ 1, empty nodes for
verifier fallback; verifier untouched, every leaf re-proved) changes the search shape:
30 nodes/root → cap witnesses at 99.8 % certain mass; 3000 nodes/root (237 k hint nodes,
5.9 k leaves) → COVERED 106.8 k vs 98.6 k, and DEFICIENT-EARLY fires 7317× — exact
rational counterexample pairs (collecting 0.948–0.992) exist in the continuum between
catalog placements, which the unhinted search never probed. Those rows are the survey
loop's row source; the first grown-catalog re-solve (md8, W₂ = 20.95828) cut the exact-hole count 220 → 57 at the same 1 M-node hinted budget (shallowest hole 0.948 → 0.964 collected): the loop converges ~4× per iteration. No corners4 PASS yet: the
honest state is a working mixed-depth emission loop with exact holes being harvested,
not a certificate.

**P0 consumption and window pricing (unchanged in form, now priced per side).** A v2 PASS
of any of these certificates at s₀ with δ = 1/1000 slack cores consumes verbatim as in
§6.6 / A73 (`Corollary P0`; ε_box = 1/833 = 3δ/(5/2 − δ) exactly): emptiness of every
packing containing the corner pins on (s₀/(1 + δ/(5/2)), s₀), i.e. the corners4 leaf of
C.K4TIER on that shell; full-window coverage is the slack-core slab grid (~38 sides at
δ = 1e-3 over [3.82, s₀]). Measured per-side loop cost at this scale: LP 25–40 min
(IPM+crossover rounds, dual-seeded), hint build ~10 min, hinted 1–2 M-node survey
15–25 min — ≈ 1 h per loop iteration, iterations-to-convergence and the certification
run itself unpriced (not reached).

## 6.8 [T+M] Lemma P-B(R): per-coordinate zones, the exact-checked A40 radius, and the saturation law (A76, 2026-09-02)

The basin row of §6 consumed ONE uniform radius (rBasin = 3/2000 in t-world) for all 33
coordinates. The bottom-up attempt A76 (`docs/proofs/grain_discharge.md`) shows no larger
basin can be certified grain-by-grain beyond the A36/A40 wall (their §5: every grain discharge
is a box-nonsingularity certificate capped by κ_eff; the hinge grains — a strip flush pair
degraded to a single-corner contact — carry ratio 48 at (10⁻², 2·10⁻³)), but it delivers two
things the row can consume today: a per-coordinate reading of the basin theorems and an
exact-rational re-check of A40.

**Lemma P-B(R) (per-coordinate form).** Let a basin theorem hold on the θ-world ∞-box of
radius h around (ẑ, ŝ): σ ≥ ŝ for every packing z with |c − ĉ|∞ ≤ h, |θ − θ̂|∞ ≤ h, |s − ŝ| ≤ h,
equality iff z = ẑ (A36: h = 37/10000, exact-checked by A70; A40: h = 5794/884563 ≈ 6.55·10⁻³,
exact-checked in A76: `attempts/A76-grain-discharge/code/a40_check_exact.py`, 2930
certificates, 168 774 checks, 0 failures, 5 gates FAIL as required, 70.5 s at PREC 330 —
`results/a40_exact_report.json`). Replace in Lemma P-B the single condition "r_z + √2·ρ_B +
slop ≤ 3/2000" by the three conditions

  centre zones   r_c + √2·ρ_B + rounding slop ≤ h,
  tilt zones     r_t ≤ h/2                            (t-radius; X.1: |Δθ| ≤ 2|Δt|),
  side shell     ρ_B ≤ h.

Then the conclusion of Lemma P-B holds verbatim (the pull-back of the N in-zone free squares
and the pins' slot drift place all 33 coordinates and the side inside the basin box; the basin
theorem's equality clause forces z = g·ẑ; the exact-stratum hypothesis contradicts). The
(1+√2) s-slab gate of `theta_t_transfer.md` X.3 is NOT needed here: the side is separately in
the shell. *Proof: as Lemma P-B, with the three coordinate families bounded separately.* ∎
Numbers: A36 gives (r_c, r_t) = (3.7·10⁻³ − √2ρ_B, 1.85·10⁻³); A40 gives (6.55·10⁻³ − √2ρ_B,
3.27·10⁻³) — e.g. ρ_B = 10⁻³: (5.1·10⁻³, 3.27·10⁻³) versus the uniform 1.5·10⁻³ in use (3.4× in
centres, 2.2× in tilts). Lean side: rBasin may be raised to 27/10000 (both X.3 gates pass with
A40's h: 2·rBasin ≤ h and rBasin(1+√2) < h) once the A40 store is accepted at the same trust
tier as A36's (it now is, at Python tier).

**Measured saturation law [M float LP, A66 rig unmodified, k4_08, β = 1, γ = 0.1, converged
cells, `attempts/A76-grain-discharge/results/pairlp_k4_08_basin_rz*.json`]:** the restricted
pair value against threshold 21 + 7β − 15γ = 26.5, with zones of radius r_z and perturbation
columns at 0.3 r_z (in-zone) and 3 r_z (out):

  r_z = 10⁻³: 25.10 (margin −1.40, in-zone ghost fraction 0.70)   [A66's pilot value]
  r_z = 3.7·10⁻³: 25.00 (−1.50, 0.87)
  r_z = 6.5·10⁻³: 24.99 (−1.51, 0.86)
  r_z = 10⁻²: 24.99 (−1.51, 0.87)
  r_z = 2·10⁻²: unconverged in the 300 s cell budget (Lmax 1.6; unscaled 24.92) — not a verdict.
  (γ = 0.2 cells unconverged at every r_z, Lmax 1.2–1.5, as in A66 beyond γ ≈ 0.245.)

The discount's gain grows by only ≈ 0.1 per DECADE of zone radius across the whole range any
local certificate can reach (A22's 5·10⁻⁴ to the A40 wall at 6.5·10⁻³ and beyond): the
fractional ghost's value is carried by mass the LP can park just outside any zone at a cost
independent of the zone's size until the meeter margins (~1.6·10⁻²) are reached — exactly
A66's "reserve, not a lever", now quantified in R. Consequence for the two-front design: the
fronts do NOT meet in the middle; the basin row's usable window is γ ≲ 0.245 with ≈ +0.4–0.5
of margin at every reachable R, and the k4 tier's kill remains the emission problem of §6.6.

## 6.9 [M+T] Lemma W‴: the complete-tree growth law, the root-order finding, and the corners4 loop verdict (A77, 2026-09-02)

**Machinery** (`attempts/A77-corners4-close/code/`, emission-side only; frozen verifiers untouched).
`hintbatch.py` builds a COMPLETE spec-§4 hint tree per root pair: level-synchronous float B&B
(every box of a level evaluated in one numpy pass over boxes × atoms, atoms pruned per chunk by
float possibility), cut = the A74 max-min lookahead over the six midpoint cuts (exact
certain-mass score; a slack-graded "soft" score and the plain widest rule were also measured),
cuts emitted as short dyadics strictly inside the float-mirrored CLIPPED interval, leaves emitted
as `null` (the verifier's own clause table discharges them in one step; a COVERED leaf hint buys
nothing since `verify_hint_leaf` re-runs `eval_node`). Leaf census {COV, EX, ND, VAC, HOLE,
OPEN}; HOLE = float-possible mass < 1 AND a float-admissible interior-disjoint placement pair on
the 3×3×3 fractional grid of the box collecting < 1. The float predicates were fuzzed against
the reference's exact `exc_certain` / `nondisjoint_certain` / `contain_vacuous` (4000 random
boxes, 0 disagreements), and an exact walk of the emitted trees with the reference's own
`split_box` / `clip_factor` / `discharge` reproduces the builder's census node for node
(roots 1,1 and 1,2: 47 092 nodes, 0 cut misses, 0 undischarged leaves). All 41 md8 hole pairs
re-check exactly (admissible, core-free, interior-disjoint, collected < 1).

**[M] The A74 "converging holes" was a budget artifact.** The Rust `--nodes` is a hard stop of
the whole search; the stored cap witnesses are a `faildump` sample. Recomputed from the A74
report counts (leaves = examined − split, undischarged = leaves − discharged): md5 unhinted 2 M
nodes → 393 k undischarged depth-34 leaves, md8 hinted 1 M nodes → 283 k. The 3000-node/root
DFS-truncated hint trees ran past `--depth 34` (hinted cut nodes bypass the depth check), so
every fallback node was already at the cap. "Holes 220 → 57" measured which slice of the tree
the traversal reached before the stop, not the certificate's residue.

**[M] Lemma W‴ (complete-tree growth law).** Let r(d) = splits(d) / (2·splits(d−1)) be the
per-level retention (fraction of children still undecided). On the md8 certificate
(363 atoms, W₂ = 20.95828):

* root 2,11, 1.59 M nodes to depth 25 (rule certain): r(d) = 0.75–0.78 FLAT from d = 14 to 25
  (0.782, 0.781, 0.775, 0.763, 0.756, 0.757, 0.747, 0.757, 0.762, 0.751, 0.771, 0.783);
  at d = 26: 475 k open boxes (certain-mass median 0.915, q90 0.979), 3280 holes (d ≥ 20,
  collecting 0.58–0.83). Rule soft: r = 0.80–0.83 (d = 8–21); rule widest: 0.73–0.89. The law
  is rule-insensitive. Root 4,6 (rule soft): r = 0.86–0.90, opens median 0.38.
* all 78 non-exempt roots (58 of 136 root pairs are EXEMPT at the root), cap 60 k/root:
  2.71 M nodes, 14 roots complete (adjacent-cell roots closed by EXEMPT/NONDISJOINT/VACUOUS at
  depths 8–50, 92 k nodes), 64 roots at the cap (depth 16–33); aggregate r(d) = 0.85–0.86 over
  d = 7–14; open-box certain mass median 0.60 (q10 0.17, q90 0.95); 41 holes at median depth 17.

Reading: the frontier grows ×1.5–1.75 per level and the retention does not fall over the
measured range (box widths 0.72 → ~0.05 per coordinate at d ≈ 25). Coverage needs widths at the
atom-depth scale of the Lemma W″ profile (70 % of the mass at 0.008–0.02, 25 % at 0.002):
4–6 more halvings per coordinate, i.e. depth ~40–50, so the complete tree is
~1.6^20–1.6^25 × (frontier at d = 25) ≈ 10⁹–10¹¹ nodes over the 78 roots. Binding resource
= tree size (the η-fine boundary structure of a tight measure — every valid corners4 measure
is tight: total slack ≤ 0.04 by Lemma W″, so no coverage redundancy can fatten the cells), not
holes and not the LP. Certification cost at the asymptote: at the measured HINTED Rust
throughput of 46 k nodes/s, 10⁹–10¹¹ nodes is 6 h–25 days of verifier time, but the hint file
is 27 bytes/node (73 MB per 2.7 M nodes) and the frozen verifier holds it as a `serde_json`
Value: ≥ 27 GB for 10⁹ nodes — beyond the frozen implementation. Unhinted, the verifier's own
splitter thrashes on t at 1.2–1.5 k nodes/s (BigInt at depth 60, caps at 0.85 certain): never.

**[M] The loop at equal budget (T1 crank, cap 60 k/root).**

| iter | catalog | atoms | W₂ | slack | tree nodes | COV / OPEN | holes | open cm median | LP / build |
|---|---|---|---|---|---|---|---|---|---|
| md8 | 469 | 363 | 20.95828 | 0.0417 | 2.71 M | 176 k / 856 k | 41 | 0.602 | 975 s / 1338 s |
| md9 | 525 (+56 hole placements) | 479 | 20.99646 | 0.0035 | 2.70 M | 175 k / 853 k | 7 | 0.594 | 1200 s (IPM kTimeLimit at r10, unconverged) / 2671 s |

Holes fall ~6× per iteration (A74 saw ~4×), but the 56 placements consumed 0.038 of the 0.042
slack at this LP budget (the first md9 solve at the A74 seed load hit the nnz cap after one
round at W₂ = 21.153 OVER; the re-solve with two seeds ran 9 rounds, W₂ 21.42 → 20.996, still
falling ~0.03/round when the IPM timed out), and the open-box count is unchanged: the loop
cannot buy the frontier down — catalog growth is NOT free once the exact holes are deep
(md9's holes collect 0.79, md8's 0.57–0.75). One more iteration crosses 21 at this budget.
Verdict: NO corners4 PASS; the route is closed by Lemma W‴ unless the certificate form changes
(a hint format the verifier streams, or a clause that certifies η-thin boundary layers
in bulk — COVERED-F fires on only 5 % of leaves here).

**[M] C3 gap found: root-enumeration order.** The two frozen implementations enumerate the
2^k×2^k centre grid differently — reference `roots()` ix-major (index = ix·2^k + iy), Rust
`build_roots` iy-major (index = iy·2^k + ix); spec §3.1/§4 are silent. Hint keys "i,j" are
therefore NOT portable: A74's and this campaign's Python-keyed trees, fed to Rust, land on the
transposed root boxes (verdicts unaffected — Lemma S — but 79–1493 hint misses and the
fallback thrash). With trees rebuilt in Rust order (`--root_order rust`), Rust reports
0 hint misses and, on the identical box-pair tree (Python key 4,8 = Rust key 1,2), both
implementations fire rule for rule: vacuous 1726, exempt 6449, nondisjoint 14201, split
22375, examined 43025, covered/covered_f/vacuous_contain 0 — exact agreement (the
VACUOUS-CONTAIN caveat is moot here: 0 firings in both). Rust on the full Rust-keyed md8 tree
(3.15 M nodes, 1767 s, jobs 6): 0 misses, exempt/nondisjoint/vacuous 30 k/245 k/375 k,
covered 476 k + covered_f 78 k, 557 k undischarged (the builder's open leaves), caps at 0.938.
Needs a spec erratum fixing the order (side data only; no verifier edit).

**A76 relay.** No P-B(R) row is added: A76 certified no Trump image compatible with the
corners4 pins within d_min = 0.8445, so the exact class is empty near every Trump image and
the basin row is irrelevant for corners4 — consistent with this wall being emission shape,
not ghost saturation. Canary SAFE at both emissions (`notes/ledger.md`).

## 6.10 [T+M] The U-row in emission, the k4_08 saturation corollary, and Lemma W⁗ (A81, 2026-09-02)

**Setting.** k4_08 (k_S = 4 pins, N = 7, m = 7 boxes, threshold 28 at β = 1), certified
side s0, slack cores δ = 1/1000, class boxes widened to h = 1/2 + ε_box with ε_box = 1/833
(the Lemma P bridge), compatible images G_S = {id, diag} (A71/A76), the rung-k counting
row of `u_ladder.md` Lemma U-ROW per image. Machinery `attempts/A81-slack-verify/code/`:
`pairlp_u.py` (the A74/A77 mixed-depth LP + the U-rows as HARD constraints in every
model, m₂ against the WIDENED boxes), `emit81.py` (v2.1 candidate form + both canaries),
`hintbatch81.py` (the A77 complete-tree builder extended to β > 0: target 1 + βU − Σγ·bz).
Frozen verifiers untouched; the v2.1 form is spec-side data, not a verifier edit.

**Corollary S-08 (saturation at k4_08) [T, exact].** Let g ∈ G_S and let Q₁…Q₇ be the
seven free-square poses of the dilated image g·ẑ at s0 (the crowdfam `trump-sym4` family,
exact rationals; diag = its reflection t ↦ (1−t)/(1+t)). Against the UNIT class boxes
(EPS_MEET-strict open-interior meeting) the family has Σ_{a<b} m₂ = 6; against the boxes
widened by ANY ε_box > 3·10⁻⁷ it has Σ m₂ = 7: member 4 (t = 0.4644, c = (1.2723, 2.4245))
is separated from slot TL(0,0) = (1/2, s0 − 1/2) by exactly −2.96·10⁻⁷ on the unit box
(the dilated 4–0 point contact of ẑ: the gap is λ − 1 ≈ 1.1·10⁻⁷ in the family's own
min SAT gap) and meets the ε_box = 1/833 box with margin +1.69·10⁻³ (exact check in
`emit81.py`/`results/canary_urow.json`, both images). Since the family is core-free,
contained and pairwise interior-disjoint, it is an admissible death witness of value
C(7,2) + β·7 = the threshold for every β ≥ 0: **no plain (P1′)/(P2′) k4_08 certificate
exists at any β**, and the restricted "21 + 6β, margin −β" of A66/A71/A80 was a unit-box
artifact. This is the canary theorem (§4) seen from the k4_08 side — the k4_08-compatible
image of Trump saturates every threshold it is counted in — so an exact-stratum row
(P-B or U-ROW) is NECESSARY for k4_08, not a reserve: it is what removes g·ẑ from the
quantifier. Measured [M, sharp LP, widened boxes, both images' columns, A66 adequacy
catalog + 110 zone/perturbation columns, converged]: plain 28.000000 (the pure family).

**The U-row in the emission LP [T].** In the depth-priced adversary LP of §6.7 add, per
image g, the hard row Σ_{ij: bz_g(ij)=1} z_ij ≤ cap_k = C(N−1−k, 2) (zones of radius r_z
about g's poses; both tilt branches at uprights). Its multiplier γ_g ≥ 0 joins the row
duals y: at any optimal solve, for every catalog pair, Σ_r A_{r,ij} y_r + Σ_g γ_g bz_g(ij)
≥ 1 + βm₂(ij), i.e. y is a restricted covering measure for the discounted claim (P2‴) of
`u_ladder.md` §3, and the value V = Σ y_r rhs_r + Σ_g γ_g cap_k ≥ W₂ + Σ_g γ_g cap_k =: GATE.
The certificate condition (P1‴) is GATE < C(N,2) + βm; slack := threshold − GATE. Sound
for every subset of G_S — but by Corollary S-08 a subset leaves the other image's family
saturating, so at k4_08 BOTH rows are mandatory, and against the two pure families the
net margin is 21γ_g − 10(γ_id + γ_diag) = γ per image at equal γ.

**[M] The two-image mixture dodge (rung 1 is DEAD).** Sharp LP, widened boxes, both
rung-1 rows (cap 10 each): value **28.000000**, γ_id = γ_diag = 0, in-zone loads
(10.000, 9.500) — the rows bind but price nothing. Exact dodge witness
(`results/pairlp_u_k4_08_sharp_wide_k1.json`, `support`): 42 pairs, Σz = 21, each image
family at weight exactly ½ on all 21 of its pairs (10.0 in its zones + one pair moved to a
3·10⁻⁴-displaced variant), class mass id|id = diag|diag = 10.5: value 2·½·28 = 28. Two
half-weight disjoint families load every point by ≤ 1, and the row of each image sees only
its own half. A80's rung-1 gain (26.000 on a ONE-image catalog, unit boxes) was the absence
of the second family; with |G_S| = 2 the mixture halves every per-image counting row. The rung-1 slack the BRIEF budgeted (≈ 2) is therefore 0 in the certificate's own
semantics.

**[M] The widened two-image ladder (sharp, converged unless noted).**

| rung k | cap C(6−k,2) | value V_k | GATE slack 28 − V_k | γ* (id, diag) | in-zone loads |
|---|---|---|---|---|---|
| plain | — | 28.000000 | 0 | — | — |
| 1 | 10 | 28.000000 | 0.000 | 0, 0 | 10.0, 9.5 |
| 2 | 6 | 27.666667 | 0.333 | 1/12, 1/12 | 6.0, 6.0 |
| 3 | 3 | 26.962441 | 1.038 | 0.149, 0.154 | 3.0, 3.0 |
| 4 | 1 | 26.061512 (budget, Lmax 1.055 — not a verdict; ≥ 24.7 scaled) | ≈ 1.94 | 0.332, 0.332 | 1.0, 1.0 |
| 5 | 0 | 25.044526 | 2.956 | (cap 0: rebate-free) | 0, 0 |

(`results/pairlp_u_k4_08_sharp_wide_k*.json`, `logs/`; 345 placements, 30 151 disjoint
pairs, 3 304 with m₂ > 0; every cell's dual is a restricted covering measure, n_ub = 0.)
Against A80's unit-box one-image ladder (−1.00, −1.41, −2.00, −2.56, −3.11, −3.72, −4.49)
the certificate-semantics ladder is shifted up by the saturation unit AND flattened at the
bottom by the mixture: gains per rung 0, 0.33, 0.70, ≈0.9, ≈1.0 (accelerating, not the
A80 flat 0.55 — once the cap is below the mixture's reach the rows start pricing the
cross-image pairs: diag|id support mass 5.67 → 3.16 → 1.84 → 2.08 across rungs 2–5). The
rung-5 row (cap 0: no two free squares of Δ_λ z in distinct zones of one image) buys 2.96
units of restricted slack at sharp semantics — the only rung in the BRIEF's "slack ≈ 2"
regime, and it needs U_5 (A80 T3 census: rung 2 alone = 41 direct + 14 atom certificates
with peeling; rung 5 unpriced).

**[M] Mixed-depth emission under the rung-5 rows (the slack-2 regime, tested).** A74 menu
extended one level deeper (η = 0.1, 0.05, 0.02, 0.008, 0.002, 0.0005; μ = 0.03), both rows,
cold start, 38 cut rounds to excess 1.3·10⁻³, full-store final solve exact (n_ub = 0):
priced value 27.455772, **unpriced W₂ = 27.000000 on 196 atoms** (consolidation 10 717 →
197 → 196 rows changes nothing: the optimal dual IS 196 atoms), GATE = 27.000 (cap 0: no
rebate), slack 1.000. Depth profile of the measure: **4.95 at η = 0.1, 12.08 at 0.05, 2.32 at
0.02, 4.93 at 0.008, 1.57 at 0.002, 1.15 at 0.0005** — 63 % of the mass at ≥ 0.05 and 72 % at
≥ 0.02, against corners4's md8 (Lemma W″: 3–4 % at 0.05, 70 % at 0.008–0.02, 25 % at 0.002).
So the slack IS spent on coarseness as the BRIEF asked. But the depth cost at k4_08 is
2 units (sharp 25.04 → 27.00), not corners4's 0.43: the rung-5 exclusion lives at the zone
scale r_z = 10⁻⁴ (forced by the U_1 reach, `u_ladder.md` §6.1) and the adversary's parked
mass sits 3·10⁻⁴ outside the zones, so every atom that cashes the row's slack must
separate an in-zone pose from its 3·10⁻⁴ variant — a margin below the shallowest menu
level — and the depth-limited measure recovers only the unit-box-like 27 = 21 + 6 of the
variant families (support: id-near|id-near 15.6 of Σz = 20.2). The rung-3 rows (sharp
slack 1.04) give W₂ = 28.000000 at every one of 31 mixed-depth rounds (run stopped: dead at
this menu). The row's slack is ultra-shallow by construction: it can be cashed only at the zone scale, which is exactly
the η-fine boundary structure Lemma W‴ prices. Certificate `certs/pair_k4_08_s0_b1_md_k5.json`
(v2.1 form; canaries SAFE ×2: trump5 witness min gap 1.06·10⁻⁷, Σm₂ = 6; U-row canary: both
image families 7/7 in-zone, 21 > cap, Σm₂(widened) = 7).

**[M] Complete hint trees on the rung-5 measure (`hintbatch81.py`, rule certain, Rust
root order, targets 1 + βU − Σγ·bz; `results/hb_md_k5.json`, `results/deep_md_k5_root7_10.json`).**

| tree | nodes | census (cov / open / hole) | r(d) |
|---|---|---|---|
| all 136 roots, cap 60 k/root (457 s, 4 procs) | 2.92 M | 228 k / 938 k / **1 848** | aggregate d = 7…14: 0.872, 0.853, 0.838, 0.866, 0.854, 0.851, 0.852, 0.841 (64 roots at the cap — the same 64 as A77's corners4 build; 72 complete) |
| root 7,10 (Rust key), cap 2 M, depth 23 (987 s) | 1.15 M | 142 k / 350 k / 396 | d = 10…21: 0.877, 0.884, 0.880, 0.875, 0.870, 0.860, 0.841, 0.828, 0.817, 0.809, 0.801, 0.794 |
| A77 corners4 md8 (slack 0.042), all roots cap 60 k | 2.71 M | 176 k / 856 k / 41 | aggregate d = 7…14: 0.884, 0.872, 0.847, 0.852, 0.862, 0.857, 0.859, 0.852 |
| A77 corners4 md8, root 2,11, 1.59 M, depth 25 | 1.59 M | 187 k / 475 k / 3 280 | d = 14…25: 0.782 … 0.783, flat 0.75–0.78 |

Open-box census on the rung-5 tree: certain-mass median 0.912 (all roots), **1.968 against target
2 on the deep root** (q90 2.15): the residue is the β-boost layer — boxes possibly meeting one
widened class box (U = 1) where the measure delivers ≈ 2 but not certainly — a frontier
source that does not exist at corners4 (β = 0) and that box widening creates at all 7
slots. Holes: 1 848 at cap 60 k (1 797 at m₂ = 0 collecting 0.57–0.90, 51 at m₂ = 1
collecting ≈ 1 against 2), against corners4's 41: the coarse measure is far less complete
on the continuum, and (A77 loop law) deep holes cost slack one-for-one when harvested.

**Lemma W⁗ (retention vs slack) [M+T].** The per-level frontier retention of a complete
spec-§4 hint tree is set by the FRONTIER STRUCTURE of the measure (the loci where coverage
responsibility hands off between atoms, and, at β > 0, the loci where the U-bound changes
— the ε_box-widened box boundaries), not by its total slack: at slack 1.0 (k4_08, rung 5,
63 % of the mass at η ≥ 0.05) the measured r(d) is 0.84–0.87 aggregate and 0.79–0.88 on a
single root to depth 21, ABOVE the tight corners4 measure's 0.75–0.86 (slack 0.042). The
mechanism is a scale separation: (i) the U-row's slack exists only at the zone scale (its
exclusion is 21 pairs inside 10⁻⁴-boxes, and by the A76 saturation law the adversary
parks at 3·10⁻⁴ with no loss), so a measure at any menu depth ≥ 5·10⁻⁴ sees at most the
unit-box-like 27 and any atom that cashes the row must have margin < 3·10⁻⁴ — the η-fine
structure Lemma W‴ prices; (ii) the slack that IS available at coarse depth (1 unit here)
fattens atoms but does not remove handoff loci: a covered leaf still needs every
placement of the box to collect the same atoms, and the number of handoff loci is a
property of which atoms serve which regions, not of how much they over-deliver; (iii)
β > 0 adds the box-meeting boundaries as target discontinuities of height 1. Tree-size
law: frontier growth 2r ≈ 1.6–1.75 per level as in W‴; root 7,10 alone has 3.5·10⁵ open
boxes at widths ≈ 0.06 and needs 6–12 more levels to the measure's dominant 0.02–0.05
scale (≈ 10⁷–5·10⁸ nodes for that root, ≈ 10⁹–3·10¹⁰ over the 64 budget roots) and ≈ 40
to its 5·10⁻⁴ tail (10¹⁵) — the W‴ wall, unchanged in order. *Proof of the T-half:* Lemma S
plus the observation that COVERED at a box needs certain membership of every counted
atom for every placement in the box (spec §3.4, an iff), so a box straddling a membership
boundary of any atom the certificate relies on is never COVERED whatever the surplus;
the surplus can only substitute atoms, and a substitute has its own boundary. ∎

**Verdict.** Slack does NOT buy verifiability: the wall is intrinsic to pair geometry (and
worse at β > 0), not to tightness. T2 not entered; no v2.1 verifier was written (the v2.1
form exists only as spec-side data in the emitted candidate). Corollary S-08 also closes
the plain boosted k4_08/k4_11/k4_03 route (every one-short class carries a compatible
Trump image saturating its widened-box threshold — k4_11/k4_03 via their own images, A71)
independently of verification cost. The protected tier redirects to conditioning trees
(`h10_stuck.md` route 3 / A60-style branch on which square deviates), where the
exact-stratum content (basin, U_R) enters as disjunctive branching rather than as a
priced row.

**Canary (per run) [M].** trump5: the dilated Trump family is an exact death witness at
δ = 1/1000, ε_box = 1/833 (min SAT gap 1.06·10⁻⁷ = λ − 1, Σm₂ = 6) — SAFE, twice
(`attempts/A81-slack-verify/results/canary_trump.json`). U-row: both image families sit
7/7 in their own zones (distinct slots), core-free and contained, Σm₂(widened) = 7, 21
discounted pairs > cap — the rows exclude exactly the pure image families through the
exact-stratum skeleton mismatch; Trump (skeleton trump5) is outside the quantifier
(`results/canary_urow.json`). SAFE.

**Discipline.** One LP at a time (the sharp ladder and the emission ran sequentially; the
hint builder used the second slot at 4 procs), BLAS pinned, the 6 GB commit gate held at
every LP start (rung 5 waited out a 23-minute dip to 5.7 GB); A57/A60/A61 untouched;
frozen verifiers untouched (import-only for roots/clip); certs/ new files only.

**Pointers (this section doubles as A81's findings file; the harness blocks
`notes/findings.md` as it did for A80).** `attempts/A81-slack-verify/code/`: `catalog81.py`
(A80-rig catalog, both images + perturbation columns), `pairlp_u.py` (A77 mixed-depth LP +
U-rows in every model, widened-box m₂, GATE = W₂ + Σγ·cap, every accepted consolidation
round dumped as a candidate, adversary support dump), `emit81.py` (v2.1 candidate + both
canaries), `hintbatch81.py` (A77 builder + β/U/zone targets; β = 0 census byte-identical),
`retention81.py`. `results/`: `pairlp_u_k4_08_sharp_wide_{plain,k1..k5}.json` (ladder +
supports), `pairlp_u_k4_08_md_k5.json` + `pair_primal_k4_08_b1_md_k5_{full,c0,c1}.json`,
`hb_md_k5.json`, `deep_md_k5_root7_10.json`, `canary_{trump,urow}.json`. `certs/`:
`pair_k4_08_s0_b1_md_k5.json` (v2.1 candidate, 196 atoms, W₂ = 27.000101),
`pair_k4_08_s0_b1_sharp_k5.json`; hinted trees regenerable (gitignored).

## 7 What remains open for a certified pair kill (the honest ledger)

* [M, pilot] the fractional pair-LP verdict per class — A66 measures k4_08 (boosted) and
  corners4 (β = 0 and boosted) at restricted-LP strength; a restricted value above threshold
  refutes the route for that class (restricted rows lower-bound every certificate's W₂).
  A71 (2026-09-02): k4_11 = 21 + 6β and k4_03 = 21 + 4β EXACTLY (margin −β, zero fractional
  excess, adequacy τ_f = 7.000000 per class) — the whole one-short critical tier shares the
  k4_08 signature; stuckness-row soundness now standalone in `stuck_rows.md` (SR-1/SR-2),
  with exact P-B image sets G_S = {id, diag}/{id}/{diag}/∅ for k4_08/k4_11/k4_03/corners4.
* [S] the verifier: `verify_pair.py` is NEW trusted code (C3-scale trust investment; the
  clean-room spec is `docs/specs/pair_certificate_v1.md` §3). Not in the TCB until a second
  implementation or a Lean port exists.
* [C] window form: the slack-core grid obligation, shared with every fixed-side kill (B.4),
  plus the ε_box widening per slab.
* [C] the k ≤ 3 tier: Lemma P applies verbatim (their boxes and censuses are in
  h10_boxspec.json); per-class LP verdicts not yet priced.
