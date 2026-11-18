# n = 127

127 unit squares in a square of side exactly

    5900396863307481119664515678048233366964863482714849291045437/500000000000000000000000000000000000000000000000000000000000
    = 11.800793726614963

The Squares Project listed 11.8017538904864874 for n = 127 on 17 November 2026 (T-305, Tomáš Kodaj, improved by JoeGun). The improvement is 0.00096.

## Construction

The packing has a tilted central band of 57 squares inside a frame of axis-aligned squares. The search started from an exact certificate of an arrangement in the public Kaggle coordinate compilations of Alex Chilton and Asterios Panoras, whose original finder could not be established. It changed the sliding offsets of the columns in the tilted band, shifted two groups of squares in the band lengthwise, and optimized the positions and angles of all squares.

## Comparison

On the Kaggle per-puzzle leaderboard of "Squares in Squares" (notebook version 370726548), Luka Cvetkovic reported 11.800793726617185 for n = 127 (16 November 2026). This packing is 2.2e-12 below that value, so the two packings are probably the same local optimum. His coordinates were not found.

The certificate proves the upper bound s(127) <= side. It makes no statement on optimality.

## Files

- `n127_exact.json`: exact rational coordinates (centre and unit edge direction of each square) and the side.
- `n127_witness.yaml`: the same packing as a Squares Project witness file (Witness/v2, corners, rational).
- `n127_record.png`: figure of the packing. The 57 tilted squares are orange.
- `verify_exact.py`: exact checker. Run `python3 -B verify_exact.py` (Python 3.10 or later, standard library only).
- `check_area.py`: second exact checker with separate code. It clips each close pair of squares and requires an intersection of area 0. Run `python3 -B check_area.py`.
- `REGISTRATION.md`: the registration request for the Squares Project, in the form of its template.
- `SHA256SUMS`: checksums of the files above.

## Method and AI assistance

The search, optimization and rational certificate were produced with GPT-6.2 Sol (OpenAI). The repository files, checks and figure were produced with Claude (Anthropic). Both worked under the direction of Joost de Winter.
