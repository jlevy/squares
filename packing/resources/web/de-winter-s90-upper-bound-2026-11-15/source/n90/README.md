# n = 90

90 unit squares in a square of side

    9.9940387666098521323

The Squares Project listed 9.998277166926 for n = 90 on 15 November 2026 (T-303, found by jazivxt). The improvement is 0.00424.

## Construction

The packing starts from T-303, which jazivxt built from a crop of the packing for n = 157 in this repository. T-303 has a cluster of 44 squares that lean away from the axes, inside a frame of axis-aligned squares.

A local search changed small groups of squares in position and angle, optimized the packing again after each change, and kept the changes that gave a smaller side. In the new packing the cluster has 40 leaning squares. Four squares in the upper left of the cluster are axis-aligned. Four squares at the top of the cluster lean by 25.1 and 27.8 degrees, where T-303 has 22.9 degrees. One axis-aligned square at the top wall lies 0.32 lower. See `n90_before_after.png` for T-303 and the new packing side by side.

## Local optimum

A linear program over all 90 squares, with every contact linearized at the solution, found no first-order improvement larger than 4e-10. The certificate keeps a smallest gap of 2e-12 between squares. An earlier packing of this arrangement passed the same test at a side 9e-8 larger, so the test covers one set of contacts and says nothing about neighbouring sets.

The certificate proves the upper bound s(90) <= side. The statement on the local optimum rests on the numerical solution described above and has no formal proof.

A public merged submission for the Kaggle competition "Squares in Squares" (bestbryant/claude_code_squaresinsquares, 15 November 2026) lists 9.998277166917 for n = 90. The best sides on the Kaggle leaderboard were not available for this comparison.

## Files

- `n90_exact.json`: exact rational coordinates (centre and unit edge direction of each square) and the side.
- `n90_witness.yaml`: the same packing as a Squares Project witness file (Witness/v2, corners, rational).
- `n90_record.png`: figure of the packing.
- `n90_before_after.png`: figure of T-303 and the new packing.
- `verify_exact.py`: exact checker. Run `python3 -B verify_exact.py` (Python 3.10 or later, standard library only).
- `check_area.py`: second exact checker with separate code. It clips each close pair of squares and requires an intersection of area 0. Run `python3 -B check_area.py`.
- `REGISTRATION.md`: the registration request for the Squares Project, in the form of its template.
- `SHA256SUMS`: checksums of the files above.

## Method and AI assistance

The local search that found the arrangement was run with GPT-6.1 Sol Max (OpenAI). The local optimization, rational certificate, checking and figures were produced with Claude Fable 5.2 (Anthropic). Both worked under the direction of Joost de Winter.
