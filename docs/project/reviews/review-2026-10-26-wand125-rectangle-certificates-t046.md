# wand125 Rectangle Certificates of 27 and 28 September: Review of T-046 and Its Census Route

- **Date:** 26 October 2026
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5-5`), at the strong sub-agent tier
  (`tbd-strong`) and the reasoning setting that tier’s harness sets, which the agent
  cannot read. Acting name `w-t046-review-1026`, the stage 4 review lane of bead
  `think-buaj`, for the intake coordinator `coord-n12-1025`.
- **Independence:** prompted separately from the lane that re-ran 22 of the census rows
  and ran all 46 controls on 25 October (`w-backlog-1025`, beads `think-kf3o` and
  `think-sb7a`), and sharing none of its context beyond the brief and the committed
  record. The same agent writes `T-046`’s records afterwards (`think-buaj`’s evidence
  entries and `think-wcex`), on the same branch, after this verdict was fixed.
- **Subject:** `T-046`’s 46 standing rectangle-density certificates (48 counts, n = 18
  to 95): the 36 of
  [wand125/square-packing-bounds at `39d8ecc`](https://github.com/wand125/square-packing-bounds/tree/39d8ecc74d651b54ec977c331c8f2015b442a6c4),
  retained in the packet
  [`wand125-rectangle-certificates-2026-09-28`](../../../packing/resources/web/wand125-rectangle-certificates-2026-09-28/README.md),
  and the 10 of `ad43d29` the same revision left unchanged.
  Also the widening of the census route’s mass condition to $n - 1/1000$ for
  `rect_n27_L56`, as section 5 of the
  [format T route review](review-2026-10-06-sqverify-fast-format-t-route.md) asks.
- **Read at:** `main` `91831e174`.
- **Verdict:** accepted.
  No finding blocks the records; one Low finding (T46-1) is about the generated entry
  text, and the records lane fixes it before the entries are entered.
- **Code:**
  [`review/review-2026-10-26/`](../../../packing/resources/web/wand125-rectangle-certificates-2026-09-28/review/review-2026-10-26/README.md)

This document registers nothing and moves no bound.

## Verdict

**Accept.** Each of the 46 certificates proves the bound `T-046` claims for its count,
and the masses of the n = 76 and n = 89 certificates carry those bounds to n = 77 and
90\. The mathematics is the certificate kind reviewed on 22 September, at the sizes
reviewed on 27 September and 2 October.
Nothing in the 28 September revision falls outside that envelope except one more
rectangle orbit count, n = 72’s 931 against the 926 of 2 October, which nothing depends
on. Every premise of the argument that is not coverage was recomputed here in exact
rationals from the retained files, and holds.

The census route carries to all 46. Each census row passes checks 1 to 6 and 8 of the
route review’s section 5, with the mass condition widened as section 3 below accepts.
This review’s own exact evaluator, written apart from the crate and from
`sqpack.rectangle_density`, reproduced every control receipt’s captures and every census
row’s least-bound leaf capture as rationals.
It also found no pose capturing less than $10001/10000$ among 38,916 it evaluated.

**The widening is accepted, and no further.** The theorem uses only $M < n$, which
admission recomputes.
The route’s condition should name the masses a review has read, $n - 1/100$ and
$n - 1/1000$, rather than drop the condition.

No verified lower bound moves: at every one of the 48 counts the case record already
holds a higher verified value.

## What Was Read and Run

**Read:**

- The 28 September packet’s README, acquisition record and preflight receipt, and the 27
  September packet’s README.
- `packing/sqverify_fast/SOUNDNESS.md`, The Claim, in full.
- The 22 September density mathematics review’s Mathematical Reduction, and the reviews
  of 27 September (checker scaling), 2 October (`T-068`’s certificates) and 6 October
  (the format T route) in full.
  For the build, the declared-net soundness review of 6 October only as the route review
  summarises it.
- `T-045`, `T-046`, `T-068`, `T-070` and `T-077` and their evidence entries.
- `tests/test_sqverify_fast_census.py` and `devtools/sqverify_fast_census.py`’s format T
  control and evidence code.
- `epistemics.md` (Confirmation, Review Records) and `result-import.md` stage 4.

This review did not read `sqpack.rectangle_density`, the crate’s `oracle.rs` or
`exact.rs`, or Tokoharu’s `verify.cpp` before its own evaluator agreed with the
receipts.

**Ran,** from `packing/` with CPython 3.14.7, five programs retained with
[this review’s code](../../../packing/resources/web/wand125-rectangle-certificates-2026-09-28/review/review-2026-10-26/README.md):

- **`certificates_t046.py`** reads all 48 retained candidates: the 46, and the two 28
  September certificates outside `T-046` (`rect_n21_L49875` and `rect_n77_L891`). It
  checks every premise but coverage in exact rationals, and the source’s accepting-run
  records against the preflight receipt.
  `PASS`, no problem, 6 s.
- **`route_t046.py`** checks section 5’s checks 1 to 6 and 8 on the 46 census rows,
  receipts and control receipts, and reads the case records.
  `PASS`, 0 failed conditions, 6 s.
- **`exact_capture_t046.py`** is this review’s exact evaluator, which `probes_t046.py`
  runs. `PASS`, 38,916 exact captures, 867 CPU seconds at two processes.
- **`rerun_t046.py`** re-ran six directions of four rows on a binary built here from
  `main`’s crate. That binary’s SHA-256 is `567a0fd5…`, the control build’s, bit for bit.
  `PASS`, 12 s.

The whole review cost about 40 CPU-minutes: the probes, which ran in full twice, and the
build of the binary.

## 1. The 28 September Certificates

**The argument is unchanged.** A certificate for count $n$ at side $L$ lists rectangles
$R_j \subset [0, L]^2$ with nonnegative rational weights $w_j$. Its density is
$g = \sum_j w_j / (8|R_j|) \sum_{S \in D_4} \mathbf 1_{S(R_j)}$, of total mass
$M = \sum_j w_j$. If at each of the 201 net half-angles $\theta_r = 2\arctan(83r/40000)$
every closed square of side $B = 9977/10000$ whose centre lies in Tokoharu’s domain
captures mass at least 1, the theorem of SOUNDNESS.md gives $s(n) \ge L$ whenever
$M < n$. The net, the shrink and the counting steps are the ones the 2 October review of
`T-068` sets out.
The accepting run and the census both decide coverage at $10001/10000$,
which only makes acceptance harder.

**Recomputed here, for each of the 38 retained candidates and the 10 read from the 27
September packet:**

- The stored file’s digest, its decompressed digest against the packet README and both
  packets’ upstream tree manifests, and the candidate’s own $n$ and $L$ against the
  directory name and `T-046`’s claim.
  JSON numbers are read as their literal decimals.
- $B = 9977/10000$, `rhs` $= 1001/1000$, the declared threshold $10001/10000$, and no
  point, segment or declared net.
- Every weight nonnegative and exact, every positive-weight rectangle nondegenerate and
  inside $[0, L]^2$, and the positive orbit count equal to the README’s.
- The mass as the exact sum of the weight strings: $n - 1/100$ for 45 of the 46, and
  $n - 1/1000$ for `rect_n27_L56` (and for `rect_n21_L49875`, outside `T-046`).
- Each scaling factor equal to its recorded quotient of target and source masses, and
  the target equal to the mass.
- The embedded and separate metadata equal, with the standard net, core, $\varepsilon =
  1/20000$ and smoothing margin.
- Each accepting run’s summary (`VERIFIED`, 201 angle cases, target $10001/10000$,
  checker `a75140df…`, the input digest) and its 201 per-angle rows: $r = 0$ to $200$
  once each, each `verified`, node and leaf sums equal to the summary, and every printed
  bound at least `up(10001/10000)` $= 1.0001000000000002$.
- The packet’s preflight receipt for the same certificate: `PASS`, with the same input
  digest, mass, side, orbit count, eight images per orbit and upstream node count.

The net identities hold exactly: $B(1 + D) = 399908091/400000000 < 1$, the smoothing
margin $399968091/400000000 < 1$, $t_{200}^2 + 2t_{200} - 1 = 89/40000 > 0$ and
$t_{200} = 83/200 \le 1/2$. $L^2 \ge 2B^2$ holds at every side.

**What is new since the reviews of 27 September and 2 October:**

| Quantity | 27 September, 44 certificates | 2 October, 37 certificates | The 36 here |
| --- | ---: | ---: | ---: |
| Side $L$ | $939/200$ to $1791/200$ | $1927/400$ to $9.8518$ | $143/25$ to $49209/5000 = 9.8418$ |
| Positive orbits | 135 to 812 | 223 to 926 | 179 to 931 ($n = 72$) |
| Expanded images, eight per orbit | up to 6,496 | up to 7,408 | up to 7,448 ($n = 72$; 7,396 distinct) |
| Weight scaling factor | $1.00052$ to $1.02659$ | $1.00004$ to $1.04329$ | $1.00030$ to $1.02697$ |
| Densest expanded image | — | — | $2^{10.9}$ to $2^{16.6}$ |
| Least printed leaf bound | $1.0001000003$ | $1.0001000000786$ | $1.000100000062878$ ($n = 57$) |
| Upstream nodes, all directions | — | — | 919,956,401 |

The sides stay in the binades $[4, 8)$ and $[8, 16)$ that both earlier reviews analysed.
The orbit count grows by five over 2 October.
Nothing in the method, the checker or the census crate depends on the count of orbits
except through running time and lemma F3’s caps (at most $10^6$ listed rows, the largest
file here lists 3,840), and the densest image is about $2^{16.6}$, against the route’s
ceiling of $2^{32}$ and lemma F3’s $2^{96}$.

**Scaling** is search provenance, as before.
Multiplying every weight by $f > 0$ multiplies the mass and every capture by $f$, and
both the accepting run and the census read the scaled file.

**The transfers by mass.** The mass of `rect_n76_L892` is $7599/100 < 77$ and that of
`rect_n89_L955` is $8899/100 < 90$. The theorem therefore applies to each certificate
with $n = 77$ (or $90$) directly: 77 (or 90) unit squares in the square of side $223/25$
(or $191/20$) would need mass at least 77 (or 90). `T-046` claims exactly these two, and
both census entries must state them (section 7).

**The records agree.** For all 36, the source README’s claims row, the candidate, the
metadata, the summary, the per-angle rows and the preflight receipt agree in every field
compared. The source’s own checker was replayed here in full on 18 of the 36
(`E-wand125-rectangle-2026-09-28-source-replay`). For the other 18, the census row is
the first confirming replay here: n = 28, 31, 37, 42, 43, 44, 54, 55, 56, 60, 66, 68,
70, 74, 76, 88, 89 and 94.

## 2. The Ten 27 September Certificates T-046 Still Cites

`rect_n18_L4695`, `rect_n19_L4815`, `rect_n20_L4895`, `rect_n26_L553`, `rect_n27_L56`,
`rect_n30_L5865`, `rect_n40_L6695`, `rect_n61_L796`, `rect_n75_L889` and
`rect_n78_L8955` are byte-identical at both revisions, and the 39d8ecc tree manifest
pins each. The 27 September scaling review read their metadata, summaries and per-angle
rows, and checked each candidate’s $n$, $L$, $B$ and `rhs` exactly; all ten were later
replayed in full with the source’s checker.
This review agrees that review read them, and read them again here by the same programs
as the 36, with the same result.
So one audit record serves all 46.

## 3. The Mass Condition at $n - 1/1000$

**What the route asks.** The test’s `format_t_problems` admits a format T row only at
mass $n - 1/100$, the mass of every certificate the route review read.
Of `T-046`’s 46, only `rect_n27_L56` has another: $26999/1000$, recomputed here from the
weight strings and equal to its census row’s `mass_exact`, with `mass_below_n` $1/1000$
and scaling factor $1.00090\ldots$.

**What the theorem uses.** Step N4 of SOUNDNESS.md: $n \le \sum_i \int_{Q_i} g \le M <
n$. Nothing else in the proof reads $M$. Admission refuses any file whose exact mass is
not strictly between 0 and $n$, recomputed from the weights.
It also requires a declared `total_mass`, if present, to equal that sum, and the
expansion to integrate back to it.
The threshold, the net and the centre domain do not depend on $M$, and neither do the
census driver’s control mutants, which scale the weights.
A mass of $n - 1/1000$ narrows the certificate’s slack in mass and changes nothing in
the argument.

**Where else the mass enters.** In the crate, the total mass is read only by admission
and by the premises it reports (`lib.rs`, `mass_exact` and `mass_below_n`); every other
`mass` there is one element’s. The driver never reads the gap.
The driver’s `rectangle_evidence_entry` prints the recorded mass rather than assuming
one; its docstring said $n - 1/100$ and is corrected on this branch.

**What the widening admits.** Three retained format T census rows have mass
$n - 1/1000$: `rect_n27_L56`, and `rect_n21_L4985` and `rect_n21_L49875`, which no
evidence entry cites and none will, since $s(21) = 5$ is settled.
A future citation of either still needs a review of its mathematics, which the test also
requires.

**The condition to write.** `FORMAT_T_MASS_GAPS = {1/100, 1/1000}`, held as $n - M$ in
that set. Dropping the condition to $M < n$ alone would also be sound.
It would, however, admit a mass no review has looked at, and the test’s purpose is to
list what the reviews read.

## 4. The Census Rows and Controls

All 46 pass checks 1 to 6 of section 5. In detail:

- **The case and the receipts.** Each row is `VERIFIED`, exit 0, at all 201 directions
  with none refused, at threshold $10001/10000$, and its least-bound leaf clears the
  threshold exactly. Each receipt has directions 0 to 200 once, each `verified` at the
  threshold. Its one summary is `VERIFIED` with no fault injected, with the row’s build
  and premises, and its node total and least bound are the row’s. The least certified
  bound of the 46 is $1.0001000000378$ ($n = 94$), and the least exact capture at a
  row’s least-bound leaf is $1.00108$ ($n = 38$).
- **The premises.** Format T, Tokoharu’s domain, the standard net and core, no point or
  segment, no declared net, metadata restating the standard net (`net_origin` `metadata`
  on the 25 October rows), and the densest image at most $2^{20.1}$ ($n = 19$).
- **The candidate.** `candidate_sha256` equals `premises.input_sha256` and the stored
  file’s SHA-256 in every row.
- **The build.** 24 rows were built from `9985c465…` (the source at `4ddf37d9c`) on 3
  October, and 22 from `d97758bb…` (`910b6b12c`) on 25 October.
  Both are in `REVIEWED_SOURCES`, release builds of rustc 1.98.0. All 46 controls ran on
  `d97758bb…`, binary `567a0fd5…`. The route review read the diff from `9985c465` to
  `d97758bb` and found the format T path unchanged (FT-8). The re-run of `rect_n72_L874`
  here, a 3 October row, on the later binary reproduced it field for field, as that
  predicts.
- **The controls.** Each is `CONTROLS_REFUSED` at $10001/10000$, receipt kind v1, with
  the selection rule’s fields: 200 centres weighed, index at least 1, the centre that
  direction’s least-bound box, and the crate’s and the independent captures equal.
  The original verified at exit 0. Both mutants were refused at exit 1 as
  `counterexample-candidate`, each with an exact capture below the threshold at the
  control centre itself.
  The control centres capture between $1.00054$ ($n = 19$) and $1.00950$ ($n = 60$).

FT-5 of the route review, a control at threshold 1 for a row recording none, no longer
arises: every row records its threshold, and `rectangle_control` now refuses a row that
does not.

**The six re-run directions** on the binary built here, one thread each, reproduced the
census receipts in every field but the timings:

| Certificate | Directions | Why |
| --- | --- | --- |
| `rect_n95_L98418` | 192, 200 | the largest side; a 25 October row; 192 is its least-bound direction |
| `rect_n72_L874` | 80 | the most orbits; a 3 October row; its least-bound direction |
| `rect_n27_L56` | 0, 197 | the $n - 1/1000$ certificate, at the axis and at its control direction |
| `rect_n94_L9795` | 193 | the least certified bound of the 46 |

## 5. This Review’s Own Captures

`exact_capture_t046.py` was written from SOUNDNESS.md’s density and the theorem’s
square, before its author read either evaluator it is compared with.
It expands each positive row into its eight images, each carrying $w/8$ uniformly, and
keeps coincident images apart.
It reads a JSON number as its literal decimal and a receipt’s pose as the exact value of
its binary64 number.
It takes the net’s cosine and sine as the rationals $(1 - t^2)/(1 + t^2)$ and
$2t/(1 + t^2)$, and clips the square against each image in exact rationals.

Per certificate, `probes_t046.py` checked:

- **The receipts’ captures.** The control centre’s, equal to both
  `exact_capture_independent` and `exact_capture_crate`. Each mutant’s at its refusal’s
  witness, as the factor times the original’s, equal to the receipt’s
  `capture_at_witness`. The census row’s least-bound leaf capture.
  All 184 equal as rationals.
- **FT-11.** The capture at all 200 oblique least-bound leaf centres: in every
  certificate the control’s index is the least, so the selection rule is as the receipt
  says. The route review checked this for one certificate only.
- **Sampled coverage.** The corner $(L - a_r, L - a_r)$ of the quarter domain at all 201
  directions, one seeded uniform pose per direction, and a seeded local search for a
  lower capture from the least of those poses and from the control centre.

The least exact capture found anywhere is $1.000512$ (`rect_n30_L5865`, found by the
local search from its control centre at direction 133, whose own capture is $1.000592$).
No pose captures less than $10001/10000$, so nothing sampled contradicts the census or
the accepting runs. A sample decides no direction; the census rows decide them.

The three-way agreement fixes the reading of the format.
`sqpack.rectangle_density` and the crate agree on it, but the crate’s authors read that
module. This evaluator was written without reading either, and agrees with both on 46
certificates: the literal decimals, the eight images with multiplicity, and $w/(8|R|)$.

**What the controls show.** Every mutant’s capture is below $10001/10000$ at the control
centre. Below 1, the 99/100 mutant’s witness is shown at 29 of the 46 and the
near-threshold mutant’s at 15. As the route review’s FT-9 says, these controls show
discrimination at the threshold, and discrimination near 1 rests on the crate’s own
tests.

## 6. The Values

At every one of the 48 counts the case record’s verified lower bound is above `T-046`’s
value, by $0.005$ ($n = 38$, `T-068`’s $1309/200$) to $0.18$ ($n = 90$). So check 8 is
met with no move: the census entries raise `T-046`’s rungs and no case record’s verified
field.

## 7. The Evidence Text

`--evidence` for `rect_n27_L56` was read against its receipts.
The identifiers, scope, source key, certificate path, both digests, $n$, $L$, the mass
$26999/1000$, the orbit and image counts, the axis vertices and least capture, the boxes
and least bound with index 179, the least-bound leaf capture, the CPU, wall and load,
the build and its review, the control index 197 and capture $1.0012693207$, both
refusals, and the independence statement all match.
It says no more than the receipts show, with one exception:

- **The route review’s re-runs (T46-1).** “The review of the format T route … re-ran
  three directions on a binary of the control build … and recomputed two receipts’
  captures” is true of `T-068`’s certificates.
  Here it reads as if it were true of this one.
  Name them as another result’s, and add what this review did for each certificate.

It also leaves out the census date.
The row of a certificate is either of 3 October or a re-run of 25 October, and `--date`
names the controls’ day only.
`T-046`’s notes should say which rows are which.
The scope is the certificate’s own count, so the two entries that carry $n = 77$ and
$90$ must have their scope widened and their theorem say so.

## Findings

No finding blocks recording the certificates or the receipts.

- **T46-1. Low, for the generated entry text.** The limitations sentence on the route
  review’s re-runs describes `T-068`’s certificates.
  Write it as another result’s, and add, per certificate, the checks of section 5 and
  any re-run direction.
- **T46-2. Note.** For 18 of the 46 certificates (section 1), sqverify-fast is the only
  replay here. The source’s own checker has not run on them, so their records are not
  reproduced. This does not change the rung, which one complete replay carries; it is the
  reproduction `next_rung` can name.
- **T46-3. Note.** The controls show discrimination at $10001/10000$; below 1, only part
  of them (section 5). This is FT-9 again.
- **T46-4. Note.** The census entries of `rect_n76_L892` and `rect_n89_L955` carry
  $n = 77$ and $90$ by mass, and the generator writes the certificate’s own count only.
  Widen both scopes and add the transfer to the theorem text.
- **T46-5. Note.** `--date` sets `source_reviewed` and the controls’ day.
  The 24 rows of 3 October and the 22 of 25 October are told apart only in the census
  rows’ builds and in the result’s notes.

## Claims by Evidential Status

- **Proved here in exact arithmetic:** the net, smoothing and reach identities; every
  mass, $n - 1/100$ except `rect_n27_L56`’s $n - 1/1000$; every scaling factor; the two
  transfers by mass; the agreement of every candidate with its pins, its README row and
  `T-046`’s claim; the receipts’ captures at 184 poses.
- **Computationally verified here:** coverage at all 201 directions of all 46, by the
  census rows (sqverify-fast, reviewed source, with controls), which this review read
  against section 5. It re-ran six directions with identical results.
- **Sampled here, deciding nothing:** 38,916 exact captures, none below $10001/10000$.
- **Reviewed by reading:** that the method, checker, net and constants are those of 22
  and 27 September and 2 October, and that the mass condition $n - 1/1000$ needs no new
  mathematics.
- **Asserted by the source and confirmed by the census:** the upstream accepting runs
  (summaries and per-angle rows read; reproduced with the source’s checker for 28 of the
  46).

## For the Records Lane

1. Map this review in `docs/project/document-map.yaml` and list it in `T-046`’s
   `reviews`: adversarial, accepted, covering `T-046`.
2. Widen `format_t_problems` to `FORMAT_T_MASS_GAPS = {1/100, 1/1000}`.
3. Generate each of the 46 entries with
   `devtools.sqverify_fast_census --evidence --only <name> --audit-record` this review
   `--date 2026-10-25`. Fix T46-1 and T46-4, and cite the entries on `T-046`.
4. Check 7 is this review.
   Check 9: each entry says *independently re-implemented*, and `T-046`’s `next_rung`
   plans no source-checker replay as the condition of the rung.
5. Let `devtools.check_results` derive the rungs.
   Expect `V3/C3`, with no verified bound moved.

## Disposition

`T-046` is accepted by this review with no defect open.
The 28 September report entry may record this review as its `external_review`
(`informally-verified`, 2026-10-26). With the census entries, `T-046` derives `V3/C3`,
confirmed, independently re-implemented.
`V4` and `C4` would need a second adversarial review by a distinct reviewer and a human
oversight record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
