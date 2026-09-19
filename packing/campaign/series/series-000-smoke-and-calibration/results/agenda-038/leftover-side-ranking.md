# Leftover First-Wave Sides

Status: **leftover wall ended**. `think-7igz` closed. Ranks 1–4 finished. Rank 5
(`1871/400`) did not start: leftover n=12 exited at 06:42:04Z with remain −4 s.

A restricted optimum already above `n` cannot retain on more wall of the same site set.
Remaining rows raise that value.
Adding sites can still lower it, so the side stays open, but leftover wall goes to an
untried side or an untried site set, not to a replay that is already above `n`.

The n=20 `973/200` four-grid plus windows 7 2400 s follow-up stopped at `19.939212`
unconverged. That set stays below 20 and is not a retain.
Leftover n=20 `971/200` finished at `19.910044` unconverged, still below 20.

## Queue

| Rank | Bead | n | Side | Site set | Why |
| ---: | --- | ---: | --- | --- | --- |
| 1 | think-zoq4 | 19 | `241/50` | T-020 auto plus windows 6 | Done. Stopped at `19.247109` unconverged after 38 rounds. Crossed 19 at round 12. |
| 2 | think-5q81 | 17 | `461/100` | T-019 auto plus windows 5 | Done. Stopped at `17.195968` unconverged after 56 rounds. Crossed 17 at round 11. |
| 3 | think-d2ad | 20 | `971/200` | T-021 auto plus windows 6 | Done. Stopped at `19.910044` unconverged after 48 rounds. Did not cross 20. |
| 4 | think-h02v | 12 | `3969/1000` | T-017 four-grid `(26,35,43,48)` plus windows 7 | Done. Stopped at `12.091168` unconverged after 36 rounds. Crossed 12 at round 11. Lower than the no-windows four-grid `12.116115`. |
| 5 | think-avmz | 18 | `1871/400` | T-028 auto plus windows 5 | Not started. Remain after leftover n=12 was −4 s. One step above `187/40`. |

## Do not replay

| n | Side | Why leftover wall is wasted for retain |
| ---: | --- | --- |
| 17 | `461/100` | Session-140 leftover auto plus windows 5 stopped at `17.195968`. |
| 17 | `23/5` | Best stock row is `17.042346` (windows 5, 9 violated). Already above 17. |
| 12 | `3969/1000` | Session-140 leftover four-grid plus windows 7 stopped at `12.091168`. |
| 12 | `397/100` | Cert-seed `12.016263`; session-140 four-grid plus windows 7 converged at `12.133391`. |
| 19 | `241/50` | Session-140 leftover auto plus windows 6 stopped at `19.247109`. |
| 19 | `481/100` | Session-140 auto plus windows 6 stopped at `19.132115`. |
| 19 | `97/20` | `19.808958`, worse than `481/100`. |
| 18 | `117/25` | Locked at `18.000000` on every named seed. |
| 18 | `469/100`, `47/10` | Plateau or above 18. |
| 12 | `398/100`, `3985/1000`, `399/100` | Grid rows at `16.000000` are dual-feasibility artifacts. |
| 20 | `971/200` | Session-140 leftover auto plus windows 6 stopped at `19.910044` unconverged below 20. Remaining rows raise. |
| 20 | `973/200` H-062 sets | Auto-grid `20.001502` and cert-seed `20.000223` already crossed. |
| 21 | `997/200` | Grid artifact at `25.000000`. |
| 11 | any side above T-026 | Covering-only. Not this campaign’s floor win. |

A longer wall on n=17 `23/5` windows 5, n=12 `397/100` `(26,35,43,48)` plus windows 7,
or n=19 `481/100` is a new named set only when the grids or windows differ.
Those sets can still lower the covering value.
They are not the first leftover spend: each already has a restricted optimum above `n`.

## Second wave

`second-wave-nagamochi-triage.md` keeps n=32, 31, 30, 26, 27, 29, 45, 44. An audit left
those eight sides in the floor-to-ceiling interval.
n=28 is in the 26–32 block and is omitted.
n=61 and n=78 stay deferred.

Leftover n=12 filled the `06:42Z` wall. Leftover n=18 `1871/400` and
`second-wave-queue.yaml` did not start (`remain=-4s`). A later session can take
n=18 `1871/400`, then n=32 `29/5`. Do not replay n=17 `23/5` or `461/100`, n=20
`971/200`, or n=12 `3969/1000` four-grid plus windows 7, for more wall.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
