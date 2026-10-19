# Replay receipts

These reports attest complete interval checks, including family structure,
input hashes, root domains, leaf tilings, and acceptance of every recorded leaf:

| Report | Index | Roots | Leaves | Refusals |
| --- | ---: | ---: | ---: | ---: |
| interval_0_0.02.json | 1 | 40,257 | 1,653,457 | 0 |
| interval_0.99_1.json | 34 | 50,787 | 1,485,224 | 0 |

Both reports have `ok: true`, `partial: false`, and `incomplete: false`.
They are byte-for-byte copies of the production reports, including their relative
input paths. They are evidence of runs, not substitutes for recomputation.

## SHA-256 of these files

```text
9b228bb8e520ab4cf9daabbd65fb5ebfe96b01c9b283373979474001163bf547  interval_0_0.02.json
78febff2f83cb981e022403e3084437a1de9e0f5c8d141c4943f1ece7a78a125  interval_0.99_1.json
107c8ee7af326c091beb4bd2506f98bb3655fde2da310b602c7d615c14d78ec2  progress_sha256.txt
```

`progress_sha256.txt` records final checkpoint hashes and accepted-root counts.
The checkpoint files themselves are not included. Report input hashes describe
checkpoint bytes read at startup, so they can differ from final hashes after
appends; an empty startup file has the SHA-256 of empty bytes. Interval 1 resumed
24,226 roots, and its timing fields omit their earlier computations. Interval 34
resumed none. Full historical CPU usage cannot be recovered from these reports.
