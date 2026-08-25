---
type: is
id: is-01m0w0cmp6zct0dze7qkpb8r7r
title: "PR #31 review 3: replace floating LP with the declared numerical method"
kind: bug
status: closed
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels: []
dependencies: []
parent_id: is-01m0w0c7yd4nabyntb3137stwm
created_at: 2026-08-25T08:25:33.637Z
updated_at: 2026-08-25T08:27:32.522Z
closed_at: 2026-08-25T08:27:32.509Z
close_reason: "Fixed PR #31 finding 3: the assurance slot now uses `numerical-f64`; floating-point LP remains a plain-language description of the refiner."
resolution: null
duplicate_of: null
---
PR #31 comment finding 3. TUTORIAL.md:613 uses `(floating LP)` in the method slot beside a row using `numerical-f64`. Replace the informal label with the actual schema method and retain LP as explanatory prose if useful.
