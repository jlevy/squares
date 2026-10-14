# Theorem U (one-square rigidity of ẑ): U-O1 executed, U-O4 composed — A65, 2026-09-01

Target: obligation **U-O1** of `unique_transfer.md` §5 (the 11 re-insertion certificates) and
the composition **U-O4** (how Theorem U + the existing D/E nodes discharge the uniqueness
collapse). Labels as in `unique_transfer.md`: [T] proved, [S] soundness statement routine given
cited items, [M] measured/computed exact, [C] open obligation.

**Statement (Theorem U, unique_transfer.md §4).** Let P be a packing at side ŝ consisting of 10
squares of ẑ (exact positions and orientations) together with one further unit square Q. Then
Q is the missing square of ẑ, i.e. P = ẑ.

## 1 [M] The certificate family (U-O1), executed

Eleven certificates `attempts/A65-low-k-closure/certs/u_reinsert_00.json … u_reinsert_10.json`
(format `case-lp-certificate-v1`), emitted by `attempts/A65-low-k-closure/code/emit_u.py`.
Common data:

* **side** s″ = 3877083591023/10¹² — rational, strictly above the A22 enclosure of ŝ
  (ŝ ≤ z0_s + 10⁻⁵⁰ < s″, checked exactly), inside T1's isolating interval, and **realised**:
  `certs/trump11_certificate_tight.json` is a verified 11-packing at exactly this side, whose
  coordinates are the dilated-and-rounded ẑ (centres λĉ rounded to 10⁻¹⁴, common tilt replaced
  by the convergent t_r = 2731751/7468508, |t_r − t̂| ≤ 10⁻¹³);
* **cores**: for certificate i, the 10 squares j ≠ i of the tight file, half-side
  a = 4999/10000 (slack δ = 10⁻⁴), tilt tm = t_r (0 for the six uprights);
* **budget** 1 (n = 11, r = 10), **atoms empty, Σw = 0 < 1** — the free space does all the work;
* **nofams**: one zone F_i = centre box of half-width 10⁻³ around the tight file's (cx_i, cy_i),
  t-intervals [t_r − 10⁻³, t_r + 10⁻³] for the five tilted squares, and for the six uprights
  the PAIR [0, 10⁻³] ∪ [999/1000, 1] (the t ≈ 1 branch is the same geometric square
  re-parametrised mod π/2 — see §3).

**Verification [M]:** all 11 PASS under the audited `verify_case.py` (byte-identical copy,
`attempts/A65-low-k-closure/code/`), cold single invocations at the composed-results
convention `--depth 60`, split 3, strict-margin 0, jobs 1; reports
`certs/u_reinsert_*.report.json`, logs `logs/u00.log … u10.log`. Box counts 424–3048,
sub-second each, zero atoms consulted: every non-exempt box discharges VACUOUS or EXEMPT-core.

**Falsifier control [M]:** `certs/u_control_00_nonofam.json` = certificate 00 with the pocket
exemption deleted. It FAILs (exit 1) with every witness a HOLE of exact mass 0 in the single
cluster θ ≈ 0, centre ≈ (0.5000014, 0.5000014) — precisely Trump's own pocket. So the PASSes
are not vacuous (the hypothesis is realisable — Trump realises it), the exemption zone is
load-bearing exactly at the true pocket and nowhere else, and the measured re-insertion wiggle
(~1.4·10⁻⁶ ≪ the 10⁻³ zone) confirms the zone sizing.

## 2 [T+M] Side conditions: the exact ledger (`results/u_ledger.json`)

Truth anchor: A22 `krawczyk_cert.json` — rational z0 with ‖ẑ − z0‖∞ ≤ r₀ = 10⁻⁵⁰
(A22 notes §3; the uprights are exactly upright at ẑ). All arithmetic below is exact
`fractions.Fraction` on interval endpoints, with ONE stated exception: the two evaluations
|2·atan(t_r) − θ₀| ≤ 10⁻¹³ and |tan(θ₀/2) − t_r| ≤ 10⁻¹³ (θ₀ = A22's common rational tilt)
are mpmath at 80 digits with outward slop 10⁻¹³ against measured ~9·10⁻¹⁶ — the same trust
tier as A22's own interval arithmetic (E.IV item), noted here and in the emitter header.

* **λ interval.** λ = s″/ŝ ∈ [s″/(z0_s + r₀), s″/(z0_s − r₀)]; λ − 1 = 2.580·10⁻¹⁰ (both ends).
* **(H) core containment.** For each j, the core K_j (half-side a, tilt t_r, centre = tight
  coordinates) sits inside the OPEN interior of Δ_λ(ẑ_j): in ẑ_j's body frame the corner
  ∞-norm is ≤ a·(cos + sin)(Δθ_j) + |off_x| + |off_y| with Δθ_j ≤ 2·10⁻¹³ + 2r₀ (tilted,
  X.1 of `theta_t_transfer.md`) resp. ≤ 10⁻⁵⁰-scale (uprights), and the centre offset bounded
  through the λ- and z0-intervals. **Margin lower bound ≥ 9.9997·10⁻⁵ > 0 on every core**
  (per-square values in the ledger; the budget is δ = 10⁻⁴ against offsets ~2·10⁻¹⁴).
* **Exemption lands in the basin.** λ⁻¹F_i ⊆ the rBasin = 3/2000 box of `theta_t_transfer.md`
  X.3 around (ĉ_i, t̂_i): centre deviation ≤ 10⁻³ + (1 − λ⁻¹)·|c| + rounding ≤ 1.0000010·10⁻³,
  tilt deviation ≤ 10⁻³ + 10⁻¹³ + r₀ (tilted) resp. the §3 bound (uprights) —
  **all < 3/2000 with ≥ 33 % headroom** (ledger `dev_*` fields).

## 3 [T] The t ≈ 1 branch for upright pockets (mod-π/2 bookkeeping)

`verify_case.py`'s parameter t = tan(θ/2) ∈ [0, 1] covers all orientations of a square mod its
own π/2 symmetry; a near-upright placement can appear at t ≈ 1 (θ ≈ π/2 ≡ 0). For the upright
pockets the zone therefore carries the second interval [999/1000, 1], and its basin containment
is exact: t ∈ [1 − h, 1] (h = 10⁻³) ⇒ the equivalent tilt θ′ = θ − π/2 satisfies
|θ′| = 2(atan 1 − atan t) = 2·atan((1−t)/(1+t)) ≤ 2h/(2−h), so the equivalent t-coordinate
|t′| = tan(|θ′|/2) ≤ x + x³ with x = h/(2−h) (atan x ≤ x ≤ tan x ≤ x + x³ on [0, 1/2]):
numerically ≤ 5.004·10⁻⁴ < 3/2000. In A36's native θ-box the same branch reads
|θ′| ≤ 2/1999 < 37/10000 directly.

## 4 [S] What a PASS + ledger proves: U-O1 discharged

Fix i and let P be a packing at side ŝ with the ten squares ẑ_j (j ≠ i) and one further unit
square Q. Dilate by λ = s″/ŝ (Lemma B machinery, `closed_disjoint_bridge.md`): Δ_λP is a
family of 11 pairwise-disjoint CLOSED unit squares in [0, s″]² (B.0(a),(b)), and by §2 each
core K_j is inside the open interior of Δ_λ(ẑ_j) — hypothesis (H) with 10 distinct owners.
The certificate has one NO-family, so **Lemma B-NO** (B.2″) applies verbatim: some non-owner
square of P — and Q is the only non-owner — has (c_Q, t_Q) ∈ λ⁻¹F_i. By §2–§3 that places
all 33 coordinates of P within rBasin of ẑ (ten exactly, the eleventh inside the contracted
zone). P is a packing at side ŝ, so σ(P) ≤ ŝ; the `basin` axiom (= A36's certified theorem
after the X.1/X.3 transfer) gives σ ≥ ŝ on the box with **equality iff the configuration is
ẑ**. Hence P = ẑ, and Q is the missing square. ∎ (Theorem U, per removed square; the D4 × S₁₁
covariance is inherited from ẑ's symmetry class as in unique_transfer §4.)

The `nofams` field is load-bearing here and nowhere else in the composition; per B.2″ the
exemption sends the dilated coordinates INTO the zone, which is the desired conclusion, not a
leak. The B.2″ outward-widening caveat for downstream consumers is vacuous here because the
consumer is §2's exact containment computation, done at this λ.

## 5 [S] U-O4: the collapse composition, assembled

Chain (unique_transfer §2, [S]): every packing z at side ŝ reaches a teleport-stuck z* in ≤ 11
CC-2/CC-2′ exchanges, each step changing ONE square's position. Kill layer (§3): z* is excluded
unless its stratum is trump5 (then z* = ẑ mod G by `trump_residual` + `basin` — nodes
D.TREE/D.SLAB/D.S6/E.COORD, the A60 campaign) or K1-protected (obligation U-O2 = H10-stuck,
`h10_stuck.md`) or a certified class not yet instantiated at ŝ (obligation U-O3 = the
k5_11/k5_16 window forms, A57 G1 campaign — cited, not redone). Collapse (§4, [T given U]):
descending the chain, each z_j is 10 squares of ẑ plus one square elsewhere, so **Theorem U —
now carried by §1–§4 above — forces z_j = ẑ mod G at every step**, hence z = ẑ mod G.

Net ledger for the uniqueness clause after A65:

* **U-O1 — DISCHARGED** (this file §1–§4; residue = the trust-tier items below);
* **U-O2 — OPEN** (= H10-stuck, the k ≤ 4 tier; see `h10_stuck.md`);
* **U-O3 — OPEN, owned by A57** (G1 slack-core window campaign, in flight);
* **U-O4 — as axiomatised**: `trump_residual` + `basin` (D.TREE/D.SLAB/D.S6 open under A60;
  E.COORD proved-prose). Theorem U consumes ONLY `basin`'s equality clause at the centre slab —
  none of the open D-node content — so U-O1's discharge does not wait on A60.

Trust residue of U-O1 (beyond the audited verifier): A22's z0/r₀ enclosure (mpmath.iv tier,
already in the TCB via `basin`/E.COORD) and the two dps-80 tilt evaluations of §2. Both
disappear under the planned t-reparametrised A22 re-emission (theta_t_transfer X.4).

**Canary.** Trump's configuration survives — it is the exemption: the control run (§1) shows
the certificates' only hole is Trump's own pocket, and the composed conclusion of §4 is
"P = ẑ", never an exclusion of ẑ. At no step is any statement asserted that ẑ falsifies.
