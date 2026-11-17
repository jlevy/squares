# n = 292

292 unit squares in a square of side

    17.5900164428464147126481796 (rounded up at 25 places)

The Squares Project listed 17.5913781454976982 for n = 292 on 16 November 2026 (T-146). The improvement is 0.00136.

## Construction

The packing has one continuous ribbon of 59 squares, tilted by 40 to 42 degrees, that runs along the diagonal from the lower left to the upper right. The other 233 squares are axis-aligned and fill the two triangular regions beside the ribbon. See `n292_record.png`.

The ribbon extends the tilted ribbon of the packing of 146 unit squares with side 12.583782190152, found by David W. Cantrell in 2025. That ribbon has 37 squares and repeats after a shift of (5, 5). Two copies, one at (0, 0) and one at (5, 5), share 15 squares and form a ribbon of 59 squares. The coordinates of the 146 packing were taken from a public notebook of the Kaggle competition "Squares in Squares" (sigmaborov, "Squares in Squares: certified contact polish", Apache License 2.0, as included in areebbb's "merge 28" notebook).

The positions of the 233 axis-aligned squares come from an integer program that places as many grid squares as possible beside the ribbon. A numerical optimization of all 292 squares followed, and the result was rounded to exact rational coordinates.

The packing listed by the Squares Project for n = 292 has two separate tilted blocks, of 16 and 33 squares.

## Local optimum and other known values

A linear program over all 292 squares, with every contact linearized at the solution, found no first-order improvement. The certificate keeps a smallest gap of 3e-12 between squares. This test covers one set of contacts and says nothing about neighbouring sets.

The certificate proves the upper bound s(292) <= side. It makes no statement on optimality.

A public merged submission for the Kaggle competition (bestbryant/claude_code_squaresinsquares, 16 November 2026) lists 17.591378147172 for n = 292. A table of the best sides per team of 8 November 2026 (Samanyu-dev/squares_in_squares) lists 17.589053943368 for the team "Cats and boxes". No packing for that side is public.

## Files

- `n292_exact.json`: exact rational coordinates (centre and unit edge direction of each square) and the side.
- `n292_witness.yaml`: the same packing as a Squares Project witness file (Witness/v2, corners, rational).
- `n292_record.png`: figure of the packing.
- `verify_exact.py`: exact checker. Run `python3 -B verify_exact.py` (Python 3.10 or later, standard library only).
- `check_area.py`: second exact checker with separate code. It clips each close pair of squares and requires an intersection of area 0. Run `python3 -B check_area.py`.
- `REGISTRATION.md`: the registration request for the Squares Project, in the form of its template.
- `SHA256SUMS`: checksums of the files above.

## Method and AI assistance

The construction and the search were run with Gemini Carbon (Google). The checking, the witness file, the figure and the comparison with other known values were produced with Claude Fable 5.2 (Anthropic). Both worked under the direction of Joost de Winter.
