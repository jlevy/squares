---
type: is
id: is-01m1q7tdecqsw4j2007eke0bek
title: "Tab selector on the certificate page: 19/5 (default) or 381/100"
kind: task
status: closed
priority: 2
version: 3
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1q0p63s2evef5mhkyn16e41
created_at: 2026-09-04T22:14:54.656Z
updated_at: 2026-09-04T22:40:11.034Z
closed_at: 2026-09-04T22:40:11.033Z
close_reason: "Commit f05a7ccb: the renderer stamps one article, tab and script per certificate (19/5 default, 381/100 second), server-side and exact; the picker toggles visibility and records the choice in the hash. Figure 5 attaches only to the certificate net-coarsening.json names."
resolution: null
duplicate_of: null
---
Review direction on PR #79. The page carries both retained certificates and a two-tab picker at the top chooses which proof is walked through: 19/5 = 3.8 (425 atoms; the simpler one, default for explanatory value) or 381/100 = 3.81 (1121 atoms; the tighter bound). The headline stays s(11) ≥ 381/100. Every quantity is rendered server-side per certificate, exactly, as now; the client only toggles which article is visible, with the choice in the URL hash. Figure 5 attaches only to the certificate net-coarsening.json names in its certificate_id.
