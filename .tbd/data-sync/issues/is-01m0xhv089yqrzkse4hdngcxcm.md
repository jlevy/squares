---
type: is
id: is-01m0xhv089yqrzkse4hdngcxcm
title: Tutorial moduli figure carried six undefined symbols and a colliding axis parameter
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m0wy9s97fwegw5kqrge2p8sy
created_at: 2026-08-25T22:49:44.439Z
updated_at: 2026-08-25T22:55:43.666Z
closed_at: 2026-08-25T22:55:43.665Z
close_reason: "Fixed on the PR 33 branch: significance passage added to TUTORIAL.md section 3, lambda/t relation stated, notation card gains F3(2), S3/D4, and lambda rows; registered as D-335."
resolution: null
duplicate_of: null
---
The F3(2) quotient-map figure in TUTORIAL.md section 3 used F3(2), S3, D4, lambda, the stratum letters, and wall/axes/stab counts with no definition anywhere in the document, against section 10's promise to collect every symbol; its axis lambda in [0,1/2] silently collided with the text's slider t in [1/2,3/2] (lambda = min(t-1/2, 3/2-t) after the t~2-t reflection); and the figure's actual significance - the exact known-answer control behind exp-032's seven rejected false component-identity policies and open question 1 - was never claimed. Fixed: a significance passage defines each quotient stage and what it kills, wires the figure to exp-032 and section 8's open question 1, and the notation card gains F3(2), S3/D4, and lambda rows. Raised by the user reading the figure cold.
