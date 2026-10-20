---
type: is
id: is-01m53v15gh50zjfvc07fhfw38k
title: "Exact sides: hold a closed form whose minimal polynomial is a non-monic quartic (#660 C13)"
kind: task
status: in_progress
priority: 3
version: 2
delegate: user-eb-policy-houses
labels:
  - regularization
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
hold: null
hold_until: null
created_at: 2026-10-17T02:28:37.521Z
updated_at: 2026-10-17T02:28:42.702Z
started_at: 2026-10-17T02:28:42.701Z
---
Review C13 of #660 (https://github.com/jlevy/squares/pull/660#pullrequestreview-5555366472), deferred by #660's addressing pass.

A closed-form ceiling whose minimal polynomial is a non-monic integer quartic, such as (sqrt(2)+sqrt(3))/2 with minimal polynomial 16x^4 - 40x^2 + 1, is refused by `devtools.exact_sides.of_bound`: `sqpack.field`'s irreducibility search cannot certify the polynomial, so the count reads unordered and `select_houses --check` fails on it. The same number read as a field element is held, because a field element's minimal polynomial is irreducible by construction (B3's Sturm-only read).

No verified ceiling has such a form today, and the refusal fails loudly rather than misordering anything.

Fix: cover every integer quartic in `sqpack.field`'s quartic factor exclusion through the monic transform q(y) = a^3 p(y/a), which is irreducible over Q exactly when p is. Alternatively, apply the transform in `exact_sides` before validating a closed form. Add a test with (sqrt(2)+sqrt(3))/2 as a closed form, held exactly, and with a reducible non-monic quartic refused.

Files: packing/src/sqpack/field.py or packing/devtools/exact_sides.py, packing/tests/test_exact_sides.py.

Done when: `exact_sides.of_bound` holds (sqrt(2)+sqrt(3))/2 exactly, and the test above passes.
