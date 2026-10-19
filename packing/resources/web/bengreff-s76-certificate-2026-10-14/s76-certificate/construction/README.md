# Construction scripts (research code; not needed to check the proof)

**Input:** wand125's `n59_mixed_cover_8.txt`, the certified s(59) = 8 cover, with sha256
`6f4d2b64f9a88ae49546f05fa28752382f9ebfa8b7f8b6e6c6f1a8e693177e19`. It is in wand125/square-packing,
`problems/square-lower-bounds/certificates/k2m5_n59_L8/`.

| file | role |
|---|---|
| `cover.py` | mixed-cover loader, band insertion (cut at 4, shift by 1), float64 capture |
| `lp.py` | candidate lattice, D4 orbits, per-element capture, random descent |
| `run14.py` | the final LP loop |
| `export_cover.py` | writes the exact cover (D = 8000, W = 4·10⁸) from an LP solution |
| `exclude_points.txt` | the excluded point candidates (3-4-5 coincidences) |

`run14.py` is the final LP loop:

- HiGHS IPM on an active set of the rows;
- D4-orbit variables, with free points capped at 0.004;
- row margin 0.005, and 0.012 at the bottom-wall tile germs;
- oracle each round: an exact export, a zmx2 D4 sweep, then dense float64 scans of every zmx2-failing root (uniform samples, wall contact, small angles, and a structured tile-germ grid).

It ran as `TAU=0.0005 MU_W=0.012 python run14.py 0.05 30 0.005 0.004 RESUME.npz`. Its earlier
versions (run3–run13) differ in oracle and row handling only.

It also needs `gpu_cuda.py` (CuPy screening) and Evan Daniel's zmx2 binary on the path used in
the script.
