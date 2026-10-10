# Packing k²−c unit squares: an upper bound of order k^{3/8} for the deficiency

Preprint, programs and data by Sungjoon Ryu (2026). Version 1.1.

Version 1.1 adds, among other tiers, the tiers marked ‡ (C1–C3), which use a sawtooth accounting of the wall rows and a choice of the lift of each band (Lemmas 8.6–8.8 and 8.11).

**Status: not refereed.** The paper has not been refereed. It was written with AI assistance and has so far been checked only by AI-based reviews and by computer programs, some of them independent re-implementations (see "Verification status" below). No human expert has reviewed it.

**Setting.** For n ≥ 1 let s(n) be the side of the smallest square that contains n unit squares with pairwise disjoint interiors, and for an integer k ≥ 2 let c\*(k) be the largest integer c with s(k²−c) = k (the *deficiency*: removing up to c\*(k) squares from the k×k grid does not allow a smaller container).

## Main results

| Statement | In the paper | Grade |
|---|---|---|
| For each tier i of the table below and every integer k ≥ k_i: c\*(k) < C_i·k^{3/8} + a_i | Theorem 1.1 | proved, with computer-assisted constants (certified in interval arithmetic); the range k ≥ k_i cannot be tested by explicit computation |
| c\*(k) < (20/3)·(3/2)^{2/5}·5.03^{3/5}·k^{2/5} + (8/3)·5.03·10^{−4/3} < 20.668·k^{2/5} + 0.623 for every integer k ≥ 16,000,000 (= 1.6·10⁷) | Theorem 1.2 | proved; constants certified in interval arithmetic |
| c\*(k) ≤ 8⌈√(k−4)⌉ − 1 < 8√(k−4) + 7 for every integer k ≥ 6 | Theorem 1.4 | proved |
| c\*(k) ≤ c − 1 for the five values of k in the second table below | Theorem 1.6 | computer-assisted: structural part proved; finite data (end packings) checked in exact rational arithmetic |

**The tiers of Theorem 1.1** (constants rounded up; C_E is the certified end constant, b₀ the threshold of the end lemma):

| Tier | b₀ | C_E | C_i | k_i | a_i | smaller than the k^{2/5} bound for k ≥ |
|---|---|---|---|---|---|---|
| B1 † | 10^7.7 | 17.461 | 46.31 | 2.2·10¹³ | 0.035 | 1.04·10¹⁴ |
| B1s † | 10^7.9 | 16.968 | 45.49 | 4.5·10¹³ | 0.029 | 5.07·10¹³ |
| B2 † | 10^8 | 16.721 | 45.08 | 6.4·10¹³ | 0.026 | 6.4·10¹³ |
| A1 | 10^8.5 | 18.961 | 48.76 | 4.6·10¹⁴ | 0.019 | 8.14·10¹⁴ |
| A1s | 10^8.58 | 18.722 | 48.38 | 6.1·10¹⁴ | 0.017 | 6.1·10¹⁴ |
| A2 | 10^9 | 17.523 | 46.42 | 2.7·10¹⁵ | 0.011 | 2.7·10¹⁵ |
| A3 | 10^10 | 15.859 | 43.61 | 9.6·10¹⁶ | 0.0039 | 9.6·10¹⁶ |
| A4 | 10^12 | 14.778 | 41.73 | 1.5·10²⁰ | 5.7·10⁻⁴ | 1.5·10²⁰ |
| A5 | 10^16 | 14.153 | 40.62 | 3.4·10²⁶ | 1.4·10⁻⁵ | 3.4·10²⁶ |
| C1 ‡ | 10^7.3617 | 14.473 | 41.19 | 5.22·10¹² | 0.04 | 5.22·10¹² |
| C2 ‡ | 10^7.2 | 14.805 | 41.78 | 2.95·10¹² | 0.047 | 2.95·10¹² |
| C3 ‡ | 10^7.15 | 14.983 | 42.09 | 2.48·10¹² | 0.05 | 2.48·10¹² |

Tiers marked † use, in addition, the variant ZC′ of the wall filler and Lemmas 8.2–8.5, which are new in version 1.1 (Section 8.2; the transition rows are Lemma 8.3 and the end region Lemma 8.4).
Tiers marked ‡ use, in addition to the lemmas of the tiers †, Lemmas 8.6 (sawtooth sums), 8.7 and 8.8 (sawtooth accounting of the start rows and the final stretches of ZC′, with one more hypothesis (W6)) and 8.11 (a lift per band with frac(ḡ) ≥ 1/2), and Corollary 8.12 (Sections 8.3 and 8.6); all new in version 1.1.

**Version 1.0 → 1.1.** Version 1.0 stated c\*(k) < 43.06·k^{3/8} + 2·10⁻⁵ for k ≥ 4·10²⁶. That statement remains proved (it is the parameter row "v1.0" of the paper), and it is superseded by the tier A5: c\*(k) < 40.62·k^{3/8} + 1.4·10⁻⁵ for k ≥ 3.4·10²⁶.

**Which bound to use.** Of the two bounds, only the k^{2/5} theorem is proved for 1.6·10⁷ ≤ k < 2.48·10¹² (k < 2.2·10¹³ without the tiers ‡, k < 4.6·10¹⁴ without the tiers † and ‡). With the tiers that use only the lemmas of version 1.0 (no † or ‡), the k^{3/8} theorem gives a smaller bound than 20.668·k^{2/5} + 0.623 for every k ≥ 6.1·10¹⁴ (tier A1s). With the tiers marked † as well, it does so for every k ≥ 5.07·10¹³ (tier B1s), and with the tiers marked ‡ for every k ≥ 2.48·10¹² (tier C3).
Below that point the k^{2/5} theorem is the better bound (or the only one). Neither bound is claimed to be close to c\*(k).

Also proved: for all integers 2 ≤ b ≤ k, the explicit L-shaped packing gives c\*(k) ≤ k² − N(k,b) − 1 < 6b + 4k/b − 3 (Theorem 1.3), and this family of packings cannot give less than 8√k − 15 (Proposition 1.5).

**The idea.** The L-shaped frame has two tilted bands of width just below an integer b. Their rows are lifted, and the deficiency equals the body cost of the bands (about 4k/b) plus the uncovered areas of the four band ends (Proposition 6.3). Each end is filled by a *staircase*: columns of squares with one common small tilt, whose lowest squares are replaced by horizontal layers, so that one tilt follows the rising end of the band. One end then costs at most 5.03·b^{2/3}, and b ≈ k^{3/5} gives the exponent 2/5. In Section 8 the two walls of each end are filled by chains of staircases whose tilt is lowered slightly from block to block, so that the layers close in phase; one end then costs at most C_E·b^{3/5} for b ≥ b₀, and b ≈ k^{5/8} gives the exponent 3/8. These ideas are those of H. D. Bui (arXiv:2508.04603v2, Sections 3–4); the proofs in the paper are self-contained.

**Certified values (Theorem 1.6, Table 2 of the paper).** For each row, k² − c unit squares are packed in a square of side less than k; the data file lists every piece of the four band ends as exact rationals. These staircase certificates are the best values we have at these k; the k^{3/8} construction gives larger values here (for example c\*(10⁸) ≤ 44299).

| k | b | y₀ | c = k² − N | Bound | Data file |
|---|---|---|---|---|---|
| 10⁵ | 623 | 257/4 | 1584 | c\*(10⁵) ≤ 1583 | `data/stair_k100000.json.gz` |
| 10⁶ | 2481 | 653/4 | 3973 | c\*(10⁶) ≤ 3972 | `data/stair_k1000000.json.gz` |
| 10⁷ | 9875 | 1663/4 | 10040 | c\*(10⁷) ≤ 10039 | `data/stair_k10000000.json.gz` |
| 3.825·10⁷ | 22086 | 710 | 16989 | c\*(3.825·10⁷) ≤ 16988 | `data/stair_k38250000.json.gz` |
| 10⁸ | 39314 | 1041 | 24791 | c\*(10⁸) ≤ 24790 | `data/stair_k100000000.json.gz` |

Together with the lower bound of order k^{1/3} in [T] (a preprint by the same author that has not been refereed), Theorem 1.1 gives k^{1/3} ≪ c\*(k) ≪ k^{3/8}. The true exponent of c\*(k) is open; it lies between 1/3 and 3/8.

## Changes in version 1.1

- **Tiers ‡ (new).** Sections 8.3 and 8.6 (Lemmas 8.6, 8.7, 8.8, 8.11, Corollary 8.12, Appendix B) give the tiers C1–C3 (‡), certified by the program `code/cert_v4/`. They also rely on the fact that the cited results hold for real lifts, checked line by line by two independent AI readings.
- **Tiered theorem.** Theorem 1.1 is now a table of 12 tiers c\*(k) < C_i·k^{3/8} + a_i (k ≥ k_i). The single bound of version 1.0 (43.06·k^{3/8} + 2·10⁻⁵, k ≥ 4·10²⁶) is superseded by the tier A5 (40.62, k ≥ 3.4·10²⁶), and the smallest threshold is now k ≥ 2.48·10¹².
- **Parameters.** The construction of Section 8 is stated with six parameters (b₀, the window coefficient c_y, the wall widths c_D, c_R, the wall tilt factor a_w and the proof parameter ϖ). No new lemma is needed for this; two short arguments are added (the error of the wall tilts for all tilts up to 1/10, and the room for the lifts).
- **New lemmas** (Section 8.2): a variant ZC′ of the wall filler, and Lemmas 8.2, 8.3, 8.4 and 8.5 with a smaller bound for the transition rows and the end region. Only the tiers marked † use them.
- **Which bound to use** (introduction): rewritten; the k^{3/8} theorem now gives a smaller bound than 20.668·k^{2/5} + 0.623 from k ≥ 2.48·10¹².
- **Appendix A**: the complete list of the normalised inequalities, with the parameters.
- **Fixes from two blank-slate AI reviews of the version 1.1 changes**: the value (32/5)(5/3)^{3/8} ≈ 7.751277, upper bounds in the tables rounded up, the condition that the successor block exists in the lemma on transition rows, the derivation of the range of t/z², and the wording "no new lemmas" for the parameter part.
- **Programs**: the author's covering `code/cert_v3/cert_v3.py` with `finalize_v3.py`, the stated constants `tiers_v3.json` and the recorded slices and merge (`code/checker_outputs/cert_v3/`); the exact tests of version 1.1 in `code/zc_tests/` with their recorded outputs (`code/checker_outputs/zc_tests/`). All files of version 1.0 are kept.
- **Programs of the tiers ‡**: the author's covering `code/cert_v4/cert_v4.py` (with `stated_v4.py`), its recorded slices and merges (`code/checker_outputs/cert_v4/`), and the exact tests `code/cert_v4/sl_t2_test.py` of Lemmas 8.6 and 8.11.
- **Status**: the verification of version 1.1 is described below and at the end of the paper.
- The bibliography adds version 1.0 of this work [U].

## Contents

| Path | Content |
|---|---|
| `paper/paper.pdf`, `paper/paper.tex` | The preprint (43 pages) |
| `paper/LICENSE` | CC BY 4.0 for the paper |
| `data/stair_k*.json.gz` | The end pieces of the five certified packings of Theorem 1.6 (exact rationals, gzip-compressed JSON) |
| `code/stair_check.py` | Checker of the certified packings (does not import the generator), with 7 negative controls |
| `code/stair_dump.py` | The program that generated the data files |
| `code/const_stair.py` | Interval-arithmetic certification of the constants of Theorem 1.2 (Corollary 7.4 and Section 7.3) |
| `code/cert3e.py` | Interval-arithmetic covering for the parameter row of version 1.0 (b ≥ 10¹⁶); written by an independent re-implementation |
| `code/cert_v3/` | The author's interval-arithmetic covering of all parameter rows (`cert_v3.py`), the merge and theorem checks (`finalize_v3.py`), the stated constants (`tiers_v3.json`) and the tier parameters (`tiers_v3_params_only.json`) |
| `code/r38.py`, `code/chk.py`, `code/run_z.py` | The wall filler of Section 8 in exact arithmetic, a generic exact checker, and an explicit validity check (m = 10⁴) |
| `code/cert_v4/` | The author's interval-arithmetic covering of the tiers ‡ (`cert_v4.py`), the rounding of their stated constants (`stated_v4.py`), and exact tests of Lemmas 8.6 and 8.11 (`sl_t2_test.py`) |
| `code/zc_tests/` | Exact tests of version 1.1: the wall filler ZC′ and the bound B_W″ (`p3test`), and end packings with the aligned cut, with ZC walls (`e38_zc`) and with ZC′ walls (`e38_zcprime`) |
| `code/README_code.txt` | Commands, expected outputs, times and SHA-256 of the data |
| `code/checker_outputs/` | Recorded outputs of the runs |
| `LICENSE` | MIT License for `code/` and `data/` |
| `SHA256SUMS` | SHA-256 of every file except `README.md`, `.zenodo.json` and itself |

## How to reproduce

Python 3 with `numpy` and `mpmath` (`pip install numpy mpmath`); `gmpy2` is optional and only makes the checkers faster. Run the commands from the top folder of this repository (the folder that contains `code/` and `data/`), except where `code/README_code.txt` says to change into `code/cert_v3`. Times are from the author's laptop.

```
python code/const_stair.py  -> last line "ALL CHECKS: True"  (about 2 s)
python code/stair_dump.py table data  # (all five rows of Table 2, about 30 s)
python code/stair_check.py data/stair_k100000.json.gz 100000
python code/stair_check.py data/stair_k100000.json.gz 100000 mutate  # (negative controls)
python code/stair_check.py data/stair_k1000000.json.gz 1000000
python code/stair_check.py data/stair_k10000000.json.gz 10000000
python code/stair_check.py data/stair_k38250000.json.gz 38250000
python code/stair_check.py data/stair_k100000000.json.gz 100000000  # (about 1 minute, 0.2 GB with Fraction)
python code/cert3e.py 160 64  -> "all_positive": true, "Psi_sup" 96.4768..., "C_E_cert" 14.9636...
python code/run_z.py 10000 1 0.5 4  # (about 10 s)  # (expected output: code/README_code.txt)
cd code/cert_v3 && python cert_v3.py run --tier B2 --nz 320 --nt 128 --iz0 160 --iz1 320 > c_B2_160_320.json
cd code/cert_v3 && python finalize_v3.py ../checker_outputs/cert_v3  -> prints code/checker_outputs/cert_v3/finalize_out.txt exactly (tables of tiers and theorem checks; theorem_ok
cd code/cert_v3 && python cert_v3.py run --lb0 16 --params 1/12,4,4,1.5,0.65 --nz 160 --nt 64 --full 1
python code/zc_tests/p3test/p3test.py 10000 0.5 4 3/2 0.65 1
python code/zc_tests/e38_zcprime/a10.py 102400 1 3 292683 100000 1.26562 0 1
python code/cert_v4/cert_v4.py run --lb0 7.3617 --params 0.153846,2.81426,3.00931,1.26,1.3608,1.35403,0.65 --nz 320 --nt 128 --iz0 0 --iz1 160
python code/cert_v4/cert_v4.py merge --stated 14.473,41.19,5.22e12,0.04 code/checker_outputs/cert_v4/10_C1_s0.json code/checker_outputs/cert_v4/11_C1_s1.json
python code/cert_v4/sl_t2_test.py 3000 500
```

Details, the outputs of every program and the SHA-256 of the data files are in `code/README_code.txt`. To check the files: `sha256sum -c SHA256SUMS` (Linux, macOS) or compare with `Get-FileHash` (Windows).

## Verification status

- **AI-written.** The proofs, the text and all programs were developed with the assistance of Claude (Anthropic); the author takes full responsibility.
- **AI reviews.** The text has been reviewed only by AI systems (instances that did not write it). An earlier write-up of Sections 3–5 received an independent AI review that found no critical or major issue. An earlier write-up of the proof of Theorem 1.2 (Section 7) received two independent blank-slate AI reviews, both of which judged it correct with no critical or major issue. The write-up of Section 8 of version 1.0 received two independent blank-slate AI reviews with their own programs (one: correct after fixes; the other: correct). The changes of version 1.1 received two further independent blank-slate AI reviews: both found the parameter part correct after minor fixes.
Both found the new lemmas correct.
All fixes are included. The proofs deserve priority in a human review.
- **Coverings of the constants of the tiers.** The constants are certified by the author's covering (`code/cert_v3/cert_v3.py`) and by three coverings written independently from the text: two by verification agents (mpmath.iv and python-flint arb) and one by a reviewer (mpmath.iv), and all three implement the same normalised inequalities (the list of Appendix A), so they check the arithmetic and the coverage but are only a weak check of the transcription of these inequalities from the lemmas; the point checks of the un-normalised formulas (at 90, 120 and 5850 points) partly address that. All programs were written by AI systems of the same family. The constant C_E = 15.54 of version 1.0 is certified by three independent full-range coverings (C_E ≤ 14.964, 14.963 and 14.9631); the first is `cert3e.py`.
  - For the tiers ‡ the author's covering is `code/cert_v4/cert_v4.py`, and the three independent coverings implement the normalised inequalities of Appendices A and B.
- **Verification of version 1.1** (details at the end of the paper):
  - Independent covering 1 (verification agent; from the text alone; mpmath.iv, 120 bits): 512 z-strips × 128 t-pieces with adaptive refinement, about 65,537 boxes per tier; gap-free check passed; z = 0 included. All nine tiers certified (C_E bound at most the stated value, every margin positive), for example A1s 18.71447, A5 14.14983, B1s 16.96349, B2 16.71729. Pointwise check of the un-normalised formulas at 90 points: passed. Negative control (parameters of version 1.0 at b₀ = 10⁹): fails (E-iii), as expected.
  - Independent covering 2 (verification agent; from the text alone; python-flint arb, 160 bits, adaptive bisection): 389–3013 leaves per tier; partition checked by a Kraft sum equal to 1 and by the total area. All nine tiers certified, for example A1s 18.70756, A5 14.14845, B1s 16.95859, B2 16.71253. Direct un-normalised evaluation at 120 cases: passed.
  - Reviewer's covering (blank-slate review; mpmath.iv, 120 bits, 320 × 128 boxes): all nine tiers agree with the table of the paper to the printed digits.
  - Independent re-implementation of ZC, ZC′, E38, E38′ and the full L-shaped packing, from the text alone, in exact rational arithmetic, with a separate exact checker (separating axes): 133 instances, 4.39·10⁷ pieces, all valid; some of these instances (end packings where (E-iii) fails) use the convention τ := 0 of Remark 8.13. Wall bounds U ≤ B_W″ hold in 49 of 49 walls ((W1)–(W5) hold in 36 of them); Lemmas 8.3 and 8.4 hold term by term in 46 of 46 accounted walls. First in-window aligned-cut tests (τ > 0), eight end packings at b = 1.5·10⁶–4·10⁶ (parameters of the tiers B1, B1s, B2): all valid; seven of the eight satisfy all hypotheses and are within the bound of Lemma 8.9; in the eighth (B1, b = 1.5·10⁶, y = 59407/4) hypothesis (E-v) fails for the lower right wall, which was filled by rows only (a convention, not part of the construction), so the bound does not apply there. Pointwise check of the corollary on the band ends at 5850 points: passed. 29 of 30 negative controls rejected; the remaining one is a valid packing.
  - Tiers ‡: two blank-slate AI reviews (one: Lemmas SL, T1/W4 and T2 correct, the corollary and theorem for these tiers correct after fixes, included; the other: all correct). Exact tests (not proofs): 53 walls ZC′ (34 with all hypotheses true), no violation, largest ratio U/B_W4 0.737; Lemma SL in 21592 cases; Lemma T2 in 376 cases plus 3000 cases forced to y1 = y0 + 1; no violation. Three independent coverings of C1–C3 written from the text, all passing: python-flint arb 14.46634 / 14.79786 / 14.97606; mpmath.iv 14.469520 / 14.801342 / 14.979582; the reviewer's mpmath.iv covering reproduces 14.47251 / 14.80459 / 14.982873. All three implement the same normalised inequalities (Appendix B); point checks of the un-normalised formulas at 46 + 36 points. That the cited results hold for real lifts was checked line by line by two independent AI readings; the lift of Lemma 8.11 satisfies the four conditions they need (Section 8.6). A direct covering of the un-normalised bound for b₀ ≤ b ≤ 10¹⁶ (python-flint arb; integer quantities enclosed exactly per box, actual wall lengths, Appendix B not used; only J₀ uses the mean-value inequality) certifies U/b^{3/5} ≤ 13.910 / 14.235 / 14.319 for C1 / C2 / C3, all margins positive; above 10¹⁶ the normalised coverings apply. Exact end packings: 15 complete end packings E38′ for C1–C3 with lifts of Lemma 8.11, b from 1.41·10⁷ to 2.30·10⁷ (1.47·10⁷–2.37·10⁷ pieces each), checked exactly (separating axes, containment, exact U): all hypotheses hold, no overlap, no failure, U ≤ 0.71 × the bound of Lemma 8.9 and U ≤ 0.69 C_E b^{3/5}, U_Z/B_W4 between 0.44 and 0.75; 3 of the 15 have y1 = y0 + 1. Of 30 negative controls 24 were rejected; the other 6 came from a flaw in the design of the controls and were rejected when applied to the whole packing.
  - The programs of the reviews, of the independent coverings and of the re-implementation are not included.
- **Other independent checks (version 1.0).**
  - Theorem 1.2 relies on one evaluation in interval arithmetic, Φ(10^{−4/3}) ≤ 5.0163, done by the author's program (`const_stair.py`) and by three independent computations; the other constants were certified in the same way.
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

Ryu, Sungjoon. *Packing k²−c unit squares: an upper bound of order k^{3/8} for the deficiency.* Preprint, version 1.1, 2026. https://github.com/squarepacker/k2-minus-c-upper. Preprint, programs and data: https://doi.org/{{DOI_VERSION}} (this version; all versions: https://doi.org/10.5281/zenodo.23256654).

## Previous works

- [U] Ryu, Sungjoon. *Packing k²−c unit squares: an upper bound of order k^{3/8} for the deficiency.* Preprint, version 1.0, 2026. https://doi.org/10.5281/zenodo.23256655 (all versions: https://doi.org/10.5281/zenodo.23256654). Version 1.0 of this work.
- [R] Ryu, Sungjoon. *Packing k²−c unit squares: s(k²−c) = k for all large k.* Preprint, version 1.2, 2026. https://doi.org/10.5281/zenodo.23194104; programs and data: https://doi.org/10.5281/zenodo.23194031 and https://github.com/squarepacker/k2-minus-c (release v1.2).
- [Q] Ryu, Sungjoon. *Packing k²−c unit squares: a lower bound of order k^{1/4} for the deficiency.* Preprint, version 1.0, 2026. https://doi.org/10.5281/zenodo.23212643; programs: https://doi.org/10.5281/zenodo.23211207 and https://github.com/squarepacker/k2-minus-c-quarter (release v1.0).
- [T] Ryu, Sungjoon. *Packing k²−c unit squares: a lower bound of order k^{1/3} for the deficiency.* Preprint, version 1.0, 2026. https://doi.org/10.5281/zenodo.23213564; programs: https://doi.org/10.5281/zenodo.23212059 and https://github.com/squarepacker/k2-minus-c-cube-root (release v1.0).

None of these preprints has been refereed.
