# k² − 5 unit squares need a square of side k for every k ≥ 7

**Claim.** For every integer k ≥ 7, k² − 5 unit squares (free rotation, pairwise disjoint interiors) do not fit in
a square of side less than k. The k × k grid holds k², so **s(k² − 5) = k**. (For k = 3, 4 it is false: s(4) = 2 and
s(11) < 3.88; k = 5, 6 are open.)

Authors: **Mohsen Khalili** and **Sara Gharabaghi** (independent researchers), with AI assistance (see the paper's
acknowledgments). Computer-assisted. Not yet peer reviewed.

Paper: [`paper/k2m5.pdf`](paper/k2m5.pdf) (14 pages, 7 figures). Technical report on the Tight-Tile Lemma:
[`paper/tight_tile_report.pdf`](paper/tight_tile_report.pdf).

## How the proof is put together

| k | n = k² − 5 | proof of s(n) ≥ k | record |
|---|---|---|---|
| 7 | 44 | our weighted cover (s44-equals-7, DOI 10.5281/zenodo.23769766) | T-252, confirmed |
| 8 | 59 | Hosono's weighted cover | T-066, confirmed |
| 9 | 76 | Greff's weighted cover | T-184, confirmed |
| ≥ 10 | 95, 116, … | **this release: one family of measures μ_k** | — |

For k ≥ 10 the paper proves:

1. **Mass** (Lemma 6): μ_k has total k² − 4D with D = 1340566927759/10¹² > 5/4, so the total is below k² − 5.
2. **Locality** (Lemma 7): every unit square in [0, k]² has the mass of a unit square in [0, 11]² (integer
   translation). Also formalized in Lean (`lean/`): `Valid11 → ∀ k ≥ 10, s(k² − 5) = k`.
3. **Validity of the 11 × 11 board** (Theorem 10): every closed unit square in [0, 11]² has μ₁₁-mass ≥ 1. Four parts:

| part | how | result |
|---|---|---|
| untilted squares | Lemma Z (exact), an independent exact evaluation, `zmx2 cert0` | min exactly 1; 2,500 roots verified |
| tilted, general position | `zmx2` (E. Daniel), first-order, D4-reduced, depth 40 | 12,024 of 12,100 roots certified |
| root 9632 | `zmx2` + `qx2_zm.py` (E. Daniel, exact rationals) | nothing left uncertified (`verification/r9632/check_9632.py`) |
| 75 tight-tile roots | **Tight-Tile Lemma** (`tight_tile/`, exact + outward-rounded intervals) and an exact coverage check | 323/323 jobs certified (≈ 2.75 M cells); 1,255,023 leftover boxes, all covered |

## Checking it

```
bash verification/verify.sh          # a few minutes: exact bookkeeping + exact audits of every recorded run
bash verification/verify.sh --full   # re-runs everything from scratch (hours for zmx2, CPU-days for the tight tiles)
```

Expected final lines of the fast run: `SANITY-OK`, `LOCALITY OK`, `ZMX2-AUDIT-OK`, `ROOT-9632-CLOSED`,
`jobs ALL-OK 308 …`, `COVERAGE-OK`. Requirements: Python 3 (standard library; `numpy` for the stress test, `scipy`
and `matplotlib` only to rerun the tight-tile jobs or redraw the board figure); `--full` also needs git and Rust.

## Folder layout

| path | contents |
|---|---|
| `paper/` | the paper and the Tight-Tile technical report (LaTeX + PDF); `figures/` holds the TikZ sources and the script that draws the board figure from the certificate |
| `certificate/` | the 11 × 11 board `sol_exact_box11.txt` (Daniel's mixed format), the family `sol_exact_family.txt`, the exact solution `sol_exact.json`, `SHA256SUMS` |
| `verification/` | `verify.sh`; exact sanity, locality, audit and stress scripts; built boards k = 10, 12, 13, 20; zmx2 logs; root 9632 files; checker controls |
| `tight_tile/` | the Tight-Tile checker `ttbox` (Python), job lists, all job outputs, the zmx2 dumps of the 75 roots (`cov.tar.xz`), the coverage check, and the controls |
| `lean/` | the Lean 4 reduction `k2m5_of_valid11` for this board (build instructions inside) |
| `search/` | how the measure was found (not part of the proof): our patches to Daniel's LP and projection tools, and the drivers |
| `docs/` | `CHECKING.md` (every claim, how it was checked, controls), `ITERATIONS.md` (search log), `BASECASES.md` |
| `SHA256SUMS_ALL` | checksums of every file in the release |

## Checkers and pins

`zmx2` and `qx2_zm.py` are Evan Daniel's, from
[evand/square-packing@659ee62](https://github.com/evand/square-packing/tree/659ee62e4a9d39542a1146e8b011cc3ab6407ede),
used unmodified except a one-line output patch (`verification/zmx2_print_all.patch`) that prints all uncertified
boxes. `qx2_zm.py` prints `zeromargin.py … DIFFERS FROM PINNED`: our `zeromargin.py` (sha256 `3cb95fb7…`) is the one
in Daniel's repository at the pin; it differs from the older pin inside `zm_mixed.py` only by two added safety
guards. Everything in `tight_tile/` and `verification/*.py` is ours.

## License

Code: MIT. Text and data: CC BY 4.0. (See `LICENSE`.)
