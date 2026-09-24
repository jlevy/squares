# Review of the Closed Rung-0 Tree, 24 September 2026

A W2 factual review (Fable, max thinking; agenda-042 BC-381, bead `think-6w2y`) of the
closed certificate tree behind
[H-236](../../../packing/campaign/hypotheses/H-236-n11-fixed-angle-global-optimality-at-trump.md),
recorded in
[exp-231](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-231-h236-rung-zero-cell-tree.md)
and
[exp-232](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-232-h236-rung-zero-closed.md).
The [contract review of 23 September](review-2026-09-23-rung0-certificate-contract.md)
verified the instrument’s six obligations and set the conditions under which a closed
verdict confirms H-236; this review checks that those conditions are met by the tree as
it exists, re-replays part of it independently, and says what the result is and is not.
The tree (7.8 GB, 257 files) lives in the Session 156 worktree’s `attic/rung0/`, outside
the record, with a SHA-256 manifest retained in the record.

## Verdict

**Accept, with the scope split.** Every closure condition holds, the reader’s verdict
reproduces on an independent re-replay through the reader’s own per-subtree path, and
the statement fields the reader does not check (the box, the image, the radius) verify
against `cases/trump11/packing.py` by this review’s own computation.

What the tree proves outright, with no pending dependency, is a machine-verified
reduction: every packing in the family with side at most $U_{hi}$ lies, after the
declared turn and relabelling, strictly within BC-240’s radius of Trump’s labelled
image.
H-236’s optimality and equality statement is that reduction composed with BC-240’s
first two clauses, which are still awaiting the source-distinct BC-241 review (BC-382).
By the predicates in [`epistemics.md`](../../../epistemics.md) the reduction supports
`V4/C3` now; the composed theorem takes BC-240’s rung until BC-241 closes.

## The Closure Conditions

| Condition | Held | Evidence |
| --- | --- | --- |
| Verdict `closed`, no unresolved leaf | yes | `h236-reader-final2.json`: `verdict: closed`, `unresolved_by_reason: {}`; leaves b 19,883,887, c 21,834,304, f 97,722,555, t 3, s 256. The retained copy `exp-232-h236-reader-final2.json.gz` decompresses to the same bytes (SHA-256 `1a04c97a…`). |
| At least one Trump-degenerate leaf | yes | Three, in subtrees 93, 109 and 117; each re-replayed here with one `t` leaf. |
| `target_is_at_least_U: true` | yes | Reader field true; this review recomputed $U$ to 60 digits from the witness field: the header’s upper end exceeds $U$ by $2.03\times10^{-45}$, and the closed form $(6u+4)/(1+2u-u^2)$ the reader brackets equals `packing.py`’s side exactly. |
| Declared box covers the registered box | yes, exactly | Declared $[91442076901/250000000000,\ 73154061521/200000000000]$; with $u$ isolated to $10^{-60}$, the left end is $6.8\times10^{-13}$ below $u_{lo}-10^{-6}$ and the right end $3.2\times10^{-13}$ above $u_{hi}+10^{-6}$, and both equal the declared floor/ceil recipe at $10^{-12}$. The reader does not perform this comparison; it is this review’s. |
| Reader bytes unchanged | yes | `git hash-object` of the working tree and the `HEAD` blob: `c4ae4e489fcf…`, the digest in `FROZEN.txt` before and after Amendment 1. |
| Producer bytes per surviving file | yes, with one nuance | 167 files carry `extra.resumed: true` and were written by the Amendment 1 bytes `9c92406…` (the `HEAD` blob): R1 wrote 88 (mtimes 09:41–12:02Z, header wall cap 10,843 s), R3 21 (15:49–18:57Z, 11,408 s), R4 58 (06:43–10:42Z on the 24th, 21,700 s). The other 89 were written by the frozen run M1 (08:20–09:11Z, cap 3,300 s) with the pre-amendment bytes `af1179a5…`; the attic copy hashes to that digest and differs from Amendment 1 by 99 added and 0 removed lines. No file falls outside the four windows. |
| No stitched or partial file | yes | No `.part` file survives; the 256 names are exactly `sub-00000` to `sub-00255`; every subtree header matches the top tree on every key the reader compares and its `root_path` equals the frontier cell the reader’s own walk of the top tree assigns to that index; the amended producer writes to `.part` and renames only on completion, never stitches. |
| The reader replayed these files | yes | The reader opens `h236.sub/sub-NNNNN.jsonl.gz` for the 256 frontier indices; the verdict (11:23Z on the 24th) postdates the last subtree write (10:42Z), and the retained manifest hashes the same 256 files plus the top tree, `FROZEN.txt` and the verdict. |

The 13 tests in `packing/tests/test_fixed_angle_tree.py` pass under the project
interpreter; the frozen copy of the test file already contained the tampering test.

## The Re-replay

`attic/review-rung0-closed/replay_sample.py` calls the frozen reader’s `replay_subtree`
exactly as `replay()` does, three workers, and appends one line per subtree.
The top tree replayed first (102 branches, 16 dual-bound and 39 Farkas leaves, 256
frontier leaves, nothing unresolved).
Subtrees were taken in this order: the three Trump-degenerate subtrees, the heaviest
subtree 128 (471 MB, 7,987,265 nodes), a seeded sample stratified by producer run (50
and 90 from M1, 138 and 157 from R1, 177 and 190 from R3, 244 from R4), then the rest
heaviest-first.

REPLAY_RESULTS

## Scope

**What H-236 now states.** In the family of eleven unit squares with six at orientation
$0$ and five sharing one orientation modulo $\pi/2$ whose half-tangent lies in the
declared box, every packing has side at least $U$, and equality holds only on the
$\mathbb Z/4\times S_6\times S_5$ orbit of Trump’s pose.
Reflections are not in the family: they send the tilt to $\pi/2-\theta^*$, whose
half-tangent $0.464$ is outside the box, so the orbit is the whole equality set.

**Where BC-240 enters.** Only at the three `t` leaves.
This review re-derived the step the contract review asserted: undoing the quarter turn
about the container’s centre carries a leaf’s packing at side $s'\le U$ to a translate
by $(0, U-s')$ inside $[0,U]^2$, a sup-norm isometry on centre differences, so BC-240’s
first clause forces it to be Trump’s labelled pose and the four wall contacts force
$s'=U$. The angle window reaches $2.0\times10^{-6}$ radians, below $\rho_{row}=0.00404$.
The declared image (rotation 1, labels `[3,4,2,5,0,1,8,10,6,9,7]`) satisfies every
symmetry row strictly and is the only turn with both centroid offsets positive, so the
row-satisfying element of Trump’s orbit is unique and must sit in a `t` leaf, which it
does.

**What it does not say.** Nothing about any tilt outside a window $2\times10^{-6}$ wide
in the half-tangent, hence nothing about H-112’s full family or about $s(11)$; nothing
about packings whose orientation classes are not six plus five; nothing beyond the
labelled, anchored chart BC-240 uses.
The trust base is `cases/trump11/packing.py`, `sqpack.field.NumberField`, Python’s
`Fraction`, and the gzip and JSON readers, shared by producer and reader.

**The n = 11 negative control** remains producer-level: the full tree at $U+10^{-3}$
stopped at its cap of 100,000 nodes with 57 unresolved leaves, every one of them
`node-cap` rather than `open`, and the Trump-cell control (one `open` leaf at LP value
3.877081) has no reader verdict because the reader refuses a non-root cell.
This is a stated limitation, not a blocker.
The reader has no LP solver, so it can never certify that a cell is open; what a
negative control guards against is a reader that accepts what it should refuse, and that
is covered by reader-checked controls that fail for the right reason
(`control-axis-5-above` returns `incomplete` with an `open` leaf; `control-n5-capture`
closes only as a capture, `capture_only: true`) and by the tampering test in the
retained test file. A node-cap stop at $U+10^{-3}$ would be uninformative even if
reader-checked, since the tree at $U$ itself needed $1.7\times10^{8}$ nodes.
H-236’s registered criterion asks the reader to accept the certificate and the negative
control not to close; both are met as written.

## Registration

**Exact claim, the reduction (registrable now).** Every packing of eleven unit squares
in a square container, six at orientation $0$ and five sharing one orientation modulo
$\pi/2$ with half-tangent in $[91442076901/250000000000,\ 73154061521/200000000000]$ (an
interval containing $[t^*-10^{-6},\ t^*+10^{-6}]$ for Trump’s exact half-tangent
$t^*=0.365769307604677\ldots$), whose side is at most the rational $U_{hi}$ of the
certificate header ($U_{hi}-U=2.03\times10^{-45}$), lies, after the quarter turn that
puts its tilted centroid in the closed upper-right quadrant and the relabelling that
orders each class by $x+y/4$, strictly within $\rho=808514697/200000000000$ of Trump’s
labelled image (rotation 1, labels `[3,4,2,5,0,1,8,10,6,9,7]`) in every centre
coordinate, with every tilted orientation within $2.0\times10^{-6}$ radians of Trump’s;
every other packing in the family has side greater than $U_{hi}$.

**Exact claim, H-236 (the reduction composed with BC-240).** Every packing in that
family has container side at least $U=3.877083590022814\ldots$, the exact side of
Trump’s packing, and a packing in the family has side exactly $U$ only if it is a
quarter-turn image of Trump’s pose with the squares relabelled within the two classes.

**Verification and confirmation, predicate by predicate.** The reduction’s evidence is
repository-origin, `method: exact-algebraic`, with a certificate (the manifest-pinned
tree), a replay command (the reader) and `replay_status: passed`, so the checker’s
`_machine_proof_shaped` predicate holds and derives `V4`; with `origin: replayed-here`
it derives `C3`, and `C5` once a mapped review artifact exists.
The results checker resolves `artifacts`, `controls` and `review_artifact` paths but not
`certificate`, so an off-record certificate does not fail it; the manifest and the
verdict are what make the entry auditable, and the limitations field must say the tree
is off-record. `C3` also needs a retained control path:
`packing/tests/test_fixed_angle_tree.py`. H-236 itself is compound; its minimum is the
BC-240 part, which has no register entry, is a proof packet awaiting its audit (so not
`V3`), and whose radius generator has not been independently replayed (so not `C2`).
Literally that is `V0/C0` with a `composition` note today, and `V3` with `C3` or better
(`C5` with the reviews mapped) when BC-241 closes with a passing radius replay.
Registering the reduction now and the composed theorem on BC-241’s return is the reading
that neither promotes nor understates.

**Significance** `S3`: a substantive case result and machine audit, the first optimality
statement with an equality case for a family containing Trump’s packing; it moves no
bound on $s(11)$, and its cost ($1.7\times10^{8}$ nodes for one box) argues against
`S4`’s reusable technique.

**Novelty** `apparently-novel`, with the narrow object stated as above.
Corpus: the repository’s recorded literature (the resources README, the n = 11 research
bundle’s files 12, 15 and 16, `frontier/n-011.md`, Stromquist 1984 and 2003, Friedman’s
DS7). Nearest prior: Stromquist 2003’s bound $2+\tfrac43\sqrt2\approx3.885618$ for
packings restricted to $0°$ and $45°$, an earlier restricted-orientation lower bound at
n = 11 that is not attained and does not contain Trump’s packing.
So X-046’s and exp-232’s phrase “the first global optimality statement in any n = 11
family” should be narrowed to “the first optimality statement with an equality case”.
Gap: this review performed no external search.

**What the entry must carry.** `claim` in full; `scope: {n_values: [11]}`; the derived
`V`/`C`; a `composition` note naming the BC-240 part; `evidence` pointing at an entry
with `claim: derived-structure` (keeping `witness-optimality` for $s(n)$ itself),
`method: exact-algebraic`, `performed_by: repository`,
`relationship_to_generator: independent-implementation`, `origin: replayed-here`,
`certificate` naming the archived tree and its manifest, `replay` the reader command,
`replay_status: passed`, a `proof` block citing the contract review for the relaxation’s
soundness and the symmetry lemma, `novelty_basis`, and `limitations` (off-record
certificate, shared trust base, producer-level n = 11 negative control, the angle
window); `artifacts` in the record (`exp-232-h236-reader-final2.json.gz`,
`exp-232-h236-tree-manifest.sha256`, `exp-232-h236-frozen.txt`, the producer, the
reader, exp-232, and for the composed theorem `isolation-theorem.md`); `controls`; and
`review_artifact` mapped in `document-map.yaml` for `C5`.

## Findings to Carry Into the Record

| Severity | Finding |
| --- | --- |
| minor | The reader does not compare the declared box with the registered $\pm10^{-6}$; the register must cite this review’s computation, or the reader should gain the check. |
| minor | 89 surviving subtree files were written by the pre-amendment bytes `af1179a5…`, not Amendment 1; the record should say so rather than “Amendment 1 for every run”. The difference is 99 added lines and none removed. |
| minor | The tree manifest `exp-232-h236-tree-manifest.sha256` is untracked at the time of this review; it must be committed with the entry. This review verified it in place: `shasum -a 256 -c` over `attic/rung0` returns OK for all 259 entries (the 256 subtree files, the top tree, `FROZEN.txt` and the verdict). |
| minor | “First global optimality statement in any n = 11 family” overstates against Stromquist’s $0°/45°$ bound; narrow it as above. |
| minor | The n = 11 negative control is producer-level only; a stated limitation, for the reasons in Scope. |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
