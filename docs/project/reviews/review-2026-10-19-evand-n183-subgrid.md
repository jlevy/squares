# Independent Mathematical Review of Issue #680

The initial static audit found a sound conditional argument for the submitted upper
bound and no blocking mathematical defect.
The replay addendum below accepts the later retained primary-certificate replay as
evidence for the finite upper bound.
The regularized certificate remains unexecuted.
Sections before that addendum preserve the initial static assessment and its then-open
replay obligations.

The main correction concerns the additional local-optimality description: the reported
27 flat modes belong to the 182-square force-bearing subsystem.
They exclude the free rattler’s three position-and-angle coordinates.
The numerical local-minimum description must also retain its numerical qualification.
Neither this correction nor the other limits below defeats the finite upper-bound claim.

- **Reviewer:** OpenAI Codex system family, strong tier, maximum reasoning.
- **Date:** 2026-10-19.
- **Scope:** Independent read-only Stage 4 mathematical review of
  [issue #680](https://github.com/jlevy/squares/issues/680), covering the original
  rational certificate, its regularized view, their checkers, and the associated
  numerical and provenance claims.
- **Source pin:** Evan Daniel’s
  [`evand/square-packing` at `3a9948c781be668b1547cc2bf64a0d1e614f9bca`](https://github.com/evand/square-packing/tree/3a9948c781be668b1547cc2bf64a0d1e614f9bca).
- **Custody:** `packing/resources/web/evand-n183-subgrid-2026-10-19/`, as declared in
  its acquisition manifest.
  The existing separate upstream worktree resolves to the full pin above.
  The record author’s checkout was read without modifying it.
- **Tracking:** `think-glg8`, claimed as `codex-680-math-review-20261019`; `think-1hmn`
  separately owns replay and controls.
- **Execution:** No upstream program, certificate replay, numerical optimizer, build,
  environment installation, or new proof search ran.
  No new verification program was written.
  Header/row inspection and custody hashes are premises, not geometry checks.
- **Independence:** I read both source checkers, the relevant generator sections,
  candidate reports, the issue snapshot, and the intake declaration and README. I read
  no earlier independent review of this result.
  The intake README already summarized the checkers and the source’s limitations; that
  exposure is disclosed.
  This review does not establish clean-room implementation independence.
- **Publication:** This artifact is an intake handoff, not a published PR review or a
  mapped register review.
  It names no provisional result ID.

## Claim and Evidence Boundary

Both certificate headers declare 183 and the exact rational side

```text
S' = 13999580178736252502081470897571 / 1000000000000000000000000000000
   = 13.999580178736252502081470897571
```

Each retained certificate has exactly 184 non-comment, nonempty rows: one header with
two fields and 183 square rows with three fields.
The two files have different bytes and the same header.
The SHA-256 checks agree with the issue and retained manifest:

| File | SHA-256 |
| --- | --- |
| `s183_h183b.cert` | `279e70d1c7fb0bc181e3e9d313e7350b672d85e223296f252b92f2916d6e5df5` |
| `s183_h183b_regularized.cert` | `67b2b26205f53915bb1a10a703a2700994a9ad16ea9ddd427bda232716f40d58` |
| `search/exact/verify_cert.py` | `3299ca0c0f02f7c221deeea69a9a85b5a90db6bc410b20727fdff211c92bed52` |
| `search/exact/verify_cert2.py` | `55140a35d95d9eaa64a14c3b044641efbcda94ebfc3b12b7dec9fa52692e31d3` |

Ordinary exact decimal arithmetic gives

```text
13.999580178736 < S' < 13.999580178737 < 14
13.999580178737 - S' = 0.000000000000747497918529102429
14 - S'                = 0.000419821263747497918529102429
```

Thus the claimed twelve-place upward rounding is correct.
The exact header, not a binary floating-point printout or the smaller numerical KKT
side, must supply the published upper bound.
These arithmetic identities do not establish that the 183 placements satisfy the
certificate’s predicates.

The source’s `S_exact` value begins `13.999580178736252501941475095783...`. It is a
numerical KKT estimate, below `S'`. The retained `.exact.txt` stores decimal centers and
angles in degrees; the `.cert` stores rational centers and rational half-angle
parameters. Interchanging those formats would change the geometry.

## Invariants and Mathematical Argument

### Unit Squares and Coordinate Convention

For a certificate row `x y t`, define

```text
c = (1 - t²)/(1 + t²),  s = 2t/(1 + t²)
u = (c,s),              v = (-s,c)
Q = (x,y) + {a u + b v : -1/2 <= a,b <= 1/2}.
```

A rational `t` is finite, and `1+t² > 0`. Expanding the numerator proves `c²+s² = 1`
exactly. The vectors `u,v` are perpendicular unit vectors, with determinant one.
Every row therefore describes a unit square, with side length one; this is stronger than
an area-one assertion.
The centers use the lower-left origin.
No numerical sine, cosine, square root, or degree conversion belongs in verification.

The parameterization need not enumerate all possible rotations.
This is an existence witness for a packing of freely rotated unit squares; it is not a
lower bound obtained by sampling or covering a continuous pose domain.

### Walls

For either coordinate, the square’s maximum displacement from its center is
`e = (|c|+|s|)/2`. The four strict inequalities

```text
x-e > 0,  S'-x-e > 0,  y-e > 0,  S'-y-e > 0
```

place the whole closed square inside the open container.
[`verify_cert.py:39–43,63`](https://github.com/evand/square-packing/blob/3a9948c781be668b1547cc2bf64a0d1e614f9bca/search/exact/verify_cert.py#L39)
checks precisely those quantities.
The polygon checker computes all four vertices and checks each coordinate against the
same walls; convexity then contains every point of the square.

Strict containment is sufficient for the usual closed-container packing convention.
It is deliberately stronger than necessary, so rejection of a touching witness would not
refute that witness under the usual convention.

### Every Pair

There are `183 * 182 / 2 = 16,653` unordered pairs.
Both loops visit every pair, with one exact shortcut: a unit square has circumscribed
radius `sqrt(2)/2`, so two such squares cannot meet if their squared center distance
exceeds `2`. Equality is not skipped.

For the remaining pairs, the first checker tests the two edge directions of each square.
For any direction `n`, the exact projection half-width is

```text
h_i(n) = (|n·u_i| + |n·v_i|)/2.
```

A strictly positive value of `|n·(p_j-p_i)| - h_i(n) - h_j(n)` separates the closed
squares. The checker takes the maximum over its four directions for each pair and then
requires every pair’s maximum to be positive.
These are the complete separating-axis directions for two rectangles; in particular,
positive acceptance is sound.
See
[`verify_cert.py:46–63`](https://github.com/evand/square-packing/blob/3a9948c781be668b1547cc2bf64a0d1e614f9bca/search/exact/verify_cert.py#L46).

The second checker constructs counterclockwise vertices.
Its oriented cross products test closed convex-polygon membership.
Its segment predicate checks both proper crossings and collinear or endpoint contact.
If two closed convex polygons intersect, either a vertex is in the other polygon or
their boundary edges meet.
Testing both vertex directions and all sixteen edge pairs therefore suffices.
See
[`verify_cert2.py:15–38,50–66`](https://github.com/evand/square-packing/blob/3a9948c781be668b1547cc2bf64a0d1e614f9bca/search/exact/verify_cert2.py#L15).

All deciding arithmetic and comparisons use `fractions.Fraction`. Floating-point
conversions occur in diagnostic printing.
There is no tolerance-based geometric acceptance in either checker.

### Generation and Scaling

[`exactsolve.py:759–779`](https://github.com/evand/square-packing/blob/3a9948c781be668b1547cc2bf64a0d1e614f9bca/search/exact/exactsolve.py#L759)
scales centers and the container, leaves the squares unit sized, rounds centers and
half-angle parameters to rationals, and checks the written certificate.

For an already feasible configuration and `f=1+epsilon`, the scaling rationale is valid.
A wall margin `m` becomes `f m + epsilon e`, gaining at least `epsilon/2`; a chosen
separating-axis gap `g` becomes `f g + epsilon(h_i+h_j)`, gaining at least `epsilon`.
These statements assume feasibility before scaling.
Finite numerical residuals and subsequent rounding do not prove that assumption.

The final rational check removes the need to trust the optimizer or a perturbation error
estimate. Its successful predicates alone would prove finite feasibility.
Conversely, a strict-clearance certificate at `S'` cannot itself be a local minimum of
the container side: its upper and right wall margins allow a small decrease of the side
while holding the squares fixed.
The local-minimum diagnostics concern a different, numerically computed limiting
configuration.

| Invariant | Review result |
| --- | --- |
| Every parsed row is a unit square | Exact algebra establishes this from the declared format |
| The claimed count and side are the ones checked | Headers and row widths match here; replay must bind them independently |
| All points satisfy the walls | The implemented finite predicate is sufficient; actual inequalities not evaluated here |
| All 16,653 pairs are covered | Loop and exact shortcut are sound by inspection; actual inequalities not evaluated here |
| Twelve-place publication rounds upward | Exact decimal comparison above |
| Regularized endpoint has the same side | Identical exact headers; feasibility still awaits its own replay |
| Local optimality, flat families, and identity path | Not established by this certificate format or this review |

## Findings and Required Dispositions

### M1 — Major, Nonblocking for the Upper Bound: The 27 Modes Exclude the Rattler

The numerical report gives `load_bearing_squares_exact: 182`, `free_squares: [11]`,
`free_clearance: 0.0249255667...`, `rank_JA: 520`, and `dim_null: 27`. At
[`exactsolve.py:1030–1035`](https://github.com/evand/square-packing/blob/3a9948c781be668b1547cc2bf64a0d1e614f9bca/search/exact/exactsolve.py#L1030),
the variable list contains only the three pose coordinates of each force-bearing square
and the side: `3*182+1=547` variables, leaving `547-520=27` directions.

The free square’s coordinates are absent.
If its reported positive clearance holds, small translations in two directions and a
small rotation supply three additional local motions of the complete packing at fixed
side. The source status string “strict modulo 27 exact flat motions” therefore does not
describe the full configuration’s motion count without this scope qualification.
The source’s `first_order_rigid` list likewise concerns the selected subsystem.

**Disposition:** Describe the source as reporting “numerical KKT diagnostics with 27
candidate flat modes in the force-bearing subsystem and one free rattler.”
Do not promote that wording to an exact local-minimum theorem, and do not silently
describe 27 as the complete packing’s flat dimension.
This finding requires a claim-wording correction, not rejection of the finite
certificate.

There is a separate numerical limitation even within the subsystem.
[`exactsolve.py:515–542`](https://github.com/evand/square-packing/blob/3a9948c781be668b1547cc2bf64a0d1e614f9bca/search/exact/exactsolve.py#L515)
uses floating-point SVD and eigenvalue thresholds; the report classifies all 27 reduced
eigenvalues as zero.
[`probe_flat:619–653`](https://github.com/evand/square-packing/blob/3a9948c781be668b1547cc2bf64a0d1e614f9bca/search/exact/exactsolve.py#L619)
tests two finite steps along each selected mode and accepts residual and side-change
thresholds.
Such probes do not prove a local manifold of constant side, its dimension, or
joint integrability of the directions.
The first-order corner-contact MILP is also numerical and does not exclude a
higher-order descent.
The issue already discloses the lack of interval proofs; retain that disclosure wherever
the diagnostics are quoted.

### M2 — Minor, Nonblocking for These Files: Bind the Parser to the Submitted Claim

[`verify_cert.py:23–31`](https://github.com/evand/square-packing/blob/3a9948c781be668b1547cc2bf64a0d1e614f9bca/search/exact/verify_cert.py#L23)
and
[`verify_cert2.py:41–49`](https://github.com/evand/square-packing/blob/3a9948c781be668b1547cc2bf64a0d1e614f9bca/search/exact/verify_cert2.py#L41)
read only the number of square rows declared by the header and ignore trailing rows and
extra tokens. They do not accept an expected count or side from the caller.
Their row-count assertions are removable by optimized Python execution.

A source trace, not an executed test, shows the consequence: a file with header `1 2`
followed by two identical `1 1 0` rows is accepted as a one-square certificate; the
second row is ignored.
That is not a valid confirmation of a two-square submission.
The second checker also reaches its success return for a zero-square header without
checking that the side is positive.

The submitted files have neither of these header/width defects.
The issue is a receipt boundary, not a demonstrated false positive for n183.

**Disposition:** The replay wrapper must require `n=183`, the exact submitted side,
exactly 183 square rows, the declared field widths, and valid finite rationals.
Run without assertion removal.
Keep file identity, parsed count and exact side in the receipt; do not infer the theorem
from exit zero or a rounded `float(S)` string alone.
Any general parser hardening belongs in a separately reviewed change.

### M3 — Note: Endpoint Feasibility Does Not Establish Regularization Identity

`s183_h183b_regularized.json:1` reports conservative level 2 and a path without
expansion. The original and regularized files change coordinates, including the first
square’s center; the free square’s numerical pose also changes.
Two successful endpoint checks would prove two feasible packings at the same side.
They would not prove a collision-free path between them, exact arrangement identity, or
that a path remained at or below that side.

The 19-to-18 angle-group statement and the prior comparison’s “distinct minimum” verdict
are source classifications.
The retained pair of endpoint certificates does not certify either classification.

**Disposition:** Keep the regularization identity and path as source assertions unless a
retained path argument or a separate, appropriately qualified identity audit establishes
them. One bound is being submitted; the display file is not an additional upper-bound
result. House regularization remains its own later obligation.

### M4 — Note: Priority and Lineage Need Evidence Beyond Geometry

Issue #680 describes a comparison against the register at `804eff36`, issues through
#678, the Kingbird catalogue and their monotone envelope, checked on 18 October.
The retained prior report compares a side-14 grid and gives source labels, not a
complete dated custody record for every comparator.
The arithmetic `183=14²-13` is exact.
Whether this was the first public packing below 14 is a historical claim requiring the
separate comparison audit.

Credit Evan Daniel, after Francisco Couzo’s n182 packing, as requested.
[`PACKER.md:4171–4174`](https://github.com/evand/square-packing/blob/3a9948c781be668b1547cc2bf64a0d1e614f9bca/search/packer/PACKER.md#L4171)
describes a non-record n182 descendant, insertion, two crossovers with unlogged mates,
and refinement. Current `explore.py` contains mate-logging code, but its presence does
not recover the historical run inputs or establish which revision ran.
The source’s L-cut experiment belongs to a separate arm that reportedly stopped above
14; it is not the submitted donor chain.
Its `lcut.py` is outside this retained packet and was not inspected or executed.

**Disposition:** Attribute the historical assertions, preserve Couzo’s donor credit, and
record the missing crossover provenance.
Feasibility replay cannot repair lineage or establish public priority.

## Trust Boundaries and Later Replay

The two standalone checkers read a caller-selected file, use only `sys` and `fractions`,
print diagnostics, and return a status.
I found no network, subprocess, dynamic evaluation, or file-write operation in either
deciding script. Their Python interpreter and standard library remain trusted.
The numerical production programs have broader imports, writes and subprocess activity;
none is needed to decide the finite certificate.

Both checkers share authorship, the certificate convention, substantially the same
parser, the rational rotation formula, `Fraction`, and the same distance shortcut.
Their different pair-intersection methods provide useful algorithmic diversity.
Re-running either or both here remains **reproduced with the producer’s code**
(`same-implementation`), not an independently authored implementation.
A separate checker written after reading this source must disclose that exposure; code
reuse would require the appropriate shared-components record.

The replay owner should retain and review the following bounded sequence:

1. Bind each certificate to its declared source identity, expected count, exact side and
   complete row set. Keep the actual deciding program digests and interpreter version.
   Use the existing project interpreter in isolation, without importing unrelated
   upstream files, and without optimization that removes assertions.
2. Run each scheduled exact route over each complete certificate.
   Preserve command, working directory, environment, exit code, stdout/stderr, CPU/wall
   time and coverage. A timeout, exception, partial result or sampled-pair check is not a
   pass.
3. For each accepted original and regularized view, retain two distinct negative
   controls: copy one square row over another while keeping n and side fixed, and move a
   square center outside the wall while keeping its rotation and the header fixed.
   Every accepting route must reject both.
   The duplicate must remain a square with valid syntax so rejection exercises geometry
   rather than parsing.
4. Independently preflight the two mutants’ intended defects and retain a test of their
   expected nonzero outcomes.
   If a new implementation is introduced, add small exact fixtures for the predicates it
   implements: nontrivial rational rotation, wall and pair touching, the distance-cutoff
   boundary, and crossing or containment as applicable.
   Those are implementation checks, not additional claims about n183.
5. Keep the review, programs and receipts outside disposable scratch; map the review and
   register the deciding and premise-checking programs with their actual independence
   metadata. Re-derive the record’s rungs from those retained entries.

The coordinator’s 0.01–0.10 CPU-hour price and 360-second first-batch ceiling are an
estimate and scheduling limit, not timing measurements from this review.
The source report’s 12 seconds prices numerical production and cannot stand in for
checker timing. No replay was authorized or launched in this mathematical-review slice.

A new Stage 3 record at `V0/C0` remains appropriate while this review is unmapped.
Once an accepted read is mapped and cited, it can support `C1`, with `V0` unchanged
absent qualifying replay evidence.
A full passing exact replay with controls, an accepted mapped mathematical review, and
the required registry integration would justify the Stage 4 finite-feasibility
conclusion at `V3/C3`, explicitly qualified by which implementation confirmed it.
This report alone supplies no `C3` receipt, local-optimality theorem, house adoption, or
priority decision.

I recommend **S3** for the proposed single-case upper-bound result under the stated
rubric. A packing below 14 at n183 is a substantive case result if valid; this packet
does not establish the reusable bound family, resolved disputed value or central-case
resolution needed for a higher score.
The assessment is separate from V/C and priority.

## Evidence Collected and Handoff

The read-only evidence operations were:

| Command or inspection | Result |
| --- | --- |
| `tbd prime`; `tbd policy show` | Workflow loaded; effective main pin `7d350455147e6df0618163272030b3cddd37affa` |
| `tbd shortcut review-code-correctness`; `tbd shortcut review-code` | Review workflow loaded; read-only brief governs execution scope |
| `tbd sync`; `tbd show think-glg8 --max-lines 160`; `tbd start think-glg8 --as codex-680-math-review-20261019`; `tbd sync` | Open child claimed and one update synchronized; initial sandbox lock denial resolved by approved filesystem escalation |
| `git rev-parse HEAD` in the existing separate upstream worktree | `3a9948c781be668b1547cc2bf64a0d1e614f9bca` |
| `shasum -a 256` on both certificates and both checker files | The four digests listed above |
| Text row-width/count inspection with `awk` | Each certificate: `data_rows=184 bad_width_rows=0` |
| `cat`, `sed`, `nl -ba`, `rg`, `jq`, and `gzip -cd` with `jq` | Read retained source and selected JSON fields; no source program imported |
| `flowmark --version` | `0.4.0`, Rust port; used for this review artifact |

An initial row-count command used an `ENDFILE` action unsupported by the host awk and
produced no counts. The reported counts come from the subsequent portable `END`
aggregation, which printed both results.
No geometry conclusion rests on either text-processing command.

The record lane owns mapping this artifact under `docs/project/reviews/`, applying the
M1 wording correction, attaching the review to the eventual registered result, and
reconciling outstanding confirmation/backlog fields.
The replay lane owns the unrun predicates, controls and receipts.
Keep `think-glg8` open until the mapped review and its required integration are present;
the present deliverable is the independent read-only mathematical audit.

Questions for the author, if a later reply requests the stronger assertions: can the
27-mode status be labeled explicitly as the force-bearing subsystem; is there a retained
path argument for the regularization; and can historical crossover mate identities or
run-version records be recovered?
None is a prerequisite for replaying the finite upper-bound certificate.

## Replay Addendum — Primary Certificate, 2026-10-19

**Verdict: accept the original certificate’s finite upper-bound claim on the retained
native replay.** The primary certificate places 183 unit squares in a square of exact
side `S'` stated above, so `s(183) <= S' < 13.999580178737 < 14`. The review found no
blocking mathematical defect in this replay.
This conclusion uses the replay lane’s completed deciding runs and my subsequent
read-only admission and source audit; I did not rerun geometry.

The original static audit above remains a record of what was known before that batch.
Its pending-replay statements are superseded for the primary certificate only.
The regularized certificate has not been replayed by this repository in this packet.
The declaration names no `same_packing` comparison.

### Retained Execution and Admission

The record lane completed the bounded batch at `2026-10-19T07:47:45.011658Z`. It used
the primary Python 3.14.7 interpreter, one worker, and a 100-second ceiling for each of
three jobs, within the declared 360-second batch ceiling.
The retained process log reports 34.87 seconds wall, 32.38 seconds user and 0.48 seconds
system time.
Native job timings total 31.27 seconds wall and 30.55 seconds route CPU; the
longest job took 10.79 seconds.
These are measurements of this batch, replacing the earlier unmeasured price for the
work actually performed.

The deciding invocation retained by that lane was:

```text
python -m devtools.upper_bound_reports evand-n183-subgrid-2026-10-19 certify --jobs-dir /Volumes/spud-ext1/agent-scratch/squares-intake-followup-20261019/n183-primary-jobs-01 --workers 1 --timeout 100
```

The metadata identifies that `python` as
`/Users/levy/wrk/github/squares/packing/.venv/bin/python3`. All three jobs completed and
the driver exited zero; its implementation requires each child’s zero exit and complete
native JSON before assembling the receipt.
Each job’s retained stdout and stderr are empty.
The source producer’s two checkers were not run.
The batch metadata records the interpreter and importer revision but not the full
execution environment.
The record lane should retain the already known certify working directory and full
`PYTHONPATH` value during integration; this provenance follow-up calls for no rerun.
The explicit import path below belongs to my separate admission command.

I separately ran this maintained admission command from the record worktree’s `packing/`
directory:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=/Users/levy/wrk/github/squares/.worktrees/confirm-422/packing:/Users/levy/wrk/github/squares/.worktrees/confirm-422/packing/src
/Users/levy/wrk/github/squares/packing/.venv/bin/python3 -m devtools.upper_bound_reports evand-n183-subgrid-2026-10-19 check --n 183
```

The external task scratch paths were set for `TMPDIR`, `CARGO_TARGET_DIR` and
`UV_CACHE_DIR`; the existing mounted scratch directory was checked first.
The command exited zero with **“1 certificates and 3 jobs admitted”** and the exact
positive margins below.
It did not use `--replay`. `upper_bound_reports.check_certification` calls the native
receipt validator, and calls the geometry replay only when that explicit flag is set.

The recorded importer revision is `f57ede12ce64cd1c74336d380b607478361c34c3`. At audit
time the record checkout was `e72a3b6f0b7174ccc2312649d2d3e7af54c648b3`. A
`git diff --name-only` against the importer revision returned no differences for the six
reviewed importer, conversion and geometry modules.
This identifies the inspected maintained code; it does not bind correctness to a Git
identifier.

### What Was Bound and Decided

The admission path first checks packet custody through `acquire_source.check`. Its
`evand-cert` adapter passes the declaration’s expected `n=183` to the strict parser.
That parser requires a positive rational side, exactly 183 pose rows, exactly three
rational literals per row, and no trailing data rows.
The declaration’s offered fraction must equal the parsed side exactly.
The retained primary bytes still have SHA-256
`279e70d1c7fb0bc181e3e9d313e7350b672d85e223296f252b92f2916d6e5df5`.

The native receipt has exactly the declared two routes and three ordered jobs.
For every job, `validate_job` compares the entire canonical deciding input with the
complete source or specified control: count, exact side and all 183 rational poses.
It also requires the native route identities, exact field, Boolean verdicts, failure
lists, full pair count, rational diagnostic signs and limitation statements.
It therefore resolves **M2 for this primary replay**; the source parsers’ weaker
behavior remains relevant if those separate programs are run later.

The finite decisions use these maintained implementations:

- `packing/src/sqpack/witness.py:exact_verify` materializes a rational center-basis
  witness and calls `packing/src/sqpack/verify.py:verify_packing` with exact rational
  sign, shape checking enabled and bucketing disabled.
  Every edge is checked to have squared length one, every corner to be a right angle,
  every corner against all four walls, and every unordered pair against the four
  square-edge separating axes.
- `packing/devtools/check_rational_witness_independent.py:check_squares` receives the
  complete rational corners produced by `evand_exact_certificates.Pose.corners`. It
  independently checks all four unit edges, adjacent orthogonality and opposite-edge
  closure, then all wall inequalities and every unordered pair by exact projection
  intervals.

Both routes count `183*182/2 = 16653` pairs in every job; neither samples pairs or uses
a floating-distance shortcut here.
Both accept boundary contact, which is permitted for a packing with disjoint interiors.
This particular original certificate has strictly positive recorded minima:

```text
minimum containment clearance = 1/200000000000000000000 = 5e-21

minimum best pair projection gap =
410634701261530154144724882523964107748445496442011038260368168329024992759793889459
/
41063470126153058863231934179550054728762808827746798831660799169182564000000000000000000000000000000000
```

Both native outputs contain exactly that same fraction.
Its numerator and denominator are positive.
It is a separating-axis projection gap, not an asserted exact shortest Euclidean
distance. No rounded “about `1e-20`” value is used to decide its sign.

The duplicate control replaces pose 1 by pose 0 while retaining the count, side and all
other poses. It is a valid unit square coincident with another valid unit square; both
routes reject it with minimum pair gap `-1`. The outside control adds `S'+2` to pose 0’s
x-coordinate, preserving its shape and the header.
From the accepted positive input, its shifted corners must lie beyond the right wall.
Both routes reject containment, returning

```text
-396700432066516800003342003333326859/25000000000000000000000000000000000
```

The positive row has empty failure lists in both routes.
The duplicate’s failures name overlap; the outside row’s failures name the right wall.
These controls exercise geometry after parsing.
The complete native cases match their corresponding durable raw job JSONs under
sorted-key JSON comparison; all three `cmp` commands returned equality.
I also read the existing receipt-mutation test cases for missing rows, altered inputs,
missing controls, incomplete pair counts and forged outcomes; I did not execute tests.

### Custody of the Audited Evidence

The following paths are repository-relative in the record author’s worktree,
`/Users/levy/wrk/github/squares/.worktrees/confirm-422`. Let `P` denote
`packing/resources/web/evand-n183-subgrid-2026-10-19/` in this table.

| Evidence | SHA-256 read during this audit |
| --- | --- |
| `P/acquisition/declaration.json` | `1c61a86335b982e451b24c4077205bd31f738b480602a819d044161f59090d8f` |
| `P/acquisition/sources.json` | `3c35c616a8b5cc7ba2a2e70666d091e40d179f8d244ec6b6fa1c2f80f69ff54d` |
| `P/acquisition/report.json` | `237d7573e2a2b169c8f0b909004571d64ce66de977942abd4e9b6270708315f9` |
| `P/receipts/exact-certification.json.xz` | `ca671960f55d78c16a36bd5ac56a55b7c3b7ba406ecb517639f7801cb3a8ee37` |
| `packing/campaign/issue-intake/intake-followup-20261019/n183-primary-replay.json` | `52506cddf8587a4d08e0fe79e398e8845421755c149d2a3278b94020b42f2a20` |

The raw native jobs and process log are retained outside disposable scratch under
`/Volumes/spud-ext1/agent-source/squares-intake-followup-20261019/n183-primary-replay-01/`.

| Relative path there | SHA-256 |
| --- | --- |
| `jobs/n183-positive.json` | `5e5a353d37f34e126d03b6ca4304df27282698ab1a2e2d0e60ca5bae3789cc55` |
| `jobs/n183-duplicate-square-overlap.json` | `df5281fac330593f3e356c8622b8b52b848eb7c4093c745720ce607888645e8e` |
| `jobs/n183-square-translated-outside-container.json` | `30a36ecee2b0b76651ab356428403447ffea9823f58ab88e25f5f89ba56fe244` |
| `run.log` | `07d0fb1046c5de9e7cf5cd677c1dff1ccafa1de3f1d2929c9fa2e58001b9d9f4` |

These digests bind this review to the evidence bytes inspected.
They do not replace the native geometry decisions or prove that execution occurred.
That execution is recorded by the separate replay lane and its retained jobs and log.

### Independence, Rating and Remaining Integration

The primary replay uses the project’s pre-existing geometry implementations, not the
source’s deciding programs.
The two maintained routes share the strict parser, half-angle conversion, Python
`Fraction`, runtime and separating-axis theorem.
Their distinct geometry implementations do not constitute two different mathematical
methods. This batch also does not establish independent human authorship, a separate
model family or a clean room.

The conversion module’s retained read log states that its author read the producer’s
certificate format and both checkers, and copied or imported none of their code.
An `independent-implementation` relationship to the producer is supported by that record
and the inspected call path, subject to recording the actual authorship and exposure
metadata required for the new evidence entry.
Use `clean_room: false`; this review cannot reconstruct unrecorded author identities or
prompt separation. Distinguish this relationship from the shared components between the
two maintained routes.
No new deciding program was authored in this review.

I propose **V3/C3 for the original finite upper bound when this replay is integrated and
cited by the actual result**, with complete coverage and retained controls.
Under `epistemics.md`, a recorded confirming-origin exact certificate replay suffices
for those rungs even when the final reviewer admits retained receipts rather than
rerunning geometry. An accepted mathematical review is a separate intake-workflow
obligation; it is not an extra requirement invented by the V3/C3 definitions.
The existing Stage 3 registration proposal may remain V0/C0 until the coordinator
performs the separate reviewed mapping and evidence integration.
I changed no rating, registry, result ID, house or case bound.
V4/C4 would additionally require the prescribed two accepted distinct reviews and human
oversight; neither follows from these two software routes.

M1 remains nonblocking and its intake wording correction is present: the 27 numerical
candidate flat modes concern the 182-square force-bearing subsystem, with one free
rattler excluded from that count.
Nothing here proves a local minimum, exact rigidity, a flat-motion family, or the
smaller numerical `S_exact`. M3 and M4 remain: the regularized certificate is
unexecuted, endpoint feasibility would not prove a no-expansion path or packing
identity, and neither priority nor the missing crossover lineage is supplied by this
geometry replay. Preserve Evan Daniel’s credit after Francisco Couzo and the unlogged
mates.

The record lane must map this review to a durable project review path and the eventual
actual result, retain the complete controls, record the deciding and premise-checking
programs with their true independence metadata, and disposition M1–M4 explicitly.
The relevant existing program IDs are `V-sqpack-verify` and
`V-check-rational-witness-independent` for decisions, and `V-upper-bound-reports`,
`V-evand-arrangement-receipts` and `V-evand-exact-certificates` for the import,
conversion and receipt premises.
Custody admission must also remain represented.
The regularized/source-checker work remains separate and is unnecessary for accepting
this one primary finite upper bound.

Keep `think-glg8` open until the mapped review and required integration exist.
The replay audit itself is complete; no additional geometry run is requested.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
