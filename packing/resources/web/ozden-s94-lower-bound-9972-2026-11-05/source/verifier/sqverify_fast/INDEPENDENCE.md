# Independence Record for sqverify-fast

This is the clean-room record that lets this crate count as an independent
implementation of the measure-capture verifier: every file read, every command run, and
every outside reference consulted while writing it, kept as the work went.
The bead is `think-gpe0` (lane W2), with milestones `think-d69e` (soundness and
Milestone A), `think-tgra` (performance loop) and `think-4vf7` (points and segments).

## The Rule

Never opened, grepped, diffed or copied: any `verify*.cpp`, `mixed_rotated_verify.cpp`,
`unified_linear_verify.cpp`, `zmx2.rs`, `zm_mixed.py`, `zeromargin.py`, `qx2_zm.py`, any
`code/` directory under `packing/resources/web/`, and the checker-driving internals of
`packing/devtools/audit_wand125_*.py` and `replay_evand_zmx2.py`. The authors’ checkers
were run only as black boxes, for timing, through the repository’s replay command.

## Files Read

Repository instructions and conventions:

- `AGENTS.md`, `operating-rules.md`, `development.md` (supported environment, tiers,
  performance work), and the `experiment-loop` skill with its `contract.md` and asset
  headers.

Mathematics (reviews under `docs/project/reviews/`):

- `review-2026-09-27-wand125-rectangle-scaling.md`, in full.
  Its sections on fixed-width types, floating-point constants and hard limits describe
  `verify.cpp`’s constants, limits and some line numbers in prose; they were read before
  that was apparent. Nothing in this crate uses them: its arithmetic (directed rounding
  per operation, rational enclosure by exact comparison), its bounds (concave-section
  trapezoids, edge-length enclosures from nine affine terms, classification with slack)
  and its limits are its own, derived in `SOUNDNESS.md`.
- `review-2026-09-22-tokoharu-density-mathematics.md`, lines 1–200 and 225–318 as
  displayed: the mathematical reduction, the net and shrink argument, the quarter-turn
  reduction, the axis-grid argument, the derivative formula and mean-value bound,
  optional smoothing and the preconditions, and also “Scope and Evidence” and “Exact
  Preconditions and Replay Results”.
  The section “Inscribed-polygon area and arithmetic” (lines 195–224), which describes
  the checker’s area routine, was meant to be skipped, but the read of lines 1–200
  displayed its first six lines.
- For Milestone B, the section headings of
  `review-2026-10-02-wand125-linear-certificates-and-n76.md` and
  `review-2026-10-02-wand125-mixed-rectangle-bounds.md`, then lines 86–161 of the first
  (“The Argument From a Linear Measure to the Bound”) and lines 1–126 of the second (its
  opening, scope and verdict, and “The Argument From Certificate to Bound”): the
  formats, the atom bounds and the per-bin domain, which spec §1.4–§1.6 restates.
  Lines 86–161 name functions of the authors’ Python driver (`unified_measure.py`) in
  prose; nothing here uses them.
  Lines 162–290 of the linear review (“The Checker, Function by Function”), which the
  testing review says paraphrase a checker routine line by line, were not displayed.
- For the Milestone C plan, §§3–4 (lines 86–233) of
  `review-2026-10-02-wand125-s59-s77-mixed-covers.md`, at the coordinator’s direction:
  the statement, the measure’s closed conventions, the scaling reduction, the pose space
  and its $D_4$ fold, and §4’s account of what the authors’ continuous-angle checker
  decides and assumes, which names its lemmas, limits and two function names but quotes
  no code. The specification’s §1.7 (the same lemmas) was read from the copy checked out
  earlier.

Lane W1’s clean outputs, checked out from its branch `worktree-agent-a9b6885d64664dd01`
at the coordinator’s instruction (these two files only; the research note, the
`attribution/` folder and the profiling script on that branch were never opened):

- `docs/project/specs/active/plan-2026-10-02-independent-measure-verifier.md`, the
  specification.
- `packing/benchmarks/results/author-checker-profile-2026-10-02/timings.json`, the
  authors’ checkers’ black-box CPU timings.

First-party code of this repository:

- `packing/src/sqpack/rectangle_density.py`, in full: the candidate format
  (`[left, bottom, right, top]`, decimal tokens as exact rationals, `rhs`, `certificate`
  metadata), the D4 images, and the exact oracle used by the differential tests.
- `packing/sqverify_exact/Cargo.toml`, `rust-toolchain.toml`, `clippy.toml` (the
  toolchain pin and lint floor were copied), and the step functions `_rust_quality` and
  `_rust_exact_geometry` and the step registry of `packing/src/sqpack/cli/validate.py`,
  with the cache steps of `.github/workflows/packing-validation.yml`, to wire this crate
  the same way.
- `packing/benchmarks/bench_rectangle_rust_verifier_ab.py` (header only) and
  `packing/benchmarks/math-startup/` (README, ledger head, one hypothesis) for this
  repository’s benchmark conventions.

Certificate data and summaries (packets under `packing/resources/web/`):

- `wand125-rectangle-certificates-2026-09-27/README.md` (lines 1–150) and
  `wand125-rectangle-certificates-2026-10-01/README.md` (lines 1–80).
- `certified_candidate.json.gz`, `certificate_metadata.json`,
  `verification_summary.json` and `verified_angles.jsonl` of `rect_n32_L595` and
  `rect_n78_L8955`, and the candidate files of every certificate verified in Milestone
  A.
- `receipts/replay/audit.json` of the 27 and 28 September packets (case list, status,
  counts and timings only) and `receipts/controls/rect_n41_L676.json` of the 1 October
  packet (mutation descriptions and witness).
- For Milestone B, in the packets `wand125-point-and-mixed-2026-10-01`,
  `wand125-mixed-bounds-2026-10-02`, `wand125-mixed-bounds-n76-2026-10-02` and
  `wand125-linear-certificates-2026-10-02`: the `candidate.json.gz` of every `mixed_n*`
  certificate (top-level keys, rows and masses), and under `receipts/` the
  `merged.json`, `summary.json` and `directions.jsonl` of each replayed range (status,
  index, nodes, CPU and wall seconds, load) and the `control.json` of n37 and n101
  (mutation descriptions, witness centre and exact coverage, the checker’s verdicts).
  The `code/` folder beside `mixed_n101_L1028` was listed by `ls` and never opened.

The two adversarial reviews of this crate, merged at the coordinator’s direction: the
soundness review (`review-2026-10-03-sqverify-fast-soundness.md`) in full, and the
testing and independence review
(`review-2026-10-03-sqverify-fast-testing-and-independence.md`) except lines 201–242
(“What the code shows”), which compares this crate with the authors’ checkers and was
skipped for that reason.

## Departures From the Specification’s Protocol

The specification (§2.2–§2.4, version `6c5ff1430`) allows only listed review sections
and forbids replay receipts.
This lane departed from it in four ways, each disclosed when it happened or found:

1. **A review read in full.** `review-2026-09-27-wand125-rectangle-scaling.md` was read
   whole, before the allowance was known; §2.2 allows only “The Net and the Box Argument
   at Side 9” and “The Monotone Transfers”.
   Its sections on fixed-width types, floating-point constants and hard limits describe
   `verify.cpp`’s constants; nothing here uses them.
2. **Review sections beyond the allowance.** In the Tokoharu review, “Scope and
   Evidence”, “Exact Preconditions and Replay Results” and six lines of the area
   routine’s section; in the mixed rectangle review, its opening, scope and verdict; in
   the s(59) and s(77) review, §4 (the coordinator’s direction, for the Milestone C
   plan).
3. **Replay receipts read.** §2.3 forbids `packing/resources/web/**/receipts/`. This
   lane read the summary fields of the replay audits (`audit.json`, `audit.json.gz`,
   `mixed-audit.json`, `exact-audit.json`), of the replay ranges (`merged.json`,
   `summary.json`, `directions.jsonl`), of the controls (`control.json`,
   `rect_n41_L676.json`) and of the n50 replay (`compare.json`, `inputs.json`):
   statuses, counts, timings, witnesses and mutation descriptions, for the census and
   the controls, which need them.
   These hold the checkers’ verdicts and numbers, not code; no log under `receipts/` was
   opened.
4. **No machine-readable record until now.** `independence-record.yaml` beside this file
   is the §2.4 record, written by hand from this lane’s transcript; the audit tool that
   §2.4 asks for (slice 4) has not run over it.

## Commands Run

- `python -m devtools.check_bootstrap`, `git submodule update --init --recursive`,
  `npm ci --ignore-scripts`, `uv sync --frozen --all-extras --group dev` (fresh-clone
  setup).
- `python -m devtools.audit_wand125_rectangles --help` (the command-line help text only,
  to learn the replay command’s options).
- `python -m devtools.audit_wand125_rectangles --packet 2026-09-27 --control --n 32
  --direction 1 --out …` and, through `benchmarks/bench_measure_verifier.py`, the same
  command for other certificates and directions: black-box timing of the unchanged
  `verify.cpp`. The tool’s receipts were read for CPU seconds, node counts and verdicts.
- `python -m devtools.audit_wand125_rectangles --packet 2026-09-27 --n 32 --replay
  --workers 1 --out …`, through the harness’s `--whole` mode: a black-box replay of
  every direction of one certificate, for whole-certificate CPU. Only the tool’s
  receipts (status, per-direction rows) were read; the process list showed the checker
  binary’s name and arguments (`./verify R R`), nothing of its source.
- `cargo build`, `cargo test`, `cargo clippy`, `valgrind --tool=callgrind` and
  `callgrind_annotate` on this crate only.
- `packing-validate --edit` and `--only` on this worktree.
- For the census of every retained certificate: a merge of the updated base branch
  (which brought the afternoon packets of 2 October), the `receipts/` summaries of every
  wand125 rectangle and mixed packet (`audit.json`, `audit.json.gz`, `mixed-audit.json`,
  `linear-audit.json`, `exact-audit.json`, `fetch.json`, and the n50 replay’s
  `compare.json` and `inputs.json`) for replay status only, and the census tool over
  every `certified_candidate.json.gz` and `candidate.json.gz` there.
  `ls` listed the `code/` folders beside some certificates; none was opened.
- For the soundness review’s findings: a merge of
  `origin/claude/review-ra-sqverify-fast` (`0e38246a9`), which added
  `docs/project/reviews/review-2026-10-03-sqverify-fast-soundness.md` and
  `tests/adversarial.rs`; both were read in full.
  The reviewer read this crate and the specification, not the authors’ checkers, so
  neither brings anything of theirs.
- For Milestone B: `sqverify-fast` on the mixed and linear candidates and on their
  mutations; `python -m devtools.check_sqverify_fast --only mixed` and
  `python -m devtools.sqverify_fast_census --family mixed`; a throwaway build of this
  crate using Tokoharu’s domain for format M and a dense NumPy evaluation of every axis
  vertex of `mixed_n76_L894`, to check the axis minimum independently (both agree with
  the sweep: 1.0075338896, below the authors’ recorded `integer_minimum` of 1.0075130,
  so that figure is their conservative bound, not the minimum); the dense evaluation is
  now `axis_minimum_dense` in `devtools/check_sqverify_fast.py`.

The census reads, from the replay receipts, only the authors’ summary fields (status,
node total, least printed bound, wall seconds and the worker count in the recorded
command; for formats M and L, each replayed direction’s index, status, nodes and CPU
seconds), to set them beside this verifier’s results.

## Outside References

None beyond the reviews above: the IEEE 754 round-to-nearest model, the Brunn–Minkowski
concavity of sections of convex sets, and Fubini’s theorem are standard.
Lemma I1’s branch-free step is the textbook bound that no gap between adjacent binary64
values exceeds $2^{-52}|x|$, applied directly; no source was consulted for it.
No web source, paper or other implementation was consulted.

## Declared Nets, 5 October 2026

Lane B of the 5 October evening intake (bead `think-8qo9`) added the declared net of
format M (`proof_net`, lemma N0), for wand125’s `mixed_n18_L470` of jlevy/squares#366.
That issue says its reporter changed a copy of this crate “in one place to read the
declared proof net”.
The patch was never requested, fetched or opened: the change here was written from the
certificate format and the mathematics.
The rule above held throughout.

Files read for the change:

- This crate: `INDEPENDENCE.md`, `README.md`, `SOUNDNESS.md`, `Cargo.toml`, `build.rs`,
  `src/certificate.rs`, `src/lib.rs`, `src/main.rs` (lines 140–295), and parts of
  `src/rotated_tests.rs` and `tests/adversarial.rs`. Also `independence-record.yaml`.
- First-party tools: `devtools/check_sqverify_fast.py`, and
  `devtools/sqverify_fast_census.py` except lines 420–470; the gate steps
  `_rust_measure_verifier` and `_rust_measure_verifier_full` of
  `src/sqpack/cli/validate.py`.
- The specification `plan-2026-10-02-independent-measure-verifier.md`, lines 25–80 and
  780–880 (its summary, goals, acceptance and evidence sections).
- jlevy/squares#366’s body, which has no comments.
  It describes the certificate and the reporter’s change in prose and quotes no code.
- From wand125/square-packing-bounds at `43050ed`, data and prose only:
  - for `mixed_n18_L470` and `mixed_n66_L843`: `README.md`, `manifest.json` and
    `candidate.json` (its top-level keys, `proof_net` and two rows);
  - the top-level keys, `net` block and per-angle status, bound and node fields of each
    `certificate.json`;
  - the root `README.md`’s two new sections.
- From the `mixed_n18_L470` proof bundle: `README.md`, `bundle.json`,
  `files-sha256.json`, `proof/summary.json`, and the fields of
  `proof/net001/result.json` with its `manifest` block.
  Also every angle’s `seconds` and `nodes`, and the same fields of the `mixed_n66_L843`
  bundle, which `mixed-fetch` unpacked.
- Of `devtools/audit_wand125_point_and_mixed.py`: its `--help` texts, the packet
  constants and certificate rows (lines 1826–1870 and 2425–2476), to add one row, and
  its module docstring.
  Nothing that drives a checker was opened.
  Also lines 52–70, 148–160 and 336–460 of `tests/test_wand125_mixed_rectangles.py`.
- The receipt `receipts/n50/full/compare.json` of the 28 September packet (its field
  names and status).
- After the change, the lane’s review,
  `docs/project/reviews/review-2026-10-05-wand125-declared-net-n18-n66.md`, except its
  section “What the Authors’ Code Shows” (lines 418–451), which compares the change with
  the source’s code and was skipped for that reason.
  Its findings DN-4 to DN-6 on this crate were then fixed from the findings’ own text: a
  `net` block outside format L is refused, five untested refusals are tested, and the
  controls match refusal messages.
  The finding DN-1 names two functions of `devtools/audit_wand125_point_and_mixed.py` as
  models; they were not opened.

Never opened: any file under a `code/` folder or `proof/verify.cpp` of a bundle.
Those files were checked out and unpacked, and only their Git blob ids and SHA-256
digests were compared, all equal to the retained `mixed_n50_L740` copies.

Commands run: `git clone --filter=blob:none`, `git sparse-checkout`, `git ls-tree`,
`git rev-parse` and `git cat-file blob` for the two tarballs, on the source; `tar xzf`,
`sha256sum` and `jq` over the bundles’ data files.
The `mixed_n18_L470` bundle’s driver ran as a black box with `--help` and the command
its README gives, at two workers.
The audit tool’s `mixed-audit`, `mixed-fetch`, `mixed-price` and `mixed-replay` ran as
black boxes.
On this crate: `cargo build`, `cargo test`, `cargo clippy`, `cargo fmt`, and
`packing-validate --only "measure verifier Rust"`.

## The Declared Net Reviewed, 6 October 2026

The soundness review of 6 October
(`docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md`) read
the whole crate diff from `e020eb1e2` and accepted the crate at `910b6b12c`. It opened
no `code/` folder or `proof/verify.cpp`. Its findings DR-1 to DR-3 were in the census
driver and in the exact evaluator of `devtools/check_sqverify_fast.py`, which the
controls use and which decide nothing.
Lane R1 of the 2026-10-06 intake fixed them there and changed no source file of this
crate (none that `source_sha256` covers).
That lane had read the 5 October declared-net review whole, including the section on the
source’s code that lane B skipped, and is recorded in `independence-record.yaml` for
that reason. The relation of this crate to the source’s checker is unchanged.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
