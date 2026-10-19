Programs and data of "Packing k^2-c unit squares: an upper bound of order k^{3/8} for the deficiency"
=====================================================================================================

(S. Ryu, version 1.0.) Section, table and lemma numbers refer to paper/paper.pdf of this release.
Run every command from the top folder of the repository (the folder that contains code/ and data/).
Requirements: Python 3 with numpy and mpmath; gmpy2 is optional (exact rationals gmpy2.mpq, faster). Without
gmpy2 the programs use fractions.Fraction; the results are the same (exact arithmetic).

1. Constants of the k^{2/5} theorem (Theorem 1.2; Corollary 7.4 and Section 7.3)
---------------------------------------------------------------------------------------------
code/const_stair.py  evaluates Phi(x) of Corollary 7.4 in interval arithmetic (mpmath.iv, 40 digits) at
                     x0 = 10^(-4/3) (b = 10^4) and at larger b, bounds Phi on all of [0, x0] by a subdivision into
                     4000 intervals (without the monotonicity argument of the proof), and certifies the constants
                     of Theorem 1.2: (20/3)(3/2)^(2/5) 5.03^(3/5) <= 20.6675, (8/3) 5.03 10^(-4/3) <= 0.6226,
                     (2 C_E/3) 10^(20/3) <= 1.6e7, and lambda' < 0.001.
                       python code/const_stair.py      -> last line "ALL CHECKS: True"   (about 2 s)
                     Recorded: code/checker_outputs/const_stair_stdout.txt and const_stair_out.json.

2. Certificates of Theorem 1.6 (Table 1, Section 9)
---------------------------------------------------
code/stair_dump.py   writes data/stair_k<k>.json.gz, the explicit packing of the square of side S = k - b + w
                     for given k, b, y0: the parameters k, b, y0, and for each of the four band ends (right band
                     and top band, bottom end and top end) its lift y, m, the tilt t = tan(alpha/2), cos alpha,
                     sin alpha and every piece as exact rationals: tilted columns (bottom-left vertex, n),
                     horizontal layers (left end, row j, length L) and left-wall rows (row h, length l).
                       python code/stair_dump.py <k> <b> <y0> [out.json.gz]
                       python code/stair_dump.py table data        (all five rows of Table 1, about 30 s)
                     The output is byte-identical with Fraction (Windows) and gmpy2 (Linux); checked for all five
                     files. This is the tuned staircase construction of Section 9 (m chosen per end among
                     floor(y + rho) and floor(y + rho) + 1 by a floating-point pre-run, tilt grid 2^-40, y0 near
                     0.9 b^(2/3)); it is not the construction of the proofs of Theorems 1.2 and 1.1,
                     and the certificates prove only the five bounds of Table 1.

code/stair_check.py  checker (c) of Section 9; it does not import the generator. From b alone it recomputes
                     the band, S (checks S < k), the numbers R of lifted rows of both bands and the upper lifts y1
                     (which must equal the lifts in the file); for every end it checks the shape of every piece, that
                     every vertex lies in Reg(y), and interior-disjointness of every pair of pieces with overlapping
                     bounding boxes by an exact separating-axis test; it recomputes N, c = k^2 - N and the waste
                     identity (Proposition 6.3) exactly. The rows and the L-shaped frame are proved in the
                     paper (Lemmas 3.3 and 6.1, Corollary 6.2) and are not re-checked;
                     c*(k) <= c - 1 then follows from Lemma 2.2.
                       python code/stair_check.py data/stair_k100000.json.gz 100000
                       python code/stair_check.py data/stair_k100000.json.gz 100000 mutate   (negative controls)

Expected results (recorded in code/checker_outputs/stair_check_k<k>.txt; every file ends with "OVERALL: PASS")

  k            b      y0       N                    c = k^2 - N   bound            exact pair decisions
  10^5         623    257/4    9999998416           1584          c*(k) <= 1583    22274
  10^6         2481   653/4    999999996027         3973          c*(k) <= 3972    119522
  10^7         9875   1663/4   99999999989960       10040         c*(k) <= 10039   969664
  3.825*10^7   22086  710      1463062499983011     16989         c*(k) <= 16988   2730501
  10^8         39314  1041     9999999999975209     24791         c*(k) <= 24790   5748521

  python code/stair_check.py data/stair_k1000000.json.gz 1000000
  python code/stair_check.py data/stair_k10000000.json.gz 10000000
  python code/stair_check.py data/stair_k38250000.json.gz 38250000
  python code/stair_check.py data/stair_k100000000.json.gz 100000000     (about 1 minute, 0.2 GB with Fraction)

In all five files: 0 shape failures, 0 containment failures, 0 overlaps, and the waste identity holds exactly.

Negative controls (mutate): one column moved right by 10^-6, one column moved down its slab by 10^-6, one column
given one more square, one layer raised by 10^-6, one layer lengthened by 1 to the left, one wall row lengthened
by 1, the region lowered by 1/100. All 7 are rejected for k = 10^5 and for k = 10^8 ("wrongly accepted: 0";
code/checker_outputs/stair_check_k100000_mutate.txt and stair_check_k100000000_mutate.txt).

Where and how long
  k = 10^5 and 10^6: generated and checked on a laptop (Windows, Python 3.12, fractions.Fraction), 0.3 s and 1.2 s.
  k = 10^7, 3.825*10^7, 10^8: generated and checked on a remote 8-vCPU Linux server (Python 3, gmpy2.mpq,
    one process per k), 3.8 s, 10.1 s and 13.2 s for the checks; recorded in stair_check_k<k>.txt.
  The three remote certificates were checked again on the laptop with fractions.Fraction, with the same results
    (stair_check_k<k>_fraction.txt; 8.2 s, 29.6 s, 59.2 s; at most 0.2 GB of memory).

SHA-256 of the data files
68d858032be5db1622ffeebeecf75caa8fcb4cd59e512bc6a54e16a146987a1c  data/stair_k100000.json.gz
6aeeb2e14b6a9b9f86b81d809d659e3d12e02aa9dfd62b9cdb0d5ad0f5b0dc19  data/stair_k1000000.json.gz
8e6e12d2a208f5ffbd9968843102041a1671abc013bcf071e6902ee659ec9212  data/stair_k10000000.json.gz
2a1e7bdca5be06168167cdb8dfd43bde299847fed4d84bed154ef86fa4f43a0a  data/stair_k38250000.json.gz
d4c76e64198c7b4782446a76916b687be694598a446827addc2f0001437918b2  data/stair_k100000000.json.gz

3. Constants of the k^{3/8} theorem (Theorem 1.1; Corollary 8.3 and Section 8.4)
---------------------------------------------------------------------------------------------
code/cert3e.py       interval certification (mpmath.iv, 120 bits) of Corollary 8.3 on a cover of the whole
                     range b >= 10^16: the variable z = m^(-1/4) in [0, z0] (z0 = 12^(1/4) 10^(-16/5), z = 0 included)
                     and t/z^2 in its admissible range are split into NZ x NT boxes; on every box it encloses the
                     margins of the hypotheses (E-i)-(E-v) of Lemma 8.2 (with (W1)-(W5) of Lemma 8.1 for the
                     three walls) and the normalised bound Psi = m^(-3/4) x (bound of Lemma 8.2), and prints
                     the smallest margins, Psi_sup, the worst box and C_E = Psi_sup 12^(-3/4)(1 + 60.000012 b0^(-4/5))^(3/4).
                     It was written by an independent reimplementation, from the text of the proof only, and is
                     included unchanged except for an internal file name in its first comment line (code
                     unchanged; the same holds for r38.py). It uses the relative slack 1.03e-12 on the wall tilts (Section 8, (E6)).
                       python code/cert3e.py 160 64   -> "all_positive": true, "Psi_sup" 96.4768..., "C_E_cert" 14.9636...
                                                        (about 30 s; it also writes code/cert3e_out_160_64.json)
                     Recorded: code/checker_outputs/cert3e_out_160_64.json (identical to the file the run writes)
                     and code/checker_outputs/cert3e_stdout_160_64.txt. C_E <= 14.964 <= 15.54 = the C_E of the paper.
                     Two further independent full-range coverings (not included) gave C_E <= 14.963 (mpmath.iv) and
                     C_E <= 14.9631 (python-flint arb). The inequalities evaluated are listed in Appendix A.
                     The margin (E-iv) is printed as 1 - eps_m; the bound eps_m + tau <= 1.03e-5 of the corrected
                     hypothesis (E-iv) is checked in the proof of Corollary 8.3 (iii).
                     Names in the comments of cert3e.py and r38.py: "Lemma W" = Lemma 8.1, "Lemma E" = Lemma
                     8.2, "Corollary 3E" = Corollary 8.3, "Theorem 4E" = Theorem 1.1;
                     ZC and E38 are the constructions of Sections 8.1 and 8.2 (h0 = chi, sig = zeta,
                     MU = varpi = 0.65, e = q, g = delta_Q, D = D_l, DR = D_r, W = w, and T = tan(theta), which is
                     mu in the paper).

4. Explicit validity check of the wall filler (Remark 8.4)
-------------------------------------------------------------------
code/r38.py          the wall filler ZC of Section 8.1 (and the end packing E38 of Section 8.2) in
                     exact rational arithmetic, the evaluation of (W1)-(W5) and B_W of Lemma 8.1 (interval
                     arithmetic), written by an independent reimplementation from the text of the proof only.
code/chk.py          generic exact checker for 1 x n rectangles in a convex polygon: shape, containment of every
                     vertex, and interior-disjointness of every pair with overlapping bounding boxes by an exact
                     separating-axis test (candidate pairs are found by bounding boxes only, with a float prefilter
                     whose margin 1e-6 is far above the float rounding error; no overlapping pair can be missed).
code/run_z.py        builds ZC on Z(chi, zeta, L) with chi = hc m^(3/4), zeta = sc/sqrt(m), L = m, initial tilt
                     t0 with tan(alpha0) = (3/2) sqrt(zeta) on the grid 2^-40, phase grid 2^-48, and (with "1") runs
                     the exact checker; prints one JSON line.
                       python code/run_z.py 10000 1 0.5 4     (about 10 s)
                     -> "fail": null, "blocks": 3, "hyp_ok": true, "res_le_eps": true, "U_exact": "6712",
                        "U_le_BW": true, cert "n_pieces": 25289, "n_exact_sat": 28402, "n_overlap": 0, "pass": true
                     Recorded: code/checker_outputs/wall_check_m10000_B4.txt (the timing fields t_build and t_check
                     differ from run to run).
                     Keys of "hyp" (lower bounds of the margins of Lemma 8.1): W1, W2, W3, W4 as in the paper
                     (W2 is (1 - varpi) tan(alpha0) - Delta_dr); "W5a" = varpi tan(alpha0) - delta_Q, the first half
                     of (W5); "W5b" = 0.21 - tan(alpha0) and "t0<=1/10", which together are the second half of (W5)
                     (t0 <= 1/10; the program checks both forms); "h0>=4" is the condition chi >= 4 on the region.
                     The keys are kept as the program prints them, so that the recorded output stays comparable.
                     This is an explicit check of validity at a small size; the asymptotic regime of Theorem
                     1.1 (b >= 10^16) cannot be tested by explicit computation.

Not included: the programs used for the exact checks of the construction of the proof of Theorem 1.2
(Remark 7.5), the author's own programs for Section 8, the reviewers' programs and the
other programs of the independent reimplementation mentioned in Remark 8.4.
