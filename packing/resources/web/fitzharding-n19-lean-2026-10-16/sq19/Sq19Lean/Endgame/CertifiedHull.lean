import CertifiedHull

/-!
# Certified local hull lower bound

Stable project import for the complete 2304-check certificate assembly.
Exports `Sq19.Endgame.Reduction.side19_le_of_hull`: every `Good Hull.prob`
configuration has side at least `3 + 4 * Real.sqrt 2 / 3`.

The generated modules retain their original names and live under
`s19/certificates/endgame_reduction/`; Lake registers both source directories.
There is no remaining numerical acceptance hypothesis. This is a local theorem;
global optimality additionally needs the census and capture-to-hull arguments.
-/
