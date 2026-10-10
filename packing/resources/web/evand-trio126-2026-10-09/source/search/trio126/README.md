# The 126 trio, reconstructed from a picture (2026-10-08)

Three packings of 126 unit squares, recovered from `~/math/square-packing/126.jpg` (one image, three panels at the same
scale; not in the repo) and polished to exact local minima.  They are other people's packings: **Ryan Xu**
(s = 11.742641, 45° lattice diamond) and **Nate Chaoweeraprasit, SQUISH phases 14 and 10** (11.763736 diagonal
staircase band; 11.773304, ~30° lattice block).  No claim here: register status not checked (see TODO: Xu's value is
below the register, possibly pending PR #442).  Use: seeds for the 126-trio generators (TODO, Packings).

| file | panel | exact S (exactsolve) | tilted squares |
|---|---|---|---|
| `n126_xu` | Ryan Xu | 11.742640687119285… = 15/2 + 3√2 | 36 at 45°, 2 others |
| `n126_ph14` | SQUISH ph14 | 11.763736443985669… | 16 (8 at ≈ 33°, 8 at ≈ 55°) |
| `n126_ph10` | SQUISH ph10 | 11.773303606603240… | ~50 at 60–68°, a few near-axis |

Each agrees with the side printed under its panel to all 6 printed decimals.  Since a picture only fixes the loaded
structure, a reconstruction may differ from the original in rattlers.

Per packing: `.txt` (f64, `fq` output), `.exact.txt` (exactsolve, 70 digits), `.cert` (rational certificate).
exactsolve says each is a local minimum of S (strict modulo exact flat motions; jammed in every corner-corner branch).

    python3 ../exact/verify_cert.py  n126_xu.cert     # VALID: s(126) <= S
    python3 ../exact/verify_cert2.py n126_xu.cert     # independent check (polygon intersection)
    sha256sum -c SHA256SUMS

## How they were made
1. `python3 ../packer/img2packing.py 126.jpg X0 X1 150 1050 SIDE out.txt` with the panel boxes 50–950 (Xu),
   1000–1880 (ph14), 1900–2800 (ph10) and SIDE = the printed side: 126 blobs each, centres ~0.02 off.
2. `fq quench --loosen L` (Xu: 1.0; ph14: 1.05; ph10: 1.02, then a second quench at 1.0 with `--stag-tol 1e-12`:
   at the first output exactsolve found no smooth equilibrium, residual 1.1e-7, i.e. not converged far enough).
3. `exact/exactsolve.py` (ph10 with `--tol 1e-7`), then both verifiers.

2×2 split of ph14 (s = 23.5275 for 504): not a local minimum, first-order descent even with all rotations locked
(`../TILINGS.md` § Split rigidity).
