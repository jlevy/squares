---
type: is
id: is-01m6jvv8f1b298n1p2wpnadbv2
title: Credit Özden as improved_by at 204 and 299 on the posters at the next infographics cut (T-263, T-264)
kind: task
status: open
priority: 3
version: 8
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-11-04T08:47:10.817Z
updated_at: 2026-11-05T23:38:33.940Z
---
T-263 (#893) and T-264 (#894) are Doğa Özden's further arrangements of Evan Daniel's packings at 299 and 204. #897 adopted both as their counts' houses (think-ybep). As the stage 4 review of record's F8 asks, the case records credit `found_by: [Evan Daniel]` and `improved_by: [Doğa Özden]` in `reported_upper_bound`, and so do `devtools/adopt_houses.py`'s CREDITS, the case pages' Improved by row, the bound citations ('Daniel & Özden, GitHub') and the register.

The posters' "Best packings due to" block reads every finder and improver in 1..324 from those fields. Adding Özden widens its three lines, and the attribution paragraphs rebalance one line shorter, so the 1-100 canvas computes 3869 px against the drawn 3898. That fails `build_known_best_atlas --check-composites` and Certificate page's `test_pdf_math_browser::test_the_complete_atlas_and_caption_fit_one_letter_page` (run 41798728350). Fixing it means redrawing both posters at an infographics cut (`devtools.cut_release --component infographics`), and the owner decides those (development.md, "Release assets are drawn at their component's version bump").

So #897 holds the name on the print only. `PRINT_CREDIT_HELD` in `devtools/build_known_best_atlas.py` maps 204 and 299 to ("Doğa Özden",), and `_poster_packing_credits` alone reads it. That function feeds the credit block, the attribution paragraphs' shared line measure, the block's data attributes, the metadata's `source_groups` and the canvas height. The metadata's `cases` list stays truthful. This is the same kind of hold as think-10l0's.

The hold cannot outlive its edition. `PRINT_CREDIT_HELD_FOR = "v0.7.0"`, and `test_the_print_credit_hold_cannot_outlive_its_edition` (through `print_credit_hold_problems`) fails the pull-request suite as soon as `INFOGRAPHIC_VERSION` or a drawn poster's version differs while the hold is not empty (review F2 of #897). The cut machinery's own validation does not read the hold.

Done when, at the next infographics cut, all of these move in the same change:
- `PRINT_CREDIT_HELD` is emptied (`{}`), and `PRINT_CREDIT_HELD_FOR` is updated or removed.
- In tests/test_known_best_atlas.py:
  - `test_print_credit_hold_keeps_ozden_and_yim_off_the_poster_credits_alone` (renamed on 5 November 2026 for think-hgpg) and `test_the_print_credit_hold_cannot_outlive_its_edition` are updated or removed with the hold.
  - The pinned poster names move: `expected_names` goes from 30 to 32 (Özden and, for think-hgpg, Yim), and each is printed in `printed_names` where the tree then puts him (Özden after Xu on 4 November).
  - `test_print_attribution_paragraphs_share_the_balanced_packing_measure`'s `[2, 3]` becomes `[2, 2]`.
- The credit block is laid out again. Since think-hgpg (5 November 2026) the hold holds Kaelan Yim at 260 too, and emptying it overflows the block's three lines (`ValueError: poster packing credits exceed their three-line information block`), so the cut must redesign or resize the block before it can draw. Released alone, Özden's name measured 3869 px and Yim's kept 3898 px.
- The canvas pins move with the redraw; the cut takes whatever the redraw then measures. They are:
  - the literal 1-100 canvas and export heights in tests/test_known_best_atlas.py (3898 and its @2x 7796 in the manifest rows, the canvas, row-pitch and PDF-page assertions, and the SVG header and viewBox);
  - the `const` heights in atlas/known-best/known-best-atlas.schema.yaml;
  - the page-size sentence in devtools/render_composite_pdf.py.
- The curation note's sentences naming this bead and think-hgpg in packing/atlas/known-best/credit-attributions.json are removed.
- think-hgpg is done in the same change: both beads end with the hold empty, and the edition tie empties the whole hold at once, so neither can close alone.
- Both posters are redrawn with the credit, and the hosted pdf job passes at the new height.

## Notes

Related: think-10l0, the same kind of hold for Khalili and Gharabaghi (and Greff), which waits on the same infographics cut. tbd has no non-blocking link type, so the relation is recorded here; neither bead blocks the other. Created by bold-ritchie-l36 on 2026-11-04 on the coordinator's poster decision for #897: the data stays true (improved_by Özden in both case records) and only the poster credit block holds the name (PRINT_CREDIT_HELD), a small tooling change made because of the owner's poster-trailing rule.

2026-11-05 (bold-ritchie-l48, on the coordinator's direction after the senior review of #911, F3): think-hgpg holds Kaelan Yim's name at 260 on the same hold, and the two beads are done together at the next infographics cut. The done-when above now names the renamed test, 30 to 32 names and the block's overflow; the hold's refusal message names both beads.

2026-11-05 (bold-ritchie-l51, #914's adoption, think-lrj4, draft PR #916): T-268 and T-269, Evan Daniel's own packings of #914, take 204 and 260 from T-264 and T-265, and the case records there credit Daniel alone (found_by [Evan Daniel], improved_by []), as do the bound citations ('Daniel 2026, GitHub'). So the hold is now {299: ('Doğa Özden',)}: Özden is credited at 299 alone (T-263), and Kaelan Yim at no count (think-hgpg). The same adoption takes Vladislav Lavrentev's and Kirill Tymchishin's names off the block, since only 268, 303 and 304 credited them, so the block prints 28 names, not 30, from 33 sources, not 34. Measured on the branch: with the hold as it stands, the 1-100 canvas computes 3898 px and the 101-324 canvas 5361 px, as drawn; with the hold emptied both stay, the block keeps its three lines and the attribution paragraphs their [2, 3], and Özden's name only changes the block's lines (29 names). So the done-when's overflow and its 3869 px no longer hold: emptying the hold at the cut needs no new layout for Özden, the pinned names go from 28 to 29 (Özden after Xu), and [2, 3] stays. The test is now test_print_credit_hold_keeps_ozden_off_the_poster_credits_alone and asserts the released canvas keeps 3898 px. No poster is redrawn; the posters keep v0.7.0.
