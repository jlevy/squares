# Joost de Winter’s August 2026 construction report

This record preserves what could be established on 2026-09-05 about the mutable
author-uploaded report at
[ResearchGate](https://www.researchgate.net/publication/411979559_An_improved_packing_of_206_unit_squares_in_a_square).
It is a source-availability and routing record, not a verified packing.

## Conflicting live revisions

The same public record exposed two different documents during the refresh:

| Observation | Document exposed | Claims visible |
| --- | --- | --- |
| Fresh search-index rendering, checked 2026-09-05 | *Improved packings of 68, 126 and 206 unit squares in a square*, dated 2026-08-14 | `n = 68`: 8.802212238746405 and 8.802187556882656; `n = 126`: 11.774735132406546; `n = 206`: 14.872219025630592; source says it checked rounded coordinates at 50-digit precision |
| Direct rendering of the same URL, checked 2026-09-05 | *An improved packing of 206 unit squares in a square*, dated 2026-08-08 | `n = 206`: 14.872219025630592; source says it checked rounded coordinates at 40-digit precision |

The advertised PDF URL returned HTTP 404. Direct non-browser retrieval returned HTTP
403, and the browser route presented a CAPTCHA; it was not bypassed. No PDF, coordinate
table, vector figure, or machine-readable witness was therefore available to retain.
The exact observations and source-reported values are stored in `results.json` so a
future agent need not repeat this failed acquisition merely to recover the metadata.

## Evidential status

All four sides are **author-reported construction candidates**. The report says that
the displayed 15-decimal coordinates were checked with high-precision separating-axis
tests, but those coordinates were not available in the retrieved corpus. The repository
has not replayed containment, side lengths, or non-overlap. Do not enter these numbers as
verified frontier values until a stable coordinate artifact is obtained and the normal
geometry verifier accepts it.

The report’s `n = 68` comparison is already stale. It compares against Kingbird’s
`8.803459936516539`, while the retained UnitSquare Release 1 witness establishes
`8.8033830747161083869…`. The proposed `8.802187556882656` would still improve that
verified witness by `0.0011955178334523869…` if its geometry is recovered and replayed.
No equivalent local replay was possible for `n = 126` or `n = 206`.

## Reopen condition

Reopen acquisition when the author record exposes a stable PDF or coordinate payload,
or when a first-party catalogue publishes the actual geometry. Retain the bytes, record
their hash and revision date, import the poses as an approximate witness, and require an
independent multiprecision separating-axis replay before changing the frontier.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
