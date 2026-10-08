# Tests

`cargo test --release` runs the following, without Python:

- the geometry and sweep helpers on exact inputs;
- the sweep against an exact area-subtraction reference on random rational polygons;
- the hidden lens of the review’s `hidden-lens` mutation on a small domain: with gap 0
  the pieces cover the domain and the sweep accepts, and with gaps 2^-40 and 1/1000 the
  sweep reports an uncovered abscissa inside the sliver;
- facets against the hull of vertex differences;
- the 256-bit product comparison;
- canonical JSON and float `repr` tables taken from CPython 3.14;
- the `random.Random(seed).sample` table;
- the receipts of the fixtures in `tests/data/` at 1, 2 and 4 threads, against the
  standing verifier’s results:
  - `closed`, `stall`, `dead` and the stalled W7 certificate;
  - the three `owned_hulls_intersect` fixtures:
    - `ohi` passes with that closure kind and the oracle’s counts;
    - `ohi-wrong-kind` is refused with
      `step 0: the derived closure is not the declared one`;
    - `ohi-point-outside` is refused with `no closure derived`.

The stalled W7 certificate is read from
`packing/campaign/explorations/X048-session-168-pilots/audit-verifier-rewrites/fixture-w7-bins8/`.

The fixtures and their expected results were produced by Python scripts that run the
standing verifier as the oracle.
Those scripts are kept outside this repository, pinned at
[wand125/square-packing@`630cdc472`, `tools/n17_kernel_verifier/tests/`](https://github.com/wand125/square-packing/tree/630cdc47209545e4aa8455223651b19379519e53/tools/n17_kernel_verifier/tests):

| script | what it checks |
| --- | --- |
| `make_fixtures.py` | the tiny closed, stalled, sampled and dead-row fixtures and their oracle results |
| `make_fixture_ohi.py` | a fixture closed by `owned_hulls_intersect` (no recorded certificate closes this way) and two controls: a wrong declared kind, and the point moved out of the hull |
| `differential.py` | 185 mutations of the fixtures at 1 and 4 threads, many of them expected to stay valid. For a PASS: status, counts, content ids and closure equal to the oracle’s. For a refused, well-formed certificate: the exact failure text. For malformed input: only the `malformed certificate:` prefix |
| `cli_check.py` | receipt bytes equal to Python’s `json.dumps(indent=1)`, exit codes, progress lines, the embedded cover |
| `make_compatibility_data.py` | the CPython float `repr`, sampling and Unicode tables |

Failure text is therefore compared exactly only for refusals of well-formed
certificates. Malformed input (missing members, JSON or I/O errors) is refused by both
verifiers, but in each implementation’s own words.
For example, a missing `schema` gives `malformed certificate: missing member schema`
here and `KeyError('schema')` in Python.

## The review’s mutation registry

The 2026-10-03 verifier review (lane R6, `audit-verifier-rewrites/mutate_cert.py.txt`)
has 34 named cases. They were applied to the stalled W7 certificate with a local loader
and saver (canonical JSON, gzip, SHA-256 names) in place of the generator’s. Both
verifiers were run on the same 34 directories.

The 33 mutations are refused by both, at the expected check where the registry names
one, with identical failure text (compared to the 160 characters the review’s record
keeps).

`hidden-lens-0-control` is a positive control, not a mutation.
Its pieces cover the row’s required domain exactly, so the row must pass its coverage
check. It does, in both verifiers:

- All steps are accepted, including the full coverage check of the modified row.
- The node is then refused at the final state (`final residual 18`). The mutation
  replaces that row’s residuals, and the final state still records the old ones.

The paired `hidden-lens-2^-40` fails the coverage check itself
(`required domain NOT covered`). The unit test above checks the same boundary directly.

The verifiers accept the unmutated certificate as a valid stall (`verify_objects`
returns without a failure).

| case | kind | expected check | both verifiers’ outcome |
| --- | --- | --- | --- |
| `region-vertex-pushed-2^-40` | mutation | `escapes the collision set` | refused: `step 13 row 7 partner 10: region escapes the collision set` |
| `region-vertex-pushed-2^-80` | mutation | `escapes the collision set` | refused: `step 13 row 7 partner 10: region escapes the collision set` |
| `region-vertex-pushed-later-row-only-2^-40` | mutation | `escapes the collision set` | refused: `step 13 row 7 partner 10: region escapes the collision set` |
| `region-outside-required-domain` | mutation | `escapes the required domain` | refused: `step 13 row 7: collision region escapes the required domain` |
| `region-names-owner` | mutation | `collision partner` | refused: `step 13 row 7: collision partner 18` |
| `region-names-unadmitted-partner` | mutation | `collision partner` | refused: `step 13 row 1: collision partner 10` |
| `cover-domain-shrunk` | mutation | `domain` | refused: `step 13 partner 0 row 0 domain` |
| `cover-domain-grown` | mutation | `domain` | refused: `step 13 partner 0 row 0 domain` |
| `cover-live-row-declared-empty` | mutation | `domain` | refused: `step 13 partner 0 row 0 domain` |
| `cover-all-rows-declared-empty` | mutation | `domain` | refused: `step 13 partner 0 row 0 domain` |
| `cover-core-scaled-1.02` | mutation | `core not strict` | refused: `step 13 partner 0 core not strict` |
| `cover-core-scaled-1+2^-20` | mutation | `core not strict` | refused: `step 13 partner 0 core not strict` |
| `cover-memo-same-domain-wider-core` | mutation | `core not strict` | refused: `step 1 partner 10 core not strict` |
| `cover-memo-same-core-grown-domain` | mutation | `domain` | refused: `step 1 partner 10 row 0 domain` |
| `cover-stale-after-partner-stepped` | mutation | `partner` | refused: `step 4: partner 10 reference` |
| `cover-stale-relabelled-after-partner-stepped` | mutation | `domain` | refused: `step 4 partner 10 row 0 domain` |
| `residual-dropped-planes-recomputed` | mutation | `NOT covered` | refused: `step 13 row 7: required domain NOT covered (uncovered at x=292/129)` |
| `residual-dropped-planes-kept` | mutation | `common-core planes` | refused: `step 13 row 7: common-core planes` |
| `residual-shrunk-1-2^-40` | mutation | `NOT covered` | refused: `step 13 row 7: required domain NOT covered (uncovered at x=21362941/9438352)` |
| `residual-shrunk-1-2^-70` | mutation | `NOT covered` | refused: `step 13 row 7: required domain NOT covered (uncovered at x=107355294864/47430597781)` |
| `residual-corner-cut-2^-40` | mutation | `NOT covered` | refused: `step 13 row 7: required domain NOT covered (uncovered at x=19795329/8745766)` |
| `residual-vertical-edge-moved-2^-50` | mutation | `NOT covered` | refused: `step 13 row 7: required domain NOT covered (uncovered at x=143/100)` |
| `collision-region-shrunk-1-2^-40` | mutation | `NOT covered` | refused: `step 13 row 7: required domain NOT covered (uncovered at x=14175698329/9913073639)` |
| `hidden-lens-2^-40` | mutation | `NOT covered` | refused: `step 13 row 7: required domain NOT covered (uncovered at x=253059607/146052101)` |
| `hidden-lens-0-control` | positive control | — | refused: `final residual 18` |
| `kernel-point-pushed-2^-40` | mutation | `kernel point fails a plane` | refused: `step 5: kernel point fails a plane` |
| `retained-vertex-moved-one-grid-unit` | mutation | `witness point` | refused: `step 0: witness point` |
| `retained-extra-point-copied-witness` | mutation | `witness point` | refused: `step 0: witness point` |
| `prior-hull-grown` | mutation | `prior hull` | refused: `step 0: prior hull 0` |
| `row-missing` | mutation | — | refused: `step 13: the rows do not reach the end of the interval` |
| `false-closure` | mutation | `no closure derived` | refused: `no closure derived` |
| `seed-row-vertex-dropped` | mutation | `seed row` | refused: `seed row 0/0 domain` |
| `seed-unowned-point` | mutation | `not owned` | refused: `seed point (Fraction(2, 1), Fraction(2, 1)) of 0 not owned` |
| `owner-core-scaled-1+2^-20` | mutation | `core not strict` | refused: `step 13 row 7: core not strict` |

## Certificates from the standard procedure

Seven certificates were produced with the standard procedure at `4148483da`. BC-428 used
`--bins 64 --max-rounds 24 --hull-limit 16 --producer-share 0.6 --split-floor 512 --max-rows
1152 --split-patience 1`. The W7 variants used bins 16, 32 and 64. Each was verified by
the standing verifier at that revision (receipt `provenance.files` blob
`1ad706c21d04cc4a052af8a942c848cbca59fd76`) and by this crate.
The cover is the embedded `cells/cover.json` (SHA-256
`40a2f1f22b1de285f5c21fb66f20eda6b51c3446a98090bcaec8a6772c585e3c`), reported as design
`ring-3-voronoi-8-tabbed-unique`.

| certificate | outcome | seed SHA-256 | node SHA-256 |
| --- | --- | --- | --- |
| W7, bins 16, octagon core | FAIL, stall | `592ebdd6dbeb3312fdc09e400bf67e15d55457a6f209302a9a492b98ccd0dacd` | `616a4c916200544a1bdc39fd308fd07a6c44a3ef089759149bcc801c5797ef1f` |
| W7, bins 32, octagon core | FAIL, stall | `934332aeaeb5a77a64b6fc83c5f6088d81fd5eb8e706760109e8d3b75416e9d7` | `cd24f2cd012b800c166db483df9c05a0944960584ef03fefb22e154d50929a62` |
| W7, bins 64 | PASS, `all_parent_poses_forbidden` (owner 5, step 57) | `8949a798f00bb376d9520fda8eb71146973905c75977173bede6aa81e0500782` | `2d516d00ab3bd989ab1d90e531c626589d819ab3753bff6ed83221590b4523ca` |
| W7, bins 64, split floor 128 | PASS, `all_parent_poses_forbidden` (owner 5, step 57) | `8949a798f00bb376d9520fda8eb71146973905c75977173bede6aa81e0500782` | `3a8cf3698ebe48a66c38fe90e1a09f270aed7d9087da6dbfb326853b6e3af7f3` |
| BC-428 u3 | PASS, `all_parent_poses_forbidden` (owner 10, step 94) | `166e71d8fc8f5db8f4c4745a7b1a7968cbd09698b90e7070854873b74938eaae` | `08c0e1c7314d36f2f94e15d984c169e6b7dd9168b80b5d6f88966978f32cb377` |
| BC-428 u4 | PASS, `all_parent_poses_forbidden` (owner 19, step 48) | `a845f83e4baee67ccaaeb0bac62a8dc9b7320fb10757fdfd9b7a9dd3407ad6d2` | `52b5ba27b3ecc01ff43167e2b2bed30b087ce5eb70d80dee71f6ea3f5c197a05` |
| BC-428 u6 | FAIL, stall | `71cbdb6e851c40c6eef040893aba723de7537b3be0d8cae433cc1852683a8a46` | `d6651f5a5ff6dc124cd0cda41283b93deff79d94f2b8541bb7e77451da678612` |

Runs whose receipts agree with the standing verifier’s on every field except
`provenance`, `directory` and `seconds`:

| build of this crate (`provenance.source_sha256`) | threads | machine |
| --- | --- | --- |
| `71e7bb956c29e4bd8c00560e8b59bf71eb24c05972b0819abe0ca8d99d332e1d`, a revision before this PR’s first commit | 1 and 16 | Linux, 16 vCPU; the timings in README.md |
| `4ac56281192febb95cf4268c4ea51672d168bceeb3435c234c04b8a3b14b277b`, contributor’s pre-integration `763ecd3ba` build | 1 and 8 | macOS, 14-core arm64 |

The certificates (215 MB) and all receipts (the standing verifier’s and this crate’s)
are kept by the contributor and can be supplied on request.
They are not published, so the seven-case agreement is contributor-reported until it is
replayed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
