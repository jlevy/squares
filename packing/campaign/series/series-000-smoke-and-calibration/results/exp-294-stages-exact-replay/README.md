# Exact Replay Stage Attribution

[exp-294](../../experiments/exp-294-h-302-stages-exact-replay.md) completes the
registered diagnostic criterion.
The fresh STAGES receipt is `COMPLETE` with full `PASS_STALL`; its mathematical payload
and seed/node/cells byte digests equal accepted exp290 NONE. All 16 step owner/count
boundaries equal accepted PHASES. The [mechanical summary](mechanical-summary.json)
retains the independently recomputed joins and stage totals; [stages.json](stages.json)
is the unchanged raw receipt.

Replay wall was 108.237456s and CPU was 104.257205s. Inclusive clocks overlap; exclusive
clocks subtract directly nested observed calls.
Principal exclusive totals:

| Stage | Calls | Wall seconds | CPU seconds |
| --- | ---: | ---: | ---: |
| Coverage | 1024 | 57.292715 | 54.915649 |
| Step work outside observed nested stages | 16 | 23.232524 | 22.460567 |
| Collision regions | 1024 | 10.218034 | 9.985962 |
| Final-state equality | 1 | 10.255051 | 10.137628 |
| Partner admission | 16 | 4.841389 | 4.378378 |
| Compression | 16 | 0.768038 | 0.762767 |

The unattributed residual is 0.224548s wall and 0.223025s CPU, including observer
overhead and unobserved work.
Decode/header observations include canonical digest and EOF work; they are not pure
parsing. No observed call failed.
Facet memo evictions were zero; 192 forbidden-pair entries were removed.
Cache lookup hits were not observed.

Coverage accounts for 52.93% of measured replay wall; collisions account for 9.44%.
Finer coverage attribution is the next diagnostic candidate.
Collision-only support aggregation has limited observed scope here.
This one accepted control under host load does not establish speedup or explain exp284’s
unaccepted replay timeout.

Outer supervision completed normally in 108.620915s, with cleanup complete.
Frozen limits were cooperative replay180s, owned-group TERM190/KILL200, and sampled
current RSS4096MiB per live process at0.25s. Maximum sampled RSS was472891392bytes;
process lifetime peak was472907776bytes and is recorded separately.
No hard allocation or aggregate group-memory cap is claimed.
This is a diagnostic replay, with no new geometric admission or optimality claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
