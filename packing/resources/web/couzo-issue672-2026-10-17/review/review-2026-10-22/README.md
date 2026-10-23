# Review Programs, 22 October 2026

These are the programs that the stage 4 mathematical review lane for Francisco Couzo’s
in-corpus certificates of issues #670, #672 and #675 (T-226, T-227 and T-228,
`think-0nse`) wrote and ran for
[`review-2026-10-22-couzo-670-672-675.md`](../../../../../../docs/project/reviews/review-2026-10-22-couzo-670-672-675.md),
with what they printed. The lane was an AI agent of the Claude system family (Anthropic), strong
sub-agent tier (`c-review-t226-t228-math`), prompted separately from the import lanes
that built the three packets and from pull request #718’s reviewers.
It ran them on 22 October 2026 against `main` at
`0281e776342f2f1b63d3df66dc3c1737e8202945` (which holds #718’s merge `7359fa8b6`) with
CPython 3.14.7, under `nice -n 10` on a shared host, at most two processes.

The stage 4 lane (`c-lane-stage4-1022`, the pull request after #722) moved them here from
the review lane’s scratch directory, as the review’s RF-7 asks: the programs and every
output byte for byte. This is the packet that already keeps the shared identity
measurement, and the [#670](../../../couzo-issue670-2026-10-17/README.md) and
[#675](../../../couzo-issue675-2026-10-18/README.md) packets’ READMEs point here.
`outputs/program-digests.sha256` is each program’s SHA-256 as it ran, which the files here
equal.
The lane’s `data/` directory (`git show` of `main`’s case records at 204 to 324, and of
`804eff369`’s at 204, 227 and 229) and `fetched/` directory (the source’s
`certificates/best/manifest.json` at the three pins, each equal to the digest its packet
pins) are left out: the repository and the packets keep or pin all of them.

## What Decides What

`review_0nse_check.py` is this review’s own exact checker, written before its author
read any of this repository’s maintained routes or any of the source’s code, standard
library only, importing nothing from the repository, with its own reader.
It decides each certificate twice, on routes that share only the reader:

- route Z uses integers only (no `fractions`): a Pythagorean triple per row, containment
  by the half-extent, and every one of the $n(n-1)/2$ pairs by the four separating-axis
  inequalities with denominators cleared, giving each pair’s exact gap;
- route C uses `Fraction`: corners from
  $(\cos, \sin) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$, unit edges, right angles,
  orientation and corner mean checked on them, every corner in the box, and every pair
  decided, with no distance filter, by the exact area that one square’s four closed
  half-planes clip from the other.

It decides; it shares `Fraction` (route C) and CPython integers with the maintained
routes, the separating-axis method (route Z) with both of them, and no code with them,
with the T-225 review’s checker or with the source.
It is registered as `V-couzo-670-672-675-review-check` in [verifiers.yaml](../../../../../frontier/verifiers.yaml), and its
runs are the evidence entries `E-couzo-670-review-exact-feasibility`,
`E-couzo-672-review-exact-feasibility` and `E-couzo-675-review-exact-feasibility`.

`sharp_controls_0nse.py` builds eight mutants of each certificate at exact contact and
$10^{-30}$ past it, and decides each with this review’s checker and with the two
maintained routes, called as the packets’ replay calls them through the `evand-cert`
adapter; it also runs the kernel’s `run_sharp`. The maintained routes’ verdicts are
theirs; the program adds the mutants and the expectations.
A premise check: it decides no certificate. It is registered as
`V-couzo-670-672-675-review-controls`.

`agree_0nse.py` holds the checker’s results to the packets’ receipts.
`margins_0nse.py` computes each side’s exact margins in report order and against `main`.
`identity_0nse.py` measures poses under the box’s eight symmetries with its own
Hungarian algorithm.
`manifest_extract_0nse.py` extracts what the source’s manifests say.
`selftest_0nse.py` runs the checker on fifteen hand-built cases.
None of these five decides anything.

## How to Run

From this directory, with any CPython 3.12 or later for the `-I` programs and the
project interpreter for the controls, `REPO` being the repository root:

```sh
W=$REPO/packing/resources/web
C670=$W/couzo-issue670-2026-10-17; C672=$W/couzo-issue672-2026-10-17; C675=$W/couzo-issue675-2026-10-18
python -I programs/selftest_0nse.py
python -I programs/review_0nse_check.py outputs/out-check-204.json \
  T-226@204=$C670/source/certificates/n204.cert \
  T-228@204=$C675/source/certificates/best/n204.cert
python -I programs/review_0nse_check.py outputs/out-check-227-229.json \
  T-227@227=$C672/source/certificates/n227.cert \
  T-227@229=$C672/source/certificates/n229.cert
python -I programs/agree_0nse.py outputs/out-agree.json \
  outputs/out-check-204.json,outputs/out-check-227-229.json \
  T-226@204=204=$C670/source/certificates/n204.cert=$C670/receipts/exact-certification.json.xz \
  T-228@204=204=$C675/source/certificates/best/n204.cert=$C675/receipts/exact-certification.json.xz \
  T-227@227=227=$C672/source/certificates/n227.cert=$C672/receipts/exact-certification.json.xz \
  T-227@229=229=$C672/source/certificates/n229.cert=$C672/receipts/exact-certification.json.xz
python -I programs/margins_0nse.py $REPO data outputs/out-margins.json
python -I programs/identity_0nse.py $REPO outputs/out-identity.json
python -I programs/manifest_extract_0nse.py $REPO fetched outputs/out-manifests.json
# from $REPO/packing with the project interpreter, PYTHONDONTWRITEBYTECODE=1,
# R being this directory and W=resources/web:
python $R/programs/sharp_controls_0nse.py $R/outputs \
  T-226@204=204=$W/couzo-issue670-2026-10-17/source/certificates/n204.cert \
  T-228@204=204=$W/couzo-issue675-2026-10-18/source/certificates/best/n204.cert
python $R/programs/sharp_controls_0nse.py $R/outputs \
  T-227@227=227=$W/couzo-issue672-2026-10-17/source/certificates/n227.cert \
  T-227@229=229=$W/couzo-issue672-2026-10-17/source/certificates/n229.cert
```

| Program | What it printed | Kept output |
| --- | --- | --- |
| `selftest_0nse.py` | 15 of 15 as expected | `selftest.log` |
| `review_0nse_check.py` | 4 of 4 accepted on both routes, the routes agreeing on least clearance, touching and overlap counts; 20,706, 25,651, 26,106 and 20,706 pairs on each route; route Z 0.065 to 0.085 s, route C 1.8 to 2.5 s a certificate | `out-check-*.json`, `check-*.log`, `time-check-*.log` |
| `agree_0nse.py` | every pose, side, pair count, least clearance and least gap equal to both receipts’ routes; every receipt control refused by both | `out-agree.json`, `agree.log` |
| `sharp_controls_0nse.py` | at every certificate, F0, N0 and P0 accepted at exactly 0 and F1, N1 and P1 refused at exactly $-10^{-30}$ by both of this review’s routes and both maintained routes; R1 refused by both readers; R2 refused by this review’s reader; the kernel’s `run_sharp` as expected | `out-controls-*.json`, `controls-*.log`, `time-controls-*.log` |
| `margins_0nse.py` | each side as the entries claim: below every earlier member of its chain, above every later one, below every bound at every later count through 324 | `out-margins.json`, `margins.log` |
| `identity_0nse.py` | the review’s identity table | `out-identity.json`, `identity.log`, `time-identity.log` |
| `manifest_extract_0nse.py` | each manifest equal to its pinned digest; the first checker, credits, provenance and strict verdicts the review cites | `out-manifests.json`, `manifests.log` |

`acquire-check-*.log`, `check-claims-*.json` and `check-replay-*.log` are this lane’s
runs of each packet’s `acquire_source --check`, `check-claims` and `check --replay`;
`pytest-670-672-675.log` is the entries’ test module.
`upstream-blobs.txt` is each certificate’s Git blob at its pin through the GitHub API,
and `local-blobs.txt` the packet copies’ blobs and digests: all equal.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
