---
type: is
id: is-01m42x9sy9mvd5sqqs7skwmfkp
title: "generate_frontier_case: fix the stale promotion/intake path before anyone runs --refresh"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m42sq026mszrdm4fwf5r8g8y
created_at: 2026-10-04T07:33:21.480Z
updated_at: 2026-10-04T07:33:21.480Z
---
From the #305 review-fix lane (think-4mzm): generate_frontier_case --range 101 324 --check reports 21 drifting records (101-105, k^2-3 and k^2-4 cases). No bound differs, but the generator (1) drops intake/update prose, (2) writes reported_status/status open for the 16 k^2-3/k^2-4 cases (it computes status before the lower-bound promotion), (3) attributes non-Karakus verified lanes (e.g. 257/25, T-064's k) to Nagamochi's general theorem with the pre-2-October template, (4) drops E-karakus-strip-lower / E-nagamochi-lemma1-counterexample from 13 records. --refresh on these would write false attributions; no gate runs --check. Fix the generator so --check is clean on all 324, then gate it.
