---
type: is
id: is-01m3zkb0bxkq14tc7sepc0xqa6
title: "Homepage: the problem intro in the owner's words of 2026-10-03, with checked s(29) examples"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-03T00:41:31.773Z
updated_at: 2026-10-03T14:38:03.471Z
closed_at: 2026-10-03T14:38:03.471Z
close_reason: Merged in jlevy/squares#312 (c831b4ee0), after a correctness and engineering review round (419a1db5d)
resolution: null
duplicate_of: null
---
Owner, 2026-10-03: README's project-intro block (rendered as the homepage's first section) reads: 'The square packing problem is a simple and long-standing problem in geometry: what is the size of the smallest square that can hold n unit squares, where the squares are free to rotate but cannot overlap? The side length of that smallest square is written s(n). / The question of the value of s(n) is simple but the answer is an open problem for most n. In many cases, s(n) is known only to lie between an upper bound (the size of the enclosing square for the tightest packing ever discovered, such as s(29) <= 5.934) and a lower bound (a size below which it is proved that no packing can exist, such as s(29) > 5.79).' Confirm the example values against the record. Checked: upper 5.93383346... (verified, T-009) so s(29) <= 5.934 holds. Lower: 5.79 is wand125's reported bound of 2026-09-28, written s(29) >= 579/100, whose coverage replay has not run here; the verified and atlas-shown lower bound is s(29) >= 5.71 (Tokoharu, T-047). The text uses the verified 5.71 with >=.
