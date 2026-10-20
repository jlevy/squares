# Review Programs, 20 October 2026

These are the two programs that the stage 4 review lane of the 19 October intake
(`c-review-678-fable`, for `think-xu4d`) wrote and ran for
[`review-2026-10-20-upper-bound-imports-678.md`](../../../../../docs/project/reviews/review-2026-10-20-upper-bound-imports-678.md),
the review of Francisco Couzo’s 85 exact upper-bound certificates of issue #678, with
what they printed. The lane was an AI agent of the Claude system family (Anthropic),
strong tier, maximum reasoning, prompted separately from the import lane that built this
packet and its replay. It wrote the programs on 20 October 2026 and ran them from 20:46Z
to 20:58Z in a worktree of `claude/intake-678-replay` at `caef09ede`. The records lane
that mapped the review moved them here unchanged (RF-5 of the review).

## What Decides What, and What Is Registered

**`review_678_check.py`** decides certificates: it is the review’s own exact checker,
standard library only, importing nothing from this repository.
It reads each of the 83 certificates and the issue body with readers of its own, and over
$\mathbb{Q}$ decides that every rotation lies on the unit circle, that every square clears
every wall of the closed box by its half-extent, and that every pair whose centres are
closer than $\sqrt2$ has a separating-axis gap of at least 0 along unit normals and an
intersection of area exactly 0, the area found by clipping one square by the other’s four
closed half-planes. At seven counts it decides every pair by separating axes, with no
filter. It holds each print to the header side rounded up at 12 places, and each side,
near-pair count, least wall clearance, least gap and 16-place ceiling to the packet’s
filtered receipt. It is registered in
[`verifiers.yaml`](../../../../frontier/verifiers.yaml) as `V-couzo-678-review-check`,
not clean-room, sharing only Python’s `Fraction` with the packet’s routes, and cited by
the confirming evidence entry `E-couzo-678-review-exact-feasibility`.

**`identity_260.py`** measures and decides nothing about a bound. It compares the three
n = 260 packings, T-196’s retained `n260_exact.json.gz`, the evand `14a9af8` seed and this
packet’s `n260.cert`, under the box’s eight symmetries, in binary64: for the best
symmetry, how many squares of one have a square of the other within a tolerance in
centre with the same axes. It is registered as `V-couzo-678-review-identity`, a premise
check that no evidence entry cites, so that what it shares is on record.

## Programs

Run each from `packing/` with the project interpreter, `python -I` as the review ran
them. `P` is this directory’s `programs/`:

```sh
P=resources/web/couzo-issue678-2026-10-18/review/programs
SRC=resources/web/couzo-issue678-2026-10-18/source
ISSUE=campaign/issue-intake/intake-20261019/issue-678.json
RECEIPT=resources/web/couzo-issue678-2026-10-18/receipts/filtered-exact-replay.json
.venv/bin/python3 -I $P/review_678_check.py $SRC $ISSUE $RECEIPT OUT.json \
    --all-pairs 204 260 330 459 499 545 998 --workers 2
.venv/bin/python3 -I $P/review_678_check.py $SRC $ISSUE $RECEIPT OUT.json \
    --only 204 260 --all-pairs 204 260
.venv/bin/python3 -I $P/identity_260.py \
    resources/web/de-winter-upper-bounds-227-229-260-2026-10-17/source/n260/n260_exact.json.gz \
    campaign/issue-intake/intake-20261019/issue-678-n260-seed-14a9af8.cert.gz \
    $SRC/certificates/best/n260.cert
```

The checker reads the receipt only to compare with it, field by field; the receipt’s
positive rows are unchanged by the near-contact control the records lane added after the
review (RF-2), so the comparison stands.

## What They Printed

| File | Program and run | What it holds |
| --- | --- | --- |
| [`outputs/out-all.json`](outputs/out-all.json), [`outputs/out-all.log`](outputs/out-all.log) | `review_678_check.py` on all 85 rows, every pair at seven counts, two workers | 85 of 85 passed, no disagreement with the receipt; 140,866 near pairs, 1,116,662 separating-axis pair decisions, 695 contacts; 368.2 CPU seconds |
| [`outputs/out-204-260.json`](outputs/out-204-260.json) | the same on 204 and 260 alone, every pair | both passed; the margins at 204 and 260 against T-186, T-155, T-196 and the seed, which the review’s Claims Covered table quotes |
| [`outputs/identity_260.log`](outputs/identity_260.log) | `identity_260.py` | 240 of the seed’s 260 squares within $10^{-7}$ of T-196’s (49 within $10^{-8}$), the other 20 axis-aligned and displaced 0.42 to 0.46; #678’s certificate within $10^{-4}$ of the seed at 162 squares |
| [`outputs/check-replay.log`](outputs/check-replay.log), [`outputs/check.log`](outputs/check.log), [`outputs/pytest.log`](outputs/pytest.log) | the packet’s own `couzo_678_replay check --replay`, `check` and its eight tests, as the review reproduced them at `caef09ede` | `OK: 85 rows verified, every control refused`; 8 passed |

The review did not keep the output of `identity_260.py`: the records lane ran it again,
unchanged, at 22:41Z on 20 October 2026, and its log is that run’s. Its counts are the
review’s. The other files are the review’s own, byte for byte.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
