# Eleven squares: owners, support chains, and angle penalties

[Read the manuscript source](eleven-squares-synthesis.tex) and
[download the self-contained verification supplement](eleven-squares-publication.zip).
The manuscript is a standalone LaTeX document with its figures and bibliography
included. Compile it with a standard LaTeX installation.

The argument combines a marker-based global reduction with a support-chain
inequality that allows the tilted squares to rotate independently. An early
corridor, a virtual bottom row and a virtual right column replace several
spatial exclusion chains. The surviving ownership case now has a 103-node
dependency graph, down from 119. The selected five-prefix ending is retained.

The exclusions of ownership cases 0, 3, and 5 have also been simplified.
Case 0 ends with an elementary three-point height bound and a blocking
segment; the ownership facts feeding that argument retain their existing
computational ancestry. Case 3 uses 12 point assertions instead of 62,
including a direct geometric proof of a point forced by the bottom wall.
Case 5 uses 65 assertions instead of 170. Its computational checking changes
little despite the smaller table. Cases 1, 2, and 4 retain their previous
exclusions.

Quantitative nonoverlap penalties control angle disagreement, replacing the
late fine capture and branched local-isolation endpoint. The manuscript writes
out the corridor and support arguments, the wider-strip lemma, and the
boundary-preservation obligations. A short companion,
[Geometric foundations](eleven-squares-geometric-foundations.tex), gives direct
proofs of the rectangle, triangle, wall and ownership rules and identifies
their precise relationship to the cited results.

## Verification

Extract the supplement, enter its top-level directory, and run:

```sh
python3 verify.py --check-inputs
python3 verify.py --quick --jobs 2
python3 verify.py --ownership --jobs 2
python3 verify.py --early
python3 verify.py --full --jobs 2
```

The checkers were tested with CPython 3.12.4 and use its standard library.
The supplement includes the required source and certificate inputs; verification
does not require the repository's large Git LFS dataset, a solver, Lean, or a
network connection. Full replay can take substantial time.

The new ownership arguments, early components, and 103-node dependency
assembly were checked during preparation. Input verification, all 13 quick
checks, the ownership replay, and the early component replay passed in a clean
extraction of this archive. The portable full command has not yet been
executed end to end. The `--ownership` command freshly checks the smaller
case-3 and case-5 tables from the initial compulsory regions, and checks the
case-0 terminal bridge under its stated ancestry premises. The latter still
require the full runner. The `--early` command freshly
checks the new components under their stated parent inputs; its result is
conditional until those parents have been
freshly established. Neither `--early` nor `--quick` proves the complete global
argument by itself.

For a complete portable replay, `--full` first runs the existing 61-stage
verifier, then the new ownership checks, revised components, and the 103-node assembly. This
transitional runner performs some redundant checks from the earlier route.
The number of executed stages is therefore different from the number of
dependencies in the shortened mathematical proof. The supplement's entry-point
documentation describes the commands and their completion conditions.

The proof combines displayed mathematical lemmas with exact-rational Python
checks. It is not a new Lean formalization or an independently refereed result.

The publication supplement contains mathematical inputs and verification code.
Optional completed-run logs and local execution records are omitted. Required
reference certificates remain inputs whose premises the verifier must check.
Inherited source notes describe their own historical stages; the manuscript and
the supplement's entry-point documentation state the scope of this proof.

## Sources

The global marker framework, strip supports, compulsory-hull propagation, and
selected pose-cover certificates come from the anonymously supplied geometric
proof and certificate archive cited in the manuscript. The original proof in
this repository informed the certificate organization and residual estimates.
Common-cone compression already appears in
the related `11SquaresFormalized` development. The principal new endpoint is the
independent-angle mixed-support comparison. The revised proof also adds the
early corridor, scalar row argument, first-round column argument and their
shorter dependency assembly. The latest ownership revision adds the
three-point height and segment-trap arguments, the floor-forced point lemma,
and the smaller case-3 and case-5 tables. No claim of literature novelty is
made for these elementary arguments. The attaining packing is Trump's pre-existing
construction. Full references and attribution appear in the paper.

The repository's earlier [PROOF.md](../PROOF.md) and verification route remain
available separately. They use a different global case reduction.
