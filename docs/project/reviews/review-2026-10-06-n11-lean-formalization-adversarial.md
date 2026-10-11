# Adversarial Review: the Import of the Lean Formalization of Eleven-Square Optimality

> Retained verbatim by the importing lane (N11) from the reviewer’s final message of
> `claude -p --agent tbd-strong --model claude-opus-5-5`, run 19:05 to 19:14 UTC in a
> detached worktree at `22208da56`; the reviewer’s session could not write files, so it
> printed the review instead.
> The dispositions of its findings are in §9 of
> [the statement audit](review-2026-10-06-n11-lean-formalization-statement-audit.md#9-the-adversarial-review-and-its-dispositions).

**Date:** 2026-10-06. **Reviewer:** Claude Opus 5.5 (claude-opus-5-5), tbd-strong agent,
xhigh reasoning; AI adversarial review, separately prompted, no shared context with the
importing lane.
**Commit reviewed:** `22208da56` ("import: retain the 11SquaresFormalized
Lean proof of s(11) = T as T-060 evidence"), which imports
[Queuingtheorydotcom/11SquaresFormalized](https://github.com/Queuingtheorydotcom/11SquaresFormalized)
at `cdc746ed907d258057c283aeb6d077cb2c27e349`.

**In one line:** the formal statement is faithful to `T-060`, and every reader-facing
view says plainly that the proof is not kernel-only.
Two things block the import as recorded.
The evidence entry encodes a private, unobserved source run as `assurance: verified`
with `replay_status: passed`, against stage 3 of the import process and against every
other external entry in the register, and that encoding lets `V5` follow from a single
review. And the receipts behind “no kernel escape” come from one-off code that is not in
the repository and record less than the audit claims.

## 1. What Was Read and Run

**Read in full:** `epistemics.md` (Verification, Confirmation, Review Records, Results
by Others); `packing/campaign/result-import.md` stages 3 to 5;
`packing/frontier/README.md` lines 255 to 334; `T-060` in `results.yaml`;
`E-n011-lean-formalization-run`, `E-k2m4-evand-lean-report`,
`E-k2m3-evand-bentz-lean-build`, `E-chelokot-square-minus-two-lean`,
`E-n013-evand-casefree-cover-lean-kernel` and the two earlier n11 entries in
`evidence.yaml`; `V-queuingtheory-n11-lean`; the bibliography entry and its predecessor
`[Ahmed n11 optimality 2026]`; the coverage entry.
In the packet: the README and `acquisition/`; `Geometry.lean`, `Endpoint.lean`,
`EndpointBounds.lean`, `Foundations.lean`, `Optimality.lean`,
`Pending/S09_GlobalLowerBound.lean`, `Verification.lean`, `lakefile.lean`,
`lake-manifest.json` (the dependency pins), `lean-toolchain`, `.gitattributes`;
`README.md`, `MISSING.md`, `ASSEMBLY.md`, `PROVENANCE.md`, `ACKNOWLEDGEMENTS.md`,
`AGENTS.md`, `docs/PUBLICATION.md`, `docs/VERIFICATION_20261006.md`;
`verification/admissions.json` and the three `completed-run-20261006` files; and from
`scripts/`, the axiom parsing in `verify_support.py` (`native_axiom_owner`,
`audit_axioms`) and the checks in `finalize_verification.py` and
`verification_artifacts.py`. All receipts except the gzipped native-axiom list.
The statement audit.
The `README.md`, `SYNOPSIS.md` and `n-011.md` prose.
The derivation code in `packing/devtools/check_results.py` (`_machine_proof_shaped`,
`_formal`, `formalization_reviews`, `derive_verification`).

**Ran:**

| Command | Result |
| --- | --- |
| `git log --oneline -1`; `git show --stat HEAD` | `22208da56`, 79 files, no `.py` file under `packing/devtools/` or anywhere else |
| `git diff HEAD~1 HEAD -- README.md SYNOPSIS.md packing/frontier/n-011.md packing/resources/bibliography.yaml packing/frontier/results.yaml packing/frontier/verifiers.yaml` | The prose and register changes quoted below |
| `grep -rln --include=*.py -e tree-scan -e token_files_raw -e AuditN11Statement` over the worktree | No output: the program that wrote `tree-scan.json` and `axioms-public-theorems.json` is not in the repository |
| `grep -n -E "^  - id:\|origin: external\|replay_status: passed\|method: proof-assistant" packing/frontier/evidence.yaml` | `E-n011-lean-formalization-run` is the only `origin: external` entry with `replay_status: passed`. Every other proof-assistant entry with `assurance: verified` is `origin: replayed-here`, and the one external Lean entry, `E-k2m4-evand-lean-report`, is `assurance: reported`, `replay_status: not-attempted` |
| `grep -rn -e ManassehA06 -e "Square Packing Fan"` over the Markdown and YAML | Appears only in files this commit adds or changes |

**Could not run.** Each of these needed approval in this session, which was not given,
and I did not work around any of them.

- `.venv/bin/python3 -m devtools.check_results` from `packing/`. I read the derivation
  code instead (§3, finding 1).
- Writing a probe file in the Lean build directory, and so `lake env lean` there.
  I had written probes of name resolution, of `Packable 1 1`, and of a rotated square
  that excludes an axis-aligned corner.
- `zgrep` or `zcat` on `native-axioms.txt.gz`.
- `gh api search/code`, to identify the one raw `axiom` hit and the four raw `sorry`
  hits in `tree-scan.json`.
- Writing this file.

Everything Lean-specific in this review is therefore read, not executed.

## 2. Statement Fidelity: No Defect Found

Read against `T-060`’s claim (`results.yaml` lines 5177 to 5180):

- **The global statement.** `Optimality := Packable 11 T ∧ ∀ S, Packable 11 S → T ≤ S`
  (`Foundations.lean` line 13) is `IsLeast {S | Packable 11 S} T`, which is s(11) = T
  with the minimum attained.
  The audit checks this by `Iff.rfl` (`audit-statement.log` lines 1 to 2).
- **The objects.** `UnitSquare` (`Geometry.lean` lines 20 to 23) is a centre and an
  unrestricted real unit axis.
  `localX` and `localY` are coordinates in the orthonormal frame `(axis, perp axis)`, so
  every rotation is available, each square chooses its own, and reflection cannot matter
  for a square. `ClosedSquare` uses `≤ 1/2` on both coordinates, so the squares are
  closed with side 1. `OpenSquare` uses `< 1/2`, the interior.
  `InContainer` is the closed [0,S]². `contained` puts every point of every closed
  square in the container, which allows boundary contact.
  `interior_disjoint` forbids a common interior point for `i ≠ j`, which is exactly
  disjoint interiors; two coincident squares violate it.
  `side_nonneg` is implied by any packing and is harmless.
  `Point` is `ℝ × ℝ` with Mathlib’s `Prod` subtraction, and control 4a in
  `AuditN11Statement.lean` pins its meaning for an axis-aligned square.
- **Neither half is vacuous.** `construction_packable : Packable 11 T` was built here,
  on the three standard axioms only (`audit-statement.log` line 51). `¬ Packable 2 1`
  shows the lower half constrains.
- **Pressure points the definitions get right.** A `Packing` that was too weak, such as
  open-square containment, would make the upper half cheap.
  One that was too strong, such as disjoint closed squares, would make the lower half
  cheap. Neither shape is present.
- **The number.** `T := (6*u+4)/(1+2*u-u^2)` and `endpointPolynomial` match the register
  symbol for symbol and term for term (checked by `rfl`, `AuditN11Statement.lean` lines
  31 to 34). `u` is a root in `(rootLo, rootHi) ⊂ (9/25, 37/100)`, and `u_unique` holds
  on the closed interval, which is stronger than the register’s open one.
  `191/50 < T < U` with `U = 3.87708359002281417731` brackets the register’s decimal.
- **Name capture in the full environment.** In Lean 4, an identifier inside
  `namespace ElevenSquare` resolves to the innermost namespace match first, so a
  root-level `Optimality`, `Packable` or `T` elsewhere in the 7,920 modules cannot
  capture the names in `Optimality.lean`. A second `ElevenSquare.Optimality` would make
  the import fail. `Optimality.lean` has no `open`. Its theorem’s type is the constant
  `ElevenSquare.Optimality`, which the closure built here elaborated from bytes
  identical to the run’s, at the same toolchain and Mathlib.
  Instances or notation in later modules cannot change an already elaborated definition.
  Without the full environment, three things remain unchecked: an
  `export … (Optimality)` or `(T)` alias inside `namespace ElevenSquare` (the scan’s
  token list as written does not include `export`), the printed type of
  `ElevenSquare.optimality` itself, and the kernel re-check of imported `.olean` files
  (no `lean4checker` run anywhere).
  I could not confirm the resolution order by a Lean probe here (§1).

## 3. Findings

### Finding 1 — BLOCKING: an external, unobserved run is recorded as a passing verified replay, and that is what lets one review produce `V5`

**Where:** `packing/frontier/evidence.yaml` lines 761 (`assurance: verified`), 762
(`method: proof-assistant-checked`), 765 (`origin: external`) and 781
(`replay_status: passed`). The same reading carries into `results.yaml` lines 5245 to
5250 (`next_rung`) and the commit message ("one retained human expert formalization
review would derive V5").

**What is wrong:**

- **Stage 3 asks for a reported entry.** The audit’s header says it covers stages 1 to
  3\. `result-import.md` line 265, stage 3, says: “Record the claim as reported … a
  reported evidence entry.”
  Stage 4 adds: “A replay that passed in scratch space and was never committed did not
  happen”. The source’s run was not even observed here.
- **The frontier README keeps the two apart.** `packing/frontier/README.md` line 266
  says “External evidence and a local replay are recorded as separate entries”, and line
  279 says “Record `replay_status: passed` only after that replay succeeds”.
- **The register’s practice is uniform and the other way.** Every other
  `origin: external` entry in `evidence.yaml` carries no passing replay.
  The only other external Lean entry, `E-k2m4-evand-lean-report` (line 16254), is
  `assurance: reported`, `reported_method: proof-assistant-checked`,
  `replay_status: not-attempted`, and its build here is the separate `replayed-here`
  entry `E-k2m4-evand-bentz4-lean-build`.
- **The run cannot be inspected by anyone here.** `EvolvingPrograms/11SquaresEvolving`
  and run 37414883750 answered 404, as the packet README says at line 31. Its logs and
  compiled objects are not retained.
  What is retained is the integrator’s own JSON (`summary.json`,
  `independent-review.json`) and a final audit whose digest matches a digest that the
  same integrator wrote into `summary.json`. That digest match is consistency within the
  source’s own claims, not observation of a run.
- **The source’s own documents are mixed.** `verification/admissions.json` at the pin
  still reads `SOURCE_COMPLETE_REPLAY_PENDING`. `independent-review.json` records
  `"independent_lean_recompilation": false` and a fresh source assembly check with
  `"global_optimality_proved": false`. The run “reused validated receipts” from earlier
  runs (`MISSING.md`), and which modules it actually compiled is not recorded anywhere
  retained.

**Why it matters for the rungs.** `check_results.derive_verification` returns `V5` as
soon as one cited entry passes `_formal` (method `proof-assistant-checked`, a
certificate, a `replay`, `replay_status == "passed"`, an `axioms_receipt`) and one
accepting human formalization review exists (`check_results.py` lines 165 to 182 and 966
to 973). Under this encoding, the whole distance to `V5` is one review document.
The review’s `build` check could then only be ticked on the source’s self-report,
because no build of the lower half is retained here or anywhere public.
That is the “blind trust in a formal system” that epistemics.md → No Blind Trust rules
out.

I grant the counter-reading.
The `V3` row of epistemics.md admits evidence “of any origin”, and `V` “does not require
this project to have replayed anything”.
A source’s own passing run could count toward `V` under that reading.
But the record cannot pick that reading by encoding when the import process, the
frontier README and every precedent say otherwise.
It is a policy decision, and it is the owner’s.

**Proposed fix.** Re-encode the entry as the precedent does: `assurance: reported`,
`reported_method: proof-assistant-checked`, `replay_status: not-attempted`. Keep the
retained final-audit extract and the statement audit in `limitations`, or record the
statement audit as the entry’s `external_review`, as stage 4 records a read.
Rewrite `next_rung` so that `V5` needs a build of the full development recorded here as
a `replayed-here` entry with its own axiom receipt, or a third party’s retained build,
plus the human formalization review.
That build is also what `C5` needs.
If the owner instead rules that a source’s run with a retained final audit is enough for
`V`, write that rule into epistemics.md and the import process first.
Then the `next_rung` must still tell the formalization reviewer that the `build` check
rests on the source’s self-report unless they build it themselves.

### Finding 2 — BLOCKING: the “no kernel escape” receipts come from one-off code and record less than the audit claims

**Where:**
`packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/tree-scan.json`
lines 20 to 29; the statement audit §4, lines 100 to 124; the packet README lines 124 to
131; `receipts/lean/axioms-public-theorems.json`;
`receipts/lean/build-statement-closure.log`.

**What is wrong:**

- **No producer is retained.** No program that produced `tree-scan.json`, the axiom
  receipt, the native-axiom list or the closure build is in the repository (the `grep`
  in §1, and the commit adds no `.py` file).
  `OR-1` says never to leave a measurement in one-off code, and here no reader can
  re-derive any of the three receipts the audit stands on.
- **The receipt records only nonzero hits.** `tree-scan.json` holds counts for four
  tokens (`import_Lean`, `native_decide`, `sorry`, `axiom_decl`) and nothing for the
  others. It does not list the token set searched, the regexes, or the comment-and-string
  stripping rules. The audit’s §4 table nevertheless reports zero for 25 tokens, among
  them `opaque`, `csimp`, `ofReduceBool`, `trustCompiler`, `#exit`, `run_elab`,
  `run_meta`, `run_tac`, `initialize`, `infix`, `elab` and “environment modification”.
  No retained record supports those zeros.
  The packet README (line 128) and the audit (line 109) do not even list the same
  tokens.
- **The raw hits are not named.** The receipt counts 4 raw `sorry` files and 1 raw
  `axiom_decl` file but names none of them.
  “In comments” (audit lines 107 to 108) therefore cannot be checked, and a stripping
  bug cannot be ruled out.
  Lean nests block comments `/- /- -/ -/`, has char literals such as `'"'`, and has raw
  strings `r#"…"#`, any of which can defeat naive comment and string stripping.
- **The absence of `axiom` declarations is load-bearing, not a premise check.** The
  source’s finalizer accepts a native axiom by its name alone: `native_axiom_owner` in
  `scripts/verify_support.py` line 53 matches
  `(.+)\._native\.native_decide\.ax_[0-9]+_[0-9]+`. A hand-written
  `axiom <approvedOwner>._native.native_decide.ax_1_1 : False` would pass the final
  audit as an approved native axiom.
  Only the source scan excludes that.
  The audit calls the scan “a premise check beside the final audit’s axiom map, which is
  the decisive record” (lines 122 to 124). For this one property it is the other way
  round.
- **The build log is a filtered excerpt.** `build-statement-closure.log` has no
  commands, no check that the built bytes were the retained ones, no record of what the
  Mathlib pruning removed, and unexplained fragment lines
  (`import Mathlib.Basic.Real.Basic`, seven times, lines 9 to 51), probably truncated
  warnings.

**Proposed fix.** Commit a devtool, for example `devtools.scan_lean_archive`, that
streams the pinned archive.
It should record each token’s regex with its count, zeros included, and every raw hit’s
path, line and stripped-or-not status.
It should also do the per-module SHA-256 comparison and the extraction of the axiom
receipt and native list from the final audit, all from the pinned digest, with a
`--check` mode. Add the scan of `export`, attribute-registered elaborators (`@[tactic`,
`@[term_elab`, `@[command_elab`) and `addDecl`. Re-run it and regenerate the receipts.
Commit the closure-build driver and keep its full output.
Then correct §4 of the audit to cite only what the new receipt shows, and to say that
the absence of `axiom` declarations is load-bearing for the native-axiom audit.

### Finding 3 — NON-BLOCKING: crediting “Square Packing Fan” as an author rests on a post that names neither the repository nor the authors

**Where:** `packing/resources/bibliography.yaml` line 51 (`authors`), and the
attributions in `results.yaml` line 5289, `n-011.md` line 214 and the packet README
lines 11 to 12 and 25.

**What is wrong:** the retained post
(`receipts/announcement/tweet-2107508501610217640.json`) is “1/n” of a thread.
It links `jlevy.github.io/squares/cases/11.html`, not 11SquaresFormalized, and it says
the proof “has been formalized … thanks to Astra and Claude” without saying by whom.
`ACKNOWLEDGEMENTS.md` does not name Square Packing Fan or @ManassehA06. The predecessor
entry gives Ahmed’s X account as @MathCompSciFTW, so nothing retained connects
@ManassehA06 to this repository or to its authorship.
epistemics.md line 455 says credit is “read from the source’s own attribution files …
never inferred here”.

**Proposed fix.** Retain the rest of the thread if it links the repository and says who
did the work. Otherwise remove Square Packing Fan from `authors` and describe them only
as the poster of the announcement, until the source says otherwise.

### Finding 4 — NON-BLOCKING: `after Kleddamag` is not in the source’s attribution files

**Where:** `packing/resources/bibliography.yaml` line 56,
`credit: Ahmed et al. after Levy, Kleddamag, Daniel`.

**What is wrong:** `ACKNOWLEDGEMENTS.md` names what the formalization builds on:
jlevy/squares' exact formulas (Levy), Evan Daniel’s definitions and checker, and
wand125’s incorporated work, which the authors list already covers.
Trump’s packing is the subject, not a basis.
Kleddamag appears only in the post’s thanks “for aiding in the process”, the same
wording as for Levy, wand125, Guzhou0806 and ctjlewis.
The `after` is evidently carried over from 11SquaresOptimal’s credit line.
That is a chain through an author who is already listed first, not a link this source
names.

**Proposed fix.** Use `after Levy, Daniel`, or cite the source text that names Kleddamag
as a basis.

### Finding 5 — NON-BLOCKING: “complete build” and “states exactly” overstate in reader prose

**Where:** `README.md` lines 45 to 46; `SYNOPSIS.md` line 1775; `n-011.md` line 218;
`results.yaml` lines 5216 and 5295; `packing/frontier/source-coverage.yaml` line 55.

**What is wrong:** the run resumed from earlier runs’ receipts.
Its scope note reads “Resumed successful run” (`summary.json`), and `MISSING.md` says it
“must not be presented as a fresh full-build”.
“Complete build passed” reads as one fresh build of all 7,920 modules.
Separately, `README.md` line 45 asserts as fact that the theorem “states exactly s(11) =
T”, on the strength of an AI audit by the importing lane only.

**Proposed fix.** Write “its source’s full verification run, resumed from earlier
validated receipts, passed”.
In the README, write “which this project’s statement audit reads as exactly s(11) = T”.

### Finding 6 — NON-BLOCKING: what `V5` still needs is understated, and so is the owner question

**Where:** `results.yaml` lines 5245 to 5250; the statement audit §8, lines 208 to 223.

**What is wrong:**

- **The `build` check has nothing to read.** As finding 1 explains, the formalization
  review’s `build` item cannot be satisfied from anything retained.
  Neither text says so.
- **The owner question is wider than the audit puts it.** The audit leaves it to the
  owner whether being thanked “for aiding in the process” makes him an author.
  The epistemics indeed names no exception for or against him.
  But two facts weigh together.
  The post credits him with aiding this formalization.
  And the formalization’s exact `T` and construction come from his project’s formulas,
  which `ACKNOWLEDGEMENTS.md` credits.
  He would be attesting to the fidelity of a statement whose key input is his own.
- **The checker does not tie the review to this formalization.** `formalization_reviews`
  counts any accepting human formalization review on `T-060`, whichever formalization it
  read. That is a gap in the checker beyond this import, worth a bead.

**Proposed fix.** Add the `build` condition to `next_rung`. In §8, recommend a reviewer
outside both the post’s thanks and `ACKNOWLEDGEMENTS.md`, or require the owner’s record
to state both connections and that he built the proof himself.

### Finding 7 — NON-BLOCKING: the immediate dependencies of the public lower bound are not retained

**Where:** the scope in `acquisition/declaration.json`;
`Pending/S09_GlobalLowerBound.lean` lines 2 and 10 to 11.

**What is wrong:** `global_lower_bound` is one call,
`global_lower_bound_of_case438_certificate case438_near_certificate`, from
`ElevenSquare.Tasks.T07.UnfinishedCapture`. That module, and the one that defines the
function it calls, are pinned only by hash.
Their names ("Unfinished", “near certificate”) and the stale doc-comments (audit F-1)
are exactly what a reader will want to inspect.
The retained packet stops one step short of the lower bound’s proof.

**Proposed fix.** Retain those two modules, a few kilobytes at most, and say in the
packet README what they contain.

### Finding 8 — NON-BLOCKING: AI assistance and the trust model are stated correctly everywhere checked

This is recorded so the record shows it was checked; there is no defect.

- **Compiler trust.** Every view that mentions the formalization says that it trusts
  Lean’s compiler for `native_decide` and is not kernel-only: README, SYNOPSIS,
  `n-011.md`, the composition and notes of `T-060`, `VERIFIERS.md`, the evidence entry,
  the coverage entry and the packet.
  None says “standard axioms only” of the full theorem.
  The two places that use that phrase (`n-011.md` line 224 and audit §5) confine it to
  `construction_packable` and the closure.
- **AI assistance.** The post’s “thanks to Astra and Claude” is quoted in the case
  record, the register notes, the README and the SYNOPSIS. The packet README correctly
  says the repository’s own files make no statement of AI assistance.
- **The axiom receipt.** It is internally consistent: 13,311 = 13,308 + 3, the owner
  count equals the 10,464 occurrences, and the three certificate targets are strict
  subsets. It says plainly that nothing here re-ran `#print axioms` on the full proof.
- **The confirmation rung.** Nothing in the import raises `C`. `origin: external` is not
  a confirming origin, and the notes record the owner’s instruction to hold `C`.

## 4. Verdict

The formal statement is `T-060`’s claim, and the trust model is disclosed honestly in
every view. Finding 1 needs an owner decision, or a re-encoding, before this entry
stands: as recorded, it is an unsupported promotion of a private source run to a passing
verified replay, and it sets up `V5` on one review.
Finding 2 needs the scan, the receipt extraction and the build driver committed as
tools, and the receipts regenerated, before §4 of the audit can be relied on.

**Verdict: `defect-open`.**

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
