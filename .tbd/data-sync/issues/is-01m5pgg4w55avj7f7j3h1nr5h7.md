---
type: is
id: is-01m5pgg4w55avj7f7j3h1nr5h7
title: "Triage evand/square-packing 659ee62 (no issue): candidates s(268), s(303), s(304) at 8a8879a (Lavrentev, Deotte and an unknown finder's Kaggle packings, exact descent) and the odd-n strips Lean work (6bc50ea, d28be37)"
kind: task
status: closed
priority: 1
version: 5
delegate: c-triage-watch-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T08:30:08.261Z
updated_at: 2026-10-24T09:12:52.149Z
started_at: 2026-10-24T08:44:28.321Z
closed_at: 2026-10-24T09:12:52.149Z
close_reason: "Stage 1 triage done (notes): evand 268 and 304 and Couzo's fa6237e 304 go to import bead think-l49q; 303 not recorded; strips and tooling nothing to import; the 659ee62 read rides the next records PR naming think-l49q."
resolution: null
duplicate_of: null
---

## Notes

2026-10-24 coord-intake-1024: from the sweep (evand/square-packing 15 commits past the 7982d7a read). 8a8879a's message: s268_lightning, Lavrentev's Kaggle lightningv08 packing, exact descent to 16.8743617159, 'the side a Kaggle per-puzzle side-only claim lists; the first public packing at that side'; s303_cdeotte, Chris Deotte's public Kaggle packing, exact descent to 17.9072382745; s304_pub, the public Kaggle packing at 17.9268989004 (finder unknown; earliest copy kozykappa's notebook); 'Posting approved by Evan in chat 10-23'. Compare with #763's 268 (16.874361715874, 23:35Z) and 303 (17.906978233799), T-174, T-230, T-239 and the 304 house, in report order. Strips: odd-n strip theorem in Lean (strip_odd_iff, 1.87 <= H < 2). Read-only triage first (stage 1).


2026-10-24 c-triage-watch-1024 (stage 1, read-only; coordinator coord-intake-1024). Nothing committed, pushed or posted. Read against main e5c1c64e3 (post #757 T-239 and #769 PR C), franciscouzo/square-packing@964ee2b (#763's pin) and @1c17153, evand/square-packing@659ee62. Scratch data and tools: scratchpad triage-watch/ (data/, tools/identity_pairs.py, out/identity-268.json, out/identity-303-304.json).

SOURCE AND TIMING
- Head 659ee62e4a9d39542a1146e8b011cc3ab6407ede, 15 commits past the 7982d7a read. GitHub activity API pushes: 7982d7a->5e862ac 2026-10-24T03:58:45Z, 5e862ac->8a8879a 04:53:53Z, 8a8879a->659ee62 05:02:45Z.
- 8a8879a2972c32cbd2d906049228cc9f0762b02a: authored 04:38:50Z, committed 04:49:33Z, pushed 04:53:53Z, all after #763 (issue 2026-10-23T23:35:51Z; 964ee2b and fa6237e pushed 23:38:42Z). Any reading of its time puts it after #763.
- NOT POSTED. 659ee62's Completed.md: "certified the public Kaggle packings (8a8879a2; 268 and 303 by exact descent of lightningv08's / cdeotte's packings) but did not post: franciscouzo's open #763 already held all three". No jlevy/squares issue or comment by evand since #728 (22 Oct); no issue mentions lightningv08/cdeotte/kozykappa. 659ee62's TODO: "Optional, Evan: a credit note on jlevy #763 (n = 268: Couzo credits kirilltym's Seam LP notebook; the packing first appears in lightningv08's CUDA Packing Search output, kirilltym's input). Our tighter 268 / 304 certificates are at 8a8879a2 if useful."
- Licence MIT (Evan Daniel). SHA-256: s268_lightning.cert c87da316, s268_lightning_regularized.cert a3095441, s303_cdeotte.cert 6cf9cc95, s303_cdeotte_regularized.cert 87db126c, s304_pub.cert 5dd7436a.

VERDICTS (exact sides from the .cert headers; members from intake_ledger.tree_members(read_on=2026-10-24) on e5c1c64e3; #763 from 964ee2b certificates/n268.cert e9833bf2 and n303.cert 39a150f4; report order as listed)
- 268. Start T-174 16.878814821007 (Couzo, improved by Daniel, PingYou).
  1. #763 (23:35:51Z) 78645658458105249171306580101/4660659750118e15 = 16.874361715873825 (print .874), -4.4531e-3 vs T-174: recorded by PR A (think-ptkk).
  2. evand 8a8879a (04:53:53Z) 8437180857934672912242411148233/5e29 = 16.874361715869346 (print .870): -4.479655e-12 vs #763, -4.453105e-3 vs T-174. Its JSON: KKT local minimum, S_exact 16.8743617158693458243..., cert 1.7e-22 above it (Couzo's is 4.48e-12 above). Below #763 by 4.48 units of the 12th place, prints differ; in the corpus, so think-fwa9's restatement ruling (beyond 324) does not reach it anyway. RECORDED by the report-order rule, as T-146 recorded Daniel's sub-print display certificates (S2).
- 303. Start T-239 17.909762327476 (Kristiansen); T-230 17.909772217275 (Daniel) superseded.
  1. #763 17.906978233799, -2.784094e-3 vs T-239: recorded by PR A.
  2. evand 8a8879a 17.907238274538241 (print .274539): +2.600407e-4 vs #763 (ABOVE), -2.524053e-3 vs T-239, -2.533943e-3 vs T-230. NOT RECORDED (later and weaker). Stays as credit evidence only.
- 304. Start T-186 17.929427758076 (Ostashev, improved by Mishapolk). #763 does not claim 304.
  1. franciscouzo fa6237e certificates/best/n304.cert (blob 953dc2e5, sha256 c8433dd7; committed 2026-10-23T18:59:39Z, pushed 23:38:42Z with 964ee2b; unchanged at 964ee2b and 1c17153) = 17.926898903393 (print), -2.528855e-3 vs T-186. Couzo's index credits it "Kirill Tymchishin (kirilltym), Kaggle 'CPU Alternating Reclosure' v3" with no Couzo refinement, which is why #763's own selection (another author's) leaves it out. A watched-repository certificate is a report from its publication (owner, 2026-10-14): RECORDED, a claim in scope the request does not mention.
  2. evand 8a8879a s304_pub.cert 1792689890035674158972360842897/1e29 = 17.926898900356742 (print .900357): -3.035902e-9 vs fa6237e, -2.528858e-3 vs T-186; KKT local minimum (S_exact 17.92689890035674158954...). RECORDED (later, stronger by 3.0e-9).
- Kaggle per-puzzle board side-only claims (no coordinates; not reports here by any current rule), from Couzo's public_bounds.json: 268 Minal kharat123 16.874361715926692 (22 Oct 18:54:00 UTC), panpanpanda 16.874361715872031 (23 Oct 14:48:22 UTC; 1.79e-12 below #763, 2.69e-12 above evand); 303 Lucas Boesen 17.908331255816149 (22 Oct 22:51 UTC), pjmathematician 17.906978233833611 (23 Oct 11:56:49 UTC; 3.47e-11 above #763); 304 panpanpanda 17.926898900359041 (22 Oct 15:48:34 UTC; 2.3e-12 above evand), Amin 17.924726031170107 (23 Oct 00:15:35 UTC; 2.17e-3 below both packings).

IDENTITY (binary64; the retained measures of resources/web/evand-regularized-2026-10-20/measure/identity.py, unchanged: nearest centre under the 8 symmetries kept only where one to one, and an optimal assignment over the 8 symmetries; scratch driver tools/identity_pairs.py)
- 268: evand vs #763: same packing, 0 squares beyond 0.1, 69 beyond 1e-2, max move 7.08e-2, max turn 1.36 deg (symmetry 4; the packing has 127 exact flat motions per its JSON). evand vs Tymchishin's EDA+Seam LP v4 parent (964ee2b parents/85dbd707..., 16.87546795): 0 beyond 0.1, max 2.49e-2. #763 vs that parent: 0 beyond 0.1, max 5.99e-2 (think-cnn7 had 5.9e-2). evand vs T-174: one to one under no symmetry; assignment 118 beyond 0.1 (think-cnn7: #763 vs T-174 119). So Lavrentev's public packing (evand's input, binary64 side 16.87436171586941), Tymchishin's v4 packing and #763's 268 are one packing.
- 303: evand (Deotte) vs #763: 4 beyond 0.1, max 0.238, max turn 27.0 deg; vs Couzo's Kaggle push parent (parents/22f07a7c..., seeded from Lavrentev CUDA v11): 2 beyond 0.1 (assignment), max 0.223; #763 vs that parent: 3 beyond 0.1 (as think-cnn7). vs T-239: 136 beyond 0.1; vs T-230: 128. Deotte's packing is the arrangement #763's 303 refines, within 2-4 squares.
- 304: evand vs fa6237e's: same packing, 0 beyond 1e-3, max 4.60e-4, max turn 0.019 deg (symmetry 0). vs T-186: no one-to-one symmetry; assignment 54 beyond 0.1, max 1.13: a new arrangement relative to the house.
- OR-1: the driver should become a devtools CLI over check_half_angle_area.arrangement_gap plus the optimal assignment (devtools.measure_identity), since three packets now carry copies of the same measurement.

CREDIT (the source's own words; never inferred)
- 268: evand 8a8879a: "Vladislav Lavrentev's (Kaggle lightningv08) public packing, exact descent (shrink-only) ... the first public packing at that side"; 659ee62 TODO: "the packing first appears in lightningv08's CUDA Packing Search output, kirilltym's input". #763 (964ee2b): "Couzo ... refines the packing of Kirill Tymchishin ... EDA+Seam LP v4". If Lavrentev's output was public before #763, #763's 268 refines a packing already public at essentially its side; the chain then reads Couzo after Tymchishin after Lavrentev, and Daniel's row is Daniel after Lavrentev (as his source says), certifying the same packing tighter. Ask both authors for the notebook versions and dates (Kaggle needs a login; not read here).
- 303: evand credits Chris Deotte's public Kaggle packing; #763 credits Lavrentev's CUDA v11 via Couzo's own Kaggle push. Not recorded, but it bears on #763's credit chain: ask which came first.
- 304: Couzo: Tymchishin's "CPU Alternating Reclosure" v3; Daniel: "finder unknown; earliest public copy: kozykappa's notebook". Ask both; do not infer. Daniel says he is not its finder.

OTHER 14 COMMITS: nothing to import.
- c1572fc, d47d17a, f3ea419, d28be37, 6bc50ea (authored 22 Oct 17:15Z-17:38Z, committed 24 Oct 03:51Z) and 8b2f214's notes: strip_odd_iff (lean/Sqpack/StripC.lean, standard axioms, no hypothesis; supersedes 7982d7a's conditional strip_odd_of): for odd n >= 3 and 1.87 <= H < 2, n unit squares fit in [0,L] x [0,H] iff L >= n or L >= (n-2)(2 sqrt 2 - H) + 4 - H; strip_row and strip_zigzag constructions; chainn LP scripts. Strips are rectangles, outside this record; at L = H < 2 the condition needs L >= 4 - H > 2 > H, so it bounds no s(n). Out of scope, as the 7982d7a read said.
- c185697: regcheck.py, satcheck_f64.py, kaggle_import.py, triangle1000.py (tools over the source's private store) and SUBMITTING.md "Beyond the register" (PUBLIC / FIRST / NEW / SIDEONLY / PENDING; FIRST claims "first publicly known packing" against a side-only Kaggle entry). Policy, no bound.
- f5fbf7b (packer stages/chains, trial.py, fq --freeze), 9a8d502, a9cdd63 and 5e862ac (TODO, CLAUDE.md public/private split): tooling.
- fd90f09, 2aae1b6, 659ee62: the live check missed #763 (repo too large to fetch); lessons; the credit note above; "Imported #763's 350 certificates for n <= 1000" into the private store (not a publication).

PROPOSED DISPOSITION
1. Import bead (new): "Import evand and franciscouzo: s(268) <= 16.874361715870 and s(304) <= 17.926898900357 (Daniel's exact descents of public Kaggle packings, 8a8879a) and s(304) <= 17.926898903393 (Tymchishin's packing, franciscouzo@fa6237e) (no issue)". Order at 304: fa6237e first. In-corpus entries: 304 (Tymchishin per Couzo, S3; then Daniel's tighter certificate) and 268 (Daniel after Lavrentev, refining T-240's packing, S2, as T-146). The 304 packet file can come from PR A's 964ee2b packet (one more file, certificates/best/n304.cert) so no second Couzo packet is needed.
2. Packet evand-kaggle-descents-2026-10-24 pinning 8a8879a: s268_lightning.{cert,json,input.txt,predescent.txt,exact.txt}, s268_lightning_regularized.{cert,json}, s304_pub.{cert,json,input.txt,exact.txt}, s304_pub_prior.json, and s303_cdeotte.{cert,json} as credit evidence; about 0.45 MB raw, Git.
3. Read in intake-watch.yaml at 659ee62 naming the import bead (held until the packet pins 8a8879a); draft below.

PRICE (cap 40 CPU-h): replay of 3 certificates (268, 304 evand; 304 fa6237e) on both maintained routes with controls, under 0.02 CPU-h; identity receipt seconds; stage 4 review of the two in-corpus entries, one tbd-strong-max review each (tokens, under 0.1 CPU-h); adoption and regularization at 268 and 304, 10-50 CPU-min each (Daniel's s268_lightning_regularized.cert is a ready display view at the tighter side). Total under 2 CPU-h; nothing held for the cap.

FOR PR A (think-ptkk) AND PR B
- Retain certificates/best/n304.cert at 964ee2b in PR A's packet (the earlier 304 report).
- #763's 268 credit: Daniel's source names Lavrentev's lightningv08 output as the packing's first appearance and Tymchishin's input (measured: one packing). Register as #763's source says; put the question in #763's acknowledgement.
- #763's 303 credit: Couzo's own 43f666c README now cedes 303 to pjmathematician's side-only board entry (see think-cncq), and Deotte's public packing is the same arrangement within 2-4 squares.
- PR B: adopting and regularizing 268 at #763's side re-houses it twice if Daniel's 4.48e-12 tighter certificate is then recorded; sequence PR B's 268 adoption after this import, or adopt Daniel's directly once it is registered.

AUTHOR QUESTIONS
- Daniel: do you claim the 268 and 304 certificates at 8a8879a as bounds (the record reads a watched-repository certificate as a report from its publication), credited "Daniel after Lavrentev" (268) and "Daniel after <finder>" (304)? Which lightningv08 notebook version and date first held the 268 packing (kaggle_import's example names lightningv08_v12_2026-10-22), and the dates of Deotte's 303 and kozykappa's 304 notebooks?
- Couzo (in the #763 acknowledgement): see think-cncq.

OWNER QUESTION (candidate, for the coordinator): Kaggle per-puzzle leaderboard sides (team, side, date, no coordinates) now drive credit in both watched sources (Daniel's FIRST class; Couzo ceding 303). No rule here covers them. Recommended: not reports (no packing), stated as dated priority annotations beside an entry when they precede it within 1e-10.

DRAFT intake-watch.yaml READ
  - url: https://github.com/evand/square-packing
    read_through: 659ee62e4a9d39542a1146e8b011cc3ab6407ede
    read_on: '2026-10-24'
    bead: <the import bead>
    note: >-
      The 15 commits past the 7982d7a read, c1572fc to 659ee62, pushed on 24 October at
      03:58:45Z, 04:53:53Z and 05:02:45Z. 8a8879a (pushed 04:53:53Z) adds
      search/packer/candidates/ certificates for three public Kaggle packings, which the
      source did not post because #763 already held the counts: s268_lightning.cert,
      s(268) <= 8437180857934672912242411148233/(5*10^29), the exact descent of Vladislav
      Lavrentev's packing, 4.48e-12 below #763's side and the same packing;
      s304_pub.cert, s(304) <= 1792689890035674158972360842897/10^29, a public packing
      whose finder the source does not know, 3.04e-9 below the same packing's certificate
      at franciscouzo@fa6237e; and s303_cdeotte.cert, Chris Deotte's packing at
      17.907238274539, above #763's 303, so not recorded. The 268 and 304 certificates
      are later reports the record takes, held for the import bead. c1572fc, d47d17a,
      f3ea419, d28be37 and 6bc50ea prove in Lean (strip_odd_iff, standard axioms) that
      for odd n >= 3 and 1.87 <= H < 2, n unit squares fit in an L x H strip iff L >= n
      or L >= (n - 2)(2 sqrt 2 - H) + 4 - H; strips are rectangles, outside this record,
      and bound no s(n). c185697 adds the source's register-check and Kaggle import tools
      and its "Beyond the register" posting policy; f5fbf7b, 9a8d502, a9cdd63, 5e862ac,
      fd90f09, 2aae1b6 and 659ee62 are packer framework, TODO, CLAUDE.md and submission
      checklist edits. Nothing else to import.

blocked_on: think-ptkk
