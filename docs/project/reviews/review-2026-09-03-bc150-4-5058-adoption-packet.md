# BC-150 — Adoption Packet for the Source-Backed 4.5058 Bound at n = 17--19

## Provenance and installation

This document is the adoption packet of BC-150, which audited the retained Massaccesi
certificate against the repository’s present evidence contract and recommended adoption
at source-backed scope, written on 2026-09-03 in the agenda-016 ten-hour run.
Its author wrote only to `scratchpad/bc150/` -- a container-local directory outside the
repository, which does not survive the session -- and modified no repository file beyond
the frontier patch its own verdict authorised.
It is installed here so that the evidence the records cite outlives that directory.

The source was `836` lines with SHA-256
`d88d47b3d0add7822f106c4d0d80af83a7bd99a8ff12f18498589d5fb57b8413`, and that hash names
the scratchpad source rather than this file.
The installation added this preface; it altered no classification, verdict, finding,
number, citation, recommendation or claim boundary, and none may be altered here.
References of the form `scratchpad/...` in the body below are the author’s own record of
what was read and where it was written at the time, and are left as written.

* * *

# BC-150 — Adoption Packet: the Retained Massaccesi `4.5058` Certificate at `n = 17, 18, 19`

Agenda 016, block BC-150 (bead think-6q88). Author: the BC-150 lane, which authored
neither the H-052 instrument, exp-059, nor the BC-149 review.
Date: 2026-09-03. Repository `/home/user/squares`, branch
`claude/squares-pr76-overnight-run-tpc888`, HEAD
`ceff44000a747bd43f81d48cecd4005d38695e49`. Interpreter `packing/.venv/bin/python3`
(Python 3.14.7) throughout; bare `python3` was never invoked.
Writes went only to `scratchpad/bc150/`. No repository file was created, modified or
deleted; no `git add`, `commit` or `push`.

This packet is immutable once BC-151 opens.
It records three determinations, kept separate, and one proposed patch that it does
**not** apply.

## Recommendation

**ADOPTION**, at source-backed scope: record `s(17) >= 22529/5000 = 4.5058` as the
verified lower bound at `n = 17`, and by monotonicity at `n = 18` and `n = 19`, as an
externally proposed, previously-published result replayed and audited here (`V4/C3`,
`novelty: previously-published`), leaving `n = 20` unchanged.

**The single strongest reason against.** Every artifact on the retained record — the
source verifier, the repository instrument, exp-059 and the BC-149 review — belongs to
one method family: an exact event-cell sweep of a shrunken square over a rational angle
net.
The reduction that turns the continuum claim into 181 finite checks is shared by all
of them, so H-052’s all-cell agreement could not have detected an error in it.
What discharges that reduction is this block: a written proof of every lemma (section 3)
and a fourth implementation that imports nothing from the repository or the source,
selects cells by its own rule, decides membership by whole-cell containment, and also
checks the true unit square at 380 off-net angles (section 2). Those are scratch
artifacts and a prose audit, both awaiting BC-151’s independent review, and no
method-distinct certificate (a pose-space interval audit, as `cases/green17` has) exists
for this bound. That is why the honest rung is `C3`, not `C4`, and why the packet’s
limitations list starts there.

The three determinations in one line each:

| Determination | Outcome |
| --- | --- |
| (a) Checker status | **Exact pass.** Retained verifier replays; exp-059 accepted and independently reviewed; a fourth from-scratch implementation reproduces all 181 rows, cell counts and hashes, and finds minimum exactly 1 at 380 further angles with the true unit square. |
| (b) Assurance / adoption | **Adoption recommended, source-backed.** Every shared lemma is discharged in this packet; no source ambiguity reaches the certificate; the evidence meets the present contract for `assurance: verified`, `method: exact-algebraic`, `origin: replayed-here`, deriving `V4/C3`. |
| (c) Monotone consequences | `n = 17, 18`: `4426213/1000000 -> 22529/5000` (+`79587/1000000`). `n = 19`: `1 + sqrt(12) -> 22529/5000` (+`0.0416984`). `n = 20`: unchanged, `22529/5000 < 1 + sqrt(13)`. All exact. |

## 1. Frozen Inputs

### 1.1 The retained source

| Artifact | SHA-256 |
| --- | --- |
| `packing/resources/web/n17-lower-bounds-2026/massaccesi-lower-bound-4_5058.html` (result post, contains the verifier) | `7dffb6e6e6cbff0ac2e887ca445b45f46c95055718219f7229d1c8cb06f84514` |
| `packing/resources/web/n17-lower-bounds-2026/massaccesi-linear-programming.html` (LP post) | `cdd27897f4f6c3b83835d59a317b3248b4f94b888f8568b740c778524a11f177` |
| `packing/resources/web/n17-lower-bounds-2026/massaccesi-verify-n17-lower-bound-4_5058.py` (the certificate: extracted verifier) | `04531a54da9a654f2318401aff43222daf721bd99e948b2491f91c05bd0b5d3f` |
| `packing/resources/web/n17-lower-bounds-2026/burns-n17-lower-bound-4.4811.md` (the proof note the certificate reuses, with parameters changed) | `a7ddd7642b2a35064506978afc78b48460904bedb7f387481b248b4d3d42db85` |
| `packing/resources/web/n17-lower-bounds-2026/README.md` (retrieval record, 2026-08-31) | `b48c0c31cf62366d44cd12f02cf321dd38b5a23391caec95f04445938e0b3d75` |

All five match the hashes the README itself records.
Source URLs:
`https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html`,
`https://gus-massa.blogspot.com/2026/08/linear-programing-for-square-packing.html`.

The certificate is the verifier’s literal data, not the prose: `L = 45058/10000`,
`M = 15513/10000`, `B = 9973/10000`, `T = 207107/500000`, `KMAX = 180`,
`WEIGHT_SCALE = 576`, `NGRID = 29`, and 23 `(i, j, w)` orbit seeds.

### 1.2 The repository instrument and the H-052 result

| Artifact | SHA-256 |
| --- | --- |
| `packing/cases/n17_weighted_certificate/extract.py` | `db176a8eff7235991c63c8e7f098e2e2979edf64905d8f76427e0cd218b011e2` |
| `packing/cases/n17_weighted_certificate/fixture.py` (168-atom fixture, static extraction) | `3b37d03f311b62f6a2ad41b099629d6a1fcfaae9c9f0b6e8083065b80336995f` |
| `packing/cases/n17_weighted_certificate/geometry.py` (shared reduction) | `2b55425f9170af03ae577f5e291499628053aad365e0220a1cb3043c2515d3c1` |
| `packing/cases/n17_weighted_certificate/independent.py` (clean-room accumulator) | `55d36239f1f7e860f059030d87f655d2ac0c82685d788b599a7dd23d33d18de0` |
| `packing/cases/n17_weighted_certificate/source_faithful.py` | `aaccd145c61fb20bc2b83a8ded83dfdd3f2d4b6d6c730ff46df31e1f1d8ae305` |
| `packing/cases/n17_weighted_certificate/target_independent.py` | `db86f6731180f8b82a9f54412c82713ac66ed9206458e222f8547574039a2ef0` |
| `packing/cases/n17_weighted_certificate/model.py` | `9321f6c7a43c2d2ffb72be4d540fcb91254fbdcfd63928c7da4927b7e14f96af` |
| `packing/cases/n17_weighted_certificate/run.py` | `177e8545400799b6a701f258b685f2712f2529132803d78bf984575b897d027c` |
| `packing/cases/n17_weighted_certificate/selftest.py` | `4bfc564cf9cacbe8c50453ec30b41dadf134f1c3fec62f422fe699321426318d` |
| Frozen package manifest (sorted `sha256sum` of the package) | `309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54` |
| `packing/cases/n17_weighted_certificate_successor/run.py` | `ab4dd8fe66b15e8f7c9837c4a3fede7234f702892addaf818bbacff1a763a553` |
| `packing/cases/n17_weighted_certificate_resume/run.py` | `3e5284fd56fd33f7b767954164128e9d43f5efad09eae4666035c3ef32c63f54` |
| `packing/cases/n17_weighted_certificate_child/run.py` | `f45227508b28f37759df836db08dbad2031d600ef2b1ac087b73f8322b156b05` |
| `packing/tests/test_n17_weighted_certificate.py` | `c3f1377db0c3443beb2557a292dcee0c19d305047e395672e1acd72bd346d7a3` |
| `packing/tests/test_n17_weighted_certificate_successor.py` | `dbe1032fc95149e72f33666ecb587dcca55c8ab1279ae1c388850f16d68e9d9b` |
| `…/results/exp-059-h-052-n17-fresh-successor-completion.json` (the H-052 result; committed at `ceff4400`) | `438dfc1ffc3f5ac2c8b83bc03014aa52e616da95b4a3b276f22326d36dee2d0a` |
| `…/results/exp-059-h-052-n17-fresh-successor-completion.checkpoint.json` | `bb45ed2a1bd01b26ec4af3a137f5f51ce6a9ad1f8ccc744b76db936e62d1d28c` |
| `…/results/exp-056-h-052-n17-sequential-larger-prefix.checkpoint.json` (immediate parent) | `0d39a7e734e8afc62fda914fda4ec8b5e9b2e48ea1b1d8b197dc08e27e7a35d4` |
| `…/results/exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json` (chain genesis) | `db5c156959b6de4e6f2c9be283454d01dd5f3a436e6489f5e6bb60c38559fdb8` |
| `…/experiments/exp-059-h-052-n17-fresh-successor-completion.md` | `c9949ff52f566df39907836481996b5a2ef7fa8a6fcb906aadbaba6d5c5b14b3` |
| `packing/campaign/hypotheses/H-052-n17-independent-certificate-agreement.md` | `dd5160d20ca074b182521db6cd3a0dd9d96ddb02530010c50d4ea3b5010d847c` |
| BC-149 review, `scratchpad/bc149/h052-agreement-review.md` | `dc1548ff7227171c1770cfaacc88e8420ffb6944827d7b1c1991a2fc5d702d78` |
| BC-149 third path, `scratchpad/bc149/my_eval.py` and `my_eval_summary.json` | `32911b97fca8d3ff…`, `41d6994fc69dfb72…` |

Values the record carries and this packet relies on: atom count 168, atom hash
`37d35da00625967f9e61d3c5f098da1a6583933c8c39979d6b6927a50546cf5a`, direction count 181,
direction hash `cc789e1a16d190064a0eda2fe5e4bf0399d939362c85fb448f1162ef5cac4e79`, total
weight `203/12`, all 181 row minima `1/1`, global minimum `1/1`, `preconditions_pass`,
`shrink_and_scaling.all_hold`, `all_mutations_rejected`, `instrument_valid` and
`decision: accepted`, all derived from emitted fields.

### 1.3 The present evidence contract

| Artifact | SHA-256 (working tree; unmodified vs HEAD unless noted) |
| --- | --- |
| `epistemics.md` | `2ecf19bfbf4fe5e61aa268846d484f07bb6dc989b325777614a8d4dff6a4adc0` |
| `conventions.md` | `04e2636a9dd63b61a4c73a23b6284719289d58b74d090ed4b2bc953694514991` |
| `packing/frontier/README.md` | `a59027677e44c04664e4ff5420581b1c7cb8d31942c2c8aaf807562d6fe8c0b8` |
| `packing/src/sqpack/assurance.py` | `71b1362cb7fc02262b97852b25b83b962119bbf40cc95d689df4139b212e06d6` |
| `packing/devtools/check_results.py` | `eaf7756d32479d92051b20b21d1f3df0de52580dbe5e574d561cd6f1cf903c50` |
| `packing/campaign/agendas/agenda-016-…md` (BC-150 contract and Routing Rules) | `b376338536cd7e53f02639327ce5215258c3e4abff5e78f71deb5d4598a2c603` |
| `packing/campaign/explorations/X-011-controls-are-not-targets.md` | `ecd16b150196a3be10908b4c21d175fdc9d9a3bc203a02fba0c96e71b987fc72` |

The contract, as it stands today, in the clauses that decide this block:

- `verified` means “an exact check, rigorous certificate, or complete proof decides the
  claim and its preconditions” (`conventions.md` §4). Frontier README, step 4: “Put a
  value in the verified lane only after an exact proof, exact witness replay, or
  rigorous interval certificate discharges its assumptions.
  Record external evidence and a local replay separately.”
- `assurance.py`: a formal method requires `verified`; `exact-algebraic` requires
  `certificate` and `replay`; `previously-published` requires `source_key`; verified
  evidence requires a displayed origin.
- `check_results.py`: `V4` from any machine-proof-shaped entry (exact-algebraic,
  certificate, replay, `replay_status: passed`); `C3` from one such repository-origin
  entry, `C4` only from two with different `method` values; “two independently written
  implementations using the same method still derive `C3`”; a `C3` result names a
  control path.
- Verification origin stays visible: “Running the source generator’s own checker is
  useful evidence but does not become an independent implementation.”
- The novelty vocabulary: `previously-published` covers “any public attributable
  artifact — paper, preprint, record table, repository”.

### 1.4 Frontier state the patch would change

| File | HEAD blob SHA-256 | Working tree |
| --- | --- | --- |
| `packing/frontier/n-017.md` | `afae0ee9ec040e9425759ba5bbc36f49eddb46b771e580fbf1f4ce8a0f1291a5` | same |
| `packing/frontier/n-018.md` | `5420bc6a13897087517c30a47effbd9fac1730b23676ed7b5589d234bd5a8e20` | same |
| `packing/frontier/n-019.md` | `eecdd7b7bbb873355f7d3f7d7abaf02c3026695ab2cf64536130e4debaf59c2d` | same |
| `packing/frontier/n-020.md` | `afb0030507e0d4881125c75f060d534a382965e48f2d7eaf689d8fb829739457` | same (must stay unchanged) |
| `packing/frontier/evidence.yaml` | `717a84c122fc9934db8b4d1c25b9d8b206fa6462465b06d591ba459b5f8648e4` | **modified by the H-060 lane**: adds `E-n005-fixed-side-local-rigidity` |
| `packing/frontier/results.yaml` | `056e8d5d205a9d66a2678a4a5799716908398aa821d090f09d41e91074ea637a` | **modified by the H-060 lane**: adds `T-014` (13 -> 14 results) |
| `packing/src/sqpack/cli/validate.py` | `e211a362eee89e5f69ec2a9eb3b80cede9344358f16b3f06d56354cc3e6225d7` | **modified by the H-060 lane** (7 lines) |
| `packing/frontier/STATUS.md`, `RESULTS.md`, `INVENTORY.md` | `adf7e4cb…`, `4fbe4553…`, `74ebf3b9…` | generated views; `RESULTS.md` modified by the other lane |

Because three of the patch targets are under concurrent edit by another lane, the
proposed patch (section 6) is keyed by content, not by byte offsets, and names the next
free identifiers conditionally (`T-015`, `T-016` if `T-014` lands as H-060’s).

Current verified lower bounds: `n = 17`: `4426213/1000000`
(E-green17-sixteen-point-lower, E-green17-interval-audit); `n = 18`: the same by
monotonicity; `n = 19`: `sqrt(19 - 2*floor(sqrt(19)) + 1) + 1 = 1 + sqrt(12)`
(E-nagamochi-lower); `n = 20`: `1 + sqrt(13)` (E-nagamochi-lower).

## 2. Determination (a): Checker Status — Exact Pass

Four implementations now agree on the certificate.
Their independence differs, and the table says at which layer each is fresh.

| Path | Where | Reduction | Per-cell mass | Result |
| --- | --- | --- | --- | --- |
| Retained source verifier (Burns’s, modified by Massaccesi) | `resources/…/massaccesi-verify-n17-lower-bound-4_5058.py` | source’s own (slab clip + v-range superset) | int64 difference array, two cumulative passes | 168 atoms, `9744/576`, 181 directions, `B(1+D) = 899635478111/900000000000 < 1`, minimum `576/576`, “CERTIFICATE CONDITIONS VERIFIED” |
| Repository source-faithful path (exp-049 package) | `cases/n17_weighted_certificate/source_faithful.py` | shared `reduce_event_cells` (transcription of the source’s) | Fraction difference array | 181 rows, all `1/1` |
| Repository independent path (exp-049 package) | `cases/n17_weighted_certificate/target_independent.py` + `independent.py` | shared `reduce_event_cells` | direct membership sum over 168 atoms at each cell centre | 181 rows, all `1/1`, byte-identical manifests (exp-059) |
| BC-149 third path (scratch) | `scratchpad/bc149/my_eval.py`, no repository imports | own events and clipping | integer product of membership matrices | all 181 rows: events, cell counts, minima, witnesses reproduced |
| **BC-150 fourth path (scratch, this block)** | `scratchpad/bc150/independent_audit.py`, no repository imports | **own cell rule**: polygon v-range over each slab from vertices and edge crossings, no Sutherland–Hodgman clip | **whole-cell containment** (`p_U - h <= u_i` and `u_{i+1} <= p_U + h`), no midpoints, no difference arrays; plus closed membership on every selected cell’s edges and corners | all 181 rows minimum `576/576`; selected cells `16,562,293`, equal row by row to the record’s `event_cell_count`; atom hash and direction hash rebuilt from the literals equal the record’s |

Replays executed in this block, all from `scratchpad/bc150/`:

| Check | Result |
| --- | --- |
| Retained verifier, normal Python, 5.3 s | output as the README recorded; log SHA-256 `68b925923c7a6b54cb6bc391642b6eea1f759c503afa4abc12275ecc7094358a` |
| Part A: 23 seeds expand to 168 atoms (19 orbits of size 8, 4 of size 4); integer total 9744; `9744/576 = 203/12 < 17`, margin `1/12`; weights in `[3, 246]`; every atom strictly inside `[0, L]^2`; grid symmetric about `L/2`; **the weighted multiset is invariant under all eight symmetries of the container** | all true |
| Part B: 181 exactly-unit directions in the first quadrant, `k = 0` axis-aligned; `(T+1)^2 > 2` so `psi_180 = 2 arctan T > pi/4`; final pair brackets the quarter turn; all 180 half-gap tangents `<= D = 207107/90000000`, all positive; `B(1+D) = 899635478111/900000000000 < 1`, slack `364521889/900000000000` | all true |
| Part C: exact monotone arithmetic (section 4) | all as stated |
| Part D: 181 `B`-square sweeps, own reduction and own membership rule; closed-boundary evaluation on all edges and corners of all `16,562,293` selected cells | every row minimum `576`, boundary minimum `576`, never below the open-cell minimum; 181 pairwise-distinct witnesses; tight cells per direction from 172 to 7,272 |
| Part E: **true unit square** (side 1, not `B`), exact sweeps at 180 net-midpoint angles and 200 pseudo-random rational angles in `[0, pi/4]` (seed `0x5058`) | minimum exactly `576/576` at all 380 angles; never below 1 |
| Cross-check against exp-059 (`crosscheck_record.py`) | atom hash `37d35da0…` and direction hash `cc789e1a…` reproduced from the literals; all 181 selected-cell counts equal `event_cell_count`; all 181 minima equal |

Part E is the check no earlier path made: it evaluates the theorem’s conclusion — every
unit square at that angle has mass at least one — directly at angles that are not in the
net, so it does not pass through the angle-net or containment step at all.
That the minimum is exactly 1 rather than above it is the expected shape of a tight LP
certificate: the extra `0.0027` of side over `B` rarely captures a grid atom at spacing
`2.9545/28`.

What agreement can and cannot see (carried from BC-149, confirmed here): a defect that
only raises masses at non-minimizing cells is invisible to a comparison of minima; the
registered criterion is on minima, so this is a scope statement.
Part D’s boundary evaluation and Part E’s unit-square sweeps are lower-bound checks and
inherit the same scope.

**Checker status: exact pass**, with the independence boundary stated: on the retained
record, accumulation-level independence over a shared reduction (BC-149’s verdict); in
scratch, two from-scratch implementations of the whole check (BC-149’s and this one),
the second with a different cell rule and membership rule and a direct test of the
conclusion off the net.

## 3. Determination (b): Assurance and Adoption — Adoption Recommended

Implementation agreement is established at the scope above.
This section audits the mathematics separately: what the certificate proves, through
which lemmas, which of them are shared by every implementation, and how each is
discharged. A lemma marked *proved here* is proved in this packet; *checked exactly*
means an exact rational computation in this block decides it for this instance.

### 3.1 The theorem and the argument

**Theorem (Massaccesi 2026, on Burns’s architecture).** `s(17) >= 22529/5000 = 4.5058`.

Let `C = [0, L]^2` with `L = 22529/5000`, and let `mu` be the atomic measure placing
mass `w/576` at each of the 168 atoms.
The argument has two halves.

*Half one (finite check, computer-assisted).* Every closed unit square `Q` contained in
`C`, at every position and orientation, has `mu(Q) >= 1`.

*Half two (the fractional-unavoidable-set lemma).* If every unit square in `C` has mass
at least 1 and `mu(C) < 17`, then `s(17) >= L`.

### 3.2 Lemma-by-lemma audit

**L1 — Scaling and disjointness (half two).** *Proved here.* Suppose 17 unit squares
with pairwise disjoint interiors lie in a closed square of side `L' < L`. Scale by
`L/L' > 1` and translate: the container becomes `C`, the squares `P_1..P_17` have side
`L/L' > 1` and still have pairwise disjoint interiors.
Let `Q_i` be the concentric unit square inside `P_i` with the same orientation; `Q_i`
lies in the interior of `P_i`. For `i != j`, `Q_i` is inside `int(P_i)`, `Q_j` inside
`int(P_j)`, and those interiors are disjoint, so the closed sets `Q_i, Q_j` are
disjoint: no atom lies in two of them, even on boundaries.
Each `Q_i` is inside `C`, so by half one `mu(Q_i) >= 1`, and by disjointness and
non-negativity of the weights
`17 <= sum mu(Q_i) = mu(union Q_i) <= mu(C) = 203/12 < 17`, a contradiction.
So no packing exists at any side below `L`. Since the achievable sides form a closed set
and the minimum is attained (`TUTORIAL.md` §1, citing Martin 2000), `s(17) >= L`. The
argument uses interior disjointness of closed squares in a closed container, which is
exactly the repository’s convention ("Disjointness is required of interiors only",
touching legal); under an open-container convention the statement is only stronger, so
no convention mismatch is possible.
Strictness sits in `mu(C) < 17`; `mu(Q) >= 1` need not be strict.
Checked exactly: `mu(C) = 203/12`, margin `1/12`, all weights positive.

**L2 — Reduction of orientations to `[0, pi/4]`.** *Proved here; symmetry checked
exactly.* A square’s orientation is defined modulo `pi/2`. For an orientation in
`(pi/4, pi/2)`, reflect the configuration across the diagonal `x = y` of `C`: the
container maps to itself, the direction `(cos t, sin t)` maps to `(sin t, cos t)`, so
the orientation becomes `pi/2 - t` in `(0, pi/4)`, and `mu` is unchanged because the
weighted atom multiset is invariant under all eight symmetries of `C` (Part A verified
this on the reconstructed atoms, not assumed from the orbit construction).
Hence it suffices to prove half one for orientations in `[0, pi/4]`.

**L3 — The angle net covers `[0, pi/4]` within `epsilon < D`.** *Proved here; checked
exactly.* With `t_k = kT/180`, `psi_k = 2 arctan t_k` runs from `0` to `2 arctan T`, and
`2 arctan T > pi/4` because `T > tan(pi/8) = sqrt(2) - 1`, which is `(T+1)^2 > 2`
(exact: true). For adjacent net angles, half the gap is
`arctan t_{k+1} - arctan t_k = arctan(D / (1 + t_k t_{k+1})) <= arctan D < D` (exact:
all 180 tangents `<= D`, positive).
So every orientation in `[0, pi/4]` is within angle `epsilon <= arctan D < D` of some
`psi_k`. Whether 181 is “the right set”: the net is not required to be uniform or
minimal, only to cover with a gap small enough for L4, and it does; 181 is the count of
`k = 0..180` and every one of the 181 directions is used.

**L4 — Concentric containment.** *Proved here; checked exactly.* A closed square of side
`B` concentric with a unit square and rotated by `epsilon` relative to it has vertices
at distance `(B/2)(cos epsilon + sin epsilon)` along each of the unit square’s axes, so
it is contained in the unit square iff `B(cos epsilon + sin epsilon) <= 1`. For
`0 <= epsilon < D < 1`: `cos epsilon <= 1` and `sin epsilon <= epsilon` give
`B(cos epsilon + sin epsilon) <= B(1 + epsilon) < B(1 + D) = 899635478111/900000000000 < 1`
(exact: strict, slack `364521889/900000000000`). Therefore every unit square in `C`
contains a concentric closed `B`-square at one of the 181 net directions, and half one
follows from: **every closed `B`-square at a net direction and contained in `C` has mass
at least 1.** The unit square’s mass is at least the `B`-square’s because the weights
are non-negative.

**L5 — Centre domain.** *Proved here.* For a direction `(c, s)` with `c, s >= 0`, the
`B`-square’s extent from its centre along `x` and along `y` is `h = B(c + s)/2`, so it
lies in `[0, L]^2` iff its centre lies in `[h, L - h]^2`; in the square’s own frame
`U = cx + sy`, `V = -sx + cy` that is a rotated square, the domain polygon.
Every net direction has `c, s >= 0` (exact), including `k = 180`, where `s > c`
slightly; the formula is symmetric in `c` and `s`.

**L6 — Membership rectangles and constancy on open cells.** *Proved here; established
constructively in Part D.* An atom `p` lies in the closed `B`-square centred at `(U, V)`
iff `|U - p_U| <= B/2` and `|V - p_V| <= B/2`, an axis-aligned closed rectangle `R_p` in
centre coordinates.
The event lines `U = p_U +- B/2`, `V = p_V +- B/2` (plus the domain’s
extreme coordinates) cut the plane into open cells on which no membership changes.
Part D does not assume this: it decides membership on a cell by whole-cell containment
(`p_U - B/2 <= u_i` and `u_{i+1} <= p_U + B/2`, and likewise in `V`), which is the
statement that the cell lies inside `R_p`, and since no event line crosses an open cell,
a cell not inside `R_p` is disjoint from it.

**L7 — Completeness of the cell enumeration.** *Proved here; checked exactly by an
independent rule.* Any open cell meeting the domain must be examined.
The source (and the shared `reduce_event_cells`) keeps a `u`-slab iff `u_{i+1} > u_min`
and `u_i < u_max`, clips the domain to the closed slab, takes its `V`-range
`[v_lo, v_hi]`, and keeps every `v`-cell with `v_j < v_hi` and `v_{j+1} > v_lo`. If an
open cell meets the domain, some domain point has `U` in `(u_i, u_{i+1})`, so the slab
is kept, the clipped polygon is non-degenerate, and the point’s `V` lies in
`[v_lo, v_hi]` and in `(v_j, v_{j+1})`, which forces `v_j < v_hi` and `v_{j+1} > v_lo`.
So the kept set is a superset of the cells that meet the domain, and a superset only
lowers the minimum, which is conservative for a lower bound.
Part D computes `[v_lo, v_hi]` by a different rule (vertices inside the slab plus edge
crossings of `U = u_i` and `U = u_{i+1}`) and reproduces exactly the record’s 181 cell
counts, `16,562,293` in total.

**L8 — Boundary points.** *Proved here; and made unnecessary for this instance by Part
D.* Membership sets are closed rectangles, so for a point `x_0` on an event line and any
`x` close enough to it, `{p : x in R_p}` is a subset of `{p : x_0 in R_p}`: the mass is
upper semicontinuous, and its minimum over the domain is attained on open cells whose
closure meets the domain — all of which L7 keeps.
Part D additionally evaluated closed membership at every edge and corner of every
selected cell and found minimum `576`, never below the open-cell minimum, so the
semicontinuity lemma is not relied on for this instance.

**L9 — Exact weight normalization and the global minimum.** *Checked exactly.* Integer
weights sum to 9744; `9744/576 = 203/12 = 16.91666…`; the registered minimum
`576/576 = 1` is exactly the row minimum on all 181 rows (source verifier, both
repository paths, BC-149’s path and Part D); `17 * 1 = 17 > 203/12`. The certificate is
tight: every row minimum is exactly 1, with 172 to 7,272 tight cells per direction and
pairwise distinct witnesses, which is what an LP-optimized certificate rounded up with
`ceil` looks like and is why the `weight_mutation_rejected` guard (any `+1/576` on one
atom changes the total) is meaningful.

**L10 — Exactness of arithmetic.** *Checked.* The source verifier keeps all geometry in
`fractions.Fraction`; its only integer arithmetic is an int64 difference array whose
entries are bounded by `4 * 9744`, far below `2^63`. The repository paths use `Fraction`
throughout. Part D uses int64 products of 0/1 matrices with weights, bounded by 9744. No
floating-point value decides any inequality anywhere in the chain.

**L11 — Monotonicity to `n = 18, 19`.** *Proved here.* A packing of `n >= 17` unit
squares contains a packing of 17 of them, so `s(n) >= s(17)` for `n >= 17`. Section 4
computes the consequences exactly and shows `n = 20` does not move.

### 3.3 Shared assumptions and how each is discharged

| Shared by every implementation | Discharged by |
| --- | --- |
| The fixture reconstruction (grid `M/2 + (L - M) i/28`, orbit expansion, `w/576`) | Rebuilt from the literals in Part A with its own code; reproduces the record’s atom hash `37d35da0…`; D4 invariance and strict interiority verified |
| The direction net (181 exact unit directions) | Rebuilt in Part B; reproduces `cc789e1a…`; L3 |
| The projection convention `U = cx + sy`, `V = -sx + cy` and the centre-domain formula | L5; identical convention for atoms and domain, checked in Part D’s code by construction |
| The event-cell reduction and its cell selection | L6, L7 proved; Part D’s independent rule reproduces all 181 counts |
| Open cells suffice | L8 proved; Part D evaluates the boundaries anyway |
| The angle-net and containment step | L3, L4 proved and checked exactly; Part E tests the conclusion directly at 380 off-net angles with the true unit square |
| Scaling, disjointness, strictness, convention | L1 proved; the repository’s convention matches, and an open-container convention only strengthens the claim |
| Preconditions and mutation guards (single implementation in the package) | The preconditions are recomputed by BC-149 and in Part B by independent arithmetic; the mutation guards are instrument hygiene, not premises of the theorem |

Nothing on this list remains an undischarged assumption.
The audit is a proof written by this lane plus exact computation; it is not a
proof-assistant check, and it awaits BC-151.

### 3.4 Source ambiguity

The prose has defects the README already records; none reaches the certificate, because
the certificate is the verifier’s literal data, which is unambiguous and hash-pinned:

- “internal grid has a total side of 3.9545” versus the code’s `L - M = 2.9545`;
- “L=4.45058” in the LP post versus `L = 45058/10000`;
- the blog drawing spaces the grid by `/29` where the verifier uses 28 intervals;
- the separate floating-point LP generator’s `range(j0, j1)` omits an inclusive endpoint
  that the final verifier handles with `j0:j1 + 1`. The LP generator produced candidate
  weights at `L = 4.5000, M = 1.5500`; the author then pushed the geometry by decimal
  search while keeping the rounded-up weights.
  The generator is not part of the proof and is not replayed; the verifier at the final
  geometry is the proof.

The proof narrative for `4.5058` exists at the source only by reference: “making the
obvious changes to the explanation posted by Sam Burns proves(?) the new bound.”
Those changes are the margin `M` (grid offset `M/2` instead of `1/2`) and the constants,
and section 3.2 is the narrative with those changes made and every step proved.
The author’s own “(?)” and the absence of peer review are recorded in the limitations
and in the proposed evidence text; they do not change the assurance of an exact
certificate this repository has replayed, but a reader must be able to see them.

### 3.5 Fit to the present contract

| Contract clause | Status |
| --- | --- |
| An exact check decides the claim and its preconditions | Yes: exact rational certificate; preconditions computed exactly (Part B, exp-059) |
| `exact-algebraic` needs `certificate` and `replay`, `replay_status: passed` | Yes for both proposed entries (section 6.1), each with a bounded-time replay whose scope is stated |
| Origin displayed | `replayed-here` for both; the argument itself is external, so the proposed text also carries a dated review note in `limitations` |
| Independent implementation versus the generator’s checker | Stated honestly: one entry is `same-implementation` (the source author’s verifier), the other `independent-implementation` at the accumulation level over a shared reduction |
| Novelty | `previously-published`, `source_key: '[Burns–Massaccesi n17]'` (the resources citation key) |
| Derived rungs | `V4/C3`; two entries with the same `method` do not make `C4` |
| A `C3` result names a control path | `packing/tests/test_n17_weighted_certificate.py`, `packing/tests/test_n17_weighted_certificate_successor.py` |
| Precedent in the verified lane | Nagamochi 2005 (`V3/C1`, external published proof, read informally) and Göbel 1979 (an outline, not reviewed) already carry verified lower bounds; Bentz 46 (`C3`, audited here) and green17 (`C4`, two methods) are the first-party precedents. The proposed evidence is stronger than the first pair on machine confirmation and weaker than green17 on method diversity |

**Assurance/adoption determination: ADOPTION recommended, source-backed.** The route
claims no new first-party mathematics; what is first-party is the replay, the
accumulation-independent instrument, and this audit.

## 4. Determination (c): Exact Monotone Consequences

`L = 22529/5000`; `(L - 1)^2 = 307265841/25000000 = 12.29063364`.

| `n` | Current verified lower bound | Proposed | Exact comparison | Change |
| ---: | --- | --- | --- | --- |
| 17 | `4426213/1000000 = 4.426213` | `22529/5000 = 4.5058` | `22529/5000 - 4426213/1000000 = 79587/1000000 > 0` | +`0.079587` |
| 18 | `4426213/1000000` (monotone from 17) | `22529/5000` (monotone from 17) | same | +`0.079587` |
| 19 | `1 + sqrt(12) = 4.46410161514…` | `22529/5000` | `(L - 1)^2 = 12.29063364 > 12` | +`0.0416983849` |
| 20 | `1 + sqrt(13) = 4.60555127546…` | unchanged | `(L - 1)^2 = 12.29063364 < 13`, so `L < 1 + sqrt(13)` | none |

Consistency checks, all exact: `L` exceeds Nagamochi’s `1 + sqrt(10)` at 17 and
`1 + sqrt(11)` at 18; exceeds Green’s reported, sourceless `(40 sqrt 2 + 19)/17`
(`(17L - 19)^2 = 3317.6… > 3200`); and lies below every reported upper bound it would
sit under: `4.67553…` at 17, `(7 + sqrt 7)/2` at 18 (`(2L - 7)^2 < 7`), and
`3 + (4/3) sqrt 2` at 19 (`9(L - 3)^2 < 32`). No conflict field is created.

Gap to the reported record after adoption: `n = 17`: `0.1697` (was `0.2493`); `n = 18`:
`0.3171` (was `0.3967`); `n = 19`: `0.3798` (was `0.4215`).

The frontier’s Nagamochi-governed count of open cases drops from 61 to 60, because
`n = 19` stops citing `E-nagamochi-lower` in its verified lane; `validate.py` asserts
that count (section 6.6).

## 5. Limitations

1. **One method family on the record.** Every retained artifact is an event-cell sweep
   of the `B`-square over the rational net.
   The method-distinct evidence — this packet’s proofs and its off-net unit-square
   sweeps — is scratch and unreviewed.
   The result would be `C3`; `C4` needs a second method (a pose-space interval
   branch-and-bound over `(theta, x, y)` with the true unit square, as
   `cases/green17/interval_audit.py` does for a 0/1 criterion), which is not built.
2. **Independence on the record is accumulation-level.** The repository’s
   `independent-implementation` entry shares `reduce_event_cells`, the fixture, the
   projection convention and the preconditions with its source-faithful sibling
   (BC-149). The from-scratch evaluators (`scratchpad/bc149/my_eval.py`,
   `scratchpad/bc150/independent_audit.py`) are not repository artifacts and cannot be
   cited as evidence until retained with a replay command.
3. **The source is not peer reviewed**, is a blog post by an individual, and its author
   marks the value “(?)”. Its verifier descends from a note authored by a language model
   (GPT-5.6 Pro) for Burns.
   The adoption is of the certificate, which is exact and replayed; it is not an
   endorsement of the prose.
4. **The retained verifier’s checks are `assert` statements** and vanish under
   `python -O`, after which it prints “VERIFIED” unconditionally.
   It must be replayed under normal Python; the repository instrument’s checks are
   explicit comparisons and its self-test is byte-identical under `-O`.
5. **Bounded-time replay of the independent path does not recompute masses.** The
   independent accumulator costs 155–188 s per direction (about nine hours for 181),
   which is why H-052 needed three chained experiments.
   The proposed replay command verifies the 181-row hash chain and recomputed agreement
   flags from the retained checkpoint in seconds; full recomputation is the executed
   exp-059 run and its ancestors, replayable one direction at a time with
   `--calibrate ORDINAL`. The source method recomputes everything in 5 s.
6. **No LP replay, and none needed.** The weights’ provenance (scipy `linprog` at a
   different geometry, rounded up) is not part of the proof.
7. **Comparison of minima is blind to defects that only raise non-minimizing cells**
   (BC-149’s injection table); every lower-bound check here has the same scope.
8. **Scale of the corroboration in Part E** is 380 angles; it is a direct test of the
   conclusion at those angles, not a proof for the continuum, which L3–L4 supply.
9. **Text consumers carry stale numbers already.** Sixty-odd generated case bodies and
   `frontier/README.md` still say “63 of the 65 open cases” are Nagamochi-governed; the
   gate’s count is 61 today and would be 60 after adoption.
   Not this block’s defect, but the patch must not repeat the stale figure in the bodies
   it rewrites.
10. **Instrument limitations recorded by BC-149** (validator does not tie the rebuilt
    spine to `carried_boundary`; no assembly path from a retained disagreement) do not
    bear on the agreement and are not repaired here.

## 6. Proposed Patch — Frozen, Not Applied

Everything below is a proposal for BC-151 to apply only on an exact pass of this packet.
No file named here changed in BC-150. Identifiers are conditional on what the H-060 lane
lands first: `T-015`/`T-016` if `T-014` is H-060’s; otherwise the next free ids.
Dates marked `<apply-date>` are BC-151’s application date.

### 6.1 `packing/frontier/evidence.yaml` — two entries

```yaml
  - id: E-n017-massaccesi-source-replay
    claim: lower-bound
    scope: {n_values: [17, 18, 19]}
    assurance: verified
    method: exact-algebraic
    performed_by: repository
    novelty: previously-published
    relationship_to_generator: same-implementation
    origin: replayed-here
    source_key: '[Burns–Massaccesi n17]'
    certificate: resources/web/n17-lower-bounds-2026/massaccesi-verify-n17-lower-bound-4_5058.py
    replay: uv run --frozen python resources/web/n17-lower-bounds-2026/massaccesi-verify-n17-lower-bound-4_5058.py
    replay_status: passed
    external_review:
      state: informally-verified
      date: '2026-09-03'
      reviewed_by: repository (BC-150 adoption packet; BC-151 review)
      note: >-
        The published argument (Burns's fractional-unavoidable-set note with
        Massaccesi's margin parameter and weights) was re-proved step by step in the
        BC-150 packet: scaling and disjointness, the D4 symmetry reduction, the
        181-direction net covering [0, pi/4] within arctan(207107/90000000), concentric
        containment B(1 + D) = 899635478111/900000000000 < 1, the centre domain, the
        event-cell reduction and its conservative cell selection, upper semicontinuity
        at event lines, and the exact totals 9744/576 = 203/12 < 17 with every row
        minimum 576/576. A fourth implementation importing nothing from the repository
        or the source reproduced all 181 rows and found minimum exactly 1 for the true
        unit square at 380 off-net angles. Not a proof-assistant check.
    limitations: >-
      Replays the source author's own exact-rational verifier (Burns's, modified by
      Massaccesi), retained byte for byte and hash-pinned: 168 atoms on a 29 by 29 grid
      with margin 15513/20000 in [0, 22529/5000]^2, total mass 203/12 < 17, and mass at
      least 576/576 for every closed 9973/10000-square at each of 181 exact rational
      directions, which by the containment and scaling argument gives
      s(17) >= 22529/5000; n = 18 and n = 19 inherit by monotonicity. The source is a
      2026 blog post, not peer reviewed, whose author marks the value "(?)"; its checks
      are assert statements that vanish under python -O, so replay under normal
      Python. The prose contains transpositions (3.9545 for 2.9545; 4.45058) and a
      drawing spaced by /29; none touches the verifier's literal data, which is the
      certificate. The LP that produced the weights is not replayed and is not part of
      the proof. This is the generator's own checker and is not an independent
      implementation; see E-n017-massaccesi-h052-agreement.
    source_reviewed: '2026-09-03'

  - id: E-n017-massaccesi-h052-agreement
    claim: lower-bound
    scope: {n_values: [17, 18, 19]}
    assurance: verified
    method: exact-algebraic
    performed_by: repository
    novelty: previously-published
    relationship_to_generator: independent-implementation
    origin: replayed-here
    source_key: '[Burns–Massaccesi n17]'
    certificate: campaign/series/series-000-smoke-and-calibration/results/exp-059-h-052-n17-fresh-successor-completion.json
    replay: uv run --frozen python -m cases.n17_weighted_certificate_successor.run --status campaign/series/series-000-smoke-and-calibration/results/exp-059-h-052-n17-fresh-successor-completion.checkpoint.json
    replay_status: passed
    limitations: >-
      The repository's exact instrument (cases/n17_weighted_certificate, package
      manifest 309ec241...) statically extracts the hash-pinned certificate and
      evaluates all 181 directions by two paths: a source-faithful Fraction
      difference-array sweep and a clean-room direct membership sum over the 168 atoms
      at every candidate cell (16,562,293 cells). H-052 (exp-049, exp-052, exp-056,
      exp-059) found the two paths' complete 181-row manifests byte-identical: atom
      hash 37d35da0..., direction hash cc789e1a..., total weight 203/12, every row
      minimum 1/1; the shrink-and-scaling preconditions hold exactly and five frozen
      mutations are rejected. Independence is at the accumulation level only: both
      paths share the event-cell reduction, fixture reconstruction, projection
      convention and preconditions (BC-149), so agreement cannot detect an error there;
      the mathematics of that shared reduction is audited in the BC-150 packet, not by
      this entry. The replay command verifies the retained 181-row hash chain and
      recomputed agreement flags in seconds and does not recompute masses; full
      recomputation is the executed run (1991 s for the last eleven directions on top of
      170 carried rows) and costs about nine hours end to end, replayable per direction
      with --calibrate ORDINAL. Same method family as
      E-n017-massaccesi-source-replay, so together they support C3, not C4.
    source_reviewed: '2026-09-03'
```

Note for BC-151: `external_review` is optional on a `replayed-here` entry
(`assurance.py` requires it only for external origins); it is included on the first
entry so a reader can see that someone here worked through an argument the repository
did not produce. If the schema’s `reviewed_by` is preferred as a bare role, use
`repository`.

### 6.2 `packing/frontier/results.yaml` — two results

```yaml
  - id: T-015            # or the next free id at application time
    claim: >-
      s(17) >= 22529/5000 = 4.5058, by Massaccesi's 168-atom fractional
      unavoidable-set certificate (2026) on Burns's architecture: total mass 203/12 < 17
      and mass at least 1 in every unit square of [0, 22529/5000]^2, reduced exactly to
      181 rational directions and finitely many event cells, replayed here by the
      source verifier and by an accumulation-independent repository instrument.
    scope: {n_values: [17]}
    verification: V4
    confirmation: C3
    significance:
      score: 3
      rationale: >-
        Raises the verified lower bound at n = 17 by 0.079587 over the first-party
        sixteen-point certificate T-001 and closes the gap to the reported record to
        0.1697; an externally proposed, source-backed result that this repository
        replayed, checked by an independent accumulation, and audited lemma by lemma,
        not new first-party mathematics.
      scored: '<apply-date>'
      by: BC-150 packet and BC-151 review (repository)
    novelty: previously-published
    evidence:
    - E-n017-massaccesi-source-replay
    - E-n017-massaccesi-h052-agreement
    artifacts:
    - packing/resources/web/n17-lower-bounds-2026/massaccesi-verify-n17-lower-bound-4_5058.py
    - packing/resources/web/n17-lower-bounds-2026/massaccesi-lower-bound-4_5058.html
    - packing/resources/web/n17-lower-bounds-2026/burns-n17-lower-bound-4.4811.md
    - packing/cases/n17_weighted_certificate/independent.py
    - packing/cases/n17_weighted_certificate/source_faithful.py
    - packing/cases/n17_weighted_certificate_successor/run.py
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-059-h-052-n17-fresh-successor-completion.json
    - packing/campaign/hypotheses/H-052-n17-independent-certificate-agreement.md
    controls:
    - packing/tests/test_n17_weighted_certificate.py
    - packing/tests/test_n17_weighted_certificate_successor.py
    next_rung: >-
      C4 by a method-distinct certificate: a pose-space interval branch-and-bound over
      (theta, x, y) with the true unit square and weighted atoms, on the pattern of
      cases/green17/interval_audit.py; or, short of that, retain a from-scratch
      whole-check evaluator (the BC-149 or BC-150 scratch evaluators) as a repository
      case with a replay so the reduction is no longer single-sourced on the record.
      V5 by a proof-assistant port of the eleven-lemma argument in the BC-150 packet.

  - id: T-016            # or the next free id
    claim: >-
      s(18) >= 22529/5000 and s(19) >= 22529/5000, by monotonicity from T-015 (a
      packing of n >= 17 unit squares contains a packing of 17). At n = 19 this
      replaces Nagamochi's 1 + sqrt(12) = 4.4641...; at n = 20 the certificate does not
      improve 1 + sqrt(13) = 4.6055... and nothing changes.
    scope: {n_values: [18, 19]}
    verification: V4
    confirmation: C3
    significance:
      score: 3
      rationale: >-
        The same movement carried to n = 18 (+0.079587 over T-002) and n = 19
        (+0.0416984, the first verified movement at n = 19 since 2005); the derivation
        adds one line beyond T-015.
      scored: '<apply-date>'
      by: BC-150 packet and BC-151 review (repository)
    novelty: previously-published
    composition: >-
      Derived: the minimum over T-015 and the monotonicity step, which is one recorded
      line carried in the evidence limitations and the case bodies; T-015 sits at
      V4/C3, so the derived claim keeps the rungs.
    evidence:
    - E-n017-massaccesi-source-replay
    - E-n017-massaccesi-h052-agreement
    artifacts:
    - packing/resources/web/n17-lower-bounds-2026/massaccesi-verify-n17-lower-bound-4_5058.py
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-059-h-052-n17-fresh-successor-completion.json
    controls:
    - packing/tests/test_n17_weighted_certificate.py
    - packing/tests/test_n17_weighted_certificate_successor.py
    next_rung: Rises with T-015; a bespoke n = 18 or n = 19 certificate stronger than the inherited bound would be a new result, not a rung change.
```

`T-001`, `T-002` and `T-003` stay registered unchanged: the sixteen-point certificate
remains a first-party theorem at `C4`; it simply stops being the operative frontier
bound.

### 6.3 `packing/frontier/n-017.md`

Frontmatter deltas (content-keyed):

```yaml
  reported_lower_bound:
    value: '4.5058'
    exact_form: '22529/5000'
    kind: unavoidable-points
    proved_by:
    - Gustavo Massaccesi
    proved_year: 2026
    source_key: '[Burns–Massaccesi n17]'
    note: >-
      Proposed 2026 fractional unavoidable-set certificate (168 weighted atoms) on Sam
      Burns's architecture; published as a blog post with an exact-rational verifier,
      not peer reviewed. Nagamochi's general closed form gives 4.162278 here and Green's
      reported but sourceless (40 sqrt 2 + 19)/17 = 4.4452.
    scope: null
    evidence:
    - E-n017-massaccesi-source-replay
    - E-n017-massaccesi-h052-agreement
  verified_lower_bound:
    value: '4.5058'
    exact_form: '22529/5000'
    evidence:
    - E-n017-massaccesi-source-replay
    - E-n017-massaccesi-h052-agreement
```

Add both evidence ids to the case-level `evidence` list; keep `E-nagamochi-lower`,
`E-green17-sixteen-point-lower` and `E-green17-interval-audit` there.
BC-151 may instead leave `reported_lower_bound` on Nagamochi (as `n = 18` was left after
green17); the verified-lane change is the substance of this patch, the reported-lane
change follows the README’s “strongest literal claims in the named source set” and is
offered for the reviewer’s discretion.

Body: replace the paragraph beginning “The verified lower bound is first-party since
2026-08-31” with:

> The verified lower bound is `s(17) ≥ 22529/5000 = 4.5058`, adopted `<apply-date>` from
> Gustavo Massaccesi’s August 2026 certificate (`[Burns–Massaccesi n17]`): 168
> rationally weighted atoms of total mass `203/12 < 17` in `[0, 4.5058]²`, every unit
> square capturing mass at least one, reduced exactly to 181 rational directions and
> `16,562,293` event cells.
> It is externally proposed and source-backed — a blog post, not peer reviewed — and it
> is replayed here twice: by the retained source verifier and by an
> accumulation-independent repository instrument that agrees on every direction cell
> (H-052, exp-059), with the argument itself audited lemma by lemma (BC-150). The
> repository’s own sixteen-point certificate (`cases/green17`, `s(17) ≥ 4.426213`,
> `T-001`) remains a first-party theorem confirmed by two methods and is now the second
> strongest bound. The bound gap to the reported record is `0.1697`.

Replace the sentence “so `s(17) ≥ 4.426213`, above Nagamochi’s general `4.162278` and a
hair below Green’s reported but sourceless `(40√2 + 19)/17 ≈ 4.4452`” accordingly
(Massaccesi’s value is above Green’s reported number), and keep the `think-iye2`
follow-on sentence for the green17 ceiling.

### 6.4 `packing/frontier/n-018.md`

```yaml
  verified_lower_bound:
    value: '4.5058'
    exact_form: '22529/5000'
    evidence:
    - E-n017-massaccesi-source-replay
    - E-n017-massaccesi-h052-agreement
```

Add both ids to the case `evidence` list.
`reported_lower_bound` stays Nagamochi (the precedent after green17). Body, opening
paragraph and “The lower bound” section: state that the operative bound is inherited by
monotonicity from the adopted `n = 17` Massaccesi certificate
(`s(18) ≥ s(17) ≥ 4.5058`), source-backed and replayed here, that the first-party
sixteen-point certificate (`4.426213`, `T-002`) is now the second strongest, and that
the gap to the reported record is `0.3171`. No `n = 18`-specific theorem is claimed.

### 6.5 `packing/frontier/n-019.md`

```yaml
  verified_lower_bound:
    value: '4.5058'
    exact_form: '22529/5000'
    evidence:
    - E-n017-massaccesi-source-replay
    - E-n017-massaccesi-h052-agreement
```

`E-nagamochi-lower` leaves the verified lane’s `evidence` only; it stays in
`reported_lower_bound` and in the case `evidence` list.
Body: the opening sentence “the best proved lower bound is `4.464102` from Nagamochi’s
general theorem, leaving a gap of `0.4215`” becomes the adopted `4.5058` by monotonicity
from `n = 17` with gap `0.3798`; “The lower bound” section replaces “Nothing specific to
this `n` has ever been proved” with the inheritance statement and keeps Nagamochi’s
closed form as the external published baseline (`1 + √12 ≈ 4.4641`, now weaker).
Do not carry the stale “63 of the 65 open cases” sentence into the rewritten body.

### 6.6 `packing/frontier/n-020.md`

No change. Optional one-line body note that the adopted `n = 17` certificate gives
`4.5058 < 1 + √13`, so Nagamochi remains operative here.
The frontmatter must not change.

### 6.7 `packing/src/sqpack/cli/validate.py` — required companion change

The “frontier corpus” full-gate step asserts
`(formal_open, reported_open, nagamochi_count) == (65, 65, 61)`. After `n = 19` stops
citing `E-nagamochi-lower` in its verified lane the count is 60. Change the tuple to
`(65, 65, 60)` and extend the comment: “60 since `<apply-date>`: the adopted Massaccesi
certificate took over the verified lower bound at n = 19.” This file is under concurrent
edit by the H-060 lane; apply against whatever lands.

### 6.8 Companion text and catalogue updates

- `packing/frontier/proof-strategies.yaml`, entry 22, last sentence: replace “The exact
  source verifier replays, but the 4.5058 proposal is not yet independently implemented
  or adopted by this repository” with “The exact source verifier replays, an
  accumulation-independent repository instrument agrees on all 181 direction cells
  (H-052), and the 4.5058 certificate is adopted as a source-backed verified lower bound
  at n = 17–19 (T-015, T-016).”
- `packing/resources/web/n17-lower-bounds-2026/README.md`, the paragraph beginning “The
  extracted verifier was replayed on 31 August 2026”: append the adoption status and
  cite H-052/exp-059 and the BC-150 packet; correct “no replayable audit checklist was
  retained” and “no independent implementation has checked the same certificate”, both
  now false. The source HTML and `.py` files must not change.
- Reader tier: `README.md` line 57 (the `T-001`/`T-002` bullet) and `SYNOPSIS.md` around
  lines 517–584 ("`verified_lower_bound` at `n = 17` and `n = 18` moved to `4.426213`")
  need one sentence each on the adoption; `SYNOPSIS.md` line 1847 and
  `frontier/README.md` say “63 of the 65 open cases” and would read 60 after adoption
  (already stale at 61). The “synopsis agrees with the artifacts” and “README agrees
  with the directory” record checks run on these files.
- `evidence.yaml` `last_reviewed` (`2026-08-25`) and `results.yaml` `last_reviewed`
  (`2026-08-31`): bump to `<apply-date>` if BC-151 follows the green17 precedent.

### 6.9 Regeneration and gates, in order

```shell
cd packing
uv run --frozen python -m devtools.validate_schemas
uv run --frozen python -m devtools.render_research_tables         # STATUS.md and research tables
uv run --frozen python -m devtools.render_results --update         # RESULTS.md
uv run --frozen python -m devtools.render_evidence_inventory --update   # INVENTORY.md
uv run --frozen python -m devtools.check_results
uv run --frozen python -m devtools.check_nagamochi_bounds
uv run --frozen python -m devtools.check_basic_bounds
uv run --frozen --all-extras --group dev packing-validate --records
uv run --frozen --all-extras --group dev packing-validate --push
uv run --frozen --all-extras --group dev packing-validate --only "frontier corpus"
```

Expected `STATUS.md` rows after regeneration:

| `n` | verified lower before | verified lower after | gap-or-conflict column after |
| ---: | --- | --- | --- |
| 17 | `4426213/1000000` | `22529/5000` | “formal upper trails report” (the “formal lower differs from report” flag clears if the reported lane moves with it; stays if not) |
| 18 | `4426213/1000000` | `22529/5000` | “formal lower differs from report” (reported stays Nagamochi) |
| 19 | `1 + √12` | `22529/5000` | “formal lower differs from report” (reported stays Nagamochi) |
| 20 | `1 + √13` | `1 + √13` | unchanged |

`check_nagamochi_bounds` skips `n = 19` after the change (it only checks cases whose
verified lane cites `E-nagamochi-lower`); `check_results` must derive `V4/C3` for both
new results; the frontier-corpus step must report 60 Nagamochi-bounded open cases.

## 7. Claim Boundary

What this route establishes: the repository adopts an externally proposed, exact,
replayed and audited certificate as its verified lower bound at `n = 17, 18, 19`. What
it does not establish: any first-party theorem, any independent proof method, any
generalization of the LP construction to other `n`, or peer-reviewed status for the
source. H-052’s acceptance and this adoption are different decisions; the first is
assurance evidence about two implementations, the second is a source-backed frontier
change that this packet recommends and BC-151 decides.
Non-adoption by BC-151 would be an assurance determination, not a mathematical
refutation.

## 8. Replay Register for BC-150

All under `scratchpad/bc150/`. Scripts import nothing from the repository or the source;
they read the retained verifier only for its hash-pinned literal data.

| Path | Purpose | SHA-256 |
| --- | --- | --- |
| `retained-verifier.sha256`, `retained-verifier-replay.log` | replay of the retained verifier under normal Python, 5.3 s | log `68b925923c7a6b54cb6bc391642b6eea1f759c503afa4abc12275ecc7094358a` |
| `independent_audit.py` | Parts A–E (fixture, net, monotone arithmetic, 181 `B`-square sweeps with boundary evaluation, 380 unit-square sweeps off the net); about 3.5 min | `517941b5f8cfdf9e941f6c747e455f1ce207052f176a87fe5e4687e048431025` |
| `independent-audit.json`, `independent-audit.log` | its complete output, every row | `f5c47fc69241914c20fa229a97a49eb4883b039a1435f498b473516feb0578b4`, `a6257d7053bf047db446de8075848a793c6ab5aa05f8f3f3567f89c05a831971` |
| `crosscheck_record.py`, `crosscheck-record.json` | atom and direction hashes, 181 cell counts and minima against exp-059 | `92b54c8cf581e835ce5752887c06e0ce866d55e92cc5fb7a9cc9e9a0cfde8139`, `fbc29f22b54f77caf1a000dbfe9612a07d63b0c6c303fc6e698b2def9cba6ad1` |

Replay:
`cd scratchpad/bc150 && /home/user/squares/packing/.venv/bin/python3 independent_audit.py && /home/user/squares/packing/.venv/bin/python3 crosscheck_record.py`.
Both scripts refuse to run if the retained verifier’s hash drifts.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
