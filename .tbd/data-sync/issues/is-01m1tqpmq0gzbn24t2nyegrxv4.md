---
type: is
id: is-01m1tqpmq0gzbn24t2nyegrxv4
title: "A9: the sweep-exactness argument skips the finiteness clause"
kind: chore
status: closed
priority: 3
version: 3
labels:
  - review-claude
dependencies: []
parent_id: is-01m1tqpgrh5ym0r6e5apbke7p8
created_at: 2026-09-06T06:50:11.551Z
updated_at: 2026-10-06T08:24:49.680Z
closed_at: 2026-10-06T08:24:49.680Z
close_reason: "Done: PR 94 (merged 2026-09-06, 3e1fd715d) implements A9. The claim template and verify_claim.py's comment carry the finiteness clause."
resolution: null
duplicate_of: null
---
verifiable_claim.md 'Why the Sweep Is Exact' and the comment block in verify_claim.py: 'every admissible center lies in the closure of some open cell that meets the admissible square, since that square has interior and finitely many lines cannot cover an open set' gives a cell within every epsilon, not one whose closure contains the point; add that there are finitely many cells, so one of them meets the domain within every distance of the point. Regenerate the claim documents.
