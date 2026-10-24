---
type: is
id: is-01m5p4qp4qzznh1xvyvwvfr758
title: Call source certificate refinements exact conversions, not regularizations, at T-174's other houses and the same wording elsewhere (#756 B1)
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T05:04:32.407Z
updated_at: 2026-10-24T05:04:32.407Z
---
Deferred from review B1 of PR #756 (https://github.com/jlevy/squares/pull/756#issuecomment-6379772274), lane c-fix-756b-1024, bead think-ecz3.

**What.** Under the owner's rule of 23 October 2026 ("there is only the concept of a regularized or not-regularized drawing ... we should convert inexact packings to exact ones. And then we should always regularize as well. We should track regularization separately"), a source's certificate refinement converts a packing to an exact one; it is not a regularization. The case records still call such a house "its source's regularization" (`devtools.regularized_drawings.case_note`, the last branch), and the case page labels the card "Regularization" (`devtools.render_case_pages._regularization`).

PR #756 fixed this at 153 and 207 only, where the note also said the regularization is owed: PR 574's algebraic certificates there (T-174) are now `kind: exact-solve` (`regularized_drawings.EXACT_SOLVES`, which now names counts per source), and `case_note` refuses a source regularization at an owed count.

**Where the word remains** (at #756's head after B1, from `case_fields`):

- T-174, `[PingYou PR 574 certificates 2026-10-13]`, 34 counts: 68, 70, 84, 86, 103, 108, 110, 127, 130, 131, 132, 172, 179, 180, 181, 182, 206, 208, 209, 210, 228, 238, 239, 240, 261, 263, 268, 269, 272, 273, 297, 305, 306, 307. The register's method is "certificate refinement: smaller padding, an exact common-centre crop or an exact re-solve of the packing's own contacts"; 70 is algebraic (an exact attainment, like 153 and 207), the rest rational.
- The same vocabulary at other sources, 12 counts: T-186 (Mishapolk KKT refinements) at 129, 156, 175, 176, 232, 264, 304; T-182 (Couzo) at 241; T-190 (Couzo) at 237; T-195 (PingYou PR 622) at 29; T-229 (Mishapolk issue 719) at 105; T-231 (Mishapolk n204) at 204.
- Not in scope: T-146 and T-225 (Evan Daniel's regularized lists, "fewest" and "conservative") at 292, 227, 229 and 260, which are regularizations.

**Done when.** Each of those counts' source item carries a kind that names the exact conversion it is (exact solve, or an exact-refinement kind with its own card label and schema enum if smaller padding or an exact crop is not a "solve"), the note says so and that it is not a regularization, `regularized_drawings --check` and `test_regularized_drawings` hold it, and the register's `regularizations` lineage is left as it is. Most of these counts draw this project's regularized view, so no note contradicts itself today; the change is vocabulary.

**Waits on.** Nothing but scheduling; it touches up to 46 generated case records, so land it after #756 and #757, which share the case records' generator.
