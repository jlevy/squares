# Independent one-axis case-to-clause audit

The independent checker binds all 3,671 canonical sign/vacancy cases to their occupied
paths, local profile decisions and Boolean exclusion clauses.
The representatives’ disjoint eight-image orbits cover all 29,368 accepted census
assignments.

| Measure | Completed |
| --- | ---: |
| Canonical cases | 3,671 |
| Full census assignments covered | 29,368 |
| Occupied-path applications | 554,159 |
| Excluded path origins and distinct clauses | 339,191 |
| Not-certified path origins | 214,968 |
| Horizontal-path exclusions | 160,115 |
| Vertical-path exclusions | 179,076 |
| Predeclared controls | 13 |

Every case row retains one accepted profile index per occupied path, and every exclusion
clause retains its complete path-origin list.
Literal masks reconstructed from physical endpoint pairs agree with those obtained from
the accepted path geometry.
Bit one means horizontal separation: horizontal-path exclusions use negative literals,
and vertical-path exclusions use positive literals.
No subsumption or graph search is performed.

The 214,968 not-certified occurrences add no clauses.
They are occurrences of the accepted local catalogue’s 5,722 not-certified profiles, not
a new count of distinct profiles or feasible placements.
The [complete receipt](results/case-clauses.json.gz) retains their profile references
alongside all excluded occurrences.

The domain is `0 < tan(theta/2) <= 1/24`, nineteen independently signed common-magnitude
tilts, one aligned tile and `S < 5`, conditional on the reviewed near-grid premises.
This check reuses the accepted
[local catalogue](../review-one-axis-general-paths/README.md),
[sign census](../review-one-axis-sign-census/README.md) and
[path covariance](../review-one-axis-path-covariance/README.md) as data.
It does not re-prove their arithmetic or geometric reductions.

The reviewer had read the producer’s source and prepared the preceding independent
slices. This is a first-party implementation with disclosed exposure.
No producer code was imported or executed.

## Frozen evidence and reproduction

The [checker](checker.py.txt) is unchanged from `check_case_clauses.py`. The
[freeze](freeze.json), [plan](frozen-plan.md) and
[original input checksums](original-input-sha256sums.txt) retain the preparation record.
Their local filenames describe the original external evidence directory.
The [retention map](retention.json) records the actual maintained paths; accepted inputs
are not duplicated here.

From this directory, using project Python 3.14 and an external supervisor:

```bash
"$PYTHON" -I -B checker.py.txt \
  --catalogue ../review-one-axis-general-paths/general-path-catalogue.json.gz \
  --census ../review-one-axis-sign-census/sign-census-isolated.json.gz \
  --covariance ../review-one-axis-path-covariance/path-covariance.json.gz \
  --output "$OUT/case-clauses.json.gz"
```

The unchanged checker accepts the compressed covariance receipt and verifies its
original byte identity after bounded decompression.
The output and its identity sidecar must be new files.
Use one worker, external scratch/cache directories, pressure-1 admission, a 90-second
wall ceiling, 0.35 GiB process-tree ceiling and pressure-level-2 stop.
The internal limits are 85 seconds and 0.33 GiB worker peak RSS. The raw output is
capped at 64 MiB and its gzip at 16 MiB.

The [historical supervisor](strict-supervisor.py.txt) records the original launcher.
Its retained admission reading and all seven journal samples report complete footprint
measurements. For new runs, use [the replay supervisor](replay-with-memory-guard.py.txt).
Pass the installed memory-guard script path, an external log prefix, the wall and GiB
ceilings, and the checker command. The supervisor refuses incomplete footprint
telemetry at admission and during execution.

Worker and guard exited zero.
The run took 7.199 supervised seconds, 6.887 worker seconds and 3.575 CPU seconds.
Peak worker RSS was 139,329,536 bytes (132.875 MiB). All seven guard samples stayed at
pressure 1, with maximum sampled process-tree cost 0.12 GiB and no intervention.

Execution evidence: [supervisor](results/case-execution-01.run.json),
[admission](results/case-execution-01.preflight.json),
[journal](results/case-execution-01.jsonl),
[observer log](results/case-execution-01.guard.stderr),
[worker log](results/case-execution-01.worker.log).
The [identity record](results/case-clauses.json.gz.identity.json) binds the original
24,888,016 bytes to the 785,142-byte deterministic gzip and records the successful
streamed decompression roundtrip.

## Remaining mathematical work

This receipt establishes the complete application of the accepted local path criterion
to the canonical census cases, with explicit orbit binding.
It does not enumerate Boolean models of the clauses.
A separate [sixteen-case graph pilot](../review-one-axis-graph-pilot/README.md) now
retains all 1,280 models for its predeclared selection, with 17 passing controls.
Complete all-case separation-graph enumeration and the subsequent geometric-rule and
graph-to-bank application remain open.
The source’s 273,584 graphs and 566 used certificates remain producer reports.

The accepted bank’s 576 polynomial identities must still be shown applicable to every
surviving graph. The one-axis theorem has not cleared Stage 4. No unrestricted lower
bound, angle-diversity claim, registry value or drawing changes.

## Compressed Files

| Stored path | Origin | Git blob of original bytes | SHA-256 of original bytes |
| --- | --- | --- | --- |
| `results/case-clauses.json.gz` | receipt | `731a840b602de44262fd81b2537642f6186313ef` | `d7dd3ba492405d5b9a61dbd6a18a21164dc9c18b9b1b64d6d4633de6c9f40237` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
