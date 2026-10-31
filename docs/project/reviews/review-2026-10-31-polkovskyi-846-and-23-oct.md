# Review: Mykhailo Polkovskyi’s Certificates of 23 October and of Issue #846 (T-253, T-259)

> **Addendum, 31 October 2026 (the records lane, `bold-ritchie-l2`; A4 of the senior
> review of #852).** This review names register ids as #852’s branch registered them at
> `e2adcd8f7`: T-253 for the nine certificates of 23 October, T-254 for #843 and T-259
> for #846’s six. The ids follow #851’s T-252 and are not yet on `main`. After this
> review, the records lane split #846’s five sub-print counts, 105, 146, 156, 229 and
> 308, from T-259 into T-260, so that the owner’s question holds them alone.
> Where this review names T-259 at those five counts, read T-260. T-259 now holds 130
> alone. The review text below is unchanged.

**Date:** 31 October 2026. **Verdict: all fifteen certificates accepted, for finite
feasibility only. At 130 the certificate is accepted for adoption.
At the other fourteen counts adoption is the owner’s decision, because each of them is a
sub-print re-certification of the house certificate.** The certificates are Mykhailo
Polkovskyi’s (Mishapolk) `certificates/0000-0999/nN.cert` at
`Mishapolk/square-packing-records@52aa2672`. Nine were first published in the commits of
23 October `e386aab` to `6c0d74a` with no issue (T-253: 154, 155, 183, 211, 227, 236,
237, 241, 271), and six are reported by issue
[#846](https://github.com/jlevy/squares/issues/846) (T-259: 105, 130, 146, 156, 229,
308). Each proves $s(n) \le S_n$ at its header side: $n$ unit squares with pairwise
disjoint interiors in the closed box $[0, S_n]^2$. No square touches a wall and no two
squares touch.

A checker written for this review decides all fifteen on two exact routes, separating
axes and exact clipping area, which share only a reader.
It shares no code with the maintained routes or the source.
Both maintained routes were replayed in full here, all 81 jobs of both packets.
At all 15 counts the least wall clearance and the least pair gap the two maintained
routes report equal this checker’s exactly, and so do they at the twelve other replayed
entries of both packets: 108 of 108 numbers.
Sharp controls at $10^{-60}$ past exact contact, below every certificate’s margin
including 156’s $4 \times 10^{-41}$, are refused by both of this checker’s routes, and
exact contact is accepted.

**Every margin is padding.** At the nine T-253 counts each side is below its house by
$S_{\text{house}} \cdot 10^{-20}$, to within $5.2 \times 10^{-12}$ of that relative
figure. That is what re-dilating the house’s contact side from $1 + 10^{-20}$ (walls at
$5 \times 10^{-21}$, pairs at $10^{-20}$, as every house certificate here clears) to
about $1 + 10^{-30}$ gives.
At 105, 146, 229 and 308 every square is unchanged from the house and the side is
lowered by exactly $10^{-21}$, and at 156 by exactly $10^{-41}$. All fourteen of these
sides round up to the house’s 12-place print.
At 130 the certificate is $2.08 \times 10^{-12}$ below Francisco Couzo’s #843
certificate. It too is a re-solve at tighter padding (RV-6), but its print differs (…983
against …985), so the restatement ruling’s words do not reach it.

**Are the ~1e-19 refinements new results or restatements?** In substance they are
restatements. Each meets the ruling’s words (think-fwa9: below an earlier report by less
than one unit in the 12th place, with the same 12-place print), and none is a new
arrangement or a new contact side.
The record as written does not exclude them, though.
The ledger applies the ruling only beyond $n = 324$. Inside the corpus the record has
registered this class before (T-155, T-170, T-186, T-195, each scored S1 as padding),
and the owner’s 16 October words on T-195 point that way.
The ruling’s text and the runbook’s refinement bullet name no horizon.
That is a real ambiguity, so the decision is the owner’s (RV-1). This review reads it as
restatement, for the reasons in [The Restatement Question](#the-restatement-question).

Eleven findings are recorded, none blocking for any certificate.
RV-1 is major: it gates adoption at fourteen counts on the owner’s answer.

This is the Stage 4 mathematical review lane
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)) for
bead `think-ikku`, covering T-253 and T-259 as draft PR #852 registers them
(`claude/bold-ritchie-xo28us-upper`, head `e2adcd8f7`), at V0/C0. Neither entry is on
`main` yet. This review names both as that branch registers them, and it is to land with
or after that registration.
It was written by an AI reviewer of the Claude system family (Anthropic), lane
`bold-ritchie-rv-polk`, at the strong sub-agent tier (`tbd-strong`) and the xhigh
reasoning setting, as the coordinator launched it (RV-11). The lane was prompted
separately from the import lane that built the packets (`bold-ritchie-l2`). Its relation
to the result is `project`. It is read-only: it moves no rung, writes no register row,
adopts no house and edits no bead.

**For the author.** All fifteen of your bounds hold exactly at the sides your
certificates state, decided by programs that are not yours: this repository’s two
maintained routes and a checker written for this review.
At 130 your certificate is $2.08 \times 10^{-12}$ below Couzo’s #843, and it is recorded
as your refinement of his packing.
At the other fourteen counts, what your certificate gains on the record’s certificate is
that certificate’s safety padding, and nothing about the arrangement changes.
At 105 and 156 the record’s certificate is your own.
The repository’s ruling of 23 October treats such re-certifications as restatements
above $n = 324$, and the maintainer will decide whether it also applies inside 324. Your
issue’s table states larger improvements at 156, 229 and 308 than the record’s standing
sides allow (RV-7), and Questions 1 to 3 ask how three of the certificates were made.

## Verdicts by Count

| n | Entry | House it is compared with (holder of the certificate) | Verdict |
| ---: | --- | --- | --- |
| 130 | T-259 | T-254, Couzo’s #843 (Couzo; packing continuing PR #574’s) | **accept for adoption** |
| 105 | T-259 | T-229 (Polkovskyi’s own #719 file, `12fc466`) | **owner decision** (RV-1, RV-3) |
| 156 | T-259 | T-186 (Polkovskyi’s own 14 October file, `70a033f`) | **owner decision** (RV-1, RV-3) |
| 146 | T-259 | T-187 (Daniel, `e006ce6`) | **owner decision** (RV-1) |
| 229 | T-259 | T-225 (Daniel, `0075967`) | **owner decision** (RV-1) |
| 308 | T-259 | T-221 (Daniel, `bc0708f`) | **owner decision** (RV-1) |
| 155 | T-253 | T-197 (Daniel, `59326b8`) | **owner decision** (RV-1) |
| 211 | T-253 | T-188 (Couzo, `487b058`; Ostashev’s packing) | **owner decision** (RV-1) |
| 236 | T-253 | T-218 (Daniel, `5ad0069`) | **owner decision** (RV-1) |
| 237 | T-253 | T-190 (Couzo, `58a7833`; Chaoweeraprasit’s packing) | **owner decision** (RV-1) |
| 241 | T-253 | T-182 (Couzo, `b85dee2`; Ostashev’s packing) | **owner decision** (RV-1) |
| 271 | T-253 | T-219 (Daniel, `757b40b`) | **owner decision** (RV-1) |
| 154 | T-253 | T-222 (Daniel, `1d2bb82`) | **owner decision** (RV-1, RV-4) |
| 183 | T-253 | T-220 (Daniel, `3a9948c`) | **owner decision** (RV-1, RV-4) |
| 227 | T-253 | T-225 (Daniel, `0075967`; de Winter’s packing) | **owner decision** (RV-1, RV-4) |

“Owner decision” means the following.
The certificate has no defect.
If the owner keeps in-corpus sub-print re-certifications as recorded results, the
verdict at that count is accept for adoption, and no second review is needed.
If the owner extends the ruling to the corpus, the count is not recorded.
T-253 is then withdrawn, T-259 keeps 130 only, and the house is unchanged.
No count is rejected.

## Claims Covered

Exact sides are the certificate headers; each register claim equals its header exactly
(`rv_claims.py`). “Print” is the side rounded up at 12 places, which is what the ruling
compares.

| n | Entry | Exact side (header, decimal) | Compared with | Below it by | Print | Its print | Same print | Least wall / pair margin |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 154 | T-253 | 12.921100940761680549727… | T-222 | 1.292e-19 | 12.921100940762 | 12.921100940762 | yes | 5e-31 / 1e-30 |
| 155 | T-253 | 12.952260944650564035137… | T-197 | 1.295e-19 | 12.952260944651 | 12.952260944651 | yes | 5e-31 / 1e-30 |
| 183 | T-253 | 13.999580178736252501941… | T-220 | 1.400e-19 | 13.999580178737 | 13.999580178737 | yes | 5e-31 / 1e-30 |
| 211 | T-253 | 14.993549626299421038785… | T-188 | 1.499e-19 | 14.993549626300 | 14.993549626300 | yes | 5e-31 / 1e-30 |
| 227 | T-253 | 15.563625652325149084636… | T-225 | 1.556e-19 | 15.563625652326 | 15.563625652326 | yes | 5e-31 / 1e-30 |
| 236 | T-253 | 15.861934390607358617085… | T-218 | 1.586e-19 | 15.861934390608 | 15.861934390608 | yes | 5e-31 / 1e-30 |
| 237 | T-253 | 15.902603638259596880020… | T-190 | 1.590e-19 | 15.902603638260 | 15.902603638260 | yes | 5e-31 / 1e-30 |
| 241 | T-253 | 15.987117095150238758161… | T-182 | 1.599e-19 | 15.987117095151 | 15.987117095151 | yes | 5e-31 / 1e-30 |
| 271 | T-253 | 16.948947733713657510553… | T-219 | 1.695e-19 | 16.948947733714 | 16.948947733714 | yes | 5e-31 / 1e-30 |
| 105 | T-259 | 10.789303783742975392483… | T-229 | 1.000e-21 | 10.789303783743 | 10.789303783743 | yes | 4e-21 / 1e-20 |
| 130 | T-259 | 11.902430645982265758612… | T-254 (#843) | 2.083e-12 | 11.902430645983 | 11.902430645985 | **no** | 9.66e-15 / 1.82e-14 |
| 146 | T-259 | 12.583782190151860342291… | T-187 | 1.000e-21 | 12.583782190152 | 12.583782190152 | yes | 4e-21 / 1e-20 |
| 156 | T-259 | 12.979165853834276453836… | T-186 | 1.000e-41 | 12.979165853835 | 12.979165853835 | yes | 4e-41 / 1e-40 |
| 229 | T-259 | 15.650161513876431064008… | T-225 | 1.000e-21 | 15.650161513877 | 15.650161513877 | yes | 4e-21 / 1e-20 |
| 308 | T-259 | 17.997149121270908735152… | T-221 | 1.000e-21 | 17.997149121271 | 17.997149121271 | yes | 4e-21 / 1e-20 |

At each count the side compared with is the start the ledger froze at `main` `3978a7f61`
(`starts.yaml`), and at every count but 130 that start equals the house witness’s exact
side (`witnesses/known-best/n-NNN.yaml`) exactly.
At 130 the comparison is with Couzo’s #843 certificate
(`couzo-issue843-2026-10-28/source/certificates/n130.cert`), which the ledger records
first.

**Pins.** At all fifteen counts the retained file’s Git blob equals the blob at the pin
`52aa267` in a fresh clone of the source (`git ls-tree`, `git hash-object`), and its
SHA-256 equals the packet manifest’s (`acquisition/upstream-subtree.sha256`). The
source’s head is still `52aa267`. At each count the commit that introduced the pinned
blob is the commit the ledger reports it from: `6664afc` (154), `3d409a5` (155),
`fb8b812` (183), `e386aab` (211, 227, 237, 241), `c695b4c` (236), `6c0d74a` (271) and
`52aa267` (the six #846 counts).
Earlier files at the same paths, from `3285fac` (22 October), are other certificates.
At 105 that earlier file is T-229’s side, Polkovskyi’s own.
The commit times in the clone match the ledger’s `reported_at` to the second.

## Runs Here

Run on 31 October 2026 in a detached worktree of `e2adcd8f7`, CPython 3.14.7 from the
project’s `.venv`, under `nice -n 10` on a shared four-core host, at most two processes.
The worktree was removed after the runs.

| Command (from `packing/`) | What it decides | Outcome | CPU |
| --- | --- | --- | --- |
| `python -m devtools.acquire_source PACKET --check`, both packets | each packet against its acquisition contract | `PACKET_MATCHES_ITS_CONTRACT`, both | under 1 s |
| `python -m devtools.upper_bound_reports PACKET check-claims`, both | the frozen comparison rebuilt | equal to the retained `claims.json`, both | 3 s |
| `python -m devtools.upper_bound_reports mishapolk-1023-refinements-2026-10-30 check --replay` | all 39 jobs on both maintained routes, held to their retained rows | `13 certificates and 39 jobs admitted` | 243 s |
| `python -m devtools.upper_bound_reports mishapolk-issue846-2026-10-30 check --replay` | all 42 jobs on both maintained routes | `14 certificates and 42 jobs admitted` | 340 s |
| `python -m devtools.intake_ledger check campaign/issue-intake/upper-bounds-843-846-20261031` | the ledger against its inputs | `OK: 16 reports, 39 claims, 29 starts` | under 1 s |
| `python -I rv_check.py selftest` | this checker on 10 hand-built packings (contact, past contact by $10^{-30}$, rotated, corner and vertex-on-face) | 10 of 10 as required | under 1 s |
| `python -I rv_check.py check`, all 25 retained certificates | this review’s two routes | 25 of 25 accepted on both routes | 6 s |
| `python -I rv_controls.py`, the 15 counts | seven mutant families through both of this checker’s routes | 105 of 105 decided as required | 25 s |
| `python -I rv_identity.py`, the 15 counts | sides, prints, symmetry, moves, free play, against the packing compared with | tabulated below | under 1 min |
| `python -I rv_gaps.py`, both 130 certificates | the near-contact gap distributions | below | under 1 s |

The maintained replay’s margins were compared field by field with this checker’s: least
containment clearance and least pair gap, on each route, at all 27 certificates both
packets retain (two of them, 211 and 241, are the same blobs).
All 108 are equal as exact rationals.

## From Certificate to Bound

A certificate is a header `n S` and $n$ rows `x y t`, each a rational.
Square $k$ is the unit square centred at $(x_k, y_k)$ with axes $u_k = (c_k, s_k)$ and
$v_k = (-s_k, c_k)$, where $c_k = (1 - t_k^2)/(1 + t_k^2)$ and $s_k = 2t_k/(1 + t_k^2)$.
Since $c_k^2 + s_k^2 = 1$ exactly, every corner $(x_k, y_k) \pm u_k/2 \pm v_k/2$ is
rational, and the square is exactly a unit square.

The bound $s(n) \le S$ follows from two facts, each decided exactly:

1. **Containment.** Every square lies in $[0, S]^2$. Route A checks
   $x_k \pm (|c_k| + |s_k|)/2$ and the same in $y$ against $0$ and $S$. Route B checks
   all four computed corners.
2. **Disjoint interiors.** For convex polygons, interiors are disjoint exactly when some
   edge normal separates them (the separating-axis theorem).
   Route A takes, for each pair, the largest projection gap over the four edge normals
   $u_i, v_i, u_j, v_j$, which are unit vectors, so the gap is a Euclidean width.
   It accepts when that gap is at least 0. It tests every pair whose centres lie within
   $3/2$. Any other pair is disjoint, since each square lies in the open disc of radius
   $\sqrt 2/2$ about its centre and $3/2 > \sqrt 2$. Route B clips one square by the
   other’s four closed half-planes (Sutherland–Hodgman) and requires the exact area of
   the intersection to be 0, on every pair whose bounding boxes overlap with positive
   area.

Nothing else is assumed: no tolerance, no floating point in any decision, and no
statement of the source’s. The least pair margin route A reports is the separating-axis
width, which is at most the Euclidean distance.
The maintained routes’ “best pair gap” equals it at all 27 certificates.

## Trust Boundaries

- **This review’s checker** (`rv_check.py`) is about 240 lines of standard-library
  Python: `fractions.Fraction` and nothing else.
  Its two routes share the reader (`read_cert`) and nothing else.
  Its author read no code of the maintained routes, the source’s
  `verify_bound_certificate.py`, or `sqpack` before it decided (Disclosure).
- **The maintained routes**, `sqpack`’s rational witness verifier and the independent
  rational corner checker, share certificate parsing, half-angle conversion, `Fraction`
  arithmetic and the separating-axis method, as both packet READMEs say.
  They share the separating-axis theorem with this checker’s route A, but no code with
  it. Route B’s clipping area is a different theorem from all three.
- **The source’s checker** was not run, by this review or by the packets.
  Every statement the issue makes about it is the author’s.
- **Shared with every route:** the reading of the format (centre, half-angle tangent,
  unit side). That reading is fixed by the certificates’ own first line (“rotation
  $(c, s) = ((1-t^2)/(1+t^2), 2t/(1+t^2))$”). Under any other reading the squares would
  not be unit squares exactly.

## The Controls

`rv_controls.py` builds seven mutants of each certificate, each at exact contact and
$\varepsilon = 10^{-60}$ past it.
It runs them through both of this checker’s routes, on the whole packing and, for the
pair mutant, on the pair alone:

| Mutant | Required | Outcome, 15 counts |
| --- | --- | --- |
| side lowered by the least far-wall clearance | accept | accepted, both routes |
| … and $\varepsilon$ more | refuse | refused, both routes |
| least-left-clearance square moved left by its clearance | accept | accepted, both routes |
| … and $\varepsilon$ more | refuse | refused, both routes |
| tightest pair’s second square moved along its widest separating normal by the gap | accept | accepted, both routes, whole packing and pair alone |
| … and $\varepsilon$ more | refuse | refused, both routes, whole packing and pair alone |
| square 1 replaced by a copy of square 0 | refuse | refused, both routes |

The packets’ own receipts (`receipts/sharp-controls-nNNN.json`, 11 controls each on both
maintained routes, at $10^{-30}$) are `all_as_expected: true` at all 15 counts.
At 156 that epsilon is larger than the certificate’s margins, which are $4 \times
10^{-41}$ at the walls and $10^{-40}$ between pairs.
The controls here at $10^{-60}$ are below every margin (RV-8).

## Identity, Measured

`rv_identity.py` compares each certificate with the packing it is compared with.
It takes the best of the box’s eight symmetries by nearest centres, then measures moves
and turns (mod 90°), and, for each square that moves beyond $10^{-9}$, its exact free
play (least margin to any wall or neighbour) in both packings.
It measures; it decides nothing.

| n | Symmetry | One to one | Moved beyond 1e-9 / 1e-3 | Largest move / turn | Moved squares touching (free play ≤ 1e-9) |
| ---: | --- | --- | ---: | --- | --- |
| 105, 146, 229, 308 | identity | yes | 0 / 0 | exactly 0 / 0 | — |
| 156 | identity | yes | 0 / 0 | 0 / 7e-15° | — |
| 155, 211, 236, 237, 271 | identity | yes | 0 / 0 | ≤ 1.8e-15 / ≤ 7e-15° | — |
| 241 | identity | yes | 1 / 0 | 1.56e-6 / 7e-15° | 1 of 1 (free play 1.4e-12, both) |
| 154 | identity | yes | 60 / 47 | 7.79e-2 / 0.85° | 51 of 60 in the house, 55 in the certificate |
| 183 | identity | yes | 27 / 24 | 0.358 / 6.24° | 26 of 27, both |
| 227 | half turn | yes | 33 / 16 | 0.168 / 2.54° | 33 of 33 in the house, 24 in the certificate |
| 130 (against #843) | identity | yes | 14 / 0 | 1.13e-6 / 5.6e-5° | 12 of 14, both |

These agree with the packets’ `measure/identity-nNNN.json` and the entries’
`regularizations` (47, 24 and 16 squares beyond $10^{-3}$ at 154, 183 and 227; 0
elsewhere).
The packet numbers the symmetry at 227 as 2; in this review’s numbering it is
the half turn.

**The sides tell more than the poses.** At the nine T-253 counts the relative margin
$(S_{\text{house}} - S)/S_{\text{house}}$ is $9.999999999007 \times 10^{-21}$ to
$9.999999999052 \times 10^{-21}$. The figure predicted for the same contact side,
re-dilated from $1 + 10^{-20}$ to $1 + 10^{-30}$, is
$(10^{-20} - 10^{-30})/(1 + 10^{-20})$, and every count is within $5.2 \times 10^{-12}$
of it in relative terms.
Each house certificate clears its walls by exactly $5 \times 10^{-21}$ and its pairs by
$10^{-20}$ (`minimum_containment_clearance` in each witness).
That is consistent with a contact solution dilated by $1 + 10^{-20}$ about the origin: a
square at contact with the left wall, centre $1/2$, moves to $(1 + 10^{-20})/2$. These
certificates clear by $5 \times 10^{-31}$ and $10^{-30}$. The contact-determined side is
therefore the house’s to within $10^{-30}$ at every count, including 154, 183 and 227,
where tens of squares sit differently (RV-4). Those squares lie in a part of the packing
that does not determine the side.

At 105, 146, 229 and 308 every centre and every basis equals the house witness’s, digit
for digit. The side is lowered by exactly $10^{-21}$, which takes the far walls from
$5 \times 10^{-21}$ to $4 \times 10^{-21}$; the near walls and every pair gap are
unchanged, the least pair gap equal to the house’s as an exact rational.
At 156 the same holds at $10^{-41}$ against Polkovskyi’s own $5 \times 10^{-41}$
certificate.

**130.** Couzo’s #843 certificate and this one have the same contact structure within
$10^{-9}$: 304 near-contact pairs and 38 wall contacts each (`rv_gaps.py`). Couzo’s pair
gaps lie between $2.08$ and $2.60 \times 10^{-13}$ (median $2.16 \times 10^{-13}$) and
his walls clear by about $10^{-15}$. This certificate’s pair gaps are about
$2 \times 10^{-14}$ and its walls about $10^{-14}$. The $2.08 \times 10^{-12}$ gained is
about ten of Couzo’s pair gaps, the length of a chain across an 11.9 box.
So 130 is a re-solve of Couzo’s packing at tighter padding, like the others, and only
its size differs: it is large enough to change the 12-place print (RV-6).

## The Restatement Question

**The ruling.** The owner on 23 October (think-fwa9): “sub-print re-certifications are
RESTATEMENTS, not new rows.
The earlier certificate stays the row”.
The record states the rule as “A side below an earlier report at its count by less than
one unit in the 12th place, with both rounding up to the same 12-place print, restates
that report” (`intake_ledger.RULINGS["restatement"]`; `result-import.md` from line 486).

**These fourteen meet its words.** Each is below its house by $10^{-41}$ to
$1.7 \times 10^{-19}$, far less than $10^{-12}$, and rounds up to the house’s print
(Claims Covered). The house is a report and not a construction.
At 105 and 156 the house certificate is Polkovskyi’s own, which is the class the ruling
was asked about: a holder’s re-certification of his earlier report.
At the other twelve it is another holder’s, the class think-oqjd leaves open.
Measured, none is a new arrangement or a new contact side (Identity, Measured).
At 211 and 241, #846 names the same blobs, so a corpus-wide ruling would leave #846’s
claims there restating T-188 and T-182 as well.

**The record as written does not apply it here.**

- The ledger applies a ruling only beyond the horizon.
  `Ruling.applies` is `HORIZON < n <= through` (`devtools/intake_ledger.py`), and its
  docstring says the rulings are “an answer of the owner the walk then applies beyond
  the horizon”. Every count here is at or below 324, so the ledger records all fourteen.
  Its verdicts are correct as the code stands.
- The runbook introduces the rulings with “Beyond the corpus the owner’s answers of 23
  October 2026 are rules of the walk” (`result-import.md` line 480). Bead think-ikku
  says the answer “was given for rows beyond 324”, and every publication the question
  named (Couzo’s 74, #715’s 30, #732’s 499) is above 324.
- Inside the corpus the record has registered this class repeatedly: T-155, T-170
  ($1.08 \times 10^{-19}$, at 105), T-174 and T-186 (to $10^{-99}$) and T-195
  ($1.57 \times 10^{-36}$ at 29). The #719 review’s significance line scores all of them
  S1, “padding”. On T-195 the owner wrote “This should be built into our policy.
  It shouldn’t even be a question.”
  (16 October, quoted under the house rule).
- The think-fwa9 bead’s notes of 22 and 23 October raise the in-corpus class
  (Mishapolk’s #719 files at 42 Kingbird-house counts) and leave it “the owner’s
  question here”. The note recording the owner’s answer of 23 October lists only
  beyond-horizon publications among the verdicts it changes.

**Against that, three texts name no horizon.** The ruling’s own words have none, and
neither does the record’s statement of it in `RULINGS`. The runbook’s refinement bullet
says a refinement is recorded “unless it restates the report below the print”
(`result-import.md` line 468, added by `a84d549ad` on 23 October with the rulings), and
it too has no horizon.

**This review’s reading: restatements, if the owner agrees.** Four reasons:

1. **The margin is the house certificate’s padding, measured.** The bound is the house’s
   contact side at every count.
   Recording the difference records the padding policy of whoever certified last, not a
   packing.
2. **The series has no end.** Any certificate with positive clearance can be shaved.
   156 is the example: the house there is Polkovskyi’s own $5 \times 10^{-41}$
   certificate, and #846 lowers it by $10^{-41}$. At 105, 146, 229 and 308 the next
   $10^{-21}$ is just as available.
3. **Adoption changes little a reader sees.** Every print stays.
   At eleven of the fourteen counts every square stays within $1.6 \times 10^{-6}$, so
   the drawing cannot change.
   Bead think-ikku prices the regularization runs at 75 to 375 CPU-minutes for the
   fifteen counts.
4. **The author says what such rows are.** On #719 (comment 6350348588) Polkovskyi
   called rows of this kind “precision continuous Newton/SQP quenches of the predecessor
   reported topologies, optimizing wall clearances and contact gaps while preserving the
   underlying macro-layout”.
   That answer left their recording “to maintainer discretion”.
   #846 does ask for registration of its Category B, which #719 did not.

The other reading is consistent too: the house rule says “smaller is decided by exact
arithmetic, never by a print”, and T-195 was recorded and adopted on facts of the same
kind.
The owner’s two answers point opposite ways inside the corpus, so the choice is the
owner’s; the reading above is a recommendation, not a ruling (RV-1, Question for the
Owner).

## Report Order and Counts

The ledger (`upper-bounds-843-846-20261031`, `ledger.json`) has these steps at the
fifteen counts, and `intake_ledger check` passes:

- **T-253’s nine.** Each is the first and only report at its count after the frozen
  start, so each is recorded against its house.
  At 211 and 241, #846 (30 October) names the same certificates and is not recorded
  (`equal`).
- **T-259’s five sub-print counts.** #846 is the only report at each, recorded against
  its house.
- **130.** Two steps: #843 (2026-10-27T19:49:57Z, Couzo) recorded $2.05 \times 10^{-3}$
  below T-174, then #846 (2026-10-30T05:46:42Z) recorded $2.08 \times 10^{-12}$ below
  #843. Both times agree with the GitHub API. The 130 certificate’s blob was introduced
  at `52aa267` (2026-10-30T05:40:00Z), after #843, and its header says it is derived
  from a Couzo file, so the order cannot be the other way.
  At 130, T-259’s claim is a later refinement of T-254’s packing, and both are recorded.

The ledger’s counts for these two entries are right: 9 recorded for T-253, and 6 for
T-259, including 130. The ledger dates the nine T-253 publications by commit and did not
read the push (RV-9).

## Credit and Lineage

The entries credit each packing to its finder, as the house the certificate re-certifies
is credited, and Polkovskyi with the re-certification, as a regularization.
At 130 they credit Couzo’s #843 packing, refined by Polkovskyi.
The measurements support this.
Every certificate pairs one to one with the packing named (Identity, Measured), and the
source index’s own lines agree: “packing refined from Evan Daniel” at 154, 155, 236 and
271, and “from Evan Daniel & Francisco Couzo” at 183. Three refinements to the text are
proposed: RV-3 (105 and 156 are Polkovskyi’s own houses), RV-4 (the moved region at 154,
183 and 227) and RV-5 (130’s margin).

The issue credits “Mishapolk (Mikhail Polk) & Antigravity Autonomous Research Lab”, and
T-259 records that phrase.
Neither entry says what kind of assistance it names.
That is the author’s to state (Question 4).

## Significance

Both entries’ draft score, S1, is confirmed.
On the record’s line, padding is S1 (T-170, T-174, T-186), and every count here but 130
is padding, measured.
130 is a padding-scale re-solve that happens to cross the print (RV-6). It is not the
case of T-229’s 105, which was seven orders above its house’s padding, with 42 squares
beyond $10^{-3}$, and was scored S2. The rationales should say “padding” (RV-2), and
T-259’s should give 130’s margin against #843 (RV-5).

## Findings

Repository paths are at `e2adcd8f7`. In the source, at `52aa267`, square $k$ (numbered
from 0) is line $k + 3$ of a certificate.

**RV-1, major, owner decision; blocks adoption at fourteen counts, not any certificate:
whether the restatement ruling reaches the corpus.** At 105, 146, 154, 155, 156, 183,
211, 227, 229, 236, 237, 241, 271 and 308 the certificate meets the ruling’s words
(think-fwa9). The ledger records it because the ruling is applied only beyond 324
(`intake_ledger.Ruling.applies`), and in-corpus precedent records the class (T-155,
T-170, T-186, T-195). The evidence both ways is in
[The Restatement Question](#the-restatement-question).
Proposed: put the question to the owner before the adoption runs (Question for the
Owner). Adopt 130 now; it is outside the ruling’s words.

**RV-2, minor: neither entry says that the margin is the house certificate’s padding.**
T-253 says “each a re-certification of the house’s packing” and gives its significance
as “Smaller finite construction sides … 1.29e-19 to 1.69e-19 below the case ceilings”.
T-259’s `method` says “an exact re-certification below the house certificate’s side (the
source states no method)”. The measurement says more.
At the T-253 counts the side is the house’s contact side, with the house certificate’s
$1 + 10^{-20}$ dilation replaced by about $1 + 10^{-30}$; the relative margin is
$10^{-20}$ to within $5.2 \times 10^{-12}$ of itself.
At 105, 146, 229 and 308 the certificate is the house certificate with its side lowered
by exactly $10^{-21}$, and at 156 by exactly $10^{-41}$. Proposed: state this in each
`method` and in both significance rationales (“padding, as T-170”).

**RV-3, minor: at 105 and 156 the house certificate is Polkovskyi’s own, and T-259 does
not say so.** The 105 house is his #719 file (`12fc466`,
`[Mishapolk issue 719 2026-10-22]`). The 156 house is his 14 October KKT refinement
(`70a033f`, `[Mishapolk KKT refinements
2026-10-14]`). T-259 says “at 105, 146, 156, 229 and 308 the house packing each case
holds”. These two are the ruling’s own class, a holder’s re-certification of his earlier
report; only the horizon separates them from it.
Proposed: name the holder of the house certificate at each count in T-259, and put the
distinction to the owner (option (c) of the question).

**RV-4, minor: at 154, 183 and 227 the certificate is not the house’s poses.** 47, 24
and 16 squares move beyond $10^{-3}$; the largest move is 0.078, 0.358 and 0.168, and
the largest turn 0.85°, 6.24° and 2.54°. Most moved squares touch a neighbour within
padding (51 of 60, 26 of 27 and 33 of 33 in the house), so these are not rattlers but a
region that deforms without changing the side, which equals the house’s contact side to
within $10^{-30}$. The entries record the moved counts
(`regularizations[].identity.moved`), but the claim’s “each a re-certification of the
house’s packing” does not distinguish these three from the six pose-identical ones.
If the owner keeps these counts, adoption replaces the house drawing in that region.
Proposed: one sentence in T-253 at these counts, and Question 1.

**RV-5, minor: T-259’s significance rationale credits Couzo’s margin to the
refinement.** The rationale says “1.00e-41 to 2.05e-03 below the case ceilings”.
The $2.05 \times
10^{-3}$ is Couzo’s #843 against T-174; Polkovskyi’s certificate is $2.08 \times
10^{-12}$ below #843. Proposed: give 130’s margin against T-254, and Couzo’s against the
case ceiling separately.

**RV-6, note: 130 is also a re-solve at tighter padding, which the print test admits.**
The contact structure is the same (304 pairs and 38 walls within $10^{-9}$). Couzo’s
pair gaps of about $2.16 \times 10^{-13}$ become about $2 \times 10^{-14}$, and about
ten of them make the $2.08 \times 10^{-12}$. Fourteen squares move beyond $10^{-9}$, the
largest by $1.13 \times 10^{-6}$. The print changes from 11.902430645985 to
11.902430645983, so the ruling as worded does not reach it, and the verdict is accept
for adoption.
If the owner instead rules that any re-certification of the same packing is
a restatement whatever the print, 130 would fall too.

**RV-7, minor, for the author: #846’s Category B table overstates three margins.**
`ISSUE_SUBMISSION_CATEGORY_B.md` lines 19, 22 and 27 give the “Literature / Standing
Verified Bound” and ΔS at 156 as 12.979165853847 and $-1.298 \times 10^{-11}$, at 229 as
$-4.597 \times 10^{-13}$, and at 308 as 17.997149121289 and $-1.7998 \times 10^{-11}$.
Against the record’s standing exact sides the margins are $10^{-41}$, $10^{-21}$ and
$10^{-21}$, and at 156 the standing side is the author’s own certificate.
The packet already notes the table’s fractions at 204, 211, 241 and 268 that are not the
headers. No record depends on the table, since every comparison here reads the header.

**RV-8, note: the packets’ sharp controls at $10^{-30}$ are coarser than 156’s
margins.** The maintained controls show neither route accepts $10^{-30}$ past contact.
At 156, whose clearances are $4 \times 10^{-41}$ and $10^{-40}$, they cannot show the
routes are exact at the certificate’s own scale.
Both routes are exact `Fraction` arithmetic by construction, and this review’s controls
at $10^{-60}$ refuse past contact at all fifteen counts.
Proposed: where a certificate’s margin is below $10^{-30}$, `sharp-controls` takes an
epsilon below that margin, or the receipt says the epsilon exceeds it.

**RV-9, note: the nine 23 October publications are dated by commit; the push was not
read.** The runbook dates a watched publication “by the push that made that commit
public where the push came later”.
The ledger’s note says “its push is not read”.
This session could not read the source’s activity log (GitHub API access to that
repository is not enabled here).
No verdict depends on it.
No other holder reports at any of the nine counts between 2026-10-23T23:36Z and the
read, in this pass’s ledger or on `main`, and at 211 and 241 the only later report,
#846, names the same blobs.
A later push could move a row’s date, at most to 30 October.

**RV-10, note: the identity receipts print a zero displacement as `0.000000e+6`.** At
105, 146, 156, 229 and 308 `measure/identity-nNNN.json` gives
`"largest_displacement": "0.000000e+6"`, and both packet READMEs repeat it.
The cause is `_root` in `packing/devtools/check_half_angle_area.py:573`, which formats a
`Decimal` zero with `.6e`; Python renders `format(Decimal(0), ".6e")` as `0.000000e+6`.
The value is zero, but the text reads as a million to a hurried reader.
Proposed: print zero as `0`.

**RV-11, note, process: tier and retention.** The runbook runs this review at
`tbd-strong-max` at maximum reasoning.
This lane was launched as `tbd-strong`, and its reasoning setting was not stated to it.
The runbook also asks that the review’s programs be kept in the result’s packet and
registered in `verifiers.yaml`. This lane may not write the tree, so they are in its
scratch space (Files) for the records lane to retain.

## Questions for the Author

1. At 154, 183 and 227, which certificate did your solver start from, and which squares
   did it free? Tens of squares move by up to 0.36 while the side stays the house’s
   contact side.
2. At 105, 146, 229 and 308 (by $10^{-21}$) and 156 (by $10^{-41}$), is the certificate
   anything other than the record’s certificate with its side lowered and every square
   unchanged?
3. At 130, is `isolated_lab/tmp_couzo_noalm.txt` Couzo’s #843 packing, and was the
   $2.08 \times 10^{-12}$ gained by re-solving its contacts at tighter padding before
   the $2 \times 10^{-14}$ dilation?
4. What did the “Antigravity Autonomous Research Lab” contribute: an AI system, people,
   or both? The record states AI assistance where a source does.

## Question for the Owner

Does the 23 October ruling (think-fwa9, “sub-print re-certifications are RESTATEMENTS”)
reach counts inside the corpus, $n \le 324$?

- **(a) Yes.** The fourteen counts are not recorded.
  T-253 is withdrawn, T-259 keeps 130 alone, the houses stay, and no regularization
  runs. #846’s 211 and 241 restate T-188 and T-182. The ledger’s ruling gains a `through`
  that reaches the corpus, or the code a rule for it.
  The precedents T-155, T-170, T-186 and T-195 stand as recorded unless the owner says
  otherwise.
- **(b) No.** Record and adopt all fifteen as the ledger does, with both regularizations
  (75 to 375 CPU-minutes by think-ikku).
  The rule text says the ruling is beyond-horizon only, and the refinement bullet’s
  “unless it restates the report below the print” gains the same limit.
- **(c) Only a holder’s own re-certifications.** 105 and 156 are not recorded, and the
  other twelve wait on think-oqjd (another holder’s re-certification).

This review recommends (a), for the reasons in
[The Restatement Question](#the-restatement-question).
Under any answer, 130 is adopted.

## Rungs

**`V3`/`C3`, supported at all fifteen counts, independently re-implemented**, once the
records lane enters the replay evidence and maps this review.
Both maintained routes replay every job complete, and C3 needs one complete replay.
This review’s checker is a clean-room re-implementation on two routes, with sharp
controls refused.
The owner’s answer decides whether the fourteen rows exist, not whether
their certificates hold.
Under (a) those rows are withdrawn rather than raised.
Neither entry reaches `V4`/`C4`, which need a second accepted adversarial review by a
distinct reviewer and a retained human-oversight record.
No lower bound, optimum, local minimum, rigidity or priority follows.

## Proposed Record Changes

For the records lane; this review writes none of them.

- **Both packets.** Retain this review’s programs and outputs (Files) under
  `review/review-2026-10-31/` with a README, and register `rv_check.py` (decides) and
  `rv_controls.py`, `rv_identity.py`, `rv_gaps.py` and `rv_claims.py` (measure, decide
  nothing) in `verifiers.yaml` with the digests below.
  Independence record: `independent-implementation`, `clean_room: true`, `shares: []`,
  `read: [mathematics, certificate-format, earlier-review-method]`, written by a Claude
  agent (RV-11, Disclosure).
- **`evidence.yaml`.** The records lane’s confirming replay entries for both packets,
  with this review as `external_review` on `E-mishapolk-1023-certificate-report` and
  `E-mishapolk-846-certificate-report`.
- **`results.yaml`.** On T-253 and T-259, a `reviews` item naming this document
  (`kind: adversarial`, `reviewer_kind: ai`, `relation: project`, `verdict: accepted`).
  Method and significance text as RV-2, RV-3, RV-4 and RV-5 propose; S1 confirmed on
  both.
- **Adoption.** At 130, adopt T-259’s certificate and regularize it under the house rule
  (credit Couzo’s packing, refined by Polkovskyi).
  At the other fourteen, hold until the owner answers RV-1, then adopt or withdraw.
- **`devtools/check_half_angle_area.py:573`.** Print zero as `0` (RV-10), and re-render
  the five identity receipts.
- **`upper_bound_reports sharp-controls`.** An epsilon below sub-$10^{-30}$ margins, or
  a receipt that says it is above them (RV-8).

## Disclosure and Independence

Read before this review’s checker ran: both packet READMEs and declarations; T-253’s and
T-259’s register text; the ledger README, `ledger.json` and `starts.yaml`; the beads
think-ikku, think-pg1y, think-fwa9 and think-oqjd.
Also `result-import.md` (Stage 4, Several Reports at One Count, the house rule), and the
headers and first rows of the certificates as data.
It also read the first 160 lines of the 22 October review of T-229
(`review-2026-10-22-mishapolk-719.md`), as the brief’s model of the shape.
That passage describes that review’s checker as “integer separating axes and a
`Fraction` clipping area”, the pair of methods this checker also uses, and reports
T-229’s 105 margins.
The packet READMEs report the maintained routes’ method and margins.
Read after it ran: the outline, Findings and Rungs of the 23 October review of 204
(`review-2026-10-23-mishapolk-n204.md`), the outline of the 24 October review of 268 and
304, the significance section of the T-229 review, T-195’s and T-170’s register text,
the docstring and rule constants of `devtools/intake_ledger.py`, and `_root` in
`devtools/check_half_angle_area.py` (for RV-10). Never read: the code of either
maintained route, `sqpack`’s verifiers, the source’s `verify_bound_certificate.py`, and
any earlier review’s programs.
No earlier mathematical review of T-253 or T-259 exists.
The T-229 review covers the house at 105 and is consistent with this one: its
significance line (padding is S1) is the line used here.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty or priority, and no human
oversight. No run of the source’s checker or search.
No decision of the owner’s question: this review gives a reading, not a ruling.
No house adoption, case-record change or regularization, and no sweep of the source’s
live head beyond confirming it is still `52aa267`. No review of the counts the ledger
does not record (88, 126, 152, 182, 204, 260, 268, 270, 299, 304), though this checker
accepted every retained certificate at them.

## Files

Retained, with their README, in
`packing/resources/web/mishapolk-issue846-2026-10-30/review/review-2026-10-31/`, for
both packets.

- `programs/rv_check.py`: the checker, two routes, and `selftest`. SHA-256
  `b2bb8d68235945cc0b7cb122969a1bda350de18148f3dd6910f0f631580692b5`.
- `programs/rv_controls.py`: sharp controls,
  `8e3d24853c486e503dbfbb24ea21e414da87268e10f49e2b6fd13208fe4881de`.
- `programs/rv_identity.py`: sides, prints, identity and free play,
  `98117bcef8e95fd08fa9d873cc0ed0050deaf92708e512235e31ff1565d7ef37`.
- `programs/rv_gaps.py`: near-contact gap distributions,
  `a6cf233602e1b1af47e96e9a10943074cbf5c6152b2cb2026abca8ac308eeb00`.
- `programs/rv_claims.py`: register claims against headers,
  `406cf6adcd37468fd2ed0ac3d970c4433d9f019896776ace19f3771ba371660f`.
- `out/rv-check.jsonl`, `out/rv-controls.jsonl`, `out/rv-identity.jsonl`: their outputs.
  `out/replay-*.txt`, `out/claims-*.txt` and `out/ledger-check.txt`: the maintained
  runs. `out/program-digests.sha256`: the digests above.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
