# n = 199

199 unit squares in a square of side

    14.61468985328358057514628890087947061618972730200175769881...

The Squares Project listed 14.6175721735928069 for n = 199 on 9 November 2026. The improvement is 0.00288.

## Construction

The packing consists of a 172-square core and a border of 27 axis-aligned squares (a row of 14 and a column of 13). The core uses the arrangement of the 172-square packing found by Evan Daniel and improved by Doğa Özden (Squares Project, 9 November 2026). The core was re-optimized here to the exact local optimum of that arrangement.

## Exact optimum

The side of the local optimum is the real root near 14.6147 of the irreducible polynomial

    62x^5 - 4426x^4 + 125017x^3 - 1746146x^2 + 12052670x - 32855154.

The optimality conditions of the core were solved to 130 digits. All 734 load-bearing or forced contacts close exactly and all other gaps stay open. The polynomial was identified from 108 digits and reproduces the side to 129 digits. The side in the rational certificate is 1.4e-99 above the root.

The certificate proves the upper bound s(199) <= side. The local optimality statement rests on the numerical solution described above and has no formal proof.

## Files

- `n199_exact.json`: exact rational coordinates (centre and unit edge direction of each square) and the side.
- `n199_witness.yaml`: the same packing in the Squares Project witness format (center-basis, rational).
- `n199_record.png`: figure. The core is grey and yellow and the border is blue.
- `verify_exact.py`: exact checker. Run `python3 -B verify_exact.py` (Python 3.10 or later, standard library only).
- `SHA256SUMS`: checksums of the files above.

## Method and AI assistance

The derivation, local optimization, high-precision solution, rational certificate, checking and figure were produced with Claude (Anthropic) under the direction of Joost de Winter.
