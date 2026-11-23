# Independent occupied-path and D4 covariance audit

The independent checker verifies every occupied five-tile path for the one-axis problem,
the local exclusion predicate under both generating reflections, and the corresponding
D4 maps of cells, diagonal edges, paths and Boolean clauses.

| Check | Completed |
| --- | ---: |
| Vacancy patterns | 120 |
| Occupied paths | 18,128 |
| D4 geometry maps | 960 |
| Path images | 145,024 |
| Local profile comparisons | 58,016 |
| Predeclared controls | 13 |

Both path constructions agree: choosing occupied cells from consecutive layers and
mapping every universal rank walk into the occupied board.
The local audit compares the complete normal-choice polynomial multisets, as well as the
exclusion verdicts, under forward and transverse reflection.
The [receipt](path-covariance.json.gz) retains the full geometry and every cell, edge
and path permutation.

The domain is `0 < tan(theta/2) <= 1/24`, one aligned tile, nineteen independently
signed common-magnitude tilts, and a hypothetical board `S < 5`, under the reviewed
near-grid premises. It uses the accepted
[general-path catalogue](../review-one-axis-general-paths/README.md) as immutable data;
it does not rerun its polynomial arithmetic.

The [review and frozen plan](frozen-review-plan.md) derives the covariance explicitly.
Reflections negate tilt signs; rotations preserve them.
Graph bits are complemented exactly when a symmetry swaps the coordinate axes.
The source’s vertical transverse rank is `4-x`. Using x with unchanged signs would
change a known local verdict.

The reviewer had read the contributor’s source and prepared the preceding independent
slices. This is disclosed-exposure first-party code, not a blind review.
No contributor program was imported or executed.

## Frozen evidence and reproduction

The [checker](checker.py.txt) is byte-identical to the original
`check_path_covariance.py`. The [freeze](freeze.json) and frozen plan describe
preparation before the completed run.
The [retention map](retention.json) resolves original local filenames to maintained
repository files. The accepted catalogue is retained once in its own evidence directory.

From this directory, with the project Python 3.14 interpreter and an external
supervisor:

```bash
"$PYTHON" -I -B checker.py.txt \
  --input ../review-one-axis-general-paths/general-path-catalogue.json.gz \
  --output "$OUT/path-covariance.json"
```

Use a new output path, one worker and external scratch/cache directories.
Retain the frozen 60-second wall ceiling, 0.25 GiB process-tree ceiling and
pressure-level-2 stop; the checker has a 55-second internal ceiling.

Worker and guard exited zero.
The run took 3.838 supervised seconds and 3.553 worker seconds, with 116,080,640 bytes
peak worker RSS (110.7 MiB). The supervisor, admission reading, complete journal,
observer log and worker log are retained under [execution evidence](execution.run.json).
Their original paths describe the historical run; replay uses the maintained input path
above. Sampled process-tree footprint is distinct from worker peak RSS.

This finite covariance audit does not enumerate separation graphs.
The separate [case-to-clause audit](../review-one-axis-case-clauses/README.md) applies
the accepted catalogue to all canonical census cases.
Global graph enumeration, geometric rule extraction and graph-to-bank coverage remain
open. The one-axis theorem has not cleared Stage 4.

## Compressed Files

| Stored path | Origin | Git blob of original bytes | SHA-256 of original bytes |
| --- | --- | --- | --- |
| `path-covariance.json.gz` | receipt | `765b49a96829d2f5122a65f1af4475b3634deb21` | `2a9a4d4df1c2e42b345225ebb1dfc5417c3a121e1562056e3a2d30456a533a90` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
