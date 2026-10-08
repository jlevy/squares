# Assembly details

The current proof integrates the verified source snapshot from
EvolvingPrograms/11SquaresEvolving commit
`1bf942a7af1ea330e95489d8997deebd4227ca71` into the existing history of
11SquaresFormalized. See [the verification report](docs/VERIFICATION_20261006.md)
for the run, exact source hashes, trust model, and audit scope.

The two Lean source trees, root Lean modules, and three pinned build files
match the successful run byte-for-byte. The T03 tree and public optimality
statements match the previous Formalized main byte-for-byte. The old six-site
admission inventory is replaced by the verified zero-admission inventory.

The old top-level `MANIFEST.json` described the earlier partial assembly and
is preserved in Git history at `b237948fa44eb8876ed87eeb21329ab5577c833c`.
The current source-hash inventory is the `source_sha256` map in
[the compressed final audit](verification/completed-run-20261006/final-audit.json.gz).
Historical verification and simplification records retain their original scope.

Only portable source, documentation, and mathematical verification evidence are
published. Raw compiler logs, local paths, build caches, and private archives
remain outside the tracked tree.
