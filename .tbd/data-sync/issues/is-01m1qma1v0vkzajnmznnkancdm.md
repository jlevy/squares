---
type: is
id: is-01m1qma1v0vkzajnmznnkancdm
title: "n = 21: DS7's 4.7438 exceeds the closed form the register calls the prior bound; T-020's novelty sentences overstate"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-05T01:53:09.983Z
updated_at: 2026-09-05T01:53:09.983Z
---
Found by the n = 19-21 audit port (think-01j2). Friedman's DS7 table (packing/resources/papers/friedman-ds7-packing-unit-squares-in-squares.md lines 394-395) lists s(19), s(20) >= 6*sqrt(2) - 4 ~ 4.4852 (Figure 34) and s(21) ~ 4.7438 (a four-decimal entry with no exact form, figure, derivation or citation), dated no earlier than the July 2000 edition. For n = 21 that 4.7438 exceeds Nagamochi's 1 + sqrt(14) = 4.741657, which the register carried as the prior bound; T-020's 24/5 still exceeds both (by 0.0562 over DS7). Two things follow. (a) results.yaml T-020 says (line ~895) 'the first lower bound of any kind proved about twenty or twenty-one squares in particular rather than read off a formula' and (line ~921) 'no bound specific to either size had ever been proved' -- both overstated; scope them to the located record as T-018's and T-017's sentences were. (b) Decide the register's prior value for n = 21: whether a bare table entry without derivation qualifies as a reported bound under epistemics.md's V rungs (and then n-021.md's front matter, the 'was' column and the +0.058343 movement figure change to DS7's value and +0.0562), or record explicitly why it does not. Re-derive every figure.
