---
type: is
id: is-01m2cxe5qged60egs7wx42616j
title: The generated session cost table labels summed concurrent agent spans as wall time
kind: bug
status: open
priority: 2
version: 1
labels:
  - research-tooling
dependencies: []
created_at: 2026-09-13T08:16:45.296Z
updated_at: 2026-09-13T08:16:45.296Z
---
Found while correcting PR157's cost summary (review DOC-04). Not in the review.

THE DEFECT. devtools/close_session.py totals() reads each rollup's span.wall_seconds (line ~157) and converts it to hours; the rendered table heads that column 'Wall' (line ~593). Summing one wall figure per rollup is right for rollups that ran one after another, and wrong for rollups that overlapped: concurrent spans are added as though they were sequential, so the column reports more elapsed time than the clock ever showed.

MEASURED on session-127. Five read-only delegates, each with its own rollup:
  sum of spans:                      1978.818 s  (0.55 h)
  contiguous union of their windows:   706.667 s  (0.196 h, 19:48:00.123Z to 19:59:46.790Z)
  overstatement factor:                   2.80x
The generated per-session row reads 0.54 h for this session -- the same sum after each rollup is rounded to two places before adding -- under a column headed 'Wall'. The true elapsed figure is 0.196 h.

WHY IT MATTERS HERE RATHER THAN BEING COSMETIC. OR-9 says a pull request leads with what the branch cost, and this table is the generated evidence a PR body is supposed to quote. A number labelled 'Wall' that is 2.8x the clock invites exactly the claim the project's own documentation standard forbids -- asserting a measurement that was not measured. Running more delegates in parallel makes the reported 'wall' cost go UP, which inverts the incentive the figure exists to create.

The table's preamble already warns against summing a SHARED log across sessions. It does not warn against summing CONCURRENT rollups within one session, which is the same error one level down.

PROPOSED FIX, owner's choice:
1. Rename the column to 'Agent time' (or 'Summed spans') and leave the arithmetic alone -- cheapest, and honest.
2. Compute the union of the rollup windows when every rollup carries a start and end, and report that as 'Wall' with the sum kept alongside as agent time. The data needed is present: each span has both endpoints.
3. Report both unconditionally, since the ratio between them is itself informative about how parallel a session actually was.

Option 2 is the one that keeps the column's name true; option 1 is the one that can land immediately.

NOT CLAIMED: no audit of how many other sessions in the corpus have concurrent rollups, so the scale of the corpus-wide overstatement is unmeasured. What is established is the mechanism and one measured instance at 2.80x.
