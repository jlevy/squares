# wand125’s cfcheck: a Second Checker for the Closed-Form Bound

On 14 October 2026, wand125/square-packing added `problems/closed-form/indep-checker/`:
cfcheck, a Rust checker of the closed-form certificate for $s(N) \ge a(N)$ at every
non-square $N \ge 49$, which its README says was written from SPEC.md and the published
bundles only and shares no code with the source’s own checker `replay4d`. The source
reports that it accepted every leaf of intervals 1 and 34 of the 34. jlevy/squares#600
(wand125, 2026-10-14T10:46:56Z) cites it, and bead think-3n1x owns its import.
The bound itself is retained at the earlier pin in
[`../wand125-closed-form-2026-10-14/`](../wand125-closed-form-2026-10-14/README.md),
whose [register plan](../wand125-closed-form-2026-10-14/register-plan.md) the records
lane applies. This packet is a later revision of the same source and is new evidence
about that entry. It retains the checker, checks its claim of independence against the
code, and records a timed sample of it run here, with the price of a complete replay.
The records lane applies the [evidence-update plan](evidence-plan.md).
No standing bound or rating changes here.

| Item | Value |
| --- | --- |
| Source | [`problems/closed-form/indep-checker`](https://github.com/wand125/square-packing/tree/746e2c5ac7a7f534996dd50a5e1fd9f1d8836a8d/problems/closed-form/indep-checker) |
| Pinned revision | `746e2c5ac7a7f534996dd50a5e1fd9f1d8836a8d`, the head of `main`, committed 2026-10-14T10:38:27Z, tree `d2ba54e9…` |
| Earlier pin | `9a28a84`, its parent, retained in `wand125-closed-form-2026-10-14/` |
| What changed | `indep-checker/` added (32 files) and `problems/closed-form/README.md` changed; the folder’s other 25 files are byte-identical to the earlier packet’s and are pinned against it |
| Retrieved | 2026-10-14T11:34:13Z |
| Checker | cfcheck 1.0.0, Rust 2021, on `num-bigint`, `num-rational`, `rayon`, `serde_json` and `sha2`; MIT |
| Source’s results | Intervals 1 and 34, all eight records: 91,044 roots, 3,138,681 leaves, 0 refusals; 242.02 worker-hours recorded |
| Release | `closed-form-v1`, unchanged: `ASSET.json` is one of the identical files |

## The Claim

The checker’s README states its independence in these words:

> Written from SPEC.md and the published bundles only; shares no code with the original
> checkers (`replay4d`, `seam4d_core`, `validate_family.py`), which were not read.
> Written with AI assistance (OpenAI Codex), reviewed by the author, and not peer
> reviewed.

The folder README, which before this commit said “An independent checker has not yet
been written; one would be welcome”, now says cfcheck “was written from `SPEC.md` and
the published assets only and shares no code with `replay4d`, `seam4d_core` or the
search tools”. It also says cfcheck “replayed intervals 1 and 34 completely (all four
regions of each) and accepted every leaf with zero refusals: 91,044 roots and 3,138,681
leaves, the same leaf count as `replay4d` on these two intervals”, and that “the other
32 intervals have not been checked with it”.
Issue #600 repeats both statements.

| Interval | δ | Roots | Leaves | Refusals | Resumed roots |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | $(0, 1/50]$ | 40,257 | 1,653,457 | 0 | 24,226 |
| 34 | $(99/100, 1]$ | 50,787 | 1,485,224 | 0 | 0 |

Interval 1 resumed 24,226 roots from checkpoints that earlier runs of the same checker
wrote. The receipts keep the final checkpoint hashes but not the checkpoints.
The source built cfcheck with rustc 1.99.0.

## Against the Register

Triage maps this by
[result-import.md](../../../campaign/result-import.md#stage-1-triage) as “new evidence
or an author’s answer about a registered entry”.
That means no new entry, the source retained at the revision that holds it, and an
evidence update. The entry is the closed-form lower bound of the 9a28a84 packet, pending
its `T-NNN`. The [evidence-update plan](evidence-plan.md) gives the evidence entry, the
verifier and what each rung can and cannot do.

One fact bounds what the report can carry.
At a count $N$ the bound $s(N) \ge a(N)$ rests on the interval where $a(N)$ is attained:
the supremum is approached by values of δ in that interval alone, or is its closed right
end, the cap $k + d_1$. The 9a28a84 packet’s evaluation names that interval at each of
the record’s 264 non-square counts, and
[`receipts/interval-counts.json`](receipts/interval-counts.json) lists the ones on
intervals 1 and 34. **No count of the record is attained on interval 1. Interval 34
carries exactly the 33 counts $m^2 - 1$, $m^2 - 2$ and $m^2 - 3$ for
$m = 8, \dots, 18$**, where $a(N) = m$ is the cap.
All 33 are `proved` already and equal to their upper bounds (T-084, T-086, T-064). The
two intervals cfcheck covers carry none of the 156 counts where $a(N)$ is above the
reported lower bound.

## Independence, as Stated and as Found

What its authors read cannot be checked here.
What its code shares with the producer’s can, and
[`comparison/shared_code.py`](comparison/shared_code.py) compared the retained cfcheck
tree (31 files) with the producer’s `checker/` and `structure/` in the 9a28a84 packet
(16 files). The output is
[`comparison/outputs/shared-code.json`](comparison/outputs/shared-code.json).

| Measure | cfcheck against the producer | Baselines: unrelated exact checkers |
| --- | --- | --- |
| Files with equal SHA-256 | 0 | — |
| Path dependencies, and local crates both `Cargo.lock` files pin | none, none | — |
| Registry crates both pin | 12: `serde_json` and its dependencies, serde’s derive macros, and `libc` | — |
| Arithmetic | `num-bigint`/`num-rational` under its own checked-`i128` rationals (`small_rat.rs`) | the producer uses `rug` over GMP |
| Source lines of ≥ 40 characters in both | 0 | — |
| Comments of ≥ 20 characters in both | 0 | — |
| Longest run of identical tokens | 34 tokens; 1 run of ≥ 30 | 15–18 tokens; none of ≥ 30 |
| 25-token windows also in the other tree | 0.02% | 0.00% |
| Longest run with identifiers and literals renamed | 96 tokens; 26 runs of ≥ 30 | 28–45 tokens; 0–8 runs of ≥ 30 |
| Renamed 25-token windows also in the other tree | 1.16% | 0.05–0.15% |

The baselines run the same measures between cfcheck, or the producer, and three Rust
checkers that share no author with either: Evan Daniel’s `zmx2` and `verify2` and this
repository’s `sqverify_exact`. A positive control appends the producer’s `wmin` (from
`seam4d_core/src/lib.rs`) to a copy of cfcheck’s `geom.rs`. It is found as a 122-token
run both verbatim and with `wmin`, `u0` and `u1` renamed, so a pasted function of that
size would not have been missed.

**Nothing is copied.** No file, line, comment, crate or arithmetic kernel is shared.
The one plain run of 34 tokens is the Rust idiom that starts the tiling check’s stack:
`vec![(root.clone(), (0..leaves.len()).collect::<Vec<_>>())]` followed by `while let`.

**The structure is shared, and SPEC.md is why.** The renamed overlap is 8 to 23 times
the baselines’. Every run of 30 tokens or more was read.
Each one is a procedure SPEC.md states step by step, a standard formula, or a Rust
idiom:

- the bisection-tree reconstruction of the tiling, with its axis order u, δ, x, y
  (SPEC.md §6.2);
- the B4U edge stage’s frontier, cap and sampling, with the resample $s \mapsto lo +
  (s - lo) \cdot 2/3$ and the 60-attempt and 2,000-run limits (§5.11);
- the 60-attempt guarded resampling loop (§5.4, §5.11);
- the edge quadratic $A = 2[g(p) - 2g((p+q)/2) + g(q)]$, $B = f(1) - f(0) - A$, whence
  the shared names `gp`, `gm`, `gq`, `fp` and `fq` (§5.11);
- the half-angle normals $c = (1 - u^2)/(1 + u^2)$ and $s = 2u/(1 + u^2)$ (§4);
- the cross product of two plane-coefficient vectors (§5.11, step 2) and the contact
  planes (§5.3);
- struct-field lists, unit-test boilerplate and parser idioms, and lists of literals,
  which renaming makes equal to any other list: cfcheck’s leaf kinds match `replay4d`’s
  table of SHA-256 round constants.

The places where the two differ are where SPEC.md leaves a choice:

- The B4U critical value: cfcheck evaluates SPEC.md’s table form $f(p) - B^2/(4A)$,
  where `replay4d` evaluates $f$ at $t = -B/(2A)$.
- The tests: cfcheck’s fixtures use other boxes and other families.
- The profiling record: cfcheck’s has none of `replay4d`’s fields.
- Many local names differ, among them `last`/`cnt`/`sign_at` against
  `prev`/`out`/`side_sign`.

SPEC.md names `nonneg_open`, and §5.12 describes `replay4d`’s own dispatch, so SPEC.md
is the producer’s description of its own checker’s procedures.
Its names and constants are the producer’s, and cfcheck follows them.

**Authorship overlaps the producer’s in both the person and the AI systems.** cfcheck’s
README names OpenAI Codex and review by the author.
`Cargo.toml` names Hiroaki Hosono (wand125) as author, and the commit that adds it names
Claude Opus 5.5 as co-author.
Issue #600 says “the search, the certificates, the checkers and this text were produced
with AI assistance (Claude and Codex), under the direction of and reviewed by Hiroaki
Hosono (wand125)”. The person who reviewed cfcheck therefore wrote the producer’s code,
with the same two system families.
Whether its prompts were separate from the producer’s is not stated.

**What the program reads that the producer wrote**:

- SPEC.md, which is the proof text and the specification.
- The certificate and its format.
- The producer’s outputs: the digests and published counts in `intervals.json`, which
  cfcheck refuses to differ from; the five values of $a(N)$ from the folder README’s
  table, which `coverage.rs` hard-codes; and a copy of `intervals.json` as its test
  fixture.

**Finding.** cfcheck is an independent implementation in the sense of
[epistemics.md](../../../../epistemics.md#the-independence-ladder): it shares none of
the producer’s code.
Its clean room is the source’s statement, and the code is consistent with it.
What the authors read cannot be checked here, and the person who reviewed it is the
producer. It implements the producer’s own detailed specification of the producer’s
procedures.
So it can rule out errors in `replay4d`’s and `seam4d_core`’s code: a slip in
an index, a dropped case, a sign, the arithmetic kernel, and the Sturm and gcd shortcuts
the mathematical review read in `b3d.rs`. It cannot rule out an error in a procedure
SPEC.md states: an omitted contact plane, an unsound limit, a wrong sampling rule.
The
[mathematical review](../../../../docs/project/reviews/review-2026-10-14-wand125-closed-form-lower-bound.md)
re-derived SPEC.md’s lemmas and found them sound; it did not read cfcheck.

## What Was Run Here

All runs used one build of cfcheck made from this packet’s retained copy.
The upstream tree was first restored in scratch (the fixture and the folder’s unchanged
files from the 9a28a84 packet, `intervals.json` decompressed), and all 39 files were
matched to this packet’s manifest by `sha256sum -c`. The host was four cores shared with
other agents, with load average 1 to 3.5 throughout.

- **Custody.** `interval_0_0.02.tar.gz`, `interval_0.99_1.tar.gz` and the release’s
  `SHA256SUMS` were downloaded at 2026-10-14T11:38:37Z. Their SHA-256 equals
  `ASSET.json` and the release API’s digests (`f847fd55…`, `04b7a25f…`, `2e31850c…`),
  each archive’s own `SHA256SUMS` passed for all six members, and the archives hold
  plain files only. They stay with the author.

- **Build and tests.** `cargo fetch --locked` fetched the 32 crates that `Cargo.lock`
  pins. `cargo build --release --locked --offline -j 2` with rustc 1.97.0 took 38 s; the
  binary’s SHA-256 is `c5a163d4…6484`. `cargo test --release --locked --offline` passed
  all 42 tests in 16.5 s of wall and 28.8 CPU-seconds.

- **Premises in full, both intervals.** Two `interval` runs with leaf selection
  ([`receipts/runs/`](receipts/runs/)) ran every check cfcheck makes before the leaf
  tests, on all eight records, and none refused:
  - every input digest against `SHA256SUMS` and `intervals.json`;
  - the structure of all four families: the wall period of mass 9/5, the reversal
    identities, the saving at both ends equal to the stored one and on the certified
    line, and global against local agreement at $k = 7, 8, 9$;
  - the region bounds;
  - the product grid and 90-degree cover of the roots;
  - the bisection tiling of every one of the 91,044 roots;
  - the published counts of roots, leaves and kinds per record.

- **Leaf tests, a stated sample.** 2,909 distinct leaves were checked, and every one was
  accepted.
  - The timing run on the smallest record, interval 1’s `top.rec` (2,673 roots, 171,634
    leaves), checked the first 200 leaves of each of its eight kinds in record order,
    1,320 leaves.
  - The two interval runs checked the first 25 leaves (interval 1) and the first 20
    (interval 34) of each kind but B4U in each record: 1,001 and 773 leaves, of which
    interval 1’s 185 in `top.rec` are among the timing run’s.
  - That is 2,909 of 3,138,681 leaves in these two intervals, and of 187,183,108 in the
    certificate.
  - B4U was left out: its 111 leaves are in the last four roots of interval 1’s
    `left.rec`, and the source times them at 1,981 s each.

- **Controls** ([`receipts/controls/`](receipts/controls/)). Three mutated copies of the
  assets were re-sealed: `SHA256SUMS`, the digests in `intervals.json` and the published
  counts were rewritten to match each mutation, so that only the targeted check could
  object. Each was refused, exit 1, with that check’s reason and no other:

| Mutation | Run | Refusal |
| --- | --- | --- |
| Interval 1, `top.rec` line 1 appended again | premises | `domain: duplicate root` |
| Interval 1, `top.rec` line 1, leaf 1 relabelled from `CORE1:Tx` to `CORE` | first root of each record | `line 1, leaf 1 (CORE): CORE bound is undefined or below 1` |
| Interval 34, every mass and density of both families times 99/100 | premises | `wall period mass is not 9/5` |

  The unmutated leaf of the second control was accepted in both runs that checked it.

| Run | Wall | CPU | Leaves checked | Verdict |
| --- | ---: | ---: | ---: | --- |
| Smallest record, interval 1 `top.rec`, 200 per kind | 154.2 s | 245.8 s | 1,320 | `CFCHECK PARTIAL`, 0 refusals |
| Interval 1, premises in full, 25 per kind and record | 1,000.9 s | 1,469.2 s | 1,001 | `CFCHECK PARTIAL`, 0 refusals |
| Interval 34, premises in full, 20 per kind and record | 647.4 s | 831.4 s | 773 | `CFCHECK PARTIAL`, 0 refusals |
| Three controls | 29.9 s | 29.1 s | 1 | `CFCHECK REFUSE` each |

`CFCHECK PARTIAL` is cfcheck’s verdict for a run with leaf selection, exit 0. It is not
acceptance of a record.
In all, the cfcheck runs here took 42.9 CPU-minutes.

## The Price

[`receipts/price.json`](receipts/price.json) prices a complete replay of intervals 1 and
34 from the source’s receipts, since the full replay is far above the brief’s 60
CPU-minutes. The receipts record 242.02 worker-hours of summed per-leaf time.
The source calls that an approximation to CPU time.
The leaves of interval 1’s 24,226 resumed roots carry no timing.
At the source’s own per-kind rates they add 46.43 worker-hours, for **288.45
worker-hours at the source’s rates**. Of that, B4U is 61.1 hours: 111 leaves, each a
single task of about 33 minutes.
The 78 EX:CORE and EY:CORE leaves the source never timed take about 0.003 s each here.

On this host, the timing run on the smallest record took 1.11 times the source’s
per-kind rates for the same kinds, which gives about 320 CPU-hours.
Over all twelve sampled region runs the ratio is 2.39 (0.43 to 5.71), which gives about
650 CPU-hours. The spread is selection as much as speed: the first leaves of a kind in
record order are not its average leaves.
Interval 1’s first 25 B3D leaves in `straddle.rec` took 27.8 s each, against 0.76 s for
the kind pooled over the regions the source timed in that interval.
The source timed nothing of that record, so its 19.95 hours are the pooled estimate;
`replay4d` spent 24.74 CPU-hours there, its costliest of the eight.
Either estimate is 80 to 160 hours of wall on four dedicated cores.

For scale, `replay4d` replayed the same eight records in 124.65 CPU-hours by the
source’s `published_checker.json`. That makes cfcheck 1.59 times as costly on interval
1, 3.77 times on interval 34, and 2.31 times on the two.
At those ratios a cfcheck replay of all 136 records would be about 9,900 worker-hours,
between 6,800 and 16,200, against `replay4d`’s 4,294. The two measures differ,
worker-thread elapsed time against process CPU time, so the ratio is a rough one.

## What Was Not Run

No record was checked in full, and no complete replay of interval 1 or 34 ran here.
The 2,909 leaves are a sample, and they decide nothing about the other 3,135,772 in
these two intervals.
The 32 other intervals were not touched.
B4U, the kind that costs most, was not timed here.
The source’s checkpoints for interval 1’s resumed roots are not published, so its
interval-1 receipt rests in part on runs that only their final hashes record.

## Programs Kept Here

Both run from `packing/` with the project interpreter and import nothing of the source.
Neither decides anything about the certificate.

- [`replay/cfcheck_replay.py`](replay/cfcheck_replay.py) prices, runs and controls
  cfcheck:
  - `plan` predicts the cost of the first roots of a record at the source’s rates.
  - `counts` lists the counts whose $a(N)$ is attained on given intervals, from the
    9a28a84 evaluation’s `counts.tsv`.
  - `price` reads the source’s two receipts and `intervals.json`. It checks that both
    receipts name only the published input digests and counts, which they do, prices the
    replay, and with `--calibration` scales the price by runs made here.
  - `run` runs one cfcheck command and writes a receipt: the binary’s digest, wall and
    `getrusage` CPU time, the exit code and verdict, cfcheck’s JSON report kept byte for
    byte, and a summary of it.
  - `mutate` writes the re-sealed mutants.
- [`comparison/shared_code.py`](comparison/shared_code.py) compares the two code trees
  as the section above says, and fails if its positive control is not found.
  It printed the table’s figures and `positive_control_found: True`.

## Retained Here

`problems/closed-form/indep-checker/` and the folder’s `LICENSE` are MIT, so
`devtools.acquire_source` retains them byte-identical under `square-packing/`, with the
changed folder `README.md` and the root `LICENSE.md`. It wrote them from the declaration
in [acquisition/declaration.json](acquisition/declaration.json):
[acquisition/sources.json](acquisition/sources.json) is the record, and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the
manifest of all 60 files of the folder and `LICENSE.md` at the pin.
The folder’s other 25 files and the checker’s test fixture
`tests/fixtures/intervals.json` are pinned by digest as identical to the 9a28a84
packet’s copies, and the acquisition compared their bytes.
So the manifest shows that nothing in the folder but `README.md` and `indep-checker/`
changed.

| Path | What it is |
| --- | --- |
| `square-packing/problems/closed-form/indep-checker/src/` | cfcheck’s 16 Rust modules: rationals, polynomials and Sturm isolation, guarded symbolic signs, geometry, family structure, records and tiling, leaf tests, checkpoints, the report |
| `square-packing/problems/closed-form/indep-checker/tests/` | The integration tests, their fixture README and the reference polynomial code; the fixture itself is pinned |
| `square-packing/problems/closed-form/indep-checker/receipts/` | The source’s two interval reports and its checkpoint hashes |
| `square-packing/problems/closed-form/indep-checker/README.md`, `Cargo.toml`, `Cargo.lock`, `LICENSE`, `.cargo/`, `.gitignore` | The checker’s claim, build, locked dependencies and MIT notice |
| `square-packing/problems/closed-form/README.md`, `LICENSE` | The folder README as changed at the pin, and the folder’s MIT notice |
| `square-packing/LICENSE.md` | The repository’s statement that each folder keeps its own licence |
| `comparison/` | The code comparison and its output |
| `replay/`, `receipts/` | The stage-4 program, the price, the interval counts, the runs and the controls |
| `evidence-plan.md` | The evidence update for the records lane |

## Sources and Notices

`indep-checker/LICENSE` is MIT, Copyright (c) 2026 Hiroaki Hosono (wand125), and
`Cargo.toml` says `license = "MIT"` and names him as author.
`problems/closed-form/LICENSE` is MIT, Copyright (c) 2026 wand125. The root `LICENSE.md`
says the repository has no single licence and that each folder keeps its own.
Neither README credits a method cfcheck builds on, and neither cites this project.
The checker’s README says it was “written with AI assistance (OpenAI Codex), reviewed by
the author, and not peer reviewed”.
The commit that adds it names Claude Opus 5.5 as co-author.
Issue #600 credits Hiroaki Hosono (wand125) and names Claude and Codex for the search,
the certificates, the checkers and the text.

## Commands

From `packing/`, with `S` a scratch directory holding the restored tree, the build and
the unpacked assets as above:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source wand125-closed-form-cfcheck-2026-10-14 --check
uv run --frozen --all-extras --group dev python -I resources/web/wand125-closed-form-cfcheck-2026-10-14/comparison/shared_code.py --out resources/web/wand125-closed-form-cfcheck-2026-10-14/comparison/outputs/shared-code.json
uv run --frozen --all-extras --group dev python -I resources/web/wand125-closed-form-cfcheck-2026-10-14/replay/cfcheck_replay.py counts --out resources/web/wand125-closed-form-cfcheck-2026-10-14/receipts/interval-counts.json
uv run --frozen --all-extras --group dev python -I resources/web/wand125-closed-form-cfcheck-2026-10-14/replay/cfcheck_replay.py price --calibration resources/web/wand125-closed-form-cfcheck-2026-10-14/receipts/runs/{smallest-record-timing,interval-1-premises-and-kind-sample,interval-34-premises-and-kind-sample}.json --out resources/web/wand125-closed-form-cfcheck-2026-10-14/receipts/price.json
```

Each run receipt records its cfcheck command, run from `S/run`, which holds
`intervals.json` and `assets/<interval>/`; the control receipts were run from
`S/controls/<mutation>/`, which `mutate` writes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
