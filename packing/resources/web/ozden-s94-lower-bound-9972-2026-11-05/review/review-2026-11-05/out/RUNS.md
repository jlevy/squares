# Runs of the think-xzxd Review

Every run used CPython 3.14.7 from `packing/.venv`
(`uv run --frozen --all-extras --group
dev`), with gmpy2 2.3.1 and NumPy 2.5.2, through `programs/run.sh`: isolated mode
(`-I -B`), `nice -n 19`, at most two processes at a time, on a shared four-core host,
2026-11-05 between 08:44Z and 09:55Z. `CERT` is the packet’s
`source/certificate/n94-L9972.json.gz`, SHA-256
`f59d4c9562d7246f41c8c389a5bc118da9cf268a794e6416d146a195fb03360c`.

## The Runs

| Program and arguments | Receipt | What it printed | CPU s |
| --- | --- | --- | ---: |
| `premises.py PACKET HOSONO_GZ OUT` | `premises.json`, `premises.log` | `ALL_CHECKS_HOLD`; N0 (b) $99498934887/99500000000$, (c) $1649/16000000$, (e) $14327846598855339/14327999975125000$; 6,720 expanded rectangles; 20 shared nodes, 4,952 new; growth $11/9972$ at the axis, $1.934 \times 10^{-4}$ to $1.516 \times 10^{-3}$; regenerated text and gzip byte-identical | 0.4 |
| `axis_exact.py CERT OUT` | `axis-r0.json`, `axis-r0.log` | 5,431 events a side, 29,495,761 vertices; minimum $1.003086850384903$ at $(6.4991051\ldots, 9.472)$, on the wall edge; mutant $0.993055981881054$ | 98.6 |
| `axis_exact.py CERT OUT 471177/49750` | `axis-r0-hosono-domain.json`, `.log` | Hosono’s domain: 5,426 events a side (5,425² cells); minimum $1.0031817020942837$ on its wall edge | 106.2 |
| `validate_bnb.py CERT OUT 1 3663 1198 4971` | `validate-bnb.json`, `.log` | `ALL_HOLD`: estimate within $7.5 \times 10^{-13}$ of exact; bound never above exact; 192/192 gradient enclosures contain the exact difference quotient; no misclassification | 3.5 |
| `sample.sh CERT sample/ R…` (two lanes), and `bnb.py CERT 3663 sample/bnb-r3663.json` | `sample/bnb-rR.json`, `.log`, `lane1.txt`, `lane2.txt` | 25 oblique directions, all `verified`; 83,847 to 104,121 nodes; largest error budget $1.09 \times 10^{-9}$ | 1,908 |
| `controls.sh CERT controls/` | `controls/*.json`, `.log`, `controls.txt` | the mutant stops as a counterexample candidate at 1198 and 3663; threshold $1.0012$ fails and $1.0010$ verifies at 1198; $1.0035$ verifies at 3663; the crate’s least-bound box at 3663 decided exactly in one box, bound $1.0300449806526146$, centre $1.0336467437483632$ | 202 |
| `bands_regions.py CERT 249 2490 4731` and `bands_regions.py CERT --width 11/9950 1 2 20 132`, then `bands.sh` | `bands/` | 14 strips, all `verified`; least centre values 1.0064 to 1.0081 at the shared nodes, 1.0031 to 1.0073 at the near-axis new nodes | 8 |
| `poses_exact.py PACKET sample/ receipts-read.json OUT` | `poses-exact.json`, `.log` | `ALL_HOLD`: both control witnesses equal their stated exact captures; every sampled direction’s least centre $\ge 1.00113$ exactly with its mutant below 1; 13 crate least-bound centres capture 1.0073 to 1.0986 | 0.5 |
| `read_receipts.py PACKET premises.json OUT` | `receipts-read.json` | `ALL_CHECKS_HOLD`; repeated directions agree 67/67 in bound and 66/66 in nodes; E’s scope as in F3 | 0.4 |
| `tabulate.py PACKET out/` | `sample-table.md`, `sample-summary.json`, `tabulate.log` | the table in the review | 0.1 |
| `explore_measure.py CERT`, `explore_measure2.py CERT` | printed | 853 rows valid as `[x1, y1, x2, y2]`, 785 as `[x1, x2, y1, y2]`; 6,720 expanded rectangles, 2,512 thinner than 0.01, densities up to 39,419.6 | 2 |
| `explore_landscape.py CERT 3663 60 explore-3663.npy` | `explore-3663.npy`, printed | a $60 \times 60$ grid at 3663: least $1.006068$, at the wall edge | 21 |
| `explore_minima.py CERT R 80 40` at 3663 and 1198 | printed | float local minima near $1.0035$ to $1.0037$: a coarse look that the deciders replaced | 7 |
| `peek_index.py INDEX` | printed | the index’s fields | 0.1 |

In all, about 42 CPU-minutes.
That includes rerunning `axis-r0`, `sample/bnb-r3663`, `validate-bnb`, `premises`,
`poses-exact` and the table once at the programs’ final bytes (about 176 s); each rerun
decided exactly what its first run did.

## Records Kept Beside the Runs

- `unread-import-lane-receipts.sha256`: the SHA-256 of the import lane’s three receipts,
  taken before any was read.
- `freeze.txt` and `review-at-freeze.md`: the time and digest of the review when its
  findings were frozen, and that state of the document, before the review of #890’s
  certificate and those receipts were read.

## Program Digests

The receipts above were written by the programs at these bytes.
The two lanes started before `run.sh` gained `-B`, which changes only bytecode caching.
`bands_regions.py` gained `--width` after the near-axis region file was first written by
an inline expression; at these bytes it writes both region files byte for byte.

See `sha256sums.txt` in this directory.
