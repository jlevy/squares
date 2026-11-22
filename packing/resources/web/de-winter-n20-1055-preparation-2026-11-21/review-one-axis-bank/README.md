# Independent polynomial-bank review for the one-axis case

The independent checker accepts all 576 conditional polynomial certificates and
9,777 uses of their first-match rules for one aligned square and nineteen
independently signed tilts of equal absolute magnitude. It covers the parameter
range $0 \le t \le 1/24$, with strict positivity required where stated for $t>0$.
Sixteen predeclared controls behaved as expected. The checker took 0.379 seconds
and used 36.7 MiB peak RSS. The guard observed normal pressure at startup.

The reviewer read the source proof and the certificate representation, then wrote
separate exact arithmetic and reconstruction code. The conditional certificates
do not enumerate the sign assignments, ownership graphs or bridge exclusions.
Those finite coverage checks remain open for the one-axis theorem. The angular
diversity claim also needs the separate large-angle proof.

Use the [frozen plan](frozen-plan.md), [checker](checker.py.txt),
[certificate bank](one_axis_24.json.gz), and [receipt](checker-receipt.json.gz)
to reproduce this check. The original attachment and credit are recorded
in the [source packet](../README.md).

## Compressed files

| File | Origin | Git blob of original bytes | SHA-256 of original bytes |
| --- | --- | --- | --- |
| `one_axis_24.json.gz` | upstream | `8da04d8ac0d26dd442d7342c8e736dfad5d7f35a` | `774cf1ffc704886c9ff3802600dc7d112ef87b25024d7147176bc2af4f14ee9f` |
| `checker-receipt.json.gz` | receipt | `b72348118152f100e3adb3cb4fffd114af4eae83` | `5f8ca1a560ef390078f9938bc98ac63af1efec0cf0be43481dd60628a7598f4c` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
