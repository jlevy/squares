---
type: is
id: is-01m2gyhy8jxc1p27shs4gfdkj0
title: Closed-form lines under Proven do not say which bound they belong to
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2gyhqfmr0xpcjsr34na3acq
created_at: 2026-09-14T21:53:14.697Z
updated_at: 2026-09-14T22:16:23.563Z
closed_at: 2026-09-14T22:16:23.561Z
close_reason: "Fixed in c94054c4: the closed-form and degree line under Proven is removed, and badges and OPEN close up 90 px. 108 of the 110 n that showed one had a two-bound chain; only n = 5 and 10 were equalities. The data keeps html_exact and degree for a design that attaches a form to its bound. check_workbench.py asserts no .exact element."
resolution: null
duplicate_of: null
---
Owner, 2026-09-14: "the math formulas present on some values of n below the Proven line are unclear as they say an exact closed form but it's not clear if it is for the upper bound or the lower bound directly above it. probably we should just skip these unless you can think of a cleaner design."

Under the proven chain `lower <= s(n) <= upper`, some n show a closed form or a description such as "algebraic, degree 18", and nothing says which bound it belongs to.

Default: drop the line. A cleaner design is worth doing only if it reads as unambiguous at a glance. For example, when `s(n)` is known exactly, the chain is already an equality and can carry the closed form itself, `s(10) = 3 + 1/sqrt(2)`; a strict chain then shows only decimals. Whatever ships, no closed form appears detached from the bound it is the value of.
