# Independent referee report

VERDICT: SOUND

**Finalized 2026-11-02 16:07:28 PST. High confidence.** The claimed lower bound is supported by a separate integer-only verification of **all 600 directions**, each over its full centre domain. The supplied floating-point checker has a demonstrated false acceptance and is **not** relied upon for this verdict. Its fatal numerical defect is superseded here by the independent full proof; it must still be fixed before using that checker as a general verifier.

## Exact premises

All premises were recomputed directly from the submitted JSON using independently written Python `Fraction` code; see `work/full.premises.json` and `work/exact_audit.json`.

| Premise | Exact result |
|---|---|
| Target and side | n=94; L=1993/200 |
| Core | B=19884161/19900000, strictly between 0 and 1 |
| Mass | M=9399999/100000; 94−M=1/100000 |
| Net | D=83/120000; last=599; 600 directions |
| Shrink | B(1+D)=2387749705363/2388000000000 < 1 |
| Stronger tangent-form shrink | B(1+D/(1−D²/4))=1146119721592254871/1146239862908900000 < 1 |
| Endpoint | t_last=49717/120000; t_last²+2t_last−1=3860089/14400000000 > 0; t_last < 1/2 |
| Nonempty domains | L²−2B²=19266759197451079/198005000000000 > 0; all 600 exact domains are nonempty |
| Atoms | 853 valid nonnegative-mass rectangle orbits inside [0,L]²; 6,824 expanded terms; no points or segments |

The mass sum equals the declared total exactly. The JSON SHA-256 is `b8b03ee83fd2738f723759e8a54442adb55e607a211dd57d28873a62db9c749c`, matching the manifest. Every rectangle and B is exactly the published quantity multiplied by λ=1993/1990; masses are unchanged. The supplied CSV contains each index 0..599 exactly once, all marked V. This establishes receipt completeness, not numerical soundness.

## Lemma-by-lemma audit

**Net and core containment: sound.** Fold an individual square's angle to φ∈[0,π/4]. With τ=tan(φ/2), a nearest node has |τ−rD|≤D/2, hence z=|tan((φ−θ_r)/2)|=|τ−rD|/(1+τrD)≤D/2. The core's extent along each unit-square axis is

    B(1+2z−z²)/(1+z²) ≤ B(1+2z) ≤ B(1+D) < 1.

Thus the closed core lies strictly inside the unit square. The requested stronger tangent condition also passes exactly, using tan|φ−θ_r|≤D/(1−D²/4). Its omission from `prep.premises()` is not fatal: the displayed half-angle proof already proves containment under the simpler checked premise.

**Centre domain: sound for this input.** Let a_r=max(0,rD−D/2) and ρ(a)=(1+2a−a²)/(2(1+a²)). The unit square's wall distance is at least ρ(a_r), since ρ increases on the folded interval. Core containment also implies distance at least B(c_r+s_r)/2. The required quadrant is therefore exactly

    [L/2, L−max(ρ(a_r), B(c_r+s_r)/2)]².

Both the claimant and independent preparation use it. Every a_r is below tan(π/8), checked by a_r²+2a_r−1<0. At the last node a=33117/80000 and this polynomial is −4544311/6400000000. The slightly overshooting final angle causes no domain error.

**Rescaling: fresh verification is indispensable.** At direction 0 the inverse-scaled new domain extends past the original domain by exactly 3/3986. All 200 common angles have strictly larger inverse-scaled upper ends, checked exactly. The common indices are multiples of 3 through 597; 400 angles are absent from the old net. Coverage on neither the added centres nor the new angles follows automatically from the published finite-net certificate.

**D4 and counting: sound, with a minor prose repair.** One global reflection cannot fold differently oriented squares simultaneously. Apply reflection to each square separately, transfer its coverage by measure invariance, and reflect its core back into the original square. The chosen cores stay inside the original disjoint interiors. Quarter turns preserve a fixed square direction modulo π/2 and move each centre into the checked quadrant. The eight-image expansion, including coincident images, is correct. Thus 94 disjoint cores of mass at least 1 contradict M<94.

## Supplied checker audit

**Fatal to reliance on its general numerical soundness claim: actual false acceptance.** The unmodified preparation, C checker and summary report `ALL_DIRECTIONS_VERIFIED`, 43/43, on `work/false_certificate.json`. This certificate has n=1, L=3/2, B=9/10, D=1/100, last=42 and 1,000 identical orbit representatives [74/100,76/100]², each of mass (1−10^−20)/1000. All exact premises pass.

Every queried core contains the entire central rectangle. Its centre coordinates are between 3/4 and 1, so every rectangle offset has coordinate magnitudes at most 26/100. Since c+s<3/2, each slab extent is below 39/100 < B/2. Every exact capture is therefore **1−10^−20 < 1**. One unit square plainly fits in the square of side 3/2.

Nevertheless every direction is verified at its root, without long-double fallback. A diagnostic copy changing only output precision reports centre sum **1.000000000000125** and claimed lower bound **1.0000000000000251**. The constant `1e-13 * ins` fails to cover accumulation error in 8,000 inside terms. Evidence: `work/false_premises.log`, `work/false_full.jsonl`, `work/false_summary.json`, `work/false_full_precise.jsonl`. Original sources were not edited. This is a concrete false acceptance, not a hypothetical rounding concern.

A second counterexample uses **exactly 853 orbits and 6,824 expanded terms**, matching the submitted certificate's size. With the same central rectangle, total mass, side and net, but unequal positive orbit weights, all 43 directions again return VERIFIED. Its root centre sum is **1.0000000000001783** and claimed lower bound **1.0000000000000784**, while every exact capture remains 1−10^−20. The exact weights and results are in `work/false_certificate_853.json` and `work/false_853_summary.json`; full receipts are `work/false_853_full.jsonl`. This also uses no fallback.

**Additional numerical defect:** on this ARM platform both mantissas have 53 bits and both types occupy 8 bytes (`work/platform.txt`). SOUNDNESS §4 assumes 64-bit precision for long double, so its fallback constants lack the stated justification here. The counterexample above already fails in the double path, independently of portability. The informal per-polygon operation count also is not a complete conditioning and summation proof.

**Otherwise appropriate decisive paths:** exact input parsing and mathematical domain construction; inward rectangles and downward densities; exact-arithmetic erosion and edge-length derivative formulas. Dropping rectangles only weakens the bound, as the supplied checker does not inherit derivative bounds. These sound ideas do not repair the false acceptance.

**Minor for this artifact, serious operationally:** `summarize.py` never compares received indices with the expected complete net; `runall.sh` does not robustly enforce all shard successes. A nonempty verified subset can be labelled ALL_DIRECTIONS_VERIFIED. The actual submitted CSV is complete, so this does not show missing directions here. Some reproduction paths incorrectly retain `results/` instead of `claim/`.

Another minor arithmetic error in the report is its stated similarity ceiling near 9.9725. The exact necessary ceiling as the net step tends to zero is L_original/B_original=99500/9977. This has no effect on the submitted L=9.965 certificate.

## Independent verification

The independent implementation is `work/independent.py` and `work/intcheck_final.cpp`; its proof and overflow limits are in `work/INTEGER-SOUNDNESS.md`. All preparation and decisions use exact rational or integer arithmetic. Areas use downward-rounded trapezoids below concave vertical sections; derivatives use outward-rounded edge-length intervals. Branch and bound covers the full centre domain, including the added wall region. Floating point appears only in timing output.

All 2,500 kernel comparisons against independent exact rational polygon/segment clipping passed, including axis cases, thin rectangles and direction 599. Another 599,800 signed floor divisions across all directions matched direct signed 128-bit division. Reciprocal division is also justified algebraically; integer-size limits are checked at admission.

The initial sample is **0,48,96,144,1,2,4,5,7,8,10,11,13,14,599**. All 15 directions are VERIFIED over their entire centre domains (`work/sample.jsonl`); eleven are absent from the old net. The lowest exact capture found at these sampled centres is in **[1.001123004123936, 1.001123004123937)** at r=144, centre

    (12226951825239/2199023255552, 32719819833211/4398046511104).

`work/exact_centres.json` retains the full exact fractions. This is an observed point value, not the exact global minimum. The independent full-net replay completed with **600/600 VERIFIED**, indices 0..599 present once each, including all **400 new angles**. It checked **166,440,592 nodes** and **83,220,596 accepted leaves** in **4801.463 CPU seconds** (one thread; initial sample: 274.170 CPU seconds). The minimum whole-domain certified bound is exactly **4398046511113/4398046511104**, at least 1.000000000002046. The lowest exact capture among the full replay's 600 retained admissible centres lies in **[1.001123004123936, 1.001123004123937)**, at r=144, centre (12226951825239/2199023255552, 32719819833211/4398046511104). All 600 retained point captures were recomputed by the separate rational clipping oracle. Full logs, exact point values, totals and file hashes are in `work/full.jsonl`, `work/full_exact_centres.json` and `work/final_summary.json`. The observed point minimum and certified whole-domain lower bound are different quantities; no exact global minimum is asserted.

| Mutant | Independent result |
|---|---|
| Similarity to L=9.975, same net | REJECT at exact premises: B=3980823/3980000>1; both shrink conditions fail |
| Masses ×0.998 | REJECT, exact admissible r=144 witness; capture in [0.999120758115689,0.999120758115690) |
| Heaviest orbit removed | REJECT, exact admissible r=0 witness; capture in [0.738040584502493,0.738040584502494) |
| Extra control: L=9.975, B held at the claimed admissible value | All premises pass; REJECT by exact admissible r=144 witness; capture in [0.998111028379968,0.998111028379969) |

Witness centres and full rational captures are in `work/mutant_results.json`. The mass-reduced and deleted-orbit instances were also refused by the integer executable. A near-threshold unresolved mutant leaf is only a refusal; the listed rejection conclusions rest separately on exact counterexamples.

**Exact weakest point and confidence:** high confidence in the claimed bound, conditional on the independently written integer verifier and compiler. The remaining trust boundary is its manual code/proof audit, especially the centre-box derivative enclosures, their inheritance, and the fixed-width overflow argument documented in `work/INTEGER-SOUNDNESS.md`. This is not a proof-assistant formalization. All 600 direction domains are covered; no numerical decision depends on floating point. The demonstrated defects in the supplied checker remain fatal to relying on its original general soundness argument, but no longer leave a gap in this independently established claim.
