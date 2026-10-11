# Plan: Confirming Four wand125 Lower Bounds of 10 October

**Date:** 2026-10-11

**Author:** Claude (agent), preparation lane, for the repository owner

**Status:** Ready to run after jlevy/squares#487 merges.
Nothing expensive has started.
The owner set a budget of about 23 to 35 CPU-hours for these four confirmations and
asked that no long job start before #487 is validated, recorded and merged.
This lane prepared the code, the packets and this plan, and proved each route end to end
on one or two directions with about 4.5 CPU-minutes in all.

**Workflow:** W2, stage 4 of the
[result import process](../../../../packing/campaign/result-import.md#stage-4-validate),
for four entries registered at V0/C0 by #487

**Beads:** `think-r333` (T-132), `think-i85v` (T-142, T-143), `think-nd7g` (T-144)

## Summary

| Entry | Claim | Certificate | Route | Priced CPU-hours |
| --- | --- | --- | --- | --- |
| T-132 | $s(29) \ge 291/50$ | `mixed_n29_L582`, check2, 2,073 directions | sqverify-fast census and whole-net control | 4.3 to 5.5 |
| T-142 | $s(28) \ge 2297/400$ | `mixed_n28_L57425`, check2, 2,073 directions | the same | 3.3 to 4.5 |
| T-143 | $s(30) \ge 2357/400$ | `mixed_n30_L58925`, check2, 2,073 directions | the same | 4.5 to 6.1 |
| T-144 | $s(122..126) \ge 563/50$ | `mixed_n122_L1126`, linear, 201 angles | T-080’s: `linear-replay` and `linear-control` | 11.2 to 14.6 |

The lower figure of each range is the intake’s price from its eight-direction or
two-angle sample; the upper is the same price at the CPU ratio of this lane’s smoke
runs, taken on a host at load 6 to 7. Both lanes together come to 23 to 31 CPU-hours,
inside the budget, and about seven hours of wall on a four-core host (see the schedule).

One finding blocks one run.
The whole-net control on `mixed_n28_L57425` will fail closed at the axis direction under
the census’s current tolerance, as explained in [Before Starting](#before-starting).
It needs an owner decision and a review before that one control runs.
Everything else is ready.

## What This Lane Changed

All on branch `claude/wand125-confirmations-2026-10-11`, from
`claude/determined-rubin-yjfy2a`:

- **The candidates are retained where the census reads them.** The three check2
  candidates are under `square-packing-bounds/certificates/NAME/candidate.json.gz` in
  their 10 October packets, written by the new `devtools.retain_wand125_release` from
  the pinned assets. Every byte is refused unless its digest is the source manifest’s.
  `retained_data check` passes on both packets.
- **The census finds them.** `MIXED_PACKETS` in `devtools/sqverify_fast_census.py` names
  both packets, and the census reads each as a case on its declared 2,073-direction net.
- **`--evidence` renders their entries.** It finds a report filed under the packet’s
  facts file rather than the candidate.
  It writes `shared-components` for a certificate whose source checker is
  `V-wand125-sqverify-proof-net`, which the 6 October entries did by hand, and it states
  the source manifest as the candidate’s pin.
- **`--sweep-timeout`.** The control’s 99/100 sweep is killed at 14,400 seconds of wall
  by default, which a 2,073-direction sweep at one thread on a shared host can pass.
  The option sets the limit.
- **T-144’s packet has the T-080 route’s shape.** It retains the five small files and
  the acquisition pins.
  The certificate is registered as `n122` in `devtools.audit_wand125_linear` (`LINEAR`),
  with its price samples and the source’s seconds.
- **A release route.** `devtools.audit_wand125_point_and_mixed` gains `--via release`.
  It downloads the pinned asset, refuses it unless its size and SHA-256 are the
  record’s, and reads the proof bundle from it.
  `auto` takes this route alone where the record pins an asset, since the commit holds
  no bundle.
- **`fine_net_followup control-sample`.** It runs the whole-net control’s mutant at
  chosen directions, and the least-bound ones of the source’s run, and judges each
  refusal with the census’s own `refusal_record` and `refusal_held`. It is a diagnostic,
  never a control receipt.
  `sample` now also reads a packet’s retained `.gz` candidate.

Every change has tests; Ruff and BasedPyright report nothing on the touched files.
None changes the census’s verdict, admission or control logic, which the declared-net
review says would need another review.
The evidence template and the timeout are not that logic, and a reviewer should confirm
this reading.

## Before Starting

1. **#487 is merged**, and a branch for the stage 4 pull request is cut from `main` with
   this lane’s commits on it.

2. **The n = 28 control and the axis tolerance.** The census control counts a refusal at
   the axis only when the exact capture at the vertex sweep’s least vertex sits above
   the sweep’s certified lower bound by at most `AXIS_ROUNDING`, one part in $10^9$
   (CR-5 of the
   [FC-1 re-check](../../reviews/review-2026-10-06-sqverify-fast-census-control-fc1-recheck.md)).
   This lane’s `control-sample` ran the 99/100 mutant at the axis of each certificate.
   The mutant was refused at all three, at a centre inside the domain, where its exact
   capture is below one.
   The gaps were:

| Certificate | Exact capture minus certified bound | Counted |
| --- | --- | --- |
| `mixed_n29_L582` | $5.2 \times 10^{-10}$ | yes |
| `mixed_n28_L57425` | $2.15 \times 10^{-9}$ | no |
| `mixed_n30_L58925` | $1.9 \times 10^{-10}$ | yes |

   The n = 28 sweep’s certified bound is wider than the tolerance, so the whole-net
   control on `mixed_n28_L57425` will write `CONTROL_FAILED` after about 1.6 to 2.2
   CPU-hours, though the refusal itself is sound.
   The interval sum of the vertex sweep grows with the number of events and with the
   densities, and n = 28’s densest row is the heaviest of the three (eight times its
   density is $4.9 \times 10^6$). Widening the tolerance, or deriving it from the
   sweep’s own enclosure, changes control logic and needs a review first.
   The owner decides. Until then, run T-142’s census row, which this does not touch, and
   hold its control (the schedule places it last).

3. **The budget.** The run starts only on the owner’s go.

## The Commands

All commands run from `packing/` with the project interpreter, never the `python3` on
`PATH`. `W` is a scratch directory outside the tree.

### Build Once

```bash
.venv/bin/python3 -m devtools.sqverify_fast_census --source-digest   # d97758bb… reviewed, exit 0
(cd sqverify_fast && cargo build --release --locked)                 # rustc 1.98.0 by rust-toolchain.toml
sha256sum sqverify_fast/target/release/sqverify-fast                 # 567a0fd5… on this lane's host
```

The census tests admit a row only from a release build of rustc 1.98.0, so install that
toolchain if `rustup` lacks it (`rustup toolchain install 1.98.0 --profile minimal`).
The linear route needs a C++17 `c++` on `PATH`.

### T-132, T-142 and T-143: The Census

```bash
B=sqverify_fast/target/release/sqverify-fast
C="--family mixed --binary $B --out benchmarks/measure-verifier/census-mixed"
ONLY=mixed_n29_L582,mixed_n28_L57425,mixed_n30_L58925

.venv/bin/python3 -m devtools.sqverify_fast_census $C --threads 2 --resume --only $ONLY
.venv/bin/python3 -m devtools.sqverify_fast_census $C --check --only $ONLY   # 3 of 3 VERIFIED
```

- **Threads:** two. Each certificate is one process over all 2,073 directions, 0.8 to 1.5
  hours of wall at two threads on an idle host.
  The census takes them in its own order, n29, n28 and n30, whatever the order of
  `--only`.
- **Receipts:** `benchmarks/measure-verifier/census-mixed/<packet>/<name>.jsonl.gz`, and
  the row in `census.json` there, written when each certificate finishes.
- **Resume:** run the same command again.
  `--resume` keeps every certificate already `VERIFIED`. The census has no per-direction
  resume: its live output goes to a temporary file outside the tree, so a killed run
  loses only the certificate it was on and restarts that one from direction zero.
  Commit after each certificate.

### T-132, T-142 and T-143: The Whole-Net Controls

One certificate at a time, after its census row, n = 28 last and only once the
[axis tolerance](#before-starting) is settled:

```bash
.venv/bin/python3 -m devtools.sqverify_fast_census $C --control --threads 2 \
    --sweep-timeout 43200 --only mixed_n29_L582
.venv/bin/python3 -m devtools.sqverify_fast_census $C --control --threads 2 \
    --sweep-timeout 43200 --only mixed_n30_L58925
.venv/bin/python3 -m devtools.sqverify_fast_census $C --control --threads 2 \
    --sweep-timeout 43200 --only mixed_n28_L57425   # held: see Before Starting
```

- **What it runs:** the original again and the near-threshold mutant at the row’s
  least-bound direction, and the 99/100 mutant at every one of the 2,073 directions
  (FC-1). It must print `CONTROLS_REFUSED`.
- **Receipt:** `benchmarks/measure-verifier/census-mixed/<packet>/<name>.control.json`,
  kind `sqverify-fast-control/v2`.
- **Resume:** none; a control is rerun whole, about as long as its census row.
- **Threads:** two, and `--sweep-timeout 43200`, so a loaded host cannot kill the sweep.
  The evidence template still says the control ran with `--control` in place of
  `--threads 2`, so the records lane says two threads where it pastes it.

### T-132, T-142 and T-143: Records

```bash
.venv/bin/python3 -m devtools.sqverify_fast_census $C --report     # census-mixed/README.md
.venv/bin/python3 -m devtools.sqverify_fast_census $C --summary    # census-summary.json and .md
.venv/bin/python3 -m devtools.sqverify_fast_census $C --evidence --only mixed_n29_L582 \
    --audit-record docs/project/reviews/<the review>.md --date <the run's date>
```

`--evidence` prints the replay entry to paste into `frontier/evidence.yaml`. Its id is
the report’s with `-sqverify-fast-replay` for `-report`, for example
`E-wand125-fine-net-n29-582-followup-sqverify-fast-replay`. It says `shared-components`,
with the crate as the shared part, as the 6 October entries do.
`tests/test_sqverify_fast_census.py` then holds the row, the control receipt, the review
conditions and the review record for every entry that names `V-sqverify-fast`.

### T-144: The Replay

```bash
.venv/bin/python3 -m devtools.audit_wand125_linear linear-fetch n122 --work W/n122 --via release \
    --out resources/web/wand125-linear-n122-2026-10-10/receipts/n122/fetch.json
.venv/bin/python3 -m devtools.audit_wand125_linear linear-replay n122 --range 0-200 \
    --work W/n122 --workers 2 --via release
.venv/bin/python3 -m devtools.audit_wand125_linear linear-merge n122   # FULL_REPLAY_MATCHES_SHIPPED
.venv/bin/python3 -m devtools.audit_wand125_linear linear-merge n122 --check   # RECEIPT_MATCHES
```

- **What it runs:** the release asset downloaded and refused unless it is 31,784,537
  bytes with SHA-256 `6443eae0…5deb`, and the proof bundle read from it and refused
  unless it is `3986d902…55d0`. The bundle is unpacked afresh and bound to the packet,
  `code/` is assembled from the retained, reviewed copies, the driver’s preconditions
  are repeated, and every input of the range is bound to the candidate.
  The shipped `compile_verifier` builds the checker, and each angle is replayed by the
  shipped `replay_angle`. An angle passes only if it returns the certificate’s own
  record.
- **Workers:** two. The axis angle comes first and is the longest, about 1,240 to 1,600
  CPU-seconds.
- **Receipts:** `resources/web/wand125-linear-n122-2026-10-10/receipts/n122/`:
  `range-000-200/{runs,directions}.jsonl` and `summary.json`, then `merged.json`. Each
  angle’s row is appended and synced when it finishes.
- **Resume:** run the same `linear-replay` command again; it replays only the angles
  with no passing row, and a torn last line is cut first.
  `--stop-after-hours H` ends a session cleanly, with exit status 3 while angles remain.
  The work directory keeps the asset and the bundle, so a resumed run downloads nothing.
  `linear-plan n122 --parts K` splits the angles into balanced ranges for several
  sessions or hosts, and `linear-merge` joins them.
- **Then:** `linear-audit --packet wand125-linear-n122-2026-10-10` prints the merged
  replay state beside its receipt, which must stay `RECEIPT_MATCHES` under `--check`.

### T-144: The Control

```bash
.venv/bin/python3 -m devtools.audit_wand125_linear linear-control n122 --work W/n122 --via release
```

It writes `receipts/n122/control.json`. At angle 37, the oblique angle with the fewest
recorded nodes, the original must be accepted and both mutations refused: every mass
scaled by 99/100, and the primitive contributing most at an exact witness centre
dropped. It takes about two minutes.

### T-144: Records

There is no evidence generator on this route; the entry is written by hand on the model
of `E-n101-wand125-linear-1028-source-replay`. Its scope is $n = 122$ to $126$,
`relationship_to_generator: same-implementation` and
`verifiers: [V-wand125-unified-linear-verify-cpp, V-audit-wand125-linear]`. Its replay
text names `--via release` in place of `--via git`, and its limitations give the
CPU-hours and host from `merged.json`, the control’s witness captures, and finding LC-4
of the 2 October review (the records hold no per-direction least lower bound).

## Schedule on a Four-Core Host

The two lanes share no file and no core.

| Lane | Cores | Order | Wall, idle host |
| --- | --- | --- | --- |
| Linear | 2 | `linear-fetch`, `linear-replay 0-200 --workers 2`, `linear-merge`, `linear-control` | 5.6 to 7.3 hours |
| Census | 2 | census rows n29, n28, n30 at `--threads 2`; controls n29, n30 at `--threads 2`; n28’s control last, once allowed | 5.2 to 6.9 hours, and 0.8 to 1.1 more for n28’s control |

Both finish in about seven hours of wall.
Commit and push the receipts at each certificate’s end, as stage 4 requires, on the
branch the beads name.
If the host has other work, keep each lane at two and expect the walls to stretch, not
the CPU. If it has none, the census lane may take four threads once the linear lane
ends.

## The Reviews

Each review is a mapped document under `docs/project/reviews/`, by a reviewer prompted
apart from the replay lane, recorded as `external_review` on the reported entry and
listed in the register entry’s `reviews`.

**T-132, T-142 and T-143.** One review may read all three, as the
[6 October check2 review](../../reviews/review-2026-10-06-wand125-check2-ten-certificates.md)
read ten. It follows the checklist of the
[declared-net soundness review](../../reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md#for-the-records-lane),
items (b)1 to (b)8:

- **(b)1, the file.** This lane pre-checked each candidate.
  Each is format M, `points` is empty and there is no `scaling_factor`. `proof_net` is
  exactly `step` 1/5002 and `last` 2072, with no top-level `net` and no metadata.
  Eight times the densest row’s density is $3.26 \times 10^6$, $4.93 \times 10^6$ and
  $3.41 \times 10^6$ for n = 29, 28 and 30, far below $2^{32}$.
- **(b)2 and (b)3, the case and its premises.** These are read from `census.json`. Lemma
  N0’s (a) to (e) hold in exact arithmetic, with $B(1 + D) = 25009997/25010000$ and the
  last tangent $1036/2501$ past $\tan(\pi/8)$.
- **(b)4 to (b)6.** The candidate’s digest and `retained_data check`, the build
  (`d97758bb…`, release, rustc 1.98.0), and the v2 control receipt with
  `captures_agree`.
- **(b)7, the mathematics of each certificate.**
- **(b)8, the words.** The entries say *re-implemented sharing named components*, since
  the source’s `sqverify-proof-net` (build `ab6e33e1…`) is this repository’s crate with
  its own declared-net reader.

Beyond the checklist, the review reads:

- the source’s 197/200 controls at 32 directions, with their exact witnesses recomputed;
- n = 30’s pre-publication receipt in its newer shape;
- the retention of the candidates under MIT;
- every number the records state;
- the draft significance scores.

**T-144.** As the
[2 October review](../../reviews/review-2026-10-02-wand125-linear-certificates-and-n76.md)
read T-080’s:

- the argument from a linear measure to the bound;
- the point and segment capture bounds;
- the quadrant reduction by the measure’s D4 symmetry, and the angle-zero branch;
- the hypotheses the checker assumes (binary64 with `-ffp-contract=off` and
  `-fno-fast-math`);
- where the request and the record differ.

It also reads what is particular to n = 122:

- the custody of a proof bundle published in a release asset that the release’s
  `SHA256SUMS` does not list, and the new release route;
- the transfer by mass to $n = 123$ to $126$, and the comparison with Green’s
  unrecovered proof, Nagamochi and the Karakuş strip lane;
- the source’s own audit, which calls its replay the same implementation.

## Smoke Evidence

The smoke runs wrote to scratch space only, never to a census folder or a packet’s
`receipts/`, so nothing reads them as a replay.

| Run | Result | CPU s | Source s |
| --- | --- | --- | --- |
| `cargo build --release --locked` | binary `567a0fd5…`, source `d97758bb…`, rustc 1.98.0 | 24 |  |
| `fine_net_followup sample`, n29, r = 0 and 1036 | both verified; nodes (326,041) and bounds equal the source’s | 5.5 | 7.0 |
| the same, n28 | both verified; nodes 276,749 and bounds equal | 4.5 | 5.1 |
| the same, n30 | both verified; nodes 348,777 and bounds equal | 5.8 | 7.7 |
| `control-sample`, n29, r = 0 and 1947 | both refused, both counted | 1.7 |  |
| `control-sample`, n28, r = 0 and 1088 | both refused; the axis not counted (gap $2.15 \times 10^{-9}$) | 1.7 |  |
| `control-sample`, n30, r = 0 and 1585 | both refused, both counted | 1.2 |  |
| `linear-audit --packet wand125-linear-n122-2026-10-10` | exact premises hold from the packet | 2.6 |  |
| `linear-replay n122 --range 37-37 --via release` | `RANGE_REPLAYED`: the asset and the bundle matched their pins, 810 files bound, the record returned | 74.3 | 73.6 |
| `linear-control n122 --via release` | `CONTROLS_REFUSED` at angle 37 | about 124 |  |

Two smoke runs used the samples’ own commands, which read the retained `.gz` candidate
the census will read; the census itself was run only as `--check`, which found the three
new cases unverified as expected.
The host’s load average was 3 to 7 on four cores while three other lanes ran.

## Open Questions for the Owner

1. **The axis tolerance** for n = 28’s control, above: widen `AXIS_ROUNDING`, derive it
   from the sweep’s enclosure, or accept T-142 with another control, and have the change
   reviewed.
2. **Retaining the candidates.** This lane followed the 6 October check2 packet, which
   retains its candidates in Git under the enclosing MIT notice, and kept the nested
   verifier archive, the logs and the assets out.
   The 8 and 10 October packets had retained no upstream byte; if the owner prefers
   that, the retention commits can be dropped before the merge.
   The census would then need another way to read a candidate.
3. **The budget’s go**, once #487 is on `main`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
