# Packings above n = 324

Fifteen packings of n unit squares in a square, each with a smaller side than the best value recorded by the Squares Project for that n on 9 November 2026 (repository `jlevy/squares` at commit 200f2eb, all registered claims and their monotonicity and border consequences).

| n | Side, rounded up | Best recorded value | Improvement | Origin |
| ---: | ---: | ---: | ---: | :--- |
| 413 | 20.8239520077 | 20.8247640387 | 0.000812 | sub-window of the n = 544 packing, re-optimized |
| 494 | 22.7365988643 | 22.7375328752 | 0.000934 | sub-window of the n = 539 packing, re-optimized |
| 539 | 23.7365988643 | 23.7366696738 | 0.000071 | n = 494 plus a border of 45 squares |
| 543 | 23.8024287170 | 23.8030532611 | 0.000625 | sub-window of the n = 590 packing, re-optimized |
| 547 | 23.8787301198 | 23.8791276533 | 0.000398 | sub-window of the n = 696 packing |
| 590 | 24.8024287170 | 24.8025271329 | 0.000098 | n = 543 plus a border of 47 squares |
| 738 | 27.6912062515 | 27.6912836295 | 0.000077 | sub-window of the n = 851 packing, re-optimized |
| 739 | 27.6912835939 | 27.6914502721 | 0.000167 | sub-window of the n = 851 packing, re-optimized |
| 753 | 27.9026514302 | 27.9079842304 | 0.005333 | sub-window of the n = 810 packing above, re-optimized |
| 794 | 28.6912835939 | 28.6914489810 | 0.000165 | n = 739 plus a border of 55 squares |
| 809 | 28.9079170470 | 28.9080360986 | 0.000119 | n = 810 with one square removed |
| 810 | 28.9079170470 | 28.9104510455 | 0.002534 | sub-window of the n = 868 packing, re-optimized |
| 851 | 29.6912835939 | 29.6914489756 | 0.000165 | n = 794 plus a border of 57 squares |
| 867 | 29.9079170470 | 29.9080360977 | 0.000119 | n = 810 plus a border of 57 squares |
| 910 | 30.6912835939 | 30.6914489756 | 0.000165 | n = 851 plus a border of 59 squares |

## Construction

The source packings for n = 544, 539, 590, 696, 851 and 868 are by Francisco Couzo (Squares Project issue #763 and `franciscouzo/square-packing` at commit 43f666c). A square sub-window of each source packing contains more squares than the best recorded packing of the same side. The squares inside the sub-window were then re-optimized locally.

For n = 413, 543 and 547 the optimality conditions were solved to 65 digits, and the side of the certificate is less than 1e-43 above the local optimum of the arrangement. For n = 494, 738, 739, 753 and 810 the certificate carries a margin of about 5e-9 above the numerical optimum. The packing for n = 753 is a sub-window of the n = 810 packing. The remaining packings follow by adding a border of axis-aligned squares or by removing one square.

The certificates prove the upper bounds. The local optimality statements rest on numerical solutions and have no formal proof.

## Files

- `nNNNN.cert`: exact rational certificate. First data line: n and the side. Then one line per square: centre x, centre y, and t = tan(theta/2) for the rotation angle theta.
- `nNNNN.png`: figures for n = 413, 494, 543, 547, 753 and 810. Tilted squares are yellow.
- `verify_cert.py`: exact checker (containment and pairwise disjoint interiors, rational arithmetic). Run `python3 -B verify_cert.py` (Python 3.10 or later, standard library only).

## Method and AI assistance

The sub-window search, local optimization, high-precision solution, rational certificates, checking and figures were produced with Claude (Anthropic) under the direction of Joost de Winter.
