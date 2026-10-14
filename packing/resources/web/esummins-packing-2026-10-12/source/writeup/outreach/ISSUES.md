# Proposed issues for jlevy/squares — titles and first paragraphs (drafts; author only, nothing posted)

Shape: your result-registration template (`.github/ISSUE_TEMPLATE/result-registration.md`: Credit name / Claim /
Certificate / Checking / What the checkers share / Not done / Lineage and credit / AI assistance), as read in #503
and #485.  Each issue is self-contained, pins one commit of https://github.com/Esummins/packing, names the
retained package (`writeup/outreach/00-README.md` §4) and ends with "What we ask".  Order of posting: the
maintainer note, then 8 (a plain confirmation record), then 1, 6, 4, 2, 3, 5; 7 is attached to 1.  The PI decides
which to post.

## Note to the maintainer (one paragraph, posted with the first issue or sent separately)

Joshua — following the PI's earlier contact about the n = 11 lab, here is the set we promised: a structural
programme (stratification of packings by their simple squares), its n = 11 scoreboard with a Lean layer, one
conjecture stated for all n, the toolkit, a first climb at n = 17 and n = 19 that your machines could finish, a
dated timeline, and an independent replay of T-037.  Nothing claims a bound; the n = 11 value is yours (T-060,
T-112).  The repository is public at https://github.com/Esummins/packing and every claim is tagged and sourced so
your intake can retain a packet and pin a commit; we will follow your import process (one issue per result, your
replies on the issue) and will not open pull requests.  The series index is `writeup/outreach/00-README.md`.
— E. Summins (PI), with the lab's AI agents (Claude); AI assistance is stated in each issue.

## Issue 1 — "Simple-square stratification of s(n): proof strategy, n = 11 scoreboard and Lean layer: registration request"

**Credit name.** E. Summins (PI), n = 11 lab; AI-assisted (Claude, Anthropic) under the PI's direction.
**Claim.** Not a bound.  A proof strategy for your catalogue (`packing/frontier/proof-strategies.yaml`, kind proof):
stratify packings by the D4-class of their lattice-slot skeleton (Young 4-tuples), kill classes on a side window by
exact per-class certificates and geometric trees, climb containment by Lemma K1.  At n = 11: a census of 1110
tuples / 163 classes exhaustive at every side in (3, 4) (Lean theorem, standard axioms), **52 of 52 k5/k6 classes
certified empty on the whole window [191/50, s0]** (parametric certificates, frozen verifier sha256 521cb01fe656…),
the k ≥ 6 tier empty, and a residue of three k = 5 classes, sixteen K1-protected classes and k = 0.  The record of
what is theorem and what is axiom is `lean/AUDIT.md` (three named open axioms).  Details:
`writeup/outreach/01-stratification-program.md`; timeline `07-timeline.md`.
**Certificate / Checking.** `attempts/A56-sparametric/results/scoreboard.json` and the certificates it names;
`attempts/A57-shadow-trees/code/verify_case.py` (stdlib + Fraction; ~seconds per certificate); Lean
`case_verifier_kill` byte-faithful to it.  **What the checkers share.** One author (the lab), the frozen verifier and
its Lean twin share the decision core by construction; the census was re-enumerated independently (A72).
**Not done.** k5_11 / k5_16 not closed on the window (A270 open slabs); the protected tier and k0 open; no tree-node
verifier clause (tree kills are exact-rational traces, `05-toolkit.md` §6).
**What we ask.** Register the strategy; tell us your vocabulary for pins / stratum kills / pads.

## Issue 2 — "Forced double meeters on the simple-square ladder (Theorem FC, SLOT-CROWD) and the forced-cell traction finding: registration request"

**Claim.** [T] Theorem FC / Lemma SLOT-CROWD (any n): a packing containing the pins of a class S but not those of
a closed extension S ∪ {p} meets p's slot box with two distinct non-pin squares (the lone meeter teleports); on the
dilated page the widened box carries pad π_i = (λ_max − 1)(i + 1 + 1/√2).  [M] every geometric rule of the toolkit
acts on such forced cells, so a class's traction = its closed one-slot extensions (corners4: 0 of 8 at n = 11);
[M] on k4_11, A100's LP-unkillable cells die at the root by geometry in 13–16 s.  [F] "all extensions dead ⇒ class
dead" is unsound (K1 climbs up).  Exact statements of ONE-TILTED, WEDGED-SEAL, EPS, SNAP with Lean names.
Details: `writeup/outreach/02-ladder-requirements.md`.  **Certificate.** `attempts/A238-k4-benchmark/results/`,
`attempts/A241-row-cascade/results/rows241.md`; Lean `slot_crowd_stmt`, `fc_transfer_stmt`, `snap_dead`, `gate`.
**Not done.** The row cascade's parametric re-expression of A55's k4 kills failed on our machine (PARAM-FAIL / timeouts).
**What we ask.** A k-of-m charge that prices "two distinct non-pin meeters of one box"; the row cascade on a bigger machine.

## Issue 3 — "k = 0 at n = 11: the no-simple-square class — theorems, refuted routes with witnesses, measured facts: registration request"

**Claim.** [T] K0-FREE, SWAP / CELLS (Lean, standard axioms); [T] the extremal reduction: for every n with
s(n) < ⌈√n⌉ some optimal packing has a flush corner unless a Ψ-minimal optimum is a four-crowd with all eight corner
meeters locked (residue LOCKED-CROWD-FREE(n), Lean `no_retreat_of_psiMin`); [F] ten routes refuted with explicit
witnesses (torque sign rule, 12 > 11 count, sweep count, click monotonicity, capacity counts / NO-CLOSURE,
handedness sums, OPPOSE, tilt floors, local charges, pocket waste); [M] 0 of 883 free Fritz-John points are
four-crowds; no teleport-stuck packing below 4.0014; every four-crowd witness has an improving corner swap; crowd
rings below 4 hold one square.  The n = 11 form STEP on the eleven converged-alive cells (swap-leaf verifier) and the
normal-ring chain with its open links.  Details: `writeup/outreach/03-k0-status.md`.
**Not done.** k0_00 is not closed; several certificate chains are [T-computed*] (resumable).
**What we ask.** A field certificate conditioned on four doubly-met corners on [31/8, s0]; the chains `pair3` / STRIP₂.

## Issue 4 — "Conjecture ONE-FLUSH(n): every optimal packing below ⌈√n⌉ has a singly-met corner — statement, equivalences, evidence: registration request"

**Claim.** A conjecture, not a result.  For every n with s(n) < ⌈√n⌉, some optimal packing has a corner box met by
≤ 1 square (equivalently s(n) is attained with a flush corner square; equivalently UNCROWD(n) / RAISE(0 → 1) at the
optimum — equivalences [T], Lean `OneFlush.lean`, `RingSwap.lean`).  Reduced [T] to LOCKED-CROWD-FREE(n)
(`LocalLock.lean`); supported [M] by the 21-record survey (all have ≥ 3 flush corners; Trump the only doubly-met
corner) and the k0 measurements; every local or counting proof route is refuted [F] with a witness (CROWD-ABOVE:
four-crowds exist at O(ε) above every record).  Why it matters: it lets every stratified search start at k ≥ 1.
Details: `writeup/outreach/04-simple-square-conjecture.md`.
**What we ask.** A threshold-type certificate conditioned on four doubly-met corners (n = 11 first, then a family
indexed by n); any angle from the charge machinery on LOCKED-CROWD-FREE(n).  We supply the witnesses, the Lean
equivalences and the exact tools.

## Issue 5 — "Geometry-before-LP toolkit for stratum trees (exact-rational leaf rules, 7.2× on closed nodes): registration request"

**Claim.** A toolkit, not a bound: closed-form stage 0, a CSP on pieces, multibox cores K′ and clip cascade, leaf
rules (corner cover, no-room with lane and pocket-rooted covers, named split, role split, pocket branching, SNAP,
EPS), inheritance across runs and start-node shards, integer polycore and C kernels; [M] 7.22× geometric mean on
11 closed nodes (A215), 5.0× on no-room nodes (A221), 0 regressions over 314 replayed rows.  Each rule's soundness is
an n-general prose lemma in `docs/proofs/`; the frozen verifiers and their Lean twins are listed with hashes.
Details: `writeup/outreach/05-toolkit.md`.  **Not done.** No verifier clause for a tree node (kills are exact traces);
the tree-file → cover check in Lean.  **What we ask.** A review of one leaf rule end to end; whether a sqverify-fast
style exact sweep can replace our lane cover.

## Issue 6 — "The simple-square climb at n = 17 and n = 19 (2,500-class census at T-043/T-065 and T-103 windows; k = 16, 15 dead at the root): compute request"

**Claim.** [T] the census of slot-set classes at your windows for n = 17 (s ∈ [116511/25000, 4675531/10⁶]) and
n = 19 ([193/40, 4885619/10⁶]) has 2,500 classes, 632 with four corners; [C: exact trace] at n = 17 every four-corner
class with k = 16 (17) and k = 15 (35) is empty on the window, proved at the tree root; k = 14: 67 of 68; k = 13
running; the record classes `n17_k08_0156` (Bidwell) and `n19_k11_0236` are the canaries and are first-order rigid
[M].  The climb rule is Lemma K1 run forward (Theorem FC's dichotomy as a spine node + cited closed extensions).
Details: `writeup/outreach/06-climb-17-19.md`.
**Certificate.** `attempts/A243-climb-17-19/{results/verdicts243_n17.jsonl,certs/n17/}` (276 spine certificates).
**Checking.** `python attempts/A243-climb-17-19/code/run243.py 17 <class> --wall 1800`; exact rationals; ~0.1–600 s per class.
**Not done.** k ≤ 13 at n = 17, all of n = 19, the climb from the four-corner root; no verifier clause for tree kills.
**What we ask.** Run the descent to the record's k and the climb on a larger machine; inputs and resume table supplied.

## Issue 8 — "Independent replay of T-037 (Kleddamag s(11) > 31/8, v1.0.2): confirmation record"

**Claim.** No new result.  We replayed T-037's exact Python sweep in full at the pinned release (12,028/12,028 rows,
0 differ from the retained evidence, minimum Γ = 0.999962528, budget M = 10.999479944, 11Γ − M = 107864·10⁻⁹),
re-ran the stdlib controls and the integrity check (54 files, twice), and spot-checked the premises in our own exact
arithmetic (scaling 191/50 ÷ 764/775 = 31/8; the D4-expanded budget; 3,240 exact poses, 0 failures; the strict
counting).  **Certificate.** `attempts/A242-replay-31-8/results/{replay242.md,replay242.json,spot242.json}`;
certificate sha256 57e9927d…cd44458.  **What the checkers share.** The row replay is the author's own code
(`same-implementation`); the spot-check shares nothing with it.  **Not done.** Their secondary JavaScript checker
(downloads an upstream file at run time; refused for network reasons).  **A note for the packet.**
`verify_threshold_algebra.py` rewrote a pinned file with CRLF on a Windows checkout; restored, integrity PASS.
Details: `writeup/outreach/08-t037-replay.md`.  **What we ask.** Retain beside T-037 if useful.

## AI assistance (every issue)

The lab's campaigns, code, certificates, Lean files and these notes were produced by AI agents (Claude, Anthropic)
under the PI's direction and readings; every number is read off a committed artefact; the executable evidence and
the stated trust bases, not the prose, are the basis offered for review.
