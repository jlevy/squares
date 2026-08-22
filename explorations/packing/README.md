# Square packing: exact verification

Tooling written while researching
[research-2026-08-22-square-packing-algorithms-and-tooling.md](../../docs/project/research/research-2026-08-22-square-packing-algorithms-and-tooling.md).

`s(n)` is the side of the smallest square holding `n` non-overlapping unit squares.
Record packings are published as high-precision decimals, and there is no public tool
that checks one **exactly**.
This is that check.

## Why exactness needs more than precision

A valid packing has squares with disjoint *interiors*, so touching is allowed — and in a
record packing many squares touch exactly.
The separation on those pairs is exactly zero.

Floating point and interval arithmetic can prove a strict inequality; neither can prove
an equality. So a float check needs a slack tolerance to accept the true contacts, and
that tolerance is then a blind spot that accepts small overlaps.
Setting the tolerance to zero rejects the true packing instead.
`negative_control.py` demonstrates both failure modes.

The fix is representational, not numerical: put the configuration in the real algebraic
number field it actually lives in, where equality is decidable.

## Layout

```
sqpack/
  field.py               exact arithmetic in Q(alpha): +, -, *, /, exact zero test,
                         exact sign by rational interval arithmetic with bisection
  verify.py              separating-axis validity check, generic over the scalar type;
                         exact or float backend, optional grid bucketing
  packings/trump11.py    Walter Trump's 1979 packing of 11 unit squares, exactly
derive_field.py          derives the number field from the published polynomial
verify_trump11.py        verify the packing and report what it took
negative_control.py      show the verifier rejects bad packings, and where float64 fails
bench.py                 exact vs approximate cost, and scaling with algebraic degree
test.sh                  run everything and check the expected results
```

Only `derive_field.py` needs a third-party package (SymPy).
The verifier itself is standard library only.

## Use

```bash
python3 verify_trump11.py     # exact verification of s(11) <= 3.877083590022814...
python3 negative_control.py   # exact rejects any overlap; float64 has a blind spot
python3 bench.py              # timings
python3 derive_field.py       # re-derive the field (needs sympy)
./test.sh                     # all of the above, with assertions
```

`verify_trump11.py` output:

```
VALID: 11 squares, 55 pairs tested
  container: 20 corner coordinates exactly on the boundary
  pairs:     14 separated with zero gap, 41 strictly
  field:     Q(u), degree 8, u = tan(a/2)
  P(s) == 0 for the published degree-8 polynomial: True
  s = 3.87708359002281417730789706010096270637645566846
```

The 14 zero-gap pairs are the ones no floating-point verifier can certify.
The 33 leading digits match the value published on the
[Squares in Squares](https://kingbird.myphotos.cc/packing/squares_in_squares.html)
record page, so this is also an independent check of that record.

## Verifying another packing

Supply the corners in an exact field and call `verify_packing`:

```python
from sqpack.field import NumberField
from sqpack.verify import verify_packing, exact_sign

field = NumberField(min_poly, isolating_interval)   # coefficients high degree first
squares = [...]                                     # 11 x 4 corners of FieldElements
print(verify_packing(squares, side, sign=exact_sign))
```

The work is in the first line.
Record packings are published as SVG transforms with 33-digit decimal entities and, for
the analytically solved ones, Mathematica source in an XML comment; recovering the field
means reading that by hand, once per packing.
`sqpack/packings/trump11.py` is the worked example.

For a quick, non-certifying check, swap in the float backend:

```python
from sqpack.verify import float_sign
verify_packing(squares, side, sign=float_sign(1e-9), bucket=True)
```

`bucket=True` grid-buckets the squares so pair enumeration is linear rather than
quadratic — at `n = 1000` that is 15,936 candidate pairs instead of 499,500.

## Scope

This checks that a *proposed* packing is valid, which is a different and far easier
question than whether it is optimal.
The only rigorous computer-assisted optimality proof for rotatable unit squares in any
container covers three squares in a circle (Montanher et al. 2018); nothing comparable
exists for squares in a square.
