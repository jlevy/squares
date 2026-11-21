# Drawing runs for the T-336 adoption at 305

On 21 November 2026 UTC, the adoption writer replaced T-309 with
[T-336](../../../frontier/RESULTS.md), Joost de Winter’s refinement of the Kodaj and
JoeGun construction.
The exact side rounds up to $17.945755838742$ at 12 places.
Both strong generators used this new witness under the
[house drawing rule](../../../campaign/result-import.md#adopt-a-house-then-regularize-it).

| Run | Outcome |
| --- | --- |
| Grid-slack at 0.5°, 1° and 5° | No view. Each exact re-solve refused because relaxed rows overlapped at the requested side. The reports retain all attempted row sets. |
| Evan Daniel’s driver at `675a5ea` | The solved view is held at row 4: its certified rational side exceeds the exact registered upper bound by about $1.79457558 \times 10^{-19}$. The same-side attempt refused with `literal-too-large`. |
| Selection | No adopted view and no row 3 candidate. The existing axis view of T-336 remains the drawing at the witness’s exact side. |

The axis view measured by the selector has seven light squares, 63 uneven squares, one
near-axis square, 32 angle classes and 19 hues, with 731 full shared sides on the house
measure and 859 on the stage measure.
The solved view improves these measures, but its larger exact side prevents adoption.
The solver reports `bound only` and an inconclusive second-order result; this packet
makes no local-optimality claim.
Other Joost variants remain separate work under `think-rbyl`.

The grid reports record 320.80, 321.78 and 323.45 elapsed seconds, 966.03 in total.
Evan Daniel’s receipt records 586.43 CPU-seconds and 602.86 wall-seconds with one
worker. The project interpreter was CPython 3.14.7. The memory guard’s retained summary
records 150 pauses and 150 resumes: 1,378.7 seconds paused during 1,847.2 seconds
watched (74.6%), with no processes killed and no abort.

The grid driver emitted per-count reports but no run receipt.
Each `run.json` here is a summary in the maintained `regularize_grid_slack.run_block`
shape, as in the n109 packet.
That shape copies the report’s `perf_counter` elapsed time into both `cpu_seconds` and
`wall_seconds`; the former is not an independent CPU measurement.
These summaries are identified as derived in [retention.json](retention.json).

The four per-count reports, Evan Daniel receipt, certificate and derived Witness/v2 are
retained without changes to their uncompressed bytes.
The selection JSON changes only nine machine-specific path values: the checkout root
becomes `.`, and the run paths become repository-relative paths into this packet.
Its decisions, exact numbers and all other bytes are unchanged.
The Markdown selection output is unchanged.
The guard summary is the single emitted summary record, without process snapshots or
session details. Compression uses gzip with a zero timestamp.

The certificate and derived view have uncompressed SHA-256 digests
`72278190f834c7adc3ebc7c622e22375a11e8321ff26362e36b16afb9a0e0bbe` and
`87615309d42c53e42c1f53b7b5e3f3dc15be43c8167633f138b91fa66db07fe4`. Retention checks
matched all 305 certificate poses to the view’s exact centers and bases, its side to the
rational `S_cert` and `side_exact` fields, and all four artifact digests in the receipt.
The reports and view bind to source witness SHA-256
`68c3d6763753ac0ed7c21548b5c8ab49c007e85f34287716cb62131f69d02f46`. The certified
rational side controls the comparison; the driver’s decimal `S_exact` field does not
establish a smaller bound.
These are custody and representation checks on completed runs, with no additional solver
or geometric verification run.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
