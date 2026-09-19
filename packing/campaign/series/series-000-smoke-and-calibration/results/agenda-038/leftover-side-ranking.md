# Leftover First-Wave Sides

Status: **leftover wall ended**. `think-7igz` closed. Ranks 1–4 finished in
Session-140. Rank 5 (`1871/400`) was started by Session-141 and retained as T-029.

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
| 5 | think-avmz | 18 | `1871/400` | T-028 auto plus windows 5 | Session-141 started it and retained T-029 at `17.889237`. |

## Do not replay

| n | Side | Why leftover wall is wasted for retain |
| ---: | --- | --- |
| 17 | `461/100` | Session-140 leftover auto plus windows 5 stopped at `17.195968`. |
| 17 | `23/5` | Best stock row is `17.042346` (windows 5, 9 violated). Already above 17. |
| 12 | `3969/1000` | Session-140 leftover four-grid plus windows 7 stopped at `12.091168`. |
| 12 | `397/100` | Cert-seed `12.016263`; session-140 four-grid plus windows 7 converged at `12.133391`. |
| 12 | `397/100` auto plus windows 7 | Session-141 exp-176 stopped at `12.097146` unconverged above 12. Remaining rows raise. |
| 12 | `793/200` auto plus windows 7 | Session-141 exp-175 stopped at `12.067502` unconverged above 12. Remaining rows raise. |
| 12 | `793/200` four-grid plus windows 7 | Session-141 exp-178 stopped at `12.066995` unconverged above 12. Remaining rows raise. |
| 19 | `241/50` | Session-140 leftover auto plus windows 6 stopped at `19.247109`. |
| 19 | `241/50` four-grid plus windows 7 | Session-141 exp-177 stopped at `19.224565` unconverged above 19. Remaining rows raise. |
| 19 | `481/100` | Session-140 auto plus windows 6 stopped at `19.132115`. |
| 19 | `481/100` four-grid plus windows 7 | Session-141 exp-174 stopped at `19.111435` unconverged above 19. Remaining rows raise. |
| 19 | `97/20` | `19.808958`, worse than `481/100`. |
| 18 | `1871/400` | Session-141 leftover auto plus windows 5 retained T-029. |
| 18 | `4679/1000` | Session-141 T-029 auto plus windows 5 retained T-030. |
| 18 | `117/25` | Locked at `18.000000` on every named seed. |
| 18 | `469/100`, `47/10` | Plateau or above 18. |
| 12 | `398/100`, `3985/1000`, `399/100` | Grid rows at `16.000000` are dual-feasibility artifacts. |
| 20 | `971/200` | Session-140 leftover auto plus windows 6 stopped at `19.910044` unconverged below 20. Remaining rows raise. |
| 20 | `971/200` four-grid plus windows 7 | Session-141 exp-164 stopped at `19.857588` unconverged below 20. Remaining rows raise. |
| 20 | `243/50` four-grid plus windows 7 | Session-141 exp-165 stopped at `19.887914` unconverged below 20. Remaining rows raise. |
| 32 | `29/5` seedless auto plus windows 5 | Session-141 exp-166 stopped at `29.803318` unconverged below 32. Remaining rows raise. |
| 31 | `57/10` seedless auto plus windows 5 | Session-141 exp-167 stopped at `28.331329` unconverged below 31. Remaining rows raise. |
| 30 | `559/100` seedless auto plus windows 5 | Session-141 exp-168 stopped at `27.178193` unconverged below 30. Remaining rows raise. |
| 26 | `513/100` seedless auto plus windows 5 | Session-141 exp-169 stopped at `25.000000` unconverged below 26. Remaining rows raise. |
| 27 | `525/100` seedless auto plus windows 5 | Session-141 exp-170 stopped at `25.000000` unconverged below 27. Remaining rows raise. |
| 29 | `548/100` seedless auto plus windows 5 | Session-141 exp-171 converged at `26.040745`, freeze mass `26.0409395`; interval refused. Do not more-wall. |
| 45 | `684/100` seedless auto plus windows 5 | Session-141 exp-172 stopped at `42.137360` unconverged below 45. Remaining rows raise. |
| 44 | `675/100` seedless auto plus windows 5 | Session-141 exp-173 stopped at `41.236782` unconverged below 44. Remaining rows raise. |
| 20 | `973/200` H-062 sets | Auto-grid `20.001502` and cert-seed `20.000223` already crossed. |
| 21 | `997/200` | Grid artifact at `25.000000`. |
| 11 | any side above T-026 | Covering-only. Not this campaign’s floor win. |

A longer wall on n=17 `23/5` windows 5, n=12 `397/100` `(26,35,43,48)` plus windows 7,
or n=19 `481/100` is a new named set only when the grids or windows differ.
Those sets can still lower the covering value.
They are not the first leftover spend: each already has a restricted optimum above `n`.

## Second wave

`second-wave-nagamochi-triage.md` keeps n=32, 31, 30, 26, 27, 29, 45, 44. Session-141
measured all eight. None printed `RETAINABLE`.
n=28 is in the 26–32 block and is omitted.
n=61 and n=78 stay deferred.

Leftover n=12 filled the `06:42Z` wall. Leftover n=18 `1871/400` and
`second-wave-queue.yaml` did not start (`remain=-4s`). Session-141 later
retained leftover n=18 as T-029 and ran n=20 `971/200` and `243/50`
four-grid plus windows 7 to `19.857588` and `19.887914` unconverged, then
n=32 `29/5` to `29.803318`, n=31 `57/10` to `28.331329`, and n=30 `559/100`
to `27.178193`, and n=26 `513/100` to `25.000000` unconverged. Do not replay
n=17 `23/5` or `461/100`, n=20 `971/200` leftover auto or four-grid, n=20
`243/50` four-grid, n=32 `29/5` seedless auto plus windows 5, n=31 `57/10`
seedless auto plus windows 5, n=30 `559/100` seedless auto plus windows 5,
n=26 `513/100` seedless auto plus windows 5, n=27 `525/100` seedless auto
plus windows 5, n=29 `548/100` seedless auto plus windows 5, n=45 `684/100` seedless auto
plus windows 5, n=44 `675/100` seedless auto plus windows 5, n=19 `481/100`
four-grid plus windows 7, n=12 `793/200` auto plus windows 7, n=12
`397/100` auto plus windows 7, n=19 `241/50` four-grid plus windows 7,
n=12 `793/200` four-grid plus windows 7, n=18 `4679/1000` T-029 auto plus
windows 5 (T-030 retained), or n=12 `3969/1000` four-grid plus
windows 7, for more wall.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
