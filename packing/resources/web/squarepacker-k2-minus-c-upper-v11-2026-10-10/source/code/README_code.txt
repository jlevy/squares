Programs and data of "Packing k^2-c unit squares: an upper bound of order k^{3/8} for the deficiency"
=====================================================================================================

(S. Ryu, version 1.1.) Section, table and lemma numbers refer to paper/paper.pdf of this release.
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

2. Certificates of Theorem 1.6 (Table 2, Section 9)
---------------------------------------------------
code/stair_dump.py   writes data/stair_k<k>.json.gz, the explicit packing of the square of side S = k - b + w
                     for given k, b, y0: the parameters k, b, y0, and for each of the four band ends (right band
                     and top band, bottom end and top end) its lift y, m, the tilt t = tan(alpha/2), cos alpha,
                     sin alpha and every piece as exact rationals: tilted columns (bottom-left vertex, n),
                     horizontal layers (left end, row j, length L) and left-wall rows (row h, length l).
                       python code/stair_dump.py <k> <b> <y0> [out.json.gz]
                       python code/stair_dump.py table data        (all five rows of Table 2, about 30 s)
                     The output is byte-identical with Fraction (Windows) and gmpy2 (Linux); checked for all five
                     files. This is the tuned staircase construction of Section 9 (m chosen per end among
                     floor(y + rho) and floor(y + rho) + 1 by a floating-point pre-run, tilt grid 2^-40, y0 near
                     0.9 b^(2/3)); it is not the construction of the proofs of Theorems 1.2 and 1.1,
                     and the certificates prove only the five bounds of Table 2.

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

3. The parameter row v1.0 (version 1.0 of the k^{3/8} theorem; Corollary 8.10, row v1.0 of Table 3)
---------------------------------------------------------------------------------------------
code/cert3e.py       interval certification (mpmath.iv, 120 bits) of Corollary 8.10 for the row v1.0 on a cover of the whole
                     range b >= 10^16: the variable z = m^(-1/4) in [0, z0] (z0 = 12^(1/4) 10^(-16/5), z = 0 included)
                     and t/z^2 in its admissible range are split into NZ x NT boxes; on every box it encloses the
                     margins of the hypotheses (E-i)-(E-v) of Lemma 8.9 (with (W1)-(W5) of Lemma 8.1 for the
                     three walls) and the normalised bound Psi = m^(-3/4) x (bound of Lemma 8.9), and prints
                     the smallest margins, Psi_sup, the worst box and C_E = Psi_sup 12^(-3/4)(1 + 60.000012 b0^(-4/5))^(3/4).
                     It was written by an independent reimplementation, from the text of the proof only, and is
                     included unchanged except for an internal file name in its first comment line (code
                     unchanged; the same holds for r38.py). It uses the relative slack 1.03e-12 on the wall tilts (Section 8, (E6)).
                       python code/cert3e.py 160 64   -> "all_positive": true, "Psi_sup" 96.4768..., "C_E_cert" 14.9636...
                                                        (about 30 s; it also writes code/cert3e_out_160_64.json)
                     Recorded: code/checker_outputs/cert3e_out_160_64.json (identical to the file the run writes)
                     and code/checker_outputs/cert3e_stdout_160_64.txt. C_E <= 14.964 <= 15.54 = the C_E of the row v1.0.
                     Two further independent full-range coverings (not included) gave C_E <= 14.963 (mpmath.iv) and
                     C_E <= 14.9631 (python-flint arb). The inequalities evaluated are listed in Appendix A.
                     The margin (E-iv) is printed as 1 - eps_m, and the tilt condition of the walls as
                     1/10 - tan(alpha0) (the forms of version 1.0); section 5 below also runs the row v1.0 with the
                     forms 1 - eps_m - tau and 1/10 - t_up of version 1.1.
                     Names in the comments of cert3e.py and r38.py: "Lemma W" = Lemma 8.1, "Lemma E" = Lemma
                     8.9, "Corollary 3E" = Corollary 8.10 (row v1.0), "Theorem 4E" = the theorem of version 1.0 (Section 8.7);
                     ZC and E38 are the constructions of Sections 8.1 and 8.4 (h0 = chi, sig = zeta,
                     MU = varpi = 0.65, e = q, g = delta_Q, D = D_l, DR = D_r, W = w, and T = tan(theta), which is
                     mu in the paper).

4. Explicit validity check of the wall filler (Remark 8.13)
-------------------------------------------------------------------
code/r38.py          the wall filler ZC of Section 8.1 (and the end packing E38 of Section 8.4) in
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

5. The tiers of the k^{3/8} theorem (Theorem 1.1; Corollary 8.10, Table 3, version 1.1)
-----------------------------------------------------------------------------------------------------------
code/cert_v3/cert_v3.py      the author's interval covering (mpmath.iv, 120 bits) of Corollary 8.10 for every
                             parameter row. Mode "run" evaluates the boxes of the z-intervals iz0 <= iz < iz1 of one row:
                             on every box the margins 1/10 - t, (E-ii), (E-iii), 1 - eps_m - tau, and for each wall
                             (W1)-(W5), chi - 4 (key h0ge4) and 1/10 - t_up (key t0), and Psi; it prints one JSON line
                             (smallest margins, also as exact binary numbers, Psi_sup, the worst box and its split).
                             Mode "merge" checks that the slices of a row cover every box exactly once and with the same
                             parameters, and checks the stated constants in interval arithmetic. The tiers marked with a
                             dagger (parts "ABC") use the bound B_W'' of Lemma 8.5; the others B_W of Lemma 8.1.
                             The inequalities are listed in Appendix A.
code/cert_v3/finalize_v3.py  merges all slices, rounds the stated constants up (C_E to 3 decimals, C_i to 2 decimals,
                             k_i and a_i to 2 significant digits), writes tiers_v3_final.json and tiers_v3.json, re-runs
                             the merge with the theorem checks (merged_v3.json) and prints the tables.
code/cert_v3/tiers_v3.json   the tier parameters and the stated constants (C_E, C_i, k_i, a_i) of Theorem 1.1;
                             tiers_v3_params_only.json: the parameters alone, as used for the runs.
Both programs read tiers_v3.json from the current folder, so they are run inside code/cert_v3 (on Windows PowerShell
type "cd code/cert_v3" and the python command separately). The recorded slices were computed on an 8-vCPU Linux
server (python 3.12, mpmath 1.4.1), one process per slice, 55-110 s per slice there; on the author's laptop one slice
took about 100 s and the merge about 3 s:
  cd code/cert_v3 && python cert_v3.py run --tier B2 --nz 320 --nt 128 --iz0 160 --iz1 320 > c_B2_160_320.json
       (one slice; the same for every tier B1 B1s B2 A1 A1s A2 A3 A4 A5 and the slices 0-160 and 160-320;
        the output equals code/checker_outputs/cert_v3/c_<tier>_<iz0>_<iz1>.json apart from "seconds")
  cd code/cert_v3 && python finalize_v3.py ../checker_outputs/cert_v3
       -> prints code/checker_outputs/cert_v3/finalize_out.txt exactly (tables of tiers and theorem checks; theorem_ok
          True for all nine tiers); writes merged_v3.json (equal to the recorded one apart from the field "files",
          which contains the path separator of the system) and tiers_v3_final.json (equal to tiers_v3.json).
  cd code/cert_v3 && python cert_v3.py run --lb0 16 --params 1/12,4,4,1.5,0.65 --nz 160 --nt 64 --full 1
       (the row v1.0, regression; recorded: code/checker_outputs/cert_v3/regression_v10_160x64.json:
        Psi_sup 96.4768909805421, C_E_cert 14.963643923032722, as cert3e.py)
Expected (finalize_out.txt, Table 3 of the paper rounds Psi_sup and C_E^cert up and the margins down):
  B1 17.46022, B1s 16.96722, B2 16.72079, A1 18.96099, A1s 18.72102, A2 17.52222, A3 15.85845, A4 14.77799,
  A5 14.15237 (C_E^cert, upper bounds), all margins positive on all 9 x 40960 boxes.
The comments of cert_v3.py use the numbering of the write-up of the proof: "Corollary 3E'" = Corollary 8.10,
"Theorem 4E'" = Theorem 1.1, "Lemma W''" = Lemma 8.5, "Lemma P2" = Lemma 8.3, "Lemma P3" =
Lemma 8.4, parts "A" / "ABC" = the tiers without / with a dagger; h0 = chi, sig = zeta, MU = varpi, e = q.

6. Exact tests of version 1.1 (Remark 8.13, "Version 1.1 checks")
---------------------------------------------------------------------------
These are the programs of the exact tests (a)-(c) of Remark 8.13. They are tests at sizes far below b0, not
part of the proof. Each folder is self-contained (run from the top folder; Python puts the folder of the script on
the import path). They were run on the 8-vCPU Linux server; the recorded outputs are in code/checker_outputs/zc_tests.
cert.py in each folder is the generic exact certificate (shapes, containment, exact separating-axis tests for all
pairs with overlapping bounding boxes); r38.py is the program of section 4.

code/zc_tests/p3test/p3test.py   the wall filler ZC (r38.py) and ZC' (r38.py with the row rule (Z4') of Section
                                 8.2) on the canonical wall of run_z.py, the bounds B_W and B_W'' in interval
                                 arithmetic, and (last argument 1) the exact certificate of ZC'.
                                 usage: python code/zc_tests/p3test/p3test.py m sc hc aw mu docert
  python code/zc_tests/p3test/p3test.py 10000 0.5 4 3/2 0.65 1   (about 100 s on the server; recorded p3test/p3_2.json:
       U_ZC 6712, U_ZCp 6512, BW 19614.34, BW2 15969.29, cert all_pass true, 25290 pieces)
  The recorded runs p3_0 ... p3_7 are, in this order: (m, sc, hc, aw) = (3000, 2.45, 4, 3/2, cert), (10000, 2.45, 4,
  3/2, cert), (10000, 0.5, 4, 3/2, cert), (40000, 2.45, 4, 3/2), (160000, 2.45, 4, 3/2), (640000, 2.45, 4, 3/2),
  (2560000, 2.45, 4, 3/2), (10000, 2.45, 2.9, 5/4, cert), all with mu = 0.65.

code/zc_tests/e38_zc/a10.py      one end packing E38 (z38.py, ZC walls) in the window [cy b^(4/5), cy b^(4/5) + 2] with wall
                                 parameters (cD = cR, aw), at y = ceil(4 cy b^(4/5))/4 + offset, built in exact arithmetic
                                 and certified by cert.py, with the internal checks of run38.py.
                                 usage: python code/zc_tests/e38_zc/a10.py b cy_num cy_den cD_num cD_den aw off_num off_den
code/zc_tests/e38_zcprime/a10.py the same with every wall filled by ZC' (z38.py with the row rule (Z4'); three lines
                                 differ from e38_zc/z38.py).
  Recorded (code/checker_outputs/zc_tests/e38_zc and e38_zcprime; arguments b cy cD aw offset):
    a1_102400        102400 1/3 2.90865 1.13636 0          a5_102400   102400 1/3 2.86364 1.25 0
    a1_204800        204800 1/3 2.90865 1.13636 1          a1_409600   409600 1/3 2.90865 1.13636 7/4
    a3_102400_cy12   102400 1/2 2.61999 1.13 1/2           b2_orig_102400  102400 1/3 2.92683 1.26562 0 (ZC walls)
    b2_zcp_102400    102400 1/3 2.92683 1.26562 0 (ZC')    b2_zcp_204800   204800 1/3 2.92683 1.26562 1 (ZC')
    b1s_zcp_102400_cy12  102400 1/2 2.92683 1.26 1/2 (ZC') b2_zcp_25600_cy1  25600 1 2.92683 1.26562 3/4 (ZC')
  for example
  python code/zc_tests/e38_zcprime/a10.py 102400 1 3 292683 100000 1.26562 0 1   (about 3 minutes on the server;
       recorded b2_zcp_102400.json: "pass": true, U 12321.99998..., 121961 pieces, 0 overlaps)
  Every recorded run has "pass": true (0 overlaps, 0 containment failures, certificate U = construction U, internal
  checks true) and an aligned cut (tau > 0).

7. The tiers with a double dagger (C1-C3; Corollary 8.12, Table 4, Appendix B)
---------------------------------------------------------------------------------------------------------
code/cert_v4/cert_v4.py    the author's interval covering (mpmath.iv, 120 bits) of Corollary 8.12: the
                           inequalities of Appendix A for the rows with a dagger, with the replacements of
                           Appendix B (bound B_W4 of Lemma 8.8, margin (W6), 4.5002 and 2.500002,
                           one wall tilt factor per wall). "run" evaluates the boxes of the z-intervals iz0 <= iz < iz1;
                           "merge" checks the cover of all boxes and, with --stated C_E,C_i,k_i,a_i, the stated constants
                           in interval arithmetic (also lambda' < 1, the room conditions and k_i >= 10^12).
code/cert_v4/stated_v4.py  proposes the stated constants (rounded up) from a merge without --stated.
code/cert_v4/sl_t2_test.py exact random tests (not proofs) of Lemmas 8.6 and 8.11.
The certification runs were made on the author's laptop (python 3.12, mpmath; 120-135 s per slice of 160 x 128 boxes,
about 21 MB of memory). Run from the top folder of the repository:
  python code/cert_v4/cert_v4.py run --lb0 7.3617 --params 0.153846,2.81426,3.00931,1.26,1.3608,1.35403,0.65 --nz 320 --nt 128 --iz0 0 --iz1 160
       (slice 0 of C1, about 2 minutes; equals code/checker_outputs/cert_v4/10_C1_s0.json apart from the time;
        slice 1: --iz0 160 --iz1 320 -> 11_C1_s1.json)
  C2: --lb0 7.2  --params 0.16,2.81426,3.00931,1.26,1.3608,1.35403,0.65   -> 20_C2_s0.json, 21_C2_s1.json
  C3: --lb0 7.15 --params 0.165,2.81426,3.00931,1.26,1.3608,1.35403,0.65  -> 30_C3_s0.json, 31_C3_s1.json
  python code/cert_v4/cert_v4.py merge --stated 14.473,41.19,5.22e12,0.04 code/checker_outputs/cert_v4/10_C1_s0.json code/checker_outputs/cert_v4/11_C1_s1.json
       (less than 1 s; equals code/checker_outputs/cert_v4/C1.json apart from the field "files": "all_checks_true": true,
        C_E_cert 14.4725092..., stated 14.473, 41.19, 5.22e12, 0.04)
  C2: --stated 14.805,41.78,2.95e12,0.047 (-> C2.json);  C3: --stated 14.983,42.09,2.48e12,0.05 (-> C3.json)
  python code/cert_v4/sl_t2_test.py 3000 500
       (recorded code/checker_outputs/cert_v4/sl_t2_test.json: Lemma SL 3000 random cases and an adversarial family,
        0 failures, excess up to 0.9993-1.0000 of 1/(8 nu); Lemma T2 500 random bands, 0 failures)
Expected C_E^cert (upper bounds): C1 14.47251, C2 14.80459, C3 14.98288; C_i = 41.19, 41.78, 42.09; k_i = 5.22e12,
2.95e12, 2.48e12. cert_v4.py is included unchanged except for internal file names in its comments (code tokens
unchanged, checked by the build); the file used for the runs had SHA-256
d6004538e6cbb912730a662f53220947d14f1a4fe15f4712591b0fc2d6bf70ba.
SHA-256 of the recorded outputs (also in SHA256SUMS):
8f2f19eb7798adc9b5c18a300dd57c236d4ed2abd658014116a0b2f515730a1f  code/checker_outputs/cert_v4/10_C1_s0.json
1f80695454033529ec43e8d7c4339785c7a8c495fa225cac297ddd5cab899f51  code/checker_outputs/cert_v4/11_C1_s1.json
a489cec12c15aa9fc9761b8d246e6f42bb922d99421361ac2dbdeac421976e9e  code/checker_outputs/cert_v4/20_C2_s0.json
b0078dcef6affe5adae99ff1fc1a014de0fc688b665f19bb722ba6aabc7b24d0  code/checker_outputs/cert_v4/21_C2_s1.json
d82c4e3f4d6bffa413862e8b657c4a272b1de825e2d089b4610a6fea3fd83803  code/checker_outputs/cert_v4/30_C3_s0.json
a56aa1348613e80f817c453ca1132c385acca93e32908c8732a14bb557bfab27  code/checker_outputs/cert_v4/31_C3_s1.json
352519e989ca3029df5c042a03bfccb68dd25ad862fadd194d636a79ae0246e7  code/checker_outputs/cert_v4/C1.json
7441d2491e55f3667cd0c52d8887e5bd5471724eb49cee611accf15ee0e32e1f  code/checker_outputs/cert_v4/C2.json
101f7bc9cc7161d2e51e137e90d0666f72f8f00866d63071afa3ea656c2f6fca  code/checker_outputs/cert_v4/C3.json
4a802c8130f012f091d75167c47e50904f3f31b5bd847cef1033abd0cc52f8b8  code/checker_outputs/cert_v4/sl_t2_test.json
The comments of cert_v4.py use the numbering of the write-up of the proof: "Corollary 3E''" = Corollary 8.12,
"Theorem 4E''" = Theorem 1.1 (tiers with a double dagger), "Lemma T1" = Lemma 8.7, "Lemma W4" =
Lemma 8.8, beta_* = nu_* of (W6).

Not included: the programs used for the exact checks of the construction of the proof of Theorem 1.2
(Remark 7.5), the author's own programs for version 1.0 of Section 8, the parameter
search, the reviewers' programs, the programs of the independent coverings and of the independent reimplementations
mentioned in Remark 8.13 and at the end of the paper.
