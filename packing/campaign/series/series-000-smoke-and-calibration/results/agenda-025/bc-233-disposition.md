# BC-233 Inset-Seed Screen and Released-Support Disposition

Status: **rejected under exp-071 and H-070**. The three screens and matched follow-on
are complete. The released seed did not beat its unseeded control under the frozen exact
accept rule.

Launch base: `c55726e1e885227f63110131c0a914665175ff89`\
Frozen preregistration: `f1b6c641e8d3a2fea39cf5aa5292cb8fc1221772`\
Cell: BC-233 (`think-jbat`)\
Experiment: exp-071, H-070

## Controls

The strict-JSON deadline controls `test_deadline_before_first_round_writes_strict_json`
and `test_summary_json_refuses_unexpected_non_finite_values` passed in 1.36 seconds.
Massaccesi’s archived n=17 program reported 168 atoms, total `203/12`, least score `1`,
and `CERTIFICATE CONDITIONS VERIFIED`. The source-distinct third-party check rebuilt
bytes identical to `control-n17-massaccesi.json` and accepted both its n=11 and n=17
controls.

The unpinned scalar verifier also accepted the retained n=11 certificate with SHA-256
`b121edbd044b6f326022d8783551efd947c95eec2738269857d039358ac6ae6a`, exact total
`434547/40000`, and least covered mass `4001/4000` over 567,131,843 reachable cells.
The project decision gate independently returned `RETAINABLE` on the same bytes: its
interval route enclosed exactly `4001/4000` after 1,570,831 boxes in 22 seconds, and its
exact sweep returned the same minimum in 8 seconds.

No control changed a source file.
The first sandboxed attempt to start BC-232 failed before its process or outputs existed
because the sandbox could not open the shared uv cache.
The manager preserved that operational guard refusal and launched the exact command with
approved cache access; no scientific process was restarted.

## Screen Contract

Each screen used side `191/50`, square side `9977/10000`, grid counts `25,34,41`, angle
limit `207107/500000`, 180 direction steps, rationalization scale 4,000,000, one column
round, at most 60 row rounds, three rows per direction, and a 540-second deadline.
All numerical-thread environment variables were pinned to one.

A screen was eligible only after zero exit, strict JSON, final row convergence, and an
emitted candidate.
Exact rational candidate mass, rather than the float objective, ranked
eligible screens.

## Screen Results

| Inset | Status | Exact candidate mass | Command wall | Candidate SHA-256 |
| --- | --- | ---: | ---: | --- |
| `1/2` | eligible; converged | `11142897/1000000` = 11.142897 | 85.175 s | `628d7e55d664c5256a9331b9a68166306a30c275432a997bfe9fab1a9ca0fc5a` |
| `2962983/4505800` | eligible; converged | `9268609/800000` = 11.58576125 | 162.342 s | `2d2a955b0549d788fa822085e8ea217abaf78a006d846be01a350b4e9b7cedc9` |
| `15513/20000` | eligible; converged | `44995603/4000000` = 11.24890075 | 69.604 s | `df5edeaf920951aa2c7d1284bd9f4e101e5f2e29caf39d5862c8dff4d8ba16a2` |

The `1/2` candidate is the unique exact minimum and is frozen as the selected seed.
Every candidate remains above eleven; none routes to exact lower-bound decision.
The runner summaries record command wall time but not process CPU time.
CPU was not captured before the first two short-lived screens exited and is recorded as
unavailable, not estimated.
The third screen had 59.03 CPU seconds at a 59-second live snapshot; that is a lower
bound rather than a final CPU measurement.

Complete output hashes:

```text
628d7e55d664c5256a9331b9a68166306a30c275432a997bfe9fab1a9ca0fc5a  bc-233-screen-1-2.candidate.json
3317beb3f4103695e268e40be7d7774e94c0e2b625e8750eddf3d6926f049de0  bc-233-screen-1-2.json
699a7fb312f6b8f51eee8349cf3b0ff0bca65c4f667378a36888ec98669e9668  bc-233-screen-1-2.log
8eae401d3f8dc00a83bd4c5be5385f3fb0d8369d2bd3ab8a67043533ff92f3a8  bc-233-screen-1-2.rows
2d2a955b0549d788fa822085e8ea217abaf78a006d846be01a350b4e9b7cedc9  bc-233-screen-2962983-4505800.candidate.json
14189bb3076c4d1526a1f228a0e14bda2b2e627753762d71ac48e095006b98c1  bc-233-screen-2962983-4505800.json
c7d8adb39b18840eca579548ccb413eb30af82897da6dff3b8105afc0bd0367b  bc-233-screen-2962983-4505800.log
a3f5f768cbbdef1c39edbdf3cedf41818fcef016167ac0b1886fca5de80a00ae  bc-233-screen-2962983-4505800.rows
df5edeaf920951aa2c7d1284bd9f4e101e5f2e29caf39d5862c8dff4d8ba16a2  bc-233-screen-15513-20000.candidate.json
5ede09727467885b0bd56246020f979652b024f4947dfea16d3717450a30ecd3  bc-233-screen-15513-20000.json
09b0e34219f4272ab4386d0262ee58dfe050536d18c886d1e1d7a1f2a8b579e7  bc-233-screen-15513-20000.log
48e7cb0024e5566781ba5cea0c769b940269a1004e74f8ec978e5a1c7f2b0fd6  bc-233-screen-15513-20000.rows
```

## Matched Follow-On

After the screens selected a seed, an upstream move froze every new launch.
The coordinator reconciled the launch-bound colgen engine SHA-256
`8c35796d7d3b3dbfa8eafd29d63078131ebb9d0b921a71c178ff77530eda01`, agenda-025 SHA-256
`510d3838a40973ec6535e4c7d99198804b8ed88a9c52126c455c97b182651c0f`, and retained state
SHA-256 `8df0b9aa530149b44367842a2e6389949b27189df038d68e9d1afa8fd87df8c6` as unchanged.
No arm ran during the hold.

The active-minute-30 gate passed before launch.
The coordinator’s explicit GO at `2026-09-06T04:03:58Z` opened the two fresh output
stems. The selected `1/2` candidate seeded the released arm through `--seed-map centre`;
the control omitted only the seed certificate.
Both used inset `1/2`, eight column rounds, 2,520-second deadlines, and the same
remaining parameters as the screens.

The released arm started at `2026-09-06T04:04:38Z` in execution session 87066 as uv PID
17163 and Python 3.14.7 PID 17164. The control started one second later in session 83855
as uv PID 17171 and Python 3.14.7 PID 17172. Neither command was restarted.

Both processes exited zero.
`jq -e` parsed both summaries, both carried `converged: true`, both completed exactly
eight rounds, and both stopped as `converged: every placement covers mass 1`. Each
emitted its named candidate.
The released summary recorded 196 seed sites; the control recorded zero.

| Arm | Exact candidate mass | Completed rounds | Stop class | Command wall |
| --- | ---: | ---: | --- | ---: |
| released | `11142893/1000000` = 11.142893 | 8 | converged | 173.003 s |
| control | `11142893/1000000` = 11.142893 | 8 | converged | 171.285 s |

The two candidate files are byte-identical.
Across all eight round records, the two summaries also agree on row, orbit, and site
counts; LP-round counts; objective, least-covered, averaged-depth, and reduced-cost
values; added-orbit counts; and the exact selected-orbit notes.
Only per-round timing, seed metadata, and output paths differ.
The final CPU total is unavailable because the exact runner does not record it and both
PIDs exited before the next process-table snapshot.
The last live snapshot gives lower bounds of 141.47 CPU seconds for released and 140.27
CPU seconds for control; those are not reported as final costs.

Both arms improved the selected one-round screen mass by exactly `1/250000`, but they
did so equally. This is evidence for the common released-support search, not for an
advantage from the seed.

Complete follow-on output hashes:

```text
607a3898c2e79174d937d259d90f5479bdd86271a66a536cc096906dbd2c5040  bc-233-released.log
6b270ddedaa0efdf0637de7366c1b2b736df289c9ef570a6e12ad4486eb0f939  bc-233-released.rows
eaf538c82706142d3b0d3cc9bd3ad7a40733bfab3f57c9707ebd7f26f3d7c972  bc-233-released.json
d47d188cd303b369423d92b01e259ae5c582b49fac3c7664cc178121f11016f2  bc-233-released.candidate.json
4a28cc3645e4d080b2edf03700ab96c4fa5df3aa3e69f10b7d7e754f8219b829  bc-233-control.log
7dd38f91cffd51744e1591e5a06e5b709b0a59c346bcab0b848a2af328d5ff8c  bc-233-control.rows
ba0af81ea4d3a91517df5ca60cded71ba3fdc20b1aa716f152b5ec42fe745a7c  bc-233-control.json
d47d188cd303b369423d92b01e259ae5c582b49fac3c7664cc178121f11016f2  bc-233-control.candidate.json
```

## Scientific Disposition

The released candidate’s exact mass is equal to the control’s, rather than strictly
smaller. H-070 and exp-071 are therefore **rejected**, not unresolved.
Both masses remain above eleven, so neither candidate enters the exact lower-bound
decision route. The equal trajectory and byte-identical candidate are retained negative
evidence. BC-233 earns no continuation block, and no replacement or successor process is
launched.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
