---
type: is
id: is-01m5gam02n3a9fnet9gaq8p4v8
title: "Owner decisions for #715 (and #666): counts above 1024, recipe-only rows, 335, hosting the bulk certificates"
kind: task
status: in_progress
priority: 1
version: 2
delegate: coord-intake-1021b
labels:
  - result-import
  - decision
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T22:51:56.373Z
updated_at: 2026-10-21T22:51:57.158Z
started_at: 2026-10-21T22:51:57.158Z
---
From the read-only triage of #715 (c-triage-715; full text: policy.md in the coordinator scratchpad triage-715/). No rule sets a ceiling above the n <= 324 horizon or mentions 1024, but the record holds nothing above 998, and #666's eight counts above 1024 wait on the same question.
D1. Track counts above 1024? Recommended: yes, no ceiling, rows recorded as reported (one answer covers #666).
D2. Do L-border/tiling rows with no certificate file of their own become rows? Recommended: yes, decided exactly from the recipe by a maintained checker; write the rule into the frontier README (4e4c8ce's deletion bounds wait on it too).
D3. Name a key reason to record 335 (#715's certificate is 1.84e-11 above Couzo's own 8 Oct decimal row)? Recommended: no; check the 8 Oct decimal poses exactly first; if they fail, propose a deferred-conflict correction.
D4. Host the certificates above 1024 (25-89 MB as Git stores them; OR-18)? Recommended: yes, a hosted-data manifest staged in the stage 2 PR; the owner publishes data/couzo-715-certificates-v1.
D5 (already open on #686): per-row credit beyond the horizon.
blocked_on: none
