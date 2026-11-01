# The Replay Here of the Two n = 40 Examples, 31 October 2026

The complete runs here of wand125’s `sqverify-fast --continuous` v4 on the two n = 40
densities it was written for, T-145’s and T-157’s, with their controls (think-flxm,
jlevy/squares#533 and #485). They were run by Claude (Anthropic), the intake lane L10
(`bold-ritchie-l10`) of the 31 October 2026 pass (epic think-3guf), tier `tbd-moderate`,
at two threads on a shared four-core x86-64 Linux container.
The lane ran only the verifier built from this packet and the
[review’s programs](../review/README.md), unchanged; it wrote no program.

The
[soundness review of 23 October 2026](../../../../../docs/project/reviews/review-2026-10-23-wand125-sqverify-continuous-soundness.md)
is the review these runs rest on.
Its §11 sets what a replay must show, and each item is checked below.

## What Ran

| Step | Command (paths as below) | Receipt |
| --- | --- | --- |
| Build | `cargo build --release --locked -j 2` in a scratch copy of [`sqverify_fast`](../square-packing/tools/sqverify_continuous/sqverify_fast/), rustc 1.98.0 | [`build-v4.json`](receipts/build-v4.json) |
| Candidates | the review’s `candidates.py` on this repository’s copies of the two densities | [`candidates.json`](receipts/candidates.json) |
| Runs | `sqverify-fast --candidate C --n 40 --continuous --core B --tau T --threads 2 --max-nodes 30000000 > runs/NAME.jsonl`, no `--resume` | `run-NAME.json`, [`runs/`](runs/) |
| Judgements | the review’s `judge_run.py runs/NAME.jsonl C --core B --tau T --expect STATUS` | `judge-NAME.json`, `run-judge-NAME.json` |

```sh
SQ=/path/to/squares
WEB=$SQ/packing/resources/web
PKT=$WEB/wand125-sqverify-continuous-v4-2026-10-12
PY=$SQ/packing/.venv/bin/python3
cp -r $PKT/square-packing/tools/sqverify_continuous SCRATCH/
(cd SCRATCH/sqverify_continuous/sqverify_fast && cargo build --release --locked -j 2)
BIN=SCRATCH/sqverify_continuous/sqverify_fast/target/release/sqverify-fast
$PY -I $PKT/review/programs/candidates.py \
    --rect-n40-l67 $WEB/wand125-rectangle-certificates-2026-10-01/wand125-rectangles/certificates/rect_n40_L67/certified_candidate.json.gz \
    --guzhou-6718 $WEB/guzhou-n40-new-supports-2026-10-11/source/certificate/certified_candidate.json.gz \
    CAND > receipts/candidates.json
$BIN --candidate CAND/c6715.json --n 40 --continuous --core 199529/200000 \
    --tau 4999/5000 --threads 2 --max-nodes 30000000 > runs/c6715.jsonl
$PY -I $PKT/review/programs/judge_run.py runs/c6715.jsonl CAND/c6715.json \
    --core 199529/200000 --tau 4999/5000 --expect VERIFIED > receipts/judge-c6715.json
```

The other runs differ in candidate, core and threshold, as the table below gives.
Each went through the review’s `run_timed.py`, whose receipts keep the absolute scratch
paths the run used and the SHA-256 of the binary, the candidate and the output.

**Custody.** The binary is
`31936c4dcfac398b729990f51820fd5a5b70e23a2e809b71de1ca5864e6de618`, the digest the
imports of 15 and 23 October recorded, and every run’s summary prints `source_sha256`
`619b3c00…c7f5`. The candidates are `c6715.json`
`f4a1ae9b05eeac7fbaca2138237e5ce313cc8e463b930e927d8e5623e3e12c34` and `c6718.json`
`38e0eff1ccb0dd156c43ec24a2292b2e770600ba704881c335d4e3e649a094ba`, the review’s, and
each run’s premises line prints the same `input_sha256`. The candidates themselves are
not kept: `candidates.py` rebuilds them byte for byte from the retained densities.

## What It Showed

| Run | Candidate | Core, threshold | Status | Nodes | Axis patch minimum | Judge | CPU-s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `c6715` | T-145’s density | 199529/200000, 4999/5000 | VERIFIED, 86 of 86 roots | 110,877,174 | 0.99988263 | holds | 3,143.9 |
| `c6718` | T-157’s density | 3350/3359, 4999/5000 | VERIFIED, 86 of 86 roots | 118,717,888 | 1.00149865 | holds | 4,746.8 |
| `c6715_control` | c6715, every weight × 985/1000 | 199529/200000, 4999/5000 | REFUSED, 86 of 86 | 7,714 | 0.98488, refused | holds; 86 refutations, least 0.98711 | 2.1 |
| `c6718_control` | c6718, every weight × 985/1000 | 3350/3359, 4999/5000 | REFUSED, 86 of 86 | 5,979 | 0.98648, refused | holds; 86 refutations, least 0.98648 | 2.5 |
| `c6715_oblique` | c6715 | 199529/200000, 24997/25000 | VERIFIED, 86 of 86 roots | 113,317,246 | 0.99988263 | holds, as VERIFIED | 3,156.5 |
| `c6718_oblique` | c6718 | 3350/3359, 1 | VERIFIED, 86 of 86 roots | 124,136,598 | 1.00149865 | holds, as VERIFIED | 4,935.5 |
| `c6718_oblique1001` | c6718 | 3350/3359, 1001/1000 | REFUSED, 17 of 86 roots, the patch verified | 169,336,387 | 1.00149865 | holds; 0 refutations | 6,624.9 |
| `c6718_oblique2503` | c6718 | 3350/3359, 2503/2500 | REFUSED, 19 of 86 roots, the patch verified | 171,796,970 | 1.00149865 | holds; 0 refutations | 6,487.3 |

**The claims.** Both runs verify at all 86 roots and at the patch, no root inherited,
every verified root a complete binary cover ($\text{nodes} = 2\,\text{leaves} - 1$)
whose least certified bound is at least $\tau$, and each summary’s claim is the
register’s: $s(40) > 1340000/199529$ (T-145) and $s(40) > 3359/500$ (T-157). Their node
totals, 110,877,174 and 118,717,888, and least certified bounds, 0.9998000000016 and
0.9998000000076, are the source README’s v3 rows to the last node, so the measure is the
same, in the same order, and v4’s search equals v3’s on it.
At two threads they took 1,624 s and 2,448 s of wall time, 0.87 and 1.32 CPU-hours,
against think-flxm’s price of about 0.66 and 0.71 (high 2.39 and 2.78); the host was
shared with another lane’s two-thread replay throughout.

**The mass controls** reproduce the review’s rows node for node and the source’s README
rows for v3. Each is refused at the axis patch and at every root within a few dozen
boxes, so, as the review’s §11 says, it is a coarse test of the oblique search.
They are the source’s controls, rebuilt here from this repository’s copies of the
densities, not controls designed here.
The source’s third control, T-157’s density at core 3348/3359, was not run again: it
stands on the 23 October review’s run alone, refused in 12,364,148 nodes with 2 of its
86 refusals refuting (the review’s SC-9).

## The Oblique Controls

§11 of the review asks for a control that keeps the axis patch and fails only at oblique
roots, so that its refusal tests the oblique bound where it is tight.
The design used here changes the threshold, not the density: each claim’s own candidate
at its own core, with $\tau'$ a round rational strictly between $\tau = 4999/5000$ and
the axis patch’s minimum that the claim’s run printed.

- **c6715**: the patch minimum is 0.99988263, and $\tau' = 24997/25000 = 0.99988$.
- **c6718**: the patch minimum is 1.00149865, and $\tau' = 1$; then, after review A1 of
  #865, $\tau' = 1001/1000$; then, after #865 merged, $\tau' = 2503/2500$.

Since $\tau' > \tau$, every premise still holds ($40\tau' > 3999/100$), and since
$\tau'$ is below the patch minimum, the patch verifies.
A refusal can then come only from the 86 oblique roots, and it counts only where the
judge finds the witness a legal pose whose exact capture, computed apart from the crate,
is below $\tau'$: a pose where the statement at $\tau'$ is false.
This is the same move as control H of the 10 October contract, which ran the producer’s
axis kernel just above and just below its minimum.

What it tests that the mass controls do not: that the oblique branch and bound refuses,
with a true witness, a statement false only at oblique poses and false there by less
than $\tau' - \tau$ (at most $8 \times 10^{-5}$ for c6715). What it cannot test: an
error that over-estimates every capture by more than the gap between the true oblique
minimum and $\tau$ would still pass the claim’s run, and this control sees only the
poses where the oblique minimum lies below $\tau'$. Had a run come back VERIFIED, it
would have shown the axis to be the binding constraint for that density at $\tau'$, and
the control would need a density mutant instead.

The oblique runs used a budget of 4,000,000 nodes a root, above every claim root’s count
(at most 3,175,983), so that a root the claim verified cheaply cannot stall the control,
and a refusal for budget, which the judge never counts, stays visible.

**c6718 came back VERIFIED at $\tau' = 1$**: every root and the patch, 124,136,598
nodes, least certified bound 1.0000000001, 4,935.5 CPU-seconds, judged faithful as
VERIFIED. So T-157’s density captures at least 1 at every legal pose of side 3350/3359,
and no threshold at or below 1 can fail at the oblique roots alone.
The run is a measured fact about the density, not a control: a counted oblique control
for it needs a threshold in $(1, 1.00149865)$, where the oblique minimum is unknown, or
a density mutant that lowers the oblique captures and leaves the axis patch alone.

**c6715 came back VERIFIED at $\tau' = 24997/25000$** too: every root and the patch,
113,317,246 nodes, least certified bound 0.99988000008, 3,156.5 CPU-seconds, judged
faithful as VERIFIED. Every legal pose of side 199529/200000 captures at least 0.99988
of T-145’s density, within $2.6 \times 10^{-6}$ of the patch’s minimum, so for this
density the axis is the binding constraint, or nearly: only a threshold in
$(0.99988, 0.99988263)$ could fail at the oblique roots alone.

**So neither run is a control.** A threshold shift is the same as scaling every weight
by $\tau/\tau'$. For c6715 the design cannot give one: the density is tightest at or
within $2.6 \times 10^{-6}$ of the axis, so a counted oblique control there needs a
density mutant that lowers the capture at oblique poses alone, with an exact check that
it still passes the patch.
For c6718 the $\tau' = 1$ run bounds the oblique minimum only from below, at 1, against
a patch minimum of 1.00149865, so the window $(1, 1.00149865)$ was still open after it
(review A1 of #865).

**c6718 at $\tau' = 1001/1000$, inside that window, came back REFUSED with no
refutation** (review A1’s proposal): the patch and 69 roots verified, 17 roots refused,
169,336,387 nodes, 6,624.9 CPU-seconds, judged faithful, every witness a legal pose and
none below $\tau'$. It is no counted control.
At the four roots of $t$ in $[23/100, 1/4]$ the search reached resolution at legal poses
whose exact captures are $1001/1000$ plus $1.9 \times 10^{-13}$ to
$2.9 \times 10^{-12}$; the other 13 refusals, roots 3 and 4 ($t$ in $[1/1000, 1/100]$)
and 75 to 85 ($t$ in $[9/25, 83/200]$), stopped at the node budget at poses capturing
1.0017 to 1.016, which decides nothing there.
With the $\tau' = 1$ run, T-157’s least oblique capture lies in
$[1, 1001/1000 + 2.9 \times 10^{-12}]$.

**c6718 at $\tau' = 2503/2500$, between those witnesses and the patch minimum, came back
REFUSED with no refutation too**: the patch and 67 roots verified, 19 roots refused,
171,796,970 nodes, 6,487.3 CPU-seconds, judged faithful, every witness a legal pose and
none below $\tau'$. Eleven refusals stopped at the node budget (roots 3 to 5, 76 and 79
to 85). The other eight, roots 49 to 52 and 74, 75, 77 and 78 ($t$ in $[71/200, 19/50]$
for the last four), reached resolution at legal poses capturing $2503/2500$ plus
$3.4 \times 10^{-13}$ to $3.0 \times 10^{-12}$.

**What the two runs show about the design.** At both thresholds the same four roots were
refused at resolution with a witness just above $\tau'$, though the $\tau' = 1001/1000$
run had already exhibited, at those roots, legal poses capturing less than $2503/2500$:
the statement at $2503/2500$ is false at oblique poses alone, with the patch holding,
but the program’s refusals do not show it.
Witnesses within $3 \times 10^{-12}$ above $\tau'$ at both thresholds are what a box
straddling the level set where the capture equals $\tau'$ would report, since the
program’s witness is the refused box’s path centre (the review’s SC-6), on that level
set rather than inside the region below it; this is an inference from the two runs, not
something the program states.
So a threshold shift near the density’s least capture yields refusals the judge cannot
count, and a counted oblique control for c6718 needs captures well below $\tau'$ over a
region the search reaches first, from a density mutant, as for c6715, or from a witness
rule that reports the least capture it found.
That design stays with think-flxm; no further threshold run is proposed.

## What This Does Not Establish

The runs decide the two claims with code other than the producer’s, by the same method:
the mode’s author read Guzhou0806’s kernel before writing it (`PROVENANCE.md`), so the
relation is independently re-implemented after reading the producer’s code, not
clean-room. They share this repository’s `axis.rs`, `exact.rs`, `interval.rs`,
`oracle.rs` and `rotated.rs` byte for byte, and the near-axis patch is the same
`axis.rs` sweep that `E-n040-guzhou-continuous-pose-crate-axis` and
`E-n040-guzhou-new-supports-crate-axis` already run.
No counted oblique control has run: the mass controls are refused at the patch and at
every root within a few dozen boxes, and of the four threshold-shift runs, this lane’s
design, two verified and two refused without a refutation.
Nothing here is a second method, a formal verification or human oversight, and no rung
moves.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
