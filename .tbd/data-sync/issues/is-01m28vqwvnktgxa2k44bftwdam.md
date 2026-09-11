---
type: is
id: is-01m28vqwvnktgxa2k44bftwdam
title: The math exposure rule judged visibility in a state the probe itself had changed
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-11T18:30:09.012Z
updated_at: 2026-09-11T18:30:15.242Z
closed_at: 2026-09-11T18:30:15.242Z
close_reason: Fixed in 15959d44; recorded as D-491
resolution: null
duplicate_of: null
---
`prepare_explainer_math`'s exposure rule — `math was exposed while its font requests were
held` — read visibility from the `before` snapshot and its exemptions from the
`_GEOMETRY_EARLY_READY` evidence. Those are two observations of two different states: the
probe injects its own carrier face and the `.katex` substitution between them, and those
styles change which boxes the page will show.

A box the substitution reveals is therefore visible in `before` and absent from the
evidence, which makes it unadmittable by construction, because `early_ready` can only name
a box the evidence saw. The rule asked about one state and took its exemptions from another.

Fixed: `geometry_findings` takes `exposed_early` and the exposure rule reads that instead of
`before`'s flags, so the question and its exemptions come from one observation. Recorded as
D-491.

Distinct from think-ghns, which is the separate gap that both explainer callers discard the
font-wait `{status}`. That one is still open, and closing it would not have prevented this.
