# n = 299

299 unit squares in a square of side exactly

    17793636991743040580325825384225613703947282755372586749208848013397/1000000000000000000000000000000000000000000000000000000000000000000
    = 17.793636991743040580

The Squares Project listed 17.801004434255294 for n = 299 on 18 November 2026 (T-277, Doğa Özden after Evan Daniel). The improvement is 0.0074.

## Construction

The search divided the container into diagonal slices and filled each slice from a reflected or translated copy of a public packing: the outer slices from 372 squares and the seven middle slices from 335 squares. Both donors came from Asterios Panoras's public Kaggle compilation (version 17). Kaggle's community explorer (nevska) links the 372-square packing to prvsiyan's notebook "A Square Deal" and the 335-square packing to four notebooks with the same score, by areebbb, jazivxt, alexchilton and prvsiyan. A local optimization followed, in which the separating edges of touching pairs were exchanged. Reflecting part of one tilted group across the diagonal x + y = S and releasing the neighbouring squares gave the final gain. In the final layout 55 squares tilt at least 15 degrees one way and 54 at least 15 degrees the other way.

## Comparison

On the Kaggle per-puzzle leaderboard of "Squares in Squares" (notebook completed 18 November 2026, 01:07:56 UTC), Nick Sarris reported 17.793636991746555 for n = 299. This packing is 3.5e-12 below that value, so the two packings are probably the same local optimum. His coordinates were not found.

The certificate proves the upper bound s(299) <= side. It makes no statement on optimality.

## Files

- `n299_exact.json`: exact rational coordinates (centre and unit edge direction of each square) and the side.
- `n299_witness.yaml`: the same packing as a Squares Project witness file (Witness/v2, corners, rational).
- `n299_record.png`: figure of the packing. Tilted squares are orange.
- `verify_exact.py`: exact checker. Run `python3 -B verify_exact.py` (Python 3.10 or later, standard library only).
- `check_area.py`: second exact checker with separate code. It clips each close pair of squares and requires an intersection of area 0. Run `python3 -B check_area.py`.
- `REGISTRATION.md`: the registration request for the Squares Project, in the form of its template.
- `SHA256SUMS`: checksums of the files above.

## Method and AI assistance

The search, optimization and rational certificate were produced with GPT-6.2 Sol (OpenAI). The repository files, checks and figure were produced with Claude (Anthropic). Both worked under the direction of Joost de Winter.
