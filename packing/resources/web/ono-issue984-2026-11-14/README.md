# Roberto Ono’s s(228) Certificate at b5636fd

This packet retains part of
[RobertoOno/squares-in-square](https://github.com/RobertoOno/squares-in-square/tree/b5636fd6694d2cc7aa5811ae33f441268b81b714)
at `b5636fd6694d2cc7aa5811ae33f441268b81b714` (committed 2026-11-14T20:26:58Z), the
repository’s `main` when it was fetched at 21:07Z on 14 November 2026, for
[issue #984](https://github.com/jlevy/squares/issues/984). The issue names
`fce076f2bf459a25be3645d899e8950b93ed977c` (20:10:31Z), 54 seconds before it was posted
at 20:11:25Z; `b5636fd` merges the run branch, whose one commit past `fce076f`,
`956f868` (20:11:53Z), changes only the run’s `FOLLOWUP.md`, which records the posting,
and the two issue texts as posted.
Every certificate, text copy and check output retained here has the same Git blob at
both commits. The certificate was first committed in `be713b7` (2026-11-11T22:15:40Z);
`FOLLOWUP.md` says the branch was pushed to the public repository at `fce076f` before
the issues were posted, and GitHub’s activity log was not read.

This is the account’s first contribution to this repository: #984 and #985, posted one
second apart, are its only issues, and neither had a comment when this packet was
written. The intake label was added at 20:55:17Z.
[ono-issue985-2026-11-14](../ono-issue985-2026-11-14/README.md) retains #985’s
certificate at 147 from the same pin.

## What the Source Claims

- `runs/2026-11-11_fable-5.2/certificates/n228_S59604312.json`, an exact rational
  certificate of 228 unit squares, each its centre `(cx, cy)` in [0, S]² and
  `t = tan(θ/2)`, bounds s(228) by its rational side, whose 12-place ceiling #984
  prints, 15.596043120921. The issue also prints the side to 30 places before an
  ellipsis, 15.596043120920791646977220704185, the side’s floor there.
  It states the gain on the registry’s 15.60460147572967429 (T-174, read at `main`
  `fa980f8e`) as 0.008558354808882, the exact gap’s floor at 15 places.
  It claims an upper bound only: no optimality, KKT or rigidity claim.
- `evidence/registration/n228.cert` is the same packing as text (`n S`, then `x y t` per
  square). `n228.strict.cert` and `n228.strict.json` are the packing moved by (10⁻¹⁵,
  10⁻¹⁵) in a square of side S + 2 × 10⁻¹⁵, for checkers that need positive wall
  margins; the issue says the packing touches the four walls.
- The issue reports three checks, run by the author: the repository’s frozen verifier
  `verify.py` (exact `Fraction`, separating axes, all 25,878 pairs) VALID;
  `search/indep_check.py` (exact rational polygon clipping, 525 close pairs) PASSED; and
  `search/fu_strict_check.py` on the strict copy STRICT VALID, least pair margin 2.389 ×
  10⁻¹⁰ and least wall margin 10⁻¹⁵. It says the first and third share the
  separating-axis method and the half-angle parametrisation, that the second and third
  were written by the agent that found the packing and the first fixed before the
  search, and that none is this registry’s verifier.
  Those statements are the author’s; no source program ran here.
- **The leaderboard, disclosed first.** The issue opens by saying the packing does not
  beat the Kaggle per-puzzle leaderboard’s side-only entries at 228,
  15.596043116631669919627353… (team Nevska, 8 November), 4.289 × 10⁻⁹ below the side,
  and 15.596043116646272293906688… (team square1000, 29 October), 4.275 × 10⁻⁹ below,
  neither of which supplies a packing.
  It says the open request #983 (Doğa Özden, 15.600801734812) lies 0.004758613890 above
  this packing and that the two arrangements were not compared.
- **Lineage.** Francisco Couzo’s packing of 404 squares as this registry retains it
  ([couzo-issue763-2026-10-23](../couzo-issue763-2026-10-23/README.md), `n404.cert`),
  mirrored, every square with 13.8 ≤ x + y < 23.8 deleted and the rest moved by (−5,
  −5), which removes five periods of its band; a penalty step and an exact-constraint
  sequential-LP polish give 15.597084912 (`n228_S59708491.json`, also certified,
  retained here, 15.597084911486421…), and basin hopping that re-seats cells at the
  band’s ends (`search/attack.py`) gives the claimed side.
  The issue asks that Couzo’s n = 404 packing be credited as the start, and says Couzo’s
  n = 906 packing with fifteen periods removed gives the same intermediate value.
- The run’s `REPORT.md` records that the run first reported this packing as an
  improvement and then withdrew that word when it found the side-only leaderboard
  entries, calling both packings rediscoveries of leaderboard sides and, as far as it
  found, the first public packings at them.
  Its calibration certificates at 11, 17, 18 and 19, each within 3 × 10⁻¹² above its
  record by the report, are not claimed and not retained.
- **AI assistance.** The issue says the packing was found, certified and checked by an
  AI coding agent (Claude, by Anthropic) working in the repository’s harness, with a
  person who set the harness up, directed the work and read the request before it was
  posted; the agent drafted the text.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is 25 files: 24 retained under [source/](source/) and one raster pinned by
digest.

| File | Bytes |
| --- | --- |
| `LICENSE` | 1,068, the MIT notice |
| `README.md`, `VERIFIER.sha256`, `verify.py` | 3,501, 163 and 7,815: the harness README and its frozen verifier with its digests, never executed here |
| `runs/2026-11-11_fable-5.2/REPORT.md`, `RUN.md`, `FOLLOWUP.md` | 26,944, 4,398 and 8,679 |
| `certificates/n228_S59604312.json` | 69,224, stored compressed: the claim |
| `certificates/n228_S59708491.json` | 70,358, stored compressed: the intermediate packing at 15.597084912 |
| `evidence/registration/n228.cert` | 59,363, the same packing as text, which the reader holds equal to the JSON |
| `evidence/registration/n228.strict.cert`, `n228.strict.json` | 69,784 and 76,617 (stored compressed): the copy moved off the walls |
| `evidence/registration/` check outputs and `issue_n228.md` | the author’s verifier, clipping and strict-check outputs, and the issue as posted |
| `evidence/candidates_notes.md`, `kaggle_per_puzzle_check.md` | 7,390 and 6,762, the run’s notes on the candidates and the leaderboard |
| `search/README.md`, `attack.py`, `indep_check.py`, `fu_strict_check.py` | 5,672, 28,524, 3,690 and 3,756, never executed here |
| `evidence/cand228_refined.png` | 128,181, pinned by digest: a picture that decides nothing |

The SHA-256 the issue states for the JSON (`98987101…0274944`), the text copy
(`be120af6…51e3f4`) and the strict copy (`e243de77…48569`) are the files’.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is about half a megabyte in a checkout and far less as Git stores it, so it
is kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `473577f42` on 14
November 2026), through the `ono-json` reader added for this source:

- **228:** exact side 15.5960431209207917 rounded up at 16 places, below the case’s
  house, T-300 (Doğa Özden’s column-band packing, adopted earlier the same day), by
  4.7586 × 10⁻³, the 0.004758613890 the issue states as the gap to #983, and below
  T-174, the house before it, by the 0.008558354808882 the issue states.
  No other register bound is pending adoption at 228.

## Report Order

The
[ledger of 14 November for this lane](../../../campaign/issue-intake/upper-bounds-984-985-20261114/README.md)
walks every report at 228 in the order it reached this repository, from a start frozen
at `main` `473577f42`, where #983 is the house as T-300, and records this packet’s claim
as a new packing. The two side-only leaderboard entries the issue states first are
unpublished and state no packing, so they are no reports and are recorded as context
only.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-300’s and T-174’s
packets, the house witness and the regularized view, and wrote
[measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **Against T-300**, the house: no symmetry of the box pairs it one to one with T-300’s
  packing by nearest centres.
  The optimal assignment, best under symmetry 0, moves 227 squares beyond 10⁻³, 137
  beyond 0.01 and 96 beyond 0.1 (largest 0.963975), and turns 90 squares by more than
  10⁻⁶ radians, by up to 43.68 degrees; aligned by box centres, 72 squares turn by more
  than a degree and 22 tilts reverse.
  The house witness and its regularized view measure as T-300.
- **Against T-174**, likewise none: 89 squares beyond 0.1 (largest 0.906908).
- Tilted beyond a degree: 55 here, at 1.29 to 43.68 degrees, 19 one way and 36 the
  other, against T-300’s 48, all one way, and T-174’s 51. So it is a new arrangement
  relative to both, not a further arrangement of either; its band is Couzo’s 404’s, cut,
  as the issue says.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 155,268 pair decisions, 24.6 seconds of job wall time
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 2.389 × 10⁻¹⁰, squares 8 and 21, the margin the author’s strict check reports,
exactly. `check --replay` decided the three jobs again.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
10⁻³⁰ past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)), with the
expected verdicts of the gross and sharp controls stated in a plan hashed before any run
of either certificate (SHA-256
`4eb6cc4e828c525e40994e5fd1e2e4dcca09ff55e7867119ecfe265737c121e3`, 21:12:34Z on 14
November, recorded on the bead).
It lowered the side by the least far-wall clearance, 0, closed the least-gap pair
(square 21 toward 8) by its gap, and moved every square toward the nearer near wall by
its least clearance, 0: both routes accepted each at contact with margin 0 and refused
each past it.
It enlarged one square to its pair and one to its wall: both routes refused
the first, square 8, at contact for its shape alone, and accepted the second, square 22,
which already touches its wall and so grew by 0, at contact; both refused each 10⁻³⁰
past it for the overlap or the wall as well.
Both refused a duplicated square.
All 11 were as stated in advance.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read the certificate through the `ono-json` reader.
Neither shares code with the author’s three checkers, which were not run here.

## The Gain Against Padding

`devtools.contraction_margin` contracted each certificate uniformly about the origin to
first contact and boxed it, each contracted packing decided on both maintained routes:

- **T-300**, the house: margin 2.949 × 10⁻¹² (1 − λ\* = 101/500000000000101, squares 118
  and 119), as its own packet measured.
  The gain, 4.7586 × 10⁻³, is 1.61 × 10⁹ times it
  ([measure/contraction-n228-t300.json](measure/contraction-n228-t300.json)), so it lies
  outside T-300’s padding, and RV-3 (think-ruu2) does not reach it.
- **T-174**: margin 0, squares 201 and 227 touching
  ([measure/contraction-n228-t174.json](measure/contraction-n228-t174.json)).
- **This certificate**: margin 3.4875 × 10⁻⁹ (1 − λ\* about 2.389 × 10⁻¹⁰, squares 8 and
  21, the least-gap pair), the padding its harness’s rounding repair leaves
  ([measure/contraction-n228-own.json](measure/contraction-n228-own.json)); contracted,
  it would be a square about 3.49 × 10⁻⁹ smaller, still about 8.0 × 10⁻¹⁰ above the
  lower of the side-only leaderboard entries.
  Nobody reported that side, and it is not registered (RV-3).

## The L Step

`devtools.l_step_scan`, with this side stood in for 228’s ceiling, finds the same L-step
and monotonicity consequences as on `main`: this bound carries to no other count
([measure/l-step-scan.json](measure/l-step-scan.json)).

## Stage 4 Review

The stage 4 mathematical review of 14 November 2026
([review-2026-11-14-ono-984-985.md](../../../../docs/project/reviews/review-2026-11-14-ono-984-985.md)),
written in a separate lane (L163) blind to this one throughout, accepts both
certificates with fourteen findings, all notes, none blocking, and scores each S3. Its
clean-room checker decides every square, wall and pair by separating axes in Python
integers and by exact Sutherland–Hodgman clipping in GMP rationals, with 40 controls
stated before they ran, all 40 as stated, and accepts the squares in the box of the
claim’s own side, 15.596043120921, and refuses them in the box of its 12-place floor
(F4). Its programs and receipts are kept in the review-only directory beside this
packet, [ono-984-985-review-2026-11-14](../ono-984-985-review-2026-11-14/README.md).

This lane recorded its replay, controls and measurements in its intake commit
(`3f0976140`, 21:29Z) and registered T-301 and T-302 (`fcce6be56`, 21:44Z) before it
read the review. It read the review’s frozen findings (`8504d8e04`, frozen at 21:17Z) at
21:45Z and its final head, the checks after the freeze (`6d1e3383e`, 21:54Z), at 21:56Z,
and merged that head before mapping it.
Read against this packet’s receipts once both were done, the review’s least pair margin
(2.38935 × 10⁻¹⁰, squares 8 and 21) is the replay’s exactly, and square 22, the square
the sharp controls grew at its wall, is one of its four wall contacts (22 at the left,
31 and 34 at the bottom, 144 at the right).
Its contraction receipts for T-174 (0, squares 201 and 227), T-300 (2.949 × 10⁻¹²,
squares 118 and 119) and this certificate (3.488 × 10⁻⁹, squares 8 and 21) equal
[measure/](measure/)’s in margin, factor and binding pair, and its identity measurement
against T-300 and T-174 equals [measure/identity.json](measure/identity.json) under
nearest centres, the optimal assignment and box-centred alignment, as do the tilt
counts. No disagreement.

What the review adds:

- **Three walls, not four** (F5): no square touches the top wall, cleared by 1.77 ×
  10⁻¹² at square 114, so the side is the packing’s extent in x.
- **The lineage** (F9): the stated cut of Couzo’s 404 gives 228 squares only under the
  mirror x → S − x (or a quarter turn) and with two squares dropped whose centres land
  outside the new box, neither of which the issue names; so read, the deepest overlap is
  0.101287, as stated, and the certificate lies 34 squares beyond a tenth from that
  seed. Removing a band period is new to the record (F10).
- **A new arrangement** relative to every registered packing at 228: T-300, T-174,
  T-128, T-098, T-092 and T-056 (F12). No s(m) + k is the side within 10⁻⁹; the nearest
  is s(37) + 9, 2.58 × 10⁻³ away.
- **The prints** hold (F14), and two of the author’s checkers decide by `assert` (F13).

Its six questions for the author, informational and holding nothing open:

1. Which mirror was applied to Couzo’s 404, and were the two squares landing outside the
   new box deleted (F9)?
2. Would the issue say three walls, naming the wall each packing misses (F5)?
3. Would the format state the box [0, S]² and the sense of θ (F6)?
4. Would `indep_check.py` and `fu_strict_check.py` raise rather than assert, and
   `verify.py` refuse a missing `t` and unknown or duplicate keys (F13)?
5. Would the `.strict.json` digests be stated beside the `.strict.cert` ones (F7)?
6. Will the diagonal-period sweep’s table of near misses be published?

## Adoption

The case adopted the certificate as its house at 228 in the pass of 15 November 2026
under the house rule, as T-301, in place of T-300, which the pass of 14 November had
adopted there and which keeps its certificate as history; this lane wrote the adoption
at 00:01Z, since one day’s archive holds one prior state a count.
Roberto Ono is the packing’s finder, from a band cut of Francisco Couzo’s packing of 404
squares, below Doğa Özden’s column-band packing, as the issue asks.
Both strong generators ran on the new witness
([the runs](../../../cases/regularized_drawings/think-17ex-2026-11-15/README.md)):
grid-slack’s views at 0.5, 1 and 5 degrees go to review at row 7, two per-square counts
falling while no total does, and Evan Daniel’s same-side view is refused at row 7, so
the axis tool’s view of the new witness stays drawn and the count is decided no better
on it. Daniel’s regularizer solved the witness to a KKT point, a local minimum 4.289 ×
10⁻⁹ below the side, 1.23 times the certificate’s own contraction margin
(3.488 × 10⁻⁹) and beyond it; its rational certificate did not validate, and it is held
at row 3 as a
register candidate and not admitted (RV-3). Its side agrees with the side-only
leaderboard entry the issue quotes first, Nevska’s 15.596043116631669919627353…, at all
24 printed places.
The rigidity block, derived again on the new witness, stays not rigid:
110 of its 228 squares translate, against 123 of T-300’s.

## What Is Not Established

- **Human oversight.** One AI review is retained; no human oversight record.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurement above shows; the cut
  from Couzo’s 404 was not rebuilt here.

## Credit and Licence

The packing is Roberto Ono’s, found by the AI agent his harness directs, from Francisco
Couzo’s packing of 404 squares with five band periods cut out, as the issue says and
asks to be credited.
The record at 228 before this import was T-300, Doğa Özden’s column-band packing, and
before it T-174, Couzo’s packing as PingYou Ltd improved it.
The harness reads its starting packings from this registry’s witnesses
(`search/witness_io.py`, not retained), so its lineage builds on this project.
The bibliography key is **[Ono issue 984 2026-11-14]**.

The repository is published under the MIT licence, copyright (c) 2026 Roberto Ono, as
[source/LICENSE](source/LICENSE) states; it names no other licence for the run’s data,
and the certificates and their copies are retained under it, beside it.

## Commands

From `packing/`, with the project interpreter.
The identity measurement reads the house witness and its regularized view as they stood
at main `473577f42`, before any adoption replaced them, so it reproduces there; the
contraction margins read the packets and reproduce anywhere
`devtools.contraction_margin` is:

```bash
python -m devtools.acquire_source ono-issue984-2026-11-14 --checkout CHECKOUT
python -m devtools.acquire_source ono-issue984-2026-11-14 --check
python -m devtools.upper_bound_reports ono-issue984-2026-11-14 check-claims --write
python -m devtools.upper_bound_reports ono-issue984-2026-11-14 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ono-issue984-2026-11-14 check --replay
python -m devtools.upper_bound_reports ono-issue984-2026-11-14 sharp-controls
python -m devtools.measure_identity --n 228 'ONO=packet:ono-issue984-2026-11-14' \
  'T-300=packet:ozden-s228-upper-bound-2026-11-14' \
  'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-228-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-228.yaml' \
  --out resources/web/ono-issue984-2026-11-14/measure/identity.json
python -m devtools.contraction_margin --n 228 'T-300=packet:ozden-s228-upper-bound-2026-11-14' \
  --against 'ono-984=packet:ono-issue984-2026-11-14' \
  --out resources/web/ono-issue984-2026-11-14/measure/contraction-n228-t300.json
python -m devtools.contraction_margin --n 228 'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  --against 'ono-984=packet:ono-issue984-2026-11-14' \
  --out resources/web/ono-issue984-2026-11-14/measure/contraction-n228-t174.json
python -m devtools.contraction_margin --n 228 'ono-984=packet:ono-issue984-2026-11-14' \
  --out resources/web/ono-issue984-2026-11-14/measure/contraction-n228-own.json
python -m devtools.l_step_scan --with 228=S228 \
  --out resources/web/ono-issue984-2026-11-14/measure/l-step-scan.json
```

In the last command `S228` is the `exact_side` in the packet’s claim record.

## Compressed Files

| Stored file | Origin | Git blob of stored file | SHA-256 of decompressed source |
| --- | --- | --- | --- |
| `source/runs/2026-11-11_fable-5.2/certificates/n228_S59604312.json.gz` | upstream | `b72ce91fdd94816fb98eab293ed9f3d2bdbee6f0` | `98987101c5a14e84cc1bdcb7497cc139be6ef71a17f7e7ec9ce3f89c80274944` |
| `source/runs/2026-11-11_fable-5.2/certificates/n228_S59708491.json.gz` | upstream | `72f2c03c96a6eeeaf4c44a2b0253cd1a46836ada` | `37366dafbf0cda4b7e55b316399e964b92485d2357329dd7d301300064d5f35c` |
| `source/runs/2026-11-11_fable-5.2/evidence/registration/n228.strict.json.gz` | upstream | `09c57edbce2812d8e5ab958578bc1da36dfbd9ba` | `f6f4457cb8d767b70e8b3599ab424033203d3d464f61b7f2a7176fc8fb14e7e7` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
