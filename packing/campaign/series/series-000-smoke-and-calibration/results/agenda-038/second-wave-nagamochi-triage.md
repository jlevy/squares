# Second-Wave Nagamochi-Only Floors

Status: **triage, no probe**. `think-b6n9`. First wave and leftover stay on
n=20/12/17/18/19. This list starts after `leftover-queue.yaml`.

These sizes have a verified Nagamochi floor and no `covering-values.yaml` row.
There is no first-party seed certificate.
The stock move is `run_fractional_colgen` with `--grid-counts auto` and
`--seed-windows 5` at a rational just above the floor.

| n | Floor | Ceiling | Gap | First side | Why this order |
| ---: | --- | --- | ---: | --- | --- |
| 32 | `1+sqrt(32-2*floor(sqrt(32))+1)` ≈ 5.796 | grid 6 | 0.204 | `29/5` | Smallest window in 26–32; auto grids stay cheap. |
| 31 | ≈ 5.690 | grid 6 | 0.310 | `57/10` | Next window to 6. |
| 30 | ≈ 5.583 | grid 6 | 0.417 | `559/100` | Same block; no published packing below 6. |
| 26 | ≈ 5.123 | `(7/2)+(3/2)sqrt(2)` ≈ 5.621 | 0.498 | `513/100` | Published packing sits well below 6; a floor above 5.12 is still a move. |
| 27 | ≈ 5.243 | `5+(1/2)sqrt(2)` ≈ 5.707 | 0.464 | `525/100` | Same pattern as n=26. |
| 29 | ≈ 5.472 | ≈ 5.934 | 0.462 | `548/100` | Published packing below 6. |
| 45 | ≈ 6.831 | grid 7 | 0.169 | `684/100` | Smallest window in 37–45. |
| 44 | ≈ 6.745 | grid 7 | 0.255 | `675/100` | Next in that block. |

n=28 is in the 26–32 block and is omitted: the tighter windows (32, 31, 30) and the
packings-below-6 trio (26, 27, 29) come first.
A side such as `271/50` would sit above the floor; it is not on this queue.

n=61 (gap 0.072 to 8) and n=78 (gap 0.063 to 9) are tighter integer windows and a worse
fit for this session: no seed, larger placement sets, and they are not low n. They stay
on the triage list, not on the four-hour queue.

A later audit kept all eight queued sides strictly above the Nagamochi floor and below
the verified or packing ceiling (margins 0.004–0.009). No side dropped.

The machine form is `second-wave-queue.yaml`, walked by
`python -m devtools.run_covering_queue`. Do not start it while a first-wave probe is on
the core. Do not treat a float LP as a floor.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
