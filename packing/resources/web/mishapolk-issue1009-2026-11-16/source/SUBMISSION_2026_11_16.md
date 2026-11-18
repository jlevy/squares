# Verified Square-Packing Upper Bounds (2026-11-16)

**Credit:** Mykhailo Polkovskyi ([Mishapolk](https://github.com/Mishapolk))

Exact rational `.cert` certificates (`certificates/0000-0999/`) and `Witness/v2` four-corner files (`witnesses/2026-11-16/`) for $n \in \{147, 156, 180, 210, 260, 262, 268, 270, 272, 292, 295, 299, 307\}$.

## Verification
```bash
python3 verify_bound_certificate.py --strict certificates/0000-0999/n{147,156,180,210,260,262,268,270,272,292,295,299,307}.cert
python3 verify_area_exact.py --strict certificates/0000-0999/n{147,156,180,210,260,262,268,270,272,292,295,299,307}.cert
python3 verify_algebraic_bounds.py
```
