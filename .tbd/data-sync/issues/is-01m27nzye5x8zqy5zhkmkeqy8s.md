---
type: is
id: is-01m27nzye5x8zqy5zhkmkeqy8s
title: Correct PR149 PDF diagnostic attribution and evidence scope
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels: []
dependencies: []
parent_id: is-01m26rygs7f0s76v147x0px4cd
created_at: 2026-09-11T07:30:26.884Z
updated_at: 2026-09-12T14:13:40.644Z
closed_at: 2026-09-11T07:38:02.807Z
close_reason: Made PDF difference attribution span-aware with cross-reference, trailer, and inter-object controls; neutralized runtime, D-490, synopsis, module, and prepared PR-body claims; retained host-qualified 211351-byte and historical 17/18-page evidence; updated current cost to 22 pages; 18 focused tests, Ruff, BasedPyright, render_defects check, synopsis check, and diff check all pass.
resolution: null
duplicate_of: null
---
Independent final review found that _difference assigns trailer, xref, and inter-object byte differences to the previous object; the runtime and D490 prose generalize one host-bound 211351-byte unfinished-face control into a categorical cause statement; and one current render-cost sentence still says 17 pages after the stack moved to 22. Track object spans explicitly, add outside-object controls, make the failure text and records neutral about cause, update current pagination language, regenerate derived docs, and rerun focused/static/record checks.
