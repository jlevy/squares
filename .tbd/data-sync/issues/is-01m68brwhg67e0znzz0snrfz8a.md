---
type: is
id: is-01m68brwhg67e0znzz0snrfz8a
title: Credit Khalili and Gharabaghi on the posters at the next infographics cut (T-252, s(44) = 7)
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m685tapg46244xgj0cmsd3x2
created_at: 2026-10-31T06:53:51.536Z
updated_at: 2026-10-31T06:53:51.536Z
---
T-252 (#842, think-1v4b) proves s(44) = 7, so Mohsen Khalili and Sara Gharabaghi are now current lower-bound source authors and optimality theorem authors in the corpus 1..324. PR #851 records n = 44 in packing/atlas/known-best/credit-attributions.json at the case level (its lower-bound case group, the new source with its bibliography record, the optimality case, the proof source khalili-gharabaghi-2026-n44 and the canonical citation), but not as print-credit contributors: an entry in lower_bounds.contributors (role current-bound-source-author) and optimality.contributors (role theorem-author) adds both names to the posters' "Lower bounds due to" and "Optimality proofs due to" paragraphs, which changes the poster layout (tests/test_known_best_atlas.py::test_the_1_100_canvas_is_what_its_specification_computes) and so needs both posters redrawn, an infographics cut (devtools.cut_release --component infographics), which the importing host could not render (no pinned Chromium for the PNG/PDF exports).

Done when: at the next infographics cut, both contributor entries are added (the shapes are in the PR's history: the script at the lane's scratch, and Hosono's and Kearney's entries as models), tests/test_known_best_atlas.py's pinned contributor and name lists are moved (lower-bound contributors 20 -> 22, the printed lists gain Gharabaghi and Khalili after Ryu and Karakuş, optimality names 18 -> 20), the curation note's sentence naming this bead is removed, and the posters are redrawn with the credits.
