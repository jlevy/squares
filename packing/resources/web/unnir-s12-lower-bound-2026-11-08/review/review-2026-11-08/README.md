# Stage 4 Review Programs and Receipts: #924, s(12) ≥ 9929/2500

The programs and receipts of the stage 4 mathematical review of jlevy/squares#924
(lane L58): unnir’s (Numaro) certificate for $s(12) \ge 9929/2500$, packet
[unnir/s12-lower-bound-3.9716](https://github.com/unnir/s12-lower-bound-3.9716) at
`064c2955670765321aaf1c0a2d5c778949daab6b`.
The review is
[review-2026-11-08-s12-unnir-3.9716.md](../../../../../../docs/project/reviews/review-2026-11-08-s12-unnir-3.9716.md).

Every program here was written by the review lane: Claude (Anthropic), tier
`tbd-strong-max`, maximum reasoning, prompted separately from the producer and from the
replay lane. They import nothing from this repository or from the producer’s packet. They
ran under CPython 3.14.7 (`uv run --no-project --python 3.14.7 --with numpy==2.3.3 python -I`)
on a shared four-core host at `nice -n 19`, at most two processes at once.
Arithmetic is exact (`int` and `fractions.Fraction`). numpy 2.3.3 `int64` arrays hold
only the integer weight counts of the sweep, whose largest value is the total
119787760.

`CERT` below is the certificate `certificate/s12_lower_3.9716.txt` of the pinned packet,
SHA-256 `833b76a179a420a40775cc76305ec9ffb7f6ea27472e587958c234c4c4712cbd`.

## Programs

| Program | What it does | What it read | Decides |
| --- | --- | --- | --- |
| `programs/premises.py` | Parses the certificate strictly, line by line, and as whitespace tokens; checks the digest, count, distinctness, positivity, containment, D4 invariance of the weighted multiset, the side, the total and the margin below n | The certificate | The premises, not coverage |
| `programs/net_coverage.py` | Finds, exactly, the bins of $\theta_k = 2\arctan(k/N)$ that cover $[0°, 45°]$, and checks that the last bin’s overshoot reflects into itself | Nothing | Net coverage |
| `programs/decide_bins.py` | The decider: for an angle bin, a core square at the bin’s mid-tangent angle with a rigorous rational shrink, its exact minimum capture over the bin’s whole centre domain by a strip sweep over the open cells of the box arrangement, subdivision of the bin on failure, and an exact-angle mode (no shrink) whose value below W would be a counterexample. The module docstring gives the proof | The mathematics, the certificate format, the producer’s README and logs; **not** the producer’s checkers, whose sources were read only after this file’s digest was recorded (`out/digests-before-reading-producer-code.txt`) | Coverage of each bin it is given |
| `programs/run_bins.py` | Driver for `decide_bins.py`: a list or range of bins, sharded, one JSON line per bin, resumable | — | Plumbing |
| `programs/test_decider.py` | Differential test: the sweep’s minimum against a brute-force enumeration of every open cell (separating-axis domain test, direct counting) on random small instances | — | Tests the sweep |
| `programs/mutation_check.py` | Shows the differential test catches one-unit errors in the half-side or the domain | — | Tests the test |
| `programs/controls.py` | On the real certificate: removes a captured orbit at a tight minimum (must refuse), enlarges the side by $1/D$, and emulates the producer’s core (endpoint reference, $\sigma_k$ and the centre box rounded down to $10^{-6}$) with this program’s own sweep | The producer’s Rust source, for the emulation (written after the freeze) | Controls; the emulation decides nothing about the bound |
| `programs/compact_sweep.py` | Writes the complete sweep’s per-bin table and summary from the shard files | — | Nothing; plumbing |
| `programs/emulate_band.py` | Daniel’s core over a range of bins, by `controls.py`’s emulation | As `controls.py` | Nothing about the bound |
| `programs/lineage.py` | Compares the point set with `T-095`’s, dilated to the new side | `T-095`’s certificate, as retained in this repository | Nothing; credit and significance only |
| `programs/summarize.py` | Summarizes the per-bin receipts | — | Nothing |
| `programs/sample-bins.txt` | The 170 sampled bins, chosen before any result | — | — |

## How to Run

From the repository root, with `PY` = `~/.local/bin/uv run --no-project --python 3.14.7 --with numpy==2.3.3 python -I`
and `P` this folder’s `programs/`:

```bash
PY P/premises.py CERT 12 833b76a179a420a40775cc76305ec9ffb7f6ea27472e587958c234c4c4712cbd
PY P/net_coverage.py 96000
PY P/test_decider.py 2000 7
PY P/mutation_check.py
PY P/run_bins.py CERT 96000 sample.jsonl --bins-file P/sample-bins.txt --exact-angles
PY P/run_bins.py CERT 96000 full-shard0.jsonl --range 0 39764 --shard 0 --shards 2
PY P/run_bins.py CERT 96000 full-shard1.jsonl --range 0 39764 --shard 1 --shards 2
PY P/summarize.py 9985226 full-shard0.jsonl full-shard1.jsonl
PY P/compact_sweep.py 9985226 39765 full-sweep-margins.tsv full-sweep-summary.json full-shard0.jsonl full-shard1.jsonl
PY P/controls.py CERT
PY P/emulate_band.py CERT 39500 39600
PY P/lineage.py CERT packing/resources/web/squarepacker-s12-lower-bound-2026-10-05/s12-lower-bound/s12_lower_3.9715.txt.gz
```

## What They Printed

- `premises.py`: `"ok": true`. Highlights:
  - side `9929/2500`, total `119787760/9985226`, margin `34952/9985226`;
  - D4 invariance under all 8 maps, orbit census `{4: 23, 8: 613}`;
  - every weight positive, 1,976 of weight 1;
  - no point on the container’s boundary.

  Receipt: `out/premises-receipt.json`.
- `net_coverage.py 96000`: the first k with θ_k ≥ 45° is 39765, so bins 0 to 39764
  cover [0°, 45°]. Exact differences: (39764 + N)² − 2N² = −136304 and
  (39765 + N)² − 2N² = 135225. The last bin’s two angles sum to less than 90°.
  Receipt: `out/net-coverage-receipt.json`.
- `test_decider.py 2000 7`: `cases=2000 mismatches=0`.
- `mutation_check.py`: one-unit mutants caught in 7, 7, 4 and 2 of 600 instances.
- `run_bins.py … --bins-file sample-bins.txt --exact-angles`: all 170 bins decided, none
  subdivided, 159.5 CPU-s. At the 510 exact angles, none is below W and 38 are exactly
  W. Bins 39532 to 39545 are at W under the core; bins 39520 to 39531 are at W + 1.
  Receipt: `out/sample.jsonl`, one line per bin with every node of its decision and the
  minimising centre.
- `controls.py`:
  - (a) with the orbit of (6281612, 7246143), weight 136132, removed, bin 39535 is
    refused (minimum 9607982) and the exact-angle counterexample is confirmed by brute
    force;
  - (b) side + 1/D leaves the band’s margins at 1, 1, 0, 0 and 0;
  - (c) Daniel’s core, emulated, is at W + 1 for bins 39518 to 39530 and at exactly W at
    39531 and 39532, with centre (1.4868216, 1.2193083) at 39531.

  Receipt: `out/controls-receipt.json`.
- `run_bins.py … --range 0 39764`, two shards, then `compact_sweep.py`:
  - all 39,765 bins present and decided, none subdivided, 9,494.1 CPU-s;
  - margin 0 (core minimum exactly W) at the 24 bins 39532 to 39555;
  - margin 1 at 55 bins: 39511 to 39531, 39556 to 39570, and 39629 to 39647;
  - every other bin at least 2702/W above W.

  Receipts: `out/full-sweep-margins.tsv.gz` and `out/full-sweep-summary.json`.
- `emulate_band.py CERT 39500 39600`: Daniel’s core is at exactly W at the 26 bins 39531
  to 39556 and at W + 1 at 39516 to 39530 and 39557 to 39572. Receipt:
  `out/emulate-band.json`.
- `lineage.py`: every one of `T-095`’s 1,736 points has a point of the new certificate
  within one coordinate unit of its image under the dilation 39716/39715. The other
  3,260 points are new. The kept points carry 59.1 % of the new total weight, and the
  row of 112 points at x = 3999969 is Daniel’s row at (141/560)·s. Receipt:
  `out/lineage-receipt.json`.

## Receipts

| File | What it holds |
| --- | --- |
| `out/findings-blind.md` | The blind findings, frozen before any comparison material was read |
| `out/freeze.txt` | The freeze time and the blind file’s SHA-256 |
| `out/digests-before-reading-producer-code.txt` | The digests of the decider and its tests, recorded at 15:08:21Z before the producer’s checkers were read |
| `out/premises-receipt.json` | `premises.py`’s output |
| `out/net-coverage-receipt.json` | `net_coverage.py`’s output |
| `out/sample.jsonl` | The 170 sampled bins, with exact-angle minima |
| `out/controls-receipt.json` | `controls.py`’s output |
| `out/full-sweep-margins.tsv.gz` | The complete sweep, one line per bin: bin, the core minimum minus W, decision nodes, decided (deterministic `gzip -9n`) |
| `out/full-sweep-summary.json` | Its summary, with the minimising centres of the tight bins and the SHA-256 of the two shard files of JSON lines, which are not retained (OR-18) and which a rerun regenerates apart from timings |
| `out/emulate-band.json` | Daniel’s core over bins 39500 to 39600, by this lane’s sweep |
| `out/lineage-receipt.json` | `lineage.py`’s output |
| `out/sha256sums.txt` | The SHA-256 of every file in `programs/` and `out/` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
