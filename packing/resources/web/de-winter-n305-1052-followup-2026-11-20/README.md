# De Winter’s #1052 Follow-Up at 305

The exact comparisons in this packet confirm that the corrected corner witness preserves
T-336 and that the precision candidate is exactly T-336 contracted to first contact.
The two alignment variants retain its exact side.
Their whole-packing feasibility remains pending on think-rbyl.
The claim that nine moved centers are necessary is tracked separately on think-3n8h.
T-336’s accepted certificate and V3/C3 house standing remain unchanged.

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
| 31-turn variant | Same exact side, no moved centers, 31 changed directions, 207 axis-aligned squares | Both maintained routes must decide the whole packing |
| 37-turn variant | Same exact side, 37 changed directions, 213 axis-aligned squares; nine moved centers, IDs 108, 140, 141, 142, 143, 150, 153, 164 and 175 | Both maintained routes must decide the whole packing |
| Maximum 31 fixed-center snaps | Five exact blocking pairs force original turns at 108, 150, 153, 164 and 175; hence at most 31 can snap under the stated keep-or-snap choices | A feasible 31-snap witness supplies the matching lower bound |
| Minimum nine moved centers | The source supplies 17 conflict groups and claims 34 bounded-motion infeasibility checks | Geometric constraints, solver replay and hitting-set argument remain unreviewed |
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

## Replay and Pending Work

[The replay program](programs/replay_comparisons.py) uses the maintained
`center-direction-json` reader, `devtools.contraction_margin.contract` and the retained
original review’s reader and integer SAT margin function.
It reads the prior proof record without modifying it.
This is a direct-source audit after reading the original review and the contributor’s
claims, not a blind Stage 4 review.

From `packing/`, with the project’s Python 3.14 environment and task scratch variables:

```bash
N305_PACKET=resources/web/de-winter-n305-1052-followup-2026-11-20
PYTHONPATH=.:src uv run --frozen --all-extras --group dev python -B \
  "$N305_PACKET/programs/replay_comparisons.py" --repo .. \
  --check "$N305_PACKET/receipts/comparisons.json"
```

The replay checks ten retained or preexisting member digests and the licence, then
reproduces the saved comparisons.
It makes five local pair decisions; it does not execute the 46,360-pair feasibility
replay for either variant or invoke a solver.
[The predeclared controls](receipts/future-controls.md) separate those pending jobs from
the completed identities.
Each future lane must retain its own verdict and controls before the request ledger
marks it complete.

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
