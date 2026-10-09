# Packing k²−c unit squares: a lower bound of order k^{1/4} for the deficiency

Preprint and programs by Sungjoon Ryu (2026). Version 1.0.

**Status: not peer reviewed.** The arguments have so far been checked only by AI-based reviews and by numerical tests (see "Verification status" below and `reviews/REVIEWS.md`). No human has reviewed them.

**Main result.** Let M(k) be the largest number of unit squares that fit in [0,k]² pairwise disjoint as closed sets, and let s(n) be the side of the smallest square containing n non-overlapping unit squares. Then:

- k² − M(k) ≥ 0.1 · k^{1/4} for every integer k ≥ 4.62·10¹² (Theorem A);
- liminf_{k→∞} (k² − M(k)) / k^{1/4} ≥ 0.1696;
- consequently s(k²−c) = k for every integer k ≥ max(4.62·10¹², 10⁴c⁴ + 1) (Corollary A). So c*(k) := max{c : s(k²−c) = k} grows at least like k^{1/4}; by recent work on the wasted area it is O(k^{3/5}).

**Dependence on a computer-assisted lemma.** The constants 0.1, 4.62·10¹² and 0.1696 above rely on the computer-assisted Lemma 4.10 of the previous paper [R]. Its box computations have been replayed with the same programs by the Squares Project, but they have not yet been reproduced by an independent implementation. Theorem A₁₃ does not use Lemma 4.10. It uses the analytic Lemma 4.9 of [R] instead, whose proof contains only a short finite check of angle conditions (done in [R] by a small program). With it, the same argument gives k² − M(k) ≥ 0.1 · k^{1/4} for every integer k ≥ 2.17·10¹³, and liminf ≥ 0.1411.

**The threshold has a small margin.** With the parameters used in the proof, the last inequality of the argument holds exactly for k ≥ k*, where k* ≈ 4.6167·10¹². The threshold 4.62·10¹² is k* rounded up to three significant digits (4.62·10¹²/k* − 1 = 7.2·10⁻⁴). If one of the constants of the proof were larger than the tolerance stated in Section 12.6 of the paper (for example A′ ≤ 10.60905 or C_Λ ≤ 1.0150), the threshold would have to be raised. For Theorem A₁₃, k* ≈ 2.1696·10¹³.

**Relation to the previous paper.** [R] (version 1.2: paper https://doi.org/10.5281/zenodo.23194104, programs https://doi.org/10.5281/zenodo.23194031, repository [squarepacker/k2-minus-c](https://github.com/squarepacker/k2-minus-c), release v1.2) proves k² − M(k) ≥ 0.0353 · log k for every k ≥ 2. This paper uses the lemmas of [R] listed in its Section 2, where their statements are quoted with the numbering of [R] (version 1.2); their proofs are in [R], and the few facts about those proofs that are used are listed in Remark 2.4. Sections 3–12 are new: flows of upward paths from the bottom side (and downward paths from the top side) that follow the orientation of the squares they cross and enter squares only through their bottom sides, organized over a continuum of scales.

## Contents

| Path | Content |
|---|---|
| `paper/paper.pdf`, `paper/paper.tex` | The preprint (108 pages) |
| `paper/LICENSE` | CC BY 4.0 for the paper |
| `code/k14_constants_check.py` | Recomputes every numerical constant and threshold displayed in the paper and checks each displayed value in its stated rounding direction (mpmath, interval arithmetic and exact rationals; prints `ALL OK`, 555 checks) |
| `code/numerical_tests/` | Numerical tests on scaled analogues of the construction: `P1_P2/`, `P3_P5/`, `P4/`, `P6/`, `P7/`, `P8/`, `assembly/`. They are tests, not part of the proof. Each folder has its programs, the recorded results and a README |
| `code/numerical_tests/rerun_linux_2026-10-07/` | A re-run of the quick checks, and of the long runs not repeated before, on a clean Linux machine, with the comparison against the recorded results |
| `reviews/REVIEWS.md` | Summary of the reviews and tests so far (all by AI systems) |
| `LICENSE` | MIT License for `code/` |
| `SHA256SUMS` | SHA-256 of every file except `README.md`, `.zenodo.json` and itself |

## Reproduce the checks

Python 3.12 with `mpmath` (and `numpy`, `scipy` for some numerical tests):

```
pip install mpmath numpy scipy
python code/k14_constants_check.py
```

For the numerical tests, see `code/numerical_tests/README.md` and the README in each folder (each has a quick mode).

## Verification status

- The paper has not been peer reviewed, and neither has [R].
- In an earlier form, each part proved in Sections 4–10 was checked by an independent AI review and by numerical tests on scaled analogues; the assembly (Section 11) by an independent AI review and an end-to-end numerical test. These reviews led to corrections, which are included.
- The present text received a blank-slate AI review: twelve parts reviewed separately, with numerical searches for counterexamples, the constants recomputed with new code, and the quotations of [R] compared with [R]. It found no critical or major issue and 18 minor ones (wording, the use of the proofs in [R], notation, and two constants displayed with a last digit larger than necessary); all have been addressed in this version. Details: `reviews/REVIEWS.md`.
- Every displayed constant is recomputed by `code/k14_constants_check.py`.
- The quick checks of the numerical tests, and the long runs not repeated before, were re-run on a clean Linux machine: 80 of 80 claims of the folder READMEs reproduced (`code/numerical_tests/rerun_linux_2026-10-07/`).
- All reviewers are AI systems of the same family and may share blind spots, and the numerical tests use small analogues, not the actual parameter regime.
- Theorem A (not Theorem A₁₃) uses the computer-assisted Lemma 4.10 of [R], whose box verification has been replayed with the same programs by the Squares Project but not reproduced by an independent implementation.

## Use of AI

Developed with extensive assistance from Claude (Anthropic), including the proofs, the text and the programs; the author takes full responsibility. Not peer reviewed. Comments and corrections are welcome (please open an issue).

## License

- Paper (`paper/paper.tex`, `paper/paper.pdf`): Creative Commons Attribution 4.0 International (CC BY 4.0), see `paper/LICENSE`.
- Programs (`code/`): MIT License, see `LICENSE`.

## How to cite

Ryu, Sungjoon. *Packing k²−c unit squares: a lower bound of order k^{1/4} for the deficiency.* Preprint, version 1.0, 2026. https://github.com/squarepacker/k2-minus-c-power. DOI: added after the release.

[R] Ryu, Sungjoon. *Packing k²−c unit squares: s(k²−c) = k for all large k.* Preprint, version 1.2, 2026. https://doi.org/10.5281/zenodo.23194104; programs and data: https://doi.org/10.5281/zenodo.23194031 and https://github.com/squarepacker/k2-minus-c (release v1.2)
