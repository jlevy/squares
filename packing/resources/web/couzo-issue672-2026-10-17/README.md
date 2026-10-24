# Francisco Couzo’s Issue 672: 46 Certificates at af8cb795

Francisco Couzo’s [issue #672](https://github.com/jlevy/squares/issues/672), opened
2026-10-17T20:48:34Z, a follow-up to #670, asks to register 46 upper bounds for n = 227,
229 and 330 to 996, each the exact rational side of a certificate in
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/af8cb7959aead318c0cf5e9f873de3caa763f77a)
at `af8cb7959aead318c0cf5e9f873de3caa763f77a` (committed 2026-10-17T20:44:59Z) rounded up
at 12 places. His comment of 17 October
([issuecomment-6242081759](https://github.com/jlevy/squares/issues/672#issuecomment-6242081759))
says 227 and 229 are based on Joost de Winter’s recent #668 findings.
This packet retains the two rows in the n ≤ 324 case corpus, registered together as
T-227. Since 22 October it also retains the issue’s 44 rows beyond the corpus, recorded
as dated beyond-horizon rows ([Beyond the Corpus](#beyond-the-corpus)).

| n | Exact side of the certificate | Issue’s print, rounded up | SHA-256 |
| --- | --- | --- | --- |
| 227 | `71427829379429597600111901507/4589408083628500000000000000` | 15.563625652343 | `65b03df883e75f890eca985232252a6340b9b5da3437c41275c9201df03d8c17` |
| 229 | `231170315041711399213831561/14771101209934000000000000` | 15.650174740273 | `9ab667ec73e55b4570fdc427b9f9930831a3e3f07b6953a2e05c6aee0a07609f` |

Each certificate gives n unit squares, each a rational centre and a rational
$t = \tan(\theta/2)$, in Evan Daniel’s certificate format.
Their per-count JSON names a CT105 web submission at 227 (`f0ca7a65…`, method `fq`,
received 2026-10-17T20:28:22Z) seeded from de Winter’s #668 certificate by way of Evan
Daniel’s exact form of it, and at 229 an `slp` refinement (search job 106640) of de
Winter’s #668 certificate. The source’s manifest credits the 227 certificate to
Couzo, retaining de Winter’s seed credit; the CT105 web submission it names as its
provenance names no submitter (RF-3 of the 22 October review), and Couzo’s answer of 24
October says he made it himself ([The Author’s Answers](#the-authors-answers)).

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of a blobless clone at
the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
Retained: every certificate the issue links, `source/certificates/nN.cert` at its 46
counts, each with its per-count JSON `nN.json`, and one 227 certificate the per-count
JSON names as the 227 submission’s seed, 93 files, 5,656,441 bytes (2.05 MB as Git’s
zlib stores them): the 227 and 229 pairs at 01:24Z on 22 October for T-227, the 44
beyond the corpus from the same pin at 04:41Z, and the seed
`certificates/parents/cdd08485….cert` from the same pin on 24 October at 09:40Z, for the
author’s answers.
The repository states no licence for its data or prose, so the certificates and their
JSON are retained as factual data under the owner decision of 9 October 2026 recorded in
[known-best-packings/README.md](../known-best-packings/README.md).
Pinned by digest only: the root `README.md` and `upper_bounds.json`, the certificate
directory’s `README.md`, `manifest.json` and `SHA256SUMS`, and the source’s exact checker
`verify_bound_certificate.py` with its MIT licence `BOUND_VERIFIER_LICENSE.txt`, which are
byte-identical to the copies the [issue-678 packet](../couzo-issue678-2026-10-18/README.md)
retains and were not run.
The rest of the tree is pinned by the commit alone.

## Exact Replay

The certificates go through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, by the declaration-driven importer
`devtools.upper_bound_reports` ([acquisition/report.json](acquisition/report.json)):
`sqpack`’s exact witness verifier and the independent rational corner checker, each
deciding every wall and every pair over $\mathbb{Q}$ after an exact half-angle conversion.
Each count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process.
Both positives pass both routes, and both routes refuse all four controls. At 227 every wall is cleared by at least $10^{-15}$; at 229 a square touches the box, a least wall clearance of exactly 0, which the closed box allows; every pair clears by at least $1.19 \times 10^{-12}$. The 6 jobs made 310,542 pair decisions in 23.85 route CPU seconds, on one worker on 22 October 2026.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method. No source script ran here. The source’s
manifest names this repository’s `sqpack/verify.py` as its first checker, and the `sqpack`
route decides through that file, so the replay shares the producer’s components (RF-1 of
the [22 October review](../../../../docs/project/reviews/review-2026-10-22-couzo-670-672-675.md)).

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes each certificate against the
record on `main` at `d7923b8d`, 22 October 2026:

- 227: below the case’s house best packing, de Winter’s T-196, by $1.71 \times 10^{-4}$,
  and above Evan Daniel’s solved view of this packing (T-225) by
  $1.76 \times 10^{-11}$.
- 229: above the house, Evan Daniel’s #674 update (T-199), by $1.32 \times 10^{-5}$, above
  T-225 by the same and above his #674 opening (T-198) by $1.15 \times 10^{-5}$, and below
  T-196 by $1.67 \times 10^{-8}$.

The [18 October ledger](../../../campaign/issue-intake/upper-bounds-20261018/README.md)
recorded both in report order after #668; at 229 #674’s opening and update followed, each
smaller, so the 229 row enters superseded.

## Pose by Pose

[measure/identity.py](measure/identity.py) measures, from the retained packets, #672’s 229
against de Winter’s #668 witness, Evan Daniel’s #674 opening and update against #672’s
229, and #670’s and #675’s 204 against each other and T-223, and writes
[measure/identity.json](measure/identity.json). It loads the evand-regularized packet’s
measurement functions (nearest centres under the box’s eight symmetries, kept where one
to one, and an optimal assignment), and decides nothing:

| n | View against | Nearest centres | Moved beyond $10^{-3}$, $10^{-1}$ | Largest move | Largest turn |
| --- | --- | --- | --- | --- | --- |
| 227 | #672 against T-196 | one to one | 59, 0 | 0.0796 | 5.842° |
| 229 | #672 against T-196 | one to one | 57, 0 | 0.00941 | 0.0308° |
| 229 | T-198 against #672 | none one to one | 167, 77 | 0.807 | 38.26° |
| 229 | T-199 against #672 | none one to one | 188, 79 | 0.873 | 38.26° |
| 204 | #675 against #670 | one to one | 63, 5 | 0.143 | 1.097° |
| 204 | T-223 against #675 | one to one | 70, 0 | 0.0847 | 2.584° |

The 227 row is the evand-regularized packet’s measurement, which read a fetched copy of
the same bytes. So #672 refines de Winter’s packing at both counts, which T-227’s
regularization items record, and Evan Daniel’s #674 packings, which #674 says started
from #672’s, are other arrangements of it. Evan Daniel’s solved view at 227 (T-225) is a
regularization of the packing T-227 holds, as its source says: nearest centres pair the
two one to one under a half turn, 194 of its 227 squares lie within $10^{-6}$ of #672’s,
16 move beyond $10^{-3}$ and 3 beyond a tenth, at most 0.168. That the two are one
packing is the source’s claim, measured here and not decided.

## The Author’s Answers

Francisco Couzo’s [comment of 24 October](https://github.com/jlevy/squares/issues/672#issuecomment-6380747582)
answers the two questions of the 22 October review; it says Claude Code assisted with it.
He made the 227 CT105 submission himself: CT105 is the server behind his search web app,
which only he runs, so the credit is his, after de Winter, as the manifest says.
He says the task was seeded from the source’s retained 227 witness `cdd08485…`, “which
is de Winter’s #668 certificate”, and that his record lists Evan Daniel’s
`alt/n-227.cert.gz` as that certificate’s seed.
His `verify.py`, he says, is this repository’s `packing/src/sqpack/verify.py` at
`37e6757`, byte for byte (`main` still holds the same Git blob): exact rational corners
from each `x y t` line, passed to `verify_packing(corners, S, sign, bucket=True)` in the
closed box. His strict verdict is false at 229 only because squares touch the walls, and
true at 227.

[measure/answers-2026-10-24.py](measure/answers-2026-10-24.py) holds the answers to the
retained files and writes [measure/answers-2026-10-24.json](measure/answers-2026-10-24.json),
in about 3 seconds; it decides nothing:

- **The digests.** The three prefixes the comment prints, `cdd08485`, `65b03df8` and
  `9ab667ec`, are the SHA-256 this packet’s manifest records for the witness and the 227
  and 229 certificates.
- **The witness.** `certificates/parents/cdd08485….cert`, first committed at the pin with
  the issue’s certificates, is not de Winter’s certificate (SHA-256 `7d386887…`). Its
  exact side, `8556247787153006491973257/549755813888000000000000`, is
  $7.26 	imes 10^{-5}$ below T-196’s and below the side the per-count JSON records for
  Daniel’s `alt/n-227.cert.gz`, which the 22 October review measured as Daniel’s exact
  form of de Winter’s certificate. Nearest centres pair it with T-196’s packing one to one
  under a reflection: 82 squares move beyond $10^{-3}$, none beyond a tenth, at most
  0.0887. #672’s 227 pairs with it one to one under the identity, 91 beyond $10^{-3}$,
  none beyond a tenth, at most 0.0793, $9.84 	imes 10^{-5}$ below it. So the witness is
  de Winter’s packing part of the way to #672’s; how it was made is the source’s own.
- **The call.** The same call here counts 58 corner coordinates on the boundary at 229
  and none at 227, with no touching pair at either, as the comment says and as the
  replay’s least wall clearances, exactly 0 and $10^{-15}$, imply.

The answers change no credit: T-227 stays credited to Couzo after de Winter, Daniel and
this project, and its claim, T-225’s and this README now say he made the submission.

## Beyond the Corpus

The issue’s 44 rows from 330 to 996 read root `certificates/nN.cert`, each first committed
at the pin, four minutes before the issue
([receipts/first-commits.json](receipts/first-commits.json)).

[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) reads every
certificate a row beyond the corpus names from this packet once `acquire_source --check`
holds it, and decides it with the filtered two-route decision and the six controls of
[`devtools.couzo_678_replay`](../../../devtools/couzo_678_replay.py), reused unchanged:
route `sqpack` through `sqpack.witness` and `sqpack.verify`’s exact predicates, route
`independent` through `devtools.check_rational_witness_independent`’s, over every corner
against every wall and every pair whose centres are closer than √2 by exact comparison.
A unit square’s interior lies in the open disc of radius √2/2 about its centre, so no
other pair can overlap; both routes check that every square is a unit square whose corner
mean is that centre. The [18 October packet](../couzo-issue678-2026-10-18/README.md#exact-replay)
states the six controls.

**All 44 are verified.** Every printed side is its header side rounded up at 12 places,
and both routes accept every packing: 88,101 candidate pairs of 15,138,963, and every
corner against every wall. 35 touch the box and 6 have touching pairs, 394 in all, which
the closed contract allows; elsewhere the least pair gap is between 1.1e-12 (at 652 and
653) and 6.6e-11. **All 264 controls are refused by both routes.** The positive decisions
took 58.8 CPU seconds;
[receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json) keeps every
row’s side, both routes’ counts, least clearance, least gap and failures, the controls,
and the per-count JSON’s seed credit. The maintained all-pairs kernel,
`devtools.evand_arrangement_reports`’s two routes with no filter, decided every pair at
996: 495,510 pairs in 221.5 CPU seconds; both routes accept it, and their least pair gap
and wall clearance equal the filtered decision’s exactly
([receipts/exhaustive-sample.json](receipts/exhaustive-sample.json)). The all-pairs replay
of every row, about 4 CPU-hours for the three Couzo packets at that rate, is not run; the
filtered route is the replay of record, as for #678 and #715. Every side is below Göbel’s
classical construction at its count, by 1.44e-02 at 330 or more
([receipts/goebel-comparison.json](receipts/goebel-comparison.json)).

The [backlog ledger of 22 October](../../../campaign/issue-intake/upper-bounds-backlog-20261022/README.md)
walks every report at these counts from the 18 October ledger’s starts, frozen at `main`
`804eff369`, and records all 44. Each is superseded on entry by the next report the walk
records at its count: Couzo’s #675 (32), #678 (7) and #715 (1), and Darius Muglich’s
#686 (4). At nine of these counts #672 is the first report the walk records, and the
start there, eight of `couzo-verified-bounds-2026-10-14`’s rows and
`fang-excess-theorem-2026-10-13`’s at 932, now names #672 as its successor instead of the
#678, #686 or #715 row that had superseded it on `main`, so each count is one chain in
report order.
[acquisition/beyond-horizon-rows.json](acquisition/beyond-horizon-rows.json) is the record
the source register reads them from.

## Stage 4 Review

The [review of 22 October 2026](../../../../docs/project/reviews/review-2026-10-22-couzo-670-672-675.md)
accepted #672’s two certificates for finite feasibility, with eight findings, none blocking,
covering T-226, T-227 and T-228 together.
It reproduced this packet’s replay and frozen comparison, decided both certificates again on a
clean-room checker of its own, on an integer route and a `Fraction` route with exact
clipping area, and ran sharp controls at $10^{-30}$ through both maintained routes and
that checker: each route accepted exact contact at the far wall, the near wall and the
least-gap pair, and refused $10^{-30}$ past it, where the certificates keep $10^{-15}$ at 227’s walls, exactly 0 at 229’s and about $1.2 \times 10^{-12}$ between pairs.
Its programs, receipts and logs are kept with the #672 packet, in
[`review/review-2026-10-22/`](review/review-2026-10-22/README.md),
and `tests/test_upper_bound_reports_couzo_670_672_675.py` runs the kernel’s two sharp
controls on #672’s 227 certificate (RF-6).
T-227 rests at `V3`/`C3` on that review, the replay it reproduced and its checker’s run.

## Credit

Francisco Couzo, with refinements of Joost de Winter’s #668 packings, as his comment
says; the issue keeps every seed, construction and certificate credit in the source’s
manifest. The source discloses OpenAI Codex assistance with its checker.
Beyond the corpus the per-count JSON credits Joost de Winter’s seeds at 12 counts (652,
653, 759, 814, 815, 817, 872, 874 and 932 to 935) and his seed or construction at 816 and
873, Fang’s rectangle and gluing with PingYou Ltd’s square input at 757 and 813, and
Couzo’s at most of the rest; those statements are the source’s.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source couzo-issue672-2026-10-17 --check
python -m devtools.upper_bound_reports couzo-issue672-2026-10-17 check-claims
python -m devtools.upper_bound_reports couzo-issue672-2026-10-17 certify --jobs-dir "$TMPDIR/jobs" --workers 1
python -m devtools.upper_bound_reports couzo-issue672-2026-10-17 check --replay
python -m devtools.upper_bound_reports couzo-issue672-2026-10-17 register-plan
python -m devtools.beyond_horizon_replay check --issue 672
python -m devtools.beyond_horizon_replay check --issue 672 --replay --workers 2
python resources/web/couzo-issue672-2026-10-17/measure/identity.py \
    --out resources/web/couzo-issue672-2026-10-17/measure/identity.json
python resources/web/couzo-issue672-2026-10-17/measure/answers-2026-10-24.py \
    --out resources/web/couzo-issue672-2026-10-17/measure/answers-2026-10-24.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
