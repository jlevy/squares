---
type: is
id: is-01m26nttcsn4ej3g9adcat0qk5
title: "N11 BC337: compare the exact full-owner forbidden domain at the fixed residual"
kind: task
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - strategy
dependencies: []
parent_id: is-01m24sm7wm3s5eh8ke6vze7mw1
created_at: 2026-09-10T22:08:24.472Z
updated_at: 2026-09-10T22:16:38.179Z
---
Secondary to BC329, build and independently admit one exact centre-space comparison on fixed exp151 direction 6 and tuple (0,0,0,7). Keep open residual domain C°, the original B-only domains and sites, and the same nine other closed centre-space obstacles from the sites and BL, BR and TL patches. The control uses the existing TR collision obstacle P_TR + (-R). The candidate uses K_TR directly, with no second Minkowski expansion, where K_TR = closure(C°) ∩ intersection over all 181 frames f and eight signed SAT axes n of {c: n·c <= min_{z in Z_f} n·z + rho_f(n) + rho_r(n)}. Define U0 = C° minus the same nine obstacles and P_TR + (-R); define U1 = C° minus the same nine obstacles and K_TR. Preserve C° as open, so exact area(U1) = 0 with independent union confirmation implies U1 is empty. Reject the fixed candidate only with positive exact area plus a rational strict escape in U1 and a compatible TR witness. Admission stops at 45 minutes. An admitted target gets one 240-second scientific allowance inside a 300-second external bound plus two-second grace, with no retry. This fixed-domain pilot cannot cover another direction or domain, close the tuple, prove routing, or change the global n11 bound.
