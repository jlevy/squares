# n = 295

295 unit squares in a square of side

    17.6996934417152215000000000 (rounded up at 25 places)

The Squares Project listed 17.70423279073603036 ((22 + 22 sqrt(2))/3) for n = 295 on 16 November 2026. The improvement is 0.00454.

## Construction

A band of 72 squares, tilted by 25 to 30 degrees and arranged 4 squares wide and 18 long, runs along the diagonal from the lower left to the upper right. The other 223 squares are axis-aligned and fill the two regions beside the band. See `n295_record.png`.

The band was built from a closed-form layout. An integer program placed the axis-aligned squares, a numerical optimization of all squares followed, and the result was rounded to exact rational coordinates. No coordinates of other packings were used.

The packings for n = 262 and n = 295 share the band. The packing for n = 295 is the packing for n = 262 with an L-shaped border of 33 axis-aligned squares, so its side is larger by exactly 1.

## Optimality

The certificate proves the upper bound s(295) <= side. It makes no statement on optimality. No local optimality test was run, and the figure shows small gaps, so a further small reduction of the side is likely possible.

## Files

- `n295_exact.json`: exact rational coordinates (centre and unit edge direction of each square) and the side.
- `n295_witness.yaml`: the same packing as a Squares Project witness file (Witness/v2, corners, rational).
- `n295_record.png`: figure of the packing.
- `verify_exact.py`: separating-axis check in rational arithmetic (`python3 -B verify_exact.py`).
- `check_area.py`: intersection-area check in rational arithmetic (`python3 -B check_area.py`).
- `SHA256SUMS`: checksums of the files above.
