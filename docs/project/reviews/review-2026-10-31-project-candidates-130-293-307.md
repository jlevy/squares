# Review: The Project’s Upper-Bound Candidates at 130, 293 and 307

- **Date:** 31 October 2026

- **Reviewer:** Claude (Anthropic), strongest tier (`tbd-strong-max`), at maximum
  reasoning (the stage 4 mathematical review lane `bold-ritchie-rv-ruu2`, for bead
  `think-ruu2` of the 31 October intake pass).

- **Subject:** three packings this project made below the houses that the pass of 31
  October adopted. None has a register entry yet, and this review names none.

| n | Candidate | House it is below |
| ---: | --- | --- |
| 130 | Evan Daniel’s regularizer, run `adopt-2026-10-31-n130-307-evand`: the view `n-130/view-solved.yaml` (git blob `8a991c28`) and the run’s `n-130/solve/witness.cert` | T-259, Mykhailo Polkovskyi’s re-solve of Francisco Couzo’s packing (T-254) |
| 307 | The same run: `n-307/view-solved.yaml` (blob `6030dd50`) and `n-307/solve/witness.cert` | T-256, Couzo’s refinement of ntumlnoob’s packing |
| 293 | T-257’s 260 certificate `s260_1028.cert` (blob `6114e28f`), side $S$, with one L strip of 33 axis-aligned unit squares in $[S, S+1]\times[0, S+1] \cup [0, S+1]\times[S, S+1]$ | T-257, Evan Daniel’s `s293_1028.cert` |

- **Read at:** `main` `e482345fe`; the run directory in the coordinator’s scratch space
  (RV-5).

- **Verdict:** all three are valid at their exact sides; none is a new arrangement.
  No finding blocks validity.
  Four are major: RV-2 on what the margins are, RV-3 and RV-4 for the owner, and RV-5 on
  custody. One is minor, and three are notes.

| n | Verdict | Why |
| ---: | --- | --- |
| 130 | **accept as recorded only; owner decision** | Valid. 2.500e-13 below T-259 with the same 12-place print (…983): a sub-print re-certification. Under the 23 October ruling that is a restatement, if the ruling reaches $n \le 324$ (think-ikku RV-1). |
| 307 | **accept; adoptable under the rules as written** | Valid. 3.752e-12 below T-256, print …685 against …689: a refinement by the ledger’s definition. 94% of the margin is T-256’s own padding (RV-2), so the review recommends the owner answer RV-3 before the adoption runs. |
| 293 | **accept; adoptable under the rules as written; credit Daniel** | Valid for three strip placements. 8.98e-13 below T-257, print …122 against …123. It is T-257’s packing square for square, with the strip undilated (RV-2). The bound may already be #845’s own report (RV-4), and RV-3 applies as at 307. |

- **Code:** retained by the records lane in
  [`packing/cases/register_candidates/think-ruu2-2026-10-31/review/`](../../../packing/cases/register_candidates/think-ruu2-2026-10-31/review/code/README.md):
  `code/` with a README, the receipts in `out/`, and in `inputs/` the run’s views and
  regularized certificates.
  The other inputs are files at `e482345fe` and the run’s two solve certificates, which
  the package retains as `certificates/n-130.cert` and `n-307.cert`.

- **Record disposition (31 October 2026, records lane, after review A of #861):** none
  of the three is registered.
  All three are held unregistered until the owner answers RV-3 and RV-4 and think-ikku’s
  RV-1, as Proposed Record Changes below proposes, and no evidence entry cites this
  review’s programs yet.
  The package retains the three certificates, the receipts on both maintained routes and
  this review’s code.

## Summary for the Author

The authors here are this project’s own lanes, and Evan Daniel and Francisco Couzo,
whose packings these are.

All three packings are valid.
A clean-room checker written for this review decided each at its exact side, in rational
arithmetic, over every wall and every pair, by two methods: separating axes with no
distance filter, and exact clipped areas.
At 130 and 307 it decided both the drawn view and the run’s solve certificate.
At 293 it decided the construction with the strip in three placements, and wrote two of
them out as certificate files that pass when read back.
All 64 sharp controls came out as expected on both methods, among them the box
$10^{-40}$ below the extent and the closest pair $10^{-40}$ past contact.
Each side is strictly below its house, decided exactly.

None of the three is a new packing.
Each is its house’s own packing, certified with less padding:

- **130 and 307.** The regularizer’s solve moves 3 squares at 130 (by up to
  $4.1\times10^{-7}$) and 5 at 307 (by up to $1.4\times10^{-4}$) beyond $10^{-11}$ from
  the house. The drawn views then move 35 and 38 free squares at the same side.
- **293.** The candidate is T-257’s 293 to $1.6\times10^{-11}$. Its 260 block is T-257’s
  block mirrored ($x \mapsto S - x$) to $1.1\times10^{-13}$. The margin is exactly the
  $1+10^{-12}$ dilation that T-257’s 293 certificate applies to the strip’s extra unit
  of side, less a $1.02\times10^{-13}$ difference between Daniel’s two inputs.
- **Padding, measured.** Scaling each house’s own coordinates uniformly to first
  contact, re-solving nothing, gives packings that both methods accept.
  At 130 that already removes 87% of the margin, and at 307 94%. At 293 it goes
  $1.67\times10^{-11}$ *below* the candidate.

So whether each counts as a result depends on the record’s rules about padding.
Those rules use the 12-place print: 130 keeps its print, while 293 and 307 change
theirs. The questions at the end ask the owner to decide that once for all three.
The credit stays where the record already puts it: Couzo’s packing at 130, ntumlnoob’s
refined by Couzo at 307, and Daniel’s packing and construction at 293. No regularizer
ran at 293.

## The Claims

Each claim is an upper bound by an explicit finite packing, and nothing more:

- $s(130) \le 1487803830747751967474793359227/(1.25\cdot10^{29}) = 11.902430645982015739798346873816$;
- $s(293) \le 8816991251060941991251052624833/(5\cdot10^{29}) = 17.633982502121883982502105249666$;
- $s(307) \le 4494812820921068365908930695861/(2.5\cdot10^{29}) = 17.979251283684273463635722783444$.

Each decimal is exact, since each denominator divides $10^{30}$. The argument has one
step. If $n$ closed unit squares with pairwise disjoint interiors lie inside $[0, L]^2$,
then $s(n) \le L$. No KKT condition, local minimality, rigidity or optimality enters.
The bead reports the two solves as strict local minima modulo 29 and 57 flat motions.
This review did not check that, and the bounds do not need it.

## Exact Verification

**Custody.** The files decided, with their SHA-256 (`out/input-digests.txt`):

| File | SHA-256 |
| --- | --- |
| `n-130/view-solved.yaml` | `95deb14bcbed5da05efc8cbee57229acc90fed606ec449ce928f2b39189d2082` |
| `n-307/view-solved.yaml` | `0297fb2719e0ecc0ba0fd6aa1109dbf41eda18e6b2a5f750072f9f491780eee1` |
| `n-130/solve/witness.cert` | `9d4b4c29e038adc9a2d05cad4dce36477f942bdaa88636011323e7926d956524` |
| `n-307/solve/witness.cert` | `f54749107b0a5ee17d11cc456c95e189e0a04f8ff8a73a24315d95e14d852884` |
| `s260_1028.cert` (from `e482345fe`) | `d6d6f45f600f6552416ea3708d8ee04416cfe88820ee4c3c422d8e131d7cdf87` |
| `out/n293-s260-plus-L-17top+16.cert` (this review’s build) | `10eac4aaba6bd92077040bd7e61014bb302c3af71ccc99ab68481a7b43a90516` |
| `out/n293-s260-plus-L-16+16+1.cert` (this review’s build) | `55c2bb439f7df60e3e6a5c2796b33326fc833a2e6b1a79b9448ff69d400f44d3` |

Each view’s `derived_from` digest equals its house witness at `e482345fe` (`138767d0…`
at 130, `ac27836a…` at 307). Each house witness equals its source certificate square for
square: Polkovskyi’s `n130.cert` and Couzo’s `n307.cert`. Each view is the run’s
`regularize.cert`, converted exactly (130 of 130 and 307 of 307 squares equal).
The `solve/witness.cert` has the same side, and 35 and 38 squares differ.

**The checker.** `qio.py` reads a view strictly, line by line: a centre-basis rational
witness with origin lower-left.
It reads a `.cert` as `n S`, then $n$ rows `x y t`, with
$(c, s) = ((1-t^2)/(1+t^2), 2t/(1+t^2))$, as each file’s header line states.
A square has corners $x \pm u/2 \pm v/2$, with $u = (c, s)$ and $v = (-s, c)$.

- **Route A, separating axes** (`route_sat.py`). It requires $c^2 + s^2 = 1$ exactly.
  On both axes, the support-function extent $h = (|c| + |s|)/2$ must lie in $[0, L]$.
  For each pair, with $\Delta = \theta_j - \theta_i$, every one of the pair’s four edge
  normals sees one square at half-width $1/2$ and the other at
  $(|\cos\Delta| + |\sin\Delta|)/2$. So one threshold
  $T = (1 + |\cos\Delta| + |\sin\Delta|)/2$ serves all four, and the interiors are
  disjoint iff some normal $w$ has $|w\cdot(x_j - x_i)| \ge T$. Every pair is decided,
  with no pruning.
- **Route B, clipped areas** (`route_area.py`). It requires unit edges, right angles and
  area 1. Each square clipped to the box (Sutherland–Hodgman, exact) must keep area
  1. A pair whose corner bounding boxes have disjoint interiors is disjoint; every other
     pair is clipped, one square against the other’s four edges, and must have area
     exactly

**Results** (`out/run_checks-*.log`, `out/check-*.json`):

| Subject | Pairs (both routes) | Clipped (B) | Least pair slack | Least wall clearance | Side − extent |
| --- | ---: | ---: | --- | --- | --- |
| 130 view | 8,385 | 86 | $1.0\times10^{-20}$ | $5.0\times10^{-21}$ | $5.0\times10^{-21}$ |
| 130 solve certificate | 8,385 | 87 | $1.0\times10^{-20}$ | $5.0\times10^{-21}$ | $5.0\times10^{-21}$ |
| 307 view | 46,971 | 296 | $1.0\times10^{-20}$ | $5.0\times10^{-21}$ | $5.0\times10^{-21}$ |
| 307 solve certificate | 46,971 | 295 | $1.0\times10^{-20}$ | $5.0\times10^{-21}$ | $5.0\times10^{-21}$ |
| 293, strip 17top+16 (the house’s placement) | 42,778 | 315 | 0 (strip squares touch) | 0 | 0 |
| 293, strip 16+16+1 (the bead’s) | 42,778 | 315 | 0 | 0 | 0 |
| 293, strip 17+16 | 42,778 | 315 | 0 | 0 | 0 |
| T-257’s 260 alone, in $[0, S]^2$ | 33,670 | 315 | $1.2016\times10^{-12}$ | $6.01\times10^{-13}$ | $6.01\times10^{-13}$ |

Every basis, tilted or not, is exactly a unit vector; the solve certificates tilt 35
squares at 130 and 108 at 307. Every subject passes both routes, and so do the three
houses. The houses’ least pair slacks are $1.823\times10^{-14}$ (T-259),
$9.99\times10^{-13}$ (T-257 at 293) and $2.0895\times10^{-13}$ (T-256).

**Controls** (`out/controls.log`). There are 64 controls on six subjects: both 130
certificates, both 307 certificates, and the 293 with strips 16+16+1 and 17top+16. Each
was decided by both routes against an expectation fixed in the program, and all came out
as expected.

| Control | Expected |
| --- | --- |
| The declared side; the box at the exact extent | accepted |
| The box at the extent − $10^{-40}$ | refused |
| The square nearest a near wall moved onto it | accepted |
| The same, $10^{-40}$ further | refused |
| The least-slack pair closed by its slack along its separating normal | accepted |
| The same, $10^{-40}$ further | refused |
| One square of that pair turned by $t = 10^{-15}$ | refused |
| One basis scaled by $1 + 10^{-40}$ | refused |
| One square duplicated | refused |
| 293 only: the strip’s column moved onto the 260 block’s rightmost corner (a gap of $6.02\times10^{-13}$) | accepted |
| The same, $10^{-40}$ further | refused |

**Trust boundary.** The checker trusts Python 3.14.7’s `fractions.Fraction` and integer
arithmetic, its reader, and the two geometric facts above.
The routes share the reader and nothing else: A builds no corners and B computes no
projection. Both read $t$ as $\tan(\theta/2)$ turning counterclockwise, as the files’
format line states. The checker shares nothing with Daniel’s checkers, the regularizer,
or the maintained routes, none of which its author read.

## Sides, Prints and Ceilings

Exact arithmetic (`out/sides.log`). Prints are rounded up at 12 places, as the record
displays a certificate’s side.

| n | Candidate − house | Below by less than 1e-12 | Candidate print | House print |
| ---: | --- | --- | --- | --- |
| 130 | $-2.500188\times10^{-13}$ | yes | 11.902430645983 | 11.902430645983 |
| 293 | $-8.980000\times10^{-13}$ | yes | 17.633982502122 | 17.633982502123 |
| 307 | $-3.751694\times10^{-12}$ | no | 17.979251283685 | 17.979251283689 |

- **The houses.** Each house side equals its case’s `verified_upper_bound` exactly.
- **Ceilings above.** No verified ceiling at $n < m \le 324$ is at or below a candidate.
  The least excesses are $U(131) - s_{130} = 4.7\times10^{-2}$,
  $U(294) - s_{293} = 2.3\times10^{-2}$ and $U(308) - s_{307} = 1.8\times10^{-2}$. The
  five algebraic ceilings (153, 207, 258, 259, 302) were read from their decimal values;
  the nearest is 302 at 17.87. Above 324, $s(m) \ge \sqrt{325} > 18$. So no candidate’s
  bound follows by monotonicity.
- **Earlier statements.** No file on `main` states any of the three exact sides.
  A `git grep` for the numerators finds only T-257’s register text naming the 293
  construction, and the decimals appear only in the run’s receipt.

## What Each Candidate Is

**Identity** (`out/identity.log`). The measurement is in binary64, pose by pose, with
nearest centres under the box’s eight symmetries.
It decides nothing.

| Candidate | Against | Pairing | Beyond $10^{-11}$ | Largest move | Largest turn |
| --- | --- | --- | ---: | --- | --- |
| 130 solve certificate | T-259 | identity, one to one | 3 | $4.1\times10^{-7}$ | $3.8\times10^{-5}$° |
| 130 view | T-259 | identity, one to one | 35 | $5.9\times10^{-2}$ | 1.84° |
| 307 solve certificate | T-256 | identity, one to one | 5 | $1.4\times10^{-4}$ | $5.7\times10^{-3}$° |
| 307 view | T-256 | identity, one to one | 39 | $3.3\times10^{-1}$ | 0.55° |
| 293: the 260 block | T-257 293’s block | mirror $x \mapsto S - x$, one to one | 0 | $1.1\times10^{-13}$ | $5.7\times10^{-14}$° |
| 293: strip 17top+16 | T-257 293’s strip | identity, one to one | 12 | $1.6\times10^{-11}$ | 0 |

T-257’s 293 places its strip as a column of 17 flush with the top wall and a row of 16
flush with the left wall.
The strip squares sit $1.6\times10^{-11}$ out from the candidate’s, which is the house’s
own $1+10^{-12}$ dilation at $x \approx 17$. The bead’s 16+16+1 and the 17+16 placement
are equally valid but do not pair one to one, since the strip has 0.634 of play along
each arm.

**Padding** (`out/contract.log`). Scale every centre about the corner by the least
$\lambda$ that keeps every pair interior-disjoint, then box the result.
The four edge normals do not change under scaling, so that $\lambda$ is exact:
$\lambda^* = \max_{\text{pairs}} T / \max_w |w\cdot d|$. The result is the house’s own
coordinates at first contact.
Both routes accepted each contracted packing, so each is a proved bound in its own
right:

| Certificate | $1 - \lambda^*$ | Contracted side | Below its certificate by | Contracted − candidate | Print |
| --- | --- | --- | --- | --- | --- |
| T-259 (130) | $1.823\times10^{-14}$ | 11.902430645982047452… | $2.183\times10^{-13}$, 87% of the margin | $+3.17\times10^{-14}$ | …983 |
| T-256 (307) | $2.090\times10^{-13}$ | 17.979251283684496199… | $3.529\times10^{-12}$, 94% of the margin | $+2.23\times10^{-13}$ | …685 |
| T-257 (293) | $9.990\times10^{-13}$ | 17.633982502105165133… | $1.762\times10^{-11}$ | $-1.67\times10^{-11}$ | …106 |
| T-257 (260) | $1.202\times10^{-12}$ | 16.633982502101892884… | $1.999\times10^{-11}$ | its 293, $-2.00\times10^{-11}$ | …102, against …122 |

The certificates’ headers say what the padding is:

- **T-259.** Its header reads “dilation certificate (dilate_cert.py, delta 2e-14)”,
  which pads the side by $2.4\times10^{-13}$.
- **T-257.** Both certificates read “delta 1e-12”, and their `.json` summaries report
  `"status": "solve failed"`, so each is a dilated binary64 point.
- **T-256.** It states no padding.
  Its least pair slack times its side is $3.76\times10^{-12}$, about the margin.

At 293 the margin decomposes exactly.
T-257 dilated the whole 293 input by $1 + 10^{-12}$, so the strip’s extra unit of side
contributes $10^{-12}$; the candidate dilates only the 260 and leaves the strip
undilated. The 293 input’s side, 17.633982502105148, is $1.02\times10^{-13}$ less than
the 260 input’s 16.63398250210525 plus one (`s293_1028.json`, `s260_1028.json`). So
$10^{-12} - 1.02\times10^{-13} = 8.98\times10^{-13}$, the margin.

## Credit Chains

- **130.** The packing is Couzo’s (T-254), credited as the record already credits it
  after the finders it names.
  The certificate re-solved is Polkovskyi’s (T-259); the run read its witness, as the
  view’s `derived_from` digest shows.
  The re-solve and the view are the Squares Project’s, with Evan Daniel’s regularizer
  (evand/square-packing, MIT).
- **307.** The packing is ntumlnoob’s, refined by Couzo (T-256, #844). The re-solve and
  the view are the Squares Project’s, with Daniel’s regularizer.
- **293.** The packing and the construction are Daniel’s.
  - **What #845 says.** His 293 is his 260 plus one L-shaped strip, and T-257 credits it
    so.
  - **What the project did.** It applied that construction to his own 260 certificate at
    its exact side. It searched nothing and moved nothing.
  - **Earlier credit.** The record already credits L-strip constructions to whoever
    states them. T-257 does at 293, and beyond the horizon the ruling “a recipe is a row
    once the maintained checker decides it” does for $tS + L$ recipes on a parent
    certificate. The case’s earlier conjectured optimum, the Kingbird catalogue’s 723/41,
    fell to this same construction, credited to Daniel.
  - **No regularizer ran at 293**, so the bead’s credit to “Daniel’s regularizer” does
    not apply there.

The record’s precedent for project re-solves below a ceiling is T-155. It registered 59
regularizer solves $5.4\times10^{-20}$ to $9.9\times10^{-15}$ below their ceilings, each
credited to its packing’s finder with the regularization to the project, at significance
1\. T-195, a source’s certificate $1.57\times10^{-36}$ below T-155, is also at 1. Both
predate the ruling of 23 October.

## Significance

S1 for each: a re-certification of a packing the record already credits, which is
bookkeeping, as at T-155 and T-195. 293 and 307 change a print, but the measurement
above puts both margins in the padding.

## Findings

No finding blocks validity: each certificate proves its bound.
Paths are at `e482345fe` unless a scratch path is named.

### RV-1 (note): All three bounds hold

Each candidate is a valid packing at its exact side, decided twice in rationals with 64
sharp controls.
This holds for the view and for the solve certificate at 130 and 307, and
for three strip placements at 293, two of them as written files read back.

### RV-2 (major): None is a new arrangement; each margin is its house certificate’s padding

**What.** At 130 and 307 the solve is the house re-solved: 127 of 130 and 302 of 307
squares lie within $10^{-11}$ of the house.
The views then move the free squares at the same side, which is a drawing matter.
At 293 the candidate is T-257’s 293 to $1.6\times10^{-11}$, and its margin decomposes
exactly into the strip’s dilation.
Contracting the houses’ own coordinates, with nothing re-solved, reaches within
$3.2\times10^{-14}$ of the 130 candidate.
It reaches within $2.2\times10^{-13}$ of the 307 candidate, at its print …685, and
$1.67\times10^{-11}$ below the 293 candidate.
So the print each candidate keeps or crosses belongs to the padding, not to the packing.

**Fix.** Any entry that registers one of these says so in its `method` and significance
rationale: “the house’s packing, re-certified with less padding; S1”, not a refinement
of the arrangement.

### RV-3 (major, owner decision): The print sorts three copies of one operation

**Where.** `result-import.md`, “A restatement is not recorded (think-fwa9)” and the
refinement bullet (“recorded like a new packing … unless it restates the report below
the print”); the House Rule (“Smaller is decided by exact arithmetic, never by a print
or a person”); `intake_ledger.Ruling.applies`.

**What.** Under the record as written the three counts land differently:

- **130** is below T-259 by less than one unit in the 12th place, with the same print.
  That is a sub-print re-certification, which the ruling calls a restatement (“sub-print
  re-certifications are RESTATEMENTS, not new rows.
  The earlier certificate stays the row”). The ledger applies the ruling beyond 324
  only, and think-ikku’s RV-1 asks whether it reaches $n \le 324$, so 130 waits with
  T-253 and T-260.
- **293 and 307** change the print, so the ruling’s words do not reach them.
  The refinement bullet and the house rule record and adopt them.

All three come from one operation, removing a house certificate’s padding.
The same arithmetic contracts T-257’s own 260 certificate to 16.633982502101892…,
$2.0\times10^{-11}$ below the 260 house and across its print (…102 against …122). It
contracts T-257’s own 293 to $1.67\times10^{-11}$ below the 293 candidate.
Adopting 293 and 307 under the house rule therefore commits the record to adopting such
a contraction at any count whose house certificate is padded and loose enough to cross a
print, whoever submits it, the project included.

**Fix.** Put the question below to the owner with think-ikku’s RV-1, before the adoption
runs at 293 and 307.

### RV-4 (major, owner decision; 293): The bound may already be #845’s report

**What.** T-257’s 260 certificate states $S$ exactly, and #845 states the recipe “260
plus one L-shaped strip” for its 293. Both were published on 29 October, so $S + 1$
follows by the recipe from a published certificate.
Two beyond-horizon rulings read exactly that as the publication’s own report: a recipe
on a certificate is a row of its source, and a deletion bound is an earlier report.
Inside the corpus they are not rules.

**Fix.** Ask the owner.
If $S + 1$ is #845’s report, the result says T-257 already proves it
(`first_certified_in: T-257`). If not, it is a re-certification of T-257 credited to
Daniel, with the exact re-assembly the project’s. Either way, no credit line names the
regularizer at 293.

### RV-5 (major, custody; for the records lane): The certificates are not in the repository

**Where.**
`packing/cases/regularized_drawings/think-3guf-2026-10-31/adopt-2026-10-31-n130-307-evand/n-{130,307}/`
retains only `report.json.gz`. That file pins the source witness, the input and the
exact side, but no digest of the view or the solve certificate.
The certificates exist only in the coordinator’s scratch run directory.
No 293 certificate file existed before this review wrote two.

**What.** At 130 and 307 the brief names the view and the bead’s Claim names the solve
certificate. These are two certificates of one side, which differ in 35 and 38 squares.
Both pass here.

**Fix.** Before registering, retain the certificate the entry registers with the SHA-256
listed above, and decide it on both maintained routes.
The view is a drawing under the regularization policy, so the solve certificate is the
natural bound certificate.
At 293, retain a written certificate, this review’s `out/` file or the records lane’s
own build, rather than a description.

### RV-6 (minor; 293): The side as built is not tight, and the placement is unspecified

**What.** The 260 block clears $x = S$ by $6.02\times10^{-13}$ and the top wall by
$6.01\times10^{-13}$, so the strip could sit $6.0\times10^{-13}$ lower and inward, with
the side lowered by as much.
Contraction goes $2.0\times10^{-11}$ further.
The bead says “16 + 16 + 1”, while the house places a column of 17 flush with the top.

**Fix.** None for validity.
A registration names the placement it certifies, and RV-3’s answer decides whether a
tighter side should replace $S + 1$.

### RV-7 (note): Ceilings and earlier certificates

No verified ceiling above any of the three counts is at or below its candidate, and no
earlier certificate states any of the three sides.
So no `first_certified_in` applies on the record as it stands.
RV-4 asks about 293’s side by recipe.

### RV-8 (note): The local-minimum statements are the regularizer’s

The bead’s “exact KKT local minima … strict modulo 29 and 57 exact flat motions” are the
regularizer’s reports.
This review replayed none of them, and no claim here rests on them.

## Questions

**For the owner (RV-3).** The review recommends (a).

> Is a re-certification of a house’s own packing, with the same arrangement and a margin
> no larger than the house certificate’s padding, a new result at any print?
> 
> - (a) No, at any margin: none of the three is recorded, and the houses stay.
>   The 23 October ruling gains an identity test, the packing measured pose by pose
>   against the house, beside its print test.
> - (b) Only across the 12-place print, as written: 293 and 307 are adopted now, and 130
>   follows think-ikku’s RV-1. The record should then expect contractions like 260’s,
>   from anyone.
> - (c) Yes, at any margin: all three are adopted.
>   The record should then register the tightest re-certification it can prove, at 293
>   the contraction rather than $S + 1$, and treat 260 the same way.

**For the owner (RV-4).** Is $S + 1$ at 293 already #845’s report, through its 260
certificate and its stated recipe?

**For the coordinator (RV-5).** Which certificate at 130 and 307 does the entry pin, the
solve certificate or the view?

## Rungs

Each candidate the owner’s answers leave standing can reach `V3`/`C3` once its
certificate is retained, replayed on the maintained routes, and this review is mapped.
This review’s two routes are a complete confirming run of each, and their confirmation
reads: *independently re-implemented, clean-room, by a Claude agent, a system family the
producer also used* (the project’s lanes and the regularizer’s author both worked with
Claude). Nothing here bears on `V4`/`C4`, a lower bound, local minimality, rigidity or
priority.

## Proposed Record Changes

This review writes none of these; they are for the records lane.

- **Custody (RV-5).** Retain the chosen certificate at each count with its SHA-256 above
  and decide it on both maintained routes; retain the 293 certificate as a file.
- **Registration (RV-3, RV-4).** Hold 130 under think-ikku.
  Register 293 and 307 as one batch only once the owner has answered RV-3, or now if the
  coordinator keeps to the rules as written.
  Score each S1 with the rationale from RV-2.
- **Credit.** At 130, Couzo’s packing as T-259 credits it, re-solved by the Squares
  Project with Evan Daniel’s regularizer.
  At 307, ntumlnoob’s packing refined by Couzo (T-256), re-solved likewise.
  At 293, Daniel’s packing and construction (T-257), re-certified by the Squares
  Project, with no regularizer.
- **`verifiers.yaml`.** Register `route_sat.py` and `route_area.py` as the deciding
  programs with this independence record: `read` mathematics, certificate-format,
  specification and producer-output, and earlier-review after the findings were written;
  `clean_room: true`; `shares: []`; `written_by` this lane at `tbd-strong-max`,
  reasoning max; `overlaps_producer: system-family`. `contract.py` decides only the
  contracted packings, which no entry registers, and the other programs decide nothing.
- **`evidence.yaml`.** For each registered count, an exact-feasibility entry,
  `independent-implementation`, `coverage: full`, citing this review as
  `external_review`.

## Independence and Disclosure

- **Programs.** Written for this review; clean-room for what they decide.
  Their author read the mathematics, the certificates’ header lines,
  `packing/witnesses/witness.schema.yaml` (a basis is $[\cos\theta, \sin\theta]$), the
  houses’ source certificates, Daniel’s `.json` summaries, and the run’s retained
  `report.json.gz`. It read no checker of Daniel’s, nothing of the regularizer’s code,
  neither maintained route, and no review program in any packet.
  It ran no code but its own, apart from `git`, `grep` and `sha256sum`.
- **Read before the findings were written:**
  - the beads `think-ruu2`, `think-ikku` and `think-fwa9`, including the note that the
    senior review of #852 (A3) built the 293 construction and a maintained route
    accepted it;
  - the case records at 130 and 293, which summarize the earlier review of T-257,
    including “up to a mirror”, and that at 307;
  - T-257’s register claim, which says three of its certificates “dilate their binary64
    inputs by 1 + 1e-12”;
  - a three-line `git grep` hit for `723/41` in that earlier review: its verdict row for
    293 and its note that the conjecture is withdrawn on adoption;
  - lines 1–14, 50, 67 and 70–80 of the README of Couzo’s #844 packet.
- **Read after the findings were written**, for shape and for the comparison below:
  [`review-2026-10-31-daniel-845-172-204-260-293.md`](review-2026-10-31-daniel-845-172-204-260-293.md)
  and
  [`review-2026-10-31-polkovskyi-846-and-23-oct.md`](review-2026-10-31-polkovskyi-846-and-23-oct.md)
  in full, and the 307 lines of
  [`review-2026-10-31-couzo-844-232-260-307.md`](review-2026-10-31-couzo-844-232-260-307.md).
- **Resources.** About 10 CPU-minutes on one core, within the brief’s two.

## Comparison with Earlier Reviews

Written after the findings above, which it changed in no respect.

- **The review of Polkovskyi’s certificates** (T-253, T-259) found every margin there to
  be padding. Its RV-6 found that T-259’s own $2.08\times10^{-12}$ over Couzo’s #843 is a
  re-solve at tighter padding which the print test admits, and it anticipated this
  review’s option (a): “If the owner instead rules that any re-certification of the same
  packing is a restatement whatever the print, 130 would fall too.”
  This review adds three things:
  - the project’s own candidates are of the same class;
  - uniform contraction measures how much of each margin is padding;
  - T-257’s certificates at 260 and 293 contract across their prints, which is the open
    series that review’s second reason foresaw.
- **The review of Daniel’s certificates** (T-257) gives the same least clearances and
  gaps for `s260_1028.cert` and `s293_1028.cert` that this review measured: $6.010\times
  10^{-13}$, $1.2016\times10^{-12}$, $4.995\times10^{-13}$, $5\times10^{-13}$ and
  $9.990\times10^{-13}$. Its finding that the 293 is the 260 “up to a mirror … to
  binary64 zero distance” is made with the 260 anchored at a corner of the 293 box.
  This review, which allowed no translation, finds $1.1\times10^{-13}$, the input offset
  below. Its sentence “the two binary64 sides differ by one to binary64 rounding”
  understates that offset: the inputs differ from one by $1.02\times10^{-13}$, about 29
  units in the last place at 17.6, and that difference is part of the 293 margin
  decomposed above. Its N-6 (a converged 204 could certify about $2.6\times10^{-11}$
  less) and N-9 (the dilations leave every square at least $5\times10^{-13}$ of room)
  point the same way as RV-2 here.
  No verdict there changes.
- **The review of Couzo’s #844**, read only at 307, found T-256 to be Couzo’s own T-255
  arrangement refined by $4.56\times10^{-12}$, with 13 squares moved beyond $10^{-2}$,
  “which alone would be S2”. The 307 candidate here differs in kind.
  94% of its margin is T-256’s own pair padding, and its solve moves 5 squares beyond
  $10^{-11}$, so S1, not S2.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
