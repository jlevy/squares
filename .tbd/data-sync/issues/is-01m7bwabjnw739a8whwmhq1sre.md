---
type: is
id: is-01m7bwabjnw739a8whwmhq1sre
title: "Import #973: moh63-dev's s(k² − 5) = k for every k ≥ 7 (one periodic family, Valid11 board, Tight-Tile Lemma)"
kind: task
status: closed
priority: 1
version: 8
delegate: bold-ritchie-l145
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
child_order_hints:
  - is-01m7bxg56ccnr8yr3dr26nrtd2
  - is-01m7c65j5dk876m77ftewkck4q
hold: null
hold_until: null
created_at: 2026-11-14T01:56:26.322Z
updated_at: 2026-11-14T08:13:57.409Z
started_at: 2026-11-14T01:56:28.028Z
closed_at: 2026-11-14T08:13:57.409Z
close_reason: "#973 imported as T-298 (#974, 9adc3a0ad), answered and closed; reply and News recorded in #976 (7629f5ade). Held validation: think-0h7r, think-kn13 (re-parented to the epic)."
resolution: null
duplicate_of: null
---

## Notes

2026-11-14 (lane L145, bold-ritchie-l145): stages 1 to 3 done and a time-boxed stage 4 replay run.
Claim map: one result, s(k^2 - 5) = k for every k >= 7 (#973 body), registered as T-298 (optimality, scope n = 44, 59, 76, 95, 116, 139, 164, 191, 220, 251, 284, 319), V0/C0, S4 drafted as a claim; evidence E-khalili-973-k2m5-family-report, E-khalili-973-valid11-report, E-khalili-973-lean-report (all reported). New counts k = 11 to 18 (reported lanes to k, verified unchanged); n = 95 already proved by T-191; k = 7, 8, 9 are T-252, T-066, T-184. T-081 and T-191 gain a sentence each. No verified bound changes.
Retained: packets moh63-dev-k2m5-family-2026-11-13 (pin 2c0b1b9, 465 of 466 files; tight_tile/cov.tar.xz pinned by digest, 8.7 MB, hosted release owed with think-0h7r) and evand-square-packing-2026-10-24 (zeromargin.py 3cb95fb7 at 659ee62). Licence MIT (README adds CC BY 4.0). AI assistance: Claude (Anthropic) per the paper's acknowledgments; builds on Evan Daniel's LP, format, checkers and Lean reduction.
Replay here, about 2.5 CPU-hours: fast verify.sh passed; zmx2 e2bb84e9 rebuilt (d68a2e35), patch is one line output-only; cert0 + 30 of 55 columns equal to the source; root 9632 whole (dump 6,850 boxes and qx2 83 boxes byte-identical; ROOT-9632-CLOSED on our outputs; the dump needs --uncert-cap 10^8, unrecorded); 26 tight-tile jobs equal (the shipped run_tt.py prints a K field the recorded outputs lack); controls all refused. Full replay and Lean build priced on think-0h7r (about 140 CPU-hours, up to 320). Stage 4 review: think-h10k (lane L144), not landed at push; the coordinator maps it.
Acknowledgement draft (post after the PR merges, by stage 7's rule): thank the authors; say the release was retained at 2c0b1b9 and registered as T-298, a reported family at V0/C0 pending the stage 4 review; what ran here (fast verify, cert0 and 30 zmx2 columns, root 9632 with both checkers, 26 tight-tile jobs, the controls), each matching their records; that the full replay (about 140 CPU-hours, up to 320) and the Lean build are priced and held for the owner; and ask the nine questions of the packet README.
2026-11-14, later (lane L145): the L144 blind review landed (f58b34b7b) and is merged and mapped in PR #974: document map; external_review on the three report entries; T-298 reviews (adversarial, accepted), so T-298 is V0/C1; V-khalili-973-review-check (independence record, not clean-room); E-khalili-973-review-partial-checks (mass/family, Lemma 7 premises, theta = 0 face, coverage of the 75 tight-tile roots, root 9632 closure, in full), cited by the nine cases. The review's section 13 duplicated section 11 and ended in a stray "S-LANE"; trimmed with a dated note. Findings: F1 (zmx2 area-density and first-order lemmas unreviewed) held on think-kn13 as a priced option; F2 (Tight-Tile Lemma one implementation, no full replay) is think-0h7r's; F3 (K field) and F8 (ctl_rise counts) agree with this lane's own findings. Reconciled price: about 145 to 180 CPU-hours, up to 320, Lean on a host with >= 24 GB (think-0h7r). The review's text does not state a significance; T-298 keeps the import lane's S4 draft. Reply draft (after merge): T-298 at V0/C1, review summary with F1 and F2, the held replay and lemma review, and the review's 7 questions merged with the packet README's 9.
2026-11-14, lane L147 (bold-ritchie-l147), after the senior review L146 of PR #974. Correction to the note above: F2 (the Tight-Tile Lemma has one implementation and no full replay) is not wholly think-0h7r's. think-0h7r's replay reruns that one implementation and closes only the second half, the full replay; no bead tracks a second implementation. Also: the "Acknowledgement draft" in the first note (V0/C0, pending the review, about 140 CPU-hours) is superseded by the later "Reply draft" (T-298 at V0/C1, the review's F1 and F2, the held replay and lemma review, the merged questions); post only the Reply draft. L147 applied L146's B, S and N items on the branch: the review's programs are no longer called clean-room in the record (independent, not clean-room), the case files carry the review's findings, both lanes' runs of the source's code are registered as samples (E-khalili-973-replay-sample, E-khalili-973-review-replay-sample), the price is about 145 to 180 CPU-hours, up to about 320, on the review's random-job Tight-Tile factor, and the PR body carries the News draft at S4. The reply should also say that the review ran at tbd-strong, not at the tbd-strong-max tier the runbook asks for.
