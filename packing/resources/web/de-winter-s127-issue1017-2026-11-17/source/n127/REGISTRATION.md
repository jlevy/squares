# Lowered upper bound for n = 127 (side 11.800795682214): registration request

This file follows the result registration template of the Squares Project (`.github/ISSUE_TEMPLATE/result-registration.md` in jlevy/squares).

**Credit name.** Joost de Winter, Delft University of Technology.

**Claim.** A packing of 127 unit squares in a square of side 11.800795682214 (rounded up at 12 places). The exact rational side is in `n127/n127_exact.json`. The case page https://squaremath.org/cases/127.html lists 11.8017538904864874 (T-305, Tomáš Kodaj, improved by JoeGun) on 17 November 2026. The gain is 0.00096.

**Certificate.** Exact rational coordinates of all 127 squares and the side, in the folder `n127` of https://github.com/JoostdeWinter/square-packing.

- `n127/n127_exact.json` (centre and unit edge direction of each square)
- `n127/n127_witness.yaml` (the same packing as a Witness/v2 file, corners, rational)

A figure of the packing is in `n127/n127_record.png`.

**Checking.**

1. `n127/verify_exact.py`. Arithmetic: Python `fractions.Fraction`. It checks that every edge direction is a unit vector, that every square lies in the container, and that every pair of squares with centres closer than sqrt(2) is separated along an edge direction of one of the two squares. It reports 127 squares and 311 close pairs. Command: `python3 -B verify_exact.py` in the folder `n127`. Cost: about 1 second on one core.
2. `n127/check_area.py`. Arithmetic: Python `fractions.Fraction`. It clips one square of each close pair against the other and requires an intersection of area exactly 0. It reports 127 squares and 311 close pairs. Command: `python3 -B check_area.py` in the folder `n127`. Cost: about 1 second on one core.

**What the checkers share.** The two scripts have one author, use Python's `Fraction` type and read the same input file. They share no code. The first uses a separating-axis test and the second uses the area of the clipped intersection. The witness file has not yet been run through the project's own checker.

**Not done.** No test of local optimality was run, and a proof of optimality is missing. On the Kaggle per-puzzle leaderboard of "Squares in Squares", Luka Cvetkovic reported 11.800793726618 for n = 127 (16 November 2026), 0.0000020 below this packing. His coordinates were not found.

**Lineage and credit.** The search started from an exact certificate of an arrangement in the public Kaggle coordinate compilations of Alex Chilton and Asterios Panoras. Its original finder could not be established. The search changed the sliding offsets of the columns in the tilted central band and then optimized the positions and angles of individual squares. Please credit the new bound to Joost de Winter, after the arrangement in the Chilton and Panoras compilations.

**AI assistance.** The search, optimization and rational certificate were produced with GPT-6.2 Sol (OpenAI). The repository files, checks and figure were produced with Claude (Anthropic). Both worked under my direction.
