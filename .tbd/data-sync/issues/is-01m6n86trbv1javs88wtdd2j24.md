---
type: is
id: is-01m6n86trbv1javs88wtdd2j24
title: "Import Özden: s(94) >= 2493/250 by rescaling Hosono's mixed_n94_L995 onto a 4,972-direction net (#910)"
kind: task
status: in_progress
priority: 1
version: 5
delegate: bold-ritchie-l49
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
child_order_hints:
  - is-01m6na15dgp4fwgm2d24mcwk2w
  - is-01m6na2ne3zs2jq13j0b5n3a7x
hold: null
hold_until: null
created_at: 2026-11-05T07:01:41.771Z
updated_at: 2026-11-05T07:40:40.368Z
started_at: 2026-11-05T07:01:46.219Z
---
Import of jlevy/squares#910 (opened 2026-11-05T06:51:55Z by kenaznia-doga, an AI agent account posting for Doğa Özden): s(94) >= 2493/250 = 9.972, above T-262's 1993/200 by 7/1000. An exact rescaling of Hiroaki Hosono's mixed_n94_L995 measure by 4986/4975 onto a declared net of 4,972 half-angles (step 1/12000), decided by the lab with this repository's unmodified sqverify-fast; "not a new packing arrangement".

## Claim map
- Source: kenaznia-doga/s94-lower-bound-9972@7d21f9bdf707102dd4ebf47e52f81b502a01004d (one commit, 2026-11-05T06:51:31Z, 24 seconds before the issue). Certificate certificate/n94-L9972.json.gz (format M; L = 2493/250, B = 24872661/24875000, proof_net step 1/12000, last 4971; 853 orbits, mass 9399999/100000). Stated digests: .gz f59d4c95...360c (native input_sha256), JSON text d1df3bc6...951c; Hosono's candidate.json at wand125/square-packing-bounds@797bdf6e 64d81953...0667a, its retained gzip df3ae678...d27c; complete receipts .gz 041284d5...7a59 and JSONL 02906bb0...312a; 99/100 mutant .gz 2f72d2dd...1532; LICENSE.md 5b8e1449...a18da4c.
- Claims in the release: (1) s(94) >= 2493/250 [register: a new lower-bound entry; T-262 keeps its claim, superseded at n = 94 once adopted]; (2) native sqverify-fast receipts (crate source d97758bb, rustc 1.98.0, release) VERIFIED at all 4,972 directions, assembled from six disjoint-selected native streams A-F, least certified bound 1.0000000000003892 at r = 3663; (3) a two-direction 99/100 mass control refused natively at r = 0 and 1198 with an exact witness at 1198 capturing 0.991109005346039... (not a whole-net control); (4) the lab's exploratory C checker at all 4,972 directions (not interval arithmetic; supplementary, not offered as evidence); (5) answers to #890's review notes F3-F5 (the quadrant via the D4 symmetry; growth m_old(t) - m_new(t)/lambda, not rho(1 - 1/lambda); the n = 31 aside not reused) and to #890's second question (the route ceiling 99500/9977 stays; no claim for the 49,707-direction 9.97285 partial).
- Consequence: s(95) >= s(94) settles nothing (n = 95 and 96 are proved = 10, T-191).
- Who else holds the value: nobody; the record's best at n = 94 is 1993/200 (T-262, V3/C3), verified and reported.
- Credit: Doğa Özden after Hiroaki Hosono, Tokoharu and this project (T-262's form). AI assistance as given: AI agents in Özden's lab (Claude and OpenAI Codex agents) constructed and rescaled the certificate, ran the checks, audited the receipts and prepared the submission under his direction.
- Licence: LICENSE.md, byte-identical to the declaration #890's packet retains (blob 9803370f): CC BY 4.0 for certificates, witnesses, receipts, data and write-ups; MIT for the lab's code. Hosono's MIT notice and the crate's own licence retained.

## Validation plan (priced)
- Replay: this repository's sqverify-fast (reviewed source d97758bb) through devtools.sqverify_fast_census over all 4,972 declared-net directions, then the whole-net control (--control). Priced on the validation bead under this one.
- Review: a separately prompted stage 4 mathematical review (tbd-strong-max), briefed on its own bead under this one.

Answer bead: this bead.

## Notes

2026-11-05 (bold-ritchie-l49): stages 1 to 3 done on branch claude/bold-ritchie-xo28us-l49 (draft PR "intake: #910 s(94) ≥ 2493/250 (T-266)"). Packet ozden-s94-lower-bound-9972-2026-11-05 at 7d21f9b; every stated digest holds; audit PREMISES_HOLD and RECEIPTS_HOLD; 13-direction sample with the census binary agrees; T-266 registered at V0/C0; n-094's reported lower lane 2493/250, verified lane unchanged at 1993/200. Replay: think-qcms (about 19.4 CPU-h, runnable after review, not held). Stage 4 review brief: think-xzxd.

Stage 7: no acknowledgement is owed before the merge. This PR registers the result, so the reply below is the import reply, and by result-import.md stage 7 it follows the merge. Post it only after the PR merges and the deploy is verified: render from main with `check_requests --draft 910` (it refuses off main), check that main and the site say T-266 at V0/C0 and n-094's reported lower bound 2493/250, adjust T-266 if renumbered, post, then record it under #910's replies (kind: final, closing the issue) in the next change. #910 is closeable once T-266 is on main: its validation names think-qcms and think-xzxd, which follow on the closed issue.

DRAFT of #910's reply (not posted):

---

Thank you, @kenaznia-doga, for posting this, and thank you to Doğa Özden (@dogaozden), whose result it is. This reply records what was done with #910 and closes the issue; the replay and the review that remain follow here as they land.

**Received and retained.** `kenaznia-doga/s94-lower-bound-9972` at `7d21f9b`, kept whole as the source packet [`ozden-s94-lower-bound-9972-2026-11-05`](https://github.com/jlevy/squares/blob/main/packing/resources/web/ozden-s94-lower-bound-9972-2026-11-05/README.md), except `.gitignore` and `source/hosono-candidate.json.gz`. That gzip is byte for byte the copy this repository already keeps of Hosono's `candidate.json` for T-091, so it is pinned by digest rather than copied twice. Every digest the issue states holds:

- the candidate gzip (`f59d4c95…360c`) and its canonical JSON (`d1df3bc6…951c`);
- Hosono's source JSON (`64d81953…0667a`) and its retained gzip (`df3ae678…d27c`);
- the complete receipts, `041284d5…7a59` as stored and `02906bb0…312a` decompressed;
- the 99/100 mutant (`2f72d2dd…1532`);
- `LICENSE.md` (`5b8e1449…a18da4c`), which is the same file #890's packet keeps.

**What was checked here.**

- **Premises and the dilation.** `devtools.audit_dilated_measure` recomputes these in exact rationals from the retained bytes:
  - format M on the declared net, and lemma N0's five conditions, with B(1 + D) = 99498934887/99500000000 < 1;
  - the last tangent 1657/4000 covering the endpoint: t² + 2t − 1 = 1649/16000000 > 0;
  - the total mass 94 − 1/100000;
  - each of the 853 rows exactly λ = 4986/4975 times Hosono's, with its mass unchanged;
  - the certificate's text and its gzip, both regenerated byte for byte from Hosono's candidate by the rule `tools/rescale.py` states.
- **Your receipts.** The same tool audits the archive from the retained files, without running anything:
  - Each of the six native runs holds exactly its stated scope.
  - Each run's summary states the certificate's premises and refuses nothing.
  - Each run is a build of the reviewed crate source `d97758bb…`, with the same compiler, profile and target as our census binary.
  - Your copy of the crate is that source.
  - All 4,972 directions appear once, each verified at threshold 1 with a finite bound of at least 1, and each selected line is byte for byte its run's line.
  - The least certified bound is 1.0000000000003892, at direction 3663.
- **Your control.** The mutant is every mass times 99/100 and nothing else. At direction 1198, your rational witness captures exactly the stated 0.991109005346039…, in the per-bin domain and the searched quadrant, where the original captures 1.00112…. The crate's own witness there, and the axis sweep's least vertex at direction 0, also capture below 1 when recomputed exactly.
- **A sample.** This repository's census binary ran 13 directions, including 0, 1198, 3663 and 4971. All verified, with your certified bound at each and your node count wherever your line records one.

None of this decides the coverage here; it is an audit of your records and a sample, not a replay.

**What is recorded.**

- [T-266](https://squaremath.org/results.html#t-266), `s(94) ≥ 2493/250`, at **V0/C0**: reported.
- n = 94's [reported lower bound](https://github.com/jlevy/squares/blob/main/packing/frontier/n-094.md) is now 2493/250, 7/1000 above T-262. Its verified lower bound stays 1993/200 for now.

**What remains.** Two things, each with its own bead:

- A complete replay here: this repository's `sqverify-fast` at all 4,972 directions, then the 99/100 mutant at every direction of the net. It is priced at about 19 CPU-hours, within our per-item limit (think-qcms).
- A separate stage 4 review of the certificate's mathematics (think-xzxd).

With both, T-266 would be confirmed, reproduced with the producer's code, since your runs used the same checker. Each step will be reported on this issue.

**On your answers to #890's notes.** The growth formula is as you now write it. On our record's measure, at the 20 nodes your net shares with Hosono's, the centre domain grows by between 1.93e-4 and 1.52e-3 in his coordinates, and by 11/9972 at the axis. The other 4,952 directions are new. Measured the same way, #890's net gives the 6.55e-5 to 1.062e-3 that the earlier review reported.

**Credit.** The record credits the certificate to Doğa Özden, after Hosono, Tokoharu and this project, as your README does. It states the AI assistance as the issue does: AI agents in Doğa Özden's lab, Claude (Anthropic) and OpenAI Codex agents, constructed and rescaled the certificate, ran the checks, audited the receipts and prepared the submission, under his direction. It claims no human review of the new certificate.
