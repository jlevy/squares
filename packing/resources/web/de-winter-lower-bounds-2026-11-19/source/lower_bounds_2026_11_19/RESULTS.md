The newest results, their comparisons and the reproduction commands are in [FOLLOWUP.md](FOLLOWUP.md).

# New square-packing bounds

34 square counts have a directly checked lower-bound improvement. Another 67 counts have improvements using the new corner certificates together with Hosono’s reported global measure theorem. All counts are below 325.

For a lower bound, the gain is the increase in the side of a board ruled out by the proof. Each comparison uses the strongest tracked result for that count, including prior work from the author and submitted results. The remaining uncertainty extends up to the smallest known feasible packing.

| Squares | Previous lower bound, approximately | New exact lower bound | Gain, approximately | Angle intervals | Center boxes |
|---:|---:|---:|---:|---:|---:|
| 114 | 10.80780161069670 | 10.875 | 0.0671983893033 | 100 | 1,406,930 |
| 115 | 10.85495712297924 | 10.875 | 0.0200428770208 | 118 | 1,264,020 |
| 104 | 10.41309367660438 | 10.432 | 0.0189063233956 | 345 | 3,492,779 |
| 113 | 10.79394788114092 | 10.808 | 0.0140521188591 | 272 | 7,002,408 |
| 111 | 10.77464646918138 | 10.781 | 0.00635353081862 | 423 | 11,248,217 |
| 135 | 11.74120722152421 | 11.747 | 0.00579277847579 | 165 | 3,899,839 |
| 109 | 10.69746605003148 | 10.703 | 0.00553394996852 | 235 | 4,615,833 |
| 130 | 11.48554056065651 | 11.491 | 0.00545943934349 | 124 | 1,644,548 |
| 131 | 11.54554473518858 | 11.551 | 0.00545526481142 | 134 | 1,716,536 |
| 134 | 11.68956528352290 | 11.695 | 0.00543471647710 | 133 | 2,012,005 |
| 137 | 11.81885066559402 | 11.824 | 0.00514933440598 | 149 | 3,467,181 |
| 105 | 10.49501029781419 | 10.499 | 0.00398970218581 | 273 | 5,340,305 |
| 87 | 9.58500287601162 | 9.5888 | 0.00379712398838 | 198 | 2,994,014 |
| 89 | 9.69000291297027 | 9.6937 | 0.00369708702973 | 208 | 3,560,832 |
| 73 | 8.82583799228449 | 8.829 | 0.00316200771551 | 269 | 5,026,063 |
| 69 | 8.63284153494131 | 8.636 | 0.00315846505869 | 463 | 8,396,247 |
| 50 | 7.41186394729352 | 7.415 | 0.00313605270648 | 447 | 11,166,243 |
| 58 | 7.93658476814316 | 7.9394 | 0.00281523185684 | 191 | 2,199,781 |
| 74 | 8.87250400699637 | 8.8752 | 0.00269599300363 | 191 | 2,346,357 |
| 75 | 8.94501150659235 | 8.94752 | 0.00250849340765 | 230 | 3,543,870 |
| 65 | 8.35500372896728 | 8.35751 | 0.00250627103272 | 184 | 3,067,870 |
| 52 | 7.55600000000000 | 7.558 | 0.002 | 198 | 2,602,114 |
| 103 | 10.30500000000000 | 10.307 | 0.002 | 171 | 2,132,165 |
| 107 | 10.59500190726287 | 10.597 | 0.00199809273713 | 244 | 7,773,120 |
| 71 | 8.72600392828862 | 8.7277 | 0.00169607171138 | 212 | 2,979,746 |
| 68 | 8.53912441869444 | 8.5408 | 0.00167558130556 | 214 | 3,925,534 |
| 70 | 8.67034084660125 | 8.672 | 0.00165915339875 | 252 | 5,118,956 |
| 57 | 7.87550000000000 | 7.8771 | 0.0016 | 191 | 2,359,577 |
| 72 | 8.77283896513843 | 8.774 | 0.00116103486157 | 234 | 3,074,976 |
| 67 | 8.49284410474418 | 8.494 | 0.00115589525582 | 242 | 4,031,362 |
| 88 | 9.64302131607013 | 9.6439 | 0.000878683929867 | 212 | 4,040,816 |
| 85 | 9.48532175930218 | 9.4862 | 0.000878240697823 | 206 | 4,094,996 |
| 93 | 9.88203596221721 | 9.8829 | 0.000864037782786 | 185 | 2,262,113 |
| 54 | 7.68652677404624 | 7.68693 | 0.000403225953758 | 146 | 1,400,078 |

## The 114-square construction

A first construction takes the measure for 73 squares on a board of side 8.826 and repeats its middle unit strip on each axis to reach side 10.826. Every unit square captures at least one unit from a total of 113.999999. The pigeonhole principle therefore excludes 114 disjoint square interiors. This uses the fact that the rectangle measure assigns zero mass to boundaries. The diagram and original proof for this construction are in the constructions directory.

The certificate at side 10.875 combines measures drawn from counts 92, 93, 74, with integer weights 9184590 : 73911664 : 16903746. The packet reconstructs each part from its rational inputs. The continuous coverage proof considered 1,406,930 center boxes in 100 angle intervals.

The winning density and a slice through the space of possible unit-square centers appear in constructions/n114-coverage.png. The color map samples an orientation of 15 degrees. The proof covers the continuous range of orientations.

## Smaller packings

For 260 squares the enclosed placement fits side 16.633520939839750616277829 (rounded upward). Its exact side is approximately 1.56637624985e-15 smaller than the strongest tracked earlier upper certificate. The 260-square layout comes from the earlier de Winter certificate after prvsiyan, Daniel and Polkovskyi. Three exact geometric predicates check every pair.

Any additional refinement smaller than 10⁻²⁰ appears in upper/precision_only.csv. Exact sides, comparison quantities, coordinate witnesses, credits and geometry audits are in upper/cases.

## Family-dependent improvements

The corner computations improve 71 counts altogether, with 67 additional to the direct table. The packet replays each new corner check. It takes the global coverage of the unchanged Hosono measures from T-180. The upstream authors report a full replay of 187,183,108 leaves. This search did not repeat that full computation.

## Reproduction

Run `python3 verify.py` from the extracted directory to check all input hashes, interval coverage, case comparisons, upper-bound witnesses and new local corner modifications. Run `python3 verify.py --replay --workers 4` to repeat all direct center subdivisions. A single count can be selected with `--n 114`. The full checker uses Python 3.10 or newer and a C++17 compiler.

The search started on November 19, 2026 at 04:57:40 UTC. The comparison registry and issue links appear in the case files. The certificates were prepared locally for review.

- https://squaremath.org/cases/114.html
- https://squaremath.org/result/t-180.html
- https://github.com/jlevy/squares/issues/1039
- https://squaremath.org/cases/260.html

The four-hour search window ended at 08:57:40 UTC.
