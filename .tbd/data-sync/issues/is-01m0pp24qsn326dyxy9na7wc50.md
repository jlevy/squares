---
type: is
id: is-01m0pp24qsn326dyxy9na7wc50
title: "High-level docs: cross-reference README and SYNOPSIS, and apply the doc guidelines"
kind: epic
status: closed
priority: 1
version: 8
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0n6nyzx5pnark7xve1dy52x
child_order_hints:
  - is-01m0pp2zjv4acvv3j65dmj9nz9
  - is-01m0pp2zx0x0bg6bmnpgcwdnpv
  - is-01m0pp3087a77n5ysn1a4j2e24
  - is-01m0pp30kr39p8gz6mn65tx4ck
  - is-01m0pp30z8rste76ygse0dz6ph
  - is-01m0pp31bhda9hxjhrz007qamk
created_at: 2026-08-23T06:48:51.705Z
updated_at: 2026-08-23T07:01:52.154Z
closed_at: 2026-08-23T07:01:52.153Z
close_reason: "All six children done. README and SYNOPSIS cross-referenced and reconciled; common-doc-guidelines applied to README, SYNOPSIS and conventions.md (em dashes, Title Case H2, 'and' not '+', no 'canonical' for a document, no filler jargon, no history notation or meta-commentary in the living docs, no proscribed extravagant language -- checked and none present). The structural outcome: README's drifting counts are gone, and tools/check_readme.py now reconciles what remains, so the gate is 18 steps and both high-level documents are checked instead of one. Follow-on work that is deliberately NOT in scope here is tracked in think-8vhj (audit every glossary term against real usage) and think-vcti (whether the cell/instance-cell rule binds outside SYNOPSIS.md)."
resolution: null
duplicate_of: null
---
README.md and SYNOPSIS.md are the two entry points and they had drifted from each other and from the artifacts. This epic cross-references them and applies tbd's common-doc-guidelines rigorously.

The finding that motivates the shape of the work: README's defect paragraph went stale twice in one session (28 vs 29 defects, 8 vs 7 unprotected fixes), because check_synopsis.py reconciles SYNOPSIS against defects.yaml and nothing reconciles README. The guidelines' "avoid duplication" rule and this repo's drift history point the same way -- the higher-level doc should not restate what the lower-level generated view owns.
