# Frozen Plan: Complete One-Axis Case-to-Clause Audit

This slice will bind every accepted canonical census case to its occupied paths, local
profile decisions and exact Boolean exclusion clauses.
It will retain all 3,671 cases if the declared caps permit completion.
There is no graph enumeration, polynomial positivity rerun or graph-to-bank coverage in
this job.

The checker has not been executed, imported, compiled or syntax-checked.
Its first execution requires the coordinator’s serial guarded slot, admission at macOS
pressure 1, and a fresh external output path.

## Accepted Inputs and Exposure

Three portable data inputs are retained beside the checker:

| Input | Expanded bytes | SHA-256 of expanded bytes |
| --- | ---: | --- |
| General-path catalogue | 14,993,939 | `a60f45a70cb57d4e1a1e58bcbe01b1f9cf1c527fc80c0e931d7e856af22b33bb` |
| Isolated sign census | 5,981,113 | `fc75c5853c16cc99e3cbdda6661ddcfb5a0d6d2b0698c47c9f7747351ccd96fe` |
| Complete path covariance | 1,489,518 | `2a9a4d4df1c2e42b345225ebb1dfc5417c3a121e1562056e3a2d30456a533a90` |

The accepted covariance run completed 120 vacancy geometries, 18,128 occupied paths, 960
D4 maps, 145,024 path images, 58,016 local profile comparisons and 13 controls.
Its worker and guard exited zero; supervised time was 3.838 seconds, and worker peak RSS
was 116,080,640 bytes.
This new slice reuses that accepted geometry and covariance evidence as data.

The reviewer has read the contributor’s source and prepared the prior independent
slices. This is not blind.
The new case binding, orbit application, literal reconstruction and streaming retention
are first-party code; they import no producer module.
The local arithmetic and geometry conclusions are accepted input premises, not
independently re-proved by this checker.

The scope remains the one-axis restricted positive-angle problem:
`0 < tan(theta/2) <= 1/24`, nineteen independently signed common-magnitude tilts, one
aligned tile, and `S < 5`, conditional on the reviewed near-grid reduction.
The zero-angle endpoint remains separate.

## Expected Coverage and Mathematical Condition

Validate the complete 29,008-profile domain and preserve its 23,286 excluded and 5,722
not-certified entries.
The local profile row index is the only profile reference in the new receipt; it is
bound to the accepted raw input above.

Read exactly 3,671 sorted unique canonical representatives and the full 29,368-case
census with orbit indices.
Using the accepted covariance receipt’s cell permutations and determinant flags,
transform each representative through its eight D4 images.
Require eight distinct images per representative, disjoint orbits, each exact census
orbit index, and equality of their union with the complete 29,368-case roster.
This generates 29,368 representative images; it does not repeat the earlier
234,944-image all-cases census check.

For each vacancy, reconstruct the lexicographic occupied-cell roster and its ordered
diagonal edges. For each accepted occupied path, reconstruct its forward ranks, vertical
transverse frame `4-x`, coordinate-to-cell indices and exact diagonal mask.
Require agreement with the accepted geometry before applying signs.

For every canonical case and every occupied path:

1. Decode the global sign mask, enforcing a zero aligned bit and exactly one aligned
   position.
2. Select the five path signs both by stored cell indices and by independently resolved
   rank coordinates; require equality.
3. Find the unique accepted rank/sign profile and retain its index.
4. If the profile is not certified, add no clause.
5. If it is excluded, emit negative literals for a horizontal path and positive literals
   for a vertical path.
6. Independently reconstruct that literal mask from the physical endpoint pairs and the
   complete diagonal-edge roster.
7. Require exact agreement of both complete clause-to-origin maps.

Bit one means horizontal separation.
A clause is satisfied by a selected bit in its positive mask or an unselected bit in its
negative mask. Only identical clauses are deduplicated.
Every excluded path occurs exactly once among the retained clause origins; every
not-certified path occurs zero times.
No subsumption or other pruning is introduced.

The result is the complete set of local-path necessary clauses for every canonical case.
The accepted D4 covariance and the explicit orbit binding extend that set of necessary
conditions to every full census case.
Survival of these clauses is not a geometric feasibility assertion.

## Retained Output

The receipt retains one row for every canonical case, in the census’s fixed order:

- Vacancy, sign mask, aligned index and edge count.
- One local profile index for every path in the accepted geometry’s exact order.
- Every deduplicated positive/negative clause mask with its full path-origin list.
- Counts of excluded and not-certified path origins.

The geometry itself and full local/census data remain portable inputs alongside the new
receipt. No transient checkout or scratch file is needed to interpret the indices.

Stream each case to deterministic gzip using level 6, empty filename and mtime zero.
Keep at most one case’s output in memory.
The raw byte digest and length are accumulated while writing; after closing, a 64 KiB
streaming decompression must reproduce both exactly.
Retain a separate identity/measurement file binding the stored bytes, expanded bytes,
scope, counts and peak RSS. The mathematical receipt contains the ordered case-row
digest and actual profile-use counts.

No expected number of clauses, applied paths or distinct used profiles is guessed.
Those counts are derived and reported.
The conservative application ceiling is 1,901,578 path lookups.
The accepted geometry’s exact 18,128 paths are spread across 120 vacancy patterns;
canonical cases use their own pattern’s complete roster.

## Thirteen Controls

The frozen checker includes these controls before the complete application:

1. Correct decoding around an aligned tile.
2. Refuse a sign mask whose aligned bit is set.
3. Refuse a mask outside the twenty-bit domain.
4. Refuse an aligned index outside the twenty positions.
5. Refuse a duplicated census case.
6. Confirm the accepted all-positive increasing walk remains not certified.
7. Refuse a missing local profile.
8. Confirm a not-certified decision emits no clause.
9. Confirm horizontal exclusions use negative literals.
10. Confirm vertical exclusions use positive literals.
11. Refuse a clause-origin map missing an excluded path.
12. Refuse a clause-origin map with reversed polarity.
13. Confirm aligned-position remapping and reflection sign negation together on a
    hand-calculated twenty-position fixture.

All controls must pass.
A changed input, malformed row, omitted case, orbit discrepancy, missing profile,
mismatched literal/origin map, cap or unexpected exception fails the job.
A partial receipt cannot count as a complete audit.

## Work and Guard Budget

Run one isolated project Python 3.14 worker with `-I -B`. Target under 30 seconds and
0.20 GiB peak RSS. Hard limits are 90 supervised seconds and 0.35 GiB owned process-tree
cost, with admission pressure exactly 1 and stop at pressure 2. Internal checks impose
85 seconds and 0.33 GiB worker peak RSS.

Expanded input ceilings are 32 MiB, 8 MiB and 4 MiB respectively.
A single serialized case is capped at 256 KiB, the complete raw receipt at 64 MiB, and
its gzip at 16 MiB. The bounded writer uses a fresh temporary file and publishes the
result only after all 3,671 cases and the complete orbit partition pass.
Use external evidence for frozen code and unique results, and external scratch for
temporary/cache environment variables.

```bash
"$PYTHON" -I -B check_case_clauses.py \
  --catalogue general-path-catalogue.json.gz \
  --census sign-census-isolated.json.gz \
  --covariance path-covariance.json \
  --output "$OUT/case-clauses.json.gz"
```

The guard receipt must independently establish successful admission, worker completion,
resource limits and absence of intervention.
Worker timings and maximum RSS are separate from sampled process-tree footprint.
If any cap fires, retain the failure and price a frozen case-range pilot or chunking
plan; do not silently narrow the successful claim.

## Remaining Mathematical Work

A complete case-to-clause audit still does not enumerate the satisfying separation
graphs or prove any of them impossible.
The next independently measurable task is a small frozen graph-enumeration pilot using
these exact clauses, followed by full, complete case coverage if its measured cost is
acceptable.

After graph enumeration, each graph’s actual geometric rules must be bound to at least
one accepted polynomial certificate.
The producer’s 273,584 graphs and 566 used certificates remain unverified comparison
counts. Neither a matching count nor the accepted bank’s 576 identities replaces that
application proof.

There is no Stage 4, unrestricted lower-bound, angle-diversity or registry promotion in
this slice.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
