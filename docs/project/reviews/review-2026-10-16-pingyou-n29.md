# Review: PingYou Ltd’s Exact Rational Certificate for s(29) (PR #622)

**Date:** 2026-10-16. **Lane:** the review lane of the W2 phase that is stage 4 of the
[result import runbook](../../../packing/campaign/result-import.md#stage-4-validate),
for pull request [#622](https://github.com/jlevy/squares/pull/622), bead `think-2jzy`
under the import bead `think-30n2`. **Reviewer:** Claude, strong sub-agent tier, max
reasoning, prompted separately from the import and replay lane that wrote the records
pull request [#661](https://github.com/jlevy/squares/pull/661). **Verdict: accepted, for
finite feasibility only.** No blocking defect was found.

It covers the one claim of #622, $s(29) \le S$ for the exact rational side $S$ of
`n29-certificate/certificates/n029.cert.json`, and the register entry #661 adds for it,
named here by its pull request since it is not on `main` yet.
It re-derives the argument from the certificate to the claim, decides the certificate
with a clean-room program written for this review, reads the replay’s two routes and its
controls, and measures the certificate against the packings the record already holds at
29\.

**What this lane saw first.** Before its own checker had decided the certificate, it had
read its brief, which states the two margins #661 claims, and the import bead’s notes,
which report the replay’s outcome and its margins.
It had also read the packet’s README, which describes the source and summarizes the
replay. None of the replay’s code was open by then: `devtools.upper_bound_reports`,
`devtools.evand_arrangement_reports`, `sqpack`’s exact verifier, the independent corner
checker and the pull request’s tests.
Those were read after commit `918b0bd30` kept this review’s decision and controls.
No earlier review of this certificate exists.
The [review of PR #574](review-2026-10-14-upper-bound-imports-574.md) is of other
certificates; #574’s N29 row was never declared.
Its layout was read after this review’s findings were written.

## Summary

This summary is written for the author, PingYou Ltd.

**The certificate is valid.** Its 29 closed unit squares, at the stated rational centres
and half-angle tangents, lie in $[0, S]^2$ with pairwise disjoint interiors.
A program written for this review decided every wall and every pair over $\mathbb{Q}$:
116 wall constraints and 406 pairs, in 12 CPU seconds.
It is standard library only and never read your checkers.
One pair touches: squares 23 and 24, the limiting pair your provenance names.
Squares touch the box at 18 walls.
Every other constraint has at least $1.04 \times 10^{-800}$ of slack.
So $s(29) \le S$, where $S$ is a fraction of 2,399 and 2,398 digits,
$S = 5.93383346267692918968946061635201913843383418107788697463882\ldots$

**Your margins reproduce exactly.** $S$ is $1.566165818922113 \times 10^{-36}$ below
this project’s exact side for the packing (T-155). It is
$7.324826736065141 \times 10^{-90}$ below your PR #574 certificate at 29 and
$5.933833462698086 \times 10^{-20}$ below Evan Daniel’s certificate.
All three figures are truncated at 16 digits.
The exact side and the three exact gains in your `COMPARISON.json` equal the differences
computed here, fraction for fraction.

**It is the catalogue’s packing.** Measured square by square against the record’s
witness of Thomas Schadt’s packing as David Ellsworth improved it (T-009), the pairing
is one to one, by index under the reflection $y \mapsto S - y$. No square moves by more
than $10^{-9}$: the largest move is $7.7 \times 10^{-20}$ and the largest turn
$3.3 \times 10^{-38}$ degrees.
Against the catalogue’s own 100-place numerical coordinates, the largest move is
$8.8 \times 10^{-100}$. That matches your classification: a certificate refinement of
the known construction, not a new packing.

**The comparison with the catalogue’s exact value stays open.** $S$ lies
$9.19 \times 10^{-15}$ above the catalogue’s print `5.93383346267692`, 0.919 of a unit
in its last place. The record’s T-009 holds a Krawczyk enclosure of the solution of the
catalogue’s own closing equations, 1e-44 wide, which its witness records as existing and
unique; this review did not check that enclosure again.
It shows the print to be a truncation of that solution, and $S$ lies inside it.
So neither the print nor the enclosure orders $S$ and the catalogue packing’s exact
side. Since your certificate realizes that packing, $S$ is expected at or just above it;
nothing here proves that.

**Controls.** Every mutated certificate tried here was refused for the reason its
mutation should cause and for no other: a duplicated square, a square moved out of the
box, the touching pair pushed together by $10^{-3000}$, and the box shrunk by
$10^{-3000}$. At the coordinator’s request this repository’s third exact route also ran,
unchanged. It decides containment by half-extents and pairs by exact intersection area,
and it accepted the certificate in 30 seconds.
All six of its controls reached their required outcomes.

**No finding is in the certificate.** The findings below are about the record, and two
small notes and two questions are for you.

## 1. What Was Reviewed

- **The source.** Pull request #622 at `31155575ce1e6b461f77bfc9f3e201adf101115b`. Its
  HostedData manifest pins the release `data/pingyou-n29-certificate-2026-10-15-v1` of
  BuddenPing/square-packing-certificates.
  That tag resolves to `318ab94e…` by `git ls-remote`, read here on 16 October.
  This lane downloaded the asset `pingyou-n29-certificate-2026-10-15.zip` itself:
  430,075 bytes, SHA-256
  `0dc9bcd1cf5f2806a4d2e0c4c1c07e4903d91bbea611b8b938bda770b9782537`, the pin.
  Its certificate member has SHA-256 `a01428c5…`, the digest the claim record prints.
  Read by member name; nothing was extracted.
  Of its 34 members, the seven Python programs were left unopened.
- **The record.** PR #661 at `893a7a0b9`: the packet
  `pingyou-pr622-certificate-2026-10-15` (README, acquisition record, derived fact
  `facts/n-029.yaml.gz`, receipt `receipts/exact-certification.json.xz`), the per-count
  ledger `upper-bounds-n29-20261016`, the two evidence entries
  `E-pingyou-622-certificate-report` and `E-pingyou-622-exact-feasibility`, the register
  entry, the coverage, bibliography, request and deferral entries, the importer change
  and the two tests. Also read: the prepared adoption branch
  `claude/intake-2026-10-16-n29-622-adopt` at `90cce6258`, for its credit at 29 only.

## 2. Verdict

- **The claim holds.** $s(29) \le S$, finite feasibility only.
  Four exact routes accept it.
  This review’s program decided the certificate itself.
  The replay’s two maintained routes and this repository’s third route, run here at the
  coordinator’s request, decided the derived fact, which this review holds equal to the
  certificate, as the third route’s own readers do.
- **The margins hold**, as §6 states them.
- **The credit and the report order** are as §7 states them: Thomas Schadt’s packing of
  2025, as David Ellsworth improved it; PingYou Ltd’s certificate of 2026, assisted by
  the PY agentic offering; undecided against the catalogue’s value.
- **The replay’s controls are genuine and refused for the right reason, and they are
  gross** (§5).
- **The rung.** The entry should hold `V3`/`C3` once the stage 4 exit maps this review,
  and not before. §8 gives what that means for the order of merges.
- **The significance.** The draft `S1` is confirmed: a padding refinement of a packing
  the record holds, by $1.57 \times 10^{-36}$.
- **The house rule.** Once the exit maps this review, the entry is the smallest
  validated packing at 29, and the house selection takes it (§9).

## 3. From Certificate to Claim

### 3.1 The statement

$s(n)$ is the least side of a square that holds $n$ closed unit squares, each rotated
freely, with pairwise disjoint interiors.
A finite configuration with those properties in $[0, S]^2$ proves $s(n) \le S$, and
nothing about optimality.

### 3.2 The encoding

A pose $(x, y, t)$ is the closed unit square with centre $(x, y)$ and axes $u = (c, s)$
and $v = (-s, c)$. Here $c = (1 - t^2)/(1 + t^2)$ and $s = 2t/(1 + t^2)$, so
$c^2 + s^2 = 1$ over $\mathbb{Q}$, and every square is a unit square with no square root
needed. Its corners are $(x, y) + (a u + b v)/2$ for $a, b \in \{-1, 1\}$. This is the
asset’s `README.txt` statement, which the native corners witness and the replay’s
derived fact both encode the same way.
The half-angle tangent covers every rotation but a half turn, and a square is unchanged
by a quarter turn, so no orientation is lost; a rational $t$ gives a rational $c$ and
$s$. The program refuses any value that is not an integer or a fraction of integers.

### 3.3 Containment

A square lies in the convex box exactly when its four corners do, since the square is
their convex hull. The program checks all four exactly, 116 inequalities in all.

### 3.4 Disjoint interiors

For squares $Q_i$ and $Q_j$ the program asks whether one of the four axes
$u_i, v_i, u_j, v_j$ weakly separates them, with $\max_{Q_i} n \cdot z \le \min_{Q_j} n
\cdot z$ or the reverse.
A projection’s extremes are at corners.

- **Sound.** If an axis separates them, the interior of each square lies strictly on its
  own side of the line between them, since an interior point can move a little along
  $\pm n$ and stay in the square.
  So the interiors are disjoint.
- **Complete.** The difference body $Q_i - Q_j$ is a convex polygon whose edge normals
  are those four axes.
  The interiors meet exactly when 0 lies in its interior, which is when no edge’s
  supporting line separates 0 from it.
  So a pair the program refuses really overlaps, and a refusal of a control is evidence
  too.

### 3.5 What the claim needs, and what it does not

It needs only the stored rationals, the encoding above and exact arithmetic.
It does not need the decoder, the 800-digit realization, the minimal polynomial or the
comparison receipts, and none of them was read for the decision.

## 4. The Checkers and What They Share

| Checker | What it decides here | What it trusts | Who wrote it |
| --- | --- | --- | --- |
| This review’s `n29_exact_review.py` | the certificate, read from the asset by member | CPython 3.14.7’s integers and `fractions`, `json`, `zipfile`, `hashlib`; the encoding as the asset’s `README.txt` states it | this lane, from that statement and the certificate’s layout, clean-room: the source’s code was never read |
| `sqpack.witness.exact_verify` and the independent rational corner checker, through `devtools.upper_bound_reports` | the derived fact, in the replay of #661 | the fact’s derivation from the certificate (§5.1 holds it equal) and `Fraction` arithmetic | earlier Claude lanes of this project |
| `devtools.check_half_angle_area`, the third route, run unchanged by this review’s driver `third_route.py` | the derived fact, after its own readers hold the fact, the certificate and the corners witness to one packing | `Fraction` arithmetic, `sqpack.yamlio` | an earlier Claude lane of this project, which had read the two maintained routes |

All three share the mathematics of the encoding.
The two maintained routes and this review’s program decide pairs by separating axes; the
third route decides them by exact intersection area.
All share CPython’s rationals.
This review’s program shares no code with any other route or with the source.
It reads the certificate from the asset rather than from the derived fact, so it also
covers the derivation.

The source reports running the two maintained routes itself, unchanged at its base
commit, on its corners witness.
A fault in those two routes would therefore have misled the source and the replay alike.
This review’s program and the third route are the confirmations that share no code with
any check the source ran (§10, R3).

All three routes are Claude’s work, so the record’s authoring diversity is low.
The source names no system behind its agentic offering, so the overlap with the producer
is unknown.

## 5. Controls

### 5.1 The replay’s two

The receipt keeps each job’s exact checker input.
Decided again here from those inputs (`outputs/receipt.json`):

- **Positive.** Its input is the certificate exactly, side and all 29 poses.
- **Duplicate square.** Only square 1 changes, set to square 0. This review refuses it
  for pair (0, 1) alone at least gap $-1$, as both routes record.
  That is the right reason.
- **Square outside the container.** Only square 0 changes, moved by $S + 2$ in $x$. This
  review refuses it for square 0’s right wall alone at least clearance $-3$, as both
  routes record, with no pair touched.
  That is the right reason.

Both routes’ recorded least pair gap and wall clearance equal this review’s, fraction
for fraction, in all three jobs.
The test
`test_upper_bound_reports_622.py::test_the_receipt_holds_both_controls_refused_on_both_routes`
holds the reasons as well as the refusals.
It calls `check_certification`, which requires a negative pair gap for the first control
and a negative wall clearance for the second (`devtools/evand_arrangement_reports.py`,
the receipt check). So these are the two mutated certificates the runbook asks for,
refused by every checker that accepted the original, for the right reason, and held by a
test.

### 5.2 They are gross

A gap of $-1$ and a clearance of $-3$ are about $10^{36}$ times the margin to T-155. A
binary64 checker would refuse both.
They show that each route’s refusal path works.
They do not show that a route decides at the precision on which this certificate’s
margins rest. T-155’s replay ran tight forms on the same two routes.
T-174 paired the gross pair with the third route’s six sharp controls.
The replay entry’s own limitations say that “the kernel’s two controls are gross”.

### 5.3 Sharp controls run here

- **This review’s program** (`outputs/controls.json`). The touching pair, 23 and 24,
  pushed together by $10^{-3000}$ along their touching axis, is refused for pair (23,
  24\) alone. The box shrunk by $10^{-3000}$ is refused for the ten top and right wall
  contacts alone. The least positive slack is $1.04 \times 10^{-800}$, so neither
  perturbation can reach any other constraint.
  Both are invisible at any precision short of exact.
- **The third route** (`outputs/third-route.json`). The side at the far-wall contact is
  accepted, and $10^{-40}$ past it refused.
  The closest pair, already in contact, is accepted, and $10^{-30}$ of the centre
  distance past it refused.
  The duplicate and the escaped square are refused.

## 6. The Side Against the Record

Exact, from `outputs/sides.json`. Every figure in scientific notation is truncated at 16
digits.

| Comparator at 29 | Read from | Against $S$ |
| --- | --- | --- |
| T-155, the verified lane’s exact form | `packing/frontier/n-029.md`; T-155’s claim prints the same decimal | $1.566165818922113 \times 10^{-36}$ above |
| PR #574’s N29 side | the 14 October ledger’s `sources.yaml`, which the asset’s baseline equals | $7.324826736065141 \times 10^{-90}$ above |
| Evan Daniel’s certificate | the asset’s baseline | $5.933833462698086 \times 10^{-20}$ above |
| the Kingbird print `5.93383346267692` | `n-029.md`’s reported lane | $9.189689460616352 \times 10^{-15}$ below |
| T-009’s pose box for $s$, $[\ldots383418, \ldots383419]$ at 44 places | `packing/witnesses/kingbird-n029-2026-interval.yaml` | $S$ inside, $1.08 \times 10^{-45}$ above its low end |
| the house witness’s 100-place numerical side | `packing/witnesses/known-best/n-029.yaml` | $2.99 \times 10^{-100}$ above |

The asset’s three baseline certificates are each valid under this review’s program.
That includes #574’s N29 certificate, which the record never replayed.
The asset’s copy of T-155’s certificate has T-155’s side exactly.

`n-029.md` prints its verified value $5.43 \times 10^{-20}$ above its own exact form,
the defect `think-gzrw` owns.
These comparisons use the exact form, as #661’s do.

## 7. Provenance, Credit and the Report Order

- **Who submitted it.** The pull request comes from the GitHub account BuddenPing, for
  PingYou Ltd. The record credits the company by name and uses the handle only to say
  which account, as the ledger’s “PingYou Ltd (BuddenPing)” does
  ([epistemics.md](../../../epistemics.md#parallel-projects-and-their-credit)).
- **AI assistance.** The pull request makes no statement.
  Asked in the acknowledgement, the author answered on 16 October 2026: “All of our
  submissions are the same affiliation.
  PingYou Ltd, assisted by the PY agentic offering”
  ([comment](https://github.com/jlevy/squares/pull/622#issuecomment-6207551818)). That
  covers this certificate, and the entry, the packet and the bibliography quote it.
  The source names no system behind the offering, and the record should not guess one.
- **Who found what, and when.** The packing is Thomas Schadt’s, found in 2025 and
  improved by David Ellsworth.
  That is how the Kingbird catalogue credits it and how `n-029.md`’s reported lane
  records it, and the measured identity (§10, R5) shows the certificate is that packing.
  The certificate is PingYou Ltd’s, published on 15 October 2026: an exact rational
  refinement, credited as a regularization of the packing T-009 holds.
  Evan Daniel is credited for the source tools and data among its stated inputs, as the
  source asks. The bibliography’s “PingYou Ltd after Schadt, Ellsworth, Daniel, Levy”
  follows the source’s own credits and the earlier PingYou entries.
- **The report order.** Two reports state a bound at 29, both PingYou Ltd’s: PR #574’s
  N29 row, first committed on 13 October 2026, and #622, opened on 15 October.
  Both are undecided against the reported lane (§6). #622 is decided below #574’s row
  and below T-155. So the owner’s report-order rule records neither by itself.
  #622 is recorded on a key reason, the owner’s house rule of 16 October 2026, which the
  ledger lists as the candidate and which this pass’s coordinator reads as settling it.
  The entry’s notes still say that the owner confirms or withdraws that reason; they
  should cite the owner’s word once it is on file.

The record may state:

- $s(29) \le S$, by a complete rational certificate replayed here, for finite
  feasibility only;
- that $S$ is $1.57 \times 10^{-36}$ below T-155 and $7.32 \times 10^{-90}$ below PR
  #574’s N29 certificate, both decided exactly;
- that against the catalogue’s `5.93383346267692` the order is undecided.
  $S$ lies 0.919 of a unit above the print and inside T-009’s enclosure of the
  catalogue’s exact side, and is expected at or just above that side;
- that the certificate is the catalogue’s packing, measured square by square, with
  PingYou Ltd credited for the certificate refinement, assisted by the PY agentic
  offering.

It may not state that #622 improves on the catalogue’s value or the reported lane.
Nor may it call the certificate a new packing, a new record at 29, or the smallest
report by the rule alone, or claim any optimality, local minimum or rigidity.

## 8. The Rung

**What the evidence supports.** The replay is exact, replayed here, complete over the
one certificate and passing, so its evidence derives `V3`/`C3`. This review is one
accepting adversarial AI review.
It moves no rung by itself: `V4`/`C4` need a second such review by a distinct reviewer
and a human oversight record ([epistemics.md](../../../epistemics.md#review-records)).
With both lanes, then, the entry holds `V3`/`C3`, and its `next_rung` should say what
rung 4 still needs.

**What #661 declares now.** #661 declares `V3`/`C3` on the replay alone, before this
lane returned. The runbook’s exit adds the replay evidence after both lanes.
PR #651’s review A2 asked T-193 to be held at `V0`/`C0` for the same reason, and the 14
October imports waited the same way.
#661 tried that hold (`f6929451a`) and reverted it (`58de4dedc`). Held, the entry is
compared with the reported lane alone.
The standing logic reads the 14-place print there as an exact number below $S$, and so
derives “superseded” with no superseding result, which the status test refuses.
The ledger rules that same comparison undecided.
The hold fails on a reading of the print, not on anything about the certificate.

**What should hold.** Since the hold is blocked, `V3`/`C3` before the exit is acceptable
only if `main` never carries it without the review.
At `893a7a0b9`, `check_requests --report` already reads #622 as settled and closeable,
and the entry as confirmed.
That is the risk A2 named: a reply or a closure that says “confirmed” before any review.
The safe order is to merge this review’s pull request into #661’s branch, make the exit
there, then merge #661 once.
Short of that, merge the two back to back, with no reply, closure or site deployment in
between. After the exit the entry stays `V3`/`C3`, its review on file.

## 9. The House Rule at 29

The owner, 16 October 2026: “We should always be adopting the smallest packing and then
regularizing it.” Once the exit maps this review as accepted, the entry meets every
condition of `devtools.select_houses`. It is at `V3`/`C3`, carries an accepted review,
cites confirming evidence, and has a house reader, which #661 adds.
Its side is below the case’s verified ceiling, T-155’s exact form, by
$1.57 \times 10^{-36}$.

It is also below every other certificate of the packing that the record or the source
holds at 29:

- T-009’s interval endpoint, $5.4 \times 10^{-20}$ above $S$;
- Evan Daniel’s certificate, $5.9 \times 10^{-20}$ above;
- PR #574’s N29 certificate, $7.3 \times 10^{-90}$ above, which the record neither
  registers nor replays.
  T-174’s houses are held for the owner in any case.

The catalogue’s print is below $S$ as a number, but it is no validated packing.
The record holds no certificate at it, and the certificate measured here is that very
packing. So the entry is the smallest validated packing at 29, and under the house rule
it is adopted and its witness regularized.
Today `select_houses` takes no candidate at 29, because no review is mapped.

Two consequences for the adoption:

- **The drawing.** The new witness is the catalogue’s packing with its rattlers where
  the catalogue puts them.
  T-155’s view had moved three of them, by up to 0.0124 (`outputs/identity.json`), so
  the regularized drawing lapses and owes the strong runs.
  The prepared adoption branch reports running them.
- **The credit.** That branch credits the packing to Thomas Schadt, as David Ellsworth
  improved it, and the certificate to PingYou Ltd.
  That is right. But its writer takes `found_year` from the certificate’s date, 2026, and
  the packing is Schadt’s of 2025 (R6).
- **The prose.** The adoption’s template says that “a third exact route, half-extent
  containment and exact intersection area, decided it again”.
  That is now true (§5.3). The sentence may stand once the exit cites the run,
  `outputs/third-route.json`, in the replay’s evidence entry with
  `V-check-half-angle-area` among its verifiers.
  Without that citation it must go.

## 10. Findings

Graded blocking, major, minor or note.
None is blocking, and none is in the certificate.

### R1. The rung is declared before the exit (minor, for the record)

`packing/frontier/results.yaml`, the entry’s `verification: V3` and `confirmation: C3`,
citing `E-pingyou-622-exact-feasibility`; and `packing/campaign/result-requests.yaml`,
#622’s `register` and `evidence` mapping.
§8 gives the order of merges under which this is acceptable.
The standing logic’s reading of a reported print as exact is worth a bead of its own.
The next unreplayed entry whose case prints its reported lane within one unit of the
entry’s side will meet the same obstacle.

### R2. The stage 4 exit is owed (minor, for the record)

Until the exit lands, the house selection takes no candidate at 29, and the entry’s text
says no review is on file.
The exit writes:

- the entry’s `reviews`: this document, kind `adversarial`, reviewer `ai`, relation
  `project`, verdict `accepted`, scope finite feasibility at 29;
- `external_review` on both evidence entries;
- a rewritten `claim`, `notes` and `next_rung`, with no sentence saying a review is
  pending;
- `activity` removed, or pointed at what is still under way;
- the deferral’s `blocked_on` updated;
- the measured identity (R5);
- this review’s programs registered, and the third route’s run cited in the replay
  evidence (R3, R4).

### R3. The independence label rests on routes the source also ran (minor, for the record)

`packing/frontier/evidence.yaml`, `E-pingyou-622-exact-feasibility`:
`relationship_to_generator: independent-implementation`. The entry’s claim sentence
reads “the source’s runs of this repository’s two maintained routes … decide nothing
here, so the replay is independently re-implemented”.
The request report prints “re-verified here by an independent implementation
(sqpack.verify, …)”. But the source reports running those very routes, so the replay
cannot rule out a fault the two routes share with the source’s own check.
T-174 is labelled the same way, which makes this a precedent rather than a slip.
The exit can make the sentence true: rest it on the third route’s run and this review’s
clean-room program, which share no code with any check the source ran.
Alternatively, it can say that the two routes reproduce the source’s own runs of them.

### R4. The replay’s controls are gross (minor, for the record)

§5.2. Cite the sharp controls that did run, the third route’s six and this review’s two.
The kernel could also take the tight forms T-155’s replay used.

### R5. The identity is left as the source’s word (note, for the record)

The entry’s `regularizations` item at 29 has `of: T-009` and `identity.basis:
source-claim`. Measured here against T-009’s witness: one to one by index under
$y \mapsto L - y$, no square moved beyond $10^{-3}$, largest move 7.685e-20, largest
turn 3.255e-38°. The exit can record `basis: measured` with those figures, pointing at
`outputs/identity.json`.

### R6. The prepared adoption writes the wrong `found_year` (minor, for the adoption)

`packing/devtools/adopt_houses.py` on `claude/intake-2026-10-16-n29-622-adopt`, in
`reported_bound`: `"found_year": date.fromisoformat(house.published).year`. At 29 that
gives 2026, the year of PingYou Ltd’s certificate.
The packing is Thomas Schadt’s, found in 2025 and improved by David Ellsworth.
`n-029.md`’s reported lane says so today, the asset’s `credits.json` says so, and the
adoption’s own history note carries 2025 forward.
The new lane should read:

- `found_by`: Thomas Schadt, `found_year`: 2025;
- `improved_by`: David Ellsworth, then PingYou Ltd;
- `source_key`: `[PingYou PR 622 certificate 2026-10-15]`, `source_date`: `2026-10-15`,
  the certificate’s own date, which is also the entry’s `attribution.published`.

The earlier regularization houses this review looked at all have a 2026 finder, so the
rule had not shown.

### R7. The ledger reads the reported lane by its print alone (note, for the record)

`packing/campaign/issue-intake/upper-bounds-n29-20261016/starts.yaml` reads the reported
lane as the print within one unit of its last place.
T-009’s pose box encloses the catalogue’s own contact solution 1e-44 wide, and it shows
the print is a truncation.
The verdict does not change, since $S$ is inside the box too.
But “what would decide it” has a cheaper route than Evan Daniel’s degree-7213 polynomial
(`think-6gti`). The six closing equations T-009 solves have six unknowns.
A Krawczyk step at about 1,000 digits would narrow the box below the $10^{-800}$ scale
at which $S$ is padded, if $S$ is above the solution at all.

### R8. The entry’s pointers name the import bead (note, for the record)

The entry’s `activity.link` and the deferral’s `bead` name `think-30n2`. The review is
`think-2jzy`.

### N1. Nothing in the record is replaced (note, in the source)

`claims.json` asks that this certificate replace your PR #574 certificate at 29. The
record never registered that row: T-174 does not cover 29, and its packet does not
declare it. So the new entry stands beside #574’s other counts and replaces nothing.
The comparison you state, $7.32 \times 10^{-90}$, is exact and correct.

### N2. The provenance paths are archival (note, in the source)

The certificate’s `provenance` names workspace-relative files.
Your README says these are not replay paths, and nothing here needed them.

## 11. Questions for the Author

1. Are the contacts your decoder makes active the ones in the catalogue’s six closing
   equations? If so, an enclosure of that system’s solution at about 1,000 digits would
   say whether $S$ lies above the catalogue packing’s exact side, and by how much.
2. How far is $S$ from your decoder’s exact limit?
   The certificate’s least positive slack, $1.04 \times 10^{-800}$, suggests the
   realization’s 800 digits.

## 12. Comparison With the Replay Lane

This review and #661’s replay agree on every number they share:

- the certificate valid, with one touching pair and wall contacts;
- the controls refused, for the reasons §5.1 states;
- $T\text{-}155 - S = 1.566165818922113 \times 10^{-36}$;
- #574’s N29 side $- S = 7.3248267360651 \times 10^{-90}$, where #661 rounds the last
  digit to 2 and this review truncates it at 1;
- the print 0.919 of a unit below $S$.

Where they differ, it is in what each lane read: the replay’s routes decided the derived
fact, and this review decided the certificate itself and held the two equal.

## 13. The Programs

The programs, with what each read and printed and how to run them, are in the packet’s
[review directory](../../../packing/resources/web/pingyou-pr622-certificate-2026-10-15/review/README.md).
`n29_exact_review.py` is this review’s own and decides.
`third_route.py` only hands the certificate to this repository’s third route.
Neither is registered in `verifiers.yaml` yet; R2 leaves that to the exit.

## 14. What This Review Does Not Establish

- No lower bound, optimum, local minimum or rigidity.
- The order of $S$ and the catalogue packing’s exact side.
- That your decoder, your 800-digit realization or your receipts are correct.
  None of them is needed for the claim, and none was read.
- Anything about your own checkers, which were neither read nor run.
- A formal proof, a second distinct AI review or a human’s oversight.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
