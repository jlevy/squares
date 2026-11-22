# Exact 228-square follow-up to issue #1038

Joost de Winter supplied a rational certificate and an algebraic certificate for
a refinement of the construction currently recorded as
[T-334](../../../frontier/RESULTS.md). His source credits the public layout to
jazivxt’s submission, Doğa Özden for the starting exact certificate, and the
refinement and algebraic reconstruction to Codex under de Winter’s direction.
The original finder and the connection to Nevska’s leaderboard entry remain
unresolved. [Submission](https://github.com/jlevy/squares/issues/1038#issuecomment-7046716722)

## Acquisition and credit

The attachment is 232,825 bytes with SHA-256
`5e0c62d9ad52b1afd78929e55e2fabf8d21f37fbe5f6e6c5a105f013ab970bd2`.
The inventory lists all 18 original members. The two new mathematical members
here decompress to their original Witness/v2 bytes. The original 76,003-byte
input matches the [retained T-334 source](../ozden-s228-upper-bound-2026-11-18/source/n228-witness.json.gz).
[Original attachment](https://github.com/user-attachments/files/35176109/squaremath_n228_exact_algebraic.zip),
[acquisition record](acquisition/source.json), [member inventory](acquisition/inventory.json)

The source archive carries [Apache 2.0](licenses/Apache-2.0.txt),
[CC BY 4.0](licenses/CC-BY-4.0.txt.gz), and
[Özden’s original notice](licenses/ozden-source-LICENSE.md.txt).
These notices apply according to their upstream terms. The new coordinates are
retained as submitted mathematical data under the
[retained factual data policy](../known-best-packings/README.md#retained-factual-data).
The original contributor programs and prose remain in the source archive.

## Sides and verification

The exact rational side is
`15.596043116631669919627353842076861324679045385375355711985032`.
It beats T-334 contracted to first contact by about `9.6587073354e-14`.
The algebraic side is smaller than the rational side by about `1.72780877985e-61`.
A separate scalar check established the stated root isolation and irreducibility,
with two wrong-bracket controls. The held local solver’s rational view is larger
than both submitted sides. Its exact-limit output lacks a valid local certificate.
[Exact side comparison](receipts/side-comparison.json)

Both maintained rational verifiers accepted all 25,878 pairs and rejected the
duplicate-square and outside-box controls. The three jobs across two routes
made 155,268 pair decisions in 89.43 seconds of worker wall time and 31.56
route CPU seconds. The maintained field verifier separately accepted all 25,878
pairs of the algebraic witness in 112.05 seconds of wall time and 57.68 CPU seconds.
The initial combined algebraic lane reached its 180-second wall limit during
the first negative control. Each resumed control finished under the same
per-job ceiling. The field verifier rejected the duplicate-square and
outside-box controls after 25,878 pair decisions each. The positive and two
completed controls took 365.26 summed job-wall seconds and 172.12 CPU seconds.
[Rational replay](receipts/native-rational.json.gz),
[algebraic replay](receipts/native-algebraic.json)

This packet records the candidate and replay results. Independent Stage 4 review
and the report-order decision remain on think-d4b0.

## Compressed Files

| File | Origin | Git blob of original bytes | SHA-256 of original bytes |
| --- | --- | --- | --- |
| `source/n228_rational.json.gz` | upstream | `5877bb01c1b32a5b0afb1ffa56f8ce7d0767c014` | `58465564994035e8e6c7f40c6651c0638f12e5e04546bd4b5225ced7808ba1bc` |
| `source/n228_algebraic.json.gz` | upstream | `5a38a5d48a43319544199051c6f74b159ff94d39` | `e32f6c3804e7bf61967a84e0b6ce520303e9b7c820b2431c342777bce7c8e1c9` |
| `receipts/native-rational.json.gz` | receipt | `e33444d317aa760ab7458a5a6c45f8d9aa8eb817` | `3b451cbfe8804a1de5dcf600af2502231abe867935a3720d93c83dc2356f0d69` |
| `licenses/CC-BY-4.0.txt.gz` | upstream | `da6ab6cc8f333d7e89a99812866df8f24374d47c` | `9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
