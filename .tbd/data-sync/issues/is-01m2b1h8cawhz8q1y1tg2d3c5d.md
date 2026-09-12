---
type: is
id: is-01m2b1h8cawhz8q1y1tg2d3c5d
title: Reap calibration workers on SIGTERM, SIGHUP, and launch-window interruption
kind: bug
status: closed
priority: 1
version: 10
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol xhigh implementation or source-distinct review; root integration
labels:
  - n11
  - calibration
dependencies:
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
  - type: blocks
    target: is-01m2b4yfx3th5wcdaw9apr0vn5
parent_id: is-01m2app5e71qnp9z5vfp9vppbp
created_at: 2026-09-12T14:49:51.753Z
updated_at: 2026-09-12T16:31:20.121Z
closed_at: 2026-09-12T16:31:20.121Z
close_reason: Astra Max source-distinct correction review at exact head b6260970 accepts CAL-2, CAL-3, CAL-4, and CAL-6. The review independently checked the repairs and representative regression sensitivity; 176 target-free tests passed with one environment-dependent test explicitly deselected, and Ruff passed. The distinct CAL-5 staging-acquisition signal window remains open. No full-shape profile or BC329 target ran.
resolution: null
duplicate_of: null
---
CAL-4 from the Astra Max source-distinct review. A real pause-only control showed SIGTERM exits the calibration supervisor with its worker alive and receipt partial with process_group_reaped false. Port the independently admitted signal, launch-window, restoration, cancellation, and process-group cleanup contract into the separate calibration supervisor, and retain real signal controls. The reviewer killed the owned test group; no BC329 target ran.

## Notes

Implementation correction is retained at 0533ebaeb90cf42acf20e0029535356282a5624c. SIGINT now shares the launch-window deferral used by TERM and HUP. The real subprocess control delivers SIGINT after child creation but before Popen returns, verifies worker disappearance, records signal provenance and truthful reaping, and proves the prior handler was restored and invoked on redelivery. Author validation: combined suites 177 passed in 18.07s; repository-wide Ruff and BasedPyright clean; edit tier passed in 50.83s. No full profile or BC329 target ran. Leave open for source-distinct re-review.
