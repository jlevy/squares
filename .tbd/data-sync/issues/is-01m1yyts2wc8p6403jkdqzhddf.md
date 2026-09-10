---
type: is
id: is-01m1yyts2wc8p6403jkdqzhddf
title: "One sans bold: caption labels, title credits and every other sans bold at the same weight"
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - explainer
  - typography
dependencies:
  - type: blocks
    target: is-01m1yzw4rzjjmtdpsc0fj438vq
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
created_at: 2026-09-07T22:11:44.855Z
updated_at: 2026-09-08T06:55:46.693Z
closed_at: 2026-09-08T06:55:46.679Z
close_reason: "Shipped: squares#119 merged to main on 2026-09-08 after a senior review (approve) and its fixes"
resolution: null
duplicate_of: null
---
Owner (2026-09-07): the caption labels (Figure 5. and the rest) should be bold, and that bold must be the same weight as the bold in the title credits and everywhere else in the sans: one bold across the design system. Today the print probe in devtools/sans_instances.py finds the caption label (figcaption strong) at 550, the medium token, while strong in the hero credits is 680, the bold token (--cert-font-weight-sans-bold), and the footnote controls sit at 600 (a kpress default). Audit every sans weight the page requests, on screen and in print, with a listing mode of the probe (weight, style, element path, and which token or literal set it), decide the single bold (680 in the paper profile; kpress's own token is 650) and the single medium, route the caption label through the bold token, and remove or justify every literal weight. Check kpress's own defaults for the same rule (kpr side if its caption or label rules name medium where bold is meant). Re-render, regenerate the print instances if the requested set changes, and record the final weight table in the plan spec's Font Consistency section.
