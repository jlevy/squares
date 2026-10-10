# Packing k²−c unit squares: an upper bound of order k^{3/8} for the deficiency

Preprint, programs and data by Sungjoon Ryu (2026). Version 1.0.

**Status: not refereed.** The paper has not been refereed. It was written with AI assistance and has so far been checked only by AI-based reviews and by computer programs, some of them independent re-implementations (see "Verification status" below). No human expert has reviewed it.

**Setting.** For n ≥ 1 let s(n) be the side of the smallest square that contains n unit squares with pairwise disjoint interiors, and for an integer k ≥ 2 let c\*(k) be the largest integer c with s(k²−c) = k (the *deficiency*: removing up to c\*(k) squares from the k×k grid does not allow a smaller container).

## Main results

| Statement | In the paper | Grade |
|---|---|---|
| c\*(k) < (32/5)·(5/3)^{3/8}·15.54^{5/8}·k^{3/8} + 2·10^{−5} < 43.06·k^{3/8} + 2·10^{−5} for every integer k ≥ 4·10²⁶ | Theorem 1.1 | proved, with computer-assisted constants (certified in interval arithmetic); the newest part; the asymptotic regime cannot be tested by explicit computation |
| c\*(k) < (20/3)·(3/2)^{2/5}·5.03^{3/5}·k^{2/5} + (8/3)·5.03·10^{−4/3} < 20.668·k^{2/5} + 0.623 for every integer k ≥ 16,000,000 (= 1.6·10⁷) | Theorem 1.2 | proved; constants certified in interval arithmetic |
| c\*(k) ≤ 8⌈√(k−4)⌉ − 1 < 8√(k−4) + 7 for every integer k ≥ 6 | Theorem 1.4 | proved |
| c\*(k) ≤ c − 1 for the five values of k in the table below | Theorem 1.6 | computer-assisted: structural part proved; finite data (end packings) checked in exact rational arithmetic |

**Which bound to use.** For 1.6·10⁷ ≤ k < 4·10²⁶ only the k^{2/5} theorem is proved; the closed forms of the two theorems cross at about k = 5.6·10¹². The k^{2/5} theorem is the effective bound, and the k^{3/8} theorem gives the better exponent.

Also proved: for all integers 2 ≤ b ≤ k, the explicit L-shaped packing gives c\*(k) ≤ k² − N(k,b) − 1 < 6b + 4k/b − 3 (Theorem 1.3), and this family of packings cannot give less than 8√k − 15 (Proposition 1.5).

**The idea.** The L-shaped frame has two tilted bands of width just below an integer b. Their rows are lifted, and the deficiency equals the body cost of the bands (about 4k/b) plus the uncovered areas of the four band ends (Proposition 6.3). Each end is filled by a *staircase*: columns of squares with one common small tilt, whose lowest squares are replaced by horizontal layers, so that one tilt follows the rising end of the band. One end then costs at most 5.03·b^{2/3}, and b ≈ k^{3/5} gives the exponent 2/5. In Section 8 the two walls of each end are filled by chains of staircases whose tilt is lowered slightly from block to block, so that the layers close in phase; one end then costs at most 15.54·b^{3/5} (for b ≥ 10¹⁶), and b ≈ k^{5/8} gives the exponent 3/8. These ideas are those of H. D. Bui (arXiv:2508.04603v2, Sections 3–4); the proofs in the paper are self-contained.

**Certified values (Theorem 1.6, Table 1 of the paper).** For each row, k² − c unit squares are packed in a square of side less than k; the data file lists every piece of the four band ends as exact rationals. These staircase certificates are the best values we have at these k; the k^{3/8} construction gives larger values here (for example c\*(10⁸) ≤ 44299) and wins only for very large k.

| k | b | y₀ | c = k² − N | Bound | Data file |
|---|---|---|---|---|---|
| 10⁵ | 623 | 257/4 | 1584 | c\*(10⁵) ≤ 1583 | `data/stair_k100000.json.gz` |
| 10⁶ | 2481 | 653/4 | 3973 | c\*(10⁶) ≤ 3972 | `data/stair_k1000000.json.gz` |
| 10⁷ | 9875 | 1663/4 | 10040 | c\*(10⁷) ≤ 10039 | `data/stair_k10000000.json.gz` |
| 3.825·10⁷ | 22086 | 710 | 16989 | c\*(3.825·10⁷) ≤ 16988 | `data/stair_k38250000.json.gz` |
| 10⁸ | 39314 | 1041 | 24791 | c\*(10⁸) ≤ 24790 | `data/stair_k100000000.json.gz` |

Together with the lower bound of order k^{1/3} in [T] (a preprint by the same author that has not been refereed), Theorem 1.1 gives k^{1/3} ≪ c\*(k) ≪ k^{3/8}. The true exponent of c\*(k) is open; it lies between 1/3 and 3/8.

## Contents

| Path | Content |
|---|---|
| `paper/paper.pdf`, `paper/paper.tex` | The preprint (30 pages) |
| `paper/LICENSE` | CC BY 4.0 for the paper |
| `data/stair_k*.json.gz` | The end pieces of the five certified packings of Theorem 1.6 (exact rationals, gzip-compressed JSON) |
| `code/stair_check.py` | Checker of the certified packings (does not import the generator), with 7 negative controls |
| `code/stair_dump.py` | The program that generated the data files |
| `code/const_stair.py` | Interval-arithmetic certification of the constants of Theorem 1.2 (Corollary 7.4 and Section 7.3) |
| `code/cert3e.py` | Interval-arithmetic covering of the whole range b ≥ 10¹⁶ for the constants of Theorem 1.1 (Corollary 8.3); written by an independent re-implementation |
| `code/r38.py`, `code/chk.py`, `code/run_z.py` | The wall filler of Section 8 in exact arithmetic, a generic exact checker, and an explicit validity check (m = 10⁴) |
| `code/README_code.txt` | Commands, expected outputs, times and SHA-256 of the data |
| `code/checker_outputs/` | Recorded outputs of the runs |
| `LICENSE` | MIT License for `code/` and `data/` |
| `SHA256SUMS` | SHA-256 of every file except `README.md`, `.zenodo.json` and itself |

## How to reproduce

Python 3 with `numpy` and `mpmath` (`pip install numpy mpmath`); `gmpy2` is optional and only makes the checkers faster. Run the commands from the top folder of this repository (the folder that contains `code/` and `data/`). Times are from the author's laptop.

```
python code/const_stair.py  -> last line "ALL CHECKS: True"  (about 2 s)
python code/stair_dump.py table data  # (all five rows of Table 1, about 30 s)
python code/stair_check.py data/stair_k100000.json.gz 100000
python code/stair_check.py data/stair_k100000.json.gz 100000 mutate  # (negative controls)
python code/stair_check.py data/stair_k1000000.json.gz 1000000
python code/stair_check.py data/stair_k10000000.json.gz 10000000
python code/stair_check.py data/stair_k38250000.json.gz 38250000
python code/stair_check.py data/stair_k100000000.json.gz 100000000  # (about 1 minute, 0.2 GB with Fraction)
python code/cert3e.py 160 64  -> "all_positive": true, "Psi_sup" 96.4768..., "C_E_cert" 14.9636...
python code/run_z.py 10000 1 0.5 4  # (about 10 s)  # (expected output: code/README_code.txt)
```

Details, the outputs of every program and the SHA-256 of the data files are in `code/README_code.txt`. To check the files: `sha256sum -c SHA256SUMS` (Linux, macOS) or compare with `Get-FileHash` (Windows).

## Verification status

- **AI-written.** The proofs, the text and all programs were developed with the assistance of Claude (Anthropic); the author takes full responsibility.
- **AI reviews.** The text has been reviewed only by AI systems (instances that did not write it). An earlier write-up of Sections 3–5 received an independent AI review that found no critical or major issue. An earlier write-up of the proof of Theorem 1.2 (Section 7) received two independent blank-slate AI reviews, both of which judged it correct with no critical or major issue. An earlier write-up of the proof of Theorem 1.1 (Section 8) received two independent blank-slate AI reviews with their own programs: one judged it correct after fixes, the other correct; all fixes are included. The proofs deserve priority in a human review.
- **Independent re-implementations.**
  - Theorem 1.2 relies on one evaluation in interval arithmetic, Φ(10^{−4/3}) ≤ 5.0163, done by the author's program (`const_stair.py`) and by three independent computations; the other constants were certified in the same way.
  - The author's own interval program for the constants of Theorem 1.1 used too little slack on the wall tilts; the constant C_E = 15.54 is certified by three independent full-range interval coverings (C_E ≤ 14.964, 14.963 and 14.9631; mpmath.iv twice and python-flint arb once); the first is `cert3e.py`. An independent re-implementation of the k^{3/8} construction found no counterexample. The asymptotic regime (b ≥ 10¹⁶, k ≥ 4·10²⁶) cannot be tested by explicit computation; the explicit checks test the validity of the construction at smaller sizes.
  - An independent re-implementation of the staircase construction, written from the text of the proof only (not included here), checked the end packings exactly for b up to 4·10⁵ and the full packings for k = 1.6·10⁷, 3.825·10⁷, 10⁸, 10⁹ and 3·10⁹.
  - The certified packings (Theorem 1.6) were checked by the generating program and by a checker written from a description of the construction, without reading the generating program; `stair_check.py` is adapted from that checker. All 7 deliberately corrupted versions of the data were rejected.
  - All of these programs were written by AI systems of the same family, which may share blind spots. No human has reviewed the programs.
- **Not refereed.** The paper has not been refereed. The lower-bound papers [Q] and [T] by the same author have not been refereed either.
- The comparison with the literature (Section 10) rests on a literature search, which cannot prove absence.

## Use of AI

Developed with the assistance of Claude (Anthropic), including the proofs, the text and the programs; the author takes full responsibility. Comments and corrections are welcome (please open an issue).

## License

- Paper (`paper/paper.tex`, `paper/paper.pdf`): Creative Commons Attribution 4.0 International (CC BY 4.0), see `paper/LICENSE`.
- Programs (`code/`) and data (`data/`): MIT License, see `LICENSE`.

## How to cite

Ryu, Sungjoon. *Packing k²−c unit squares: an upper bound of order k^{3/8} for the deficiency.* Preprint, version 1.0, 2026. https://github.com/squarepacker/k2-minus-c-upper. Preprint, programs and data: https://doi.org/{{DOI_VERSION}} (this version; all versions: https://doi.org/{{DOI_ALL}}).

## Previous works

- [R] Ryu, Sungjoon. *Packing k²−c unit squares: s(k²−c) = k for all large k.* Preprint, version 1.2, 2026. https://doi.org/10.5281/zenodo.23194104; programs and data: https://doi.org/10.5281/zenodo.23194031 and https://github.com/squarepacker/k2-minus-c (release v1.2).
- [Q] Ryu, Sungjoon. *Packing k²−c unit squares: a lower bound of order k^{1/4} for the deficiency.* Preprint, version 1.0, 2026. https://doi.org/10.5281/zenodo.23212643; programs: https://doi.org/10.5281/zenodo.23211207 and https://github.com/squarepacker/k2-minus-c-quarter (release v1.0).
- [T] Ryu, Sungjoon. *Packing k²−c unit squares: a lower bound of order k^{1/3} for the deficiency.* Preprint, version 1.0, 2026. https://doi.org/10.5281/zenodo.23213564; programs: https://doi.org/10.5281/zenodo.23212059 and https://github.com/squarepacker/k2-minus-c-cube-root (release v1.0).

None of these preprints has been refereed.
