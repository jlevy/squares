# Review Programs, 22 October 2026

These are the programs that the stage 4 mathematical review lane for issue #719’s two
in-corpus certificates (T-229, `think-4h23`) wrote and ran for
[`review-2026-10-22-mishapolk-719.md`](../../../../../../docs/project/reviews/review-2026-10-22-mishapolk-719.md),
with what they printed.
The lane was an AI agent of the Claude system family (Anthropic), strong sub-agent tier
(`tbd-strong-max`), at maximum reasoning, as `c-review-t229-math`. It was prompted
separately from the import lane that built [the packet](../../README.md) and from the
records pull request’s reviewers.
It ran them on 22 October 2026 between 12:20Z and 13:00Z. They ran against the records
branch `claude/intake-2026-10-22` at `56d6d0d6ddbb79d7108b53a5d2798412860ca697` and
`main` at `76496462b0704486dc5099f866ef291c486f7840`, with CPython 3.14.7 (the self-test
also under 3.13), under `nice -n 10` on a shared host, at most two processes.
All of it took about 6 CPU minutes.

The stage 4 lane (`c-lane-stage4-1022`, the pull request after #722) moved them here, in
the #719 packet’s `review/review-2026-10-22/`, from the review lane’s scratch directory,
as the review’s RF-8 asks: the programs and every output byte for byte.
`outputs/program-digests.sha256` is each program’s SHA-256 as it last ran, which the files
here equal.
`review_t229_check.py` ran as `b470c70b…` throughout: it was written, self-tested and
run on both certificates before its author read any maintained route or any of the
source’s code, and it was not changed afterwards.

The lane’s `data/` directory is left out, and nothing in it is needed to read the
outputs. It held:

- `git show` of `main`’s case records at 105 to 324 and its house witnesses at 105 and
  204, which the repository keeps;
- Couzo’s `4e4c8ce` and `5a299b4` certificates at 105 and 204, pinned by those commits
  in his history;
- a 105 certificate with square 2 replaced by square 1, used to show what
  `sqpack/verify.py` does when run as a script.
  It is a copy of the source’s bytes, which this packet’s derived-only custody does not
  retain.

The outputs hold no upstream byte: paths, digests, verdicts and numbers only.

## What Decides What

`review_t229_check.py` is this review’s own exact checker.
It uses the standard library only and imports nothing from the repository.
Its own readers take the source’s certificate text (`n S`, then `x y t` rows) and the
packet’s Witness/v2 `center-basis` fact, with a strict line reader for exactly that
layout. It decides each input twice, on routes that share only the reader:

- route Z uses integers only (no `fractions`): a Pythagorean triple per row, containment
  by the half-extent, and every one of the $n(n-1)/2$ pairs by the four separating-axis
  inequalities with denominators cleared, giving each pair’s exact gap;
- route C uses `Fraction`. It builds corners from the rotation and checks unit edges,
  right angles, orientation and the corner mean on them, then every corner in the box.
  It decides every pair, with no distance filter, by the exact area that one square’s
  four closed half-planes clip from the other.
  For each pair whose centres are closer than 2 it also computes the exact squared
  Euclidean distance between the closed squares.

The routes must classify every pair the same (disjoint, touching or overlapping) and
find the same least wall clearance and wall contacts.
Its `same` command decides whether a fact states exactly a certificate’s squares, row by
row. Its `selftest` command runs 21 hand-built packings and 6 reader cases: separated,
touching at an edge, a corner and a vertex, overlapping by $10^{-30}$, and separated
only on the second square’s axis.
It decides. It shares `Fraction` (route C) and CPython integers with the maintained
routes, and the separating-axis method (route Z) with both of them.
It shares no code with them, with any earlier review’s checker, or with the source.
It is registered as `V-mishapolk-719-review-check` in [verifiers.yaml](../../../../../frontier/verifiers.yaml), and its run
is the evidence entry `E-mishapolk-719-review-exact-feasibility`.

`sharp_controls_t229.py` builds eight mutants of each certificate, at exact contact and
$10^{-30}$ past it. It takes the packet’s derived fact, writes it back in the source’s
certificate format exactly (checking the round trip), and builds the mutants from that.
It decides each mutant with this review’s checker and with the two maintained routes,
called as the packet’s replay calls them through the `evand-cert` adapter.
It also runs the kernel’s `run_sharp`, and checks that the adapter’s certificate equals
the packet’s fact as `read_facts` admits it.
The maintained routes’ verdicts are theirs; the program adds the mutants and the
expectations. It is a premise check: it decides no certificate. It is registered as
`V-mishapolk-719-review-controls`.

`agree_t229.py` holds the checker’s results to the packet’s receipt.
`margins_t229.py` computes each side’s exact margins in report order, against the house,
and against every later count’s bounds on `main`, with the prints’ rounding.
`identity_t229.py` measures poses under the box’s eight symmetries with its own
Hungarian algorithm.
It also reports the most-turned square’s nearest neighbours and the squares moved beyond
a tenth. None of these three decides anything, and no evidence entry needs to cite them.

## How to Run

From this directory, `REPO` being the repository root, `P` this packet, and `CHECKOUT` a
clone of `Mishapolk/square-packing-records` checked out at
`12fc46678fa8eefa3f156ff37dfffd84c8f3a580`. The source’s certificates are not retained
here; every command that names `$CHECKOUT` also has a run from the packet’s facts alone.
`DATA` is prepared with `git show` as listed above.
The `-I` programs run on any CPython 3.12 or later.

```sh
P=$REPO/packing/resources/web/mishapolk-issue719-2026-10-22; C=$CHECKOUT/certificates
python -I programs/review_t229_check.py selftest outputs/selftest-py314.json
python -I programs/review_t229_check.py check outputs/out-check-105.json \
  "T-229@105:cert=$C/n-105.cert" "T-229@105:fact=$P/facts/n-105.yaml.gz"
python -I programs/review_t229_check.py check outputs/out-check-204.json \
  "T-229@204:cert=$C/n-204.cert" "T-229@204:fact=$P/facts/n-204.yaml.gz"
python -I programs/review_t229_check.py same outputs/out-same.json \
  "T-229@105=$C/n-105.cert=$P/facts/n-105.yaml.gz" "T-229@204=$C/n-204.cert=$P/facts/n-204.yaml.gz"
python -I programs/agree_t229.py outputs/out-agree.json \
  outputs/out-check-105.json,outputs/out-check-204.json $P/receipts/exact-certification.json.xz \
  "T-229@105:fact=105=$P/facts/n-105.yaml.gz" "T-229@105:cert=105=$C/n-105.cert" \
  "T-229@204:fact=204=$P/facts/n-204.yaml.gz" "T-229@204:cert=204=$C/n-204.cert"
python -I programs/margins_t229.py $REPO $DATA $C outputs/out-margins.json   # or - for $C
W=$REPO/packing/resources/web; H=$DATA/main-witnesses
python -I programs/identity_t229.py outputs/out-identity-105.json \
  "719@105=$P/facts/n-105.yaml.gz" "T-174 house@105=$H/n-105.yaml" \
  "T-174 facts@105=$W/pingyou-pr574-certificates-2026-10-13/facts/n-105.yaml.gz" \
  "T-183 #593@105=$W/mishapolk-records-2026-10-14/facts/n-105.yaml.gz" \
  -- "719@105:T-174 house@105" "719@105:T-183 #593@105" "T-174 house@105:T-174 facts@105" \
  "T-174 house@105:T-183 #593@105" --focus "719@105:T-174 house@105"
python -I programs/identity_t229.py outputs/out-identity-204.json \
  "719@204=$P/facts/n-204.yaml.gz" "T-225 house@204=$H/n-204.yaml" \
  "T-225 source@204=$W/evand-regularized-2026-10-20/source/search/regularize/lists/certs/n-204.cert.gz" \
  "T-223 #678@204=$W/couzo-issue678-2026-10-18/source/certificates/best/n204.cert" \
  "T-228 #675@204=$W/couzo-issue675-2026-10-18/source/certificates/best/n204.cert" \
  "T-226 #670@204=$W/couzo-issue670-2026-10-17/source/certificates/n204.cert" \
  "T-186@204=$W/mishapolk-kkt-refinements-2026-10-14/facts/n-204.yaml.gz" \
  "T-183 #593@204=$W/mishapolk-records-2026-10-14/facts/n-204.yaml.gz" \
  "719 n204.cert@204=$C/n204.cert" \
  -- "719@204:T-225 house@204" "719@204:T-223 #678@204" "719@204:T-228 #675@204" \
  "719@204:T-226 #670@204" "719@204:T-186@204" "719@204:T-183 #593@204" \
  "T-225 house@204:T-225 source@204" "T-225 house@204:T-223 #678@204" "719 n204.cert@204:719@204" \
  --focus "719@204:T-225 house@204" "719@204:T-223 #678@204" "719@204:T-228 #675@204" \
  "719@204:T-226 #670@204" "719@204:T-186@204"
python -I programs/identity_t229.py outputs/out-identity-204-couzo-copy.json \
  "719@204=$P/facts/n-204.yaml.gz" "T-225 house@204=$H/n-204.yaml" \
  "T-223 #678@204=$W/couzo-issue678-2026-10-18/source/certificates/best/n204.cert" \
  "Couzo 5a299b4 best/n204@204=$DATA/couzo/5a299b4-certificates-best-n204.cert" \
  -- "Couzo 5a299b4 best/n204@204:T-225 house@204" "Couzo 5a299b4 best/n204@204:T-223 #678@204" \
  "719@204:Couzo 5a299b4 best/n204@204"
# from $REPO/packing with the project interpreter, PYTHONDONTWRITEBYTECODE=1, R this directory:
python $R/programs/sharp_controls_t229.py $R/outputs mishapolk-issue719-2026-10-22 "T-229@105=105=$P/facts/n-105.yaml.gz"
python $R/programs/sharp_controls_t229.py $R/outputs mishapolk-issue719-2026-10-22 "T-229@204=204=$P/facts/n-204.yaml.gz"
# what the issue's sqpack command does: exit 0, no output, whatever the argument
python -I $REPO/packing/src/sqpack/verify.py $C/n-105.cert; echo $?
```

| Program | What it printed | Kept output |
| --- | --- | --- |
| `review_t229_check.py selftest` | 27 of 27 as expected, under 3.14.7 and 3.13 | `selftest.log`, `selftest-py313.log`, `selftest-py314.json`, `selftest-py313.json` |
| `review_t229_check.py check` | 4 of 4 accepted on both routes, the routes agreeing pair by pair. At 105: least wall clearance exactly $5 \times 10^{-21}$ and least gap $9.999999999999988 \times 10^{-21}$ (squares 71 and 86). At 204: $4.9998207 \times 10^{-13}$ and $9.980857291582 \times 10^{-13}$ (squares 11 and 17). No contact. 5,460 and 20,706 pairs on each route; route Z 0.03 to 0.12 s, route C 1.4 to 3.9 s an input | `out-check-105.json`, `out-check-204.json`, `check-*.log`, `time-check-*.log` |
| `review_t229_check.py same` | each fact states its certificate exactly, 105 and 204 rows | `out-same.json`, `same.log` |
| `agree_t229.py` | every side, pose, pair count, least clearance and least gap equal to both receipt routes, from the facts and from the certificates; every receipt control refused by both | `out-agree.json`, `agree.log` |
| `sharp_controls_t229.py` | at both counts, F0, N0 and P0 accepted at exactly 0, and F1, N1 and P1 refused at exactly $-10^{-30}$, by both of this review’s routes and both maintained routes. R1 refused by both readers; R2 refused by this review’s reader and read exactly by the maintained one; the kernel’s `run_sharp` as required; the adapter’s certificate equal to the packet’s fact | `out-controls-T-229-n105.json`, `out-controls-T-229-n204.json`, `controls-*.log`, `time-controls-*.log` |
| `margins_t229.py` | each side below every earlier report at its count (15 and 13), below T-174 by $5.1834384423 \times 10^{-12}$ and T-225 by $1.0063597267 \times 10^{-8}$, and below all 438 and 240 bounds at later counts; the prints’ rounding | `out-margins.json`, `margins.log` |
| `identity_t229.py` | the review’s identity table, square 38’s release at 204, and the squares moved beyond a tenth | `out-identity-105.json`, `out-identity-204.json`, `out-identity-204-couzo-copy.json`, `identity-*.log`, `time-identity-*.log` |

`acquire-check.log`, `check-claims.json` and `check-replay.log` are this lane’s runs of
the packet’s `acquire_source --check`, `check-claims` (equal to the retained
`claims.json`) and `check --replay` (`2 certificates and 6 jobs admitted`), with their
`time-*.log`. `sqpack-verify-as-script.log` is `packing/src/sqpack/verify.py` run as the
issue runs it: exit 0 and no output on the 105 certificate, on the duplicated-square
certificate, and on a path that does not exist.
`sqpack-verify-history.log` is every revision of that file, none with an entry point.
`checker-decided-at.txt` is when the checker had decided both certificates (12:24:41Z).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
