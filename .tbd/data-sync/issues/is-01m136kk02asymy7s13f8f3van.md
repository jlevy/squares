---
type: is
id: is-01m136kk02asymy7s13f8f3van
title: "Registry: n=54 has an unrecorded exact closed form"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - packing
dependencies: []
parent_id: is-01m136khr29m0p8t6q8kybd562
created_at: 2026-08-28T03:28:53.754Z
updated_at: 2026-08-28T03:36:17.592Z
closed_at: 2026-08-28T03:36:17.590Z
close_reason: "Not a defect on current main. My survey ran against a stale checkout (branch packing/symbolic-survey-plan predated merges #45/#46/#47). frontier/n-054.md on main already carries exact_form: 7 - (1/2)sqrt(2) + sqrt(1 + sqrt(2)). Verified: evaluates to 7.846667192843489782943314590958298, matching witnesses/known-best/n-054.yaml to all 30 digits. Re-ran the gap scan on main: only n=29,55,68,69,71 have neither exact_form nor minimal_polynomial, and 55/68/69/71 are correctly null."
resolution: null
duplicate_of: null
---
frontier/n-054.md reported_upper_bound has exact_form/algebraic_degree/minimal_polynomial all null, but the archived catalogue carries s = 7 - (1/2)sqrt(2) + sqrt(1+sqrt(2)). Verified: evaluates to 7.846667192843489782943314590958298, matching witnesses/known-best/n-054.yaml side 7.84666719284348978294331459096 to all 30 digits. Only n<=100 whose catalogue closed form is missing from the registry; it is the sole n<=100 rendered in a begin{aligned} block rather than a plain $s = ...$ line, so the original transcription likely skipped it mechanically.
