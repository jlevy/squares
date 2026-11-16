# Lowered upper bound for n = 90 (side 9.994038766610): registration request

This file follows the result registration template of the Squares Project (`.github/ISSUE_TEMPLATE/result-registration.md` in jlevy/squares).

**Credit name.** Joost de Winter, Delft University of Technology.

**Claim.** A packing of 90 unit squares in a square of side 9.994038766610 (rounded up at 12 places). The exact rational side is 99940387666098521323/10000000000000000000. The record holds 9.998277166926 for n = 90 (T-303) at commit 91acf2022a69531da3421889810a3bc53aa89753 of jlevy/squares. The gain is 0.00424.

**Certificate.** Exact rational coordinates of all 90 squares and the side, in the folder `n90` of https://github.com/JoostdeWinter/square-packing at commit 64d5ee762a1159248d375973fb33825d51da637d. Later commits leave these files unchanged.

- `n90/n90_exact.json` (centre and unit edge direction of each square)
- `n90/n90_witness.yaml` (the same packing as a Witness/v2 file, corners, rational)

A figure of T-303 and the new packing side by side is in `n90/n90_before_after.png`.

**Checking.**

1. `n90/verify_exact.py`. Arithmetic: Python `fractions.Fraction`. It checks that every edge direction is a unit vector, that every square lies in the container, and that every pair of squares with centres closer than sqrt(2) is separated along an edge direction of one of the two squares. It reports 90 squares and 199 close pairs. Command: `python3 -B verify_exact.py` in the folder `n90`. Cost: less than 1 second on one core.
2. `n90/check_area.py`. Arithmetic: Python `fractions.Fraction`. It clips one square of each close pair against the other and requires an intersection of area exactly 0. It reports 90 squares and 199 close pairs. Command: `python3 -B check_area.py` in the folder `n90`. Cost: less than 1 second on one core.
3. `packing/devtools/check_rational_witness_independent.py` of jlevy/squares at commit ed7aff6506190a618e4a66b5895b6ef023df2ec3, run on `n90/n90_witness.yaml`. It reports "VERIFIED: 90 squares, 4005 pairs". Cost: about 1 second on one core.
4. The witness file validates against `packing/witnesses/witness.schema.yaml` of jlevy/squares at the commit named under Claim (jsonschema, 0 errors).

**What the checkers share.** The first two scripts have one author, use Python's `Fraction` type and read the same input file. They share no code. The first uses a separating-axis test and the second uses the area of the clipped intersection. The third checker is the project's own and reads the corners in the witness file.

**Not done.** The statement that the packing is a local optimum of its arrangement rests on numerical work: a linear program over all 90 squares, with every contact linearized, found no first-order improvement larger than 4e-10. That test covers one set of contacts: an earlier packing of this arrangement passed it at a side 9e-8 larger. The certificate keeps a smallest gap of 2e-12 between squares, so an exact solution of the contact equations would be smaller by an amount of that order. A proof of local or global optimality is missing. The best sides on the Kaggle leaderboard of "Squares in Squares" were not available to me. A public merged submission (bestbryant/claude_code_squaresinsquares, 15 November 2026) lists 9.998277166917 for n = 90.

**Lineage and credit.** The packing starts from T-303 by jazivxt (issue #989), which is built from a crop of my packing for n = 157 (T-293). A local search changed small groups of squares in position and angle, optimized the packing again after each change, and kept the changes that gave a smaller side. T-303 has 44 leaning squares and the new packing has 40. Four squares in the upper left of the cluster are axis-aligned, four squares at the top of the cluster have a new angle, and one axis-aligned square at the top wall lies 0.32 lower. Please credit the new bound to Joost de Winter, as an improvement of jazivxt's packing.

**AI assistance.** The local search that found the arrangement was run with GPT-6.1 Sol Max (OpenAI). The local optimization, rational certificate, checks and figures were produced with Claude Fable 5.2 (Anthropic). Both worked under my direction.
