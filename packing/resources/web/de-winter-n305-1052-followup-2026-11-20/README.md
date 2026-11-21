# De Winter’s #1052 Follow-Up at 305

The exact comparisons in this packet confirm that the corrected corner witness preserves
T-336 and that the precision candidate is exactly T-336 contracted to first contact.
Both alignment variants are now verified at its exact side on both maintained routes,
with their positive, gross-refusal and sharp controls complete.
A 36-turn version with square 43 restored is also feasible with the same nine moved
centers.
The finite hitting-set minimum is nine; the geometric minimum-nine claim remains
conditional on 34 unverified local exclusions, tracked on think-3n8h. T-336’s accepted
certificate and V3/C3 house standing remain unchanged.

Joost de Winter submitted these claims in
[comment 7058958734](https://github.com/jlevy/squares/issues/1052#issuecomment-7058958734).
The
[source mirror](https://github.com/JoostdeWinter/square-packing/tree/dad9c3fd3443bcb9f8950bc302445bdf1e3fbbcc/attachments)
is pinned to `dad9c3fd3443bcb9f8950bc302445bdf1e3fbbcc`, committed 21 November 2026 at
07:05 UTC. The packet name retains the original submission date; acquisition was on 21
November. The exact retrieval time, retained members and pinned-only files are in
[the custody manifest](acquisition/manifest.json).

## Computed Findings

[The comparison receipt](receipts/comparisons.json) records exact rational results:

| Claim | Computed finding | Remaining check |
| --- | --- | --- |
| Corrected witness | Removing seven metadata lines restores the original YAML bytes; all 1,220 corners equal the accepted JSON geometry | None for this artifact identity |
| 31-turn variant | Same exact side, no moved centers, 31 changed directions, 207 axis-aligned squares; both routes accept all 46,360 pairs | Drawing review only; no new bound |
| 37-turn variant | Same exact side, 37 changed directions, 213 axis-aligned squares; both routes accept all 46,360 pairs | Drawing review only; no new bound |
| 36-turn version, square 43 kept | Restore only square 43’s original half-angle in the 37-turn candidate; both routes accept all 46,360 pairs, with the same nine centers moved by at most 2e-11 per coordinate | This establishes sufficiency, not necessity |
| Maximum 31 fixed-center snaps | The feasible 31-turn witness and five exact blocking pairs establish maximum 31, with original centers and side, all other directions fixed, and each of the specified 36 directions kept or snapped | Complete for this restricted claim |
| Minimum nine moved centers | The 17 submitted conflict groups have hitting-set minimum nine, with 1,581 minimizers and 10,991 search nodes; the nine moved IDs hit every group | All 34 local geometric exclusions still require review and replay before nine is a geometric minimum |
| Export reconstruction | All 610 center coordinates and 305 half-angle tangents satisfy the claimed grids and exact side-rounding identity | Historical export settings and intent are not established |
| Precision candidate | Its exact side and all 305 poses equal the accepted first-contact contraction; the side difference is zero | No new upper-bound result follows |

With $Q=10^{82}$, the centers are on the $1/Q$ grid multiplied by $1+3/Q$, and each
half-angle tangent is on the $1/Q$ grid.
The reconstructed pre-expansion extent is $H=S-54/Q$, and $S=\lceil Q(1+3/Q)H\rceil/Q$.
A common translation and trim, computed by the maintained contraction function with
factor one, removes approximately $3.162732483775234\times10^{-82}$ from the side.

The precision candidate equals
[the original contraction receipt](../de-winter-n305-1052-review-2026-11-20/out/contraction-1052.json),
including every rational center and half-angle tangent.
Its gain is approximately $3.20427\times10^{-81}$, already established by that receipt,
and its upward 12-place ceiling is 17.945755838742. It is a restatement under
[Option D](../../../campaign/result-import.md#stage-3-record).
The current comparison reuses the accepted contraction factor; it does not recompute
first contact or repeat that receipt’s pair checks.

## Custody and Credit

The ZIP is 510,763 bytes, with SHA-256
`559ab31345d5b3df5ac1c63f92ab4101b619dac3c060fb0e3f78ac83e5292fca`. Acquisition checked
every one of its 26 declared member digests.
[The upstream member manifest](acquisition/upstream-members.sha256) preserves those
digests; the ZIP itself is pinned only.
Nine files are retained: both variant JSONs, the corrected YAML, the movement CSV and
conflict groups, the precision input and candidate, and the two original READMEs.
Source programs, producer verdicts and historical snapshots are pinned only.
No source program was executed.

The original JSON is byte-identical to
[the accepted packet’s copy](../de-winter-n305-2026-11-20/source/n305/n305_exact.json.gz).
This packet refers to that copy instead of duplicating it.
The root MIT licence at the pin is byte-identical to
[the retained licence](../de-winter-upper-bounds-227-229-260-2026-10-17/source/LICENSE),
copyright 2026 Joost de Winter; it covers his submitted material.
The retained mathematical data and attribution READMEs follow the source-retention
policy. No third-party program is copied from the attachment.

The source [README](source/README.md) credits the arrangement to Tomáš Kodaj and JoeGun
and credits OpenAI Codex for this follow-up, under de Winter’s direction.
The issue credits Codex for the search, optimization and rational certificate and Claude
for repository files, checks and the figure.
The author states that he used GPT6.2 Astra in Codex; that model attribution is a source
statement. The starting Chilton CSV version and its exact relation to T-309 remain
unresolved.

## Completed Replay Evidence

The two supplied variants passed the three maintained full-roster jobs each: positive,
duplicate-square overlap and outside-container refusal.
Both routes evaluated every job, for 12 route outcomes.
The complete inputs and native results are retained in
[31-turn feasibility](receipts/feasibility-31-aligned.json.xz) and
[37-turn feasibility](receipts/feasibility-37-aligned.json.xz).
The routes are `sqpack.verify` and `devtools.check_rational_witness_independent`. The
maintained `validate_receipt` admits both complete records.

The [31-turn](receipts/sharp-controls-31-aligned.json) and
[37-turn](receipts/sharp-controls-37-aligned.json) sharp receipts contain 11 cases each,
with both routes matching every expected verdict, failure category and exact margin: 22
cases and 44 route outcomes.
They cover near-wall translation, far-wall lowering, tightest-pair closing, enlargement
to pair and wall contact, their violations by $10^{-30}$, and duplication.
The enlargement cases test unit-shape refusals as well as geometric margins.

The [square-43-kept receipt](receipts/square43-kept.json.xz) retains the exact deciding
input formed from the 37-turn candidate by restoring only square 43’s original
half-angle. It changes the 36 specified near-axis orientations and nine centers: 108,
140, 141, 142, 143, 150, 153, 164 and 175. Each coordinate moves by at most
$2\times10^{-11}$, and both routes accept the entire packing.
This establishes a feasible witness under either allowed treatment of square 43. The
separate sharp-control runs apply to the original 31- and 37-turn inputs; the restored
version has a two-route positive check only.

| Positive packing | Minimum wall clearance | Minimum pair gap |
| --- | --- | --- |
| 31-turn | $1.5\times10^{-82}$ | approximately $1.7150659269971042\times10^{-82}$ |
| 37-turn | $1.5\times10^{-82}$ | approximately $4.499999999934193\times10^{-126}$ |
| 36-turn, square 43 kept | $1.5\times10^{-82}$ | approximately $4.499999999934193\times10^{-126}$ |

The routes agree exactly on the margins.
[The concise receipt audit](receipts/alignment-results.json) records the rational
values, witness IDs and exact side, and checks each saved native input against its
source or declared construction.
This audit does not rerun geometry or the hitting-set search.

The original six feasibility jobs took 191.617 seconds elapsed; the two sharp runs took
357.590 and 335.422 seconds, below their 900-second ceilings.
Their dedicated passive observers recorded peak process-tree costs of 0.25 and 0.23 GiB
respectively, with normal pressure and no signals.
The square-43-kept positive took 32.603 seconds.
These are historical measurements, not replay acceptance conditions.
[The retention manifest](acquisition/completed-replays.json) identifies the original
first-party receipts in the external evidence archive.
Their bytes are unchanged, or losslessly XZ-compressed where stated.
No additional upstream data or code was retained for this update.
The original custody manifest records the acquisition checkpoint; the completed-replay
manifest and this README state the later results.

## Reproduction and Remaining Proof

[The comparison program](programs/replay_comparisons.py) reproduces the earlier
artifact, reconstruction, five blocking-pair and contraction identities.
[The alignment harness](programs/replay_alignment_results.py) checks the completed
receipts and can replay each calculation through maintained first-party entry points.
Neither loads a contributor program.
The [predeclared plan](receipts/future-controls.md) remains the unchanged record of the
acceptance criteria before execution; its pending language describes that checkpoint.
The current results are above.
These follow-up checks are implementation-aware, not a blind Stage 4 review.

From `packing/`, with Python 3.14.7 and the external scratch variables required by
`AGENTS.md`:

```bash
N305_PACKET=resources/web/de-winter-n305-1052-followup-2026-11-20
PYTHONPATH=.:src uv run --frozen --all-extras --group dev python -B \
  "$N305_PACKET/programs/replay_alignment_results.py" check --repo ..
```

The `check` action verifies source custody and retained receipt identities, binds the
native inputs, and checks saved outcomes and exact margin rules without a proof replay.
To repeat a deciding calculation, substitute one of the following actions and use a
fresh `--out` path outside the retained packet:

```bash
PYTHONPATH=.:src uv run --frozen --all-extras --group dev python -B \
  "$N305_PACKET/programs/replay_alignment_results.py" feasibility --repo .. \
  --variant 31-aligned --control positive --out "$TMPDIR/n305-31-positive.json"
PYTHONPATH=.:src uv run --frozen --all-extras --group dev python -B \
  "$N305_PACKET/programs/replay_alignment_results.py" sharp --repo .. \
  --variant 31-aligned --out "$TMPDIR/n305-31-sharp.json"
PYTHONPATH=.:src uv run --frozen --all-extras --group dev python -B \
  "$N305_PACKET/programs/replay_alignment_results.py" square43 --repo .. \
  --out "$TMPDIR/n305-square43-kept.json"
PYTHONPATH=.:src uv run --frozen --all-extras --group dev python -B \
  "$N305_PACKET/programs/replay_alignment_results.py" hitting-set --repo .. \
  --out "$TMPDIR/n305-hitting-set.json"
```

Use `37-aligned` for the other supplied variant and `duplicate-square-overlap` or
`square-translated-outside-container` for its gross controls.
Each replay compares the fresh result to the retained record, ignoring timing only.
Run one worker under the coordinated passive memory observer.
The harness limits feasibility jobs to 600 seconds, sharp runs to 900 seconds and the
restored witness or hitting-set replay to 120 seconds.
`--startup-delay 5` gives a dedicated observer time to attach.
A failure or timeout is not a confirming replay.

[The complete hitting-set receipt](receipts/hitting-set.json.xz) records all 1,581
minimum covers of the 17 submitted groups, decided by
`devtools.select_n11_field_minimum.minimum_covers` in 10,991 nodes, with two small
recovery controls. This is a combinatorial statement about the retained groups.
If all 34 local geometric exclusions are correct, every admissible moved-center set must
hit every group, so at least nine centers must move.
The geometric premise remains unverified; this packet does not establish minimum nine.

The outstanding input is [local-move-conflicts.json](source/local-move-conflicts.json),
paired with the original exact certificate, the original side, aligned directions for
the specified 36 squares and the $2\times10^{-11}$ coordinate bound.
There are 17 subsets in each of two square-43 orientation cases.
The next proof lane must independently derive the exact linear separation disjunctions,
wall constraints and displacement bounds, preserve the relaxation from omitted tiles,
and retain all 34 controlled solver inputs and results.
The available Python 3.14.7 environment has no `z3` module or `z3` executable, so this
publication pass installed nothing and ran no solver.
The existing hitting-set and witness replay commands above need no new solver runtime.

Drawing selection and the bounded-motion proof remain separate work.
T-336’s original certificate, exact side, house drawing and V3/C3 standing are
unchanged.

## Compressed Files

These rows bind decompressed upstream bytes.
The original source names omit the archive-added `.gz` suffix.

| Stored file | Origin | Git blob of decompressed bytes | SHA-256 of decompressed bytes |
| --- | --- | --- | --- |
| `source/n305_31_quarter_turns.json.gz` | upstream | `52e3a4c0432d0c17bce01c931942f5f2a5fb6bdd` | `97fdbb544b9df751784999231a83e190e6d9cc14c2889d981c3f1268429e570f` |
| `source/n305_37_aligned.json.gz` | upstream | `25c0354cbf7f547143fb3b9ab870628c2d4276fe` | `11bbca8a3e2fc3a238cba51d2011779117a578c4db0c9365d49003c0d0f98500` |
| `source/n305_witness.yaml.gz` | upstream | `580e2c8b7b18bcac110f94672f7d2240e8f2a074` | `1098f986ff0ab6ecc56454d19292f995627131cf7fdbf27cca2d68db6cfe4d82` |

## Original Gzip Files

These upstream gzip files are retained without recompression.

| Stored file | Origin | Git blob of stored bytes | SHA-256 of stored bytes |
| --- | --- | --- | --- |
| `source/precision/n305-candidate.json.gz` | upstream | `e1c1a6f19aaa3fe4b9acae73bbd3498b17acfd38` | `ae59fb0d8b88020aa499e650263c250bd3908d51a5b0b48ed7e4ea646b45ba53` |
| `source/precision/input.json.gz` | upstream | `514540569c3669eb862ea370b8e12aa85fa82b65` | `a33f0888d982b27a2769234118f2c8e4c794bb232529a523528d8104df95dbd1` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
