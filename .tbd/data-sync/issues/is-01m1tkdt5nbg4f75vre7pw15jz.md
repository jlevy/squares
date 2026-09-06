---
type: is
id: is-01m1tkdt5nbg4f75vre7pw15jz
title: "Explainer: drop the false warning that <= in Condition 4 lets shrunken squares share an atom (F1)"
kind: bug
status: closed
priority: 1
version: 3
labels:
  - review-gpt6
dependencies: []
parent_id: is-01m1tkdspk8c3n71xsc2e2t4g7
created_at: 2026-09-06T05:35:27.924Z
updated_at: 2026-09-06T06:21:09.246Z
closed_at: 2026-09-06T06:21:09.245Z
close_reason: "Implemented in 41fb401a on claude/pdf-paper-small-fixes (PR #92); reviewed by the coordinator; CI green"
resolution: null
duplicate_of: null
---
Finding 1, confirmed. packing/devtools/templates/explainer-article.md, 'The Contradiction' (line ~452): 'With <= in Condition 4, two shrunken squares could share an atom on a common boundary...' is false for any net with positive gaps. Derivation: D > 0; if d = 0 then B <= 1/(1+D) < 1; if d > 0 then B(cos d + sin d) = B cos d (1 + tan d) < B(1 + tan d) <= B(1+D) <= 1. Containment is strict either way. Keep the strict test in the verifier (harmless, conservative) but describe it as a sufficient condition, and reword 'Because Condition 4 is a strict inequality, each Q_i sits inside its unit square's interior' so strictness of containment does not rest on strictness of the test. Acceptance: the paragraph is gone or corrected, the explainer re-rendered, tests/test_explainer.py green.
