---
type: is
id: is-01m22dpzdy703v9pq1yyfqbph7
title: "Record spike B's loop defects: premature ROWS COMPLETE and float provenance refused"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-09-09T06:29:32.222Z
updated_at: 2026-09-09T06:29:32.222Z
---
Two defects from the threshold loop, evidenced in the lane B report: lp_threshold2.py reports a sweep cut by its deadline as complete (run 3 declared ROWS COMPLETE with directions 80-180 unswept), and freeze_candidate.py wrote provenance.lp_objective as a JSON float, which decide_threshold_certificate's strict parser refuses before deciding anything. Both scripts are scratch-only; record them in defects.yaml if the loop is promoted to a devtool, with the retained logs as evidence.
