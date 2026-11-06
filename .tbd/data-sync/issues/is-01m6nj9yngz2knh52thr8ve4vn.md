---
type: is
id: is-01m6nj9yngz2knh52thr8ve4vn
title: Credit Yim as improved_by at 260 on the posters at the next infographics cut (T-265)
kind: task
status: open
priority: 3
version: 4
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-11-05T09:58:09.839Z
updated_at: 2026-11-06T02:44:27.526Z
---
The adoption of T-265 at 260 on 5 November 2026 (PR #911, think-o7ly) credits Kaelan Yim as improved_by of Evan Daniel's packing there. The case record, its page, the register and the bound citation ("Daniel & Yim, GitHub") credit him now. The atlas posters, drawn for the v0.7.0 edition, do not: `PRINT_CREDIT_HELD` in `packing/devtools/build_known_best_atlas.py` holds his name off the posters' "Best packings due to" block, beside Doğa Özden's at 204 and 299 (think-tj4o), until the next infographics cut redraws the posters and empties the hold.

Measured on 5 November 2026: released alone, Yim's name fits the block and leaves the 1-100 canvas at 3898 px, though it changes the block's lines; released together with Özden's, the block overflows its three lines (`ValueError: poster packing credits exceed their three-line information block`). So the cut that empties the hold must also lay the block out for one more name. `test_print_credit_hold_keeps_ozden_and_yim_off_the_poster_credits_alone` in `packing/tests/test_known_best_atlas.py` holds both facts.

Done when: the next infographics cut credits Yim at 260 (and Özden at 204 and 299, think-tj4o), the hold is empty, and the block fits.

## Notes

2026-11-05 (bold-ritchie-l48): done together with think-tj4o, Doğa Özden's names at 204 and 299 on the same hold, at the next infographics cut; neither bead can close alone, since the edition tie empties the whole hold and emptying it overflows the block. The hold's refusal message (`print_credit_hold_problems`) names both beads, and test_print_credit_hold_keeps_ozden_and_yim_off_the_poster_credits_alone asserts that Yim's name alone keeps the 1-100 canvas at 3898 px (F6 of #911's senior review).

2026-11-05 (bold-ritchie-l51, #914's adoption, think-lrj4, draft PR #916): T-269, Evan Daniel's own packing of #914 at 260 (the tilted island of his #845 packing, from a search started from Kirill Tymchishin's Kaggle notebook packing), replaces T-265 there, and the case record credits Daniel alone (found_by [Evan Daniel], improved_by []). Yim is credited at no current count, so PRINT_CREDIT_HELD no longer holds him: it is {299: ('Doğa Özden',)}. T-265 keeps its register entry, and the case record keeps it as an earlier house claimed by Evan Daniel and Kaelan Yim. This bead's done-when (the next cut credits Yim at 260) no longer applies; whether to close it now or with think-tj4o is the coordinator's call. The hold's refusal message still names both beads.

2026-11-06 (bold-ritchie-l51, F2 of #916's senior review): the coordinator asked to close this bead, since no current count credits Kaelan Yim. The close guard, `python -m devtools.check_bead_tree --before-close think-hgpg`, run from the #916 branch at 262d6e1fb plus the review fixes, exits 2: it refuses off main ('a bead closes only once main stops naming it'), and main still names this bead in build_known_best_atlas.py's refusal message and in test_known_best_atlas. #916 drops both, so the bead closes once #916 is on main and the guard, run there, exits 0; it was not closed here. Reason to give then: T-269 replaced T-265 at 260 on 6 November 2026 (#916), the case record credits Evan Daniel alone, Yim is credited at no current count, and PRINT_CREDIT_HELD holds only Özden at 299 (think-tj4o).
