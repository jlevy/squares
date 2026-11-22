# Row 3 Scalar Audit: Original and Reading Copy

This audit was performed after the independent finite-feasibility result froze.
It supplies historical scalar comparisons and artifact-availability observations; it
does not alter or enlarge the original feasibility verdict.

[compare_row3.py.txt](compare_row3.py.txt) is the exact program that produced
[held-row3-comparison.raw.json](receipts/held-row3-comparison.raw.json), retained
without edits.
The raw audit keeps the historical absolute paths and binds the program by
SHA-256. It used CPython 3.14.7 and one worker under an observe-only memory guard.
The original execution and observer logs remain at
`/Volumes/spud-ext2/agent-scratch/n90-row3-followup-20261121/`.

[held-row3-comparison.json](receipts/held-row3-comparison.json) is an integration
reading copy. Exactly nine input or missing-artifact path values were replaced by
repository-relative paths.
No numerical value, source digest, verdict, chronology, program identity or limitation
changed.
The [provenance receipt](receipts/row3-audit-provenance.json) lists each old and
new path, both audit digests and the program digest, and records an exact recursive
comparison of all other fields.

The exact new candidate is about 9.99404 × 10⁻²⁰ below row 3’s rational envelope and
rounds to its 65-significant-digit local-side display.
That display is not a certified root interval.
Missing solved coordinates prevent pose comparison and an Option-D comparison against
row 3 itself. Both rational sides beat T-304 contracted to its first contact.
Credit remains jazivxt, improved and refined by Joost de Winter; the earlier project run
using Evan Daniel’s regularizer supplies the prior computational context.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
