# The simple-square stratification — an outreach series for the Squares Project (jlevy/squares)

**Abstract.** Eight self-contained notes from the n = 11 lab of E. Summins (PI) to the Squares Project: a
structural programme for s(n) — stratify packings by their simple (lattice-slot) squares, kill strata on a side
window, climb the ladder of strata by forced double meeters — with its n = 11 scoreboard, its lemmas, its one
conjecture (ONE-FLUSH(n)), its toolkit, its first run at n = 17 and n = 19, its dated timeline, and an independent
replay of your T-037.  Each note ends with "What we ask": compute on the climb, proofs of the conjecture, and
registration of the strategy.  Every mathematical claim is tagged and sourced; nothing here claims s(11).

Repository: **https://github.com/Esummins/packing** (public; files cited as `blob/master/<path>`).
Licence: code MIT, documents and data CC BY 4.0 (LICENSE at the repository root).  Author only — these notes are drafts for the PI; nothing has been
posted.  Tags shared with your record: **[T]** proved in prose (Lean name given where one exists), **[M]** measured
(run cited), **[F]** refuted (witness given), **[C]** obligation / conjecture / certificate-backed as stated; the
lab's own status sheet (`writeup/05_status_sheet.md`) adds [L] Lean-checked and [P] priced.

## 1. The PI's framing

> "What I was pursuing was a program to gain deeper insight into the square packing problem for all n; the
> solutions posted seem in many ways to be refinements of a general search that don't tell us much about the
> underlying STRUCTURE.  I want to push the investigation in a more constructive direction."

Your record now holds s(11) = T (T-060, V3/C3/S5) and uniqueness (T-112); T-037 (s(11) > 31/8) was the verified
bound before them.  The lab's n = 11 work — a certified window scoreboard, a Lean layer with three named open
axioms, a residue of three k = 5 classes, sixteen protected classes and k = 0 — is therefore offered as a
STRUCTURAL programme and a set of n-general lemmas, with n = 11 as the worked instance, and n = 17 / 19 as the
first climb.  Your machines are larger than ours; each piece names what to run and what to prove, with inputs.

## 2. The series

| # | file | what it is | the ask |
|---|---|---|---|
| 01 | `01-stratification-program.md` | the stratification: classes, window, pads, Lemma K1 (direction corrected), `stratum_kill`, why it is constructive, the n = 11 scoreboard, the Lean layer, a catalogue entry | register the strategy |
| 02 | `02-ladder-requirements.md` | double meeters up and down k: SWAP, Theorem FC, SLOT-CROWD, the traction finding (A238), the row cascade (A241), k4_11's pressed fifth square, ONE-TILTED / WEDGED-SEAL / EPS / SNAP exactly | a two-square row; the row cascade on a bigger machine |
| 03 | `03-k0-status.md` | k = 0: K0-FREE, SWAP/CELLS, the extremal reduction, every refuted route with its witness, the measured facts, STEP on the eleven cells, the n = 11 chain | a field certificate conditioned on four doubly-met corners |
| 04 | `04-simple-square-conjecture.md` | Conjecture ONE-FLUSH(n) in your vocabulary: equivalences, what is proved, refuted, measured; LOCKED-CROWD-FREE(n); the Lean files | the n-indexed certificate family |
| 05 | `05-toolkit.md` | geometry before LP: stage 0, the CSP, multibox cores and clips, the leaf rules, exact kernels, speed (7.22×, 5.0×), what is frozen, how to run one page | a soundness review of one leaf rule; a kernel |
| 06 | `06-climb-17-19.md` | the census (2,500 classes, 632 four-corner), the windows with T-numbers, the descent so far (k = 16, 15 dead; k = 14 67/68; k = 13 running), record rigidity, PENDING | **run the descent and the climb** (inputs supplied) |
| 07 | `07-timeline.md` | A01 → A243 (+ A244–A281), one line per campaign with a result, by month; T-037 / T-060 / T-112 placed | — |
| 08 | `08-t037-replay.md` | our replay of T-037: 12,028/12,028 rows, 0 differ; exact spot-check PASS; the CRLF note; the window consequence | retain beside T-037 if useful |
| — | `ISSUES.md` | proposed issue titles and first paragraphs, one per piece, in the shape of your intake issues; a note to the maintainer | — |

How the pieces relate: 01 is the frame; 02 is the mechanism that makes the frame a ladder (closed strata at k + 1
are forced cells at k); 03 and 04 are the bottom of the ladder (k = 0 is the only stratum with no certificate route,
and it is the conjecture); 05 is what runs; 06 is the ladder at n = 17 / 19; 07 is how we got here; 08 is a service.

## 3. What we ask, in one place

1. **Compute on the climb** (06): the four-corner descent at n = 17 from k = 13 to the record's k = 8 and the root,
   then n = 19; ≈ 100 s per class with growing walls, two processes here — days to weeks; hours on your machines.
   Also the row cascade (02 §3) and the k0 chains (03 §5), all resumable.
2. **Proofs of the conjecture** (04): a threshold-type certificate conditioned on four doubly-met corners at
   n = 11 on [31/8, s0] (it would close k0_00), and the family indexed by n; or an argument on LOCKED-CROWD-FREE(n).
3. **Registration of the strategy** (01 §7) in `packing/frontier/proof-strategies.yaml`, and a unification of
   vocabulary (pins / parents, stratum kill / per-class certificate, pad / dilation).

## 4. The retained package (what a pin of https://github.com/Esummins/packing would retain)

| path | what it is | cited by |
|---|---|---|
| `writeup/outreach/*.md` | this series | — |
| `writeup/{01_summary,02_mathematics,05_status_sheet,06_compute_plan}.md`, `writeup/outreach_simple_square_conjecture.md` | the lab's write-up, the canonical status table, the conjecture note | 00, 01, 04 |
| `docs/proofs/{contact_census,instratum_bridge,closed_disjoint_bridge,forced_corners,slot_crowds,protected_trees,sideband,ring_swap,one_flush,local_lock,swap_leaf,k0_route,k0_count,wall_torque,wedged_seal,lemma_eps,snap_rule,two_grains,handedness,cross,no_vv,realign,ring_capacity,pocket_waste,drain_flow_k0,noroom,corner_seal,threshold_bound}.md` | the lemma files (n-general statements, proofs, refutations) | 01–05, 08 |
| `docs/residue_ledger.md`, `docs/shadows/STATUS.md`, `docs/residue_map/` | what is left, the galleries and pages | 01, 03 |
| `lean/PackingCertMathlib/` (`Main.lean`, `Statements/`, `Statements/Open/`), `lean/AUDIT.md` | the Lean layer and its generated audit | 01, 04, 08 |
| `certs/` (`measure_certificate_3.8{0,1,2}.json`, `trump11_certificate*.json`, `octic_root_isolation.json`, `cidl_identity.json`, `tube_*.json`, `verify_*.py`, `README.md`) | the 3.82 measure certificates, Trump's exact data, the tube certificates, the stdlib verifiers | 01, 05 |
| `attempts/REGISTRY.md`, `LOG.md` | the campaign registry and the notebook | 07 |
| `attempts/A53-simple-strata/results/{name_to_slots,name_to_shapes,skeletons}.json`, `attempts/A56-sparametric/results/scoreboard.json` | the n = 11 census names and the 52-row window scoreboard | 01 |
| `attempts/A57-shadow-trees/code/verify_case.py` (frozen v1, sha256 521cb01fe656…), `attempts/A135-polycore-verifier/code/verify_case_v3.py`, `attempts/A185-boxed-windows-clause/code/verify_case_v4.py`, `attempts/A190-guardline-clause/code/verify_case_v5.py`, `attempts/A232-swap-leaf/code/verify_swap232.py` | the certificate verifiers | 05 |
| `attempts/A211-coarse-tree/code/`, `attempts/A202-fast30/`, `attempts/A203-csp-consistency/`, `attempts/A213-int-polycore/`, `attempts/A214-c-kernel/`, `attempts/A215-closed-node-benchmark/results/benchmark215.md`, `attempts/A221-lane-cover/notes/lane221.md` | the live engine and its benchmarks | 05 |
| `attempts/A238-k4-benchmark/{notes/k4_238.md,results/}`, `attempts/A241-row-cascade/{notes/cascade241.md,results/rows241.md,code/}` | the k4 benchmark and the row cascade | 02 |
| `attempts/A243-climb-17-19/` (`BRIEF.md`, `notes/climb243.md`, `code/`, `results/census243_n{17,19}.json`, `results/verdicts243_n17.jsonl`, `results/climb243*.{md,json,jsonl}`, `results/rigid243_n{17,19}.json`, `certs/n17/`) | the n = 17 / 19 climb: census, verdicts, 276 spine certificates | 06 |
| `attempts/A242-replay-31-8/` (`results/`, `ext/PIN.json`, `logs/`; the clone itself is git-ignored) | the T-037 replay receipts | 08 |
| `attempts/A217-torque-probe/results/witnesses217.jsonl`, `attempts/A226-one-flush/` | the four-crowd witnesses and the 21-record survey | 03, 04 |

Pinned commit: the commit that carries this series on `master` (to be quoted by the PI when posting; every number in
the notes is read off a committed artefact at or before it).  Bulk data (A57/A60 tree records, gallery SVGs, logs)
is in the repository but need not be retained.

## 5. Reading order and conventions

Read 01 → 02 → 04 (the idea, the mechanism, the conjecture), then 06 (the run), then 03 / 05 / 08 as needed.
Each note has a five-line abstract, tagged claims with lab sources (`docs/proofs/<file>.md §n`, `attempts/<id>/…`,
Lean names in backticks), and a closing "What we ask".  Numbers: ŝ = 3.877083590022814 (Trump's side, the octic
root), s0 = 969271/250000 (its rational ceiling), W = [3.82, s0], W′ = [31/8, s0].  Corner frames: BL, BR, TL, TR;
a slot (c, i, j) by its offsets from corner c; a class name `k5_11` = the 11th D4 class with 5 pins at n = 11, and
`n17_k14_0215` = the 215th class with 14 pins in the n = 17 census.
