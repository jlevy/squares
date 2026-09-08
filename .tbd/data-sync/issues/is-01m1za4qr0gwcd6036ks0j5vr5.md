---
type: is
id: is-01m1za4qr0gwcd6036ks0j5vr5
title: Refuse stale exact verified bounds in case prose
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
created_at: 2026-09-08T01:29:25.502Z
updated_at: 2026-09-08T09:02:20.098Z
closed_at: 2026-09-08T09:02:20.097Z
close_reason: |
  Completed in merged PR120 after integrating origin/main through 2980c5bc and independently reviewing compatibility with PR116 and PR121. The Stromquist n26 audit, 56 DS7 reported-bound corrections and D-483 exact-fraction prose checks are committed. Friedman remains best found among the dated public sources; verified and upper bounds are unchanged. Final source c610b481 has passing affected validation and required hosted checks. The complete 318-record translation screen replay passed, with all six declared exclusions retained; historical full-checkpoint timeout remains accurately recorded alongside successful replay evidence. Private-communication attribution, MacIver review, cumulative session costs and unresolved research follow-ups are retained.
resolution: null
duplicate_of: null
---
The n20 and n21 case bodies still call 24/5 = 4.8 the current verified lower bound under frontmatter 97/20 = 4.85. The prose checker discards the exact fraction and accepts the truncated decimal; its named-field matcher misses the s(n) anchor. Preserve exact identities for explicitly named verified fields, keep directional rounding for displays, recognize the new independently-verified generator wording, and repair the case descriptions without changing any verified bound.
