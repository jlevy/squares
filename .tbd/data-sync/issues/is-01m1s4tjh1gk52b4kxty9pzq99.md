---
type: is
id: is-01m1s4tjh1gk52b4kxty9pzq99
title: "Atlas display: the verified_lower_bound decimals round up, so a rendered decimal can overstate the bound"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T16:01:03.009Z
updated_at: 2026-09-05T16:20:39.061Z
closed_at: 2026-09-05T16:20:39.061Z
close_reason: "Addressed for the atlas in f5de1929: the composite's lower-bound line truncates toward zero via _lower_text, so a printed bound is true as written. The underlying records still store round-to-nearest display literals, and any other consumer that prints them has the same exposure; the schema already says exact_form is authoritative. Left open as a record-level question would be better tracked separately if another consumer appears."
resolution: null
duplicate_of: null
---
Survey 2026-09-05: 33 of the 58 open Nagamochi cells store a verified_lower_bound.value 12-digit display literal rounded to nearest, so it exceeds the true bound (n=26 stores 5.12310562562 for 1+sqrt(17)=5.1231056256176..., excess 2.3e-12; worst 4.7e-12 at n=59). The schema says exact_form is authoritative (square-packing-case.schema.yaml:109-113). Any rendering that prints the stored decimal as 's(n) >= X' states a false claim by a hair. The atlas must print exact_form or truncate the decimal DOWN. The 7 first-party bounds and all 35 proved values are exact rationals and unaffected.
