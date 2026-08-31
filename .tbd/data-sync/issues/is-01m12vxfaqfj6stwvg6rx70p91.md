---
type: is
id: is-01m12vxfaqfj6stwvg6rx70p91
title: n=68 and n=69 witnesses are too coarse for contact claims
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T00:22:03.350Z
updated_at: 2026-08-28T01:26:22.936Z
---
Both are UnitSquare Project SVG imports at tolerance 2e-6 (witnesses/known-best/n-068.yaml:705,718) whose corners are not exact unit squares -- edge lengths differ at ~1e-8 -- so no contact registers. Any contact-based analysis reports every square movable at 1e-12 and 23 of 68 at 1e-6, which is a witness-fidelity artifact rather than a finding. These two must be excluded from contact work until the geometry is normalized.
