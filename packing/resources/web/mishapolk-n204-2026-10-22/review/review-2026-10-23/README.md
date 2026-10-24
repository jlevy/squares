# Review Programs, 23 October 2026

These are the programs that the stage 4 mathematical review lane for Mykhailo
Polkovskyi’s `certificates/n204.cert` at `Mishapolk/square-packing-records@12fc4667`
(the entry the records branch registers as T-231) wrote and ran for
[`review-2026-10-23-mishapolk-n204.md`](../../../../../../docs/project/reviews/review-2026-10-23-mishapolk-n204.md),
with what they printed.
The lane was an AI agent of the Claude system family (Anthropic), strong sub-agent tier
(`tbd-strong-max`), at maximum reasoning, as lane `c-review-t231-math` for the intake
coordinator `coord-intake-1023`. It was prompted separately from the records lane
(`c-lane-719-records-1023`) and read none of that lane’s notes.
It ran them on 23 October 2026 from 05:17Z to 06:15Z against `main` at `31584003e`,
under `nice -n 10` on a four-core host shared with five other lanes, one process at a
time.

## What Decides What, and What Is Registered

`programs/review_t231_check.py` is this review’s own exact checker.
It was written for this review from the format line the certificate carries and the
mathematics.
Standard library only, it imports nothing from the repository or the source,
and has its own reader.
It decides the certificate twice, on two routes that share only the reader:

- **Route Z** uses integers only and never loads `fractions`; its receipt says so.
  It decides containment by each centre’s clearance of each wall by the half-extent
  $(|a| + |b|)/(2d)$, and every one of the 20,706 pairs by the four separating-axis
  inequalities along the two squares’ edge normals, with every denominator cleared.
- **Route C** uses `Fraction`. It builds each square’s four corners and checks unit
  edges, right angles, positive orientation and the corner mean, then decides
  containment from the corners.
  It decides every pair by the exact area that one square’s four closed half-planes clip
  from the other, and again by corner projections on the four normals.
  It also computes the exact squared Euclidean distance of every pair whose centres lie
  within 2.

Its last change was at 05:17:09Z (SHA-256 `2c8053b1…`). It decided the certificate at
05:17:19Z (route Z) and 05:17:33Z (route C), before this lane opened any file under
`packing/devtools/` or `packing/src/sqpack/`, or any of the source’s code.
It has not changed since.
It is proposed as `V-mishapolk-n204-review-check` (decides).

`programs/sharp_controls_t231.py` builds sixteen mutants of the certificate and decides
each with this review’s two routes and with the two maintained routes.
Ten are sharp: exact contact and $10^{-30}$ past it, at the top and right walls, the
left wall, the bottom wall, and three pairs: two squares tilted alike, a tilted with an
aligned square, and two aligned squares.
Four are gross or reader controls: a duplicated square, a square moved outside, a
dropped row, and a decimal literal (a reader difference).
`programs/maintained_routes_t231.py` runs the maintained routes as
`devtools.upper_bound_reports certify`’s child reaches them.
It reads the file through the `evand-cert` adapter into
`devtools.evand_arrangement_reports.run_case`, then applies `validate_job` and the
kernel’s own `run_sharp`, one job per process.
Both are premise checks: their verdicts are the routes’, and they decide no certificate.
They are proposed together as `V-mishapolk-n204-review-controls`.

Four programs decide nothing and are kept unregistered:

- `programs/agree_t231.py` holds this review’s numbers to the maintained routes’ at
  every number they share, and to the records lane’s receipt.
  It also holds the T-229 reference to the T-229 packet’s derived fact, pose by pose.
- `programs/margins_t231.py` computes the side’s prints and its exact margins against
  every report at 204 the record holds and every bound at 205 to 224. It also checks the
  side against Evan Daniel’s exact solver’s side for T-229’s witness, as the project’s
  run reported it.
- `programs/identity_t231.py` measures the packing against T-229, T-225, T-223, T-226,
  T-228 and T-186 under the box’s eight symmetries: by nearest centre, by an optimal
  assignment (its own Hungarian algorithm) with exact displacement thresholds, and by
  the bottleneck (its own Hopcroft–Karp bisection).
- `programs/lineage_t231.py` compares the certificate, row by row, with the outputs of a
  rerun of Evan Daniel’s regularizer driver on T-229’s witness.

## How to Run

From `packing/` of a checkout at `31584003e`, with the project interpreter
(`.venv/bin/python3`, CPython 3.14.7), and `$P` this directory:

```bash
CERT=resources/web/mishapolk-n204-2026-10-22/source/certificates/n204.cert
python3 -I $P/programs/review_t231_check.py --self-test --out $P/outputs/selftest.json
python3 -I $P/programs/review_t231_check.py --route Z $CERT --out $P/outputs/check-z.json
python3 -I $P/programs/review_t231_check.py --route C $CERT --out $P/outputs/check-c.json
for job in positive duplicate-square-overlap square-translated-outside-container; do
  python3 -I $P/programs/maintained_routes_t231.py --packing . $CERT --job $job \
    --out $P/outputs/maintained-$job.json
done
python3 -I $P/programs/maintained_routes_t231.py --packing . $CERT --sharp --out $P/outputs/maintained-sharp.json
python3 -I $P/programs/sharp_controls_t231.py --packing . $CERT --out $P/outputs/sharp-controls.json
```

The other four read two files that the repository does not retain.
They are `certificates/n-204.cert` at the pin (T-229, blob `17e243a`, SHA-256
`7c77ad00…a4f3`), which the T-229 packet keeps only as its derived fact, and
`certificates/n204.cert` at `70a033f` (T-186, blob `301c930`, SHA-256 `f0885fa8…5b40`).
This lane read both from a blobless clone of the source.
`agree_t231.py` holds the first to the T-229 fact pose for pose.

```bash
python3 -I $P/programs/identity_t231.py --self-test --out $P/outputs/identity-selftest.json
python3 -I $P/programs/identity_t231.py --test $CERT --ref T-229=N-204.CERT \
  --ref T-225=resources/web/evand-regularized-2026-10-20/source/search/regularize/lists/certs/n-204.cert.gz \
  --ref T-223=resources/web/couzo-issue678-2026-10-18/source/certificates/best/n204.cert \
  --ref T-226=resources/web/couzo-issue670-2026-10-17/source/certificates/n204.cert \
  --ref T-228=resources/web/couzo-issue675-2026-10-18/source/certificates/best/n204.cert \
  --ref T-186=N204-70A033F.CERT --out $P/outputs/identity.json
python3 -I $P/programs/identity_t231.py --test $CERT --undilate --ref T-229=N-204.CERT \
  --out $P/outputs/identity-undilated.json
python3 -I $P/programs/margins_t231.py --packing . --cert $CERT --t229 N-204.CERT \
  --t186 N204-70A033F.CERT \
  --run-report cases/regularized_drawings/think-4h23-2026-10-23/adopt-2026-10-23-n105-204-evand/n-204/report.json.gz \
  --run-report $P/outputs/regularizer-rerun/report.json.gz --out $P/outputs/margins.json
python3 -I $P/programs/lineage_t231.py --cert $CERT --t229 N-204.CERT \
  --solve-dir $P/outputs/regularizer-rerun/solve --regularized $P/outputs/regularizer-rerun/regularize.cert \
  --identity $P/outputs/identity.json --ref T-225=… --ref T-223=… --ref T-228=… --ref T-226=… \
  --out $P/outputs/lineage.json
python3 -I $P/programs/agree_t231.py --outputs $P/outputs --cert $CERT --t229 N-204.CERT \
  --t229-fact resources/web/mishapolk-issue719-2026-10-22/facts/n-204.yaml.gz \
  --records-receipt resources/web/mishapolk-n204-2026-10-22/receipts/exact-certification.json.xz
```

The rerun of the regularizer driver was the project’s own command, from `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.regularize_evand run \
  --run-dir $SCRATCH/t231-regrun --n 204 --workers 1
```

It read `witnesses/known-best/n-204.yaml` (T-229, SHA-256 `2533ca0a…6261`) and took
112.7 s of wall.
`outputs/regularizer-rerun/` keeps its receipt, its report, its upstream
input (`input.txt`, SHA-256 `4fa2b348…344e`, the digest the 22 October run records), the
solve’s certificate and its two JSON records, and the regularized certificate.
It does not keep the views, whose Git blobs the report records (`5ee06383…` solved,
`1937dcf6…` same), equal to the 22 October run’s. The run is the project’s generator.
It decides nothing for this review and is cited as a measurement.

The programs lie under `packing/resources/`, outside the Ruff and BasedPyright floor.
They were checked with Ruff’s error rules (pyflakes, pycodestyle errors and warnings,
bugbear and pylint errors) and nothing beyond style was found.
They were left unchanged so that the digests in `outputs/program-digests.sha256` stay
the ones that ran.

## What They Printed

| Program | Printed | CPU |
| --- | --- | ---: |
| `review_t231_check.py --self-test` | 13 hand-built cases as expected on both routes, with equal per-pair gap and wall digests; 12 malformed texts refused by the reader; 1,500 random pairs decided alike, 500 of them built to touch, half of those then pushed $10^{-30}$ into overlap | 1.1 s |
| `--route Z` | accepted; 20,706 pairs; no pair touches and no square touches a wall; least gap $\approx 1.0 \times 10^{-20}$ at (63, 84); least clearances $5 \times 10^{-21}$ at the left and bottom walls and $5.000000000688 \times 10^{-21}$ at the right and top | 0.25 s |
| `--route C` | accepted; every clipped area 0 and every clipped polygon empty; the same per-pair gap digest and wall digest as route Z; 763 pairs with centres within 2, least Euclidean distance $\approx 1.0 \times 10^{-20}$ at (63, 84) | 6.8 s |
| the same, again (`outputs/second-run/`) | identical receipts apart from timing |  |
| `maintained_routes_t231.py`, three jobs | positive accepted by `exact_verify` and `independent`, `validate_job` passed; both gross controls refused by both | 16.4 s |
| `maintained_routes_t231.py --sharp` | at contact accepted with margin exactly 0, and $10^{-30}$ past it refused at exactly $-10^{-30}$, at the wall and at the pair, on both routes | 22.3 s |
| `sharp_controls_t231.py` | all sixteen mutants as expected on all four deciders (`outputs/sharp-controls.json`) | 181 s |
| `identity_t231.py` | against T-229, one to one under the identity, every square within $2.02 \times 10^{-11}$; the other references as the review tabulates; the self-test’s 300 instances match brute force | 2.7 s |
| `margins_t231.py` | the side, its ceilings at 12, 16, 18 and 30 places, below every report at 204 and every bound at 205 to 224; the solver’s `S_cert` equal to the header in both reports | 1 s |
| `lineage_t231.py` | 119 rows byte-identical to the solve’s certificate; the 85 others are the solve’s 21 free squares and the 64 squares of its frozen variables; each free square’s clearance in the certificate, in T-229 and in the solve’s certificate; the near-axis tilts and large turns of the 204 family | 0.4 s |
| `agree_t231.py` | 63 of 63 checks equal | 0.5 s |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
