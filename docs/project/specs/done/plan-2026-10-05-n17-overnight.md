# Plan: n = 17 Overnight, 5 October 2026

**Date:** 2026-10-05

**Status:** Ready to execute.
Written after the October 5 W3 status review of X-048 and an adversarial Opus review of
it; nothing has run yet.

**Workflow:** W10 codification and selection (opening phase) → W6 research loop as the
coordinating phase, dispatching two W6 rounds, two W3 lanes and one W9 lane; W2 at the
morning checkpoint for any verdict change.

**Tracking:** `think-tmz6` (BC-418, the n17 coordinator), `think-e17c` (H-264),
`think-j6qy` (flag certification), `think-g2qn` (lane R9 and the capture route),
`think-gygy` (the census flag list).
New beads per lane are created at launch (see Registration).

## Objective

Make as much measured progress on $s(17) = S^\ast$ as one night on this container
allows, in two currencies:

- **Census progress.** Certified exclusions that lower the residue below 126,168 states
  in 15,953 orbits, each admitted by a standing verifier’s full pass.
- **Decisive planning evidence.** The per-state price of the residue tail (H-264), the
  capture route after pilot 2 (lane R9), and why mixed flags stall.

Nothing tonight moves a bound, a frontier field or a register rung.

## Branch and Evidence Baseline

Fetched 2026-10-05 around 07:40 UTC:

| Ref | Head | Note |
| --- | --- | --- |
| `main` | `b9a55a51d` | #359 merged |
| #347 `claude/n17-sessions-167-168` | `0e01d6580` | main merged in; the claim calibration from the W3 review |
| #354 → #356 | `f19ab81bd`, `018ee13c5`, `1a73d1e86` | not yet cascaded from #347’s head |
| #360 `claude/n17-fixed-witness-certificates` | `451154f60` | stack top |
| #350 `wand125/n17-bb-native` | `9179aab7d` | leaf on #347 |

The n17 instrument (the kernel, its producer and checker, both standing verifiers, the
branch and bound, the selector, survey and census tools) is identical at `0e01d6580` and
`451154f60` apart from one docstring line in `census_n17_certified.py`. Either commit,
or the cascaded #360, freezes the same instrument.

The review this plan acts on is `opus-review.md` beside it (findings F1 to F19). Its
consequences for tonight: H-264 must be rewritten before it can be measured (F1, F2);
the capture continuation cannot resume (F3); several instruments in the W3 table need
tool changes (F8 to F10); and flag certification is the cheapest direct census progress
(F12).

## What Tonight Decides, Re-Ranked

The W3 draft put the H-264 pilot first.
This plan keeps it as the main measurement but orders the lanes by expected information
and census progress per CPU-hour, and by readiness:

1. **Lane K, flag certification (W6, H-267).** Ready now: H-267 is registered with
   `instrument_ready: true`, the recipe that closed SW9 is frozen in its receipts, and
   the standing verifiers admit.
   Each of the 87 standing flags projects 1,516 (median) to 3,480 orbits off the
   certified 15,953. Six high-margin mixed arity-7 flags (2,410 to 3,024 each) never had
   adaptive rows.
2. **Lane A, the per-state price (W6, H-264).** H-264’s falsifier is the most decisive
   planning measurement available, but it needs a rewrite first (30 to 45 minutes).
3. **Lane R, the capture route (W3, lane R9).** No CPU; settles the open architectural
   question from receipts already committed.
4. **Lane D, stall diagnosis (W3).** A by-product of lane K’s stalls; minutes of CPU
   each.
5. **Lane H, records and tools (W9).** Makes the census read the recheck (87 flags,
   2,197 orbits), adds the survey option lane E needs, and lands the corrected X-048
   addition.
6. **Backfill, lane E, near-endpoint sizing (W6, H-273).** Only when a compute slot
   frees and lane H’s survey option has landed.

## Session Record and Entry Point

- **Session id:** `session-182`. Session-181 is reserved for Session 168’s record
  (`think-wcqs`), 170 to 180 are taken on the stack, and no ref claims 182 or later.
- **File:** `packing/campaign/agent-sessions/session-182-n17-overnight-lanes.md`,
  created at launch with the real start.
- **Entry point (OR-5):** `review-planning-oversight` (insight).
  BC-418’s exit ends with “then W10 on the results”, and the opening phase codifies
  H-264 and selects the lanes.
  The coordinating phase is then `research-loop` (correctness).
  Lanes R, D and H declare their own workflows in their beads; each lane’s phase is
  recorded.
- **Phase history to record:** (1) W3 status review, already performed by a sub-agent
  (the X-048 draft); (2) W10 codification and selection; (3) W6 coordination with the
  dispatched lanes; (4) the morning checkpoint.
- **Clock:** start at the registration commit.
  Wall budget 24 hours, deadline 24 hours after start.
  The morning handoff at **14:30 UTC (07:30 America/Los_Angeles, the October 1 plan’s
  convention for the owner’s morning)** is a checkpoint, not a stop.
  Under OR-8 only the owner, an external blocker or exhausted work ends the run.
- **OR-12:** at the W10 phase, read the count of blocks since the last efficiency block
  from the ledger. At eight, add a W5 block measuring `--edit` and `--push` against their
  ceilings and the kernel producer’s self-check against the standing verifier (0.91
  against 0.18 s a row on N1). Between four and eight, defer it with the reason
  recorded: CPU is tonight’s bottleneck, and a gate measurement would contend with the
  compute lanes.

## Preflight

The coordinator does this before any target run.
Controls may start as soon as the run worktree exists (OR-3); targets wait for the
registration commit.

1. **Resources.** Run `nproc`, `free -g`, `df -h /` and `uptime`. At review time: 4
   CPUs, 14 GB of RAM available, 5.0 GB free on `/`. The scratchpad is on the same
   filesystem and already holds 11 GB.

2. **Disk reclaim, target at least 8 GB free.** The candidates are `spb` (3.5 GB) and
   `fetch282` (3.0 GB) in the scratchpad, both last written 2026-10-04. Delete only
   after confirming no process uses them (`ps -eo pid,args`) and that nothing in them is
   the only copy of a record.
   Leave `wtn17stack` and `wt307fix` alone: other agents are using them (one switched
   branches during the review).
   If less than 8 GB can be freed, lane A runs 10 states instead of 12 (H-264’s lower
   bound), and lane K skips branch-and-bound certificate runs, which write the largest
   objects.

3. **Session branch.** `claude/n17-session-182-overnight` from #360’s head.
   Cascade `0e01d6580` through #354 to #360 first if that is already planned; otherwise
   branch from `451154f60` and cascade later, since the instrument is unchanged.
   Session edits happen in the coordinator’s stack checkout, never in `wtn17stack` or
   `wt307fix`.

4. **Run worktree.** After the registration commit:
   `git worktree add --detach "$SCRATCH/s182-run" <registration commit>`, then from
   `"$SCRATCH/s182-run/packing"`: `uv sync --frozen --all-extras --group dev`. The
   stack’s lock adds gmpy2, which main’s venv lacks.
   Check with `.venv/bin/python3 -c "import gmpy2"`, the one sanctioned inline check.
   Lanes A and K run only from this worktree, and it is never edited.
   That keeps the verifier receipts’ provenance clean, which the census checks before it
   admits. Expect about 1.1 GB for the checkout; the venv hardlinks from the 2.1 GB uv
   cache.

5. **Output tree.** `"$SCRATCH/s182/{A,K,D,logs}"`, outside every worktree.

6. **Environment for every compute job:** `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`,
   `nice -n 10`, a hard `timeout -k 120` above the tool’s own ceiling, and
   `.venv/bin/python3` of the run worktree.
   Never the `python3` on `PATH`; it cannot parse PEP 758 syntax that the project uses.
   The commands below assume `SCRATCH` is the session scratchpad, the working directory
   is `"$SCRATCH/s182-run/packing"`, and `PY=.venv/bin/python3`.

7. **Memory watchdog**, started once in the background and retained as
   `s182/logs/watchdog.sh.txt`:

   ```bash
   while sleep 60; do
     ps -eo pid,rss,args | awk '/devtools\./ && $2 > 5000000 {print $1}' | xargs -r kill
     free -m | awk '/Mem:/ {print strftime("%FT%TZ", systime(), 1), $7}' >> "$SCRATCH/s182/logs/mem.log"
   done
   ```

   A job killed by it is a resource refusal, recorded as such, never a mathematical
   outcome.

## Registration (W10 Phase)

One commit, pushed before the first target run, so the record proves the order.
The coordinator owns every file here.
ID tooling: identifiers are allocated by checking all refs (done at review time: next
free H-273, exp-251, BC-419, session-182); records are YAML-frontmatter Markdown
validated by `packing-ledger check`.

### H-264, Rewritten in Place

H-264 exists only on the stack, so it is an unlanded draft that conventions §7 lets be
rewritten. Its notes name `451154f60` as holding the previous text.
Keep the id, the question and the falsifier; change these fields:

```yaml
claim: >-
  On a seeded stratified draw of residue orbits on the H-266 unique-state cover at cap
  U = 1169/250 (survey_n17_residue's arity8 frame: the 2,256 orbits surviving the 90
  arity-at-most-8 selector flags; draw --sample 12 --seed 182), what fraction does the
  17-owner ownership-induction kernel at 32 bins exclude by a certificate the standing
  kernel verifier re-proves in full, at what producer, checker and verifier cost per
  state, and what does that extrapolate to over the frame's drawn strata?
instrument: >-
  devtools.check_n17_subpattern at the session-182 registration commit with N1's
  parameters (--bins 32 --max-rounds 24 --hull-limit 16 --max-seconds 7000, producer
  share 0.5, envelope core, collisions on); closures re-proved by
  devtools.verify_n17_kernel_certificate in full mode under the kernel-closed-covers
  listing or a later one; a float pre-screen by devtools.survey_n17_residue on the same
  draw
instrument_ready: true
regime: >-
  n=17; the H-266 unique-state cover at U; cap above S* so exclusions apply to every
  smaller side by the centred embedding. The draws at distance 4 or more from the
  endpoint's state are counted; the distance-2 draws are a declared secondary stratum,
  reported separately because such a state may be feasible at U. A draw the float
  pre-screen places leaves the count and is reported as a candidate near-endpoint state
  pending an exact check. A run that ends at its wall ceiling with process CPU below
  6,300 s is re-run once at the same ceiling and the re-run counts. A draw in N1's orbit
  takes N1's admitted receipt. Strata the draw does not reach (at review time, every
  distance-8-or-more stratum, 430 of 2,256 orbits) are reported as unsampled, not
  extrapolated.
cost_estimate: At most 7,000 s wall per state; with the endpoint control, at most 26 CPU-hours
prereqs: [H-266, H-267, think-e17c]
```

Notes to add: the falsifier is unchanged: fewer than half of the counted draws are
excluded within two CPU-hours each, with N1’s 7,000 s wall ceiling standing in for that
limit. The verdict is fixed as soon as the arithmetic determines it, and the remaining
runs continue for the cost estimate.
N1 and F1 (seed 168, the 44-flag frame) are prior evidence, not part of the count.
With seed 182 and sample 12 the draw is 2 states at distance 2, 7 at 4 and 3 at 6, so 10
are counted. The criterion is met at five closures and falsified at six non-closures.
The reviewer previewed this draw only to validate the command; no outcome was seen.

### Agenda Cells

Append to `agenda-042` under BC-418, as Session 167 did with BC-415 to BC-418, with
`parallel_group: n17-overnight-182` and `depends_on: [BC-418]`:

- **BC-419**, research, H-264, lane A: the question, budget and stop rules of lane A
  below; `next_evidence` the session-182 record.
- **BC-420**, research, H-267, lane K: the frozen recipe, the target filter, budgets and
  stop rules of lane K below.
- **BC-421**, research, H-273, lane E: added only when lane E launches.

### Beads and Views

- Create child beads of `think-tmz6` for lanes K, A, R, D and H (`tbd create`), each
  naming its write set, then `tbd start` and `tbd sync`.
- `packing-ledger render`; add this plan to `docs/project/document-map.yaml` and run
  `render_document_map`; idea-board rows only if a new H is registered.
- `packing-validate --records`, then `--push`, then push.

## Lanes

| Lane | Workflow | Model tier | Slots | CPU budget | Wall ceiling per job | Stop rule |
| --- | --- | --- | --- | --- | --- | --- |
| K, flag certification | W6 under H-267 | Opus, extra | 1, then 2 when slot 4 opens | kernel ≤ 17 CPU-h; branch and bound ≤ 14 CPU-h | 7,000 s per kernel target; 300 s per Knuth estimate; 5,400 s per certificate run | target list exhausted; a soundness alarm; one verifier FAIL stops admissions from that producer |
| A, per-state price | W6 under H-264 (rewritten) | Opus, high | 2 | ≤ 26 CPU-h | 2,700 s control; 7,000 s per state | all 12 draws run; a soundness alarm; the verdict stops nothing |
| R, capture route | W3 (lane R9) | Fable, max | none | reads only | 30-minute slices; about 3 hours | a written verdict of one of three kinds (below) |
| D, stall diagnosis | W3 | Fable, extra | short jobs at `nice -n 19` | ≤ 2 CPU-h | 1,200 s per diagnosis | every lane-K stall classified, plus C2 and C5 assessed |
| H, records and tools | W9 | Opus, high | none (tests only) | minutes | `--push` ceiling 1,800 s | H1 to H3 committed |
| E, near-endpoint sizing (backfill) | W6 under H-273 | Opus, high | freed slots only | ≤ 6 CPU-h | 3,600 s survey timeout per shard | all 95 orbits searched, or a placement found |

Slot policy: start with three compute slots (A, A, K). Open the fourth for lane K’s
branch and bound when the coordinator’s stack CI work is done, or when the load stays
below 3.5 for 15 minutes.
A freed slot goes first to lane K’s kernel queue, then lane A’s re-runs, then lane K’s
certificate runs, then lane E.

### Lane K: Flag Certification

**Question.** Do the standing flags with the most census weight close under the
adaptive-row kernel recipe that closed SW9, or under the branch and bound where its tree
is small enough to admit tonight?
Each closure is admitted by a standing verifier’s full pass, so it lowers the certified
census. Arity-7 closures also count toward H-267’s own criterion: at most $10^4$ orbits
under arity-at-most-7 certificates, against 17,690 after W7 and A.

**Inputs.** The census at the run worktree, written once at the start:

```bash
$PY -m devtools.census_n17_certified --output "$SCRATCH/s182/K/census-start.json"
```

**Kernel targets.** Arity at most 7, at least three wall or corner cells, best
penetration at least $5\times10^{-3}$ (the selector overstates penetration by 20 to 70
per cent, so lower values are likelier false), in projected-gain order.
The default receipts’ placed false flag is arity 8, so this filter excludes it without
lane H’s fix:

```bash
jq -r '.flagged_uncertified.classes
  | map(select(.arity <= 7
      and ([.cells[] | select(startswith("interior") | not)] | length) >= 3
      and .best_penetration >= 0.005))
  | sort_by(-.projected_gain.orbits) | .[] | .cells | join(" ")' \
  "$SCRATCH/s182/K/census-start.json" > "$SCRATCH/s182/K/kernel-targets.txt"
```

At review time this gives eight classes.
Six have three wall and four interior cells (side cells plus interior-SW, -NW, -W, -S)
and project 3,024, 2,883, 2,853, 2,794, 2,636 and 2,410 orbits.
Two have four wall and three interior cells and project 1,346 and 1,232. The file,
committed in the registration, is the frozen order.

**Frozen kernel recipe** (SW9’s, from `kernel-split-flag3-a9-bins64.json` and exp-250):

```bash
nice -n 10 timeout -k 120 7600 $PY -m devtools.check_n17_subpattern --cells $CELLS \
  --bins 64 --max-rounds 24 --hull-limit 16 --producer-share 0.6 \
  --split-floor 512 --max-rows 1152 --split-patience 1 --max-seconds 7000 \
  --save-objects "$SCRATCH/s182/K/objects/k$J" --output "$SCRATCH/s182/K/kernel-k$J.json"
```

**Control first:** the same command with `--pattern endpoint7 --max-seconds 3600` in
place of `--cells`. It must not close: the endpoint’s own west-wall cells are feasible
at $U$. A closure is a soundness alarm.

**On a closure** (`PASS_CERTIFIED_CLOSED`): move the seed and node into
`"$SCRATCH/s182-run/packing/campaign/explorations/X048-session-168-pilots/certificates/s182-k$J/"`.
The path is ignored, so the worktree stays clean for tracked files, and the receipt
names a repository path.
Then:

```bash
nice -n 10 timeout -k 120 4000 $PY -m devtools.verify_n17_kernel_certificate --progress \
  --output <dir>/verification.json <dir>
```

**On a stall:** hand the saved node to lane D. The coordinator deletes the node once
lane D’s receipts name its content id.
At most three undiagnosed nodes may be kept; beyond that the oldest is deleted, and its
receipt keeps the id.

**Branch-and-bound queue (slot 4).** First the controls and calibration:

```bash
# control: must never certify
$PY -m devtools.pilot_n17_subpattern_bb --cells side-N0,side-N1,side-N2,interior-W,interior-N,interior-E \
  --control --label control-endpoint-north --max-seconds 90 --output "$SCRATCH/s182/K/bb/control-north.json"
# calibration: A (41,598 nodes recorded) and W7 (did not close in 24 M native nodes)
$PY -m devtools.pilot_n17_subpattern_bb --cells interior-SW,interior-NW,interior-W,interior-S,interior-N,interior-SE \
  --estimate 150 --seed 1 --max-seconds 300 --label knuth-A --output "$SCRATCH/s182/K/bb/knuth-A.json"
$PY -m devtools.pilot_n17_subpattern_bb --cells corner-SW,side-N0,side-W0,side-W1,side-W2,interior-SW,interior-W \
  --estimate 150 --seed 1 --max-seconds 300 --label knuth-W7 --output "$SCRATCH/s182/K/bb/knuth-W7.json"
```

Route on the receipt’s mean estimate, not the median, which put W7 at $2\times10^5$. If
A’s mean misses 41,598 by more than a factor of three, stop routing and record the
estimator as miscalibrated.
Then run Knuth estimates (same flags, `timeout -k 30 420`) on the 34 flags with at most
two wall cells and on the eight kernel targets.
Certify, smallest mean first, every class whose mean is at most $1.5\times10^5$ nodes:

```bash
nice -n 10 timeout -k 120 6000 $PY -m devtools.pilot_n17_subpattern_bb --cells $CELLS \
  --max-seconds 5400 --label $L \
  --save-certificate "$SCRATCH/s182-run/packing/campaign/explorations/X048-session-168-pilots/certificates/s182-bb-$L" \
  --output "$SCRATCH/s182/K/bb/cert-$L.json"
nice -n 10 timeout -k 120 $((NODES * 56 / 1000 + 600)) $PY -m devtools.verify_n17_bb_certificate \
  --output <dir>/verification.json <dir>
```

The verifier timeout is 1.5 times 37.3 ms a node, plus 600 s. A tree of $1.5\times10^5$
nodes costs about 30 minutes to search in Python and 1.6 hours to verify, which is the
reason for the cap.

**Admission** (coordinator, per closure with a verifier PASS). Copy the certificate
directory into the session checkout at the same path.
From `packing/`, run
`python -m devtools.hosted_data stage --manifest hosted/n17-x048-session-168-certificates.yaml --from campaign/explorations/X048-session-168-pilots/certificates/<name>`;
that release has no assets yet, so its object list may grow.
Add the ledger entry to `certified-sub-patterns.yaml` (`status: admitted`, `evidence:`
the exp-251 record,
`verification: {receipt, verifier: kernel-streamed | bb-enclosure-retry}`). Run the
census and `hosted_data check`. Copy producer receipts into
`packing/campaign/explorations/X048-session-182-overnight/receipts/K/`.

**Outputs.** exp-251 (H-267), with the census before and after; the admitted entries;
the stage-updated manifest; the stall receipts for lane D. **Positive:** every closure
is a permanent exclusion of thousands of orbits.
Three or four arity-7 closures could decide H-267, after a W2 review.
**Negative:** stalls under adaptive rows on mixed arity-7 flags.
With lane D’s classification, that decides whether the next build is a producer split
policy or a branch predicate.

### Lane A: The Per-State Price

**Question.** H-264 as rewritten: do at least half of the counted draws close within the
7,000 s ceiling, and what does a closure cost?

**Steps:**

1. **Float pre-screen.** It also runs the endpoint’s positive control, which must place:

   ```bash
   nice -n 10 timeout -k 60 3900 $PY -m devtools.survey_n17_residue --flag-set arity8 \
     --sample 12 --seed 182 --workers 2 --timeout 3600 --output "$SCRATCH/s182/A/survey-seed182.json"
   jq -r '.states[] | "\(.index) \(.distance) \(.stratum) \(.mask) \(.cells | join(" "))"' \
     "$SCRATCH/s182/A/survey-seed182.json" > "$SCRATCH/s182/A/draws.txt"
   ```

   About 13 states at a median of 205 s each on two workers: about 25 minutes.
   Any state other than the endpoint’s that the survey places is a candidate
   near-endpoint state.
   Stop and tell the coordinator; the exact check is `diagnose_n17_flag check` on a
   placement receipt, or a W7 slice if the survey’s witness format is not accepted.

2. **Kernel control:** the endpoint’s own state (`.population.endpoint.state` in the
   survey receipt) with the command below at `--max-seconds 2700`. It must not close.

3. **Kernel runs, in the survey receipt’s random order** (`index`), two at a time:

   ```bash
   nice -n 10 timeout -k 120 7600 $PY -m devtools.check_n17_subpattern --cells $CELLS17 \
     --bins 32 --max-rounds 24 --hull-limit 16 --max-seconds 7000 \
     --save-objects "$SCRATCH/s182/A/objects/m$MASK" --output "$SCRATCH/s182/A/kernel-m$MASK.json"
   ```

4. **Each closure:** the standing verifier exactly as in lane K, then admission (each
   closed state removes its own orbit), with evidence the exp-252 record.

5. **Contended runs.** A run that hits its ceiling with `process_cpu_seconds` below
   6,300 is re-run once when a slot frees, as registered.

**Resume.** The kernel producer has no mid-run checkpoint, so the job is the unit: the
queue skips any draw whose receipt exists, and a killed job is re-run from scratch (at
most 2 hours lost).

**Outputs.** exp-252 (H-264), with a per-state table (distance, stratum, outcome,
rounds, rows, producer, checker and verifier seconds, process CPU, peak memory from the
watchdog log). The extrapolation is over drawn strata only; the distance-2 stratum is
reported separately.
**Positive (at least five of ten close):** the tail of 2,197 orbits is priced from
measured CPU, and flag certification becomes a cost choice.
**Negative (six or more fail):** per-state exclusion needs a grammar change (a branch
predicate or sub-cell seeds) before the tail is attacked, and flags carry the weight.

### Lane R: The Capture Route

**Question (lane R9, `think-g2qn`).** Pilot 2 met the after-pilot falsifier at round 17.
Was that another producer limit, and which one, or is n11’s capture architecture wrong
for n17?

**Inputs:** the pilot-2 receipts (`receipt.json`, `score.txt`, `partial.json`,
`rounds-14-17.log`); the capture feasibility, after-pilot, widened-projection scope and
local-radius reviews; the kernel adaptation spec; findings F3 to F5 of the Opus review.
The one sanctioned tool is `devtools.score_n17_capture`, for per-side extents.
A new measurement is specified for a later W7 slice, not improvised (OR-1).

**Exit, one of three:**

- **Producer-limited.** Name the limit (hull cap 48, the envelope or octagon core loss,
  partner pruning, or one-sided measurement) and write the pilot-3 settings and a
  sharper falsifier. Pilot 3 must start from round 0 with `--checkpoints`, since no
  checkpoint resumes (F3).
- **Architecture.** Write a candidate hypothesis for the widened projection theorem
  (mechanism, falsifier, expected information, limits) and the patch-count instrument’s
  contract: inputs, the dual-basis enumeration, the sample size fixed in advance, and
  its decision thresholds.
  It is built in a later W7 slice.
- **Undecidable from receipts.** Specify the single cheapest discriminating measurement.

**Output:** `docs/project/reviews/review-2026-10-05-n17-capture-r9.md` (dated by the day
it is finished), with an evidence-status table.
The coordinator codifies any candidate at the morning W10.

### Lane D: Stall Diagnosis

**Question.** For each lane-K stall, is the stall loss-limited or consistency-limited?
Loss-limited means some owner has a support share below 10 per cent and a median cut
margin above the run’s first-order losses at its finest row.
Consistency-limited means every owner is at least half supported.
Does flag 2’s reading generalise?

**Per node** (at `nice -n 19`, only while the load is below 4.5):

```bash
timeout -k 60 1200 $PY -m devtools.diagnose_n17_flag support NODE --samples 400 --refine 200 --seed 1 \
  --output "$SCRATCH/s182/D/support-$ID.json"
timeout -k 60 1200 $PY -m devtools.diagnose_n17_flag domains NODE --output "$SCRATCH/s182/D/domains-$ID.json"
```

**Output:** `docs/project/reviews/review-2026-10-05-n17-stall-classification.md`
(planning review), with receipts under
`packing/campaign/explorations/X048-session-182-overnight/receipts/stall-diagnosis/`. It
also assesses candidates C2 (aimed splits) and C5 (branch predicates) against the
classification, and states which build should come first.
Lane D writes no shared record.

### Lane H: Records and Tools

- **H1, census reads the recheck** (`think-gygy`). `census_n17_certified` accepts
  `n17-sub-pattern-recheck/v1` receipts (their `flagged` list is the still-flagged set)
  and defaults to `selector-recheck-90-seed1.json`. Test in
  `packing/tests/test_census_n17_certified.py`: the projection is 87 flags, 2,197 orbits
  and 17,168 states, the certified line is unchanged, and the endpoint survives.
  Measured for the review by converting the receipt in a scratch copy.
- **H2, a survey distance filter for lane E.** `survey_n17_residue --distance D`
  restricts the frame to one distance and `--sample 0` takes every orbit in it, with a
  test in `packing/tests/test_survey_n17_residue.py`. The run worktree’s frozen copy is
  unaffected.
- **H3, the X-048 addition.** Apply the Opus review’s fixes to the W3 draft (F4, F5, F6,
  F13 to F19 at least), then integrate it into
  `packing/campaign/explorations/X-048-n17-optimality-after-n11.md` by addition:
  `sources`, and `proposes` with H-261 to H-268 (plus H-273 if registered).
  Run a `pprose-common-edit` pass (OR-7).

**Write set:** the two tools, their tests, and X-048. Validation: `--edit` while
editing, and tests reachable from the diff (`--push`) before handing back.
The coordinator commits.

### Backfill: Lane E, Near-Endpoint Sizing

Launch only when H2 has landed and a slot is free.

**Registration** (coordinator, its own commit before the run):
`packing/campaign/hypotheses/H-273-n17-distance-two-infeasible-at-cap.md`.

- **Claim:** each of the 95 distance-2 orbits of the 2,256-orbit frame is infeasible at
  $U$.
- **Falsifier:** an exact placement at $U$ of any of them.
- **Instrument:** `survey_n17_residue --flag-set arity8 --distance 2 --sample 0` with
  its default full rounds.
- **Limits:** float search can refute the claim but never confirm it.
  Its candidate form is C1’s first half (F14).

Add BC-421 and an idea-board row.

**Run:** `--workers 2 --timeout 3600` in shards of 30 orbits, about 5.4 CPU-hours (95 ×
205 s).

**Positive (a placement):** the near-endpoint stage is non-empty and the composed
argument needs exclusion at $U'$. **Negative:** “no placement in N searches”, recorded
as unresolved.

## Machine Budget and Guards

| Resource | Allocation | Guard |
| --- | --- | --- |
| CPU | at most 4 compute processes at `nice -n 10`, plus short lane-D jobs at `nice -n 19` while load is below 4.5 | pause lane K’s branch-and-bound queue (never kill a running target) if load stays above 6 for 15 minutes |
| RAM | budget 3 GB per producer; the self-check peaked at 1.23 GB on flag 2, the streamed verifier at 0.2 to 1.0 GB | the watchdog kills any job above 5 GB; below 1.5 GB available, stop launching |
| Disk | worktree about 1.2 GB; objects at most about 3 GB (closed states about 26 MB each; certificates up to about 200 MB) | below 2.0 GB free, stop launching; below 1.0 GB, kill the newest job and delete its partial objects |
| Wall | ceilings per job as tabled; validation tiers at their development.md ceilings (`--records` 300 s, `--push` 1,800 s) | the full checkpoint (3,600 s ceiling) does not run on this host while compute runs; the session is marked pending certification |

Every compute job writes its own receipt; every queue skips jobs whose receipt exists,
which is the resume mechanism for jobs of at most two hours.
No job tonight runs longer than two hours in one process; capture is the only
computation that would, and it is not scheduled (see Not Tonight).

## Records, Branching and Validation

- **One session PR**, `claude/n17-session-182-overnight` stacked on #360
  (`github-stacked-prs` is granted), opened with `tbd shortcut
  create-or-update-pr-simple`. The body leads with what the branch cost (OR-9).
- **Commit order:**
  1. the registration;
  2. lane H’s tool commits;
  3. one commit per admission (receipts, ledger entry, manifest, census);
  4. if `release_pin --check` reports the data changed, `release_pin --update` alone in
     the next commit;
  5. exp-251 and exp-252 when their rounds close (allocate in the order the records are
     written);
  6. lane R’s and lane D’s reviews;
  7. X-048;
  8. the handoff commit: the session record checkpoint, the SYNOPSIS handoff,
     `close_session --render` and `packing-ledger render`.
- **Before every push:** `packing-validate --records`, then `packing-validate --push`.
  Push at the first commit worth a hosted run and read CI receipts at the next check-in,
  never by polling (OR-3).
- **Bulk data (OR-18):** certificate objects never enter Git.
  They stay in the session checkout’s ignored certificates folder and are listed in the
  manifest. Publishing is the owner’s, later (`think-jhgi`); this environment’s egress
  refuses uploads. Stall nodes are never committed.
- **Admission (OR-16 as amended):** a standing verifier’s full pass under a listing that
  admits new entries (`kernel-closed-covers` or later; `bb-enclosure-retry`), run from
  the clean run worktree.
  No per-certificate review is needed, per exp-250’s precedent.
  A verdict change on H-264 or H-267 gets a W2 review before X-048 or the frontier says
  so.
- **Sub-agent briefs** must carry: the Python 3.14 rule; OR-16 and OR-18 (data and
  verifiers); the write set; “report commands run and their results, with paths and
  content ids”; no commits or pushes; and the model and thinking level (OR-2).

## Check-ins, Abort Conditions and Continuity

**Continuity (OR-8).** One-shot `send_later` pings every 30 minutes, with a recurring
Routine at the shortest interval the project allows (normally hourly) as the floor.
Deleting that Routine needs the owner’s request.

**Each check-in, in this order:**

1. Clock against the morning checkpoint.
2. `uptime`, `free -m`, `df -h /`.
3. `ps -eo pid,etime,rss,args | grep devtools` against each lane’s queue.
4. New receipts, and the outcome line of each.
5. Soundness alarms (below).
6. Admit closures with a verifier PASS.
7. Commit and push coherent work, at least every four hours (OR-6).
8. Re-plan only future slices: never a frozen criterion, never a running job’s ceiling.

**Abort conditions:**

- **Soundness alarm, stop the instrument at once:** the kernel closes the endpoint’s
  state or `endpoint7`; the branch and bound certifies an endpoint control; a census
  reports the endpoint not surviving.
  Preserve every object, record a defect, admit nothing from that instrument, and
  escalate to the owner in the handoff.
- **Verifier FAIL** on a producer closure: no admission.
  Stop admissions from that producer until a review; other lanes continue.
- **Three consecutive crashes or refusals** of one instrument stop that instrument.
- **Resource guards** as tabled.
  A resource kill is recorded, never read as an outcome.
- **Another agent’s changes** in a checkout this plan uses: preserve them and
  re-establish a clean checkout before writing.

## Morning Handoff

At 14:30 UTC the coordinator writes, and commits with the session record, a handoff that
leads with what changed scientifically:

- The certified census before and after (states, orbits) and each admission with its
  verifier receipt. Lane K’s kernel and branch-and-bound outcomes per target, and H-267’s
  arity-7 count.
- H-264: the per-state table so far, the verdict if determined, and the extrapolation
  over drawn strata.
- Lane R’s verdict and lane D’s classification, each with the next build it selects.
- Costs: CPU-hours per lane, agent time per lane, and what is still running, with each
  job’s expected end.
- Decisions for the owner: the R9 route; uploading the manifest’s objects; merging the
  stack (`github-merge` is `confirm-session`); whether to let the run continue.
- Beads updated, the PR link, CI status and the gate declaration (pending certification
  unless a full checkpoint ran).

The run does not stop at the handoff unless the owner says so (OR-8).

## Not Tonight

| Item | Reason |
| --- | --- |
| Capture pilot 3, or continuing pilot 2 with the hull cap lifted | No checkpoint resumes here (`partial.json` is a partial receipt, and a changed `hull_limit` is refused); a rebuild is about 9.7 hours in one process to round 17. Lane R9 chooses the producer change first. |
| R9’s “exact LP” half | The after-pilot probe already shows zero first-order extent at $\varepsilon = 0$, and the kernel spec gives the $U'$ radius; it would decide nothing. |
| Building the dual-sheet patch counter | No instrument exists on any ref; it needs lane R’s contract, a W7 build and a review. |
| Resuming the residue-universe sweep | Chunks 0 to 60 were in another container and were never committed, so `sweep` would restart at chunk 0. 787 CPU-hours remain, and its falsifier is met so far (39.3% < 50%). |
| #350’s native kernel | Buildable here (rustup has 1.98.0 with clippy and rustfmt; the crates are cached), but the native path writes no certificate. Admission is verifier-bound at 37.3 ms a node, so Python search covers every tree that can be admitted tonight. It would also need its own worktree (about 1.1 GB). |
| F2’s verifier rewrite, a branch-predicate grammar, the compiled kernel backend | Each is a multi-slice build with a review. |
| Publishing hosted data, the R071 replay | Egress refuses uploads; R071 needs Boost and moves no n17 bound. |
| The composed argument | It waits on the capture route and the near-endpoint stage. |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
