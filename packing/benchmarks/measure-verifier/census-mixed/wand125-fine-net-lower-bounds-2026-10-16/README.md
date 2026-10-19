# Accepted Mac Checkpoints: n68, n84 and n85

Generated from exactly the three accepted rows by
`devtools.sqverify_fast_census.render_mixed_report`; do not edit by hand.
Other current-packet certificates and historical Linux n108 are outside this scoped
view.

Every retained certificate of formats M (rectangle rows, per-bin centre domain) and L
(points, segments and rectangles, Tokoharu’s domain), verified by `sqverify-fast` at
every direction of its net (201, unless the file declares its own) at the threshold the
certificate declares, 1. *Replayed directions* are those the authors’ checker replayed
in this repository; where there are none, this census is the first complete check here.
*Exact leaf* is the exact rational capture at the centre of the least-bound leaf of the
least-bound direction.
*Authors’ CPU* is the authors’ checker’s recorded CPU seconds on the directions this
repository replayed; *ours, same directions* is `sqverify-fast`’s thread CPU on exactly
those directions. Per-direction CPU is unavailable unless every compared direction has a
reading; the native summary’s zero does not supply missing readings.
*CPU s, all directions* is aggregate process CPU from `wait4` (user plus system),
separate from the direction readings.
Load is given only where recorded.
*Control* is the status of the `--control` receipt on the certificate itself, where one
is kept: the original verified again and a near-threshold mutant refused at its
least-bound direction, and the 99/100 mutant refused at one direction at least, every
direction of the net run (v2), or at that direction alone (v1).

| Certificate | n | Format | Status | Directions | Nodes | Least certified bound | Exact leaf | CPU s, all directions | Load | Replayed directions | Authors’ CPU s | Ours, same directions | Ratio | Control |
| --- | ---: | --- | --- | ---: | ---: | --- | --- | ---: | ---: | --- | ---: | ---: | ---: | --- |
| `mixed_n68_L853` | 68 | M | VERIFIED | 201 | 104,110,078 | 1.0000000000889968 | clears | 855.9 | 3.3 | none: first complete check here | - | unavailable | - | CONTROLS_REFUSED |
| `mixed_n84_L94225` | 84 | M | VERIFIED | 201 | 136,054,170 | 1.000000000314376 | clears | 1395.7 | 6.0 | none: first complete check here | - | unavailable | - | CONTROLS_REFUSED |
| `mixed_n85_L9475` | 85 | M | VERIFIED | 201 | 126,895,910 | 1.000000000004128 | clears | 1414.0 | 7.9 | none: first complete check here | - | unavailable | - | CONTROLS_REFUSED |

3 of 3 certificates verified; 3666 recorded aggregate process CPU seconds in all.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
