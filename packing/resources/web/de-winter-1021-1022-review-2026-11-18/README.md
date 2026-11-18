# Stage 4 Review Programs for #1021 and #1022 (Lane r1021-1118)

The programs and receipts of the blind stage 4 mathematical review of Joost de Winter’s
certificates of $s(268)$ (issue #1021) and $s(270)$ (issue #1022), at
`JoostdeWinter/square-packing` commit `a1ba5019e787e407646293d7bef81d63c9951b32`. The
review is
[`docs/project/reviews/review-2026-11-18-de-winter-1021-1022.md`](../../../../docs/project/reviews/review-2026-11-18-de-winter-1021-1022.md).

Every program here was written for this review and imports nothing from this
repository or from the source.
The checker, the measurements, the controls plan and the self-test were frozen before
any of them read a certificate (`frozen/checker-frozen.sha256`, pushed 06:08:52Z on 18
November 2026). One program, `r1021_post.py`, was written after that freeze; it
converts the predecessors’ file layouts for the frozen modules and decides nothing
itself (see below).

The source files are not retained here.
`out/custody.json` gives their SHA-256 and Git blob ids, and
`frozen/sources-pins.sha256` checks a copy fetched at the pin.

## The Programs

| Program | What it does | Reads |
| --- | --- | --- |
| `r1021_read.py` | Strict readers: form J (`n2NN_exact.json`), form C (Witness/v2 corners, ids `square-k`), a house corners file (integer ids) and a centre-basis witness; one scalar grammar; YAML read twice (events and composer, then line by line) | the files given |
| `r1021_geom.py` | Method A: separating axes on poses in Python integers; wall clearances; the twin test; contact factors | poses only |
| `r1021_clip.py` | Method B: Sutherland–Hodgman clipping in GMP rationals, both ways round; walls and area inside the box; margins from corners (control C0) | corners only |
| `r1021_check.py` | The decision: a report (form J and form C, both methods, natively and crossed) or a house file | the files given |
| `r1021_contract.py` | Option D’s quantities: $\lambda^*$, the binding pairs, the shrunk side and the contraction margin; the option D test | poses |
| `r1021_identity.py` | Identity of two packings under the box’s eight symmetries, in the lower-left and box-centred frames; nearest centres and the optimal assignment | poses |
| `r1021_measure.py` | Sides and prints, the contraction margins (each shrunk packing decided by both methods), option D, identity, the house witness on `main`, the issues’ numbers | de Winter’s files, a house per count, the house witnesses |
| `r1021_controls.py` with `controls-plan.json` | The frozen controls: 45 for a report, 33 for a house | the files given |
| `r1021_custody.py` | SHA-256 and blob ids by every route, the trees at the pin and the head, the source’s `SHA256SUMS`, the pushes | a clone and fetch directories |
| `r1021_selftest.py` | 67 hand-derived checks and 10 broken copies | nothing |
| `r1021_synth.py`, `r1021_trial.py`, `r1021_ctrial.py` | Synthetic packings, pricing, and the controls under each broken copy | synthetic files only |
| `r1021_fmt.py` | Exact decimal prints; decides nothing | — |
| `r1021_post.py` | Written after the checker freeze: unquotes side and corner scalars, reads `.cert` files, makes house witnesses ASCII and drops their certificate block, each checked with PyYAML to leave every value unchanged; then decides and measures through the frozen modules | the predecessors’ files |
| `issue-1021.json`, `issue-1022.json` | The issues as the REST API returned them at 05:36:49Z | — |

## How to Run Them

With the project interpreter, from `programs/`, under `nice -n 19`, at most two at a
time. `SRC` holds the four source files fetched at the pin (`frozen/sources-pins.sha256`
checks them), `W` is `packing/resources/web`, and `CONV` a scratch directory.

```bash
PY="nice -n 19 ../../../../.venv/bin/python3 -I -B"
$PY r1021_selftest.py ../out/selftest.json
$PY r1021_synth.py 6 60 $CONV && $PY r1021_ctrial.py $CONV ../out/ctrial.json
$PY r1021_trial.py 270 60 ../out/trial-270-60.json; $PY r1021_trial.py 270 120 ../out/trial-270-120.json
$PY r1021_custody.py CLONE a1ba5019e787e407646293d7bef81d63c9951b32 ../out/custody.json \
  PIN API1 RAW1 API2 RAW2 --activity ACTIVITY.json
$PY r1021_check.py report 1021 $SRC/n268_exact.json $SRC/n268_witness.yaml ../out/check-1021.json
$PY r1021_check.py report 1022 $SRC/n270_exact.json $SRC/n270_witness.yaml ../out/check-1022.json
$PY r1021_check.py house T-289 $W/ozden-s268-upper-bound-2026-11-10/source/n-268-candidate.yaml ../out/check-T289.json
$PY r1021_check.py house T-283 $W/ozden-s270-upper-bound-2026-11-09/source/n-270-candidate.yaml ../out/check-T283.json
# after the checker freeze: the predecessors' layouts converted for the frozen readers
M=$W/mishapolk-issue1009-2026-11-16/source
$PY r1021_post.py unquote $W/ozden-s268-upper-bound-2026-11-10/source/n-268-candidate.yaml $CONV/unquoted-T-289.yaml
$PY r1021_post.py unquote $W/ozden-s270-upper-bound-2026-11-09/source/n-270-candidate.yaml $CONV/unquoted-T-283.yaml
$PY r1021_post.py unquote $M/witnesses/2026-11-16/n-268.yaml $CONV/unquoted-T-320.yaml
$PY r1021_post.py unquote $M/witnesses/2026-11-16/n-270.yaml $CONV/unquoted-T-321.yaml
$PY r1021_post.py cert $M/certificates/0000-0999/n268.cert $CONV/unquoted-T-320.yaml $CONV/form-j-T-320.json
$PY r1021_post.py cert $M/certificates/0000-0999/n270.cert $CONV/unquoted-T-321.yaml $CONV/form-j-T-321.json
$PY r1021_post.py compare WIT0/n-268.yaml $CONV/cmp-main0-n-268.yaml   # house witnesses at 0f191a2d23
$PY r1021_post.py compare WIT0/n-270.yaml $CONV/cmp-main0-n-270.yaml
$PY r1021_measure.py $SRC $CONV/unquoted-T-289.yaml $CONV/unquoted-T-283.yaml \
  $CONV/cmp-main0-n-268.yaml $CONV/cmp-main0-n-270.yaml ../out/measure.json
$PY r1021_post.py $SRC $W/ozden-s268-upper-bound-2026-11-10/source/n-268-candidate.yaml \
  $W/ozden-s270-upper-bound-2026-11-09/source/n-270-candidate.yaml POLK WIT0 WIT1 $CONV
$PY r1021_controls.py report 1021 $SRC/n268_exact.json $SRC/n268_witness.yaml ../out/controls-1021.json
$PY r1021_controls.py report 1022 $SRC/n270_exact.json $SRC/n270_witness.yaml ../out/controls-1022.json
$PY r1021_controls.py house T-289 $CONV/unquoted-T-289.yaml ../out/controls-T289.json
$PY r1021_controls.py house T-283 $CONV/unquoted-T-283.yaml ../out/controls-T283.json
```

`POLK` holds `n268.cert`, `n270.cert`, `polk-n-268.yaml` and `polk-n-270.yaml` (#1009’s
files as `main` retains them), and `WIT0` and `WIT1` the house witnesses `n-268.yaml`
and `n-270.yaml` at `0f191a2d23` and `86284ec203`.

## What They Printed

The review gives the numbers and what they mean; each line below is the program’s
summary.

- `r1021_selftest.py`: `PASSED 67 checks; 10 of 10 broken copies caught; failed: []`.
- `r1021_trial.py`: one decision of a 270-square synthetic packing by both methods, 4.6
  CPU-seconds at 60-digit numbers and 11.5 at 120.
- `r1021_ctrial.py`: `PASSED`; the intact programs pass every control on the synthetic
  report and house, each broken copy of the checker fails at least one control or has
  its original refused, and M9 (the identity measurement) is caught by the self-test.
- `r1021_custody.py`: `routes ['pin1', 'api1', 'raw1', 'api2', 'raw2'] agree True`, and
  the source’s `SHA256SUMS` at the head match all four files.
- `r1021_check.py`: `1021 ACCEPT`, `1022 ACCEPT`; `T-289 REFUSE read: square 38 corner
  3[0]: not a plain scalar` and `T-283 REFUSE read: square 84 corner 0[1]: not a plain
  scalar` (the review’s F3).
- `r1021_post.py unquote`: 3, 2, 2,145 and 2,161 lines unquoted in T-289’s, T-283’s,
  T-320’s and T-321’s files, `values unchanged True` each; `cert`: reading `tan-half`,
  0 twin failures at 268 and at 270; `compare`: one line made ASCII in each witness
  before #1023, 20 certificate-block lines dropped in each of the four, values unchanged.
- `r1021_measure.py`: `268 gain 2.015998680e-3 margin 3.204483004e-12 new True` and
  `270 gain 8.343869912e-4 margin 3.211509047e-12 new True`, one to one under no
  symmetry at either.
- `r1021_post.py` (the driver): T-289, T-320, T-283 and T-321 `ACCEPT`; every step new
  under option D; the gains and margins in the review’s Option D section.
- `devtools.contraction_margin` and `devtools.measure_identity` (the second route): the
  receipts in `out/second-route/`; `r1021_routes.py`: `all equal: True comparisons: 52`.
- `r1021_controls.py`: 45 of 45 as stated at #1021, #1022, T-320 and T-321, and 33 of 33
  at T-289 and T-283; `not_as_stated: []` and `not_run: []` at each.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
