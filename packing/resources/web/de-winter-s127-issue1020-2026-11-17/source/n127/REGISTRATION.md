# Lowered upper bound for n = 127 (side 11.800793726616): registration request

This file follows the result registration template of the Squares Project (`.github/ISSUE_TEMPLATE/result-registration.md` in jlevy/squares).

**Credit name.** Joost de Winter, Delft University of Technology.

**Claim.** A packing of 127 unit squares in a square of side exactly 5900396863307571/500000000000000 = 11.800793726615142. The case page https://squaremath.org/cases/127.html lists 11.8017538904864874 (T-305, Tomáš Kodaj, improved by JoeGun) on 17 November 2026. The gain is 0.00096.

**Certificate.** Exact rational coordinates of all 127 squares and the side, in the folder `n127` of https://github.com/JoostdeWinter/square-packing at commit cc20a26845789c2502950041c26709eda8a71081. Later commits leave these files unchanged.

- `n127/n127_exact.json` (centre and unit edge direction of each square)
- `n127/n127_witness.yaml` (the same packing as a Witness/v2 file, corners, rational)

A figure of the packing is in `n127/n127_record.png`.

**Checking.**

1. `n127/verify_exact.py`. Arithmetic: Python `fractions.Fraction`. It checks that every edge direction is a unit vector, that every square lies in the container, and that every pair of squares with centres closer than sqrt(2) is separated along an edge direction of one of the two squares. It reports 127 squares and 312 close pairs. Command: `python3 -B verify_exact.py` in the folder `n127`. Cost: about 1 second on one core.
2. `n127/check_area.py`. Arithmetic: Python `fractions.Fraction`. It clips one square of each close pair against the other and requires an intersection of area exactly 0. It reports 127 squares and 312 close pairs. Command: `python3 -B check_area.py` in the folder `n127`. Cost: about 1 second on one core.

**What the checkers share.** The two scripts have one author, use Python's `Fraction` type and read the same input file. They share no code. The first uses a separating-axis test and the second uses the area of the clipped intersection. The witness file has not yet been run through the project's own checker.

**Not done.** No test of local optimality was run, and a proof of optimality is missing. On the Kaggle per-puzzle leaderboard of "Squares in Squares", Luka Cvetkovic reported 11.800793726617185 for n = 127 (16 November 2026). This packing is 2.04e-12 below that value, so the two packings are probably the same local optimum. His coordinates were not found.

**Lineage and credit.** The search started from an exact certificate of an arrangement in the public Kaggle coordinate compilations of Alex Chilton and Asterios Panoras. Its original finder could not be established. The search changed the sliding offsets of the columns in the tilted central band and optimized the positions and angles of individual squares. A second stage repeatedly changed the aspect ratio of the enclosing rectangle while moving and rotating squares, and then returned to a square, which shifted the tilted cap at the top of the band. Please credit the new bound to Joost de Winter, after the arrangement in the Chilton and Panoras compilations.

**AI assistance.** The search, optimization and rational certificate were produced with GPT-6.2 Sol (OpenAI). The repository files, checks and figure were produced with Claude (Anthropic). Both worked under my direction.
