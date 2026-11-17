# n = 297

297 unit squares in a square of side

    17.73945555828895172457454811760973557490907042860652...

The Squares Project listed 17.7404172875438019 for n = 297 on 14 November 2026. The improvement is 0.00096.

## Construction

The packing keeps the layout of the Squares Project record T-174 (packing by Francisco Couzo, exact optimum by Evan Daniel, refinement by PingYou Ltd). That layout has an upper left block and a lower right block of axis-aligned squares with staircase edges, a block of 10 squares in the lower left corner and in the upper right corner, and a diagonal band of 18 columns of tilted squares between the two staircases.

Two things are new.

1. Each staircase has two steps of double size, at the 6th and at the 13th column of the band (counted from the lower left). Between these two places the band lies one staircase step closer to the upper left block. The upper left block has 6 squares fewer than in the record and the lower right block has 4 squares more. The band column at each double step holds 7 squares. The other 16 columns hold 6 squares. The band holds 110 squares and the blocks hold 187.
2. The band columns lean in two groups. The columns on the lower left lean one way by 0.375 degrees and the columns on the upper right lean the other way by the same angle (89 of the 110 band squares). The other 21 band squares have other small leans. Most of them lie in the four middle columns and in the two end columns. In the record the columns lean in four groups (by 0.260 degrees), because some columns are held between a corner of the lower staircase and a corner of the upper staircase, and these corners dictate the lean direction. The shift of the middle part of the band reverses the dictated direction there, so one change of direction remains where the record has three. Each change of direction costs length along the band. The saved length allows a smaller side.

The double step was taken from the staircases of the pinwheel packings for n = 132 and n = 157 in this repository. See `n297_before_after.png` for the record and the new packing side by side.

## Local optimum

The band was optimized with a sequence of linear programs. The optimization was restarted many times from random changes to groups of band squares. Two series of restarts with different random seeds ended at the same side, 17.7394555582889. A linear program over all 297 squares then found no first-order improvement. The contact equations of the result were solved in 330-digit arithmetic. All 4289 contact equations (a corner of one square on the edge line of another square, or a corner on a wall) are satisfied to 1e-306, and the 33 other near contacts stay open by at least 2.1e-7. The side in the rational certificate is 1.8e-59 above this solution.

The place where the lean direction changes was also tried one and two columns to either side of the middle. Before the random restarts, the middle position gave 17.7394733018 and the four other positions gave 17.7394781380. The random restarts were run for the middle position only.

The certificate proves the upper bound s(297) <= side. The statement on the local optimum rests on the numerical solution described above and has no formal proof.

The per-puzzle leaderboard of the Kaggle competition "Squares in Squares" listed 17.7404101723 as the best side for n = 297 on 13 November 2026. That leaderboard shows no packings.

## Files

- `n297_exact.json`: exact rational coordinates (centre and unit edge direction of each square) and the side.
- `n297_witness.yaml`: the same packing as a Squares Project witness file (Witness/v2, center-basis, rational).
- `n297_solution_250_digits.txt`: the solution of the contact equations. The first line is the side. Each further line gives x, y and the angle in radians of one square.
- `n297_record.png`: figure of the packing.
- `n297_before_after.png`: figure of the Squares Project record and the new packing.
- `verify_exact.py`: exact checker. Run `python3 -B verify_exact.py` (Python 3.10 or later, standard library only).
- `check_area.py`: second exact checker with separate code. It clips each close pair of squares and requires an intersection of area 0. Run `python3 -B check_area.py`.
- `SHA256SUMS`: checksums of the files above.

## Method and AI assistance

The construction, optimization, high-precision solution, rational certificate, checking and figures were produced with Claude Fable 5.2 (Anthropic) under the direction of Joost de Winter.
