---
type: is
id: is-01m53fpy7t6jb17mc9gsdhha75
title: "Regularization: a second exact route over number fields, so a strong view at an algebraic house can be admitted (#660 A4)"
kind: task
status: in_progress
priority: 2
version: 4
delegate: w-regularize-algebraic-1026
labels:
  - regularization
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
hold: null
hold_until: null
created_at: 2026-10-16T23:10:48.058Z
updated_at: 2026-10-26T03:38:04.868Z
started_at: 2026-10-16T23:10:55.263Z
---
The regularization of the exact algebraic houses: a regularizer that draws an exact view of a number-field witness at or below its house's side, and a second exact route that admits such a view (#660 A4; scope restated by review A3 of #756 on 24 October 2026).

Under the house rule an algebraic house is adopted like any other, and then regularized like any other. Since #756 the house writer writes an algebraic side, and these counts draw their exact houses unregularized: T-174 at 153 and 207, and T-193 at 102, 123, 258, 259 and 302. Each is `regularization-owed` in `packing/atlas/known-best/default-drawings.json`, and its `default_drawings.SETTLED` entry's `owed` names this bead, which `check_bead_tree` holds open through `default_drawings.deferrals`. (70 and 295 read regular as published and owe nothing.) An algebraic house adopted later at another count, such as T-193's remaining staged counts, joins this scope the same way.

What is missing today, on the runs of 23 October 2026 (`packing/cases/regularized_drawings/think-ot5c-2026-10-23/`):
- a generator: grid-slack has no exact frame on a number-field witness (`no-exact-frame`) and draws nothing, and Evan Daniel's regularizer solves each count to a rational side 1.06e-19 to 1.79e-19 above the algebraic U, which is held at row 4 (no rational view is `same` or `bound` at an irrational side) and, by the owner's answer to question 13 (think-r8cn, 23 October), is not drawn: a regularized drawing changes the side only as a strict improvement;
- a second exact route: a number-field view must be decided on two exact routes (regularization policy, obligation 1), and only `sqpack.field`'s route decides a number-field pose today. This is the W7 checker this bead first named: one that decides a number-field pose exactly on a route independent of `sqpack.field`'s.

Done when: each count above has run a strong generator that draws an exact view of its number-field witness at or below the case's verified side, judged by the improvement rule on an admitted view, so that its state is `regularized` or `decided-no-better` and its `regularization-owed` entry is gone from `SETTLED`.

## Notes

2026-10-24 c-fix-756-1024 (review A3 of #756, https://github.com/jlevy/squares/pull/756#issuecomment-6378226088): description rewritten to the bead's true scope, the regularization of the exact algebraic houses at 102, 123, 153, 207, 258, 259 and 302, which needs a regularizer for number-field witnesses as well as the second exact route. The done-when alternative "or the owner's answer to question 13 is recorded" is dropped, since that answer is recorded (think-r8cn, 23 October) and leaves the regularization owed. The stale delegate `user-eb-policy-houses` (the 16 October lane) is cleared and the status set to open: nobody is acting on it. It stays open because `default_drawings.SETTLED` names it in the seven entries' `owed`, which the bead-tree gate holds. `_OWED_MBDW` in `packing/devtools/default_drawings.py` says the same in #756.

The description as it stood until this note (written 16 October 2026 under #660 A4):

> Review A4 of #660. Under the house rule an algebraic house is adopted like any other. Its count's regularization runs then settle it, because no strong view can be admitted at an irrational side today:
> - no rational view is `same` or `bound` there (obligation 2, row 4);
> - no number-field view is decided on two exact routes (regularization policy, obligation 1; the follow-up of question 4).
>
> That holds for T-174's houses at 70, 153 and 207 on main and for 19 houses on the stack (T-174's three and T-193's 16). Today a strong view draws 12 of the stack's counts: 88, 126, 153, 175, 204, 207, 259, 266 and 301 (Evan Daniel's driver) and 199, 267 and 292 (grid-slack). They would settle on the axis view or the house drawing.
>
> This bead is the second route: a W7 checker that decides a number-field pose exactly on a route independent of `sqpack.field`'s, so that a view at an algebraic house can pass obligation 1. Keeping a rational view just above an algebraic U instead is a question 13 decision for the owner. It is put once, with the counts it concerns, and it holds no adoption.
>
> Done when: the policy names the second route for number-field views, and a strong view at an algebraic house is admitted on it, or the owner's answer to question 13 is recorded.
