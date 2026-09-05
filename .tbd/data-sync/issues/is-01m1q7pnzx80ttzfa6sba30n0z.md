---
type: is
id: is-01m1q7pnzx80ttzfa6sba30n0z
title: Rename certificate conditions C0–C4 to Condition 1–5 in the explainer and first-party code
kind: task
status: closed
priority: 1
version: 2
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1q0p63s2evef5mhkyn16e41
created_at: 2026-09-04T22:12:52.338Z
updated_at: 2026-09-04T22:40:09.805Z
closed_at: 2026-09-04T22:40:09.802Z
close_reason: "Renamed and renumbered in commit 00474e8f: C0→Condition 1 … C4→Condition 5 across sqpack/fractional, the tests, README, SYNOPSIS, pages.yml, the renderer (--verify-condition-5), the coarsening tool and the page template. thirdparty/ and the review records deliberately keep C0–C4; every epistemics rung untouched. ruff, basedpyright and the 59 fast tests green."
resolution: null
duplicate_of: null
---
Review feedback on PR #79. The certificate conditions are labelled C0–C4, which collides with the C0–C5 confirmation levels in epistemics.md. Renumber 1-based: C0→Condition 1 (D4 symmetry), C1→Condition 2 (total mass below n), C2→Condition 3 (net reaches pi/4), C3→Condition 4 (containment B(1+D)<1), C4→Condition 5 (every reachable cell carries mass 1). Scope: devtools/templates/certificate_page.html, devtools/render_certificate_page.py, devtools/measure_net_coarsening.py, src/sqpack/fractional/*.py, tests/test_fractional_*.py, tests/test_decide_certificate.py, SYNOPSIS.md, README.md, conventions.md, .github/workflows/pages.yml. Out of scope, deliberately: cases/n11_fractional_certificate/thirdparty/ (frozen artifact an adversarial review read line by line), docs/project/reviews/ and campaign records (historical), and every C-level that is an epistemics confirmation level.
