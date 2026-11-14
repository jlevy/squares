# n = 332 and n = 409 from the n = 297 packing

Two packings of n unit squares in a square, each with a smaller side than the best value recorded by the Squares Project for that n on 14 November 2026 (repository `jlevy/squares` at commit 7629f5a).

| n | Side, rounded up | Best recorded value | Improvement |
| ---: | ---: | ---: | ---: |
| 332 | 18.739455558289 | 18.740417287544 | 0.00096 |
| 409 | 20.739455558289 | 20.740417290708 | 0.00096 |

## Construction

Both packings are the packing of 297 squares in [n297](../n297/) plus axis-aligned squares.

- n = 332: the 297 packing moved by (1, 1), 18 squares along the bottom wall and 17 squares along the left wall.
- n = 409: the 297 packing moved by (3, 3), two arms of 3 x 17 squares against the far walls, and 10 squares in the corner. Five of these 10 squares lie in a square of side 2.72, with one of them tilted by 45 degrees.

The recorded values for 332 and 409 are built in the same way from the record T-174 for n = 297. The credit stated in [n297](../n297/) applies here as well: the layout is that of T-174 (packing by Francisco Couzo, exact optimum by Evan Daniel, refinement by PingYou Ltd).

## Files

- `n332_exact.json`, `n409_exact.json`: exact rational coordinates (centre and unit edge direction of each square) and the side.
- `build.py`: writes both files from `../n297/n297_exact.json`.
- `verify_exact.py`, `check_area.py`: two exact checkers with separate code. Run `python3 -B verify_exact.py n332_exact.json` and `python3 -B check_area.py n332_exact.json` (Python 3.10 or later, standard library only).
- `SHA256SUMS`: checksums of the files above.

## Registration request

**Credit name.** Joost de Winter, Delft University of Technology.

**Claim.** s(332) <= 18.739455558289 and s(409) <= 20.739455558289 (rounded up at 12 places). The record holds 18.740417287544 and 20.740417290708.

**Certificate.** `n332_exact.json` and `n409_exact.json` in this folder.

**Checking.** `verify_exact.py` (separating-axis test, Python `fractions.Fraction`) reports 332 squares with 729 close pairs and 409 squares with 875 close pairs. `check_area.py` (area of the clipped intersection, Python `fractions.Fraction`) reports the same counts. Each run takes a few seconds.

**What the checkers share.** One author, Python's `Fraction` type and the same input files.

**Not done.** The certificates have not been checked with the tools of the Squares Project.

**Lineage and credit.** The packing of 297 squares in this repository, which builds on T-174. The added squares follow the construction of the recorded values for 332 and 409.

**AI assistance.** The construction and the checks were produced with Claude Fable 5.2 (Anthropic) under my direction.
