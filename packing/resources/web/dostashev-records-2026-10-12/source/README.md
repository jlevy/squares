# Squares in a square: new record packings

Packings of *n* unit squares into the smallest square we know of. Each record comes with an exact
certificate and the code to verify it.

| n | side *s* (ours) | previous best | improvement | files |
|---:|---|---|---:|---|
| 155 | 12.952425406958457 | 12.952498944014007, Francisco Couzo's exact refinement of SQUISH's packing | 7.35e-5 | `records/n0155.*` |
| 156 | 12.979172613644427 | 12.982082698516893, Evan Daniel's exact optimum of Francisco Couzo's packing | 2.91e-3 | `records/n0156.*` |
| 211 | 14.996336721336316 | 14.997960704967362, Evan Daniel's exact optimum of Joost de Winter's packing | 1.62e-3 | `records/n0211.*` |
| 175 | 13.764174317486597 | 13.767119024198364, Francisco Couzo's packing (seeded from Ryan Xu's, exact optimum from Evan Daniel's solver) | 2.94e-3 | `records/n0175.*` |
| 232 | 15.764174317486597 | 15.767428349941842, Nate Chaoweeraprasit's (SQUISH) composition | 3.25e-3 | `records/n0232.*` |
| 264 | 16.774735132387833 | 16.778174593052023, Göbel's pattern 9 + (11/2)√2 | 3.44e-3 | `records/n0264.*` |

"Previous best" is the best packing we could find in any public source at the time of writing
(October 2026). We checked:

- David Ellsworth's records page [1];
- the jlevy/squares register, including its side packets and pending registration requests [2];
- the contributors' own repositories [4–7].

Write-up: *Square Packing* (Daniil Ostashev, October 2026).

## Verify

```sh
./verify_all.sh
```

This needs a C++20 compiler, CMake, GMP and MPFR (`brew install gmp mpfr` or
`apt-get install libgmp-dev libmpfr-dev`), and Python ≥ 3.10 with `mpmath` (or `uv`). It runs
three independent checks on every record:

1. **`sqverify --precise --certify`** reads the decimal packing, checks containment and
   non-overlap (separating axes) in 100+-bit arithmetic, then builds an **exact rational
   certificate**:
   - every angle is replaced by a rational half-angle tangent *t*, so cos θ = (1−t²)/(1+t²) and
     sin θ = 2t/(1+t²), and every square is exactly a unit square;
   - centres and side are scaled by 1 + δ (δ = 1e-30);
   - non-overlap and containment are then proven in exact rational arithmetic (GMP), with no
     tolerance.

   The certified bound is printed as `s <= ...`. This construction follows Ryan Xu's
   certificates [3].
2. **`sqverify --check-cert`** checks the shipped `.sqcert` files exactly, with no dilation and
   no tolerance.
3. **`tools/crosscheck_mpmath.py`** is an independent 80-digit check written separately in
   Python.

## File formats

**`.sqpk`.** `#` lines are comments, then `n <n>`, `s <side>`, and *n* lines `cx cy theta_deg`:
unit squares with centre (cx, cy), rotated by theta degrees counter-clockwise, inside
[0, s] × [0, s].

**`.sqcert`.** The same layout in exact rationals: `n`, `s` (rational), then *n* lines `x y t`.
The rationals x and y give the centre, and t = tan(θ/2) gives the rotation exactly. The header
records the dilation δ and the source file.

## How these were found (short version)

Records in this range consist of axis-aligned staircase blocks (Young diagrams) in the corners
and a band of tilted squares between them. Growing such bands by random search does not work
above n ≈ 130: they jam. We instead:

1. **Construct** a V-shaped tilted band explicitly at a chosen angle, and fill the rest of the
   box with aligned corner blocks, chosen by an integer program. No existing record geometry is
   used.
2. **Re-harden on a GPU** (soft-to-rigid [8]): soften the squares slightly, hold the box at its
   side while they re-harden, then release everything and compress it together.
3. **Polish exactly.** With all angles fixed, minimising the side is a linear program (the
   "cell" idea from [2]); iterate it to the exact local optimum.
4. **Canonicalise.** At the same side, slide every square toward its corner, so blocks sit flush
   and the structure is easy to read. Loose squares that fit axis-aligned into a corner block are
   straightened into it, and of the packing's 8 symmetric copies the one with the largest corner
   block top-right is kept.
5. **Exact optimum.** Read off which corner of which square touches which edge, solve that system of
   polynomial equations to 60 digits, and check that no nearby motion shrinks the box (nonnegative
   KKT multipliers). The stored packing is that optimum with the load-bearing squares scaled by
   1 + 1e-20, so every pair is strictly apart; the sides in the table are rounded up, and the files
   give all 60 digits.

### Compositions (175, 232, 264)

Many records are compositions: rectangles of n unit squares whose sides differ by an integer d,
placed in two opposite corners of the box, with the rest filled by aligned squares. David
Ellsworth's s(171), for example, is two copies of a 36-square (h + 2) × h piece of Thomas Schadt's
s(50) plus 99 aligned squares. We built a library of the best known such rectangles (cut from every
known square packing, then re-optimised as rectangles) and a composer that assembles squares from
it, then searched for better rectangles with the same GPU soft-to-rigid method run in a rectangular
box. It found 38 unit squares in an (h + 2) × h rectangle with h = 5.7641743…. Used in place of
s(50)'s piece, it gives 175. Next to a 76-square piece of Erich Friedman's s(85) it gives 232, and
next to a 93-square piece of Joost de Winter's s(126) (Evan Daniel's exact optimum) it gives 264.
Each composite is then taken to the exact optimum of its contact topology, as in step 5.

## References

1. D. Ellsworth, *Squares in Squares* (record table and packings), <https://kingbird.myphotos.cc/packing/squares_in_squares.html>.
2. J. Levy et al., *jlevy/squares*, a register of square-packing bounds, <https://github.com/jlevy/squares>, <https://jlevy.github.io/squares>.
3. R. Xu, "Improving 25 square packing upper bounds", *Slightly Supervised*, October 2026, <https://slightlysupervised.substack.com/p/improving-25-square-packing-upper>; data and certificates <https://github.com/ry-xu/square_packing>.
4. F. Couzo, *square-packing*, <https://github.com/franciscouzo/square-packing>.
5. E. Daniel, *square-packing*, <https://github.com/evand/square-packing>.
6. N. Chaoweeraprasit (SQUISH), *squish-certs*, <https://github.com/itsnaka/squish-certs>.
7. E. Friedman, "Packing Unit Squares in Squares: A Survey and New Results", *Electronic Journal of Combinatorics*, Dynamic Survey DS7, <https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS7>.
8. Y. Nakajima, *Soft-to-rigid packing*, <https://yoheinakajima.github.io/soft-to-rigid-packing/>, <https://github.com/yoheinakajima/soft-to-rigid-packing>.

## License

MIT, see `LICENSE`. This covers the verification code and our record packings and certificates.
