---
type: is
id: is-01m7prszpzj5azeejtcmphhqav
title: "Import #1031: Joost de Winter's s(299) <= 17.793636991744 (0.0074 below the house), JoostdeWinter/square-packing n299/ at 497eb478"
kind: task
status: in_progress
priority: 1
version: 5
delegate: w6r2-dewinter-1118
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-18T07:26:42.911Z
updated_at: 2026-11-18T08:35:17.583Z
started_at: 2026-11-18T07:33:41.966Z
---

## Notes

2026-11-18T07:36Z w6r2-dewinter-1118: claimed. Triage, read-only (issue read 07:32:46Z, no comment, intake label): #1031 (06:44:45Z) names 497eb478 (06:34:51Z, 'Add the packing for n = 299'; 3293038d at the same second adds REGISTRATION.md and SHA256SUMS; 72323289/aae089c3 at 07:30-07:31Z touch n109 only, #1012's). n299/ at the pin: README.md, n299_exact.json (blob 0a8e8120, SHA-256 199e6132...4a9c), n299_witness.yaml (Witness/v2, corners), n299_record.png, verify_exact.py, check_area.py; MIT per the repository. Exact side 17793636991743040580325825384225613703947282755372586749208848013397/10^66 = 17.79363699174304058, 12-place ceiling 17.793636991744 = the issue's print. Measured against main (86284ec20), not the issue's T-277: the house is T-325 (#1009, Polkovskyi's re-solve of Daniel after Ozden), 2225125554281470853018439796251/125000000000000000000000000000 = 17.8010044342517669; the claim is 7.3674e-3 below it (the issue's T-277 print 17.801004434255294 is 3.53e-12 above T-325). Kaggle: the issue says Nick Sarris reported 17.793636991746555 at 01:07:56Z on 18 Nov with no coordinates found; that is 3.51e-12 above this side, a score with no packing, so not a result here (priority question for the review/owner only if coordinates surface). Lineage per the issue: diagonal slices from Panoras's compilation v17 packings of 372 (prvsiyan 'A Square Deal') and 335 (areebbb, jazivxt, alexchilton, prvsiyan), then local optimization and a diagonal reflection. AI: GPT-6.2 Sol (OpenAI) and Claude (Anthropic), under his direction. Path: upper bound below the house, the house rule; stages 2-3 on claude/intake-2026-11-18-import-1031 after #1029, #1024 and #1021/#1022's PRs; blind review (tbd-strong-max) requested from the coordinator now. Nothing retained yet (scratch download only).

2026-11-18T08:20Z w6r2-dewinter-1118: R-1031 writes on think-r3tn (coordinator); this lane does not read think-r3tn, nor any R-1031 section here, until #1031's review merges. Nothing measured yet for #1031 beyond the triage's side and gains (scratch download at 07:33Z).

2026-11-18T08:33Z w6r2-dewinter-1118: for #1031's PR Limits: at about 08:30Z the coordinator's message relayed R-1031's summary verdict (accept; 7.37e-3 below T-325, about 2e24 times T-325's margin; a new arrangement; S3), before this lane ran any measurement of #1031 beyond the triage's side and gain (07:33Z). The import's replay, controls, identity and margin measurements will be its own programs' outputs under a controls plan hashed before they run.
