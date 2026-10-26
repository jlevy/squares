# The machines of the ValidTilt9 run

All times are UTC. The facts were read from the machines on 2026-10-16, after the run, and from the
operations notes kept during it.

## Common to both machines

| | |
|---|---|
| type | Google Cloud `c4a-highmem-48`, Spot (preemptible). 48 vCPU (Arm, aarch64), 376 GB memory |
| OS | Ubuntu 24.04.5 LTS, aarch64 |
| kernel | `7.0.0-1011-gcp` until 2026-10-11, then `7.0.0-1014-gcp`. Unattended upgrades installed it on 10-11 at 06:15 (A) and 06:58 (B), and it took effect at the next boot. |
| disk | hyperdisk-balanced, one ext4 root file system |
| swap | none |
| Lean | `leanprover/lean4:v4.33.1` (commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`), Lake 5.0.0-src+819816b, elan 4.2.4 |
| Mathlib and other packages | as in `lake-manifest.json` (identical to evand/square-packing `060c1a1`). The packages were built once and shared through `LEAN_PATH`. |
| Python | 3.12.3 (Ubuntu). `python3-sympy` 1.12 and `python3-mpmath` 1.2.1 were installed with apt on 2026-10-11 at 17:46 (A) and 17:47 (B). numpy 1.26.4 is present. Neither gmpy2 nor python-flint was installed. |
| other | zstd 1.5.5; Google Cloud SDK 588.0.0 (A) and 589.0.0 (B), updated automatically during the run |

`sympy` is imported only by one rare branch of the certificate generator (`gen_exact.factor_certs`). On
2026-10-12 that branch was reached for the first time, at root 8535, and failed on 42 roots because
sympy was missing. The package was installed and those roots re-ran from their markers.

## OS settings changed

| setting | default | changed to | when | where |
|---|---|---|---|---|
| `vm.max_map_count` | 1048576 | 4194304 | 2026-10-15 20:59 | machine A, `sysctl -w`, not persistent |

The change was made just before the second assembly attempt (`receipts/main_try1.log`, `receipts/main.log`).
No other kernel or OS setting was changed.

## Machine A (even roots, then the assembly)

- Zone `europe-west4-a` until the preemption at 2026-10-15 14:16. The disk was then copied from a
  snapshot to a new VM of the same type in `europe-west4-b`, which ran from 14:43 on.
  - The snapshot was taken after the preemption, of the stopped disk.
  - The driver resumed from its markers, with no marker lost.
  - The original VM and the snapshot were deleted afterwards.
- Disk: 400 GB at the start. It was enlarged to 550 GB on 2026-10-15 at about 17:45 (`growpart` and
  `resize2fs`, online) to hold machine B's oleans for the assembly.
- Boots (from `journalctl --list-boots`; this list continues across the snapshot):

| first entry | last entry |
|---|---|
| 10-10 09:40 | 10-10 11:00 |
| 10-10 11:02 | 10-10 23:00 |
| 10-10 23:01 | 10-11 08:54 |
| 10-11 08:56 | 10-13 15:02 |
| 10-13 15:06 | 10-13 15:06 |
| 10-13 15:10 | 10-13 15:18 |
| 10-13 15:22 | 10-15 14:14 |
| 10-15 14:43 | 10-15 15:05 (new zone) |
| 10-15 17:37 | 10-15 22:08 (assembly) |
| 10-16 02:51 | (reading these facts) |

## Machine B (odd roots, then 744 of machine A's highest even roots)

- Zone `europe-west4-a` throughout.
- Disk: 150 GB at the start. It was enlarged to 200 GB, and then on 2026-10-14 to 250 GB, both online.
- Boots:

| first entry | last entry |
|---|---|
| 10-10 09:40 | 10-10 23:00 |
| 10-10 23:01 | 10-11 07:29 |
| 10-11 07:34 | 10-12 03:04 |
| 10-12 03:06 | 10-12 14:38 |
| 10-12 14:44 | 10-14 13:07 |
| 10-14 13:13 | 10-14 14:23 |
| 10-14 14:25 | 10-14 15:03 |
| 10-14 15:08 | 10-15 00:14 |
| 10-15 00:15 | 10-15 22:07 |
| 10-16 02:51 | (reading these facts) |

The gaps between boots on both machines are of three kinds: Spot preemptions, stops for a machine-type
or disk change, and stops after the work was done. In every case the driver resumed from its per-task
markers. A task cut off by a stop ran again from the start, and such tasks appear twice in `tasks.jsonl`.

## Moving data between the machines

Data between the two machines went through a private Cloud Storage bucket in `europe-west4`.

- Machine A's 744 roots checked on machine B: oleans and markers were synced every 2 hours while B worked
  on them, and the md5 of each file was compared on both sides.
- Machine B's oleans for the assembly: sent in 17 chunks of 500 roots (`tar | zstd`), each with its file
  list. The copy relied on the storage tool's own transfer checksum. After unpacking, every listed file
  was checked to exist; the only missing entries were the leaf directories of roots without leaves.
- The rebuilt roots (two packages: three roots, then 8917): the md5 of each package was checked after the
  copy, and every listed file was checked to exist.
