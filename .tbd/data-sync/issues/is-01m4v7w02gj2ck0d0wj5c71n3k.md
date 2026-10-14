---
type: is
id: is-01m4v7w02gj2ck0d0wj5c71n3k
title: Run check_vendored_evand --upstream in a networked gate when the vendored copy changes
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-13T18:19:49.710Z
updated_at: 2026-10-13T18:19:49.710Z
---
Review B on PR #509 (B1, Medium) found that the offline pin check for
`vendor/evand-regularize/` holds the copy to `vendored.yaml` but nothing holds
`vendored.yaml` to upstream, so a pull request that edits a vendored file and its
manifest line together passes every offline gate. The fix on #509 adds
`python -m devtools.check_vendored_evand --upstream`, which fetches
evand/square-packing at the manifest's `source_commit` (blobless, into a temporary
bare repository) and compares the commit's tree, date and subject, every pristine
file's Git blob id and mode, and the file set with upstream's tree.

`--upstream` needs the network, so no tier runs it: it is run by hand at a re-pin and
whenever `vendored.yaml` changes (vendor/evand-regularize/README.md, Checking the Copy).
The residual risk is that a reviewer forgets to run it.

Done when a gate that has the network runs `--upstream` on every pull request whose
diff touches `vendor/evand-regularize/vendored.yaml` or any vendored file, and fails
the pull request on a finding: for example a separate CI job with `contents: read`
selected by those paths, or a `packing-validate` step outside the PR surface selected
by `touches=("vendor/evand-regularize/*",)` and run where the network is available.
It must not join an offline tier (OR-13, OR-17), and it must stay a fetch of trees
only (about 1 s and 360 KB at the 675a5ea pin).

Files: packing/devtools/check_vendored_evand.py, packing/src/sqpack/cli/validate.py,
.github/workflows/, vendor/evand-regularize/README.md, development.md.
