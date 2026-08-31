---
type: is
id: is-01m16npfryqwgbe00z84gz7g9t
title: Retrack the n=29 homotopy in higher precision to account for the lost paths
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-08-29T11:50:20.702Z
updated_at: 2026-08-29T11:50:20.702Z
---
agenda-006 BC-072, following BC-070. The double-precision run bounded the degree of s(29) at 15,744 by mixed volume, but its count was refused by BC-070's own kill condition: 148 of 15,744 paths ended in 'no solution', 600 solutions were reported singular, and only 8,327 reached the final list. Double-double path tracking targets exactly those failures. If it accounts for its paths, the number of distinct s values is the degree of the projection to the s-axis and turns BC-060's blind sweep into a targeted search; if it does not, the refusal is recorded again with a second precision behind it.
