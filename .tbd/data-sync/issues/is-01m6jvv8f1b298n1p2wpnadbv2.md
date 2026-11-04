---
type: is
id: is-01m6jvv8f1b298n1p2wpnadbv2
title: Credit Özden as improved_by at 204 and 299 on the posters at the next infographics cut (T-263, T-264)
kind: task
status: open
priority: 3
version: 4
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-11-04T08:47:10.817Z
updated_at: 2026-11-04T08:51:50.660Z
---
T-263 (#893) and T-264 (#894) are Doğa Özden's further arrangements of Evan Daniel's packings at 299 and 204. #897 adopted both as their counts' houses (think-ybep). As the stage 4 review of record's F8 asks, the case records credit `found_by: [Evan Daniel]` and `improved_by: [Doğa Özden]` in `reported_upper_bound`, and so do `devtools/adopt_houses.py`'s CREDITS, the case pages' Improved by row, the bound citations ('Daniel & Özden, GitHub') and the register.

The posters' "Best packings due to" block reads every finder and improver in 1..324 from those fields. Adding Özden widens its three lines, and the attribution paragraphs rebalance one line shorter, so the 1-100 canvas computes 3869 px against the drawn 3898. That fails `build_known_best_atlas --check-composites` and Certificate page's `test_pdf_math_browser::test_the_complete_atlas_and_caption_fit_one_letter_page` (run 41798728350). Fixing it means redrawing both posters at an infographics cut (`devtools.cut_release --component infographics`), and the owner decides those (development.md, "Release assets are drawn at their component's version bump").

So #897 holds the name on the print only: `PRINT_CREDIT_HELD` in `devtools/build_known_best_atlas.py` maps 204 and 299 to ("Doğa Özden",). It is read only by `_poster_packing_credits`, which feeds the poster's credit block, its metadata and the canvas it sizes. This is the same kind of hold as think-10l0's.

Done when, at the next infographics cut:
- `PRINT_CREDIT_HELD` is emptied (`{}`), and `test_print_credit_hold_*` in tests/test_known_best_atlas.py is updated or removed with it.
- tests/test_known_best_atlas.py's pinned poster name list moves: `expected_names` goes from 30 to 31, and Özden is printed after Xu in `printed_names`, where the 4 November tree puts him.
- The curation note's sentence naming this bead in packing/atlas/known-best/credit-attributions.json is removed.
- Both posters are redrawn with the credit, the 1-100 canvas at its new height.

## Notes

Related: think-10l0, the same kind of hold for Khalili and Gharabaghi (and Greff), which waits on the same infographics cut. tbd has no non-blocking link type, so the relation is recorded here; neither bead blocks the other. Created by bold-ritchie-l36 on 2026-11-04 on the coordinator's poster decision for #897: the data stays true (improved_by Özden in both case records) and only the poster credit block holds the name (PRINT_CREDIT_HELD), a small tooling change made because of the owner's poster-trailing rule.
