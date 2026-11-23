# Independent polynomial-bank review for the one-axis case

The independent checker accepts all 576 conditional polynomial certificates and
9,777 uses of their first-match rules for one aligned square and nineteen
independently signed tilts of equal absolute magnitude. It covers the parameter
range $0 \le t \le 1/24$, with strict positivity required where stated for $t>0$.
Sixteen predeclared controls behaved as expected. The checker took 0.379 seconds
and used 36.7 MiB peak RSS. The guard observed normal pressure at startup.

The reviewer read the source proof and the certificate representation, then wrote
separate exact arithmetic and reconstruction code. The conditional certificates
do not enumerate sign assignments, separation graphs or bridge exclusions.
The separate [bridge review](../review-one-axis-bridges/README.md) now accepts all
3,488 positive-cost local profiles. The separate
[sign and symmetry census](../review-one-axis-sign-census/README.md) now retains
29,368 assignments in 3,671 D4 orbits. The
[general-path review](../review-one-axis-general-paths/README.md) now classifies
all 29,008 local profiles. Application to global paths, separation graphs, rule
extraction and graph-to-certificate coverage remain open for the one-axis theorem. The angular diversity claim also needs the separate large-angle proof.

Use the [frozen plan](frozen-plan.md), [checker](checker.py.txt),
[certificate bank](one_axis_24.json.gz), and [receipt](checker-receipt.json.gz)
to reproduce this check. The original attachment and credit are recorded
in the [source packet](../README.md).

## Compressed Files

| Stored path | Origin | Git blob of original bytes | SHA-256 of original bytes |
| --- | --- | --- | --- |
| `checker-receipt.json.gz` | receipt | `b72348118152f100e3adb3cb4fffd114af4eae83` | `5f8ca1a560ef390078f9938bc98ac63af1efec0cf0be43481dd60628a7598f4c` |

## Original Gzip Files

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `one_axis_24.json.gz` | upstream | `69cdbf53f097cc89cb136adca3bb4bb81a71ccfc` | `451b1116cf5b6eaa78ecc8233ee4e4c931537e6dfd3bd4fba2a6d91b1922d257` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
