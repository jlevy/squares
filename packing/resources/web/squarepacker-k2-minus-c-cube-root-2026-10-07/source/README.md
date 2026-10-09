# Packing k²−c unit squares: a lower bound of order k^{1/3} for the deficiency

Preprint and programs by Sungjoon Ryu (2026). Version 1.0.

**Status: not peer reviewed.** The argument has so far been checked only by AI-based reviews, by computer programs and by a numerical test on scaled analogues (see "Verification status" below and `reviews/REVIEWS.md`). No human has reviewed it.

**Main result.** Let M(k) be the largest number of unit squares that fit in [0,k]² pairwise disjoint as closed sets, let W_min(k) = k² − M(k), and let s(n) be the side of the smallest square containing n non-overlapping unit squares; for integers 0 ≤ c < k², s(k²−c) = k exactly when c < W_min(k). Then (Theorem 1.1):

- W_min(k) > 10⁻⁴ · √k for every integer k with 10⁸ ≤ k ≤ 2.5·10¹⁵;
- W_min(k) > 7·10⁻⁵ · √k for every integer k with 2.5·10¹⁵ ≤ k ≤ 3.5·10¹⁷;
- W_min(k) > 0.06 · k^{1/3} for every integer k ≥ 3.5·10¹⁷ (and > 0.0625 · k^{1/3} for k ≥ 10²¹);
- liminf_{k→∞} W_min(k) / k^{1/3} ≥ 0.06285.

For every k ≥ 4.62·10¹² these bounds exceed the bound 0.1 · k^{1/4} of the previous paper [Q]; at k = 4.62·10¹² they give W_min ≥ 215 (against 147).

**The new ingredient.** The squares crossed by one upward path of the flow of [Q] occupy pairwise disjoint height intervals, so the lemma of [R] on the cost of inclinations (Lemma 4.13 of [R]) applies to their union. Hence the total inclination along any path is at most a constant times W, independently of the height, and a single flow with a tilt threshold of order 1/W keeps every path quantized at every height.

**Dependence on earlier results.** The proof uses, as black boxes:

- Sections 3–8 of [Q] (the flow of upward paths, the height identity, the shadow inequality and the bounds for the terminations);
- Lemma 3.1, Corollary 3.3, Lemmas 3.4, 3.5, 4.13 and 4.15 of [R] (version 1.2);
- for Theorem 1.1 (not for Theorem 1.2), the computer-assisted Lemma 4.10 of [R], whose box computations have been replayed with the same programs by the Squares Project but not reproduced by an independent implementation. Theorem 1.2 uses the analytic Lemma 4.9 of [R] instead and gives 8.5·10⁻⁵ · √k on [10⁸, 2.4·10¹⁵], 6·10⁻⁵ · √k on [2.4·10¹⁵, 3.39·10¹⁷], 0.05 · k^{1/3} from 3.39·10¹⁷ on, and liminf ≥ 0.05229.

## Contents

| Path | Content |
|---|---|
| `paper/paper.pdf`, `paper/paper.tex` | The preprint (9 pages) |
| `paper/LICENSE` | CC BY 4.0 for the paper |
| `code/check_table_iv.py` | Checks the eight cases of Table 1 (conditions (i)–(iv) of Proposition 6.1) in interval arithmetic (mpmath) |
| `code/check_table_exact.py` | Independent check in exact rational interval arithmetic: the rounded constants of Section 2.1 and the eight cases of Table 1 |
| `code/check_table_exact2.py` | A second independent check in exact rational arithmetic (standard library only): Table 1 and the numbers quoted in the text |
| `code/*.out.txt` | The outputs of the three programs |
| `code/numerical_tests/` | The numerical test on scaled analogues (programs, summaries, raw records, README); a test, not part of the proof |
| `reviews/REVIEWS.md` | Summary of the reviews and tests so far (all by AI systems) |
| `LICENSE` | MIT License for `code/` |
| `SHA256SUMS` | SHA-256 of every file except `README.md`, `.zenodo.json` and itself |

## Reproduce the checks

Python 3.12 with `mpmath`:

```
pip install mpmath
cd code
python check_table_iv.py
python check_table_exact.py
python check_table_exact2.py
```

## Verification status

- The paper has not been peer reviewed, and neither have [Q] and [R].
- The argument was checked by independent blank-slate AI reviews (of two drafts of the argument and of drafts of this text). None found a critical or a major issue; their minor remarks have been addressed. Details: `reviews/REVIEWS.md`.
- Table 1 was checked by three programs written independently of each other (`code/`).
- A numerical test on scaled analogues (k = 14, 16; 2,560 exactly verified packings) found no counterexample to the lemmas of Sections 3–5 with measured constants. Such a test cannot check the constants of [Q] and [R].
- All reviewers are AI systems of the same family and may share blind spots. The parts that deserve priority in a human review are Lemma 3.1 of the paper, [R, Lemma 4.13] (and, for Theorem 1.1, [R, Lemma 4.10]) and [Q, Sections 3–8].

## Use of AI

Developed with extensive assistance from Claude (Anthropic), including the proofs, the text and the programs; the author takes full responsibility. Not peer reviewed. Comments and corrections are welcome (please open an issue).

## License

- Paper (`paper/paper.tex`, `paper/paper.pdf`): Creative Commons Attribution 4.0 International (CC BY 4.0), see `paper/LICENSE`.
- Programs (`code/`): MIT License, see `LICENSE`.

## How to cite

Ryu, Sungjoon. *Packing k²−c unit squares: a lower bound of order k^{1/3} for the deficiency.* Preprint, version 1.0, 2026. https://github.com/squarepacker/k2-minus-c-cube-root. DOI: added after the release.

[Q] Ryu, Sungjoon. *Packing k²−c unit squares: a lower bound of order k^{1/4} for the deficiency.* Preprint, version 1.0, 2026. https://doi.org/10.5281/zenodo.23211207 (preprint and programs) and https://github.com/squarepacker/k2-minus-c-quarter (release v1.0)

[R] Ryu, Sungjoon. *Packing k²−c unit squares: s(k²−c) = k for all large k.* Preprint, version 1.2, 2026. https://doi.org/10.5281/zenodo.23194104; programs and data: https://doi.org/10.5281/zenodo.23194031 and https://github.com/squarepacker/k2-minus-c (release v1.2)
