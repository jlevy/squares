---
type: is
id: is-01m51ctckj8khpbpkw54wn45eb
title: "PR #636 C1: admission guard measures a candidate against the layer's view even where the rule does not draw it (n = 176 undrawn axis view vetoes a strong view better than the drawn house)"
kind: bug
status: closed
priority: 2
version: 3
delegate: tbd-moderate-pr636-c
labels: []
dependencies: []
parent_id: is-01m51ct5f1m0k1swz8x23dkd7p
hold: null
hold_until: null
created_at: 2026-10-16T03:41:46.482Z
updated_at: 2026-10-16T04:01:32.401Z
started_at: 2026-10-16T03:41:51.221Z
closed_at: 2026-10-16T04:01:32.400Z
close_reason: "fixed in 89ef0da33: regularize_select.drawn (the record's default picture via default_drawings.judged) is the reference for the selection and for admission (regularize_evand.worse_than_drawn); test_a_view_is_held_to_the_drawn_house_not_to_a_view_the_rule_holds replays 176's measures (fails with the old reference on ([4], []) == ([], [4])); test_a_view_is_judged_against_the_picture_the_record_draws on real data"
resolution: null
duplicate_of: null
---
Severity Low. PR #636 review C (https://github.com/jlevy/squares/pull/636#pullrequestreview-5542797505). Files: packing/devtools/regularize_evand.py:3213 (now = select.today((root, n, {n: entry}))), packing/devtools/regularize_select.py:334-337 and :670 (today goes through census.drawing_for, which returns the layer's view whenever the index says regularized, drawn or not); rule: docs/project/guides/regularization-process.md:18-29. At 176 the axis view (33/73/45/76/19/146/409) is undrawn; the house (70/71/52/83/19/33/393) is drawn. A strong view at 40/60/45/76/19/146/409 improves on the drawn house but is kept out as worse than the layer's view on light_axis. Fix option (a): compare against the drawn picture in worse_than_layer and regularize_select.today. Blocks think-la7h (176 first).
