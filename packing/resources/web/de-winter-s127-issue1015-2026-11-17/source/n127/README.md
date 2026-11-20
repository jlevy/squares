# n = 127

127 unit squares in a square of side

    11.800795682213569410918500357438642704527

The Squares Project listed 11.8017538904864874 for n = 127 on 17 November 2026 (T-305, Tomáš Kodaj, improved by JoeGun). The improvement is 0.00096.

## Construction

The packing has a tilted central band of 57 squares inside a frame of axis-aligned squares. The search started from an exact certificate of an arrangement in the public Kaggle coordinate compilations of Alex Chilton and Asterios Panoras. It changed the sliding offsets of the columns in the tilted band and then optimized the positions and angles of individual squares.

## Comparison

On the Kaggle per-puzzle leaderboard of "Squares in Squares", Luka Cvetkovic reported a side of 11.800793726618 for n = 127 (16 November 2026), which is 0.0000020 smaller than this packing. His coordinates were not found.

The certificate proves the upper bound s(127) <= side. It makes no statement on optimality.

## Files

- `n127_exact.json`: exact rational coordinates (centre and unit edge direction of each square) and the side.
- `n127_witness.yaml`: the same packing as a Squares Project witness file (Witness/v2, corners, rational).
- `n127_record.png`: figure of the packing. Tilted squares are orange.
- `verify_exact.py`: exact checker. Run `python3 -B verify_exact.py` (Python 3.10 or later, standard library only).
- `check_area.py`: second exact checker with separate code. It clips each close pair of squares and requires an intersection of area 0. Run `python3 -B check_area.py`.
- `REGISTRATION.md`: the registration request for the Squares Project, in the form of its template.
- `SHA256SUMS`: checksums of the files above.

## Method and AI assistance

The search, optimization and rational certificate were produced with GPT-6.2 Sol (OpenAI). The repository files, checks and figure were produced with Claude (Anthropic). Both worked under the direction of Joost de Winter.
