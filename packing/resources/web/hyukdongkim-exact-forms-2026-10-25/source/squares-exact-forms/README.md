# Exact sides of the record packings for n = 88, 126, 172, 199, 263

`exact_forms.json` gives, for each count, the minimal polynomial over Q (coefficients from
the highest degree down) and the record side to 100 digits.

## Rerun the check

```
git clone https://github.com/evand/square-packing
git -C square-packing checkout 659ee62e4a9d39542a1146e8b011cc3ab6407ede
pip install numpy scipy sympy python-flint
python verify_exact_forms.py square-packing/site/www/data/p 400     # about 2.5 min
python verify_exact_forms.py square-packing/site/www/data/p 3000    # about 25 min
```

For each count the script:
1. reads the record packing from `best-<n>.json`;
2. polishes it to a local optimum (LP at fixed angles, trust-region SLP on the angles);
3. extracts the active contacts;
4. solves the KKT system to the requested number of digits;
5. checks that the claimed polynomial vanishes at the solved side, that the polynomial is
   irreducible, and that the matching exact real root agrees with the solved side.

It prints `ALL OK` when every check passes.

## Files

- `verify_exact_forms.py`: the check above.
- `lppolish.py`: LP/SLP polisher, separating-axis geometry and feasibility check.
- `exactform.py`: active-contact extraction and the contact equations.
- `kkt.py`: values, gradients and analytic second derivatives of the contact equations.
- `kkt_fast.py`: mixed-precision KKT solver.
- `exact_forms.json`: the claimed polynomials and values.

Tested with Python 3.13, numpy 2.5, scipy 1.18, sympy, python-flint 0.9.0.
