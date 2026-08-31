---
type: is
id: is-01m0wer5thdeaa90gg0mapcwbw
title: Correct session-011 synopsis aggregate
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/campaign/hypotheses/H-037-asymptotic-waste-exponent.md
labels:
  - packing
  - bookkeeping
  - ci
dependencies: []
parent_id: is-01m0rvm4r4s2kf1d81dcscwm2c
created_at: 2026-08-25T12:36:31.696Z
updated_at: 2026-08-25T12:50:48.257Z
closed_at: 2026-08-25T12:50:48.256Z
close_reason: Corrected the derived unprotected-fix aggregate to 106; check_synopsis and the complete gate pass. D-305 retains the pushed red checkpoint.
resolution: null
duplicate_of: null
---
CI check_synopsis computed 106 fixed non-outstanding defects with no regression check, while the source-validation checkpoint manually wrote 105. Correct the canonical synopsis, retain the failed gate evidence, and require the authoritative synopsis check before the repair checkpoint.
