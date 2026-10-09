# For every fixed c, s(k²−c) = k for all large k — with an explicit constant

Preprint and verification programs by Sungjoon Ryu (2026). Version 1.2.

**Main result.** For every fixed c ≥ 0 one has s(k²−c) = k for all sufficiently large integers k, where s(n) is the side of the smallest square containing n non-overlapping unit squares. Equivalently, if M(k) is the largest number of unit squares that fit in [0,k]² pairwise disjoint as closed sets, then k² − M(k) → ∞. The constant is explicit:

- k² − M(k) ≥ 0.0353 · log k for every integer k ≥ 2;
- k² − M(k) ≥ 1.99954 · (log k − 13.06675) / 30.418 for every k ≥ 2, so k² − M(k) ≥ (0.0657 − o(1)) · log k as k → ∞;
- if one also uses E. Daniel's computer-assisted, not yet refereed result s(k²−3) = k for all k ≥ 6 (checked again by an independently written program and recorded as entry T-064 of J. Levy's Squares Project), then k² − M(k) ≥ 0.0541 · log k for every k ≥ 2 (Corollary 1.3). The main theorem does not use this result, and the asymptotic slope is unchanged.

The value 0.0353 uses a computer-assisted lemma (Lemma 4.10, see below). Without it, the analytic Lemma 4.9 alone gives the constant 0.0319, so the qualitative result does not depend on the computer.

So c*(k) := max{c : s(k²−c) = k} → ∞. Whether c*(k) → ∞ was recorded as open in E. Daniel's notes (evand/square-packing, `s12/search/FRIEDMAN.md`).

**What it does not do.** The result is qualitative: it says nothing about any k within computational reach. For example, it yields s(k²−4) = k only for log k > 73.92, and it says nothing about s(12). (For concrete values, see the computer-assisted, unrefereed announcement of s(k²−4) = k for all k ≥ 5 in evand/square-packing, which addresses a different question.)

## Constants with and without the computer

- Lemma 4.9 (analytic): at uncovered points at most 13 of the Roth–Vaughan rectangles of nearly touching pairs overlap. With this alone the proof gives k² − M(k) ≥ 0.0319 · log k for every k ≥ 2.
- Lemma 4.10 (computer-assisted): at most 9 overlap. This gives the constant 0.0353. The bound 9 is sharp for the number of all pairs at distance < d; whether it is sharp for the edges of a single graph is not known.
## The computation behind Lemma 4.10

- **Disc model.** The lemma reduces to bounding U(I) = E_II + W_I + Σ D_i*(I) over all configurations I of at most 5 centres near the uncovered point, without a side and with one side.
- **Branch-and-bound.** A floating-point search (`bnb.py`, `bnb_wall.py`) found a cover of the parameter domain by 78,673 accepted boxes. Every box is either infeasible, has no possible side pair, or has bound ≤ 9.
- **Rigorous re-verification.** Every accepted box was re-verified in Arb ball arithmetic through python-flint (`verify_leaves2.py`), with 59,238 further bisections. There were 0 failures, and the largest rigorous bound was 9.
- **Coverage check.** A separate program (`coverage_check.py`) rebuilds the bisection tree and checks, with exact rational volumes, that the accepted boxes leave no gap. It reuses the bisection rule of the search, so it is not independent of it.
- **Independent coverage checks.** Two further programs, written independently of the search by different methods, confirm that the accepted boxes leave no gap: an exact-volume check and a recursive covering check (`code/coverage_independent/`, with results and a README). They were written by separate sessions of the same AI system (Claude) that helped to write all the programs, and they share with the search the lists of boxes and the description of the domain.
- **Superseded verifier.** An earlier verifier (`verify_leaves.py` used alone, and `verify_edge.py`) did not cover one-ulp gaps between floating-point direction cells. It is superseded (see `code/SUPERSEDED.md`). The certificate is the output of `verify_leaves2.py`.
- **What is independently reproduced.** The coverage (no gap) is confirmed by the two independent checks above. The verification of the individual boxes (the Arb re-verification) has not yet been reproduced by an independent implementation. It takes from the search programs the grids of direction cells and of radial intervals, the floating-point value of gamma_0, their floating-point prefilter (which only proposes cells to discard; every discard is certified in Arb), the final point count (in floating point; the proof of Lemma 4.10 shows that its result is exact) and the bisection rule. The Squares Project (J. Levy) reports a complete replay of the re-verification with these programs (it used the version 1.0 release, whose programs and data for Lemma 4.10 are identical to these), with the same results (jlevy/squares, issue #368); this repeats the same implementation.

## Contents

| Path | Content |
|---|---|
| `paper/paper.pdf`, `paper/paper.tex` | The preprint (28 pages) |
| `paper/LICENSE` | CC BY 4.0 for the paper |
| `code/verify_v11.py` | Recomputes every numerical constant in high-precision arithmetic (mpmath). It also checks that the computation of Lemma 4.10 is complete (needs `data/kw9_data.zip` unpacked into `code/`). Prints `ALL OK` (170 checks) |
| `code/consts_v11.py` | Constants of Sections 5–6 |
| `code/kw13_check.py` | Numerical facts used in Lemma 4.9(c), and the constants of the variant without Lemma 4.10 (Remark 7.5) |
| `code/bnb.py`, `code/bnb_wall.py` | Branch-and-bound search (without / with a side) |
| `code/verify_leaves.py`, `code/verify_leaves2.py` | Rigorous Arb re-verification (`verify_leaves2.py` is the certificate; it imports routines from `verify_leaves.py`) |
| `code/coverage_check.py`, `code/make_stats_v10.py`, `code/run_seq.py`, `code/run_v2.py` | Coverage check, statistics, job runners |
| `code/check_hand9_indep.py`, `code/attack_kw/hand9.json` | The configuration with 9 pairs (sharpness) and its check in 80-digit arithmetic |
| `code/SUPERSEDED.md` | Note on the superseded first verifier |
| `code/coverage_independent/` | Two independent checks that the accepted boxes of Lemma 4.10 cover the parameter domain (exact volumes; recursive covering), with results; see its README |
| `code/experiments/` | Search programs and stored results behind the numerical experiments of Remark 7.5 (not part of the proof); see `code/experiments/README.md` |
| `data/kw9_data.zip` | Accepted boxes of the final runs, verification and coverage results, logs |
| `reviews/REVIEWS.md` | Summary of the independent (AI) reviews |
| `LICENSE` | MIT License for `code/` and `data/` |

Reproduce the checks (Python 3.12; packages `mpmath`, `numpy`, `python-flint`):

```
pip install mpmath numpy python-flint
python code/kw13_check.py
python code/check_hand9_indep.py
```

Unpack `data/kw9_data.zip` into `code/`, then run:

```
cd code
python coverage_check.py bnb_n3_T9_0of1_final_leaves.jsonl
python verify_leaves2.py bnb_n3_T9_0of1_final_leaves.jsonl 9 0 1
python make_stats_v10.py
python verify_v11.py
```

The full re-verification of all boxes took about 1.7 hours on 4 cores.

## Changes in version 1.2

- The paper (edition 11) also uses the lines near the bottom and top sides: the excess over 1 of the long chords on such a line is paid for by the waste (new Lemmas 3.5 and 4.15). In Section 6 the cutoff d(y) ≥ √k/4 is replaced by a constant, and Lemmas 4.14, 5.2 and 5.4 are restated for the new parameters. The constant improves from 0.033 to 0.0353 for every k ≥ 2, and the asymptotic slope from 0.0331 to 0.0657 (0.027 → 0.0319 without Lemma 4.10).
- New Corollary 1.3: if one also uses E. Daniel's computer-assisted, not yet refereed result s(k²−3) = k for all k ≥ 6, the constant for every k ≥ 2 becomes 0.0541. The main theorem (0.0353) does not use it. New references: J. Levy, The Squares Project (entry T-064); wand125, valid7-independent-check.
- `code/verify_v11.py` and `code/consts_v11.py` replace `verify_v10.py` and `consts_v10.py`; `verify_v11.py` contains every check of `verify_v10.py` that still applies. The version 1.1 programs remain in the v1.1 release.
- After an AI review of version 1.1 by the Squares Project (J. Levy; jlevy/squares, file `docs/project/reviews/review-2026-10-05-squarepacker-k2-minus-c.md`, commit 6953107, and issue #368), several passages were revised without changing the results: Section 4 and the proof of Lemma 4.10 now agree that k ≥ 4 there, and Section 4 states that Sections 4 and 5 are used in the proof only for k ≥ 10^12 (for 2 ≤ k < 10^12 the theorem follows from Corollary 3.3); the proof of Lemma 4.10 now explains why extending the angle intervals to 2π covers the arc (2π_float, 2π), shows that the floating-point point count is exact, says which parts of the search programs the re-verification uses, and reports the replay by the Squares Project; the authorship of the two further coverage checks is stated; Remark 7.1 lists further uses of disjointness; Remarks 4.11 and 7.2 are marked as not used in the proofs; acknowledgements and a reference to the review were added. Remark 7.5 now also restates Lemma 4.13 for its hypothetical value Q* = 1/3. `code/verify_v11.py` checks the new statements.
- `code/coverage_independent/recursive_cover/summarize.py` no longer stops with `round(inf)` before its verdict line when run outside Windows; `code/kw13_check.py` now checks the constants of version 1.2 for the variant without Lemma 4.10 (its second half checked those of an earlier draft).
- The computation of Lemma 4.10 (programs and data) is unchanged.

## Changes in version 1.1

- Added `code/coverage_independent/`: two independent coverage checks for Lemma 4.10, with their results.
- One sentence in the proof of Lemma 4.10 (and the corresponding line above) now states precisely what has been independently reproduced: the coverage, by two independent checks; not yet the verification of the individual boxes.
- `SHA256SUMS` now covers every file except `README.md` and `.zenodo.json` (metadata that may be edited on the GitHub web page). The mathematics is unchanged.

## Status and use of AI

Developed with extensive assistance from Claude (Anthropic), including the proofs, the text, the programs and the computation for Lemma 4.10; the author takes full responsibility. Not peer reviewed. Comments and corrections are welcome (please open an issue).

## License

- Paper (`paper/paper.tex`, `paper/paper.pdf`): Creative Commons Attribution 4.0 International (CC BY 4.0), see `paper/LICENSE`.
- Programs and data (`code/`, including `code/experiments/`, and `data/`): MIT License, see `LICENSE`.

`LICENSE` contains the MIT License text; it applies to `code/` and `data/`. The paper is licensed separately under CC BY 4.0 (`paper/LICENSE`).

## How to cite

Ryu, Sungjoon. *Packing k²−c unit squares: s(k²−c) = k for all large k.* Preprint, version 1.2, 2026.

- This repository (software record on Zenodo): DOI (v1.2): added after the release. DOI (v1.1): https://doi.org/10.5281/zenodo.23165736. DOI (v1.0): https://doi.org/10.5281/zenodo.23164302
- The paper alone (PDF record on Zenodo): all versions https://doi.org/10.5281/zenodo.23165915; version 1.1: https://doi.org/10.5281/zenodo.23165916; version 1.2: added after the release.

Software record, all versions (always the latest): https://doi.org/10.5281/zenodo.23164301
