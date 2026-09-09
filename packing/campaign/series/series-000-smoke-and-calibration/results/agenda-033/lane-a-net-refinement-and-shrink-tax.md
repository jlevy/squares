# Agenda 033, lane A: net refinement, frozen-measure expansion, and the shrink tax on the frozen T-018 atoms

Retained measurement-lane report for
[X-023](../../../../explorations/X-023-three-losses-and-a-new-atom.md), written by a
sub-agent on 2026-09-09 under the breadth survey.
The spike ran as “spike A/C” because it carried direction D2 (frozen-measure expansion,
wave C) alongside D1 and D3; the report is reproduced as delivered, with its own status
labels, and X-023 carries the coordinator’s reading.
The 720-step and 1440-step certificates measured in Part A2 were since frozen, decided
and registered as `T-024`, whose proof packet is
[`t-024-dilation-limit-proof.md`](../../../../../cases/n11_fractional_certificate/t-024-dilation-limit-proof.md);
the numbers below are this lane’s measurement, not that packet’s statement, and nothing
here is a registered round or a new bound.

Retained beside this report: the four crossing-shrink receipts, the frozen-expansion
receipt, the two parent-feasible-domain receipts and the three fixed-site LP receipts,
all listed under [Files](#files); the 51 per-direction `dirmin-*.jsonl` sweep logs are
not retained.

Source: `packing/cases/n11_fractional_certificate/certificate.json` (SHA-256
`b121edbd044b6f326022d8783551efd947c95eec2738269857d039358ac6ae6a`, loaded through
`devtools.decide_certificate.load_frozen_bytes`): L0 = 381/100, B0 = 9977/10000, T =
207107/500000, 181 directions, 1121 atoms, M = 434547/40000 = 10.863675, threshold M/11
= 434547/440000 = 0.9876068. A pass is `m > M/11` decided in `Fraction`s on the
library’s own sweep (`sweep_direction_minimum`) or on `scaled_mass_grid`’s exact integer
grid; floats propose, never decide.
T-022 reference: 3.810025723614703.

## Findings

| # | finding | value | label |
| --- | --- | --- | --- |
| A0 | control: retained certificate replayed on its own net at B0 = 9977/10000 | least mass 4001/4000 at every one of the 181 directions (all 181 minima are exactly 4001/4000); 44 s | EXACT |
| A1 | finer nets at the ORIGINAL B0: more directions alone | S=360: least 96377/100000 (0.96377) < M/11, 3 of the 361 directions fail; S=720: least 96377/100000 (0.96377) < M/11, 8 of the 721 directions fail; S=1440: least 96377/100000 (0.96377) < M/11, 19 of the 1441 directions fail; S=2880: least 96377/100000 (0.96377) < M/11, 39 of the 2881 directions fail (none of the 181 original ones) — every refinement FAILS, always at ~25.0 deg (also 28.3 and 44.2 deg) | EXACT |
| A2 | finer nets at the SHARPENED largest grid B: larger B alone | S=360: B=9988513/10000000, least 4001/4000; S=720: B=9994251/10000000, least 4001/4000; S=1440: B=2499281/2500000, least 4001/4000; S=2880: B=4999281/5000000, least 4001/4000 — every refinement PASSES with every direction’s minimum exactly 4001/4000; the dilation supremum at L0 is then only 3.81000003..3.81000038 (no room left) | EXACT |
| A3 | crossing shrink B_cross(S) (least passing B on the 10^-7 grid, bracket <= 10^-6) and the dilation family bound L0 sqrt(1+D^2)/(B_pass (1+D)) | S=360: B in (2494809/2500000, 4989621/5000000], side sup 3.813539939 = 6350000*sqrt(32400042893309449)/299721721812149 (+0.003514 vs T-022); S=720: B in (2494809/2500000, 9979243/10000000], side sup 3.815730319 = 38100000*sqrt(129600042893309449)/3594594251080001 (+0.005705 vs T-022); S=1440: B in (9979803/10000000, 2494953/2500000], side sup 3.816609503 = 3175000*sqrt(518400042893309449)/598960960743657 (+0.006584 vs T-022); S=2880: B in (9979803/10000000, 2494953/2500000], side sup 3.817158227 = 3175000*sqrt(2073600042893309449)/1197749680743657 (+0.007133 vs T-022) | EXACT (pass at B_pass; the bound is the exact surd) |
| B1 | frozen-measure expansion (B0, 181 directions): largest certified side | L* = 176536859/46335000 = 3.810010985 = L0 + 2*509/92670000 (delta* = 5.4926e-06); m(L) = 4001/4000 on [L0, L*] exactly, then drops to 85353/100000 (0.85353) at direction 0 cell [56, 475] (corner-snug axis core losing the wall orbit at x0 = 1849127/1853400 = B0 - 509/92670000, weight 917/6250 each); composed with T-022: 3.8100367089 (+1.10e-05) | EXACT |
| B2 | library sweep confirmation at L* and L* + 10^-8 | L=3.810010985: least 4001/4000 at k=0, PASS; L=3.810010995: least 85353/100000 at k=0, FAIL | EXACT |
| B3 | m(L) ladder (library sweep, all 181 directions) | L0+1/10000: 85353/100000 (0.85353); L0+1/5000: 85353/100000 (0.85353); L0+1/2000: 85353/100000 (0.85353); L0+1/1000: 39319/50000 (0.78638) | EXACT |
| B4 | expansion with parent-feasible domains (Part C domains + Part B) | L* = 3.810049258 (delta* = 2.4629e-05), first failure at direction 1 mass 0.85353 | EXACT |
| C-sharp | parent-feasible centre domains (h_low within 1e-12 of h(alpha_k)) | least mass 4001/4000 -> 4001/4000 (unchanged), 0 of 181 directions improved, reachable cells 567130649 -> 566589601 (541048 disappear, 0.095%) | EXACT |
| C-coarse | parent-feasible centre domains (h_low within the previous net direction) | least mass 4001/4000 -> 4001/4000 (unchanged), 0 of 181 directions improved, reachable cells 567130649 -> 566823745 (306904 disappear, 0.054%) | EXACT |

## Interpretation

**The shrink tax cannot be recovered from the frozen atoms by refining the net alone.**
The two effects separate cleanly.
At the original shrink B0, every refinement of the net (360 … 2880 steps) fails
Condition 5, and always in the same three narrow angular windows — about 25.0°, 28.3°
and 44.2° — where the frozen weights were never asked to cover; the worst cell is an
interior placement at 25.04° (centre ≈ (1.387, 1.343), wall clearances 0.68–1.80) with
mass 96377/100000 = 0.96377, 2.4 % below the threshold, and that value recurs at 720,
1440 and 2880 steps because the same atoms are missed.
Only 3/180, 5/360, 11/720 and 20/1440 of the added directions fail.
At the sharpened largest grid shrink B_sharp(S), every refinement passes, and with the
same flat profile as the retained certificate: every direction’s minimum is exactly
4001/4000 — 361, 721, 1441 and 2881 directions out of as many — so the raise in B
(0.9977 → 0.99885 … 0.99986) lifts the deficient windows back above the tight interior
cells. But choosing B_sharp uses up the whole dilation room: the family bound at L0 is
3.81000003–3.81000038, below T-022’s 3.8100257. So the number that matters per net is
the crossing shrink B_cross(S), the least B at which the finer net passes at L0: the
certified side is then L0·sqrt(1+D_S²)/(B_cross(S)(1+D_S)), and B_cross sits between B0
(fail) and B_sharp (pass).
Part A2 measures it.

**The crossing shrink is 0.99792–0.99798, and it buys +0.0035 (360), +0.0057 (720),
+0.0066 (1440), +0.0071 (2880) in side.** Bisecting B on the 10^-7 grid (Part A2), the
360-net passes at B_pass = 4989621/5000000 = 0.9979242 and fails at 2494809/2500000 =
0.9979236; the binding direction is the 44.21° window (k = 353, mass 12307/12500 =
0.98456 just below the crossing), while the 25° deficiency lifts already by B = 0.99784
and the 28.3° one by 0.99792. The 720-net adds no binding direction (its added
directions’ least is 198931/200000 = 0.994655 at 31.42° for every B tested), so its
crossing is the same to 10^-7: B_pass = 9979243/10^7. The 1440-net’s added directions do
bind: the 28.32° window (k = 877, mass 39001/40000 = 0.975025 for B <= 0.9979803) moves
the crossing up to B_pass = 2494953/2500000 = 0.9979812 (fail at 9979803/10^7), so the
crossing rises slowly with refinement while the containment cap rises faster.
The family bounds are exact surds in T-022’s form (below): 360 steps: 3.813539939
(+0.003514 over T-022); 720 steps: 3.815730319 (+0.005705); 1440 steps: 3.816609503
(+0.006584); 2880 steps: 3.817158227 (+0.007132). The 2880-net’s added directions never
bind either (their least is 100003/100000 at 44.2° down to the 1440 crossing), so
B_pass(2880) = B_pass(1440) = 2494953/2500000; that bisection swept only the 20
directions failing at B0 (12 s per test), because a direction that passes at B0 passes
at every larger B and a coarser net’s directions pass above its own crossing — the
bookkeeping `packing/devtools/measure_net_refinement.py` does for any net.
Each is a genuine certificate of the retained atoms at (L0, B_pass, net) with weights
rescaled by the least mass (the full sweeps at B_pass in the tables give that mass), and
the sharpened dilation then rules out every side below the surd.
So the frozen atoms DO recover most of the shrink tax once the shrink is set at the
crossing rather than at the sharpened limit: the tax at 3.82 is 0.0088; the 1440-net
recovers 0.0066 of it, at the price, in the first (scratch) bisections, of sweeping
every added direction per test (2059 s at 1440 on a loaded host); the knowledge-based
bisection costs seconds.

**Frozen-measure expansion is rigid: it fails after 1.1e-5 in side.** With the walls
moved out by δ and the atoms translated, m(L) stays exactly 4001/4000 up to L* = L0 +
509/46335000 = 3.810010985 and then falls to 0.85353 in one step.
The cause is a single D4 orbit of four heavy atoms (weight 917/6250 = 0.14672 each,
0.587 in total, 5.4 % of M) at (x0, x0) and its images with x0 = 1849127/1853400 = B0 −
5.49e-6: they sit exactly at the far corner of the corner-snug axis core [0, B0]², which
the LP made tight at mass 4001/4000. The moment the walls move by more than 5.49e-6 the
corner core can slide off the orbit and loses 917/6250. Composed with T-022’s dilation
this route yields 3.8100367, a gain of 1.1e-5 over T-022 — worthless.
The retained measure is optimal for its container and nothing else; any expansion needs
the wall-adjacent structure re-solved, not translated.

Composing the expansion with the parent-feasible domains of Part C only moves the cliff
from δ* = 5.49e-6 to 2.46e-5 (L* = 3.810049258, first failure at direction 1, the same
wall orbit; composed side 3.8100750): direction 0’s domain is now inset by 1/2 instead
of B0/2, but direction 1’s parent-feasible inset exceeds its core-fit inset by only
8.7e-6, and the orbit is lost there.

**Parent-feasible centre domains buy nothing on the frozen atoms.** Restricting each
direction’s core centres to the parent unit square’s own wall clearance (a sound
tightening of Condition 5 under the concentric core construction) removes 0.095 % of the
reachable cells and raises no direction’s minimum: the retained certificate has tight
cells (mass exactly 4001/4000) at every direction just inside the restricted domain
(witness clearances 0.0000–0.04 from the new inset), because the LP was solved against
the larger domain and its tight cells hug the corner at every angle.
The tightening could only matter for a certificate optimised against the restricted
domains; on these atoms it is inert.
The “sharp” rational bound for h(α_k) is within 1e-12 of the true value, so the result
is not an artefact of a loose inset.

**What this says about the method’s reach.** The certified side from the retained atoms
is capped by the interplay of two rigidities: the net-direction windows (fixed by
reweighting, which costs mass) and the wall orbit (fixed only by moving sites).
Both are properties of the LP optimum on the 1121 sites, not of the container.

## Timings (one worker, PACK_JOBS=1, 0.25–0.4 s per direction on 1121 atoms)

Part A chain: 180 original 44.0 s (181 dirs); 180 sharp 43.4 s; 360 original 44.7 s (180
added dirs); 360 sharp 88.4 s (361); 720 original 90.3 s (360); 720 sharp 185.3 s (721);
1440 original 182.4 s (720); 1440 sharp 362.4 s (1441); 2880 original 355.5 s (1440);
2880 sharp 910.7 s (2881). Chain total 38 min.
Part B direct: 137 s for all 181 directions (632 exact cell decisions after pruning;
0.23–1.68 s per direction).
Part C: 107 s per bound (two sweeps per direction).
Part A2 and Part D timings are in their tables below.

## What failed or was cut

- The queued driver had to be relaunched twice (a `pkill -f` pattern matched the agent’s
  own shell); no measurement was lost because per-direction minima are logged as JSON
  lines and every script resumes from its log.
- The Part B ladder was cut from ten to four sides (L0 + 1e-4, 2e-4, 5e-4, 1e-3) once
  the direct decision showed L* − L0 = 1.1e-5: all four fail, and the ladder only
  documents the slope beyond the cliff.

## Recommended next measurement

The discriminating number is the covering LP on the frozen 1121 sites at (L0, B0 =
9977/10000, 360-net) — Part D’s second solve.
If its objective is below 11 (it can only be above the retained 10.8637, since the
360-net adds rows), rationalising those weights with the usual margin gives a
certificate at the original shrink on the 360-net, and T-022’s dilation with D_360 then
certifies every side below 38100·sqrt(32400042893309449)/1797926306539 = 3.8143969 — the
shrink-tax recovery the brief asked about — without any new sites.
The same LP at 720/1440/2880 steps (3.8166 / 3.8177 / 3.8182 if feasible below 11) is
the follow-on, at 2–8× the row cost.
If the 360-net LP lands above 11, the deficiency at 25° is a site problem, and the next
step is one round of column generation (`colgen.generate_adaptive`) seeded with the
frozen sites at the 360-net and B0.

## Result tables

## Part A: net refinement on the frozen atoms (L0 = 381/100)

| steps | D (exact) | B_sharp | B_coarse | m at B_sharp | argmin | M/m | sup side at B_sharp | m at B0 = 9977/10000 | argmin | pass at B0 | sup side at B0 if it passed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 180 | 207107/90000000 (0.0023012) | 9977067/10000000 | 124713/125000 | 4001/4000 (1.000250) | 0 | 10.860960 < 11 | 3.8100001378 | 4001/4000 (1.000250) | 0 | PASS | 3.8100257236 |
| 360 | 207107/180000000 (0.0011506) | 9988513/10000000 | 9988507/10000000 | 4001/4000 (1.000250) | 0 | 10.860960 < 11 | 3.8100003398 | 96377/100000 (0.963770) | 193 | FAIL | 3.8143969053 (not certified) |
| 720 | 207107/360000000 (0.0005753) | 9994251/10000000 | 39977/40000 | 4001/4000 (1.000250) | 0 | 10.860960 < 11 | 3.8100003772 | 96377/100000 (0.963770) | 386 | FAIL | 3.8165881607 (not certified) |
| 1440 | 207107/720000000 (0.0002876) | 2499281/2500000 | 2499281/2500000 | 4001/4000 (1.000250) | 0 | 10.860960 < 11 | 3.8100002876 | 96377/100000 (0.963770) | 771 | FAIL | 3.8176852075 (not certified) |
| 2880 | 207107/1440000000 (0.0001438) | 4999281/5000000 | 9998561/10000000 | 4001/4000 (1.000250) | 0 | 10.860960 < 11 | 3.8100000256 | 96377/100000 (0.963770) | 1541 | FAIL | 3.8182340860 (not certified) |

T-022 reference supremum: 3.810025723614703. Threshold M/11 = 434547/440000 = 0.987607.

## Part A2: crossing shrink per net (bisection on B, 10^-7 grid, resolution 10^-6)

| steps | D | B_fail | B_pass | L0/B_pass | dilation supremum at B_pass (exact surd) | float | gain over T-022 | tests | seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 360 | 207107/180000000 | 2494809/2500000 | 4989621/5000000 | 3.8179252 | 6350000*sqrt(32400042893309449)/299721721812149 | 3.8135399386 | +0.0035142 | 11 | 388.3 |
| 720 | 207107/360000000 | 2494809/2500000 | 9979243/10000000 | 3.8179249 | 38100000*sqrt(129600042893309449)/3594594251080001 | 3.8157303194 | +0.0057046 | 11 | 1484.3 |
| 1440 | 207107/720000000 | 9979803/10000000 | 2494953/2500000 | 3.8177072 | 3175000*sqrt(518400042893309449)/598960960743657 | 3.8166095028 | +0.0065838 | 11 | 2059.0 |
| 2880 | 207107/1440000000 | 9979803/10000000 | 2494953/2500000 | 3.8177072 | 3175000*sqrt(2073600042893309449)/1197749680743657 | 3.8171582266 | +0.0071325 | 11 | 101.5 |

Bisection trace S=360: B=0.9982756 PASS (least 0.998640 at k=125, 180/180 dirs, 57.3s);
B=0.9979878 PASS (least 0.998640 at k=125, 180/180 dirs, 57.1s); B=0.9978439 FAIL (least
0.975025 at k=219, 110/180 dirs, 36.1s); B=0.9979158 FAIL (least 0.984560 at k=353,
177/180 dirs, 56.4s); B=0.9979518 PASS (least 0.998640 at k=125, 180/180 dirs, 49.0s);
B=0.9979338 PASS (least 0.998640 at k=125, 180/180 dirs, 45.1s); B=0.9979248 PASS (least
0.998640 at k=125, 180/180 dirs, 42.9s); B=0.9979203 FAIL (least 0.984560 at k=353,
1/180 dirs, 0.2s); B=0.9979225 FAIL (least 0.984560 at k=353, 1/180 dirs, 0.3s);
B=0.9979236 FAIL (least 0.984560 at k=353, 1/180 dirs, 0.2s); B=0.9979242 PASS (least
0.998640 at k=125, 180/180 dirs, 43.7s)

Bisection trace S=720: B=0.9986743 PASS (least 1.000250 at k=1, 360/360 dirs, 86.9s);
B=0.9982989 PASS (least 1.000250 at k=1, 360/360 dirs, 87.1s); B=0.9981112 PASS (least
0.994655 at k=489, 360/360 dirs, 114.0s); B=0.9980174 PASS (least 0.994655 at k=489,
360/360 dirs, 96.5s); B=0.9979705 PASS (least 0.994655 at k=489, 360/360 dirs, 95.9s);
B=0.9979470 PASS (least 0.994655 at k=489, 360/360 dirs, 465.2s); B=0.9979353 PASS
(least 0.994655 at k=489, 360/360 dirs, 107.9s); B=0.9979294 PASS (least 0.994655 at
k=489, 360/360 dirs, 106.7s); B=0.9979265 PASS (least 0.994655 at k=489, 360/360 dirs,
97.0s); B=0.9979250 PASS (least 0.994655 at k=489, 360/360 dirs, 111.2s); B=0.9979243
PASS (least 0.994655 at k=489, 360/360 dirs, 115.6s)

Bisection trace S=1440: B=0.9988180 PASS (least 1.000250 at k=1, 720/720 dirs, 190.9s);
B=0.9983708 PASS (least 0.998640 at k=501, 720/720 dirs, 187.0s); B=0.9981472 PASS
(least 0.998640 at k=501, 720/720 dirs, 190.9s); B=0.9980354 PASS (least 0.998640 at
k=499, 720/720 dirs, 244.8s); B=0.9979795 FAIL (least 0.975025 at k=877, 439/720 dirs,
152.8s); B=0.9980074 PASS (least 0.998640 at k=499, 720/720 dirs, 265.6s); B=0.9979934
PASS (least 0.994655 at k=979, 720/720 dirs, 263.1s); B=0.9979864 PASS (least 0.994655
at k=979, 720/720 dirs, 194.2s); B=0.9979829 PASS (least 0.994655 at k=979, 720/720
dirs, 193.9s); B=0.9979812 PASS (least 0.994655 at k=979, 720/720 dirs, 175.3s);
B=0.9979803 FAIL (least 0.975025 at k=877, 1/720 dirs, 0.2s)

Bisection trace S=2880: B=0.9989182 PASS (least 1.000250 at k=1537, 20/20 dirs, 11.5s);
B=0.9984492 PASS (least 1.000250 at k=1537, 20/20 dirs, 6.8s); B=0.9982147 PASS (least
1.000250 at k=1537, 20/20 dirs, 7.7s); B=0.9980975 PASS (least 1.000030 at k=2825, 20/20
dirs, 7.3s); B=0.9980389 PASS (least 1.000030 at k=2825, 20/20 dirs, 7.5s); B=0.9980096
PASS (least 1.000030 at k=2825, 20/20 dirs, 6.1s); B=0.9979949 PASS (least 1.000030 at
k=2825, 20/20 dirs, 5.9s); B=0.9979876 PASS (least 1.000030 at k=2825, 20/20 dirs,
7.9s); B=0.9979839 PASS (least 1.000030 at k=2825, 20/20 dirs, 14.0s); B=0.9979821 PASS
(least 1.000030 at k=2825, 20/20 dirs, 13.8s); B=0.9979812 PASS (least 1.000030 at
k=2825, 20/20 dirs, 12.6s)

Full sweep at S=360, B=4989621/5000000: least 12483/12500 (0.998640) at k=125, M/m =
10.878470, 117.8s. Full sweep at S=720, B=9979243/10000000: least 198931/200000
(0.994655) at k=489, M/m = 10.922053, 189.8s.

## Part B: frozen-measure expansion (B = 9977/10000, 181 directions)

[`lane-a-part_b_direct.json`](lane-a-part_b_direct.json) (library-inset): delta* =
509/92670000 = 5.492608e-06; L* = 176536859/46335000 = 3.810010985; first bad cell at
direction 0, cell [56, 475], mass 85353/100000 (0.853530); composed dilation supremum
3.8100367089 (+1.099e-05 vs T-022); 137.4s.

| reachable for L > | L (float) | m(L) drops to | passes | direction | cell |
| --- | --- | --- | --- | --- | --- |
| 176536859/46335000 | 3.810010985 | 85353/100000 (0.853530) | NO | 0 | [56, 475] |

`part_b_direct-sharp.json` (sharp; not retained (scratch only)): delta* =
37144754196134068716494282188885180715002831/1508157384795156922223001171008162982910163940000
= 2.462923e-05; L* =
2873076962788970070903533725052739367624577308531/754078692397578461111500585504081491455081970000
= 3.810049258; first bad cell at direction 1, cell [210, 318], mass 85353/100000
(0.853530); composed dilation supremum 3.8100749824 (+4.926e-05 vs T-022); 110.8s.

| reachable for L > | L (float) | m(L) drops to | passes | direction | cell |
| --- | --- | --- | --- | --- | --- |
| 2873076962788970070903533725052739367624577308531/754078692397578461111500585504081491455081970000 | 3.810049258 | 85353/100000 (0.853530) | NO | 1 | [210, 318] |

`part_b_direct-coarse.json`: (pending) — not produced, not retained (scratch only).
Library sweeps (threshold):

| L | L (float) | least reachable mass | argmin direction | passes | all 181 swept | seconds |
| --- | --- | --- | --- | --- | --- | --- |
| 176536859/46335000 | 3.810010985 | 4001/4000 (1.000250) | 0 | yes | True | 54.8 |
| 3530737189267/926700000000 | 3.810010995 | 85353/100000 (0.853530) | 0 | NO | True | 57.2 |

Library sweeps (ladder):

| L | L (float) | least reachable mass | argmin direction | passes | all 181 swept | seconds |
| --- | --- | --- | --- | --- | --- | --- |
| 38101/10000 | 3.810100000 | 85353/100000 (0.853530) | 0 | NO | True | 55.2 |
| 19051/5000 | 3.810200000 | 85353/100000 (0.853530) | 0 | NO | True | 62.4 |
| 7621/2000 | 3.810500000 | 85353/100000 (0.853530) | 0 | NO | True | 60.0 |
| 3811/1000 | 3.811000000 | 39319/50000 (0.786380) | 0 | NO | True | 59.5 |

## Part C: parent-feasible centre domains (L0, B0, 181 directions)

bound=sharp: least mass control 4001/4000 -> parent-feasible 4001/4000 (1.000250);
reachable cells 567130649 -> 566589601 (541048 disappear, 0.10%); directions whose
minimum rose: 0 of 181; 106.7s. Five lowest per-direction minima with parent-feasible
domains: k=0: 4001/4000 (1.000250); k=1: 4001/4000 (1.000250); k=2: 4001/4000
(1.000250); k=3: 4001/4000 (1.000250); k=4: 4001/4000 (1.000250)

bound=coarse: least mass control 4001/4000 -> parent-feasible 4001/4000 (1.000250);
reachable cells 567130649 -> 566823745 (306904 disappear, 0.05%); directions whose
minimum rose: 0 of 181; 98.0s. Five lowest per-direction minima with parent-feasible
domains: k=0: 4001/4000 (1.000250); k=1: 4001/4000 (1.000250); k=2: 4001/4000
(1.000250); k=3: 4001/4000 (1.000250); k=4: 4001/4000 (1.000250)

## Part D: fixed-site LP re-optimisation (float, CHECKED, not a bound)

The delivered report stops at this heading: the three Part D solves finished after it
was written. Their receipts are retained, and this table is the retaining agent’s, every
field copied from them.

| receipt | steps | B | objective (float LP) | stopped | rounds | rows | support orbits | s |
| --- | ---: | --- | ---: | --- | ---: | ---: | ---: | ---: |
| [`lane-a-part_d_lp-S180-B9977000.json`](lane-a-part_d_lp-S180-B9977000.json) | 180 | `9977/10000` | 10.860299456291461 | converged: every placement covers mass 1 | 37 | 2208 | 113 | 368.3 |
| [`lane-a-part_d_lp-S360-B9977000.json`](lane-a-part_d_lp-S360-B9977000.json) | 360 | `9977/10000` | 10.874446085672329 | converged: every placement covers mass 1 | 37 | 2863 | 100 | 531.0 |
| [`lane-a-part_d_lp-S360-B9988513.json`](lane-a-part_d_lp-S360-B9988513.json) | 360 | `9988513/10000000` | 10.708668941979518 | converged: every placement covers mass 1 | 27 | 2771 | 72 | 327.3 |

All three are the covering LP on the frozen 1121 sites (149 D4 orbits) at `L = 381/100`,
each stopping with `least_covered_at_end` within `1e-12` of 1, against the retained
total mass `434547/40000 = 10.863675`. Float LP values, CHECKED, not bounds; the
per-round row, violation and timing logs are in the receipts.

## Files

Retained beside this report, in this directory:

- Part A2, one crossing-shrink receipt per net:
  [`lane-a-part_a2-S360.json`](lane-a-part_a2-S360.json) (3,340 B),
  [`lane-a-part_a2-S720.json`](lane-a-part_a2-S720.json) (3,373 B),
  [`lane-a-part_a2-S1440.json`](lane-a-part_a2-S1440.json) (3,363 B),
  [`lane-a-part_a2-S2880.json`](lane-a-part_a2-S2880.json) (3,598 B). Each carries
  `steps`, `D`, `B_fail`, `B_pass`, the unit-equivalent side `L0/B_pass`, the exact
  `dilation_supremum_squared` with its float, the eleven bisection tests with their
  least mass, argmin and seconds, and the total seconds.
- Part B: [`lane-a-part_b_direct.json`](lane-a-part_b_direct.json) (43,716 B), the
  library-inset expansion — `delta_star`, `L_star`, the first bad direction, cell and
  mass, the composed dilation supremum as an exact square, the step function, and all
  181 per-direction rows.
- Part C: [`lane-a-part_c-sharp.json`](lane-a-part_c-sharp.json) (150,310 B) and
  [`lane-a-part_c-coarse.json`](lane-a-part_c-coarse.json) (128,702 B) — control and
  parent-feasible least mass, both reachable-cell counts, and one row per direction with
  both insets, the inset gain and both minima.
- Part D: the three receipts tabulated above (7,800 B, 7,829 B, 5,827 B).

Not retained (scratch only):

- The 51 per-direction sweep logs `dirmin-*.jsonl`, 6.4 MB in total: 181 B to 831,284 B
  each, twelve of them 200 KB or more, the largest `dirmin-S2880-sharp.jsonl` at 831,284
  B and `dirmin-S2880-original.jsonl` at 410,765 B. One JSON line per direction — the
  index `k`, its exact half-tangent `t`, the exact least reachable mass `min`, the exact
  rational witness centre `witness_uv` in the rotated frame, and the seconds.
  They are the resume logs each script restarts from and the source of the per-direction
  numbers quoted above; no table above needs them.
- The twelve Part A summaries `part_a-*.json` (about 1.1 KB each), whose contents are
  the Part A table in full.
- The other Part B files: `part_b_direct-sharp.json` (49,936 B, its numbers quoted in
  Part B above), `part_b_direct-S360-B9979242.json` (89,026 B),
  `part_b_direct-S360-B9988513.json` (88,841 B), `part_b_direct-partial.json` (1,421 B),
  and the library-sweep summaries `part_b_sweeps-threshold.json` (754 B) and
  `part_b_sweeps-ladder.json` (1,414 B), which are the two sweep tables above.
  `part_b_direct-coarse.json` was never produced.
- Scripts and driver logs: `common.py`, `part_a.py`, `part_a2.py`, `part_a2_fast.py`,
  `part_b_sweeps.py`, `part_c.py`, `part_d_lp.py`, `expand_frozen.py`, `inset_sweep.py`,
  `summarize.py`, `time_one.py`, `write_report.py`, the `run_*.sh` drivers,
  `part_a.log`, `run_rest.log` (51,268 B), `run_tail.log` (76,131 B), and the draft
  `narrative.md`. The net-refinement bookkeeping the bisections used is committed as
  `packing/devtools/measure_net_refinement.py`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
