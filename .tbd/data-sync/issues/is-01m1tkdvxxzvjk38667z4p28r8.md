---
type: is
id: is-01m1tkdvxxzvjk38667z4p28r8
title: "Claim documents: 'lighten one atom and the verifier refuses' is false; state exact perturbations (F5)"
kind: bug
status: closed
priority: 1
version: 3
labels:
  - review-gpt6
dependencies: []
parent_id: is-01m1tkdspk8c3n71xsc2e2t4g7
created_at: 2026-09-06T05:35:29.724Z
updated_at: 2026-09-06T06:21:09.279Z
closed_at: 2026-09-06T06:21:09.279Z
close_reason: "Implemented in 41fb401a on claude/pdf-paper-small-fixes (PR #92); reviewed by the coordinator; CI green"
resolution: null
duplicate_of: null
---
Finding 5, confirmed at packing/devtools/templates/verifiable_claim.md:155-156 (rendered into both t-018-verifiable-claim-*.md): 'Perturb the certificate, by lightening one atom, dropping an orbit member, or shortening the net, and the verifier refuses it.' Counterexample from the review: the central atom (381/200, 381/200), a one-point D4 orbit with weight 27899/200000, lightened by 1/200000 keeps every placement at mass >= 4001/4000 - 1/200000 = 200049/200000 > 1 and improves Condition 2, so all five conditions still hold. Fix: list exact perturbations with magnitudes and the condition each is meant to violate (e.g. lighten the central atom by 51/200000, which exceeds the 50/200000 margin), and include one benign perturbation expected to remain valid. Regenerate both claim documents and the proof card.
