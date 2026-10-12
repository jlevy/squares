---
type: is
id: is-01m4ed9phxjf6z6rf1284ex7r6
title: Simplify and format the PDF publication text
kind: task
status: closed
priority: 2
version: 5
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T18:44:33.980Z
updated_at: 2026-10-09T13:44:10.635Z
started_at: 2026-10-08T18:47:22.239Z
closed_at: 2026-10-09T13:44:10.635Z
close_reason: Implemented, independently reviewed and qualified for PR474 source 6ccbbf000f0c9b48f2985c07c9893f98fe73ba92 against main 6a0499ba4; combined tree c65da41410e89a8dedffe93d3c1e153adb05096d. Local named push 65/65 and hosted 93 fast + 13 actual deferred (106) plus Pages passed; final readiness receipts recorded.
resolution: null
duplicate_of: null
---
Use BEST KNOWN SQUARE PACKINGS as the PDF title, removing 324. Remove the entire corpus-details line: n=1 through 324, the square-bound row count, and total unit-square count. Format s(n) with italic s and n and upright parentheses, and put the algebraic-degree explanation on its own line. Preserve the triangle, packing cards, enlarged typography and clean upper-right alignment. Regenerate and visually verify the retained PDF.

## Notes

The title omits324; redundant range and aggregate lines removed; s(n) uses italic variables/upright parentheses, with deg explanation on its own line. Latest request shortens displayed bounds by one decimal digit for clear space before degree labels: PDF triangle upper and lower captions5decimals, website lower statements5decimals and gap captions2decimals. Display only, safe directional inequality rounding, recorded mathematical values unchanged.
