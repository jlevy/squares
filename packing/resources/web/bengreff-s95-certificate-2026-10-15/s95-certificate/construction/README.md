# Construction scripts (research code; not needed to check the proof)

**Input:** wand125's `n59_mixed_cover_8.txt`, the certified s(59) = 8 cover, with sha256
`6f4d2b64f9a88ae49546f05fa28752382f9ebfa8b7f8b6e6c6f1a8e693177e19`. It is in wand125/square-packing,
`problems/square-lower-bounds/certificates/k2m5_n59_L8/`.

| file | role |
|---|---|
| `cover.py` | mixed-cover loader, band insertion (cut at 4, shift by K - 8), float64 capture |
| `lp.py` | candidate lattice, D4 orbits, per-element capture, random descent (side K from env `SQK`) |
| `run18.py` | the cutting-plane loop |
| `gpu_ipm.py` | mixed-precision interior-point LP solver on the GPU (CuPy) |
| `gpu_cuda.py` | unit-square capture on the GPU: float32 screening, float64 scans |
| `export_cover.py` | writes the exact cover (D = 8000, W = 4·10⁸) from an LP solution |
| `exclude_points.txt` | the excluded point candidates (73 points, 70 orbits) |
| `find_coinc.py`, `find_near_edge.py` | locate atoms on the edges of zm_mixed's degenerate poses |

The loop, each round:

1. LP solve on an active set (rows with slack below `TAU`), with `gpu_ipm` and HiGHS as fallback.
2. A 2M-pose GPU screen.
3. Once the screen has at most 2,000 violators: an exact export, a zmx2 D4 sweep, then dense
   float64 GPU scans of every zmx2-failing root.

It stops when the screen minimum and all scans stay ≥ 1 + MU/2.

How the final cover was made:

1. The first run used `run17.py`, which is `run18.py` with the dense scans on the CPU:
   `SQK=10 CAND_CAP=100000 TAU=0.0005 MU_W=0.012 python run17.py 0.05 40 0.006 0.004 resume.npz`.
   It resumed from an earlier HiGHS-era state seeded with the s(76) rows, mapped to side 10 and
   copied into the new centre band.
2. zm_mixed found 3 degenerate sub-roots in that cover.
3. Their 42 atoms were added to `exclude_points.txt`.
4. `run18.py`, with the same settings and `ZCAP=20000`, re-solved and gave `s95_cover_v2.txt`.
