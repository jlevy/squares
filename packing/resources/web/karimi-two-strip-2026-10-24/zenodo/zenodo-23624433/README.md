# Two-strip square packings: improved upper bounds for s(n)

**Author:** Mohsen Karimi (independent researcher, Zanjan, Iran) — ORCID 0009-0004-1055-8267

This record set contains 683 packings of n unit squares in a square of side
s < ⌈√n⌉, for n between 1184 and 3775. Each one improves the best known
upper bound in the public catalogues Mishapolk/square-packing-records (commit 7e82c64,
23 Oct 2026) and franciscouzo/square-packing (snapshot of 24 Oct 2026).
In 85 cases the previous best was the trivial grid.

## Construction (Karimi two-strip construction)

The idea and the cost–benefit design are due to Mohsen Karimi.
In a box of side S just below an integer K, a plain grid fits K−1 squares per row.
Two strips of squares tilted by a small angle a are attached to the walls:

* an **H strip** of mH rows lying on the bottom wall, from the left wall to the V strip;
* a **V strip** of mV columns standing on the right wall, full height;
* the rest is a (K−mV) × (K−mH) axis-parallel grid in the top-left corner.

Within a strip, consecutive rows touch with vertical pitch cos a and horizontal shift
sin a, so a strip of m rows is m·cos a + sin a high. The strip pays for itself when
m(1 − cos a) ≥ sin a + (K − S): then each grid column (row) above (beside) it holds K
squares instead of K−1, at a cost of about sin a per unit length plus the two strip ends.
The angles have rational tan(a/2), so every coordinate is rational.

## Regenerating the certificates

The certificates are not stored here; they are rebuilt exactly from the parameters:

    python3 regenerate.py            # all 683, about 10 seconds, Python 3 only
    python3 regenerate.py 2458       # a single n

## Verification

Every certificate (`certificates/n<N>.cert`, format `x y t` with t = tan(θ/2), exact
rationals) was checked with the exact rational verifier `verify_bound_certificate.py`
of Mishapolk/square-packing-records (separating-axis test in exact arithmetic; result
VALID, closed container). Run `python3 check_packing.py certificates/nN.cert` from
that repository to re-check any of them.

## Files

* `records.csv` — n, new side (exact and decimal), previous best, and the construction parameters (K, mH, tH, phH, mV, tV, phV).
* `regenerate.py` — rebuilds every certificate exactly from `records.csv`.

## Credits

Construction idea, strip cost–benefit analysis and research direction: Mohsen Karimi.
Code and computations were written with the assistance of Claude (Anthropic), an AI
model, under the author's direction. Verifier: M. Polkovskyi (Mishapolk).

License: data CC BY 4.0; code MIT.
