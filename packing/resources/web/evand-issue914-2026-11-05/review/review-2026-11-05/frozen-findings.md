# Frozen findings: stage 4 review of issue #914 (bead think-lrj4)

Frozen on 2026-11-05 before reading the import lane's route receipts (`receipts/` in
either packet), its identity measurements (`measure/`), its ledger
(`campaign/issue-intake/upper-bounds-914-20261105/`), the two packet READMEs, the draft
register entries T-268 to T-273, and the earlier reviews of 31 October (T-257),
4 November (Özden) and 5 November (Yim).

Reviewer: Claude, as a separately prompted tbd-strong-max stage 4 review sub-agent at
maximum reasoning. Programs and receipts: `programs/` and `out/` beside this file.

## Seen before freezing

- The brief (beads think-lrj4 and its parent), which states the lane's figures: route
  totals, the clearances (5e-21 and 9.99e-21; at 260 4.98e-13 and 9.98e-13), the
  identity counts (60, 66, 42 and 33 against T-257, 80, 193, 124, 66; tilted squares
  48/50 ... 110/99), the views' and inputs' relations, and the issue's relationship
  numbers.
- The draft entry T-267 (`packing/frontier/results.yaml` lines 38923 to 39060 on the
  branch), read after this review's identity run; its notes summarise the lane's identity
  figures at 175 and its sharp-control design.
- Main's register rows for T-186, T-188, T-230, T-239, T-240, T-242, T-257, T-263, T-264
  and T-265, and the significance rationales of T-185, T-189, T-230, T-244, T-257 and
  T-265, which state the 31 October and 5 November reviews' significance conclusions.
- The 23 October review of T-239 (its identity section and RF-4) and the 16 October
  review's RT-1, read for the record's rule on refinements and arrangements.
- Packet A's `acquisition/sources.json` and the keys of `acquisition/report.json`.

## Per-count verdicts

| n | file | verdict |
| --- | --- | --- |
| 175 | s175_1105.cert, view s175_1105_regularized.cert | accept |
| 204 | s204_trig1.cert, view s204_trig1_regularized.cert | accept |
| 260 | s260_ks_1105.cert (no view) | accept with findings (F3, F4) |
| 268 | s268_1105.cert, view s268_1105_regularized.cert | accept |
| 293 | s293_1105.cert, view s293_1105_regularized.cert | accept |
| 303 | s303_1105.cert, view s303_1105_regularized.cert | accept |
| 304 | s304_1105.cert, view s304_1105_regularized.cert | accept |

No blocking or major finding. The bounds s(n) <= header side hold at all seven counts.

## Findings

**F1, note: all thirteen files are exact packings at their header sides.** Method A
(separating axes in `fractions.Fraction`) and method B (exact clipped areas in
`gmpy2.mpq`, its own corner construction) each decided every wall and every pair, with
no distance filter: 239,966 pairs over the seven certificates and 206,296 over the six
views, each by both methods, in three classes that agree pair by pair. Every pair is
strictly separated (no touching pair), every square inside. Least wall clearance exactly
1/200000000000000000000 = 5e-21 in the six KKT certificates and six views, and
4.98999...e-13 at 260 (square 258, right wall). Least pair gap 9.9999999999999e-21 in
the twelve (e.g. 175 pair 145 and 164), 9.98999...e-13 at 260 (pair 98 and 244). Every
square's clipped area is exactly 1. Self-test: 19 known answers, 3,000 random pairs and
6,000 pairs moved to exact contact and 1e-30 past it, both methods agreeing; the reader
refuses 14 malformed variants. Receipts: `out/feasibility/`, `out/self-test.json`.

**F2, note: the sharp and gross controls and the reversed sense come out as stated.**
Fourteen controls per file, each decided by both methods: the box at its extent (accept)
and 1e-30 below (refuse); the packing translated to the near walls (accept) and 1e-30
past each (refuse); the least-gap pair closed along its axis (accept) and 1e-30 past
(refuse); the least-clearance square moved to its wall (accept) and 1e-30 past (refuse);
a square of the least-gap pair enlarged by the least closing amount (accept) and 1e-30
more (refuse); a duplicate, a square centred outside, and every square turned to
t = 0, all refused. All 182 pass. Two of this review's own control constructions were
corrected before the final run and both earlier runs are kept: G2 first moved square 1
left by 1, which leaves it inside wherever it sits far from the left wall (both methods
accepted it, correctly); and the "1e-30 past" expectation at the least-gap pair was
first left unstated where two of the pair's axes are parallel. At 260 that expectation
is still unstated by the rule (squares 98 and 244 differ in angle by about 1e-13
degree); both methods refuse it, and the enlargement control at the same pair, whose
expectation is stated, passes. Reading every file with the rotation reversed (s -> -s)
makes all thirteen infeasible on both methods (69, 67, 173, 96, 76, 117 and 106
overlapping pairs in the certificates), so the header's convention is the one that
holds. Receipts: `out/controls/`, `out/reversed-sense/`.

**F3, minor: the 260 certificate dilates its binary64 input by 1 + 1e-12, not by
8.8e-12.** Its side is the input's stated side 16.6335209508719 times 1 + fl(1e-12),
rounded up at 30 places, exactly, and its centres are the input's times the same factor
to within 5.0e-31 in x and in y (a fitted map x' = alpha x + beta has alpha - 1 = 1.0e-12, |beta| <
1e-30); the certificate's first line says "delta 1e-12". The side is 1.66e-11 above the
input's. The issue's "dilates the f64 packing (by 8.8·10⁻¹²)" matches the side's
excess over the pre-descent input's stated side, 16.633520950879706 (8.83e-12). The
brief repeats "a dilation of its binary64 input by the issue's 8.8e-12"; wherever the
record says so, it should say "a dilation of its binary64 input by the factor
1 + 10^-12 (1.66e-11 in side)" and attribute 8.8e-12 to the issue. Question 1 asks the
author. Receipts: `out/sides-and-kkt.json` (input fit), `out/input-260.json`.

**F4, note: the issue's S' print at 260 is the side's binary64 value.** "S' =
16.633520950888535" is 1.48e-15 above the header side 16.633520950888533520950871899666
(its round-to-15-places would end ...534); it is the binary64 value. At the other six
counts the S' prints equal the header sides to all 30 places. The bound is the header
side, whose 12-place round-up is the issue's 16.633520950889. Also: the binary64 input
read exactly overlaps in 19 pairs by up to 3.9e-16 and reaches 8.3e-16 past its own
stated side, which is why it needs the dilation.

**F5, note: sides, prints and extents.** Each header side equals the claim fraction in
the brief; each rounds up at 12 places to the issue's print; each lies 5.0e-21 (plus the
30-place round-up, at most 9.2e-31) above the largest corner coordinate, and the least
corner coordinate is exactly 5e-21, so the corners span the side less 1.0e-20 in x and
in y; at 260 they span it less 1.0002e-12 in x and 1.0007e-12 in y (5.012e-13 at the
near walls, 4.990e-13 and 4.995e-13 at the far ones). Each view states its certificate's side exactly and has the
same 5e-21 margins. The issue's S* prints are prefixes of the 80-digit points.

**F6, note: the KKT certificates and the views are the 1 + 1e-20 dilations of their
points.** At 175, 204, 268, 293, 303 and 304, S' - (1 + 1e-20) S* lies in [6.7e-32,
9.2e-31] (the 30-place round-up), every centre is (1 + 1e-20) times the 80-digit
point's within 5.0e-36, and every angle 2 atan(t) is the point's within 5.7e-34 degree.
Each view is likewise (1 + 1e-20) times its JSON's regularized point (centres within
5.0e-36), and the regularized point's box is S* to within 5e-49 except at 303, where it
is 1.9066e-32 above S*, as the issue says, with (1 + 1e-20) S_reg <= S'. These are the
author's points read as data; KKT and local-minimum statements stay the author's.

**F7, note: none of the seven is one to one with its house; all are new arrangements.**
Measured against main's house witnesses (main 81f06acb3) under the box's eight
symmetries, by this review's Hungarian algorithm cross-checked against SciPy's optimal
cost:

| n | house | best symmetry | nearest centres one to one | distinct targets | beyond 0.1 | beyond 0.01 | largest | turned > 1 deg | tilted new/house | tilts reversed |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| 175 | T-186 | half turn | under none | 172 | 60 | 83 | 0.774 | 38 | 48/50 | 24 |
| 204 | T-264 | anti-transpose | under none | 202 | 66 | 126 | 1.032 | 51 | 63/76 | 0 |
| 260 | T-265 | identity | under none | 258 | 42 | 165 | 0.602 | 15 | 103/105 | 2 |
| 260 | T-257 | identity | under none | 256 | 33 | 160 | 0.633 | 15 | 103/104 | 2 |
| 268 | T-242 | half turn | under none | 264 | 80 | 139 | 1.072 | 80 | 98/81 | 29 |
| 293 | T-257 | anti-transpose | under none | 269 | 193 | 249 | 0.995 | 137 | 54/104 | 15 |
| 303 | T-240 | anti-transpose | under none | 298 | 124 | 144 | 1.104 | 125 | 112/102 | 42 |
| 304 | T-242 | identity | under none | 302 | 66 | 157 | 0.867 | 76 | 110/99 | 43 |

Box-centred assignments give the same counts within three. Calibration: the same
program finds T-264 one to one with T-257's 204 under the identity with 6 squares beyond
0.1 (largest 0.190) and T-265 one to one with T-257's 260 with 26 (largest 0.382), as
the register states, and main's 293 witness with the same poses as T-257's
s293_1028.cert. Under
the record's rule (one to one under a box symmetry: a refinement or a further
arrangement of that packing; otherwise another arrangement than it: T-230, T-239, T-264,
T-265), all seven are new arrangements, as the drafts say. Each certificate is one to
one with its binary64 input under the identity, row for row (largest move 1.41e-4 at
175, 303 and 304, 1.25e-6 at 204, 1.64e-7 at 293, 1.57e-8 at 268, 2.28e-11 at 260); each view
pairs with its certificate by the optimal assignment (half turn at 204, 293 and 303)
with 3 to 8 squares beyond 0.1, one to one by nearest centres except at 293. Tilt angles:
no tilted square of the new packing shares an angle (within 0.01 degree, up to sign)
with any of the house's at 175, 293, 303 and 304; at 204 five do and at 268 fourteen
(single-angle coincidences, not shared groups); the issue's "no shared tilt angle"
(on regularized views of load-bearing squares) is the author's. Receipts:
`out/identity.json`, `out/tilts.json`.

**F8, note: 260 is a new arrangement built on T-257's island, not a further arrangement
of T-257's packing; S3, not S2.** No box symmetry pairs it one to one with T-257's 260 (256
distinct nearest targets for 260 squares) or with T-265's; 33 squares move beyond 0.1
and 160 beyond 0.01 against T-257, where T-265, a further arrangement, moves 26 and 64
and pairs one to one. The 97 squares tilted beyond 10 degrees (63 at 24.50 degrees) form
T-257's island to within 0.042 (RMS 0.012, none beyond 0.1) only after a half turn about
the box centre and a shift of 1.0011 upward; in place, with the best translation, 26 of
them are beyond 0.1. So the island was turned and moved as a block and the 163-square
frame rebuilt around it, which is what "recomposed in a 260 frame" means; it is not a
deformation of T-257's packing. The record's reading is a new arrangement whose island
is T-257's, credited after T-257's lineage (Tymchishin's Kaggle start) as the issue asks,
and scored as a new arrangement 4.62e-4 below the house. Receipt: `out/island-260.json`.

**F9, note: the improvements are real against each house's precision and slack.** Exact
gaps below main's house sides: 1.24266e-4 (175), 3.25961e-3 (204), 4.61551e-4 (260),
1.86220e-3 (268), 1.09173e-2 (293), 5.14548e-3 (303), 5.95481e-3 (304); each house's
12-place round-up equals the issue's "best public bound before it". The houses' own
slack, measured exactly here (least wall clearance, least pair gap): T-186 3.6e-78 and
7.3e-78; T-264 1.0e-17 and 1.0e-17; T-265 0 and 1.3e-15; T-242 at 268 and 304 5e-21 and
1e-20; T-257 at 293 5.0e-13 and 1.0e-12; T-240 1e-15 and 2.1e-13. Every improvement
exceeds its house's slack by a factor of at least 1e10, and a unit in the 12th place by
at least 1e8. Receipts: `out/sides-and-kkt.json`, `out/slack-and-contacts.json`.

**F10, note: custody holds at bb4cc78.** This review fetched evand/square-packing at
bb4cc78e5b35103c1f177db55e9cf08974e66563 itself (blobless, through the session's git
proxy): authored and committed by Evan Daniel at 2026-11-05T18:29:13Z, tree 341f5ffb,
parent 39fb4f02 (the regularizer fix the issue names); it adds exactly 56 files, all
under search/packer/candidates/. The packet's 53 plain copies are byte-identical to
upstream and its three .json.gz files decompress to the upstream bytes; LICENSE (MIT,
"Copyright (c) 2026 Evan Daniel") and CREDITS.md are identical to upstream; the two
checkers at the pin are byte-identical to the n183 packet's copies (hashed, not read or
run). The thirteen SHA-256 digests in the issue equal the packet's and upstream's files.
The commit ends with a Co-Authored-By trailer naming Claude, and CREDITS.md says the
work was produced by Claude under human direction. The issue was opened at
2026-11-05T19:07:50Z and last edited at 21:18:34Z; this review read the edited body
(SHA-256 d3d3b498...), and its edit history is not readable from here. Receipt:
`out/custody.json`.

**F11, note: credit and lineage.** The credit the issue asks for (Evan Daniel, Chris
Deotte for the method at all seven; the register's 175 packing as the start; his own
s(233) and s(370) at 204; #845's island and Tymchishin's Kaggle s(260) at 260; donors
unrecorded at 268, 293, 303 and 304) is the author's own statement in the issue.
CREDITS.md and README.md at the pin do not name Deotte or the composer, so the record's
credit cites the issue. At 175, F7's measurement (not one to one, 60 squares beyond a
tenth, 24 tilts reversed) means the packing is no regularization or refinement of
T-186's: it takes no `regularizations` item and no "improved by" credit, only the "after"
credit for the start the issue asks for, as T-230's "after Ostashev" did for a new
arrangement found from Ostashev's packing.

**F12, note: S3 at all seven is confirmed.** All seven are new arrangements, 1.24e-4 to
1.09e-2 below their houses: at or above T-230's 1.86e-4 at 303 and T-257's 1.64e-4 at
293 (both new arrangements, S3) except 175's 1.24e-4, which is above T-189's 1.01e-4
(S3, a refinement) and far above the further arrangements scored S2 (T-188 9.29e-6,
T-239 9.89e-6, T-264 6.48e-6, T-265 1.99e-10). 260 is S3 by F8, not S2 as T-265.

## Questions for the author

1. At 260 the issue says the certificate dilates the f64 packing by 8.8e-12; measured,
   it dilates s260_ks_1105.input.txt by the factor 1 + 1e-12 (its side 1.66e-11 above
   the input's), and 8.8e-12 is its side's excess over the pre-descent input's. Which
   did the issue mean?
2. At 260 the S' print 16.633520950888535 is the side's binary64 value; the exact side
   is the header's 8316760475444266760475435949833/(5 * 10^29). Is that right?
3. At 260 the island matches #845's after a half turn about the box centre and a shift
   of one unit upward. Is that how the composer placed it?
4. Would you name the composer and Chris Deotte's method in CREDITS.md or a README, so
   the credit is in the repository's own attribution files as well as the issue?
5. The issue was edited at 21:18:34Z after it was opened; did the edit change a claim,
   a digest or a credit?

## Cost

About 0.19 CPU-hours: feasibility 106 CPU-s, reversed sense 107, controls 144 (and 289
for the two kept earlier runs), self-test 10, slack 3, identity, sides, tilts, island,
custody and the 260 input under 15.
