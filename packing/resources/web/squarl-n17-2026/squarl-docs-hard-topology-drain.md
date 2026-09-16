# Retained hard-topology drain

`hard-topology-drain-20260804t204824z` ran for 3h 59m without generating
roots or updating weights. It canonicalised the 199-entry source queue to 156
material continuations and left 144 ordered pending entries after processing
12 queue states. The audit found 158 candidate IDs, 120 raw hashes, 157
optimised states and 143 material continuation basins. Forty-one entries were
duplicate optimised states, one merged into the `4.677648...` family, and one
was irrecoverable. No retained state exactly matched the published-record
material basin.

The drain processed 76 jobs. It saved 310 high-precision candidates, 310
float32-safe candidates, 310 geometry certificates and 310 double-replay logs.
The best strict float64 state was `4.675530187520610`, which is
`9.39e-8` above the published reference. Its deterministic replay was
`4.675530329141030`; stricter LP and nearby-start checks did not establish a
record or record-basin equivalence.

The missing priority-zero clustered state was recovered unchanged at float64
`4.6761251124189345`. High-precision-rounded and float32-safe replay widths
were `4.676125220823666` and `4.676125872485721`. A saved one-angle stage
improved to float64 `4.676123513345406` and replay `4.676123591669321`.

The best newly refined productive chains were:

| Parent | Float64 | Replay |
|---|---:|---:|
| root 37, `best-non-record-revisit-35` | 4.675623713288518 | 4.675623820710515 |
| root 62, `best-non-record-revisit-26` | 4.675684987880598 | 4.675685064601630 |
| root 50, `best-non-record-revisit-12` | 4.675718556354253 | 4.675718619115896 |

The next eight-hour non-learning run should use 40-proposal blocks: 16 archive
mutations split 6/5/5 over those three parents, 12 separator-boundary mutations
split four per parent, eight fresh topology kicks, and four frozen-source
proposals. Centre LP ranks the queue; critic predictions do not. Send the best
centre-LP candidate plus one physically distinct certificate hedge to
60-second cooperative deep polish, extending to 180 seconds only below
`4.6765`. Reserve the final 90 minutes for the unfinished root-19 chain, these
three parents, and the first 32 entries of the corrected queue.

The full local result is under
`data/experiments/hard-topology-drain/hard-topology-drain-20260804t204824z/`.
`final-report.json` enumerates every saved result below `4.6765`, while
`per-job-continuation-report.json` contains every job and numerical failure.

