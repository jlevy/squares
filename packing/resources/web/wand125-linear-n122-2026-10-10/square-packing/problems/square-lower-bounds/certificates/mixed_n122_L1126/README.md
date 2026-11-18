# s(122) >= 563/50 = 11.26

A certificate proving that 122 unit squares do not fit in a square of side `L = 563/50 = 11.26`.
This exceeds Green's reported bound for `k = 11` (Friedman DS7, Theorem 9),
`G_11 = 2√2 − 1 + (1100 + 10√22)/122 = 11.2292…`, by more than `0.0307191`
(compared exactly with integer square-root bounds; see `completion-audit.json`).
Since the total mass is below 122, the same certificate gives `s(N) >= 11.26` for every `N >= 122`
(it improves on `√N` for `N = 122, …, 126`).

The measure is linear: 502 point masses, 1268 segments of uniform linear density and 3 rectangles, with exact rational
geometry and masses, D4-symmetric. The total mass is `12199999/100000 = 121.99999 < 122`. The setting is that of
[`mixed_n101_L1028`](../mixed_n101_L1028/README.md): core side `B = 9977/10000`, and 201 half-angle net nodes with step
`83/40000`.

At every net angle, every closed core of side `B` at that angle has measure `>= 1`. This was checked with the verifier in
`code/` (`unified_linear_verify.cpp` and its Python driver), which proves the bound over every centre domain with
outward-rounded interval arithmetic. It is the verifier of `mixed_n101_L1028` (the same source, SHA-256
`0249726ab1e67dc481e0c53f43b524902a48f95d051b1b08865a3cf3ef89a06d`).

The initial measure came from a floating-point LP over points and segments on a lattice at multiples of `B` from the
walls, scaled to the target mass, and was then repaired against exact counterexamples on the full net and proved at all
201 angles.

## Argument

D4 symmetry reduces orientations to `[0, π/4]`, and `B(1 + 83/40000) < 1`. So every unit square, at any orientation,
contains a closed core of side `B` at a net angle, strictly in its interior. Each such core has measure `>= 1`. Cores
chosen inside the squares of a packing are disjoint, so 122 squares would need total mass `>= 122`.

## Files

- `candidate.json`: the rational measure (points, segments and rectangles with their weights).
- `certificate.json`: the per-angle records, including every input's SHA-256.
- `manifest.json`: the angle net.
- `completion-audit.json`: the audit of the candidate, the mass, the angle set, the replay states, the source hashes
  and the exact comparison with `G_11`.
- `code/`: the verifier (Python 3 and a C++17 compiler) and `replay_linear_bundle.py`.
- `n122-L11.26-proof-bundle.tar.gz`: the complete bundle, 810 entries including every angle's input and result
  (SHA-256 `3986d902d11ba2c91a8e56c9b18bb07bf8876c24451587480b2a86c4ba9a55d0`).

## Reproduce

```sh
tar xzf n122-L11.26-proof-bundle.tar.gz
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/replay_linear_bundle.py n122-L11.26-proof-bundle --workers 3
```

You need Python 3 with numpy, scipy, numba and highspy, and a C++17 compiler. The replay regenerates all 201 inputs
from the candidate, re-runs the verifier on each, and requires every record to equal the stored one. It ends with
`ALL_LINEAR_ANGLES_REPLAYED_MATCHING_CERTIFICATE`.

Before publication the full replay was run from this tarball on a fresh Ubuntu 24.04 machine with only the
requirements above installed (`--workers 3`). It ended with `ALL_LINEAR_ANGLES_REPLAYED_MATCHING_CERTIFICATE` for
`n = 122`, `L = 563/50`, total mass `12199999/100000` and candidate digest
`c91a750977764335d3668599bf7e599539b30f7c81969372fc27ad90561e9ed4`, in 7 h 41 min of wall time. The
replay re-executes the same outward-rounded implementation; it is not an independent second algorithm or a
proof-assistant formalization.
