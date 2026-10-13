# Independent Operational Review: BC329 Three-Profile Run Sheet

**Verdict: REFUSE execution and operational admission from this snapshot.** The sheet
has the right target-free scope, literal CLI shape, and prospective gates, but its
post-coordinator readback and retention steps do not yet prove the complete evidence
claim. The integrated implementation is also not at an eligible, commonly accepted PR
head.

## Review Boundary

- Entry point: read-only operational review of the run sheet and CLI contracts.
  No calibration profile, BC329 target, repository edit, bead action, or PR mutation was
  performed.
- Sheet:
  `docs/project/specs/archive/plan-2026-09-13-n11-bc329-three-profile-run-sheet.md` in
  `/private/tmp/squares-n11-bc329-stack`, SHA-256
  `0cd2eb288dac4701de7d5eb5700d2890597d3c78750150e706156ac870da3b6e`. All sheet line
  numbers below refer to those exact bytes.
- Local stack HEAD at review: `fc3e314daaeb1cb07705ce4a44ae682e80eafa6a`. Live PR 156
  head returned by `gh pr view` at 2026-09-13 18:17 UTC:
  `52e4ab65ad4581421a1005a91d3f7d76e802acad`. The stack checkout was dirty: the sheet
  was untracked and the reader and its tests had concurrent edits.
  This report does not judge those unfinished edits or infer that prior source refusals
  persist after repair.
- Reviewed context: `AGENTS.md`, the preceding run-sheet review, the September 13
  topology/coordinator reviews, the September 13 source-distinct reader review, and the
  current coordinator, producer, and reader CLI source.
  The older reviews are exact-revision findings, not verdicts on the concurrent working
  tree.

## What Checks Out

- Concatenated fenced Bash blocks passed `bash -n`. The coordinator `run` parser accepts
  the sheet’s exact flags, three cache observations, and three background-load
  observations. The reader parser accepts its five flags.
  The coordinator code creates three fresh sequential profiles, retains exact internal
  argv/status/stdout/stderr, measures command-return wall time, performs immediate
  producer and inventory readback, and validates an atomically published summary.
- The macOS arm64 shape in the sheet matches both current producer and coordinator
  formulas: four requested workers, effective raw/exact workers $4/4$, and effective
  reflected-interval/dilation workers $1/1$. The command uses the frozen
  `4 / 5400 / 7200 / 2` tuple.
  The frozen fixture is 935 bytes and its measured SHA-256 is the stated
  `1aface38ab79526397b7b9f24325df844e2eb9717d3e29a094fcdefe8822f539`.
- Direction accounting is exact: $2881 + 2881 + 5761 + 2881 = 14{,}404$ retained
  direction rows per profile.
  Dense/slab share the normalized-exact row.
  The sheet explicitly refuses missing, wrong, or duplicate labels and wrong known
  answers.
- The preflight checks the live PR head, local HEAD, clean tree, Python 3.14 virtual
  environment, uv floor, fixture bytes, platform, and fresh external roots.
  The sibling review root keeps later reader output outside the immutable run root.
  The host snapshot uses `comm=`, so it does not retain process arguments.
- The gate table is substantially candid: the producer still needs integrated-head
  review; the coordinator’s three later findings and the reader’s independent refusal
  remain pending; the sheet does not claim positive profiles or BC329 execution.

## Findings Requiring Repair

### R1 — A failed source-distinct profile does not stop the reader sequence

Lines 211–251 disable `errexit` for all three reader commands and defer all status tests
until after profile 3. If profile 1 refuses, profiles 2 and 3 still run.
That contradicts the sheet’s stop-on-refusal rule and complicates the evidence trail.
Record each status immediately, then test it before launching the next reader.
The first nonzero reader status must terminate this run-set’s admission path while
keeping the refused root and logs.

### R2 — The retained reader outputs are not checked against the admitted run set

Lines 211–251 require only exit status zero.
They do not parse the reader’s accepted JSON proof or compare its `execution_revision`,
`reader_revision`, `run_order`, `profile_directory`, invocation identity, and receipt
digest/byte count to the coordinator’s summary.
They also do not retain an exact argv record for these three external reader
invocations, although line 282 says to refuse a changed reader command.
The current reader CLI returns those binding fields in its proof.

Add a maintained post-readback admission step that duplicate-key-safely parses each
proof, requires `status: accepted`, compares its identity and receipt binding to the
corresponding summary run, records the exact reader argv and status, and refuses a
missing, extra, malformed, or mismatched proof.
Keep its output in `REVIEW_ROOT`. This check does not replace independent acceptance of
the reader’s source bytes.

### R3 — Run-root immutability is stated but not established at retention

Lines 191 and 282–284 require unchanged run artifacts after the coordinator returns.
Lines 333–345 copy the summary, archive the run root, and hash that archive, but no step
captures a byte/type inventory at coordinator return or compares it after the three
source-distinct reads and before/after archiving.
The archive hash proves only that the archived bytes did not change after hashing; it
cannot prove they are the bytes admitted by the coordinator or source-distinct readers.
A changed top-level coordinator record is outside the single-profile reader’s scope.

Capture an exact run-root inventory immediately after coordinator success, outside
`RUN_ROOT`: relative path, regular-file type, byte count, and digest for every file.
Compare it before the reader sequence, before archiving, and against an extracted or
streamed archive inventory.
Refuse any added, removed, replaced, or changed artifact; recheck the copied summary
against the same inventory.
Keep the manifest with the retained evidence.
A maintained verifier is preferable because this is an admission measurement, not a
one-off checksum of the final tarball.

### R4 — The final source-freeze check covers only three files

Lines 348–357 check `git diff` for producer, coordinator, and reader modules, then say
the evidence commit must not change *any* source path bound by a profile receipt.
The producer’s source manifest includes the generic packet module, mathematical helpers,
package initializers, runtime declarations, lockfile, and fixture beyond those three
modules. The literal check therefore does not implement the stated source-closure rule.

Before the evidence commit, compare the complete manifest path set and blob IDs from all
three accepted receipts to `EXECUTION_REV` and to the intended evidence commit’s tree.
Refuse a source-path addition, deletion, or change, including runtime declarations.
The sheet should name the exact maintained verification command or literal read-only Git
check used for that comparison.

### R5 — Current admission gates prohibit the coordinator now

At the review snapshot, local HEAD differs from live PR 156 head, the sheet is
untracked, the reader has uncommitted edits, and the table at lines 19–33 leaves
producer integration, topology/coordinator, reader, sheet, and remote-identity gates
open. The September 13 coordinator rereview at `fc3e314d` refused inverted route
chronology, oversized phase time, and the second `result.json` read.
The reader review at `212e0dfc` refused full source closure, running-reader identity,
witness agreement, typed fields, dilation fields, and lifecycle/topology contradictions;
it also identified exceptional-number paths that did not take the declared refusal exit.
These are precise prior-review scopes.
The current table groups the main defects truthfully, but should mention the
exceptional-number refusal path under the reader row so no known open class disappears
from the admission checklist.

Commit and integrate the repairs and sheet, obtain independent acceptance of the exact
resulting head for each gate, then re-run the executable PR-head and clean-tree checks.
A prior ancestor acceptance cannot admit the integrated resolution.
This finding is a present execution gate, independent of R1–R4’s sheet repairs.

## Operational Disposition

Keep the `4 / 5400 / 7200 / 2` tuple and 14,404-row shape as proposed until an
exact-head admission disposition freezes them.
Repair R1–R4 in the sheet and any maintained verification support, then have the revised
sheet reviewed at the same clean PR head as the producer, coordinator, and
source-distinct reader.
Run no positive profile or BC329 target on this snapshot.
A refusal supplies operational evidence only; it does not decide BC329 mathematics or
performance.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
