# n = 305

305 unit squares in a square of side exactly

    179457558387415886710583983360138290031648651962347523515443824166144058057388817807/10000000000000000000000000000000000000000000000000000000000000000000000000000000000
    = 17.945755838741589

The Squares Project listed 17.9457623596589697 for n = 305 (T-309, Tomáš Kodaj, improved by JoeGun). The improvement is 6.5e-6.

## Construction

The arrangement is Tomáš Kodaj's public Kaggle packing as improved by JoeGun (T-309, two quench runs with Evan Daniel's code and a fault-line step). The search started from that arrangement in Alex Chilton's public compilation and re-optimized the positions and angles of all squares, followed by a rational enclosure. Compared with the project's regularized drawing of T-309, all 305 squares correspond under the identity symmetry: 302 move by less than 0.1, the largest move is 0.178, the RMS move is 0.018, and no tilt is reversed.

## Comparison

On the Kaggle per-puzzle leaderboard of "Squares in Squares" (version 38, run 371230297), Shadoks reported 17.94575583874176 for n = 305 on 15 November 2026. This packing is 1.7e-13 below that value, so the two probably reach the same local optimum. Their coordinates were not found. The certificate is also below the project's own local re-solve of T-309 (17.945762359467513).

The certificate proves the upper bound s(305) <= side. It makes no statement on optimality.

## Files

- `n305_exact.json`: exact rational coordinates (centre and unit edge direction of each square) and the side.
- `n305_witness.yaml`: the same packing as a Squares Project witness file (Witness/v2, corners, rational).
- `n305_record.png`: figure of the packing. Tilted squares are orange.
- `verify_exact.py`, `check_area.py`: two exact checkers with separate code. Run `python3 -B verify_exact.py` and `python3 -B check_area.py`.
- `REGISTRATION.md`, `SHA256SUMS`.

## Method and AI assistance

The search, optimization and rational certificate were produced with OpenAI Codex. The repository files, checks and figure were produced with Claude (Anthropic). Both worked under the direction of Joost de Winter.
