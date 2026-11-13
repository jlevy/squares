# n = 157

157 unit squares in a square of side

    12.99330261134322364133727935496577166311874424252458...

The Squares Project listed 13 for n = 157 on 11 November 2026, the side of the 13 x 13 grid. This packing has a side below 13. The improvement is 0.0067.

## Construction

The packing is a pinwheel: a central block of tilted squares with four arms, surrounded by four blocks of axis-aligned squares. It holds 61 tilted squares, with four distinct tilt angles between 24.0 and 27.6 degrees, and 96 axis-aligned squares.

It was derived in two steps from the public packing of 109 unit squares in the repository `Samanyu-dev/squares_in_squares` (commit `53551d7`, file `best_fit_101_500.csv`, side 10.949289581). The README of that repository reports this packing as a result of its own stretch and quench chains. Each step cuts the packing along one horizontal and one vertical line, moves the parts about one unit apart, fills each gap with one layer of squares that continues the local lattice, and re-optimizes all squares. The first step gives the packing of 132 squares in [n132](../n132/). The second step gives this packing.

Credit for the pinwheel arrangement at n = 109 belongs to Samanyu-dev.

## Local optimum

All squares were optimized together with an interior-point solver (IPOPT). The contact equations of the result were then solved to 250 digits. All 2024 contact equations (a corner of one square on the edge line of another square, or a corner on a wall) are satisfied to 1e-247, and all other gaps stay open. The side in the rational certificate is 1.4e-59 above this solution.

Non-negative contact forces in balance exist, which is the first-order condition for a local minimum (checked in floating point). In 297 perturbation trials (random noise, local kicks, small rotations of a region, shifts along a cut line), each followed by re-optimization, no smaller side came up.

The certificate proves the upper bound s(157) <= side. The local optimality statement rests on the numerical solution described above and has no formal proof. A search for a minimal polynomial of the side up to degree 16 found none.

The Kaggle competition "Squares in Squares" has a per-puzzle leaderboard that lists sides without packings. I have not seen its values for n = 157, so an unpublished packing with a smaller side may exist.

## Files

- `n157_exact.json`: exact rational coordinates (centre and unit edge direction of each square) and the side.
- `n157_witness.yaml`: the same packing as a Squares Project witness file (Witness/v2, center-basis, rational).
- `n157_record.png`: figure. Tilted squares are yellow.
- `verify_exact.py`: exact checker. Run `python3 -B verify_exact.py` (Python 3.10 or later, standard library only).
- `SHA256SUMS`: checksums of the files above.

The code that produced this packing is in [method_n132_n157](../method_n132_n157/).

## Method and AI assistance

The derivation, optimization, high-precision solution, rational certificate, checking and figure were produced with Claude Fable 5.2 (Anthropic) under the direction of Joost de Winter.
