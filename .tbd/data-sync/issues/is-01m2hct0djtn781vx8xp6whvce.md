---
type: is
id: is-01m2hct0djtn781vx8xp6whvce
title: "PR #125 review D26: campaign renumbering left dangling identities"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb401yy3ph99cfn5mhpcv4
created_at: 2026-09-15T02:02:19.442Z
updated_at: 2026-09-15T02:19:04.667Z
closed_at: 2026-09-15T02:19:04.664Z
close_reason: "Fixed in a7c18798: results/exp-135-round-1 moved to exp-202-round-1 (git mv), six record: paths repository-relative, exp-134 -> exp-201 in the catalogue and rendered survey table, SYNOPSIS H-201 105.7m, exp-205 over-budget list completed, packing-ledger check refuses duplicate idea numbers (ideas renumbering itself was 6f30d5b7). method.record resolving check deferred to think-7e1j."
resolution: null
duplicate_of: null
---
Review source: PR #125 review F25 (Medium); triage row D26. Checked against #155 R12 (D34): different identities, both touch ideas.md.

The campaign renumbering left dangling identities: (a) record: of exp-202, exp-203, exp-205 and exp-202's replay command (:210-212) point at results/exp-202-round-1/, which does not exist (data in results/exp-135-round-1/); nothing validates method.record. (b) the six new record: paths are packing-relative. (c) packing/frontier/search-strategies.yaml:298 and docs/project/research/research-2026-08-22-packing-11-unit-squares.md:1320 say exp-134 for exp-201. (d) packing/campaign/ideas.md:277-281 reused idea numbers 119-123 (renumbered to 175-179 at 6f30d5b7). (e) SYNOPSIS H-201 131.7m wall vs ledger 105.7m. (f) exp-205 :236-238 over-budget list omits n = 52 and n = 29.
