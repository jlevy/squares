---
type: is
id: is-01m0vxwz54jtrrk1xvg7z3fc46
title: "TUTORIAL accuracy drift: five claims that no longer match SYNOPSIS or the record"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m0vxe4ntpat4xcagtf04c37z
created_at: 2026-08-25T07:42:02.915Z
updated_at: 2026-08-25T07:42:02.915Z
---
Checked every number, count, and attribution in `TUTORIAL.md` against
[`SYNOPSIS.md`](SYNOPSIS.md), [`conventions.md`](conventions.md), the experiment
artifacts, and the source. Most of it holds—the `n = 11` bounds and gap, the 14-of-55
zero-separation pairs and 20 boundary coordinates, `2 + (4/3)√2 ≈ 3.885618` for the
`0°`/`45°` class, the `4.4e-16` LP rebuild agreement, the D-029 `n = 10` figures
(`+5.6440e-04` versus `+4.4409e-16`), the `[38°, 42°]` scan, degree 8 over `ℚ(u)`, six
angle classes at `n = 29`, the 20-strategy and 30-strategy catalogue counts and their
family splits, and the two-then-three unknowns at `n = 11` and `n = 17`.
Every relative link resolves. Five things do not.

## 1. The gate has thirty-one steps, not thirty

§6: "a thirty-step gate all exist, and the whole gate runs in one to two minutes."
`SYNOPSIS.md` ("Reading the gate") and `conventions.md` §10 both say `packing-validate`
runs **thirty-one** steps, and the recorded checkpoint is "all 31 normal-gate steps in
103.91 wall-seconds". The timing claim is right; the count is one low.

## 2. "None recovered from a search output" now has an exception

§6: "Every exact configuration in the repository—Trump's packing, the `n = 3` and
`n = 4` optimal families—was authored from published data or derived analytically, none
recovered from a search output."

`SYNOPSIS.md` says "`exact` **almost always** means checked something already known
exactly", and names the exception: exp-033's pair of exact `n = 5` endpoints, recovered
from retained *search* poses at their shared nonoptimal side, through a dedicated
single-instance checker rather than a general tool.
The tutorial's headline claim—no general executable path—still stands.
The absolute sentence under it does not, and it is the sentence a careful reader will
quote.

## 3. §4 attributes the wrong baseline column

§4: "Replacing smooth descent with a bracketing search over merged angle classes … took
`n = 5` from `3.4e-08` to `2.2e-15` and `n = 10` from `5.3e-03` to `1.3e-15`."

Those baselines are the **annealer** column of `SYNOPSIS.md`'s table, not the descent
column. Descent gives `3.1875e-08` and `4.507e-03`; the annealer gives `3.4274e-08` and
`5.318e-03`. The endpoints are right and the conclusion is unaffected—either fix the
verb to name the annealer output as the starting point, or use the descent figures.
Same mismatch in §4's `n = 11` sentence (`8.8e-02 → 6.3e-02` is annealer-to-bracketing,
while descent is `6.999e-02`), though there the synopsis phrases it the same way.

## 4. The separating-axis statement drops the word the section depends on

§2: "Two convex polygons are **disjoint** exactly when some line separates them."

`SYNOPSIS.md` writes it correctly: "Two squares have **disjoint interiors** exactly when
some line separates them." The distinction is the tutorial's own §1 headline—touching is
legal, and 14 of 55 pairs touch—so interior-disjointness with weak separation is exactly
the case that matters. As printed, the sentence describes the case the project does not
have.

## 5. Missing: the whole `n = 5` terminal-family lane

exp-033 through exp-036 landed on 2026-08-24, the same day as the tutorial's last edit,
and the tutorial does not mention them. They are the campaign's current live frontier—
`SYNOPSIS.md` gives them their own section ("The Current `n = 5` Handoff") and leads
"Where This Stands" with them: an exact fixed-angle optimal face shared by two retained
poses, an exact two-parameter angle-and-slide sheet containing it, complete first-order
systems admitting one non-sheet direction, and an exact second-order obstruction
excluding that direction from the true Bouligand tangent cone.

This matters for the tutorial specifically, not just for completeness.
§3's Trap 2 is argued entirely from the `n = 3` sliding family, which a reader can
dismiss as a degenerate toy. The `n = 5` sheet is the same phenomenon at a size that is
not obviously trivial, and it is the case where the project is actually working.
§6's and §8's statements about what is built and what is open are shaped by it.

## Also worth deciding, lower confidence

- **`s(n)` as minimum versus infimum.** §1 says "the side of the **smallest** square
  that contains `n` … squares"; `SYNOPSIS.md` says "the **infimum** of the `s` for which
  one exists". Both readings are used in the directory, and `README.md` uses "smallest".
  Attainment follows from compactness and there is a primary source archived for it
  (`resources/papers/martin-2000-compactness-theorems-geometric-packings.pdf`).
  A tutorial is the right place for one clause saying the infimum is attained, so the
  two words agree on purpose rather than by accident.
- **Unattributed record.** §1 and §7 give `n = 17`'s `4.6755` with no source, while
  Trump's `n = 11` value is attributed in the same table. It is Bidwell 1998, per
  `SYNOPSIS.md`'s lay-of-the-land table.
