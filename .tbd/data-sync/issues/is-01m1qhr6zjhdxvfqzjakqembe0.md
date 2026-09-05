---
type: is
id: is-01m1qhr6zjhdxvfqzjakqembe0
title: SYNOPSIS n = 11 fact table, TUTORIAL figures and T-017's gap figure still describe the pre-T-018 rung
kind: bug
status: in_progress
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-05T01:08:28.273Z
updated_at: 2026-09-05T01:17:45.467Z
---
Found by the think-rl03 port. Pre-T-018 figures still stand in durable prose: SYNOPSIS.md's n = 11 fact table gives 'Best certified lower bound | 2 + 4/sqrt(5) = 3.788854382...'; TUTORIAL.md gives 'best lower bound | 2 + 4/sqrt(5)', 'bound gap 0.088229208023 | open since 2003' and 'The interval [3.788854, 3.877084] has stood since 2003'; and T-017's significance rationale in results.yaml says 'the gap to the conjectured 4 is 0.07' where the claim says 0.04. All D-442/D-439 class: a durable record describing a rung after the rung moved. Fix each from the artifacts (n-011.md front matter, results.yaml T-018/T-017), and extend check_rung_figures or check_synopsis to read the fact-table and gap forms so the class cannot recur there. Record as a defect entry with recurrence_of D-442.
