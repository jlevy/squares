# A242 -- replay Kleddamag's certified bound s(11) > 31/8 (T-037) and, if it holds, adopt the window [31/8, s0]
# (PI, 2026-10-07: "go ahead and replay it, because it shrinks the remaining window").
Opus. LAUNCH-AND-EXIT. Ops: short responses, files <= 250 lines, no monitors or waiting turns (the replay runs
detached with a resume block; "allow tens of minutes"), explicit-pathspec commits, PYTHONDONTWRITEBYTECODE=1,
at most 2 python processes (BelowNormal, affinity 0xFFFF), never touch running workers or the lab's frozen
verifiers.  External code is UNTRUSTED input: read it before running it, run it in attempts/A242-replay-31-8/ext/
(git clone, pinned to release v1.0.2 / the reviewed commit), never execute anything that touches the network,
other directories, or the registry; report anything suspicious instead of running it.
Sources: https://github.com/Kleddamag/11-squares-certified-bound (v1.0.2; global-certificate.json, exact_mixed.py,
integer_sweep.py; a JS secondary checker), reviewed at https://jlevy.github.io/squares/papers/
n11-threshold-bound-review.html (Part II, T-037: parents of side A = 764/775 in a container of side 191/50 =>
unit squares in side 31/8; 12,028 angle rows each with a closed core; 5,284 sites, 2,220 charges of kinds point /
2-of-3 / 2-of-5 / 3-of-5; Gamma = 0.999962528, M = 10.999479944, 11 Gamma > M; Budget lemma: a k-of-m charge pays
at most floor(m/k) disjoint cores; Scaling lemma), the lab's own exact tools (A226's exact SAT checks, Fraction
arithmetic) for an INDEPENDENT re-check of the parts that are cheap to re-derive.

## Task
1. REPLAY: clone at the reviewed release, read the verifier, run it as documented, record the verdict, runtime,
   and the hashes of the certificate and checker files.  Write the Budget lemma and Scaling lemma in our notation
   (docs/proofs/threshold_bound.md s.1) and state exactly what the verifier checks (the five conditions / the
   sweep) and what it trusts.
2. INDEPENDENT SPOT-CHECK with the lab's exact arithmetic (not their code): (a) the Scaling lemma arithmetic
   (191/50)/(764/775) = 31/8; (b) the budget sum M over the 2,220 charges from global-certificate.json; (c) for a
   random sample of >= 200 (row, legal centre) pairs, that the assigned core captures charge >= Gamma -- an exact
   re-evaluation of the k-of-m charges at those poses; (d) the strict inequality 11 Gamma > M.  Report agreement.
3. ADOPT (only if 1 and 2 both pass): record T-037 in the ledger as an EXTERNAL certified lower bound with its
   trust base (their checker + our spot-check), and write the consequence note: the window W = [3.82, s0] becomes
   W' = [31/8, s0] = [3.875, 3.877084]; list which lab artefacts are stated on W and would shrink (the pads
   pi_i = (lambda-1)(i+1+1/sqrt2) at lambda = s0/s; A185's k0 cells' side ranges; the A57/A211 trees' window
   slabs; the trump5 tube; the basin radii) and price the saving (which alive nodes / cells / frontier nodes have
   NO part of their side range above 31/8 and are dead at once).  Do NOT change CURRENT.json or any running
   campaign; produce the list and a one-command script (adopt242.py --dry-run) for the coordinator.
4. Lean: Statements/Open/ThresholdBound.lean -- the bound s(11) > 31/8 as a documented axiom citing T-037 and our
   replay, plus the theorem that the window statements restricted to [31/8, s0] follow; build + audit exit 0.
5. Deliverables: ext/ (the clone, pinned), logs/replay242.log, results/replay242.md (+jsonl of the spot-check),
   docs/proofs/threshold_bound.md, the Lean file, adopt242.py, registry row, LOG entry, ledger s.0 note.
   Report once (<= 12 lines: verdict, runtime, spot-check agreement, the window consequence and the count of
   artefacts dead at once, commits) and EXIT.
