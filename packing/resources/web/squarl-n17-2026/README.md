# Squarl: an open `n = 17` search pipeline, retained 2026-09-08

[sam-bee/squarl](https://github.com/sam-bee/squarl) is Sam Burns's Go, CUDA and GoMLX
project for packing seventeen congruent squares. It is retained here because it is the
only public implementation of this problem that writes down every component the record
engines keep closed: the formulation, the move set, the two-tier local refinement, the
acceptance guard, and the final production run's own accounting.

It did not beat the record. That is part of why it is worth retaining: its closeout
document reports what a well-built 2026 pipeline achieved at `n = 17` and what it did
not.

## What is retained

All files were fetched on **2026-09-08** from `raw.githubusercontent.com` at commit
`016dff982938c69f0b7b2d63edd90d2e7e839dcc` on branch `master`, the tip at the time of
retrieval. The repository is MIT licensed, created 2026-07-25 and last pushed
2026-08-05.

| Local file | Upstream path | What it carries |
| --- | --- | --- |
| `squarl-README.md` | `README.md` | The formulation (unit container, `s = 1/7` initial states, reported width `1/s`), the move set in the author's own words, and the training loop |
| `squarl-LICENSE.txt` | `LICENSE` | MIT, 2026 Sam Burns |
| `squarl-docs-README.md` | `docs/README.md` | The documentation index |
| `squarl-docs-deep-polishing.md` | `docs/deep-polishing.md` | The deep-polish architecture: per-pair directed separating axis, the fixed-angle simplex LP over 34 centre coordinates and the width, angle tie-and-release, and the double-replay acceptance guard |
| `squarl-docs-final-search-closeout.md` | `docs/final-search-closeout.md` | The final non-learning production search: 32,390.38 seconds, 36 blocks of 40 proposals, 1,162 centre-LP candidates, 143 deep attempts, best strict `float64` width `4.675530095599908` |
| `squarl-docs-hard-topology-drain.md` | `docs/hard-topology-drain.md` | The earlier drain whose retained states did not match the published-record material basin |
| `squarl-docs-architecture.md` | `docs/architecture.md` | Component layout, the CUDA rollout path, and the archive |
| `squarl-docs-model.md` | `docs/model.md` | The graph-transformer policy and its action space |
| `squarl-docs-world-record-reference.md` | `docs/world-record-reference.md` | The published `n = 17` reference the project measures against |
| `squarl-repo-metadata.json` | GitHub API `/repos/sam-bee/squarl` | Licence, default branch, creation and push timestamps |
| `squarl-docs-listing.json` | GitHub API `/repos/sam-bee/squarl/contents/docs` | The full 23-file `docs/` listing, so the selection above is visibly a selection |

| File | SHA-256 |
| --- | --- |
| `squarl-README.md` | `be22bbdf750d26363536825d2691be5333f9f24166eeb55018a9a396e8fbb003` |
| `squarl-LICENSE.txt` | `588d56e87833df8dbe1f9491aab783ae8182f3558c1908cb015c8d35c766c3f3` |
| `squarl-docs-README.md` | `7233405e347395e74fce9c9a240cab2f389a1cc491b2638aa78a3fe44d4b86ee` |
| `squarl-docs-deep-polishing.md` | `7c3b217206d719d5ded0a1701ea93b36a3655231ee1f7d4290a89f84fc954ef2` |
| `squarl-docs-final-search-closeout.md` | `d69272a8bda11939dc8277804743dca4ebac760f1dffac34b5b31bf6bf737490` |
| `squarl-docs-hard-topology-drain.md` | `cb433388c1c207be609167ccdb9b54c6b73844e04ea4d2a0a1ab9854abde4ab7` |
| `squarl-docs-architecture.md` | `1dc51f24ebb5018a8038b3526375ca0efa4b3861973da64948158f99b97e93f7` |
| `squarl-docs-model.md` | `56304af62975acb4545838bff7f02a75c2c7dfd874dfd7be6ea70aeec79472ba` |
| `squarl-docs-world-record-reference.md` | `f1fc0db5b16e156732e289044192c83dbd660b72013000542cc39f897d31b225` |
| `squarl-repo-metadata.json` | `d5ee5d1d4d7940b20acbf3a6f30aedee5ea67e2c7438a0eed8792f59ea312a8a` |
| `squarl-docs-listing.json` | `c159519686b0561ad1daefd34e374bcd95916827df1bfb4eba53132973f46066` |

The Markdown files are the upstream bytes, renamed only so that a flat directory can
hold both `README.md` and `docs/README.md` beside this index. Nothing in them is edited.

## What was checked against these files

The claims the
[annealing research report](../../../../docs/project/research/research-2026-09-08-annealing-for-square-packing.md)
makes about Squarl were read from these bytes, not from the blog series:

- The tolerances in section 7's local-solver specification — `5e-5` ambiguity, `0.002`
  near-axis snap, `0.01` tie radius, 96 clustered and 32 released evaluations, the beam
  of at most two pairs and four states with one full alternative refinement — are
  `squarl-docs-deep-polishing.md` verbatim.
- The LP shape, 34 centre coordinates and the container width under 68 wall constraints
  and 136 directed pair constraints, is the same file.
- The acceptance guard, two deterministic replays agreeing within `5e-7` and passing
  independent wall and separating-axis verification within `2e-7`, is the same file.
- The production-run figures in section 2.3 are `squarl-docs-final-search-closeout.md`
  verbatim, including the `1.99535674836588872951685e-09` gap the document rounds to
  `2e-9` and the author's own conclusion that the reference was not beaten.
- The caveat that this was a warm search over a self-built archive rests on
  `squarl-docs-hard-topology-drain.md`, which says of an earlier drain that no retained
  state exactly matched the published-record material basin.

## What this is not

Nothing here has been replayed. These are the project's own documents reporting its own
results, retained as method provenance and as an independent arrival at an architecture
this repository reached separately in exp-006. The `n = 17` arrangement Squarl converged
on, and its coordinates, are retained separately under
[`burns-n17-series-addendum-2026-09-07`](../burns-n17-series-addendum-2026-09-07/README.md),
which this directory extends rather than replaces.

The repository's data directory, CUDA sources, trained weights and experiment outputs
are not retained. Only the documentation needed to check the report's claims is.
