---
type: is
id: is-01m4jr7mpcvv3wqm8280bt2x19
title: Keep website publication and frontend validation within their contracts
kind: bug
status: in_progress
priority: 1
version: 14
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels:
  - website
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T11:12:38.602Z
updated_at: 2026-10-10T16:13:29.743Z
started_at: 2026-10-10T11:13:19.000Z
---
Resolve PR 462 publication and frontend findings without relaxing existing contracts. Preserve script inventory refusal, native MathML readiness, stable Atlas geometry, 300 ms startup assertions, all browser checks and current effective PR hard ceiling. Retained fixes cover non-inherited Headroom clearance, concurrent browser-lane startup, canonical render setup and Atlas host reuse. Final hosted gates must pass before closure; full pre-merge checkpoint remains think-xio5.

## Notes

Exact head f489084511a56b130e6d86fc46a8260f4fb530bb is committed and pushed to draft PR462. All407 functional browser tests pass with6skips, including reduced motion and startup trace regression. Hosted frontend38065629234/job114252561386 still fails: two desktop HTTP native initial-render tasks303/302ms exceed300ms; mobile cases pass. Overall frontend413.44s exceeds effective330s PR ceiling. All29 other checks pass, including publication and strict papers. Native failing task precedes Atlas JavaScript; Atlas script now36.8/36.6ms with31.7ms forced layout, so removed repeated flushes stayed fixed. Retained CSS reduced-motion correction has matched4targetPASS and Astra approval; corrected final floors all5PASS99.19s. All content/assertions/budgets retained. Two bounded controls now active: per-reading ancestor-style memoization in case layout diagnostic probe, and native MathML wrapper percentage/inline-block sizing. No new production fix or performance benefit claimed before matched measurements. Prior pre-push4658PASS35skip1staleoracle was corrected with exact1PASS; aggregate not repeated. Full pre-merge checkpoint remains think-xio5; all implementation closeouts remain held until exact-final-head hosted checks pass.
