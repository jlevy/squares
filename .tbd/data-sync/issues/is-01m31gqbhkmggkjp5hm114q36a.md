---
type: is
id: is-01m31gqbhkmggkjp5hm114q36a
title: corner_clip consumer justification fits two of its four consumers
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:18:37.746Z
updated_at: 2026-09-21T08:18:37.746Z
---
PR 206 re-review, new Low introduced by 9a19d393. The new section at corner_clip.py:66-93 justifies all four excludes consumers with one argument: 'drop what the predicate excludes, dropping only weakens the ceiling'. Two of the four do not drop. colgen.dual_support (colgen.py:716) and colgen.check_ceiling (:993-997) drop; ceiling._condition_corner_clip and independent_ceiling_reader.check_k4 refuse (holds=False). Those two are safe by the review's own strictness argument - K4 tests > d, stricter than the closed row domain - not by the dropping argument. Conclusion holds, stated reason is wrong for two of four.
