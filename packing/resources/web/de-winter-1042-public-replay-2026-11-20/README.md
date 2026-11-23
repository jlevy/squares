# De Winter’s 155-Count Public Replay: Retention and Triage

This packet retains the exact archive in
[issue 1042, comment 7022143149](https://github.com/jlevy/squares/issues/1042#issuecomment-7022143149).
The comment was posted on 19 November 2026 at 21:02:44 UTC and edited on 20 November at
02:02:32 UTC. The retained revision requests lower bounds at 155 distinct counts from 18
to 313. It withdraws the 19-square claim; that count is absent from the archive.
The intake owner is `think-4iec`.

The source key proposed for this revision is
`[de Winter issue 1042 public replay 2026-11-20]`. The date identifies the retained
revision, while report order keeps the comment’s original timestamp.
No reconstruction of the earlier comment revision or claim about when each edited byte
first appeared is made.
Joost de Winter directed the work, Hiroaki Hosono supplied the underlying measures, and
the comment identifies GPT6.2 Astra as the AI author.
The seven `registered_boundary` rows also name this project’s retained measures and
coverage receipts. Those inputs remain separately attributed dependencies.

## Custody

The single base85 block decodes to the original 48,944-byte
[ZIP](source/squaremath_public_replay.zip), SHA-256
`2035790a40ac73479e047dc6a6a861137295468458ab6b015c4aad5ebd61c3ab`.
[The manifest](acquisition/comment-archive.json) records the official API response, exact
comment text, archive identity and all four members.
[The comment text](source/issuecomment-7022143149.raw.md),
[certificate](source/certificate.json),
[embedded program texts](source/replay_sources.json),
[launcher](source/verify_public.py) and [source README](source/README.md) retain their
bytes. The archive contains no separate LICENSE member; its README points to the credit
and licence notices in the pinned public source.

The producer’s source dependency is `JoostdeWinter/square-packing` at
`21d944c43098e2261ab7d713cd10f02a5eb13f3d`, under `lower_bounds_2026_11_19/`. The
earlier [source packet](../de-winter-lower-bounds-2026-11-19/README.md) inventories that
tree.
The compact archive contains 78 source specifications, five repair descriptions and
76 boundary descriptions; its 13 embedded Python texts are data in this intake.
No contributor program, imported module, compiler, geometric verifier or coverage replay
ran here.

## Exact Scalar Dispositions

The [per-count index](receipts/claim-dispositions.tsv) and
[full receipt](receipts/scalar-triage.json.gz) preserve each original endpoint,
predecessor and comparison basis.
They were computed from the retained tables on main
`de145a9905bf6bbd6050d72ee06e5fc0770061b3`.

- All 155 rational sides strictly exceed the archive’s own stated previous endpoints.
- All 94 rows that state a mass satisfy `0 < mass < n`. This checks the stated numbers,
  not the reconstructed measure or its coverage.
- Against the 139-row walk of #1039, #1041, #1042 and the 161 follow-up, 79 counts have
  a same-count predecessor.
  At 154 counts the new side exceeds that earlier walk’s monotone floor; 18 has no
  predecessor in this scoped walk.
- The new report has 148 primary rows and seven monotonicity consequences: 102 from 101,
  123–125 from 122, and 146–148 from 145. These are row dispositions, not a proposed
  number of register entries.
- All 153 endpoints also appearing in the later
  [#1060 Attachment D](../de-winter-1060-1063-2026-11-21/lower/D/claims-final.csv.gz)
  are strictly smaller than D’s endpoints.
  The remaining counts are 18 and 20. Later reports do not erase earlier report order.

This comparison does not inspect every current case lane or every intervening report.
In particular, #1055’s later claims at 20 and the separate 18-square proof belong in the
final current-standing check.
No bound, verification rung, confirmation rung or adoption changes here.

## Proof Work by Method

The method names below are the archive’s labels.
The dispositions come from its claim fields and the dispatch in the embedded
`verify_public.py`; they do not assert that its implementation is sound.
The per-count index identifies every member of each group.

| Method | Rows | Remaining obligation |
| --- | ---: | --- |
| `family_cut` | 61 | Establish T-180’s coverage on the unchanged region, identify the inherited family, then review and replay both reflected modified corners over their full angular domain. Scalar mass savings do not discharge global coverage. |
| `registered_boundary` | 7 | Bind the seven registered input/receipt pairs, verify their full premise and coverage scope, and review the new core/centre-margin transfer and boundary correction. Counts: 18, 28, 42, 53, 55, 56, 94. |
| `archived_boundary` | 15 | Recover the exact #1039 archive dependencies and inherited direction receipts; review and replay each changed boundary. Reuse neither the old endpoint nor a partial census as proof of the new side. |
| `boundary` | 43 | Ten rows use published certificate folders and 33 reconstruct transformed measures. Check their source/transform identities, complete anchor coverage and new boundary angular coverage. |
| `direct` | 6 | Reconstruct the six transformed measures, verify nonnegative mass and the stated total, and replay the full new angular cover. Counts: 29, 30, 72, 74, 84, 129. |
| `mixed_gap` | 10 | Review the mixed-core transfer and its angular coverage for 101, 122 and 145. The other seven rows inherit their respective parent by monotonicity. |
| `native_reserve` | 1 | At 50, verify the inherited native receipt and the exact loss-budget transfer; the scalar endpoint gain alone is insufficient. |
| `derived_boundary` | 10 | Check the foundation, any strip extension and corner repair, and the final boundary coverage. Counts: 135, 137, 138, 160, 187–189, 218, 248, 281. |
| `corner_copy` | 1 | At 216, verify the modified-corner coverage and copy/extension geometry, then its exact scaled mass. |
| `periodic_boundary` | 1 | At 217, verify the corrected 161-square anchor’s boundary coverage and the periodic extension premises and mass. |

The T-180-dependent counts are 152–159, 179–186, 207–215, 235–240, 242–246, 267–272,
274–279 and 301–313. The other 94 rows still require the obligations above; they are not
automatically blocked on T-180. Some inherit the earlier reports’ own unfinished
coverage, which must be tracked by the particular source specification rather than by a
blanket hold. Before any producer execution, review the complete imported-source
boundary, retain the bytes it will read, freeze controls and price the selected work.
The launcher writes and executes the embedded programs; it is not a data-only validation
command.

## Validation Scope

The custody parser rejected duplicate JSON keys, required the exact comment identity and
timestamps, bounded archive/member sizes, checked the archive digest, and refused any
unexpected member or path traversal.
The scalar parser used exact `Fraction` arithmetic and the retained predecessor table;
it imported no project geometry or contributor code.
Both jobs ran under the memory guard, stopped on warning pressure or an incomplete
footprint reading, and had 60-second and 0.15-GiB ceilings.
They completed in 0.027 and 0.085 seconds of worker time, at approximately 25.6 and 23.0
MiB peak RSS. Both worker and guard exits were zero; observed pressure remained 1. The
subsecond jobs each had one admission sample, so the worker’s process-accounting peak is
reported separately from the sampled tree footprint.

The maintained `devtools.lower_bound_claims` current-case walk and records/schema gates
remain coordinator validation after the report fragment is integrated.
The earlier source bytes and the later #1060 table are comparison inputs, not a new
proof check.

| Compressed file | Origin | Git blob of uncompressed original | SHA-256 of uncompressed original |
| --- | --- | --- | --- |
| `receipts/scalar-triage.json.gz` | scalar triage receipt | `44c5ea901099b35e70d567aff5972f270ee7f822` | `a695b1b0ec27a8c798fa16dda69e88b17446d04ccbc24d40ffa41332ec459b35` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
