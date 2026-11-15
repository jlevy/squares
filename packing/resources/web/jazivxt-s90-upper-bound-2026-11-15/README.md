# jazivxt’s s(90) Certificate at f9b31b4

This packet retains
[dpre4ai/n90-square-packing](https://github.com/dpre4ai/n90-square-packing/tree/f9b31b4ebddb278a128b6cb5c43836a305a24dca)
at `f9b31b4ebddb278a128b6cb5c43836a305a24dca` (committed 2026-11-15T03:10:54Z), the
repository’s `main` when it was fetched at 03:13Z on 15 November 2026, for
[issue #989](https://github.com/jlevy/squares/issues/989), opened by the account
`dpre4ai` at 03:00:53Z. The issue names the head’s parent, `179fcba` (03:00:42Z), 11
seconds before it; the pin adds only a construction figure, `n90-construction.png`, and
every other file has the same Git blob at both.
The certificate was first committed in `e5c2ecc` (03:00:02Z), 51 seconds before the
issue, with the bytes the pin keeps; `179fcba` changed only the AI collaborator’s name
in `README.md`, from “Codex Astra Ultra” to “GPT-6 Astra Ultra”, and that file’s line in
`SHA256SUMS`. Every commit is by the account’s committer, “Daniel”.
This is the account’s first contribution to this repository: #989 is its only issue,
with no comment when read.

## What the Source Claims

- `n90.cert`, Evan Daniel’s text format (the count and the side, then each square’s
  centre `x y` in [0, S]² and `t = tan(θ/2)`, all rational), bounds s(90) by its side,
  4999138583463/500000000000 = 9.998277166926, which terminates at 12 places; the issue
  and `README.md` print it exactly.
  The issue states the gain on the side 10 of this registry’s n = 90 case record as
  0.001722833074, exactly the gap.
  It claims an upper bound only and says the exact optimum remains open: no optimality,
  KKT or rigidity claim.
- `README.md` says the origin is the lower left corner and positive θ turns
  counterclockwise; `n90.csv` lists the same squares’ centres rounded and their angles
  in degrees, in certificate order, and `n90.png` draws the packing.
- **Checks.** The issue and `README.md` say Francisco Couzo’s public checker,
  `verify_bound_certificate.py` at franciscouzo/square-packing `712c6a6` (“based on Evan
  Daniel’s verifier”), accepted the certificate in strict mode, positive clearance from
  every wall and separation between every pair, and that a separate exact check tested
  all four walls per square and all 4,005 pairs, both in rational arithmetic by
  separating axes, the least pair separation on a certifying axis about 1.19448 × 10⁻¹².
  Neither check’s output is published, nor the second checker.
  The checker at `712c6a6` is already in the record: its blob, `0c305135`, is the
  `verify_bound_certificate.py` the couzo-issue678-2026-10-18 packet retains and the
  couzo-issue843-2026-10-28 and couzo-issue844-2026-10-28 packets pin at that commit, so
  nothing further is retained for it.
  Those statements are the author’s; no source program ran here.
- **Lineage.** The issue and `README.md` say the construction started from a rectangular
  crop, about 12.993303 wide and 9.353384 high, of Joost de Winter’s n = 157 packing
  (JoostdeWinter/square-packing `c70defa`, `n157/n157_exact.json`, the same Git blob,
  `079d4cb1`, as the copy the de-winter-s157-upper-bound-2026-11-11 packet retains for
  T-293, his pinwheel and 157’s house); successive copies offset horizontally by one
  unit fit together at a vertical pitch of 9.019403 in place of about 9.353384; a square
  window across two copies held 90 squares, whose centres and orientations were then
  tightened and made exact.
  The README says the arrangement was found during Kaggle’s Squares in Squares
  competition.
- **Credit and AI assistance.** The issue asks for credit to “jazivxt and GPT-6 Astra
  Ultra”, links jazivxt’s Kaggle profile and says GPT-6 Astra Ultra was the AI
  collaborator on the search and verification; the first published README (`e5c2ecc`)
  named it “Codex Astra Ultra”.
  The record credits people, not AI agents
  ([attribution.md](../../../../attribution.md)), and states the assistance in the
  source’s words.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the whole tree, 7 files: 4 retained under [source/](source/) and 3 pinned.

| File | Bytes |
| --- | --- |
| `n90.cert` | 11,975, the claim |
| `n90.csv` | 4,775, the squares rounded, angles in degrees |
| `README.md`, `SHA256SUMS` | 2,459 and 383, the author’s note and its digests |
| `DONOR-LICENSE.txt` | 1,072, Joost de Winter’s MIT licence, pinned against the identical `LICENSE` the de-winter-upper-bounds-227-229-260-2026-10-17 packet retains |
| `n90.png`, `n90-construction.png` | 120,546 and 124,983, pinned by digest: pictures that decide nothing |

The SHA-256 the issue states for the certificate (`88c93b2f…d466`) is the file’s, and
`SHA256SUMS` states the digests of five of the seven files, which hold; it predates the
construction figure.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `a4f36ae70` on 15
November 2026), through the `evand-cert` reader:

- **90:** exact side 4999138583463/500000000000 = 9.998277166926, below the case’s
  house, the 10 × 10 grid’s 10, by 861416537/500000000000 = 1.722833074 × 10⁻³, the
  0.001722833074 the issue states.
  It is the first packing of 90 squares below the grid on record.
  No register bound is pending adoption at 90.
- The lower bounds at 90 stay below it: the verified 973/100 = 9.73 (T-091) and the
  reported 489/50 = 9.78 (T-212, a report not yet replayed).
  No register entry claims s(90) = 10: the optimality families T-084 (k² − 1), T-086 (k²
  − 2), T-064 (k² − 3), T-081 (k² − 4) and T-298 (k² − 5) do not reach 90 = 10² − 10,
  and the local-minimum claims of T-124 and T-261 that list 90 are about their own
  source configurations and claim no global bound.
  The case’s conjectured optimum is the integer, 10, which this side is below.

## Report Order

The
[ledger of 15 November for this lane](../../../campaign/issue-intake/upper-bounds-989-20261115/README.md)
records this claim at 90 as a new packing, the only report at that count.

## Pose by Pose

`devtools.measure_identity` measured the certificate against the house witness, the
grid, and wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.
No symmetry of the box pairs the two one to one by nearest centres.
The optimal assignment moves every square beyond 10⁻³, 54 beyond 0.01 and 52 beyond 0.1
(largest 1.33219), and turns 48 squares by more than 10⁻⁶ radians.
Tilted beyond a degree: 44, at 22.61 to 31.56 degrees, all clockwise; five more are
within 0.07 degrees of upright, and 41 are exactly upright (t = 0). So it is a new
arrangement relative to the grid, as the issue says.
The 157 packing it starts from is at another count, which the measurement cannot pair.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 24,030 pair decisions, 2.77 seconds of job wall time
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
No square touches the box: the least wall clearance is 2.1000000001021 × 10⁻¹⁵ (square
28), the least far-wall clearance about 2.377 × 10⁻¹³, and every pair clears by at least
1.19448 × 10⁻¹², squares 79 and 81, the separation the issue states.
`check --replay` decided the three jobs again.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
10⁻³⁰ past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)), with the
expected verdicts stated in a plan hashed before any run of the certificate (SHA-256
`d23ca310bd13f3881abc69d0d946e14aa31fb982c68b04b56e28124fd06fd2f6`, 03:16:30Z on 15
November, recorded on the bead).
The side lowered by the least far-wall clearance, the least-gap pair closed (square 81
toward 79) and every square moved toward the nearer near wall by the least near-wall
clearance were each accepted at contact with margin 0 and refused 10⁻³⁰ past it.
Square 81 enlarged to its partner and square 28 enlarged to its wall were each refused
at contact for their shape alone, and 10⁻³⁰ past it for the overlap or the wall as well.
Both routes refused a duplicated square.
All 11 were as stated in advance.
The two routes are `sqpack`’s exact separating-axis verifier and the independent
rational corner checker; they share `Fraction` arithmetic and the reader, and neither is
the source’s code.

## The Gain Against Padding

`devtools.contraction_margin` contracted each packing uniformly about the origin to
first contact and boxed it, each contracted packing decided on both maintained routes:

- **The house**, the grid: margin 0, squares 1 and 2 touching
  ([measure/contraction-n090.json](measure/contraction-n090.json)), so the whole gain,
  1.7228 × 10⁻³, lies outside any padding.
  A packing below the grid is no re-certification of it, and RV-3 (think-ruu2) does not
  reach it.
- **This certificate**: margin 1.0988 × 10⁻¹¹ (1 − λ\* about 1.1945 × 10⁻¹², squares 79
  and 81) ([measure/contraction-n090-own.json](measure/contraction-n090-own.json));
  contracted, it would be a square about 1.1 × 10⁻¹¹ smaller.
  Nobody reported that side, and it is not registered (RV-3).

## The L Step

`devtools.l_step_scan`, with this side stood in for 90’s ceiling
([measure/l-step-scan.json](measure/l-step-scan.json)), finds the same L-step
improvements and monotonicity consequences as on `main`, and one fewer L extension: the
grid at 111, 11, was the L step from the grid at 90, and that step now lands at 109, at
10.998277166926, above 109’s ceiling, 10.9497…. Monotonicity carries nothing: s(89) ≤
9.9497… is already below this side.
So the bound carries to no other count.

## What Is Not Established

- **Optimality** of any kind.
- **The lineage** the source states, beyond what the measurement above shows; the crop
  and window from de Winter’s 157 were not rebuilt here.
- **Identity.** Whether the account `dpre4ai`, whose commits name “Daniel”, is jazivxt
  or posts for jazivxt is not established; the record credits the name the issue asks
  for.

## Credit and Licence

The packing is credited to jazivxt, as the issue and the source’s README ask, after
Joost de Winter, whose n = 157 packing (T-293) supplied the motif.
The issue names GPT-6 Astra Ultra as the AI collaborator on the search and verification.
The bibliography key is **[jazivxt s90 upper bound 2026-11-15]**. The repository states
no licence for its own data or prose; the account submitted it in the issue, so the
owner’s ruling of 24 October 2026 (think-cnn7) gives a presumption of permission to
retain and import it, and the certificate is factual data under the owner decision of 9
October 2026 as well.
`DONOR-LICENSE.txt` is Joost de Winter’s MIT notice for the donor packing.

## Commands

From `packing/`, with the project interpreter:

```bash
P=jazivxt-s90-upper-bound-2026-11-15
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 90 "JAZIVXT=packet:$P" \
  'grid=witness-corners:witnesses/known-best/n-090.yaml' \
  --out resources/web/$P/measure/identity.json
python -m devtools.contraction_margin --n 90 'grid=witness-corners:witnesses/known-best/n-090.yaml' \
  --against "jazivxt-989=packet:$P" --out resources/web/$P/measure/contraction-n090.json
python -m devtools.contraction_margin --n 90 "jazivxt-989=packet:$P" \
  --out resources/web/$P/measure/contraction-n090-own.json
python -m devtools.l_step_scan --with 90=4999138583463/500000000000 \
  --out resources/web/$P/measure/l-step-scan.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
