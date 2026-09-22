---
type: is
id: is-01m351ehfbza13y8x3dydtfr2c
title: "Build devtools.certification_queue: the read-only queue of uncertified upper bounds"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-22-upper-bound-certification-blocks.md
labels: []
dependencies: []
parent_id: is-01m350mb40w609b2j8aksv4gq6
created_at: 2026-09-22T17:08:37.994Z
updated_at: 2026-09-22T17:08:37.994Z
---
Block 3 of think-2716, W7. Build the read-only command specified in the spec's section The queue command: uv run --frozen --all-extras --group dev python -m devtools.certification_queue [--next] [--group A|B|R|C] [--json]. Reads packing/frontier/n-*.md, packing/frontier/evidence.yaml, packing/witnesses/known-best/n-*.yaml and the count rules of cases/gobel_strip, gobel_family, gobel_offcentre. Certified set computed with the one shared rule in sqpack.assurance (today bounds_agree_at_declared_precision; the owner's decision on the spec's first open question may replace it, and the tool must call whatever function the stage generator calls, never its own copy). Groups derived from fields, never a hand list: UnitSquare source_key -> C; exact_form matched by a family count (including n - 1 by deletion where reported sides are equal) -> A; other exact_form -> B; else R. One row per queued n: group, sub-family, blocker kinds, exact_form or degree, witness form and significant digits, witness-side-minus-reported gap in units of the last printed place, instrument or none, data retained. Writes no file. Controls over the recorded register: group A sizes equal the modules' count matches (18 on 2026-09-22: 104, 125, 149, 174, 201, 231, 262, 295, 296, 109, 124, 147, 148, 227, 232, 233, 264, 265); total equals the tripwire's TRAILING_BY_CORPUS count under the same rule (129 today, 128 if n = 29 is excused). Sub-second; register it in the records tier. print is allowed (devtools).
