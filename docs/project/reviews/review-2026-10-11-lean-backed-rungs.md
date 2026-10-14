# The Lean-Backed Claims Against the Rung Predicates: `T-060`, `T-084`, `T-055` and `T-120` to `T-124`

**Verdict: no entry can move today, and the pieces that would move each are named.**
Every Lean formalization the record knows of is linked and pinned: Ahmed’s
11SquaresOptimal and 11SquaresFormalized on `T-060`, chelokot’s archive on `T-084` and
`T-086`, wand125’s overlay on `T-055`, and Evan Daniel’s `Packs` modules, committed on
11 October, for the exact forms of `T-120` to `T-123`. Under the predicates of
[epistemics.md](../../../epistemics.md#verification), a formalization moves nothing by
itself: `V4` and `C4` do not mention one, and `V5` and `C5` count one only with a
passing build the record holds and a human expert’s review of the formal statement.
For every entry here the build the record holds is missing, reported, or not yet
registered, and no human expert’s formalization review and no human oversight record is
retained anywhere in the register.
The statement closure of the `n = 11` formalization was built again here today at the
pinned toolchain and gave the receipt of 6 October (§5); the full proof was priced and
not built. Twelve findings are recorded, `LR-1` to `LR-12`; the three marked blocking
block a rung, not the record as it stands.

This is lane R2 of the 2026-10-11 intake pass (epic `think-mq0k`, bead `think-66e5`),
written by an AI agent (Claude, at maximum reasoning effort) prompted separately from
the import, replay and records lanes.
It registers nothing, moves no rung and edits no register; §8 is what the records lane
would change and §9 what only the owner can decide.
It is not an adversarial review of any of the proofs, and it is not a human record of
any kind.

## 1. What Was Checked

| Source | How |
| --- | --- |
| The predicates | [epistemics.md](../../../epistemics.md): No Blind Trust, Verification, Confirmation, Review Records, Scope and Composition, Enforcement; [results.schema.yaml](../../../packing/frontier/results.schema.yaml) `review` and `open_review`; the ladder plan’s open decisions 11, 13 and 15 |
| The derivation | [`devtools/check_results.py`](../../../packing/devtools/check_results.py): `_machine_proof_shaped`, `_formal`, `adversarially_reviewed`, `overseen`, `formalization_reviews`, `derive_verification`, `derive_confirmation`, `review_problems`; [`result_status.latest_review`](../../../packing/devtools/result_status.py) |
| The entries | `T-060`, `T-055`, `T-084`, `T-086`, `T-006`, `T-112`, `T-120` to `T-124` in [results.yaml](../../../packing/frontier/results.yaml); their Lean evidence in [evidence.yaml](../../../packing/frontier/evidence.yaml); [n-011.md](../../../packing/frontier/n-011.md) |
| The `n = 11` formalization | The [6 October packet](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/README.md), its receipts, the source’s `summary.json`, `docs/VERIFICATION_20261006.md`, `docs/UBUNTU_RUNNER.md`, `MISSING.md`; the [statement audit](review-2026-10-06-n11-lean-formalization-statement-audit.md) and the [adversarial review](review-2026-10-06-n11-lean-formalization-adversarial.md) of 6 October |
| Upstream, read-only, 2026-10-11 20:38 to 20:52 UTC | GitHub’s API through `gh api`: the two repositories of Queuingtheorydotcom and the user’s repository list; EvolvingPrograms/11SquaresEvolving; evand/square-packing at `6bbae379` and `main`; jlevy/squares#419 comment 6104596297; wand125/square-packing-bounds at `781afb3` and `main`, wand125/square-packing, wand125/n11-optimality-lean; chelokot/square-packing-archive at `753079eb` and `main` |
| Run here | `devtools.audit_n11_lean stage` and `build` on the packet’s retained bytes (§5), with elan, Lean `v4.34.1` and Mathlib `d13f23b7`’s cache fetched for the closure’s 22 Mathlib imports only |

Not done: no full Lean proof was built, no author’s script was run, nothing was fetched
from the private repository of §2.3 beyond the API’s metadata, and no review of the
mathematics was repeated.

## 2. Upstream State on 11 October

### 2.1 Queuingtheorydotcom

The author has two public repositories and no other.
Neither states a licence.

- **11SquaresFormalized** is unchanged: `main` is `cdc746ed`, the pin, pushed
  2026-10-06T05:23:46Z. Its sixteen branches and twenty-one tags all predate the pin
  (the last tag, 2 October).
  No build receipt, axiom audit or `native_decide` count has changed past the pin,
  because nothing has.
- **11SquaresOptimal** is three commits past the `f9e0de7` pin of `T-060`: `2e4c4cd` and
  `f49664b` of 8 October and `4262f07` of 9 October, which touch `README.md` and
  `paper/` only (the synthesis manuscript, its SHA-256 list and publication archive).
  [intake-watch.yaml](../../../packing/campaign/intake-watch.yaml) already records them
  under `think-3i74`, which owns the independent validation of the proof; nothing there
  is Lean.

### 2.2 The Other Lean Sources

- **evand/square-packing** `6bbae379` (2026-10-11T02:23:00Z) commits
  `lean/Sqpack/Exact/Packs/`: 258 modules `Sqpack.Exact.Packs.N<n>`, one per exact form
  with field degree at most 20, each proving
  `packs : ∃ s : ℝ, peval pS s = 0 ∧ Sa ≤ s ∧ s ≤ Sb ∧ Packs n s` by `decide +kernel`,
  with `SHA256SUMS` and a README; the 62 quadratic sides also get `packs_closed` and
  `minSide_le_closed`. The author’s
  [comment on #419](https://github.com/jlevy/squares/issues/419#issuecomment-6104596297)
  of the same minute says every theorem prints the three standard axioms, that the
  rebuild cost about ten process-hours in all (14 s to about 5 min per count), and that
  the eleven forms of field degree above 20 have no Lean.
  The build pins are Lean `v4.33.1` and Mathlib `0df444a3`, the pins of the `s(13) = 4`
  and Bentz-4 builds already made here.
  Among the four new forms of #419, only `n = 102` (`T-120`, degree 8) has a module:
  `N102.lean` with `N102/Data.lean` (122,693 bytes) and five chunk modules, 125 s at the
  source. `n = 106`, `152` and `177` (`T-121` to `T-123`, degrees 32, 40 and 32) do not.
  `main` is `675a5ea` (16:34Z); the commits after `6bbae379` merge wand125’s Valid7
  kernel check (`s(k² − 3) = k` for `k ≥ 6`, PR #6 there), which is outside this lane
  and belongs to the evand watch (`think-jtlq`).
- **wand125/square-packing-bounds** was archived on 7 October at `069f327`; its content
  moved to wand125/square-packing (`04fbef0`, 2026-10-11T11:29Z), whose `MOVED.json`
  maps every old path.
  The `s(21) = 5` Lean work stays readable at the old commits: `point_n21_L5/lean/` (the
  conditional overlay of `b64f96e6`, retained in the
  [28 September packet](../../../packing/resources/web/wand125-point-and-mixed-2026-09-28/README.md))
  and `point_n21_L5/lean/zero-margin/` (the hypothesis-free `n21pts_eq_5` of `77636c63`,
  five small files, not retained here).
  wand125/n11-optimality-lean is unchanged since 30 September (`ee96259`) and is moving
  to `lean/n11-optimality/` of the new repository.
- **chelokot/square-packing-archive** is at `e1e9ef5` (2026-10-07T09:01Z), Apache-2.0.
  The 7 October commits move the small results to Bend; `NagamochiPackingTheorem.lean`
  at `main` is blob `da209bad`, the pinned `753079eb` blob, and the toolchain is still
  `leanprover/lean4:v4.33.0`.

### 2.3 The Source Repository of the `n = 11` Run Is Now Visible to the Owner

On 6 October the API answered 404 for EvolvingPrograms/11SquaresEvolving and for run
37414883750, so the formalization was recorded as the source’s report
(`E-n011-lean-formalization-report`). Today the owner’s GitHub token sees the
repository, with `admin`, `maintain`, `push` and `pull` permission.
It is private, since renamed SquaresLean, and the run is inspectable: workflow “Verify
simplified proof”, manually dispatched, `completed` with conclusion `success` on
`1bf942a7`, 2026-10-06T04:41:17Z to 05:00:52Z, and its three artifacts are not expired:
`proof-checkpoint` (7,942,182,870 bytes, until 2026-11-05), `proof-diagnostics`
(7,381,409 bytes, until 2026-11-05) and `proof-evidence` (2,005,620 bytes, until
2027-01-04). The repository is active, with at least thirty commits between 7 and 11
October, an `n = 11` comparator workflow, an `n = 12` formalization effort and this
repository added as a submodule; a verification run was in progress at 19:21Z today.

Nothing was downloaded from it.
What this changes is the owner question of the adversarial review of 6 October (its
finding 1): the owner can now read the run’s logs and audit himself.
§9 says what follows.

## 3. The Predicates Against Each Entry

What each rung needs, read from epistemics.md and the checker, in the same words:

- **`V3`:** machine evidence of any origin (`exact-algebraic`, `interval-certified` or
  `proof-assistant-checked` with a certificate, a replay command and
  `replay_status: passed`), or a published or audited proof.
- **`V4`:** `V3` machine evidence, two retained adversarial AI reviews by distinct
  reviewers in the result’s `reviews`, the latest-dated review accepting, and one human
  oversight record (`kind: oversight`, `reviewer_kind: human`, `checked` including
  `trust-boundary`, `certificate-meaning` and `ai-findings`). A formalization plays no
  part.
- **`V5`:** a `proof-assistant-checked` entry of any origin with certificate, replay,
  `replay_status: passed` and `axioms_receipt`, plus one formalization review
  (`kind: formalization`, `reviewer_kind: human`, `independent_of_author: true`,
  `checked` including `statement-fidelity`, `definitions`, `axioms` and `build`,
  accepting). One review is the checker’s provisional count (decision 15 of the ladder
  plan is open).
- **`C3`, `C4`:** the same as `V3` and `V4` on confirming-origin evidence
  (`audited-here`, `replayed-here`, `independently-external`) and reviews with
  `relation` other than `source`; `C` never exceeds `V` from `C2` up.
- **`C5`:** the formal entry with `origin: replayed-here`, an `open_review` record
  (`sources`, `terms`, `replay`, `retained`) and two formalization reviews by distinct
  named experts.
- **Composition:** an equality takes the `C` of its lower half; a compound claim the
  minimum of its parts.

### 3.1 `T-060`, `s(11) = T` (`V3/C3`)

| Piece | State |
| --- | --- |
| Machine evidence | `E-n011-global-optimality-independent` (exact-algebraic, `audited-here`, passed): `V3` and `C3` |
| Adversarial AI reviews in `reviews` | One: GPT-6 Astra, 2026-09-29, accepted |
| Adversarial AI reviews retained but not in `reviews` | GPT-6 Pro’s unified review of 2026-10-03, which `T-112` lists as `accepted` with `relation: project`; the 2026-10-03 paper review by Claude Code (“no mathematical error”); the 2026-10-06 Lean import review by Claude Opus 5.5 (`defect-open`, each finding dispositioned in the statement audit §9); the 2026-10-07 paper review adjudicated by GPT-6 Astra Pro |
| Human oversight record | None |
| Formal evidence | `E-n011-lean-formalization-report`: `assurance: reported`, `origin: external`, `replay_status: not-attempted`, with an `axioms_receipt`. `_formal` is false, so it counts toward neither rung. `E-n011-lean-statement-closure-build` (`replayed-here`, passed, standard axioms) is the upper half only and is cited by the case record, not by `T-060` |
| Formalization review by a human expert | None |
| `open_review` | None; and the source states no licence, so `terms` has nothing true to say (`LR-6`) |

Supported now: `V3/C3`. For `V4` and `C4` the record lacks a second review entry and the
oversight record. GPT-6 Pro’s review of 3 October is recorded on `T-112` as accepted.
It names Astra’s review of 29 September as a source (its R4), so whether it counts as a
distinct reviewer under epistemics.md (“no shared context”) is the owner’s decision,
which the oversight record states (`LR-3`). For `V5` it lacks a build the record can
rest on and the expert review (`LR-4`); for `C5`, the build must be `replayed-here`, the
terms must exist and two experts must sign.

### 3.2 `T-084`, `s(k² − 1) = k` (`V3/C3`)

| Piece | State |
| --- | --- |
| Machine evidence | `E-karakus-strip-measure-interval` (interval-certified, audited here) for Proposition 5.1; the rest read |
| Adversarial AI reviews | One, 2026-10-06, accepted |
| Formal evidence | chelokot’s `Records.NearSquare.squareMinusOne_isMinimumSide` was compiled here on 2 October inside the `T-086` replay, and the archive’s `Audit.lean` printed its axioms as `propext`, `Classical.choice`, `Quot.sound` ([`build.log`](../../../packing/campaign/series/series-000-smoke-and-calibration/results/chelokot-lean-replay/build.log) line 218); the receipt and its `ReplayAxioms.lean` name `squareMinusTwo` only, no evidence entry cites it, and no statement reading of it is retained (`think-5i1z`) |
| Oversight, formalization review, `open_review` | None |

Supported now: `V3/C3`. `V4`: a second adversarial review and the oversight record.
`V5`: the Lean route registered as a `proof-assistant-checked, replayed-here` entry with
its own axiom receipt, and a human expert’s reading that `IsMinimumSide (k·k − 1) k`
over chelokot’s `Packing` is this record’s `s(k² − 1) = k`; the formal route is then
chelokot’s proof beside Karakuş’s, and the composition note must say so.
`C5`: the replay is already here; add `open_review` (public, Apache-2.0, the pinned
commit) and a second expert.

### 3.3 `T-055`, `s(21) = 5` by points only (`V3/C3`)

| Piece | State |
| --- | --- |
| Machine evidence | `E-n021-wand125-point-endpoint-source-replay` (exact-algebraic, `replayed-here`, the source’s runner): `V3/C3` |
| Adversarial AI reviews | One, 2026-09-28, accepted |
| Formal evidence | The conditional overlay `n21pts_eq_five_of_checker : N21PtsCheckerCover → minSide 21 = 5` is retained and was never built here (the 29 September receipt ends `LEAN_OVERLAY_PREFIX_OK_LAKE_NOT_RUN`); the hypothesis-free `n21pts_eq_5 : minSide 21 = 5` of `77636c63` is not retained (`think-f2bm`) |
| Oversight, formalization review, `open_review` | None |

Supported now: `V3/C3`. `V4`: a second adversarial review and the oversight record.
`V5`: retain `zero-margin/` (stage 2), build it here or retain a third party’s build,
and a human expert’s review.
`C5`: the build here, `open_review` (MIT, the archived repository at its commits) and a
second expert. The conditional overlay cannot carry `V5` on its own: its hypothesis is
the checker’s run.

### 3.4 `T-120` to `T-124`, Evan Daniel’s exact forms and local minima (`V0/C0`)

| Entry | Lean at `6bbae379` | Supported now | With the module built here |
| --- | --- | --- | --- |
| `T-120`, `n = 102` | `Sqpack.Exact.Packs.N102.packs`, degree 8, 5 chunks, 125 s at the source | `V0/C0` | `V3/C3` on a `proof-assistant-checked, replayed-here` entry, for the bound and the root identity; the source’s minimality assertion stays unestablished (Lean proves no irreducibility) and the claim must keep the two apart |
| `T-121`, `n = 106`; `T-122`, `n = 152`; `T-123`, `n = 177` | None (field degree 32, 40, 32) | `V0/C0` | Unchanged; their `C3` route is `verify_exact.py` replayed here (exact-algebraic), owned by `think-63vx` |
| `T-124`, 178 local minima | The `IsLocalMinPacking` statements (`N11L`, `N28L`, 176 band lemmas) were already in the tree the 7 October packet retains; `6bbae379` adds nothing to them | `V0/C0` | Not priced: no build figure is retained, and the source’s `n = 28` figures are reports |

`V4` and `V5` for `T-120` then need what every entry needs: two adversarial reviews, the
oversight record, the expert review; `C5` adds `open_review` (MIT) and a second expert.

## 4. What `native_decide` Means for the Axiom Receipt

`V5`’s predicate asks for an `axioms_receipt`; the checker reads only that the field
names a path. The receipt of the `n = 11` formalization
([`axioms-public-theorems.json`](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/lean/axioms-public-theorems.json))
lists, for `ElevenSquare.optimality`, the three standard axioms and 13,308 axioms of the
form `<declaration>._native.native_decide.ax_<i>_<j>`, one per proposition that a
`native_decide` call evaluated with compiled code and the kernel never checked.
The theorem therefore trusts Lean’s compiler, code generator and runtime as well as its
kernel; the source names this trust model, `lean_kernel_and_native_compiler`, and says
it is not a kernel-only verification.
The record already treats it that way everywhere it mentions the formalization
(`README.md`, `SYNOPSIS.md`, `n-011.md`, the entry’s `assumptions`, the packet, the
statement audit §3), and never writes “standard axioms only” of the full theorem.

epistemics.md has no rule about compiler trust: neither the predicates nor the evidence
schema distinguish a kernel-only receipt from one with native axioms, and nothing bars
the second from `V5`. Where the distinction lives today is the formalization reviewer’s
`axioms` check, which a human must accept explicitly, and in prose.
By contrast every other Lean receipt on the record is kernel-only: chelokot’s, Daniel’s
`s13_eq_4` and Bentz-4 builds, wand125’s overlay and the new `Packs` modules all print
the three standard axioms and use `decide +kernel` where data is involved.
Whether `V5` or `C5` may rest on a compiler-trusting proof, and whether the trust model
should be an attribute shown beside the rung as the distinct-method count is, is the
owner’s (§9, D4). The 13,308 count itself cannot fall without a new commit of the
source, and none exists.

## 5. The Price of a Lean Replay Here, and the Build Made Today

| Build | Pins | Price | Feasible on this host (4 shared cores, 15 GB, no swap, about 7 GB free) |
| --- | --- | --- | --- |
| `n = 11`, the whole proof: 7,920 modules | Lean `v4.34.1`, Mathlib `d13f23b7` | No cold-build time is on record anywhere. The source’s workflow runs `scripts/run_verification.sh --bootstrap --jobs N` on a GitHub runner in resumable jobs under a 4 h 45 min limit, modules compiling serially; the passing run of 6 October used a 64-worker runner and resumed from a checkpoint, 19.5 min of wall; the compiled objects are 7.94 GB beyond Mathlib’s cache of about 7 GB; the author’s “2–3 hour macOS” figure is a target, not a measurement (`MISSING.md`) | No. Disk alone rules it out; a cold build would take days at `--jobs 2`. The cheapest route the record could hold is a fork of the public pin dispatching the source’s own workflow on GitHub-hosted runners, `--jobs 2`, resumed across jobs, with the final audit, logs and axiom report retained here; count unknown until the first job reports its throughput |
| `n = 11`, the statement closure: 18 modules and the probe | the same | Today: elan and the toolchain 54 s; Mathlib’s cache for the closure’s 22 imports only (1,697 files; the whole cache is about 7 GB and did not fit the disk) 1 m 44 s; the build, see below | Yes, done |
| `T-084`, chelokot’s archive, 277 modules | Lean `v4.33.0`, Mathlib `db584cd6` | About 53 min from source over Mathlib’s cache on 2 October, plus the cache fetch; 52 s to rebuild the four modules over a warmed tree. Extending `replay_chelokot_lean` to name `squareMinusOne` is an hour of lane work | Yes, about an hour, several GB |
| `T-055`, wand125’s hypothesis-free proof: 64 generated parts | Lean `v4.33.1`, Mathlib `0df444a3`, evand `6aa82ba4` | At the source on an M4 under load: generation 1,459 s with 6 workers, the kernel check about 3.5 h of wall with two parts at once near 6 GB each; the generated data is 88 MB and not distributed | One part at a time to fit memory: about 6 to 8 h of wall, 8 GB of disk; not now |
| `T-055`, the conditional overlay | the same, evand `6e1223cf` | About 24 min and 8 GB on an M4 | Yes, but it moves no rung |
| `T-120`, `Sqpack.Exact.Packs.N102` | Lean `v4.33.1`, Mathlib `0df444a3` | 125 s at the source in five 25-square chunks; counts whose 25-square chunks exceeded 14 GB were only `n = 129` and `146`, so `n = 102` should fit; the cache is about 7 GB, which does not fit beside today’s | About an hour of lane work and under ten minutes of build, after a staging tool with blob checks like `stage_evand_bentz4_lean` |

**The statement closure built again today.** `devtools.audit_n11_lean stage` wrote the
18 modules, the three pins and the probe from the packet’s retained bytes, which
`acquire_source --check` holds to the upstream manifest; `devtools.audit_n11_lean build`
then built them one module at a time in import order with `nice -n 10` and
`LEAN_NUM_THREADS=2` on a host whose load average was above 9 throughout, and ran the
probe. All 18 modules built with exit 0 and the probe elaborated without error, from
20:56:37 to 21:15:44 UTC: 19 min 7 s of wall and 9 min 22 s of CPU, against the 7.6 min
of wall of 6 October, the difference being the host’s load and not the build.
The same six theorems, `construction_packable`, `u_unique`, `T_lt_U`,
`optimality_of_lower_bound`, `improvement_within_cover` and
`packing_has_canonical_mask`, print `[propext, Classical.choice, Quot.sound]`. The
receipt is retained in the packet as
[`receipts/lean/build-statement-closure-2026-10-11.log`](../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/lean/build-statement-closure-2026-10-11.log).
It is the definitions and the upper half, says nothing about the lower bound, and moves
no rung; it shows that the replay command of `E-n011-lean-statement-closure-build` is
live. The wall passed the fifteen-minute ceiling this lane was given, since the priced
figure was measured on a quieter host; the build ran at `nice -n 10` throughout.

## 6. The Derivation Code and the Fields a Promotion Needs

`derive_verification` and `derive_confirmation` in `check_results.py` are the predicates
of §3 word for word: `V5` is `_formal` on any cited entry and
`formalization_reviews ≥ 1`; `V4` is `_machine_proof_shaped` on any entry and
`adversarially_reviewed` (two distinct `reviewer` strings among `kind: adversarial,
reviewer_kind: ai`, and `latest_review` accepting, the last-listed winning a date tie)
and `overseen`; `C5` filters to `origin: replayed-here`, requires `open_review` without
structural faults and two formalization reviewers with `relation` other than `source`;
`C4` and `C3` filter to the confirming origins.
`_formal` is `_machine_proof_shaped` plus `axioms_receipt`, and `_machine_proof_shaped`
needs `replay_status == "passed"`, which is why the `reported` entry on `T-060` cannot
reach `V5` whatever review is added.
`review_problems` checks each review’s path, its row in
[document-map.yaml](../document-map.yaml), its kind, date, relation and `covers`, and
the `open_review.retained` path; it does not tie a formalization review to the evidence
entry it reviews (`LR-7`).

What `T-060` would need in the record:

- **`V4` and `C4`:** in `results.yaml`, a second `reviews` item of `kind: adversarial`
  with a distinct `reviewer`, an accepting `verdict` and `covers` naming `T-060`, the
  document mapped as a non-superseded `review`; one item of `kind: oversight`,
  `reviewer_kind: human`, `relation: owner` (or another named person), `checked:
  [trust-boundary, certificate-meaning, ai-findings]`, `verdict: accepted`, whose
  document under `docs/project/reviews/` says what was inspected; the latest-dated item
  must accept; then `verification: V4`, `confirmation: C4`, a dated `notes` line and a
  rewritten `next_rung`, since `rung_label_problems` refuses stale rung prose.
- **`V5`:** in `evidence.yaml`, an entry with `method: proof-assistant-checked`,
  `assurance: verified`, `certificate`, `replay`, `replay_status: passed`,
  `axioms_receipt`, `verifiers`, a `proof` block and `limitations`, of origin
  `replayed-here` or `independently-external`, or the `E-n011-lean-formalization-report`
  entry re-encoded under the owner’s ruling (§9, D1); in `results.yaml`, `T-060` cites
  it, and `reviews` gains an item of `kind: formalization`, `reviewer_kind: human`,
  `independent_of_author: true`, a `relation`, `checked: [statement-fidelity,
  definitions, axioms, build]`, `verdict: accepted`; then `verification: V5`.
- **`C5`:** the entry’s origin `replayed-here`; `open_review: {sources, terms, replay,
  retained}` on the result; a second formalization item by a distinct named reviewer;
  then `confirmation: C5`.

## 7. Findings

- **`LR-1`, not blocking: the author’s repositories are linked, pinned and unchanged
  where it matters.** 11SquaresFormalized has no commit past the pin; 11SquaresOptimal’s
  three later commits are the manuscript and are already watched under `think-3i74`.
  Nothing new to import from either.
- **`LR-2`, not blocking, an owner matter: the private source repository and run are now
  visible to the owner** (§2.3). Its run logs and artifacts could make the report
  entry’s `assumptions` a record of what the owner read, and its `proof-diagnostics` and
  `proof-evidence` artifacts are small enough to retain; the repository states no
  licence and is private, so retention needs the author’s consent and stated terms.
  Owner: `think-8spq` (the import of the formalization).
  The `n = 12` and comparator work there is not for this lane; the coordinator may want
  a watch row, since the register holds no `n = 12` formalization.
- **`LR-3`, blocking for `V4` and `C4` on `T-060`: the second adversarial review exists
  and is not recorded.** `T-060`’s `reviews` holds Astra’s review of 29 September;
  `T-112` already records GPT-6 Pro’s review of 3 October as `accepted`,
  `relation: project`, and that review is of `T-060`’s proof and paper.
  It names Astra’s review of 29 September as a source (its R4, “Mathematical acceptance
  and dependency contract”, which it cites eleven times), so whether it counts as a
  distinct reviewer under epistemics.md (“a separately prompted independent lane with no
  shared context”) is the owner’s decision, which the oversight record states (D2), as
  `RR-1` of the sibling rungs review asks for fourteen entries.
  If the owner rules it distinct and it is recorded on `T-060`, the oversight record is
  the only other piece `V4` needs, and no outside expert is needed for it.
  `C4` then follows, since the machine evidence is `audited-here` and every review is
  project-side.
- **`LR-4`, blocking for `V5` on `T-060`: no build the record holds.** The formal entry
  is `reported`; `_formal` fails on `replay_status`. Three routes: a third party’s
  complete build retained here (`independently-external`; Julian-JJ’s HPC run and
  wand125’s and Guzhou0806’s component checks are named in the source’s
  acknowledgements, and none is published); the fork-dispatched run of §5, which is this
  project’s replay from the public pin and could serve `C5` as well; or the owner’s
  ruling that the source’s own run, which he can now inspect, counts toward `V` (D1),
  which the import process and the frontier README would have to say first.
  Then the human expert’s formalization review (D3), outside the owner’s gift.
- **`LR-5`, not blocking: `native_decide` is disclosed and unregulated** (§4). No
  wording in the record overstates the trust model.
  D4 asks whether the ladder should.
- **`LR-6`, blocking for `C5` on `T-060`: the source states no licence.**
  `open_review.terms` must say under what terms the sources may be inspected and run,
  and for 11SquaresFormalized the true answer is that none are granted beyond GitHub’s
  terms of service for viewing; `integrations/wand125/` carries MIT notices for the
  incorporated work only.
  Asking Ahmed for a licence (MIT, like the parts he incorporated) is the author’s
  action and the owner’s to request.
- **`LR-7`, not blocking: the checker does not tie a formalization review to a
  formalization.** `formalization_reviews` counts any accepting human formalization
  review on the result, whichever formalization it read; `T-060` could one day cite two
  formalizations (Ahmed’s and wand125’s). Finding 6 of the 6 October review reported it;
  no bead was found. Proposed: a `formalization_of: <evidence id>` field on
  `kind: formalization` items, required by the schema and checked by `review_problems`
  to name a cited `proof-assistant-checked` entry.
- **`LR-8`, not blocking: `T-084`’s Lean route is half held** (§3.2). The 2 October
  build compiled `squareMinusOne_isMinimumSide` on the standard axioms, and nothing
  cites it. `think-5i1z`’s plan stands and is priced at about an hour; it is a second
  machine method beside the rung and the only formal route `T-084` has toward `V5`.
- **`LR-9`, not blocking: `T-055`’s hypothesis-free proof is not retained** (§3.3).
  `think-f2bm` should retain `point_n21_L5/lean/zero-margin/` from the archived
  repository at `77636c63` or `781afb3` (five files; the 88 MB of generated data is
  regenerated by the build script and pinned by `data-sha256.txt`), and the build is
  priced at 6 to 8 hours here.
  Note that its certificate is `n21-capture-one.txt`, the cover renormalised to
  threshold 1, not the `n21-original.txt` of the entry; the theorem is the same
  `minSide 21 = 5`.
- **`LR-10`, not blocking: Daniel’s Lean binding reaches `T-120` and not `T-121` to
  `T-124`** (§3.4). `think-63vx` should retain `lean/Sqpack/Exact/Packs/N102.lean`,
  `N102/`, `SHA256SUMS`, the README and the modules they import (`ExactPack.lean`,
  `ExactCheck.lean`, `Spec.lean` and their closure, pinned by blob), and build `N102`
  here; `T-120`’s claim then separates the kernel-checked bound from the asserted
  minimality. The other three stay on the exact checker’s route.
- **`LR-11`, not blocking: the statement closure builds again** (§5), so
  `E-n011-lean-statement-closure-build`’s replay command is live at a second date on the
  same pins.
- **`LR-12`, not blocking: the owner’s question answered in the ladder’s terms.** Both
  repositories are linked (since 29 September and 6 October).
  A formalization merits no `V4`: `V4` is two adversarial AI reviews by distinct
  reviewers and a human oversight record over machine evidence `T-060` already has, so
  the owner’s own record, with the ruling on distinctness that `LR-3` leaves to it, is
  the shortest path to `V4/C4`. It merits `V5` only with a build the record holds and a
  human expert’s review, neither of which the source’s private run supplies as recorded
  (`LR-4`); `C5` is further off still (`LR-6`). The owner’s “not C4 until replayed here”
  is met for `T-060` by the audited-here executions that carry its `C3`
  (`E-n011-global-optimality-independent`); the Lean does not enter `C4`. If the owner
  means a fresh end-to-end replay (`think-e2ot`), that is `C5`’s requirement today, and
  asking it at `C4` would be a change to the ladder.

## 8. Proposed Record Changes, for the Records Lane

1. `T-060.reviews`: add GPT-6 Pro’s review of 2026-10-03 as `kind: adversarial`,
   `reviewer_kind: ai`, `relation: project`, `verdict: accepted`,
   `covers: [T-060, T-112]` (its row in `T-112` is the template), and the 2026-10-03
   paper review by Claude Code as a third, with its scope in its own words.
   Neither moves the rung without the oversight record, which must state the owner’s
   decision whether GPT-6 Pro’s review, which names Astra’s as its source R4, is by a
   distinct reviewer (`LR-3`); `rung_label_problems` accepts the `next_rung` text as it
   stands.
2. `T-060.next_rung` and `notes`: a dated line that the source repository and run are
   visible to the owner since 11 October, that the pin is unchanged, and that `V4` waits
   on the oversight record and the distinctness ruling it states.
3. `E-n011-lean-statement-closure-build.limitations`: the second build of 11 October
   (§5), with its receipt `receipts/lean/build-statement-closure-2026-10-11.log` in the
   packet.
4. `intake-watch.yaml`: a row for EvolvingPrograms/SquaresLean (private; read on
   2026-10-11 through the owner’s token; `n = 12` and comparator work; no bead) and one
   for the `6bbae379` Lean binding under `think-63vx`, if the evand watch row does not
   already carry it.
5. A bead for `LR-7`, the `formalization_of` field.
6. `T-084.next_rung` already says what `think-5i1z` does; `T-055.next_rung` should name
   the hypothesis-free proof and its price (`LR-9`); `T-120.next_rung` the `N102` module
   (`LR-10`).

## 9. Decisions Only the Owner Can Make

- **D1. Does a source’s own passing proof-assistant run count toward `V` once the owner
  has read it?** The `V3` row admits evidence “of any origin”, the import process
  records a run nobody here observed as a report, and the 6 October review left the
  choice to the owner.
  He can now observe it.
  If yes: write the rule into epistemics.md and result-import.md stage 3, re-encode
  `E-n011-lean-formalization-report` as `assurance: verified`, `origin: external`,
  `replay` the source’s command, `replay_status: passed`, with the owner’s inspection in
  its `assumptions`, and `V5` then waits on D3 alone.
  If no: `LR-4`’s first two routes.
- **D2. The human oversight record for `T-060`**, and in time for `T-055`, `T-084` and
  `T-120`: the owner or a named person, a document under `docs/project/reviews/` that
  says what was inspected under `trust-boundary`, `certificate-meaning` and
  `ai-findings`.
- **D3. The human expert formalization reviewer for 11SquaresFormalized**, and whether
  one or two are needed at `V5` (decision 15). The 6 October audit §8 states the two
  facts that bear on the owner serving: the announcement thanks him, and the exact `T`
  and construction are this project’s.
- **D4. Whether compiler-trusting proofs may hold `V5` or `C5`**, and whether the trust
  model becomes a recorded attribute beside the rung (§4).
- **D5. Retention from the private repository** (`LR-2`), and the request to Ahmed for a
  licence on 11SquaresFormalized (`LR-6`).
- **D6. Whether to pay for the full build**, and where: the fork-dispatched Actions
  route of §5 is the only one this project can run; a third party’s published build
  would do for `V5` but not `C5`.

## Status, 14 October

Review A of the pull request that carries this review (#563, finding A1) found that
`LR-3`, §3.1 and `LR-12` called GPT-6 Pro’s review of 3 October distinct from Astra’s
under decision 11’s reading, dropping epistemics.md’s “with no shared context”, though
that review names Astra’s as its source R4 and cites it eleven times.
Those passages and §8’s items 1 and 2 now leave the ruling to the owner’s oversight
record, as `RR-1` of the sibling rungs review does.
`LR-12` also now says how the owner’s “not C4 until replayed here” stands against the
ladder. The other findings stand.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
