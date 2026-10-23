# The Stage 4 Review of Issue #755: Programs and Receipts

These are the programs and receipts of the stage 4 mathematical review of Amund
Kristiansen’s certificate at 303, from issue #755
([the review](../../../../../../docs/project/reviews/review-2026-10-23-amundsk-n303.md)).
The entry the records branch `claude/intake-2026-10-23-755` registers for it is T-238,
which `main` does not yet hold.
They were written on 23 October 2026 by the review lane `c-review-t238-math` (bead
`think-jdz0`), an AI reviewer of the Claude system family (Anthropic) at the strong
sub-agent tier (`tbd-strong-max`) and maximum reasoning.

The certificate is not retained here: the gist states no licence.
Every program reads it from a checkout of the gist at
`511f56bf6e6afb4eb22f12d31371c2a2fe7b4767`, whose `s303_amund.cert` has SHA-256
`9ec01059…511b` and whose `s303_amund.input.txt` has `19fc5d17…4ba4`. Each receipt
records the digest of the file it read.

All programs ran with CPython 3.14.7 (`packing/.venv/bin/python3`), with `-I`, under
`nice -n 19`, at most two at a time, on 23 October 2026. `/home/user/squares/packing`
below is the `packing/` directory of a checkout at `main` `c1115c095`, and `CERT` and
`INPUT` are the gist’s two files.

## What Each Program Does

The programs are in `programs/` and their receipts in `outputs/`.

| Program | Role | What it read | Receipt |
| --- | --- | --- | --- |
| `review_t238_check.py` | **decides** finite feasibility, on two routes that share only a reader | the certificate | `outputs/check-route-z.json`, `outputs/check-route-e.json`; the second run’s in `outputs/second-run/`; `--self-test` in `outputs/selftest.json` |
| `maintained_routes_t238.py` | premise check: runs the two maintained routes as `upper_bound_reports certify`’s child does, and the kernel’s sharp controls | the certificate; the records lane’s declaration for the witness prefix and limitations | `outputs/maintained/` |
| `sharp_controls_t238.py` | premise check: 21 mutants, decided by both of the checker’s routes and both maintained routes | the certificate; the checker; the maintained routes | `outputs/sharp-controls.json` |
| `agree_t238.py` | decides nothing: holds every shared number equal | the receipts above; the records lane’s replay receipt and derived fact | `outputs/agree.json` |
| `margins_t238.py` | decides nothing: the side, its prints and its margins | the certificate; the retained file of every report at 303 and the case records at 304 to 320, at `c1115c095` | `outputs/margins.json` |
| `method_t238.py` | decides nothing: the certificate against the float packing it was made from, and T-230’s against its own | the certificate and input; T-230’s retained certificate and input | `outputs/method.json` |
| `identity_t238.py` | decides nothing: poses against fourteen packings at 303, and contacts against T-230 | the certificate; the retained packings at `c1115c095`; the checker, for exact gaps | `outputs/identity.json`; run on T-230’s certificate, `outputs/identity-t230.json`; `--self-test` in `outputs/identity-selftest.json` |

`review_t238_check.py` was written from the mathematics, the issue, the gist README and
the certificate, before its author read any maintained route, replay tool, or program of
the source or of Evan Daniel’s repository.
Its SHA-256 when it decided, at 16:36Z on 23 October, was
`ba967921422bbc56363e83e03f1ef9593303c72d0b1683553a73f6c011bb8480`, and it has not
changed since. Its author read Evan Daniel’s `verify_cert.py`, `verify_cert2.py` and
`dilate_cert.py` at `7982d7a` afterwards, and ran none of them.
`maintained_routes_t238.py`, `sharp_controls_t238.py`, `margins_t238.py`,
`method_t238.py` and `identity_t238.py` were first written after the checker decided and
before that reading, and `agree_t238.py` after it.
None of them uses anything of Daniel’s programs except `method_t238.py`, which was
revised after the reading to write out `dilate_cert.py`’s formulas and compare them with
the certificate. `sharp_controls_t238.py` was revised afterwards only to choose its
tilted pairs by angle, `identity_t238.py` to report more of what it measures, and
`margins_t238.py`, after the 22 October review of T-230 had been read, to add the
Kingbird catalogue’s captures.

## How to Run Them

From any directory, with the project interpreter:

```bash
PY=/home/user/squares/packing/.venv/bin/python3
DIR=packing/resources/web/amundsk-n303-2026-10-23/review/review-2026-10-23/programs
$PY -I $DIR/review_t238_check.py --self-test
$PY -I $DIR/review_t238_check.py CERT --route Z --receipt OUT-Z.json [--pairs Z.tsv]
$PY -I $DIR/review_t238_check.py CERT --route E --receipt OUT-E.json [--pairs E.tsv]
$PY -I -B $DIR/maintained_routes_t238.py CERT --packing /home/user/squares/packing \
    --declaration report.json --out OUTDIR --sharp
$PY -I -B $DIR/sharp_controls_t238.py CERT --checker $DIR/review_t238_check.py \
    --packing /home/user/squares/packing --declaration report.json --out sharp-controls.json
$PY -I $DIR/agree_t238.py CERT --checker $DIR/review_t238_check.py --outputs $DIR/../outputs \
    --receipt exact-certification.json.xz --fact n-303.yaml.gz --out agree.json
$PY -I $DIR/margins_t238.py CERT --repo /home/user/squares --ref c1115c095 --out margins.json
$PY -I $DIR/method_t238.py CERT INPUT --reference T230.cert T230.input.txt --out method.json
$PY -I $DIR/identity_t238.py --self-test
$PY -I $DIR/identity_t238.py CERT --checker $DIR/review_t238_check.py --repo /home/user/squares \
    --ref c1115c095 --out identity.json
$PY -I $DIR/identity_t238.py T230.cert --repo /home/user/squares --ref c1115c095 \
    --out identity-t230.json
```

`report.json`, `exact-certification.json.xz` and `n-303.yaml.gz` are the records lane’s
`acquisition/report.json`, `receipts/exact-certification.json.xz` and
`facts/n-303.yaml.gz` in the packet, read from the records branch at `3003d81d5`.
`T230.cert` and `T230.input.txt` are
`packing/resources/web/evand-n303-2026-10-22/source/search/packer/candidates/s303_r303w0.cert`
and `.input.txt`.

## What They Printed

- `review_t238_check.py --self-test`: 15 hand-built cases, 13 malformed texts and 2,000
  random pairs, every one as expected, with no failures; the two routes decided every
  random pair alike, 1,600 of them built to touch and 800 of those pushed $10^{-30}$
  into overlap.
- `review_t238_check.py`, route Z: `ACCEPTED`, 45,753 pairs, least gap
  $1.205000000000204 \times 10^{-12}$ at (2, 13) and five other pairs, least wall
  clearance $6.020000000001029 \times 10^{-13}$ at the top (square 3), 0.31 s. Route E:
  `ACCEPTED`, 45,029 pairs by discs and 724 close, the least Euclidean distance the same
  number at the same six pairs, 8.7 s. The two routes’ per-square wall clearances and
  per-pair gaps are equal (equal digests).
- `maintained_routes_t238.py --sharp`: the positive accepted by `exact_verify` and
  `independent` and validated; the duplicate-square and outside-container controls
  refused by both; both sharp controls accepted at contact with margin 0 and refused
  past it at $-10^{-30}$.
- `sharp_controls_t238.py`: every one of the 21 mutants as expected on all four
  deciders.
- `agree_t238.py`: 116 of 116 checks equal.
- `margins_t238.py`, `method_t238.py` and `identity_t238.py`: the tables of the review.
  `margins_t238.py` was extended after its author read the 22 October review of T-230,
  to read the Kingbird catalogue’s two retained captures at 303.
- `identity_t238.py --self-test`: 300 instances, no failures.

## Registration

`review_t238_check.py` decides and belongs in `packing/frontier/verifiers.yaml` with its
independence record.
`maintained_routes_t238.py` and `sharp_controls_t238.py` are premise checks and belong
there too. `agree_t238.py`, `margins_t238.py`, `method_t238.py` and `identity_t238.py`
decide nothing and are cited by no evidence entry; they are kept as the review’s
measurements. `outputs/program-digests.sha256` lists every program’s SHA-256.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
