# Blind Stage 4 Review of jlevy/squares#1050: Programs and Receipts

Lane r1050 of the intake pass of 20 November 2026 (bead `think-5jr0`). This packet holds
the plan, programs, frozen digest lists and receipts of a blind stage 4 mathematical
review of Mira Cult’s claim $s(18) = (7+\sqrt7)/2$. The review itself is
`docs/project/reviews/review-2026-11-20-mira-1050-n18.md`.

The source is read as data at
[Mira-Cult/math `78bec6aa`](https://github.com/Mira-Cult/math/tree/78bec6aacebf304d942a9225e16c2f18165778ff/notes/geometry/unit-square-packing-18),
folder `notes/geometry/unit-square-packing-18/`; `programs/source-files.sha256` holds the
SHA-256 of its 51 files. No source program was opened before checker freeze 2.

## Programs

Every program is this lane’s own, imports nothing from the source or this repository, and
runs under the project interpreter (CPython 3.14.7) as `python -I`; the C++ refuter
builds with the host’s g++ 13.3.0 as `-O2 -std=c++17 -ffp-contract=off`.

| Program | Frozen | Reads | Decides |
| --- | --- | --- | --- |
| `r1050_q7.py` | 1 | (a module) | nothing: exact $\mathbb Q(\sqrt7)$, supports, separating axes, the construction reader |
| `r1050_construction.py` | 1 | a construction file | every wall and pair exactly, and four kinds of mutation |
| `r1050_rack.py` | 1 | the rack | the covering lemma, by an exact branch and bound in $t$ and the centre |
| `r1050_orbits.py` | 1 | the rack; a construction | the orbit count; the cases a packing and its loose moves reach |
| `r1050_selftest.py` | 1 | synthetic inputs only | nothing: holds the four programs above to toy cases |
| `r1050_refute.cpp`, `r1050_refute.py` | 2 | the rack, `out/orbits.json`, `out/witness.json` | refutation attempts on the sample (double precision, $10^{-9}$ padding) |
| `r1050_locate.py` | after | rack, construction, `full-endpoint-mask-cases.json` | nothing: finds the terminals of case 53 that hold a packing |
| `r1050_mutations.py` | after | a copy of the source’s replay folder | nothing by itself: runs the source’s scripts on five mutated inputs |

`programs/review-plan.md` is the plan and `programs/plan-amendment-1.md` its amendment;
`programs/issue-1050.json` is the issue as the REST API returned it at 16:39:34 UTC on 20
November (body only). `out/eight-tilt18-transcribed.json` is the eight-tilt packing of the
source’s `endpoint_rack_gap.eight()`, transcribed here after the freeze.

## Freeze Protocol

1. The plan was committed and pushed with its digest (`frozen/plan-frozen-digest.txt`,
   16:54:02Z) before any checker was written.
2. C1 to C4 and their self-test were frozen (`frozen/checker-frozen-digests-1.txt`,
   17:00:40Z) after running on synthetic inputs only, then ran on the source’s data.
3. C5 and the plan’s amendment were frozen (`frozen/checker-frozen-digests-2.txt`,
   17:28:46Z), after calibration on the source’s lattice at caps 4.40 and 4.70 only.
   The amendment cites freeze 1 by its push time, 17:00:45Z.
4. Only then were the source’s programs opened and run.
5. The findings were frozen in `frozen/findings-frozen-digests.txt` before the record at
   $n = 18$ was read.

Verify a freeze from this directory:

```bash
cd packing/resources/web/mira-cult-n18-1050-review-2026-11-20
sha256sum -c frozen/plan-frozen-digest.txt frozen/checker-frozen-digests-1.txt \
  frozen/checker-frozen-digests-2.txt
```

## Reproduction

From the repository root, with the source cloned at the pin and `$S` its `replay/`
folder:

```bash
R=packing/resources/web/mira-cult-n18-1050-review-2026-11-20
P=$R/programs
PY="packing/.venv/bin/python3 -I"
$PY $P/r1050_selftest.py --scratch "${TMPDIR:-/tmp}" --out $R/out/selftest.json
$PY $P/r1050_construction.py --construction $S/six-tilt18.json --out $R/out/construction.json
$PY $P/r1050_rack.py --rack $S/stabs18-endpoint-window.json --out $R/out/rack.json
for d in 1000,1000 797,359 1000,716 390,390; do
  $PY $P/r1050_rack.py --rack $S/stabs18-endpoint-window.json --drop $d \
    --out $R/out/rack-control-drop-${d/,/-}.json
done
$PY $P/r1050_rack.py --rack $S/stabs18-endpoint-window.json --erosion 1/2 \
  --out $R/out/rack-control-erosion-1_2.json
$PY $P/r1050_orbits.py --rack $S/stabs18-endpoint-window.json --out $R/out/orbits.json \
  --construction $S/six-tilt18.json --witness-out $R/out/witness.json
$PY $P/r1050_refute.py selftest --scratch "${TMPDIR:-/tmp}" --out $R/out/selftest-refute.json
$PY $P/r1050_refute.py sample --rack $S/stabs18-endpoint-window.json \
  --orbits $R/out/orbits.json --witness $R/out/witness.json --scratch "${TMPDIR:-/tmp}" \
  --out $R/out/refute-sample.json --seconds 1200
```

After the freeze: the margin runs `--erosion E` to `out/rack-margin-*.json`; the
eight-tilt packing through `r1050_construction.py` and `r1050_orbits.py` to
`out/construction-eight.json` and `out/witness-eight.json`; `r1050_locate.py` to
`out/locate-six.json` and `out/locate-eight.json`; the source’s replay, from a copy of
`replay/`, as `packing/.venv/bin/python3 -S verify_exact_18.py --workers 3` (log in
`out/source-replay.log`); and `r1050_mutations.py --replay $S --scratch DIR --out
$R/out/mutations.json`.

## What Each Program Printed

The review’s
[What I Ran](../../../../docs/project/reviews/review-2026-11-20-mira-1050-n18.md#what-i-ran)
lists every run, what it printed and its CPU time, and its tables of controls and of the
source’s replay give the rest. In short: the self-tests pass; C1 prints
`CONSTRUCTION_VALID ALL_CONTROLS_REFUSED`; C2 prints `COVERED` and each of its five
controls `UNCOVERED_POSE_FOUND`; C3 prints `orbits 187 burnside 187`; C4 prints
`WITNESSES_CLASSIFIED` with one orbit; C5 prints `UNDECIDED` for all six sampled cases
and the witness; the source’s replay prints its final `PASS`; and the mutations print
`ALL_MUTATIONS_REFUSED`.

C5’s sample ran partly in its driver and partly in `case` mode: cases 91, 93, 56 and 86
in the frozen driver (`out/refute-sample-driver.log`), which was then stopped; cases 2
and 80 and the witness in parallel (`out/refute-case-1.json` to `-3.json`), with the same
settings and budget. `out/refute-sample.json` assembles the seven results with the
sample as the frozen rule draws it.

## What Failed Along the Way

Before the freezes, on synthetic inputs and calibration only:

- The covering checker first looked for a witness of failure at cell centres only; on a
  toy rack whose failure sits on a wall at $t = 0$ it reported undecided, not a false
  pass. It now probes centres and corners.
- The self-test of C1 to C4 first expected eight loose moves in a 2 × 2 grid; there are
  four. The expectation was wrong, not the checker.
- The refuter with fixed angle slices could not refute four squares in a box of side 1.99
  (the inner squares lost more than the margin), and with an unbounded node budget it
  recursed until the stack overflowed. It now bisects slices adaptively and stops at
  depth 400 (plan amendment 1).

After the freezes nothing in `programs/` changed except the additions marked “after”,
and one change made after the findings freeze: `r1050_mutations.py` now finds the rack
file by glob instead of naming it, because this repository’s embedded-JavaScript scan
reads the literal file name as JavaScript (`window.json`). The mutations’ receipt came
from its frozen bytes, SHA-256 `05f747d8…`, which are at commit `08d98848d3`; the current
bytes are `9832dc61…`, so `sha256sum -c frozen/findings-frozen-digests.txt` reports that
one entry as changed, by design.
The first launch of the source’s replay failed before running anything, because the host
has no `/usr/bin/time`; it was relaunched with the shell’s `time`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
