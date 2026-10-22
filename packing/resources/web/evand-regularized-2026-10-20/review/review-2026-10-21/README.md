# Review Programs, 21 October 2026

These are the programs that the stage 4 mathematical review lane for Evan Daniel’s
regularized views at 204, 227, 229 and 260 (T-225, `think-ql4v`) wrote and ran for
[`review-2026-10-21-evand-regularized-views.md`](../../../../../../docs/project/reviews/review-2026-10-21-evand-regularized-views.md),
with what they printed.
The lane was an AI agent of the Claude system family (Anthropic), strong sub-agent tier,
reasoning setting xhigh (`c-review-t225-math`), prompted separately from the import lane
that built the packet and the replay, and from pull request #716’s senior reviewer.
It ran them on 21 October 2026 against #716’s head `be6416a03` and `main` at
`bb0c24e9f`, under `nice -n 10` on a shared four-core host, at most two processes.

The stage 4 lane (`c-lane-t225-stage4`, the pull request after #716) moved them here from
the review lane’s scratch directory, as the review’s RF-6 asks: the programs and every
output byte for byte, including the controls program’s first run in
`outputs/first-controls-run/`. `outputs/program-digests.sha256` is the review lane’s
SHA-256 of each program as it ran, which the files here equal.
The lane’s `data/` directory is left out: it held copies of this packet, of the
packet’s receipt decompressed, of `main`’s case records at 204 to 324, and of the
certificates named below, all of which the repository keeps, and one fetched file,
#672’s `certificates/n227.cert` at `franciscouzo/square-packing@af8cb79` (SHA-256
`65b03df883e75f890eca985232252a6340b9b5da3437c41275c9201df03d8c17`), which #672’s
import now retains in
[`couzo-issue672-2026-10-17`](../../../couzo-issue672-2026-10-17/README.md) (T-227).

## What Decides What, and What Is Registered

`review_t225_check.py` is this review’s own exact checker: written for it from the format
line each certificate carries and the mathematics, before its author read this
repository’s two maintained routes or any of the source’s code, standard library only,
importing nothing from the repository, with its own reader.
It decides each certificate twice, on two routes that share only the reader: route I
uses integers only (no `fractions`), deciding containment and every one of the
$n(n-1)/2$ pairs by separating-axis inequalities cleared of denominators; route F uses
`Fraction`, deciding containment from the corners, every pair by projecting corners on
the four unit edge normals, and every pair whose bounding boxes overlap again by the
exact area one square’s closed half-planes clip from the other.
It decides; it shares `Fraction` (route F) and CPython integers with the maintained
routes, and no code with them or with the source.
It is registered as `V-evand-regularized-1020-review-check` in
[`verifiers.yaml`](../../../../../frontier/verifiers.yaml), and its run is the evidence
entry `E-evand-regularized-1020-review-exact-feasibility`.

`sharp_controls_t225.py` builds eight mutants per count at the scale of the margins
($10^{-30}$ past exact contact, and exact contact) and decides each with this review’s
checker and with the two maintained routes, reached through the packet’s own
`evand-cert` adapter.
It also runs the kernel’s `run_sharp` on each certificate.
The maintained routes’ verdicts are theirs; it adds the mutants and the expectations.
It is registered as `V-evand-regularized-1020-review-controls`, a premise check: it
decides no certificate, and its receipts are what the confirming entries’ limitations
cite for the sharp controls (RF-3).
`tests/test_upper_bound_reports_regularized_1020.py` runs the kernel’s two sharp controls
on all four certificates at contact and $10^{-30}$ past it on both maintained routes.

`agree_t225.py` holds the checker’s results to the import lane’s receipt: each pose of
the receipt’s `checker_input` against the row this review’s reader read, the side, the
least wall clearance, the least pair gap and the pair count across all four
computations. It compares and decides nothing.

`margins_t225.py` computes each side’s exact margins against the houses on `main` and
against every verified and reported upper bound at every later count through 324. It
decides no geometry.

`identity_t225.py` measures each view against the packing its credit names, under the
box’s eight symmetries, by nearest centre and by an optimal assignment (its own
Hungarian algorithm), with exact displacement thresholds.
A measurement for credit; it decides nothing.

`selftest_t225.py` runs the checker on eight hand-built cases with known answers and
four malformed texts.
`diag_pair_t225.py` shows which pairs a closing move of the least-gap pair also closes;
it decides nothing.
None of these four is registered: each is kept, and decides nothing.

## How to Run

The programs read a data directory: `packet/` (a copy of
`packing/resources/web/evand-regularized-2026-10-20/`), `receipt.json` (the packet’s
receipt, decompressed), `compare/` (copies of `n204.cert` and `n260.cert` of
`couzo-issue678-2026-10-18`, `s229_v2.cert` of `evand-n229-dilation-update-2026-10-18`,
and `n227_exact.json.gz` and `n260_exact.json.gz` of
`de-winter-upper-bounds-227-229-260-2026-10-17`), `fetched-672/n227.cert`
(`franciscouzo/square-packing@af8cb79`, `certificates/n227.cert`, Git blob `8172d92`,
SHA-256 `65b03df8…3d8c17`, checked by the program), and `main-cases/` (`git show` of
`main`’s `packing/frontier/n-204.md` to `n-324.md`, with `MAIN_COMMIT` holding
`bb0c24e9f5125546316be2860bce295149ac299c`).

```sh
P=programs; D=data; CERTS=$D/packet/source/search/regularize/lists/certs
python -I $P/selftest_t225.py
python -I $P/review_t225_check.py $CERTS outputs/out-check-a.json 204 227
python -I $P/review_t225_check.py $CERTS outputs/out-check-b.json 229 260
python -I $P/agree_t225.py $CERTS $D/receipt.json outputs/out-agree.json outputs/out-check-a.json outputs/out-check-b.json
python -I $P/margins_t225.py $D outputs/out-margins.json
python -I $P/identity_t225.py $D outputs/out-identity.json
# with the worktree's interpreter, PYTHONPATH=<packing>/src:<packing>, PYTHONDONTWRITEBYTECODE=1:
python $P/sharp_controls_t225.py $CERTS outputs 204 260
python $P/sharp_controls_t225.py $CERTS outputs 227 229
```

| Program | What it printed | Kept output |
| --- | --- | --- |
| `selftest_t225.py` | 12 of 12 as expected: contact accepted, $10^{-30}$ overlap and wall crossings refused at exactly $-10^{-30}$, malformed literals refused | `outputs/selftest.log` |
| `review_t225_check.py` | 4 of 4 passed on both routes: every wall cleared by at least exactly $1/(2 \cdot 10^{20})$; 20,706, 25,651, 26,106 and 33,670 pairs decided, none overlapping or touching, least gaps $\approx 9.99999999999999 \times 10^{-21}$; 178, 149, 170 and 171 bounding-box-overlapping pairs clipped to area exactly 0; the two routes equal to every digit; route I 0.07 to 0.09 s, route F 3.6 to 4.8 s per count | `outputs/out-check-a.json`, `outputs/out-check-b.json`, `check-a.log`, `check-b.log`, `time-a.log`, `time-b.log` |
| `agree_t225.py` | every pose, side, least clearance, least gap and pair count equal across this review’s two routes and the receipt’s two | `outputs/out-agree.json`, `agree.log` |
| `sharp_controls_t225.py` | at every count, F0, N0 and P0 (exact contact) accepted and F1, N1 and P1 ($10^{-30}$ past) refused, by both of this review’s routes and both maintained routes, each at a margin of exactly $0$ or $-10^{-30}$; R1 (a row dropped) refused by both readers; R2 (a decimal literal) refused by this review’s reader and read exactly by the maintained one; the kernel’s `run_sharp` likewise at contact and past it | `outputs/out-controls-nNNN.json`, `controls-a.log`, `controls-b.log`, `time-controls-a.log`, `time-controls-b.log` |
| `margins_t225.py` | each side equal to its claim and to `S_cert`, and to `S_exact` × (1 + 10^-20) rounded up at 30 places; below its house on `main` by 1.389753e-9, 1.710513e-4, 1.912210e-11 and 2.514377e-11; below every verified and reported upper bound at every later count through 324, the least margin at n + 1 | `outputs/out-margins.json`, `margins.log` |
| `identity_t225.py` | the counts in the review’s identity table, equal to the packet’s `identity.json` | `outputs/out-identity.json`, `identity.log`, `time-identity.log` |
| `diag_pair_t225.py` | at 204, 229 and 260 either move of the least-gap pair closes a second pair at the same exact gap | `outputs/diag-pair.log` |

`outputs/out-check-672-n227.json` is the checker’s run on #672’s fetched certificate
(feasible at its own side on both routes). It decides nothing for this record: T-227,
which registers #672 since this review, rests on its own replay, and its review is
think-0nse’s. `outputs/check-replay.log`, `check-claims.log` and
`acquire-check.log` are this lane’s runs of the packet’s own `check --replay` (all 12
jobs equal to the receipt, 62 s), `check-claims` (equal to the retained `claims.json`)
and `acquire_source --check`. `outputs/upstream-blobs.txt` is the Git blob of each of
the eight retained gzip files at the pin `0075967` and at `88385ab`, read through the
GitHub API, and `outputs/local-blobs.txt` the same files’ blobs as the packet holds them:
all equal. `outputs/first-controls-run/` is the controls program’s first run, before two
corrections: R2 was then expected to be refused by both readers, and no pair mutant was
built where the closing move also closes a second pair; its other outcomes are the same.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
