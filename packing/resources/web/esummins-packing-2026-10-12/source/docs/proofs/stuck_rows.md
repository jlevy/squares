# The stuckness rows — CC-2′ 2-crowds as exact LP rows (Lemma P's input), A71, 2026-09-02

Lemma P (`pair_kill.md` §2) consumes the stuckness hypothesis in one step (step 4) and cites
CC-2′ for it. This file is the standalone row-soundness account that step compresses: WHICH
teleport-blocked configurations yield WHICH pair/occupancy constraints, in exactly the LP-row
form the pair-certificate composition prices, at drain-v3 rigor. Nothing here changes Lemma P;
it discharges the BRIEF-T2 obligation that its input be formulated and proved as a named lemma
rather than inline. Labels: [T] proved, [S] routine given cited items, [M] measured/computed
exact, [C] open.

Standing ingredients (all cited, none re-proved): the selection chain and the definition of
**teleport-stuck** (`unique_transfer.md` §2: every completable slot box is either
simple-clipped or met, open interiors, by ≥ 2 non-simple squares); CC-1(ii)/(iii) and CC-2′
(`attempts/A58-clear-corner/notes/theory.md` §§1–2, re-based on teleport-stuckness per
`h10_stuck.md` standing-ingredients paragraph — K*-maximality is used only to OBTAIN a stuck
packing, never below); the InStratum-exact semantics (`instratum_bridge.md`: in stratum
exactly S the non-pin squares are exactly the non-simple ones); the unclipped completable-box
census and its s-stability (`attempts/A58-clear-corner/results/occupancy_matrix.json`, A53
L2(iv) slot arithmetic; exact per-class lists `attempts/A65-low-k-closure/results/h10_boxspec.json`);
Δ_λ facts B.0(a)–(c) (`closed_disjoint_bridge.md`).

## 1 Setting and the row objects

Fix a Young class S (k pins), a side m̃ ∈ [3.82, s0], and the unclipped completable boxes
B_1(m̃) … B_m(m̃) of S: the Young-ready cells of S's corner diagrams plus the clear-corner
roots (offsets ≤ 2), MINUS every box whose open interior meets a pin square of S at side m̃
(the simple-clip census). Box centres are slot-affine: b_i(s) = α_i + β_i·s per coordinate
with β ∈ {0,1}, |α| ≤ 5/2 (A56 P1; verified against the census lists — every k4-tier box
centre coordinate is one of ±1/2, ±3/2, ±5/2 modulo the β·s term).

**[S] Census s-stability.** The list {(α_i, β_i)} and the clip verdicts are constant over
m̃ ∈ [3.82, s0]: clip incidence between box i and pin j is a sign condition on
|b_i(s) − p_j(s)| vs 1, whose coordinates are (α_i − α_j) + (β_i − β_j)·s — affine in s with
integer-or-half-integer α-parts, and the A53 L2(iv) slot-separation margins keep every such
comparison strictly on one side across the window (the census was computed once at s0 and its
margins exceed the window width; `occupancy_matrix.json` records the exact values). Hence
"the s″ list read at m̃" in Lemma P step 4 is well-defined: same (α, β) data, evaluated at m̃.

**The row family R_S (LP form).** For a certificate at side s″ with widened boxes
B̃_i (centre b_i(s″), half-side 1/2 + ε_box), the stuckness rows are the (P2′) instances

>  ROW_i:  for every unordered pair {Q, Q′} of admissible core-free interior-disjoint
>  placements with int Q ∩ int B̃_i ≠ ∅ and int Q′ ∩ int B̃_i ≠ ∅:  μ₂{Q,Q′} ≥ 1 + β·(…),

i.e. exactly the rows of the frozen `pair-certificate-v1` semantics in which box i
contributes to m₂. The certificate does not carry ROW_i separately: (P2′)'s
m₂-counting bonus IS the simultaneous LP encoding of all m rows (a pair meeting r boxes
pays the base 1 plus β·r — the r rows share the base). What stuckness must deliver, and all
it must deliver, is the REVENUE side: a stuck packing realises at least m pair-incidences.

## 2 [T] Lemma SR-1 (which blocked configurations yield which constraints)

**Lemma SR-1.** Let z* be a teleport-stuck packing at side m̃ with skeleton exactly S. Then
for every unclipped completable box B_i(m̃) there exist TWO DISTINCT non-pin squares
q_{a(i)}, q_{b(i)} of z* with int q_{a(i)} ∩ int B_i(m̃) ≠ ∅ and int q_{b(i)} ∩ int B_i(m̃) ≠ ∅.

*Proof.* Teleport-stuckness gives, at every completable slot box, the alternative: either the
box is simple-clipped, or ≥ 2 non-simple squares meet its open interior
(`unique_transfer.md` §2 endpoint property; = CC-2′'s R1/R2 with R0 "empty" and "single
non-simple meeter" both excluded by the exchange). B_i is by hypothesis UNCLIPPED: no pin
square's open interior meets int B_i. In stratum exactly S, simple squares = pin squares
(InStratum-exact), so "simple-clipped" is false at B_i and no simple square meets it at all;
the alternative collapses to R2. The ≥ 2 non-simple meeters are non-pin squares. ∎

Remarks. (i) The EXACT stratum hypothesis is load-bearing in two places: it turns the census's
pin-clip exclusion into the R1 exclusion, and it makes "non-simple" = "non-pin" so that the
meeters are among the N = 11 − k free squares Lemma P prices. A monotone hypothesis ("z*
contains the pins of S") would leave R1 open (an extra simple square not in S could clip the
box) — same failure surface as Lemma P-B's monotone trap (`pair_kill.md` §6). (ii) CLIPPED
completable boxes yield NO row: the alternative can be satisfied by the clipping pin, which
prices nothing (pins own their cores and stand outside the pair measure's quantifier). The
census subtraction is therefore not a convenience but the exact boundary of the input.
(iii) Nothing else is consumed: no CC-3 (certificate-backed occupancy — those rows are
side-s0-only and stuckness-free; absorbing them is `h10_stuck.md` §6's separate ledger item),
no CC-4 (persistence/contact content — that is the A50-G1/FJ layer), no corridor geometry.

## 3 [T] Lemma SR-2 (row soundness under the bridge: incidences → Σm₂ ≥ m)

**Lemma SR-2.** Setting of Lemma P: s″ certified side, λ = s″/m̃ ∈ (1, 1 + δ/A),
ε_box ≥ 3(λ − 1), z* teleport-stuck at m̃ with skeleton exactly S, Δ_λ the centre dilation.
Then the dilated free squares Δq_1 … Δq_N satisfy

>  Σ_{a<b} m₂(Δq_a, Δq_b) ≥ m,  with m₂(Q,Q′) = #{i : int Q ∩ int B̃_i ≠ ∅ ≠ int Q′ ∩ int B̃_i}.

*Proof.* Fix i and the pair {a(i), b(i)} from SR-1.

1. *Incidence survival.* If x ∈ int q ∩ int B_i(m̃) then λx ∈ int Δq ∩ int λB_i(m̃) (dilation
   is a homeomorphism carrying interiors to interiors; int Δq = λ·int q by definition of Δ_λ
   on the centred square). Per coordinate, the centre of λB_i(m̃) is λ(α_i + β_i m̃) and that
   of B̃_i is α_i + β_i s″; their difference is (λ−1)α_i, |(λ−1)α_i| ≤ (5/2)(λ−1), while the
   half-side grows from λ/2 = 1/2 + (λ−1)/2 ≤ 1/2 + ε_box... more precisely every point of
   λB_i(m̃) is within (5/2)(λ−1) + (λ−1)/2 = 3(λ−1) ≤ ε_box of B̃_i's un-widened box in the
   sup-metric, hence λB_i(m̃) ⊆ B̃_i, and interior into interior since the containment has
   the strict half-side margin ε_box − 3(λ−1) ≥ 0 plus the openness of the sets: concretely
   int λB_i(m̃) ⊆ int B̃_i because λB_i(m̃) ⊆ B̃_i and interiors are monotone. So both
   Δq_{a(i)}, Δq_{b(i)} meet int B̃_i: box i contributes 1 to m₂(Δq_{a(i)}, Δq_{b(i)}).
2. *No double counting, exact tally.* Define φ(i) = {a(i), b(i)} (any measurable choice; the
   chain is not canonical and none is needed). For an unordered pair {a,b},
   m₂(Δq_a, Δq_b) ≥ #φ⁻¹({a,b}) — by step 1 every box i with φ(i) = {a,b} is counted in
   m₂(Δq_a, Δq_b), and distinct boxes are distinct indices in the m₂ count. Summing over
   unordered pairs: Σ_{a<b} m₂ ≥ Σ_{a<b} #φ⁻¹({a,b}) = m (φ is a total function on
   {1,…,m}). ∎

Remarks. (i) A box with ≥ 3 meeters only helps (any chosen pair suffices; the surplus is not
priced — that is exactly the headroom the death-witness criterion measures from the other
side). (ii) One pair {a,b} serving several boxes is handled by the tally, not excluded by it:
m₂ counts boxes, so a pair meeting r chosen boxes pays 1 + β·r against those r rows at once.
(iii) The λ-strictness is NOT used in this lemma (incidences survive at λ = 1 too); it is
used by the neighbouring steps of Lemma P (core ownership, atom additivity), which is why the
shell stays half-open there and no claim is made at m̃ = s″.

## 4 [M] The per-class row lists (the k4-tier instantiation)

From `h10_boxspec.json` (unclipped census, s-stable per §1), with slot shorthand
w = s − 1/2, v = s − 3/2:

* **k4_08** (N = 7, m = 7, threshold 21 + 7β): boxes at (1/2,5/2), (3/2,3/2), (5/2,1/2),
  (w,1/2), (w,v), (v,w), (1/2,w). Crowdfam floor Σm₂ = 6 (TL root (1/2,w) deficient).
* **k4_11** (N = 7, m = 7, threshold 21 + 7β): boxes at (1/2,5/2), (3/2,1/2), (w,3/2),
  (v,1/2), (w,v), (v,w), (1/2,w). Crowdfam floor Σm₂ = 6.
* **k4_03** (N = 7, m = 5, threshold 21 + 5β): boxes at (3/2,3/2), (5/2,1/2), (w,1/2),
  (w,w), (3/2,w) — two further completable cells are pin-clipped and yield NO row (§2 Rem ii).
  Crowdfam floor Σm₂ = 4.
* **corners4 = k4_13** (N = 7, m = 8, threshold 21 + 8β): eight boxes, no realisable family
  known at all (A65); the β = 0 emptiness form needs no rows from this file.

**P-B scoping (exact, new).** The basin row's compatible-image sets G_S (D4 images g of
trump5's five slots with g·slots ⊇ pins(S)), computed exactly at s0 (A71):
k4_08: {id, diag} (|G_S| = 2 — note: TWO images, the A66 pilot's trump-sym4 embedding is the
id member; a basin-discounted k4_08 emission must either declare both zone families or claim
the discount only for the declared subset, which is sound — undeclared images simply forgo
revenue); k4_11: {id}; k4_03: {diag}; k4_13: ∅. The rebate in (P1″) is γ·C(N−1,2)·|G_S| with
the DECLARED G_S.

## 5 [T] The canary identity (why these rows are exactly as strong as they can be)

Trump's packing realises SR-1 with equality on trump5: each of his 6 unclipped boxes has
exactly 2 free-square meeters and the 6 chosen pairs are distinct
(`occupancy_matrix.json` trump_canary; meeter pairs (4,7), (7,8), (8,10), (9,10), (6,9),
(4,6) on BL(0,2), BL(1,1), BR(0,1), TR(0,1), TR(1,0), TL(0,0)), so Σ_{a<b} m₂ = 6 = m with
zero surplus, and by the death-witness criterion (`pair_kill.md` §4) every pair certificate
on a shell reaching ŝ has W₂ ≥ C(6,2) + 6β = threshold: the row family of §§2–3 is saturated
with equality by the packing every argument must spare. Consequently: (a) no generic
strengthening of the stuckness input (more pairs per box, corner-coupled bonuses priced into
the SAME threshold) can be sound — it would push Trump's forced revenue above his threshold;
(b) all per-class killing power lives in the JOINT non-realisability of the m pair-incidences
by any actual disjoint family (crowdfam floors, §4), never in the rows themselves. The one
sound refinement NOT priced by v1 semantics: CC-1(ii)'s crowd disjointness across distinct
clear corners (the four squares of two distinct-corner crowds are distinct). Monetising it
needs a threshold term beyond C(N,2) + βm, i.e. a v2 certificate format; recorded as [C],
with the canary constraint that Trump's own distinct-corner crowds ARE disjoint (his
saturation would survive, so a v2 bonus priced on corner-pair rows is not automatically
unsound — the check must be repeated at v2 design time).

## 6 Composition ledger

Lemma P step 4 = SR-1 + SR-2 verbatim; no other consumer exists today. Inputs consumed:
teleport-stuckness (selection chain), InStratum-exact, census + s-stability, B.0 dilation
facts, ε_box ≥ 3(λ_max − 1) per slab. Outputs delivered: Σm₂ ≥ m for the dilated free
family, per class per §4. Open: [C] the k ≤ 3 tier lists are in the same census files and
SR-1/SR-2 apply verbatim; their LP verdicts are unpriced (A71 T2 measures the k4 tier only).
