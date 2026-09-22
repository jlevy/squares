---
type: is
id: is-01m32t2yc3xenfb97kxn844rc7
title: Stage layout revision for the ascent video
kind: epic
status: open
priority: 1
version: 26
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
child_order_hints:
  - is-01m32t26s6dbh3ab5g7n2epn9m
  - is-01m32svwep5f1qatwy5hj65zgh
  - is-01m32szhzvqgp7awv3kd69m95p
  - is-01m32stt4mg3cb4mwg654dxhqv
  - is-01m32ssx2nkebzvt6mqqrv5b1z
  - is-01m32tj6292r9kke6622mkc14c
  - is-01m32tnmps6qw5h8tde5xq9zmw
  - is-01m32ypsxmkf33wwk99djtqd52
  - is-01m3319g2ggyq2yrrtth7xzxkv
  - is-01m336y5tjaf1xvy8mh6mp2fad
  - is-01m336y682k19wzvvppep4jh36
  - is-01m336y6n04th664pbvpnkyx4e
  - is-01m338m3kdks21pzathyt75ksr
  - is-01m33ba5vyzekrecg2br1k5nes
  - is-01m33ba6m8vbx0bcbk9qqn84sa
  - is-01m33bbb6ra0f844hfak2w97wd
  - is-01m33bc36wk6ma25mk93sqt1kc
  - is-01m33bj34g60trhsnazpyetwsj
  - is-01m33dg2182wpdc4xef4f072aw
  - is-01m350manrfxvxb7xwyhbdgkyh
  - is-01m351fy0zas9zjmwrdq7v54wx
  - is-01m354hkswsakmr8mnhf60m2mz
  - is-01m354ty99aychrjcyq62qvwyn
  - is-01m354tywpqgb1eek5dwddvbaq
  - is-01m354v0cb5an8kycvyh93n1xf
created_at: 2026-09-21T20:21:29.084Z
updated_at: 2026-09-22T18:07:52.202Z
---
One pass over the 1920x1080 poster the video is captured from, gathering the owner's requests from the 2026-09-21 review of the first cuts. They are one piece of work because they all move the same space: the middle gap between the packing box and the facts column.

**The column, top to bottom, after this pass:**

1. `n = ...`, moved up from below the box (think-gln1)
2. KNOWN BOUNDS, a section head in PROVEN's styling (think-gln1)
3. the gap bar with its ticks and sqrt labels
4. PROVEN, the chained bound, the badges
5. OPEN, when anything is open
6. the composite's explanatory lines and `github.com/jlevy/squares`, smaller (think-kgx1)

**The geometry:** the box grows and the column widens, both into the middle gap (think-emuj, think-sc44). The box ends at x = 1060 today and the column starts at x = 1160.

**Why one bead and not five:** every one of these changes the amount of space the others have, so each is only measurable against the rest. Doing them separately means measuring the same frame four times and getting three wrong answers.

**What must be re-measured, not assumed:**
- Every element in the column is absolutely positioned at a fixed top; moving the headline in shifts all of them.
- `layoutHeadline` measures the numerals once the faces land and sets `--stage-numeral-left`; the roll has to keep working wherever the headline goes.
- Stage sizes are `--stage-*` tokens in stage pixels, not the UI scale, and the type scale has a floor because a device scale below one blurs it.
- The design-system test refuses raw values for tokenised properties.
- The widest bound over the corpus is `10.055385 <= s(101) <= 10.535534`.

Verify in a captured frame at 1920x1080 under capture preview, not in the browser pane: the explanatory text explains the PICTURE and must survive capture preview, which hides everything that explains the PAGE.
