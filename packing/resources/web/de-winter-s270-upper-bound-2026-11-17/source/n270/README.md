# n = 270

270 unit squares in a square of side exactly

    16927314216351701364094693919616632628260321141481608494025753/1000000000000000000000000000000000000000000000000000000000000
    = 16.927314216351701

The Squares Project listed 16.928148603342855 for n = 270 on 17 November 2026 (witness n-270 at jlevy/squares commit f9ddfeeef9070ede581142154ab992149b278ab0). The improvement is 0.00083.

## Construction

The search started from the 270-square packing in Asterios Panoras's public Kaggle compilation (version 17, side 16.92746606488242), a merge of many contributors that does not name the finder of this arrangement. It removed and relaxed the two end regions in turn, compressed a 68-square region at the bottom inside a rectangle, reassembled the packing and optimized the position and angle of every square.

## Comparison

The best public coordinates are those of Panoras's compilation at 16.92746606488242. Danil Malyshev's coordinates in issue #1012 give 16.927469593519. This packing is 0.00015 below both. On the Kaggle per-puzzle leaderboard of "Squares in Squares" (notebook version 370726548), the team [NUP] Junie is all you need reported 16.927314216351814 for n = 270 (9 November 2026). This packing is 1.1e-13 below that value, so the two packings are probably the same local optimum. Their coordinates were not found.

The certificate proves the upper bound s(270) <= side. It makes no statement on optimality.

## Files

- `n270_exact.json`: exact rational coordinates (centre and unit edge direction of each square) and the side.
- `n270_witness.yaml`: the same packing as a Squares Project witness file (Witness/v2, corners, rational).
- `n270_record.png`: figure of the packing. The 78 tilted squares are orange.
- `verify_exact.py`: exact checker. Run `python3 -B verify_exact.py` (Python 3.10 or later, standard library only).
- `check_area.py`: second exact checker with separate code. It clips each close pair of squares and requires an intersection of area 0. Run `python3 -B check_area.py`.
- `REGISTRATION.md`: the registration request for the Squares Project, in the form of its template.
- `SHA256SUMS`: checksums of the files above.

## Method and AI assistance

The search, optimization and rational certificate were produced with GPT-6.2 Sol (OpenAI). The repository files, checks and figure were produced with Claude (Anthropic). Both worked under the direction of Joost de Winter.
