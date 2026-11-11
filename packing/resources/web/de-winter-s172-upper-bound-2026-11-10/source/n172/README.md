# n = 172

172 unit squares in a square of side

    13.61468985328358057514628890087947061618972730200175769881498026931092424681356737007190165664341823032345866914...

The Squares Project listed 13.6146898532862152 for n = 172 on 10 November 2026. The improvement is 2.6e-12.

## Predecessor

The arrangement is the 172-square packing found by Evan Daniel and improved by Doğa Özden (Squares Project issue #935, registered on 9 November 2026). No square was added, removed or moved to a different position in the contact structure. Credit for the arrangement belongs to them.

## Contribution

The packing was re-optimized here to the exact local optimum of that arrangement. The side of the local optimum is the real root near 13.6147 of the irreducible polynomial

    62x^5 - 4116x^4 + 107933x^3 - 1397031x^2 + 8918035x - 22427977.

The polynomial was identified from 108 digits of a 130-digit solution of the optimality conditions. An independent solution of the contact equations at about 390 digits closes all contacts with a residual below 1e-389, and its side agrees with the root of the polynomial to 386 digits. The contact equations have rank 285 and fix the side to first order. Non-negative contact forces in balance exist (checked in floating point). The side in the rational certificate is 1.6e-319 above the root.

The certificate proves the upper bound s(172) <= side. The local optimality statement rests on the numerical solution described above and has no formal proof. The polynomial was identified numerically and confirmed by an exact sign test. A symbolic derivation from the geometry is absent.

The same packing with a border of 27 axis-aligned squares gives the packing in [n199](../n199/).

## Files

- `n172_exact.json`: exact rational coordinates (centre and unit edge direction of each square) and the side.
- `n172_optimum_300_digits.txt`: side, centres and edge directions at the local optimum, truncated to 300 decimals. Squares that can move without changing the side keep the position they have in the certificate.
- `n172_witness.yaml`: the same packing in the Squares Project witness format (center-basis, rational).
- `n172_record.png`: figure. Tilted squares are yellow.
- `verify_exact.py`: exact checker. Run `python3 -B verify_exact.py` (Python 3.10 or later, standard library only).
- `SHA256SUMS`: checksums of the files above.

## Method and AI assistance

The local optimization, high-precision solution, rational certificate, checking and figure were produced with Claude (Anthropic) under the direction of Joost de Winter.
