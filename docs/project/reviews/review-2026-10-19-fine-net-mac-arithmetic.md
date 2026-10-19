# Fine-Net Mac Arithmetic and Capture Review

2026-10-19. Review A, kind `correctness`, by Codex/OpenAI Astra at maximum reasoning
(`tbd-strong-max`). Review bead `think-m1ff`, under qualification bead `think-haaq`.
Workflow entry point: `tbd shortcut review-code review-code-correctness`. This is a
scoped platform and execution review; no pull request is being reviewed or published.

**Decision: accept the preserved Mac binary for the proposed raw capture and control
route, with the conditions below.** The coordinator may run the isolated n108 control
calibration, then the 13 remaining first-subset cases.
No mathematical blocker to that platform transition was found.
A1 blocks use of the current evidence renderer for Mac assurance.
A2 requires an explicit unavailable-CPU annotation and separate aggregate timing.
Both are tracked by open follow-up `think-dazj`.

This decision establishes neither a new completed certificate nor a stronger assurance
level for any case. Each new case still needs complete coverage, its controls, and the
separate certificate mathematics and records review.
Historical n108 remains T-216 with its Linux evidence.
No full direction verification, certificate capture, or control ran as part of this
review.

## Scope and Custody

The source tree is `.worktrees/review-668-math-20261018`, at
`461e20b939c7635e65fcb5491ec39399b2177045`. Its 19 files listed in the
[build receipt](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-mac/platform/fine-net-mac-build.json),
and `packing/devtools/sqverify_fast_census.py`, were independently compared byte for
byte with Git objects at main `0ee05f4f3d0863f75c1036757839985e75655677`; all matched.
The scoped `git diff` between those commits was empty.
Source references below use repository-relative paths and line numbers in this tree.

| Identity | Observed value |
| --- | --- |
| Crate source digest, recomputed by `build.rs`’s rule | `d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88` |
| Preserved binary SHA-256, independently recomputed | `e44f27eb8f3375d85c71e085fe7d04667d38f28c589beae267457573be4ae61d` |
| Binary size and format | 849,712 bytes; Mach-O 64-bit executable arm64 |
| Binary’s emitted build identity | `release`, `aarch64-apple-darwin`, `rustc 1.98.0 (88d9e12ae 2026-08-18)` |
| Installed compiler | Commit `88d9e12ae178fab0fb5cc050a94da85685d449ea`; LLVM 22.1.8; host `aarch64-apple-darwin` |
| Observed OS | macOS 26.5.2, build 25F84; `uname -m` = `arm64` |
| Cargo binary fingerprint | `rustflags: []`; release profile from the unchanged manifest |

The executable is
`/Volumes/spud-ext1/agent-source/squares-fine-net-mac-haaq/sqverify-fast`. That
directory also preserves `build-receipt.json`, `build.log`, and `native-tests.log`. The
coordinator’s build command was
`cargo +1.98.0 build --release --locked --offline --jobs 2`; its retained log reports
18.20 seconds.
I inspected the native release test log: 13 library, 17 adversarial, and 8
declared-net tests passed, with zero failures or ignored tests.
I did not rebuild the verifier or rerun that suite.

The accepted declared-net review’s build checklist at
`docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md:611`
requires this source, release profile, and Rust 1.98.0; its re-review conditions at line
634 cover source, lockfile, build script, toolchain, and control-logic changes.
It contains no blanket ARM exclusion.
This report supplies the additional bounded platform evidence; it does not repeat the
unchanged net, domain, and capture proof.

All 18 physical `candidate.json.gz` files under
`/Volumes/spud-ext1/agent-source/squares-671-retention-20261018/packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/`
were independently compared with the same pinned main Git objects.
Their stored and decompressed sizes and SHA-256 values also matched
[the acquisition audit](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-mac/platform/fine-net-resume-evidence.json).
The stored candidates total 763,547 bytes.
The unlicensed adapted verifier archive was neither opened nor executed.

Materializing these 18 exact candidate blobs in the existing sparse source tree is
compatible with the standard CLI. `mixed_cases` reads those candidates; `run` and
`control` use their paths directly (`sqverify_fast_census.py:258,375,797`). Raw capture
and controls need no upstream checker or replay-source files.
The complete preserved external packet remains the acquisition evidence.
No symlink, replacement implementation, or runtime modification is needed for this
route.

## Arithmetic Invariants Checked

**Outward bounds require separately rounded binary64 operations and gradual underflow.**
`interval.rs:1–94` implements lower and upper rounding by adding or subtracting a
representable outward increment; it does not set a directed hardware rounding mode.
Lemma I1 in `SOUNDNESS.md:416–441` assumes round to nearest and retention of the
smallest subnormal. A flush-to-zero setting would break that argument at zero and tiny
inputs.
ARM availability of fused instructions alone does not imply that this binary uses
them.

Rust documents `f64` as binary64, directs readers to the primitive arithmetic contract
using round-to-nearest/ties-to-even, and distinguishes `mul_add` from separate multiply
and add. Apple’s XNU ARM64 definitions set the default FPCR to zero, with separate
rounding-mode and flush-to-zero fields.
These contracts support the platform argument; the actual executable and runtime checks
below provide local evidence.
[Rust f64](https://doc.rust-lang.org/std/primitive.f64.html),
[primitive arithmetic](https://doc.rust-lang.org/std/primitive.f32.html),
[fused versus separate operations](https://doc.rust-lang.org/std/primitive.f64.html#method.mul_add),
[Apple FPCR definitions](https://github.com/apple-oss-distributions/xnu/blob/main/osfmk/arm64/proc_reg.h#L744-L777).

The preserved executable’s disassembly contained 470 `fadd`, 180 `fsub`, 340 `fmul`, and
31 `fdiv` instructions, and zero `fmadd`, `fmsub`, `fnmadd`, `fnmsub`, `fmla`, or `fmls`
instructions. No write to FPCR was found.
A small probe compiled from the unchanged `interval.rs`, with Rust 1.98.0 and the
release optimization settings, reported FPCR `0x0` on both its main thread and a spawned
worker. In each context, 12 boundary values and 197,291 eligible signed random bit
patterns passed `dn(x) <= x.next_down()` and `up(x) >= x.next_up()`. Separate
multiply/add, NaN propagation, and overflow refusal checks also passed.
The exact probe is retained below.
These are bounded checks, not an exhaustive hardware or compiler proof.

**Admission and exact oracles remain rational.** `exact.rs:112–144` checks rational
enclosures by exact comparisons and adjacent floating-point values.
Net directions are rational rotations, so the route does not acquire a platform `sin`,
`cos`, or `atan` accuracy dependency.
The existing adversarial tests exercise overflow and NaN behavior; target-specific NaN
payload bits are not an acceptance criterion.

The preserved Mac binary was also probed at three n108 centres selected from its
historical Linux log.
Every exact capture agreed with the separately implemented Python `mixed_exact`, and
every certified centre lower bound was at most that exact capture.
The point coordinates were interpreted as the exact rational values of their binary64
representations, as the CLI does.

| Probe argument `r,x,y` | Mac certified centre lower bound | Result |
| --- | ---: | --- |
| `1,8.968381471571806,6.164718135848612` | 1.0790363969005965 | Exact agreement; valid lower bound; exit 0 |
| `100,9.82882009963122,7.67278175144116` | 1.1215651722588005 | Exact agreement; valid lower bound; exit 0 |
| `200,6.301150360420976,5.907836725333286` | 1.019116016778944 | Exact agreement; valid lower bound; exit 0 |

**Partial work cannot establish the theorem.** A bounded native invocation with
`--directions 1 --max-nodes 1 --confirm --threads 1` returned exit 1, `unresolved`, one
node, summary `REFUSED`, and the expected Mac build identity.
It did not verify direction 1. In the source, the native summary requires all requested
directions verified and a full net before emitting `VERIFIED` (`main.rs:264–272`). The
scoped review found no platform change in these predicates or the exact threshold
comparison.
Two workers assign independent directions and join before the sorted summary.

## Findings

**A1 — High: the evidence renderer makes false host claims for Mac results.**
`packing/devtools/sqverify_fast_census.py:1336–1337` writes “4-core x86-64 Linux
container” and describes the build as x86-64 Linux regardless of its recorded target.
The rectangle renderer has the same platform problem at lines 1545–1547. Applying
`--evidence` to a valid Mac result would publish inaccurate assurance metadata.

**Fix:** derive compiler, profile, and target from each preserved build receipt; derive
host facts from a run receipt or omit them when unknown.
Keep historical Linux descriptions true.
Until that focused change is reviewed, do not use `--evidence` or publish its Mac
output. The coordinator also keeps report generation out of this raw execution phase.
Tracked by `think-dazj`; no source edit was made here.

**A2 — Medium: an unavailable CPU measurement becomes zero in the native summary.**
`packing/sqverify_fast/src/lib.rs:25–31,87–89` reads Linux `/proc/thread-self/schedstat`
and omits per-direction `cpu_seconds` on Mac.
`src/main.rs:281` sums the present values, yielding zero for an empty set.
The bounded native run reproduced `direction_cpu_seconds: -0.0` with no direction CPU
field. That value is unavailable data, not measured zero consumption.

**Fix:** represent unavailable per-direction totals explicitly in future output or its
consumer. Preserve the already produced native bytes and attach the interpretation in a
separate execution receipt.
A change to the crate creates a new source/build identity and needs its own focused
review; this finding does not require replacing the qualified binary before raw capture.
Tracked by `think-dazj`.

The capture driver independently records process CPU as `wait4` user plus system time
(`sqverify_fast_census.py:410,477`). Its per-direction map is empty on Mac; the mixed
report displays absent comparison timing as `-` and suppresses the ratio (`:1837–1869`).
No inspected verdict or control predicate reads CPU fields.
Controls record wall seconds, with no aggregate CPU field (`:500–522,712–760`), so
preserve `/usr/bin/time -l -o UNIQUE_LOG` output for the complete control command.
The coordinator will time captures the same way and compare their native-process CPU
with the census `wait4` figure, allowing for driver and exact-probe overhead.
Neither zero nor wall seconds may be reported as the control’s CPU cost.

## Accepted Execution Conditions

1. Use the preserved binary above and the unchanged reviewed driver.
   Keep the normal floating-point environment; no fast-math build or floating-point mode
   override is covered.
   A new executable, source, toolchain, or arithmetic configuration requires renewed
   qualification. Retain command, build identity, candidate identity, platform, and
   timing together with each result.

2. Confirm the materialized candidate files and exact selection before execution.
   The first subset is n = 38, 68, 84, 85, 86, 88, 89, 90, 91, 92, 106, 107, 108, and
   110\. n108 is already complete.
   The remaining 13 cases comprise n38 with 2,073 directions and 12 cases with 201 each,
   totaling 4,485 capture directions.
   Counts 40, 41, 43, and 51 are outside this launch.
   Assert the complete roster and each single-case selection; a missing packet or
   misspelled `--only` can select zero cases and make `--check` print `0 of 0` with exit
   0 (`:2142–2170`).

3. For the coordinator’s chosen calibration, copy the authentic completed n108 census,
   capture, and control into an isolated external output directory and preserve a
   baseline copy. Run the standard whole-net `--control --threads 2` there.
   The driver explicitly allows a newer control build (`:842`), so this is a Mac route
   calibration against an existing genuine `VERIFIED` row.
   Its new control must never replace the historical Linux evidence or be presented as a
   new Mac n108 capture.
   Require a complete `CONTROLS_REFUSED` result before advancing in this chosen launch
   sequence.

4. Run each missing case through the maintained CLI in this order: capture with
   `--threads 2 --resume`, `--check --only CERTIFICATE`, then whole-net
   `--control --threads 2`. The runbook says “Run `--control` before counting on its
   receipt” (`packing/campaign/result-import.md:547`); it does not require an impossible
   control before a missing case has a verified census row.
   `control` checks for that row at `sqverify_fast_census.py:811–813`.

5. Require the selected capture’s zero native exit, `VERIFIED`, exact complete indices,
   all direction verdicts verified, matching net premises, and exact least-leaf capture
   at least one. `--check` is necessary but checks only summary status, exit, and the
   least-leaf flag; inspect the saved rows as well.
   The capture CLI itself returns zero after recording a failed case, so its shell exit
   alone is insufficient.
   Require `CONTROLS_REFUSED`, complete control indices, matching candidate/build
   identity, independent exact capture agreement, and valid in-domain coverage refusals
   before reliance. `unresolved`, an arithmetic error, or a sampled control cannot
   substitute for that result (`:771–794,1022–1047`).

6. Keep one writer to each output census.
   Preserve each completed capture/control pair and execution/timing receipt outside
   disposable scratch before the next case.
   `--resume` preserves a complete `VERIFIED` case across builds; avoid `--same-build`
   when retaining Linux n108. It neither resumes partial direction streams nor proves
   that a skipped capture has controls.
   Live capture streams are private temporary files and the completed census/control
   files use replacing writes; they are not a crash-safe checkpoint journal.
   Preserve prior snapshots and rerun an interrupted certificate completely, rather than
   trusting a partial file.

7. Maintain the two-native-worker ceiling and the coordinator’s host scheduling gate.
   Use external `TMPDIR`, a task/worktree-specific `CARGO_TARGET_DIR`, external
   `UV_CACHE_DIR`, bytecode disabled, and the supplied pytest retention options if tests
   are run. The initial sandboxed write check failed; an authorized external-directory
   check and probe creation then succeeded.
   The volume had 58 GiB available.
   This review created no new environment or checkout.

8. Retain the native CPU zero unchanged, mark it unavailable in the execution receipt,
   and preserve measured aggregate CPU and wall time for both capture and control.
   The earlier 24.7–28.4 CPU-hour first-subset price includes completed n108 and is
   based on an earlier host comparison; it is not a measured Mac price.
   Calibration is additional work.
   Account for actual costs as cases finish, and do not expand this launch to the
   approximately 95 CPU-hour full set.

## Design Assessment and Documentation

The existing CLI with exact candidate-only materialization keeps the reviewed admission,
capture, and control code together.
Direct `Case` orchestration would add another invocation path without a benefit for this
bounded run.
Preserving genuine Linux n108 and separating optional Mac calibration avoids
discarding valid evidence or inventing cross-platform reproducibility.
Per-case retained checkpoints limit loss if the driver or host stops between cases.

The published proof still depends on IEEE arithmetic, trusted execution, the retained
candidate, the unchanged reviewed mathematics, and complete per-case receipts.
This report supplies platform qualification and process conditions; it supplies no new
whole-domain coverage.
Stage-4 promotion still requires the independent certificate review and records checks
specified by the import runbook.
The renderer correction and CPU interpretation belong to `think-dazj`; no broad
documentation or source rewrite is needed to begin retaining raw evidence.

## Commands, Results, and Review Limits

- Ran `tbd prime`, `tbd policy show`, the two review shortcuts, relevant engineering,
  Rust, Python, filesystem, and documentation guidelines, and child create/start/sync.
  Effective grants were read from main; this review made no GitHub mutation.
  The sandbox initially denied the tbd lock; authorized bookkeeping succeeded with
  escalation. `think-haaq` and the original `think-f40c` delegate were preserved.
- Ran `git rev-parse`, scoped `git diff`, and `git show` comparisons using the existing
  Python 3.14.7. Results: 19 crate-associated files and the driver identical to pinned
  main; all 18 candidate stored/raw comparisons passed.
  Recomputed the crate digest using its ordered filename/NUL/content/NUL rule and
  matched the accepted value.
- Ran `/usr/bin/file`, `/usr/bin/shasum -a 256`, `rustc +1.98.0 -vV`, `uname -m`, and
  `sw_vers`; the identity table records their results.
  Ran `/usr/bin/otool -tv` and counted instruction mnemonics; it exited zero with
  nonfatal Apple developer-tool cache-location diagnostics.
  Read the Cargo binary fingerprint’s empty `rustflags`.
- Compiled and ran the probe below, exit zero.
  Inspected the 38 native release test passes already retained by the coordinator; no
  broad gate was run.
- Ran the three point probes and one-node refusal shown above.
  Independent evaluation used
  `mixed_exact(raw, Fraction(x_float), Fraction(y_float), r)`. Two initial scratch
  assertions used the wrong probe contracts: decimal-rational coordinates instead of
  binary64 coordinates, then an assumed certified upper bound from `centre_estimate_up`.
  Reading `main.rs:140–177` and `rotated.rs:1107–1125` resolved both: the latter is a
  stopping heuristic. The corrected checks match the maintained differential tool’s
  contract and passed.
  Neither initial failure demonstrated a verifier defect.
- Read local `man time`: `-l -o FILE` is supported, and the wrapper preserves the
  utility’s exit status.
  A second one-node diagnostic tested descendant accounting:
  `/usr/bin/time -lp -o "$TMPDIR/one-node-wrapper.time"` wrapped Python using
  `os.posix_spawn` and `os.wait4` on the same bounded native command.
  Native exit was 1, as expected; its `wait4` CPU was 0.465506 seconds (0.461188 user,
  0.004318 system), and the outer wrapper reported 0.50 real, 0.48 user, and 0.01 system
  seconds. The wrapper therefore included the native child’s cost in this observed run.
  No timed full capture/control was run here.
  The primary external references above were read; the versioned Rust 1.98 HTML URL was
  unavailable, so compiler identity comes from the installed toolchain and executable,
  not that URL.

The arithmetic probe ran in
`/Volumes/spud-ext1/agent-scratch/squares-fine-net-mac-math-m1ff/tmp/`, using external
cache and target paths.
Its source is reproduced here so the unique review evidence does not depend on
disposable scratch. Command:

```bash
rustc +1.98.0 --edition=2024 -C opt-level=3 -C lto=fat -C codegen-units=1 \
  -C panic=abort "$TMPDIR/fp_contract.rs" -o "$TMPDIR/fp_contract"
"$TMPDIR/fp_contract"
```

```rust
#[allow(dead_code)]
#[path = "/Users/levy/wrk/github/squares/.worktrees/review-668-math-20261018/packing/sqverify_fast/src/interval.rs"]
mod interval;
use std::hint::black_box;
fn check(label: &str) {
    let fpcr: u64;
    // SAFETY: reads the AArch64 user floating-point control register, no memory or state mutation.
    unsafe { std::arch::asm!("mrs {v}, fpcr", v = out(reg) fpcr, options(nomem, nostack, preserves_flags)); }
    assert_eq!(fpcr & ((3 << 22) | (1 << 24)), 0, "round-to-nearest and gradual underflow required");
    let a = black_box(1.0 + f64::EPSILON);
    let b = black_box(1.0 - f64::EPSILON);
    let c = black_box(-1.0);
    let separate = a * b + c;
    assert_eq!(separate, 0.0, "implicit FMA would give -epsilon squared");
    let special = [0., -0., 1., -1., f64::from_bits(1), -f64::from_bits(1), f64::MIN_POSITIVE, -f64::MIN_POSITIVE, 1e-310, -1e-310, 1e300, -1e300];
    for x in special {
        let x = black_box(x);
        assert!(interval::up(x) >= x.next_up() && interval::dn(x) <= x.next_down());
    }
    let mut state = 0x86b5_92ce_a713_f149u64;
    let mut tested = 0;
    for _ in 0..200_000 {
        state = state.wrapping_mul(6_364_136_223_846_793_005).wrapping_add(1);
        let x = black_box(f64::from_bits(state));
        if x.is_finite() && x.abs() < 1e300 {
            assert!(interval::up(x) >= x.next_up() && interval::dn(x) <= x.next_down(), "{x:e}");
            tested += 1;
        }
    }
    assert!(interval::fmin(black_box(f64::NAN), 1.).is_nan());
    assert!(interval::fmax(1., black_box(f64::NAN)).is_nan());
    assert!(interval::add_dn(black_box(f64::MAX), f64::MAX).is_nan());
    println!("{label}: fpcr=0x{fpcr:x}; nonfused={separate}; boundary=12; random={tested}; NaN/overflow=pass");
}
fn main() {
    check("main");
    std::thread::spawn(|| check("worker")).join().expect("worker passed");
}
```

Output:

```text
main: fpcr=0x0; nonfused=0; boundary=12; random=197291; NaN/overflow=pass
worker: fpcr=0x0; nonfused=0; boundary=12; random=197291; NaN/overflow=pass
```

## Records Preparation Addendum, 19 October 2026

The records lane retains this earlier local decision as the mapped stage-4 review.
Its accepted computations and findings are unchanged; relative artifact links now name
the retained packet copies.
The verbatim local note is retained under the packet’s `review-mac/notes/` directory.
Historical commands and source comparisons describe the original run, not a rerun
against today’s tree.

The coordinator accepted the current fine-net reporter after the B1/B2 correction at
`e062abfacfef60aa160ccd7b177c5b29eb31c2f8`. Current-packet output retains actual Mac
build facts, unavailable direction CPU, shared verifier components and the distinct
per-case exit/control observations.
The historical no-run prose issue remains separately owned by `think-vxh5`; no
historical evidence was regenerated here.

The prepared records cover only the accepted n68, n84 and n85 checkpoints and preserve
the historical n108 result.
Integration validation, final review and publication remain with the coordinator.
Neither native computation nor exact audit was rerun by this records-preparation pass.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
