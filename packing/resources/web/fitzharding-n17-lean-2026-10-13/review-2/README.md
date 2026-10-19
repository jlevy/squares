# The Second Review’s Programs, 13 October 2026

These are the programs the
[mathematical-correctness review](../../../../../docs/project/reviews/review-2026-10-13-fitzharding-n17-mathematical-correctness.md)
of Fitzharding’s Lean proof wrote and ran on 13 October 2026, kept as they ran, with the
output each printed in [`outputs/`](outputs/).
The review was the second of this proof, by an AI agent, a Claude model at the
tbd-strong-max tier, reasoning max, prompted separately from the first review lane and
in a session of its own. It ran each program with the project interpreter (Python
3.14.7, `python3 -I`), reading a checkout of the pin and members of the release’s
`generated-sources.tar.gz` as data. No program imports or executes anything of the
source, and no Lean ran.

Nothing here was re-run when the folder was retained on 14 October 2026; the outputs are
the lane’s own. The review’s “Checks Run Here” section summarizes them, and its Steps 2
to 5 say what each establishes.

## What Its Authors Read

The lane read the whole hand-written Lean development before writing any of these
programs, the checker modules and their soundness proofs included (the review’s Scope
and Evidence). In a Lean proof the proof text and the producer’s checking code are one
body of source, so none of these programs is clean-room. The trace checker shares the
four producer definitions it transcribes into Python; the other programs share none
of the producer’s implementation.

The trace checker, [`hpfast.py`](programs/hpfast.py) with its drivers, is a transcription
into Python of the definitions of `HalfPlaneFast`, `CaptureRunFast`, `CaptureTableFast`
and `CaptureSummaryFast`, written from their Lean text with exact integers and fractions.
It evaluates the same definitions a second way, so it tests the compiled evaluator on the
facts it replays, which is the `native_decide` trust boundary, and not the definitions
themselves.

Both the source and this review were written with AI assistance from the same system
family: the source’s README says it was developed with Claude and Codex.

## The Programs

| Program | What it does | Reads | Output |
| --- | --- | --- | --- |
| [`endpoint_check.py`](programs/endpoint_check.py) | Solves the two endpoint polynomials by Newton’s method at 80 digits (mpmath) from a crude start, compares the root with the declared midpoint, computes the side and the margins of the two frames | `EndpointRootData.lean`, `HalfPlaneFrameBounds.lean` | [`endpoint_check.out`](outputs/endpoint_check.out) |
| [`census_check.py`](programs/census_check.py) | Rebuilds the D4 action on the 24 cells, counts the orbits of 7-subsets, and checks the 346,104 census rows, the representative tree, the 35 patterns, the 2,781 full rosters and the classifier that routes them, exactly | `CellPermutation.lean`, `ExactCellCoverData.lean`, `OrbitCensus/Chunk*.lean`, `RepresentativeCaseData.lean`, `RepresentativeCaseParts/*.lean`; from the archive `OrbitRepresentativeFiniteData.lean` | [`census_check.out`](outputs/census_check.out) |
| [`geometry_checks.py`](programs/geometry_checks.py) | The eight interior cells’ squared diameters, exactly; the cover of the box by the 24 cells at grid points, random points and every vertex; a random search for two separable squares in each wall-cell class | `ExactCellCoverData.lean`, `ExactWallCapacity.lean` | [`geometry_checks.out`](outputs/geometry_checks.out) |
| [`rigidity_dual_check.py`](programs/rigidity_dual_check.py) | Re-implements the affine weight check and the sparse residual check of the 93-box dual certificate with exact fractions, checks the box cover of the slider box for all 90 signed directions, and the final inequality at radius $10^{-7}$ | `LocalRigidityResidualMetadata.lean`, `LocalRigidityResidualSupport.lean`, `LocalRigidityWeightCoverData.lean`; from the archive `LocalRigidityMatrixData.lean`, `LocalRigidityWeightData.lean` | [`rigidity_dual_check.out`](outputs/rigidity_dual_check.out) |
| [`hpfast.py`](programs/hpfast.py) | The checker functions, lifted from `fast_replay.py` without its driver: integer half-planes, boxes, collision, walls, steps, decoders | (a module) | — |
| [`fast_replay.py`](programs/fast_replay.py) | Replays one branch-tree node: decodes its table, initial state and steps, runs every step and evaluates `excludes` | from the archive `HalfPlaneTrees/T1528/Node3.lean` and `Tree.lean`; `HalfPlaneTrees/T1528/Common.lean` | [`fast_replay_node3.out`](outputs/fast_replay_node3.out) |
| [`chunk_replay.py`](programs/chunk_replay.py) | Replays `runToCheck` on one chunk: every step, then exact equality of the result with the declared end state | from the archive `Neighbour329/Chunk{0000,0050,0107}Data.lean` and `CaptureOpen/Chunk{0000,0080,0164}Data.lean` | `chunk_replay_*.out`, six files; `chunk_replay_n329_0000.out` is `Neighbour329` chunk 0000 |
| [`table_check.py`](programs/table_check.py) | Replays `freshCheck 44`: the degree-44 Taylor checks of a chunk table’s fresh entries | from the archive `CaptureOpen/Chunk{0000,0080}Data.lean` with their `Checks` files | `table_check_capture_Chunk{0000,0080}.out` |
| [`summary_check.py`](programs/summary_check.py) | Replays `summaryCheck` on the terminal capture state against the 17 targets; `--perturb` lowers one target’s angle bound by $10^{-12}$ | from the archive `CaptureOpen/Chunk0164Data.lean`; `CaptureSummaryTargetsFast.lean` | [`summary_check.out`](outputs/summary_check.out): its first four lines are the run without `--perturb`, its last two the end of the run with it |

**Changed at retention.** Seven programs are byte-identical to the lane’s. Two carry one
change each, marked in the file, because the repository’s check that keeps JavaScript
out of Python strings (`devtools.check_no_embedded_js`, which admits no exception)
refuses the arrow `=>`, here Lean syntax and prose: in `census_check.py` the pattern
`\| (\d+) => \[` is written `\| (\d+) =[>] \[`, which matches the same text, and in
`geometry_checks.py` the printed `=>` is written `={chr(62)}`, which prints the same
characters. Both equivalences were tested apart from the programs, which were not
re-run. The lane’s copies as they ran have the SHA-256
`db93b922661015688928043f7d3bc148d87cf20a5d0d5fdff2745b307459d6ea` (`census_check.py`) and
`b3fb2580b417f6b55e826b8372d3e241185fc81b907cfe69c85865b087519a76` (`geometry_checks.py`).

`fast_replay_node3.out` ends “no bounds found in tree file for Node3”: the node’s table
check was not replayed, as the review says. `geometry_checks.py` seeds no random
generator, so a second run of its wall-class search prints other gaps.
Two of the review’s controls, one integer of `Neighbour329` chunk 0000’s declared end
state changed by one and one cut offset lowered by $10^{30}$ (its check 14), were run on
edited copies of that chunk file that the lane did not keep; they are reported in the
review and cannot be repeated from this folder. The summary control is
`summary_check.py --perturb`.

## What They Decide

Each program is in [`verifiers.yaml`](../../../../frontier/verifiers.yaml) with its
structured independence record, and each run that decides or samples something has an
evidence entry with its coverage.
n-017’s case record cites the entries; T-154 does not, since none of them is a complete
build of the proof (epistemics.md, Every Run’s Code Is Kept).

| Program | Registered as | Evidence | Coverage |
| --- | --- | --- | --- |
| `hpfast.py`, `fast_replay.py`, `chunk_replay.py`, `table_check.py`, `summary_check.py` | `V-sq17-review2-trace-checker` | `E-n017-fitzharding-native-facts-review2` | a sample, 10 of the 13,343 `native_decide` facts: one node of the three branch trees, 6 of the 273 chunk runs, 2 table checks and the capture summary over all $17 \times 1{,}024$ rows |
| `census_check.py` | `V-sq17-review2-census` | `E-n017-fitzharding-census-review2` | full: the census and the classifier |
| `geometry_checks.py` | `V-sq17-review2-cell-geometry` | `E-n017-fitzharding-cell-geometry-review2` | a sample: 8 of the 24 cells’ capacities decided exactly; the cover and the wall cells only sampled |
| `rigidity_dual_check.py` | `V-sq17-review2-rigidity-dual` | `E-n017-fitzharding-rigidity-dual-review2` | full: the 93 weight certificates over the 90 signed directions |
| `endpoint_check.py` | `V-sq17-review2-endpoint-frames` | `E-n017-fitzharding-endpoint-frames-review2` | full: the endpoint and the two frames, at 80 digits |

## Commands

From `packing/`, with `CLONE` a checkout of the pin and `X` the members of the release’s
`generated-sources.tar.gz` unpacked, the archive having the size and SHA-256
`manifest.json` gives (the packet’s README, The Release Archives):

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source fitzharding-n17-lean-2026-10-13 --checkout CLONE
P=resources/web/fitzharding-n17-lean-2026-10-13/review-2/programs
.venv/bin/python3 -I -B $P/endpoint_check.py CLONE
.venv/bin/python3 -I -B $P/census_check.py CLONE X
.venv/bin/python3 -I -B $P/geometry_checks.py CLONE
.venv/bin/python3 -I -B $P/rigidity_dual_check.py CLONE X
.venv/bin/python3 -I -B $P/fast_replay.py X/Sq17Lean/HalfPlaneTrees/T1528/Node3.lean \
  CLONE/Sq17Lean/HalfPlaneTrees/T1528/Common.lean X/Sq17Lean/HalfPlaneTrees/T1528/Tree.lean
for c in Neighbour329/Chunk0000 Neighbour329/Chunk0050 Neighbour329/Chunk0107 \
         CaptureOpen/Chunk0000 CaptureOpen/Chunk0080 CaptureOpen/Chunk0164; do
  .venv/bin/python3 -I -B $P/chunk_replay.py X/Sq17Lean/${c}Data.lean
done
for c in 0000 0080; do
  .venv/bin/python3 -I -B $P/table_check.py X/Sq17Lean/CaptureOpen/Chunk${c}Data.lean \
    X/Sq17Lean/CaptureOpen/Chunk${c}Checks.lean
done
.venv/bin/python3 -I -B $P/summary_check.py X/Sq17Lean/CaptureOpen/Chunk0164Data.lean \
  CLONE/Sq17Lean/CaptureSummaryTargetsFast.lean
.venv/bin/python3 -I -B $P/summary_check.py X/Sq17Lean/CaptureOpen/Chunk0164Data.lean \
  CLONE/Sq17Lean/CaptureSummaryTargetsFast.lean --perturb
```

The chunk replays took 69 to 141 seconds each on the lane’s host; the rest take seconds.
The lane ran them on copies of the source files passed as arguments; the paths above
are written for a checkout and the unpacked archive.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
