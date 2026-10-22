---
type: is
id: is-01m5jn336nm6erpp0ygedhgpva
title: "Significant-result announcements fail silently: T-194 (S5) never announced; make S4/S5 News systematic (owner: most urgent)"
kind: epic
status: open
priority: 0
version: 11
labels:
  - process
dependencies: []
child_order_hints:
  - is-01m5jn352zx91cynrscj9prwne
  - is-01m5jn36mh8x87f540ps2bc4jr
  - is-01m5jn38xtd10xgdmshtkeat2w
  - is-01m5jn3aef5zxqyjnpk4q15xjf
  - is-01m5jndazhq3txnf5w5vzkv3w2
  - is-01m5jpfmjqpbx2geqhn5aqw43e
  - is-01m5jpfpf3dd0ftcn7tq0hckne
  - is-01m5jpfr0qy3dwar98cc3g4jzn
  - is-01m5jpfse3y2j2thgax8h0ejbv
  - is-01m5jpfvqftdgnchf2rmw46wsa
created_at: 2026-10-22T20:33:25.717Z
updated_at: 2026-10-22T20:57:52.623Z
---
Owner, 22 October 2026 (in conversation): "this means we have a serious failure in the process ... This is the most urgent part of the work." Significant results are not announced systematically.

Measured on main e44a51f44 (coordinator):
- T-194 (S5, landed 16 October, Fitzharding's Lean proof that Wainwright's packing is optimal, s(19) = 3 + 4√2/3) has NO News item (no site-changelog.yaml entry lists it in result_ids). The home page's News box shows S5 announcements only, so it has led with a 13 October item for six days.
- 13 S4/S5 results landed 1–29 September (T-010, T-017, T-018, T-019, T-020, T-022, T-024, T-025, T-026, T-037, T-047, T-051, T-052) have no News item; T-060 (30 Sep) is the first with one. Whether the News archive existed then is to be checked.
- 26 S3+ results landed since 16 October have no News item (T-189, T-194, T-197, T-200..T-219, T-221, T-222, T-224); 43 since 10 October have one.
- Nothing enforces an announcement: the runbook renders one into the PR description "for the owner" (result-import.md ~73-82, 189-191) and says agents never post the announcement.

Owner decisions: S4 and S5 are the significant results, handled systematically; the home page News box has a discreet significance filter at the top right, preselected to S5 when there are enough S5 items for the box, else S4+S5.

Children: root cause and postmortem; the S4/S5 announcement gate and runbook step; the T-194 backfill (and the September decision); the home page filter; the S3 announcement audit.
