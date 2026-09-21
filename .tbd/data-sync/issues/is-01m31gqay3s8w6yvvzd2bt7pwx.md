---
type: is
id: is-01m31gqay3s8w6yvvzd2bt7pwx
title: Banner the .out and .json retained scratch files
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:18:37.120Z
updated_at: 2026-09-21T08:18:37.120Z
---
PR 209 re-review, finding 3 residual. The 12 .py.txt files under h230-gap-wedge-scratch/ and h232-ring-centre-scratch/ each open with a banner naming them frozen Session 148 scratch, the lane, the base 19cdd4f8, and why the .py.txt suffix. The 7 .out and 3 .json files in the same two directories carry no marker and neither directory has a README, so a reader opening analyse.out or h232-transported-family-96-25.json gets no signal. Nothing enforces the banners either - the two cheap tests hold the patch header lines, not the script banners.
