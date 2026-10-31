# zm_mixed.py logs (s(44) = 7)

Checker: `zm_mixed.py` (E. Daniel), evand/square-packing@659ee62, unmodified; input sha256 c9fde0f1…cae0.

- `mac/colNN.*` — the D4 sweep, all 9,800 root boxes, split by 35 x-columns (`--depth 24`), Apple M1 Pro.
  1,265 boxes in 27 roots were uncertified at depth 24 (`mac/uncert_roots.txt`).
- `mac/deep.*` — root cx[1/2,3/5] cy[7/5,3/2] u<1/16 re-swept at `--depth 30`: 0 uncertified.
- `mac/dNN.*` — the 24 roots listed in `mac/deep_jobs.txt`, each re-swept in full at `--depth 30`: 0 uncertified.
- `cloud_deep/{a,b}.*` — the two col34 roots (cx[17/5,7/2] cy[6/5,13/10], u in [1/4,5/16] and [5/16,3/8])
  re-swept at `--depth 30`: 0 uncertified.

Together: every root is certified (27 of them at depth 30). `.jsonl` files are the per-root resume records;
`_manifest.json` files hold the hashes and settings of each run. The large leaf dumps are not included.
