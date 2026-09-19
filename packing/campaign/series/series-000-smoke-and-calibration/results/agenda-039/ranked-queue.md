# Session-141 Ranked Covering Queue

Status: **ranked**. Walker file is `rank-queue.yaml`. Optional follow-ups are
`optional-queue.yaml`. Do not walk agenda-038 leftover or first-wave queues.

A restricted optimum already above `n` cannot retain on more wall of the same site set.
Remaining rows raise that value. Adding sites can still lower it. Leftover wall goes to
an untried side or an untried site set.

## Ranked queue

| Rank | Bead | Claim | n | Side | Site set | Deadline |
| ---: | --- | --- | ---: | --- | --- | ---: |
| 1 | think-u11x | H-219 | 18 | `1871/400` | T-028 auto plus windows 5 | **T-029 retained** |
| 2 | think-so2k | H-218 | 20 | `971/200` | T-021 four-grid `(34,46,56,64)` plus windows 7 | **19.857588 unconverged** |
| 2b | think-so2k | H-218 | 20 | `243/50` | same four-grid plus windows 7 | **19.887914 unconverged** |
| 3 | think-coet | H-220 | 32 | `29/5` | auto plus windows 5, no seed | **29.803318 unconverged** |
| 4 | think-coet | H-220 | 31 | `57/10` | auto plus windows 5, no seed | **28.331329 unconverged** |
| 5 | think-coet | H-220 | 30 | `559/100` | auto plus windows 5, no seed | **27.178193 unconverged** |
| 6 | think-coet | H-220 | 26 | `513/100` | auto plus windows 5, no seed | **25.000000 unconverged** |
| 7 | think-coet | H-220 | 27 | `525/100` | auto plus windows 5, no seed | **25.000000 unconverged** |
| 8 | think-coet | H-220 | 29 | `548/100` | auto plus windows 5, no seed | **26.040745 freeze; interval refused** |
| 9 | think-coet | H-220 | 45 | `684/100` | auto plus windows 5, no seed | **42.137360 unconverged** |
| 10 | think-coet | H-220 | 44 | `675/100` | auto plus windows 5, no seed | **41.236782 unconverged** |
| 11 | think-so2k | H-218 | 19 | `481/100` | T-020 four-grid `(34,45,56,64)` plus windows 7 | **19.111435 unconverged; crossed 19** |
| 12 | think-so2k | H-218 | 12 | `793/200` | T-017 auto plus windows 7 | **12.067502 unconverged; crossed 12** |
| 13 | think-so2k | H-218 | 12 | `397/100` | T-017 auto plus windows 7 | **12.097146 unconverged; crossed 12** |
| 14 | think-so2k | H-218 | 19 | `241/50` | T-020 four-grid `(34,45,56,64)` plus windows 7 | **19.224565 unconverged; crossed 19** |
| 15 | think-so2k | H-218 | 12 | `793/200` | T-017 four-grid `(26,35,43,48)` plus windows 7 | **12.066995 unconverged; crossed 12** |
| 16 | think-u11x | H-221 | 18 | `4679/1000` | T-029 auto plus windows 5 | **T-030 retained** |

Insert optional rank 1b (n=18 four-grid plus windows 5, 1800 s) only if rank 1 stays
below 18 unconverged. Insert optional n=20 `243/50` only if rank 2 stays below 20 and
does not retain. Do not walk n=17 `231/50`: nearby auto plus windows 5 already crossed
17 at `461/100`. The live walker loaded the file before ranks 11–12 were appended;
the 11:26Z resume picks them up.

First walker `--stop-at 2026-09-19T10:26:00Z`. Resume the same file after W5 with
`--stop-at 2026-09-19T15:26:00Z`. Halt on freeze mass `< n`. T-id only on `RETAINABLE`.

## Do not replay

| n | Side | Site set | Why |
| ---: | --- | --- | --- |
| 18 | `187/40` | T-027 auto plus windows 5 | T-028 retained at `17.879034` |
| 32 | `29/5` | seedless auto plus windows 5 | Session-141 `29.803318` unconverged; remaining rows raise |
| 31 | `57/10` | seedless auto plus windows 5 | Session-141 `28.331329` unconverged; remaining rows raise |
| 30 | `559/100` | seedless auto plus windows 5 | Session-141 `27.178193` unconverged; remaining rows raise |
| 26 | `513/100` | seedless auto plus windows 5 | Session-141 `25.000000` unconverged; remaining rows raise |
| 27 | `525/100` | seedless auto plus windows 5 | Session-141 `25.000000` unconverged; remaining rows raise |
| 29 | `548/100` | seedless auto plus windows 5 | Session-141 freeze mass `26.0409395`; interval refused; do not more-wall |
| 45 | `684/100` | seedless auto plus windows 5 | Session-141 `42.137360` unconverged; remaining rows raise |
| 44 | `675/100` | seedless auto plus windows 5 | Session-141 `41.236782` unconverged; remaining rows raise |
| 18 | `1871/400` | T-028 auto plus windows 5 | T-029 retained at `17.889237` |
| 18 | `4679/1000` | T-029 auto plus windows 5 | T-030 retained at `17.893285` |
| 18 | `117/25` | every named seed | Locked at `18.000000` |
| 18 | `469/100`, `47/10` | T-019 auto | Plateau or above 18 |
| 20 | `971/200` | T-021 auto plus windows 6 | `19.910044` unconverged; remaining rows raise |
| 20 | `971/200` | T-021 four-grid plus windows 7 | Session-141 `19.857588` unconverged; remaining rows raise |
| 20 | `243/50` | T-021 four-grid plus windows 7 | Session-141 `19.887914` unconverged; remaining rows raise |
| 19 | `481/100` | T-020 four-grid plus windows 7 | Session-141 `19.111435` unconverged; crossed 19; remaining rows raise |
| 12 | `793/200` | T-017 auto plus windows 7 | Session-141 `12.067502` unconverged; crossed 12; remaining rows raise |
| 12 | `397/100` | T-017 auto plus windows 7 | Session-141 `12.097146` unconverged; crossed 12; remaining rows raise |
| 19 | `241/50` | T-020 four-grid plus windows 7 | Session-141 `19.224565` unconverged; crossed 19; remaining rows raise |
| 12 | `793/200` | T-017 four-grid plus windows 7 | Session-141 `12.066995` unconverged; crossed 12; remaining rows raise |
| 20 | `973/200` | T-021 four-grid plus windows 7 | `19.939212` after 2400 s; remaining rows raise |
| 20 | `973/200` | H-062 auto-grid and cert-seed | Already crossed 20 |
| 21 | `97/20` | T-021 auto plus windows 6 | Same side as T-021 |
| 12 | `397/100` | T-017 four-grid plus windows 7 | Converged `12.133391` |
| 12 | `3969/1000` | T-017 four-grid `(26,35,43,48)` plus windows 7 | `12.091168`, crossed 12 |
| 17 | `23/5`, `461/100` | Session-140 named sets | Already above 17 |
| 19 | `241/50`, `481/100`, `97/20` | T-020 auto plus windows 6 | Already above 19 |
| 11 | any side above T-026 | stock covering | Covering-only; T-026 stands |

n=18 `1871/400` does not confirm H-218. n=18 `4679/1000` retained T-030
and does not confirm H-218. n=20 `971/200` and `243/50` four-grid did not.
H-218 stays unconfirmed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
