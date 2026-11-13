# Method for n = 132 and n = 157

This folder holds the code that produced the packings in [n132](../n132/) and [n157](../n157/), and the high-precision solutions behind the two certificates.

## Steps

1. Growth step (`grow.py`, `surgery.py`). The packing is cut along one vertical and one horizontal line. The parts are moved about 1.15 apart. Every square in the layer next to a cut is copied once across it: axis-aligned squares by one unit, tilted squares by 1/cos(theta) along the normal of the cut. A copy is dropped when it overlaps another square by more than 0.15.
2. Optimization (`slp.py`, `nlp.py`). Remaining overlaps are removed with linear programs at a fixed side. All squares are then optimized together with IPOPT (through CasADi). The model minimizes the side under the wall constraints and one separating-axis constraint per corner of each pair of nearby squares. The choice of axes is renewed between solves.
3. High-precision solution (`newton.py`). The contact equations of the result are solved with Newton's method at 900 bits (python-flint). One equation is written for each corner of a square within 1e-6 of the edge line of a neighbouring square, on an axis that separates the two squares, and one for each corner within 1e-6 of a wall. This gives 1407 equations for n = 132 and 2024 for n = 157.
4. Certificate (`package.py`, `mkcert.py`). The solution is scaled by 1 + 1e-60 and shifted by 1e-60, written as exact rationals and checked in rational arithmetic.

## Reproduction

The seed is the packing of 109 squares in `best_fit_101_500.csv` of `Samanyu-dev/squares_in_squares` at commit `53551d7`. That file is not part of this repository.

    python grow.py best_fit_101_500.csv 3.48 8.61 n132.npz 109
    python grow.py n132.npz 9.71 3.33 n157.npz
    python newton.py n132.npz . n132
    python newton.py n157.npz . n157
    python package.py n132 . out132
    python package.py n157 . out157

The first two commands print the sides 11.976048386602 and 12.993302615406. The last two commands write `n132_exact.json` and `n157_exact.json`, which are byte for byte equal to the files in [n132](../n132/) and [n157](../n157/).

Requirements: Python 3.10 or later with numpy, scipy, casadi, python-flint, mpmath and matplotlib. The two checks below also need shapely.

## Further checks

- `check_binary64.py`: separating-axis test over all pairs in binary64. It reports a least separation of about -2e-15 for n = 132 and -4e-15 for n = 157, which is rounding error of binary64 on gaps of 1e-60.
- `check_shapely.py`: area of the union of the squares with Shapely. It reports 132.0000000000 and 157.0000000000.

Both scripts read the exact file, for example `python check_binary64.py ../n132/n132_exact.json`. They were written for this folder and repeat the two checks reported with the packings. The exact checker is `verify_exact.py` in each packing folder.

## Files

- `n132_solution_250_digits.txt`, `n157_solution_250_digits.txt`: the solutions of the contact equations. The first line is the side. Each further line gives x, y and the angle in radians of one square.
- `grow.py`, `surgery.py`: growth step.
- `slp.py`, `nlp.py`: optimization.
- `newton.py`, `mkcert.py`, `package.py`: high-precision solution and certificate.
- `check_binary64.py`, `check_shapely.py`: further checks.

The perturbation trials and the force-balance check described in the two packing folders are outside this folder.

## AI assistance

This code was written with Claude Fable 5.2 (Anthropic) under the direction of Joost de Winter.
