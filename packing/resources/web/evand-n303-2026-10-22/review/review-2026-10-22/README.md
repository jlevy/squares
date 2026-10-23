# Review Programs, 22 October 2026

These are the programs that the stage 4 mathematical review lane for Evan Daniel’s
certificate at 303 from issue #728 wrote and ran for `review-2026-10-22-daniel-728.md`
in `docs/project/reviews/`, with what they printed.
The lane was an AI reviewer of the Claude system family (Anthropic), strong sub-agent
tier (`tbd-strong-max`), at maximum reasoning, lane `c-review-728-math`, prompted
separately from the triage and import lanes of #728. It ran them on 22 October 2026 with
CPython 3.14.7, under `nice -n 10` on a shared host, at most two processes.
Every run that reads the repository read `main` at `cacdafc1f`. The lane’s brief named
`78dc902c1`; every file those runs read at 303 to 324, and every deciding program, is
byte-identical at the two revisions.
`outputs/program-digests.sha256` holds each program’s SHA-256 as it ran.

Not kept here: the certificate, which the packet retains; the source’s f64 input
`s303_r303w0.input.txt`, its report `s303_r303w0.json` and its checkers `verify_cert.py`
and `verify_cert2.py`, whose digests and Git blobs at `f06521f` are in
`outputs/custody.txt` (the checkers equal the versions registered as
`V-evand-verify-cert-py` and `V-evand-verify-cert2-py`); and the eight mutants, which
`sharp_controls_728.py` rebuilds and whose SHA-256 are in `outputs/sharp-controls.json`.

## What Decides What

`review_728_check.py` is the review’s own exact checker.
It was written before its author read any of this repository’s maintained routes or any
of the source’s code; it uses the standard library only, imports nothing from the
repository, and has its own reader.
It decides the certificate twice, on routes that share only the reader:

- route Z uses integers only and never loads `fractions`: a Pythagorean triple per row,
  containment by the half-extent, and every one of the $n(n-1)/2$ pairs by the four
  separating-axis inequalities with denominators cleared, giving each pair’s exact gap;
- route C uses `Fraction`: corners from
  $(\cos, \sin) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$, with unit edges, right angles,
  orientation and corner mean checked on them, every corner in the box, and every pair
  decided, with no distance filter, by the exact area that one square’s four closed
  half-planes clip from the other.
  It also computes the exact squared distance of every pair whose centres lie within 2.

It decides. It shares `Fraction` (route C) and CPython integers with the maintained
routes, and the separating-axis method (route Z) with `sqpack`; it shares no code with
them or with the source.
`--self-test` runs it on 13 hand-built feasible, touching and overlapping cases, 13
malformed inputs and 3,000 random pairs.
`run_checker.sh` runs its two routes as two processes.

`maintained_routes_728.py` runs this repository’s two maintained exact routes on a
certificate the way `devtools.upper_bound_reports certify` runs them for an evand
certificate: through the `evand-cert` adapter and the kernel’s `run_case` and
`validate_job`. With `--sharp` it also runs the kernel’s `run_sharp`. The verdicts are
the maintained routes’; the driver adds nothing.
`run_maintained.sh` runs it on the positive and on the kernel’s two controls.

`sharp_controls_728.py` builds eight mutants of the certificate, at exact contact and
$10^{-30}$ past it (a shrunk box, every square moved to a wall, one square of the
least-gap pair moved onto the other) and two reader mutants.
It decides each with both routes of `review_728_check.py` and, through
`maintained_routes_728.py`, with both maintained routes.
A premise check: it decides no certificate.

`agree_728.py` holds the checker’s results to the maintained routes’ and to the source’s
report. `margins_728.py` checks the side and the issue’s prints and computes the exact
margins against the record at 303 and every later count to 324. `identity_728.py`
measures poses against the house and T-146 under the box’s eight symmetries with its own
Hungarian algorithm and bottleneck matching; its `--self-test` checks both against brute
force. These three decide nothing.
`margins_728.py` and `identity_728.py` read the record with PyYAML, and
`identity_728.py` uses numpy, both from the project environment.

## How to Run

From this directory, with the project interpreter as `PY`, the repository root as
`REPO`, the packet’s retained certificate as `CERT`, the source’s f64 input and report
as `INPUT` and `REPORT`, and a scratch directory as `SCRATCH`, all as absolute paths
(`run_maintained.sh` and the controls run the maintained routes from `packing/`):

```sh
$PY -I programs/review_728_check.py --self-test
programs/run_checker.sh $CERT outputs $PY
programs/run_maintained.sh $CERT $PWD/outputs $REPO/packing $PY
$PY -I programs/sharp_controls_728.py $CERT --mutants SCRATCH/mutants \
  --out outputs/sharp-controls.json --packing $REPO/packing --python $PY
$PY -I programs/agree_728.py $CERT outputs $REPORT --out outputs/agree.json
$PY -I programs/margins_728.py $CERT --repo $REPO --input $INPUT --out outputs/margins.json
$PY -I programs/identity_728.py --self-test
$PY -I programs/identity_728.py $CERT --house $REPO/packing/witnesses/known-best/n-303.yaml \
  --contrast "T-146=$REPO/packing/resources/web/evand-regularized-2026-10-10/source/search/regularize/lists/certs/n-303.cert.gz" \
  --out outputs/identity.json
```

`margins_728.py` also reads the intake sweep’s Kingbird captures under the untracked
`attic/intake/` where a checkout has them, and the retained capture otherwise.

| Program | What it printed | Kept output |
| --- | --- | --- |
| `review_728_check.py --self-test` | the 13 hand-built cases as expected on both routes, the 13 malformed inputs refused, and 3,000 random pairs (1,453 apart, 628 touching, 919 overlapping) decided alike by both routes | `self-test.txt` |
| `review_728_check.py`, both routes | accepted; 45,753 pairs on each route; least wall clearance `60480000000010479/10^29` (square 0, left wall); least gap $1.2045000000002 \times 10^{-12}$ (squares 284 and 296); no contact; the side equal to the claim; route Z 0.34 CPU s, route C 4.81 CPU s | `route-Z.json`, `route-C.json`, `route-*.summary.json`, `route-*.time` |
| `maintained_routes_728.py` | positive accepted by both maintained routes with the same least clearance and gap, `validate_job` passed; both kernel controls refused by both; `run_sharp` accepted at contact and refused at exactly $-10^{-30}$ | `maintained-*.json`, `maintained-*.txt` |
| `sharp_controls_728.py` | F0, N0 and P0 accepted at exactly 0, and F1, N1 and P1 refused at exactly $-10^{-30}$, by both of the review’s routes and both maintained routes; R1 refused by both readers; R2 refused by the review’s reader and read exactly by the maintained one | `sharp-controls.json`, `sharp-controls.txt` |
| `agree_728.py` | 13 of 13 checks equal, including the same side and poses read by both readers | `agree.json`, `agree.txt` |
| `margins_728.py` | the side equal to the claim and its prints right; $1.860737955802 \times 10^{-4}$ below the house (T-186); below all 23 retained earlier reports at 303 and all 42 bounds from 304 to 324 | `margins.json`, `margins.txt` |
| `identity_728.py` | no symmetry pairs nearest centres one to one with the house; 64 squares beyond a tenth, 24 tilts reversed; the self-test 0 mismatches in 300 | `identity.json`, `identity.txt`, `identity-self-test.txt` |

For F1, N1 and P1, `sharp-controls.json` records the kernel’s `validate_job` refusing
the row, because a `positive` row must pass.
The routes’ verdicts are the decision.

`custody.txt` records the pin, the commit’s author and times, the issue’s opening time,
and the SHA-256 and Git blob of each source file the lane read.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
