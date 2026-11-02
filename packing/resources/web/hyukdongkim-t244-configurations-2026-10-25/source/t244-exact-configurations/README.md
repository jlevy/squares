# Exact configurations for T-244: s(172) and s(263)

Each certificate places the record packing of n unit squares in the square of side S*. Here S* is the exact side registered as T-244 from issue #804: the root of the degree-24 (n = 172) or degree-17 (n = 263) polynomial given there. Every centre and every half-angle tangent lies in a number field K = Q[t]/f. Every contact is an identity in K, and every other pair and every wall is separated exactly.

| file | n | K | generator t | side S* | equal to the record within |
|---|---:|---|---|---|---|
| `n172.minpoly.json` | 172 | degree 24, f height 1.8·10⁷ | half-angle tangent of square 136 (the 44.73° band) | root of P₁₇₂ in [Sa, Sb] | 1.8·10⁻¹² (centres), 6.5·10⁻¹²° (angles) |
| `n263.minpoly.json` | 263 | degree 17, f height 41402 | half-angle tangent of square 120 (the 43.81° band) | root of P₂₆₃ in [Sa, Sb] | 3.5·10⁻¹³ (centres), 3.3·10⁻¹²° (angles) |

The records are T-174's witnesses, read from evand/square-packing `site/www/data/p/best-<n>.json` at revision `659ee62e4a9d39542a1146e8b011cc3ab6407ede`. In both certificates S itself lies in K, as `S.in_K`.

## Format

The files use exactly the `minpoly.json` format of evand/square-packing's `search/exact/verify_exact.py`:
- `field.f`: the integer coefficients of f, lowest degree first.
- `field.t_interval`: a rational interval holding the root t*.
- Per square: the centre `x`, `y` and the angle parameter `u = tan(θ'/2)`, each as rational coefficients in t; and `m`, the number of quarter turns. The side directions are (c, s) = R^m((1−u²)/(1+u²), 2u/(1+u²)).
- `S`: `in_K`, the integer polynomial `poly` and an isolating `interval`.

## Check

Run two checkers that share no code:

```
# 1. The reviewed checker (T-193), unchanged, from the pinned revision:
python3 evand-square-packing/search/exact/verify_exact.py n172.minpoly.json n263.minpoly.json

# 2. An independent checker in this bundle (needs python-flint):
pip install python-flint
python3 check_field_packing.py n172.minpoly.json n263.minpoly.json
```

The two checkers report:

| | verify_exact.py | check_field_packing.py |
|---|---|---|
| n = 172 | VALID: 1026 identities in K, 4030 strict by intervals, 14130 pairs by discs; ~7 s | VALID: 347 contacts exact in K, 683 strict by Arb balls, 14364 pairs far apart; ~3 s |
| n = 263 | VALID: 1593 identities in K, 6231 strict by intervals, 33549 pairs by discs; ~10 s | VALID: 564 contacts exact in K, 1043 strict by Arb balls, 33898 pairs far apart; ~3 s |

How `check_field_packing.py` differs from `verify_exact.py`:
- **Arithmetic.** Exact arithmetic in K uses FLINT `fmpq_poly` reduced mod f, with inverses by extended gcd. Signs come from Arb balls at t*, after exact bisection of the t interval; an inequality whose ball contains 0 must be exactly 0 in K.
- **Separation test.** For each pair it projects onto the four side normals and checks |Δc·a| − h_i(a) − h_j(a) ≥ 0, rather than testing corners against side lines.
- **Extra checks.** It also asserts that f is irreducible and that the number of squares equals n.
- **Different counts.** It stops at the first axis that proves a pair, which is why its counts differ from those of `verify_exact.py`.

## Controls

`python3 controls.py <checker> <cert>` mutates a certificate and runs the checker on each mutation. Both checkers reject every one of these, at both counts:
- a duplicated square, with n raised;
- the side reduced by 10⁻³⁰;
- the t interval moved off the root;
- a band square turned by about 10⁻³⁰ (square 136 at 172, square 120 at 263);
- most single-square moves by 10⁻³⁰ in x or y.

A move is accepted, identically by both checkers, only where the square has slack in that direction: square 0 at 263 (+x and −y).

With the square count left inconsistent with `n`, `verify_exact.py` checks only the first n squares, so the claim is unaffected. `check_field_packing.py` rejects such a file.

## How the configurations were built

1. Solve the KKT system of minimizing the side on the record's active contacts to 3000 digits, starting from the binary64 record (issue #804's method).
2. Take t, the half-angle tangent of a band square. LLL gives its minimal polynomial f. Recognize S and every other half-angle tangent in Q(t) by LLL.
   - Squares whose angle is a free direction of the numerical solve are snapped back to their angle class: 4, 145 and 181 at 263, by less than 2·10⁻¹⁶; 133 at 172, by 0.
   - Every angle in both certificates is in K.
3. With S and the angles exact, every active contact is linear in the centres. Pin the free directions of that linear system to the record's own binary64 values, exactly: 8 coordinates at 172 and 3 at 263. Solve the system to about 2850 digits.
4. Recognize every centre in Q(t) by LLL. The largest numerator or denominator in the data has 65 digits at 172 and 83 at 263.

The checkers depend on none of these steps.

`distance_to_record.py` reports the distance to the record, evaluated in binary64.
