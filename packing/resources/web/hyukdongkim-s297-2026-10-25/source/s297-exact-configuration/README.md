# Exact configuration for s(297): the stationary side, degree 21

`n297.minpoly.json` places T-174's record packing at 297 (#574, atlas `best-297.json` at `659ee62`) in the square of side S*.
S* is the only real root of an irreducible degree-21 integer polynomial (`S.poly` in the file):

S* = 17.740417287543801850975801594884289593640654923446195273425233561350268049817798181605818039609627693...

This is 3.36e-90 below #574's certificate.

- Every centre and every half-angle tangent lies in K = Q(t), where t is the half-angle tangent of the 44.74-degree band (square 195). K has degree 21, and f has height 300667.
- S lies in K.
- Every contact is an identity in K.
- The configuration equals the record within 1.6e-14 (centres) and 7.1e-14 degrees (angles), evaluated in binary64.

The format is that of evand/square-packing `search/exact/verify_exact.py`. The construction and the checkers are the same as for T-244 (issue #804), and the same controls pass.

```
python3 evand-square-packing/search/exact/verify_exact.py n297.minpoly.json   # VALID: 1750 identities in K, 7138 strict, 42922 by discs
python3 check_field_packing.py n297.minpoly.json                              # VALID: 615 exact in K, 1204 strict (needs python-flint)
python3 controls.py <checker> n297.minpoly.json
```

Licence: CC0 1.0 (public domain dedication).
