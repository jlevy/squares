# n = 132

132 unit squares in a square of side

    11.97604838360340752372871695271367782454646197183552...

The Squares Project listed 11.9856801988458088 for n = 132 on 11 November 2026. The improvement is 0.0096.

## Construction

The packing is a pinwheel: a central block of tilted squares with four arms, surrounded by four blocks of axis-aligned squares. It holds 54 tilted squares and 78 axis-aligned squares.

It was derived from the public packing of 109 unit squares in the repository `Samanyu-dev/squares_in_squares` (commit `53551d7`, file `best_fit_101_500.csv`, side 10.949289581). The README of that repository reports this packing as a result of its own stretch and quench chains. The packing of 109 squares was cut along one horizontal and one vertical line. The parts were moved about one unit apart, each gap was filled with one layer of squares that continues the local lattice, and all squares were re-optimized. The same step applied to this packing gives the packing of 157 squares in [n157](../n157/).

Credit for the pinwheel arrangement at n = 109 belongs to Samanyu-dev.

## Local optimum

All squares were optimized together with an interior-point solver (IPOPT). The contact equations of the result were then solved to 250 digits. All 1407 contact equations (a corner of one square on the edge line of another square, or a corner on a wall) are satisfied to 1e-269, and all other gaps stay open. The side in the rational certificate is 1.3e-59 above this solution.

Non-negative contact forces in balance exist, which is the first-order condition for a local minimum (checked in floating point). In 324 perturbation trials (random noise, local kicks, small rotations of a region, shifts along a cut line), each followed by re-optimization, no smaller side came up.

The certificate proves the upper bound s(132) <= side. The local optimality statement rests on the numerical solution described above and has no formal proof. A search for a minimal polynomial of the side up to degree 16 found none.

The Kaggle competition "Squares in Squares" has a per-puzzle leaderboard that lists sides without packings. I have not seen its values for n = 132, so an unpublished packing with a smaller side may exist.

## Files

- `n132_exact.json`: exact rational coordinates (centre and unit edge direction of each square) and the side.
- `n132_witness.yaml`: the same packing in the Squares Project witness format (center-basis, rational).
- `n132_record.png`: figure. Tilted squares are yellow.
- `verify_exact.py`: exact checker. Run `python3 -B verify_exact.py` (Python 3.10 or later, standard library only).
- `SHA256SUMS`: checksums of the files above.

## Method and AI assistance

The derivation, optimization, high-precision solution, rational certificate, checking and figure were produced with Claude Fable 5.2 (Anthropic) under the direction of Joost de Winter.
