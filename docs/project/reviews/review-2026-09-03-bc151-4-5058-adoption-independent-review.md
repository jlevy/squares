# BC-151 — Independent Review of the 4.5058 Adoption Packet

## Provenance and installation

This document is the independent review deliverable of BC-151, which replayed the
source, re-proved the eleven lemmas, checked the certificate against a fifth
from-scratch implementation, and applied the frozen frontier patch on an exact pass,
written on 2026-09-03 in the agenda-016 ten-hour run.
Its author wrote only to `scratchpad/bc151/` -- a container-local directory outside the
repository, which does not survive the session -- and modified no repository file beyond
the frontier patch its own verdict authorised.
It is installed here so that the evidence the records cite outlives that directory.

The source was `373` lines with SHA-256
`5b54c1f7440af4981591a86c371c1afa9f1a61aa857c0a70d1a63bd39b3500ca`, and that hash names
the scratchpad source rather than this file.
The installation added this preface; it altered no classification, verdict, finding,
number, citation, recommendation or claim boundary, and none may be altered here.
References of the form `scratchpad/...` in the body below are the author’s own record of
what was read and where it was written at the time, and are left as written.

* * *

# BC-151 — Independent Review of the BC-150 Adoption Packet (Massaccesi 4.5058 at n = 17, 18, 19)

Agenda 016, block BC-151 (bead think-bagn).
Reviewer: the BC-151 lane, which authored neither the H-052 instrument, exp-059, the
BC-149 review, nor the BC-150 packet.
Date: 2026-09-03. Repository `/home/user/squares`, branch
`claude/squares-pr76-overnight-run-tpc888`, HEAD `eee785d8` at review start (three
commits past the packet’s `ceff4400`: T-014 registered and published, the exact n = 17
result kept out of the mutation snapshot, the run’s reviews installed).
Interpreter `packing/.venv/bin/python3` (Python 3.14.7) throughout; bare `python3` never
invoked. An earlier attempt at this review was terminated by an infrastructure rate
limit; its partial artifacts in `scratchpad/bc151/` (10:29–10:32Z) were not used.
Everything below was re-run under `scratchpad/bc151/fresh/`.

Packet under review: `scratchpad/bc150/adoption-packet.md`, SHA-256
`d88d47b3d0add7822f106c4d0d80af83a7bd99a8ff12f18498589d5fb57b8413` (matches the
commission). It recommends adoption at source-backed scope:
`s(17) >= 22529/5000 = 4.5058`, and by monotonicity `s(18), s(19) >= 4.5058`, as
`V4/C3`, `novelty: previously-published`, with `n = 20` unchanged.

## Classification: PASS — patch applied

Every packet claim I was told to verify rather than transcribe reproduces exactly; the
eleven lemmas hold under my own proofs; my own fifth implementation, built on a
different cell-selection rule and a different membership rule, agrees on every row and
adds two tests the packet did not run (orientations in `(pi/4, pi/2)`, and random poses
with no cell machinery at all).
The rung is `V4/C3` and not `C4`, exactly as the packet says, because every retained
artifact is one method family.
Sections 5–7 record the patch, the before/after bounds and the caveats that travel with
the record.

## 1. Replay Register

All under `scratchpad/bc151/fresh/`. Scripts marked *own* import nothing from the
repository, the source, or BC-150.

| Check | Result |
| --- | --- |
| Retained verifier `04531a54…`, normal Python 3.14.7, `retained-verifier-replay.log` | 168 atoms, `9744/576`, 181 directions, `B(1+D) = 899635478111/900000000000 < 1`, minimum `576/576` at every logged orientation, “CERTIFICATE CONDITIONS VERIFIED”, exit 0, 9.2 s wall on this loaded host (the packet’s 5.3 s was an idle host; the arithmetic is identical) |
| BC-150’s `independent_audit.py` (SHA-256 `517941b5…`), copied unchanged and re-run into my directory, `bc150-audit-replay.log`, `independent-audit.json` | Parts A–E reproduce: D global minimum 1 with boundary minimum 576 on every row; the seven logged cell counts (2025, 92781, 94145, 92873, 91589, 90869, 90221) equal the packet’s; E minimum exactly 1 over all 380 off-net angles |
| exp-059 result `438dfc1f…` and checkpoint `bb45ed2a…` | hashes match the packet; `decision: accepted`, `instrument_valid`, `preconditions_pass`, `all_mutations_rejected`, `exact_manifest_agreement`, both summaries with atom hash `37d35da0…`, direction hash `cc789e1a…`, total `203/12`, global minimum `1/1` |
| Proposed replay command for the second evidence entry (`…successor.run --status …checkpoint.json`) | `all_agree`, `chain_verified`, `complete`, 181 rows, 11 new, last row hash `60e58a70…`, 2.0 s |
| Frontier case files n-017/018/019/020 | byte-identical to the packet’s frozen HEAD blobs (`afae0ee9…`, `5420bc6a…`, `eecdd7b7…`, `afb00305…`); `validate.py` unmodified against HEAD and still asserting `(65, 65, 61)` |
| **`bc151_own_check.py` (own)**, `bc151-own-check.log`, `bc151-own-check.json` | see section 2 |

### 2. The fifth implementation (own)

Hand-transcribed literal data (constants and the 23 seeds), compared by regex against
the hash-pinned retained file before anything runs — a slip aborts.
Then:

- **Fixture and net.** 168 atoms, integer total 9744, `203/12 < 17`, all strictly inside
  the container, invariant under the four D4 generators I chose (`x -> L - x`,
  `y -> L - y`, swap, quarter turn); record atom hash `37d35da0…` and direction hash
  `cc789e1a…` reproduced from my own serialization; 181 exactly-unit first-quadrant
  directions, `(T+1)^2 > 2`, final pair brackets the diagonal, all 180 half-gap tangents
  `<= D`, `B(1+D) = 899635478111/900000000000 < 1`.
- **Part D, 181 net directions, `B`-square.** Cell selection by a per-cell
  *separating-axis test of the open event cell against the closed centre-domain polygon*
  (axes `U`, `V` and the polygon’s two edge normals, whose projections of the domain are
  `[lo, hi]` exactly) — the exact set of cells whose interior meets the domain, not a
  superset. Membership by closed inequalities at the cell midpoint (an interior point);
  mass as an int64 product of 0/1 membership matrices with the weights.
  Results, every row: minimum over the exact-meets set `576`; minimum over the
  re-derived slab/v-range set `576`; closed membership at every corner of every selected
  cell `>= 576`; midpoint membership equals whole-cell containment for every (cell,
  atom) (lemma L6 checked, not assumed); exact-meets set is a subset of the slab set;
  slab counts equal the record’s `event_cell_count` on all 181 rows, total 16,562,293.
  **Finding:** the exact-meets total is *also* 16,562,293 at every direction — the
  source’s “slight superset” contains no spurious cell here.
  Section 3, L7, proves why.
- **Part Q, true unit square (side 1) at 65 orientations strictly inside
  `(pi/4, pi/2)`** (`t = 0.415 + 0.009 m`, `m = 0..64`, all with `s > c`), the range the
  D4 reduction folds away and which no earlier path evaluated: minimum exactly `576/576`
  on the exact-meets set, on the slab set, and at every selected corner.
- **Part R, random poses, no cells.** 30,000 poses of the true unit square — rational
  orientation uniform over `[0, pi/2]`, centre uniform over the closed centre domain —
  scored by direct membership only: minimum `exactly `576/576 = 1`(worst pose at`t =
  24737/200000`, i.e. orientation `2 arctan t`), never below 1`.

## 3. The Eleven Lemmas, Audited

I re-proved each lemma from the statement rather than checking the packet’s wording.
Where the packet’s phrasing is loose I say so; none of the looseness reaches the
conclusion.

**L1 (scaling and disjointness).** Suppose 17 unit squares with pairwise disjoint
interiors lie in `[0, L']^2`, `L' < L`. Scaling by `L/L' > 1` puts squares `P_i` of side
`L/L' > 1` with disjoint interiors into `C = [0, L]^2`. The concentric unit square `Q_i`
(same orientation) lies in `int(P_i)`, so the closed `Q_i` are pairwise disjoint and
each is a closed unit square contained in `C`. Half one gives `mu(Q_i) >= 1`; additivity
and non-negativity give `17 <= sum mu(Q_i) = mu(union Q_i) <= mu(C) = 203/12 < 17`.
Contradiction, so no packing exists at any side below `L`, and `s(17) >= L` directly
from the definition of `s` as an infimum — the packet’s appeal to attainment of the
minimum is unnecessary but harmless.
Convention: interior-disjointness in a closed container is the repository’s; an open
container only strengthens the claim.
Strictness sits in `mu(C) < 17` (margin `1/12`, exact).
Sound.

**L2 (orientations reduce to `[0, pi/4]`).** A square’s orientation is defined modulo
`pi/2`. Reflection in the diagonal `x = y` maps `C` to itself, maps an edge direction
`(cos t, sin t)` to `(sin t, cos t)`, i.e. `t -> pi/2 - t`, and fixes `mu` because the
weighted atom multiset is D4-invariant about `(L/2, L/2)` — verified exactly on the
reconstructed atoms by BC-150 and again by me, and the grid itself is centred
(`M/2 + (L - M) = L - M/2`). So half one for `t in [0, pi/4]` implies it for all `t`.
Sound; and Part Q tests the folded range directly.

**L3 (net coverage).** `psi_k = 2 arctan(kT/180)`, `psi_0 = 0`,
`psi_180 = 2 arctan T > pi/4` iff `T > tan(pi/8) = sqrt 2 - 1` iff `(T+1)^2 > 2`, which
is `500000309449/250000000000 > 2` (a margin of `1.24e-6`, but exact).
For `t` between adjacent net angles the nearer one is within
`arctan t_{k+1} - arctan t_k = arctan(D/(1 + t_k t_{k+1})) <= arctan D < D`. Every
direction `k = 0..180` is swept, so angles slightly beyond `pi/4` are covered too.
Sound.

**L4 (concentric containment).** In the unit square’s frame the concentric `B`-square
rotated by `eps in [0, pi/4]` has vertices with largest coordinate
`(B/2)(cos eps + sin eps)`; convexity makes vertex containment sufficient, so it lies
inside the unit square iff `B(cos eps + sin eps) <= 1`. With `cos eps <= 1`,
`sin eps <= eps` and `eps < D`: `B(cos eps + sin eps) < B(1+D) < 1`. Hence every closed
unit square in `C` contains a closed `B`-square, at a net direction, contained in `C`,
and non-negative weights carry the mass bound up.
Sound.

**L5 (centre domain).** For direction `(c, s)`, `c, s >= 0`, the `B`-square’s extent
from its centre along each axis is `h = B(c+s)/2`, so it lies in `[0, L]^2` iff its
centre lies in `[h, L-h]^2`. The frame `U = cx + sy`, `V = -sx + cy` is the rotation
`R(-theta)`; applying the same map to atoms and centres preserves the membership test.
For `k = 180`, `s > c` slightly; the formula is symmetric.
Sound.

**L6 (membership rectangles, constancy on open cells).** Atom `p` is in the closed
`B`-square centred at `(U, V)` iff `|U - p_U| <= B/2` and `|V - p_V| <= B/2`: a closed
axis-parallel rectangle `R_p`. Its edges are event lines, so no open cell is crossed by
an edge and the mass is constant on each open cell.
Whole-cell containment and midpoint membership coincide — checked on every (cell, atom)
in Part D.

**L7 (completeness of the cell enumeration).** The source keeps slab `i` iff
`u_{i+1} > u_min` and `u_i < u_max`, clips the domain to the closed slab, takes its
`V`-range `[v_lo, v_hi]`, and keeps `j` iff `v_j < v_hi` and `v_{j+1} > v_lo`
(`bisect_right(ve, v_lo) - 1 .. bisect_left(ve, v_hi) - 1` is exactly that set; I
checked the index arithmetic).
If an open cell meets the domain, some domain point has `U` in the open slab, the clip
is a convex set with non-empty interior (the domain has one), so `v_hi > v_lo`, and the
point’s `V` lies in both `[v_lo, v_hi]` and `(v_j, v_{j+1})`. So the kept set contains
every cell that meets the domain.
**Stronger, and new here:** it contains nothing else.
The domain’s `u_min, u_max, v_min, v_max` are themselves event coordinates, so a kept
slab lies inside `[u_min, u_max]` and the domain’s vertical section `[lo(u), hi(u)]` is
non-empty and continuous across it; a cell `(u_i, u_{i+1}) x (v_j, v_{j+1})` that misses
the domain at every `u` is covered by the two disjoint closed sets
`{u : lo(u) >= v_{j+1}}` and `{u : hi(u) <= v_j}`, so lies in one of them, forcing
`v_{j+1} <= v_lo` or `v_j >= v_hi` — exactly the excluded cases.
That is why my separating-axis count equals the slab count at all 181 directions.
The enumeration is complete and, in this instance, exact.

**L8 (boundary points).** `m(z) = sum_p w_p [z in R_p]` with closed `R_p` is upper
semicontinuous, and takes finitely many values, so its minimum over the compact domain
`P` is attained at some `z*`. If `z*` lies on an event line, a neighbourhood has
`m <= m(z*)`; it meets `int(P)` (P is the closure of its interior) in an open set, which
contains a point of some open cell (event lines have measure zero); that cell meets `P`
and carries value `<= m(z*) = min`, hence `= min`. So the minimum over `P` equals the
minimum over open cells meeting `P`, and open cells suffice — the packet’s “attained on
open cells whose closure meets the domain” is looser than needed but its conclusion is
right. BC-150’s edge-and-corner evaluation and my corner evaluation both found `576`
everywhere, so the lemma is also not load-bearing for this instance.

**L9 (totals and the global minimum).** `9744/576 = 203/12 = 16.91666…`; the registered
minimum `576/576 = 1` is the row minimum on all 181 rows in five implementations (source
verifier, two repository paths, BC-149, BC-150, mine); `17 > 203/12`. Tight, as an LP
certificate rounded up should be (I count 172 to 7,272 tight cells per direction).

**L10 (exactness).** The source decides every inequality in `fractions.Fraction`; its
only integer arithmetic is an int64 difference array bounded by `4 * 9744`. The
repository paths are `Fraction` throughout; my path multiplies int64 0/1 matrices by
weights bounded by 9744. No float decides anything anywhere in the chain.

**L11 (monotonicity).** A packing of `n >= 17` unit squares contains a packing of 17.
Exact consequences: `n = 17, 18`: `22529/5000 - 4426213/1000000 = 79587/1000000 > 0`;
`n = 19`: `(L-1)^2 = 307265841/25000000 > 12`, so `L > 1 + sqrt 12`; `n = 20`:
`(L-1)^2 < 13`, so `L < 1 + sqrt 13` and nothing changes.
Also `L < 4.6755…` (n = 17 reported upper), `(2L - 7)^2 < 7` (n = 18) and
`9(L-3)^2 < 32` (n = 19): no conflict field is created.
All recomputed exactly by me.

## 4. Judgements the Commission Asked For

**Is the off-net unit-square sweep (BC-150 Part E) circular?** Partly independent, not
circular, and not a proof.
It evaluates the theorem’s *conclusion* — every closed unit square at that orientation
has mass `>= 1` — at 380 orientations that are not in the net, so it passes through
neither the net-coverage step (L3) nor the containment step (L4); an error in either
would be visible exactly at the net midpoints, which are the worst case for containment.
It does share the per-direction machinery (L5–L8) with Part D. That residue is what my
own path addresses: L7 is now discharged by a different selection rule (and shown
exact), L6 by an equality check, L8 by corner evaluation, and Part R scores random poses
with no events, no cells and no net.
Part E remains a test at 380 angles; the continuum is carried by L3–L4, which are
proved.

**The packet’s strongest objection (one method family).** Correct and weighed.
The retained record — source verifier, repository instrument, exp-059, BC-149 — is one
family: an exact event-cell sweep of a shrunken square over a rational angle net, with
the continuum-to-181 reduction shared by all of them, so H-052’s agreement could not
have caught an error in that reduction.
What discharges the reduction is proof (section 3), replicated by two reviewers, plus
two from-scratch scratch implementations.
Under `epistemics.md` that is `C3`: repository-origin exact-algebraic evidence with a
certificate and a passing replay.
It is not `C4`: both evidence entries have `method: exact-algebraic`, and “two
independently written implementations using the same method still derive C3”. No
pose-space interval audit exists for this bound, and one would need the semicontinuity
argument built in, because the certificate is tight on open cells (naive box splitting
will not terminate at event lines).

**Classification: pass.** Not “bounded caveat”: every caveat below is a scope or
provenance statement the packet already makes, none is a defect in what was checked.

## 5. Patch Application

Applied with `scratchpad/bc151/apply_patch.py`, content-keyed (17 replacements, each
required to match exactly once; a dry run confirmed this before any write).
Result ids re-derived at application time: `T-014` is the last registered id (committed
at `7b4ff870`), `T-015`/`T-016` occur nowhere in the tree, so they are the next free
ids. Evidence ids `E-n017-massaccesi-source-replay` and
`E-n017-massaccesi-h052-agreement` occur nowhere.

Files changed: `packing/frontier/evidence.yaml` (two entries), `results.yaml` (two
results; `last_reviewed` bumped to 2026-09-03 following the green17 precedent),
`n-017.md`, `n-018.md`, `n-019.md` (verified lane, case evidence lists, bodies),
`src/sqpack/cli/validate.py` (`(65, 65, 61)` -> `(65, 65, 60)` with the dated comment);
regenerated `STATUS.md`, `RESULTS.md`, `INVENTORY.md`. `n-020.md` untouched (verified
against HEAD). The exact diff of these nine files is `patch-receipt.diff` (530 lines).

The packet’s companion edit to `proof-strategies.yaml` entry 22 was applied, found to
pull a regeneration of
`docs/project/research/research-2026-08-22-packing-11-unit-squares.md` (the
strategy-catalogue table mirrors the entry), and was **reverted**, because
`docs/project/` is outside my write scope; both are reported in section 8. The
`resources/…/README.md` paragraph in packet §6.8 was likewise not edited.

Discretion exercised: `reported_lower_bound` stays Nagamochi at n = 17, 18 and 19. The
frontier README’s reported lane holds “the strongest literal claims in the named source
set”, the cases’ named source sets (`resources`) do not include the blog post, and that
is how green17 was handled; moving n = 17’s reported lane later is a separate,
reversible edit that would also add the `[Burns–Massaccesi n17]` resource and a coverage
entry.

### Validation after the patch (logs under `validation/`)

| Step | Result |
| --- | --- |
| `devtools.validate_schemas` | 100 frontmatter artifacts + 312 datasets validate (run again after flowmark: same) |
| `devtools.render_research_tables`, `render_results --update`, `render_evidence_inventory --update` | STATUS.md, RESULTS.md, INVENTORY.md regenerated |
| `devtools.check_results` | 16 registered results, every declared rung passes its structural checks, every path resolves, every reader-tier mention exists; RESULTS.md agrees with results.yaml; T-015 and T-016 render as `V4 / C3 / S3 / previously-published` |
| `devtools.check_nagamochi_bounds` | 85 lower bounds re-derived from Theorem 2, all agreeing, none inverted (86 before) |
| `devtools.check_basic_bounds` | 81 exact grid witnesses replayed, 100 cases checked |
| `packing-validate --only "frontier corpus"` | 100 artifacts; formal lane 35 proved, 65 open; reported lane 35 proved, 65 open; **60 formal-open cases use Nagamochi** (61 before); exit 0 |
| `packing-validate --records` | 25 of 26 record steps passed on the first run (12:04Z); the final run against HEAD `204d0534` (12:07Z, `packing_validate_records_final.log`) passes all 26 of 58 named-tier steps, exit 0, synopsis agreeing. The one failure, “synopsis agrees with the artifacts”, lists only defect-log drift — `SYNOPSIS.md` does not state the defect count 427, class table count for validity 114, gate-detector aggregate 61 of 427, open defect D-427 not mentioned — all of which come from `packing/defects.yaml`, which another lane was editing in the working tree throughout this review (I never touched it). Nothing in the failure list concerns the frontier, T-015/T-016, or the adopted bounds |
| `ruff check .`, `ruff format --check .` | all checks passed; 761 files already formatted |
| Declared replay of `E-n017-massaccesi-source-replay`, run from `packing/` exactly as recorded | “CERTIFICATE CONDITIONS VERIFIED … s(17) >= 22529/5000”, 9.0 s |
| Declared replay of `E-n017-massaccesi-h052-agreement` | `all_agree`, `chain_verified`, `complete`, 2.0 s |
| `make format-check` | `n-017.md`, `n-018.md` drifted after my edit; reformatted with the pinned `uvx --from flowmark-rs==0.3.2 flowmark --auto` on the three case files; no frontier drift remains (other lanes’ review documents still drift; not mine) |

The final `--records` run came after flowmark, so the formatted case files are what it
validated.

## 6. Exact Before/After Bounds

| `n` | verified lower before | verified lower after | change | reported lower (unchanged) |
| ---: | --- | --- | --- | --- |
| 17 | `4426213/1000000 = 4.426213` (T-001, green17) | `22529/5000 = 4.5058` (T-015) | `+79587/1000000 = +0.079587` | Nagamochi `4.162277660168` |
| 18 | `4426213/1000000` (T-002, monotone) | `22529/5000` (T-016, monotone) | `+0.079587` | Nagamochi `4.316624790355` |
| 19 | `1 + sqrt 12 = 4.46410161514…` (E-nagamochi-lower) | `22529/5000` (T-016, monotone) | `+0.0416983849…` | Nagamochi `4.464101615138` |
| 20 | `1 + sqrt 13 = 4.60555127546…` | unchanged | none (`(L-1)^2 = 12.2906… < 13`) | Nagamochi |

Gaps to the reported record after adoption: n = 17 `0.1697` (was `0.2493`), n = 18
`0.3171` (was `0.3967`), n = 19 `0.3798` (was `0.4215`). Nagamochi-bounded open cases:
61 -> 60. T-001, T-002, T-003 stay registered and unchanged.

## 7. Caveats That Travel With the Adopted Record

1. **External provenance, not peer reviewed.** The source is a 2026 blog post by an
   individual; its author marks the value “(?)”; its verifier descends from a note
   authored by a language model (GPT-5.6 Pro) for Burns.
   The adopted object is the verifier’s hash-pinned literal data and the argument
   re-proved here, not the prose, which contains transpositions (3.9545 for 2.9545;
   4.45058) and a mis-spaced drawing.
2. **No new first-party mathematics.** What is first-party is the replay, the
   accumulation-independent instrument, and two written audits.
   `novelty: previously-published`, `source_key: [Burns–Massaccesi n17]`.
3. **One method family on the record; `C3`, not `C4`.** Both evidence entries are
   `exact-algebraic` event-cell sweeps over the same reduction.
   The from-scratch evaluators (BC-149, BC-150, BC-151) are scratch, not repository
   artifacts, and are not cited as evidence.
   `next_rung` names the method-distinct certificate.
4. **The LP is not replayed and is not part of the proof.** The weights’ provenance
   (scipy `linprog` at a different geometry, rounded up) is irrelevant to the
   certificate’s validity, which the exact verifier decides.
5. **The retained verifier’s checks are `assert` statements** and vanish under
   `python -O`; replay under normal Python only.
   The repository instrument uses explicit comparisons and its self-test is
   byte-identical under `-O` (BC-149).
6. **The second entry’s replay does not recompute masses**: it verifies the retained
   181-row hash chain in seconds; full recomputation is the executed ~nine-hour run,
   replayable per direction with `--calibrate ORDINAL`. The source verifier recomputes
   everything in seconds.
7. **Independence on the record is accumulation-level** (BC-149): the two repository
   paths share the reduction, the fixture, the projection convention and the
   preconditions. Agreement cannot detect an error there; the audits do.
8. **Comparison of minima is blind to defects that only raise non-minimizing cells**
   (BC-149’s injection table); every lower-bound check here has that scope.
9. **Part E and my Parts Q and R are tests at finitely many angles or poses**, not
   proofs for the continuum; L3–L4 carry the continuum.
10. **Instrument limitations recorded by BC-149** (validator does not tie the rebuilt
    spine to `carried_boundary`; no assembly path from a retained disagreement) are
    untouched and do not bear on the agreement.

## 8. Reported to the Coordinator, Not Applied (outside my write scope)

- `README.md` line 57 (the T-001/T-002 bullet) and `SYNOPSIS.md` around lines 517–584
  need one sentence each on the adoption; `SYNOPSIS.md` lines 1857 and 3704 say “63 of
  the 65 open cases” are Nagamochi-bounded — already stale at 61, now 60.
- `packing/resources/web/n17-lower-bounds-2026/README.md`, the paragraph beginning “The
  extracted verifier was replayed on 31 August 2026”: “no replayable audit checklist was
  retained” and “no independent implementation has checked the same certificate” are now
  false; append the adoption status citing H-052/exp-059, the BC-150 packet and this
  review. The source HTML and `.py` must not change.
- `packing/frontier/proof-strategies.yaml` entry 22, last sentence, still reads “The
  exact source verifier replays, but the 4.5058 proposal is not yet independently
  implemented or adopted by this repository” — now false.
  Replace with: “The exact source verifier replays, an accumulation-independent
  repository instrument agrees on all 181 direction cells (H-052), and the 4.5058
  certificate is adopted as a source-backed verified lower bound at n = 17–19 (T-015,
  T-016; V4/C3, one method family, not peer reviewed).” Then re-run
  `devtools.render_research_tables`, which rewrites the mirrored row 22 in
  `docs/project/research/research-2026-08-22-packing-11-unit-squares.md` (one line).
- `packing/devtools/check_nagamochi_bounds.py` docstring says `E-nagamochi-lower`
  supplies 86 of the hundred verified lower bounds; it is 85 now (the count is not
  asserted; the check passes).
- `TUTORIAL.md` and `docs/project/` were not inspected for stale n = 17–19 bounds.
- The first `--records` run’s synopsis failure (defect-log drift, D-427) was resolved by
  the coordinator’s commit `204d0534`; the final run passes.
- Working-tree files I never wrote but which showed as modified by another lane during
  this review: `defects.md`, `packing/defects.yaml`, and briefly `SYNOPSIS.md`.
- If a reviews document for this review is to be mapped in `document-map.yaml` (the C5
  route), that is a `docs/project/` change.

## 9. Artifacts

| Path (under `scratchpad/bc151/`) | Purpose |
| --- | --- |
| `fresh/retained-verifier-replay.log` | source verifier replay, normal Python |
| `fresh/bc150_independent_audit_copy.py`, `fresh/bc150-audit-replay.log`, `fresh/independent-audit.json` | BC-150 audit replayed unchanged |
| `fresh/bc151_own_check.py`, `fresh/bc151-own-check.log`, `fresh/bc151-own-check.json` | own fifth implementation, Parts D/Q/R |
| `apply_patch.py` | the content-keyed patch, dry-run then applied (its proof-strategies edit later reverted) |
| `patch-receipt.diff` | the exact diff of the nine repository files this block changed |
| `validation/` | logs of every regeneration and gate run after the patch, plus STATUS rows before and after |
| `bc151-review.md` | this document |

SHA-256 of the load-bearing artifacts: `apply_patch.py` `d467661d…`,
`fresh/bc151_own_check.py` `8a86f38e…`, `fresh/bc151-own-check.json` `fd43e8eb…`,
`fresh/bc151-own-check.log` `4abdf7da…`, `fresh/bc150_independent_audit_copy.py`
`517941b5…` (identical to BC-150’s), `fresh/independent-audit.json` `f5c47fc6…`
(byte-identical to BC-150’s own output), `fresh/retained-verifier-replay.log`
`b9861cd6…`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
