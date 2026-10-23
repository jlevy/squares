---
type: is
id: is-01m5mr7439b7eqzqzccqrxnkxa
title: "Import Amund Kristiansen: s(303) <= 17.909762327476, 9.89e-6 below T-230 (#755)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: c-lane-755-1023
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T16:06:32.296Z
updated_at: 2026-10-23T17:29:07.806Z
started_at: 2026-10-23T16:06:37.444Z
---
Issue #755 (https://github.com/jlevy/squares/issues/755), opened 2026-10-23T11:12:48Z by amundsk (Amund Kristiansen): one upper bound at 303, a dilation certificate made with Evan Daniel's dilate_cert.py (evand 7982d7a), gist 78f9f0e7b4669f2f509a281845081768 at 511f56bf6e6afb4eb22f12d31371c2a2fe7b4767, s303_amund.cert SHA-256 9ec01059b35cc983cb28a1bb33bd215a2717228f7efd182e1724de6b22dc511b, side 223872029093440709529093216833/12500000000000000000000000000. Below the house T-230 (Daniel, #728) by 9.89e-6 if verified. Stages 1-3 then stage 4 (separate review lane), then adoption and regularization at 303 (think-ykgh owns 303's open row-7 review).

## Notes

2026-10-23 c-lane-755-1023 (import lane, sole committer, branch claude/intake-2026-10-23-755).

## Stage 1 triage (claim map and price)
- Source pinned: gist amundsk/78f9f0e7b4669f2f509a281845081768 at 511f56bf6e6afb4eb22f12d31371c2a2fe7b4767, committed 2026-10-23T11:12:11Z, 37 s before the issue. It is the gist's only revision and its head when read at 16:11Z (GitHub API history: one version; no comments). Files: s303_amund.cert (SHA-256 9ec01059...511b, matches the issue), s303_amund.input.txt (19fc5d17...bba4, matches the issue) and README.md (870ead51...0c58, not printed).
- Licence: none in the gist or the issue, so custody is derived-only: no upstream byte is retained, the three files are pinned by digest and blob, and the certificate is kept as an exact Witness/v2 fact.
- Claims: one, s(303) <= 17.909762327476, the exact side 223872029093440709529093216833/12500000000000000000000000000 rounded up at 12 places. The issue's 18-place print "17.909762327475256427..." is the binary64 value nearest the side, 3.35e-16 below it. Map: a new register entry (T-238) at 303.
- Report order: #755 is the only open report below T-230 at 303. #375, #470, #573 and #593 are registered and above it, with no comments since #728. #732 starts at 328, and the open records PRs add no claim at 303. evand's head is still 7982d7a, and Mishapolk's commits since #728 concern 328 to 10,000. No ledger is needed.
- Method and lineage, as measured (measure/identity.py, the #728 packet's identity program loaded unchanged): one to one with T-230's packing; largest move 0.547; 12 squares beyond 0.1, 31 beyond 0.01; 96 tilted squares against 91, all one way; every one of T-230's tilted squares pairs within 0.1 with the same sign. These are the issue's figures. A new arrangement near T-230's, not a refinement. Against T-186, T-174 and T-162 there is no one-to-one match and 68 to 70 squares move beyond 0.1. The dilation was confirmed against the checkout (side rounded up at 30 places; centres within 4.9e-31).
- Significance draft: S3, as T-230 (a new arrangement at 303, 9.89e-6 below the house, found from the previous house).
- Price: replay about 1 CPU-minute (certify 28.7 route CPU-s, 46 s wall; check --replay 46 s; sharp controls 39 CPU-s), all run in this pass. Review 5 to 10 CPU-minutes (think-jdz0). Regularization at 303 5 to 25 CPU-minutes after adoption. Total well under the 40 CPU-h item cap.
- Credit: Amund Kristiansen (GitHub amundsk); bibliography credit "Kristiansen after Daniel, Ostashev, Levy" (the start the issue names is T-230/W-known-best-n303, whose chain is Daniel after Ostashev, Levy). Claude assistance disclosed.

## Stages 2 and 3
- 3003d81d5: packet amundsk-n303-2026-10-23 (derived fact, claims.json at main c1115c095, receipt, sharp controls, identity). acquire_source --check: PACKET_MATCHES_ITS_CONTRACT. Pushed and reported to the coordinator for the stage 4 lane.
- 02de0b762: T-238 at V0/C0, S3 draft, pending adoption; evidence E-amundsk-755-n303-report; coverage; bibliography key [Kristiansen n303 2026-10-23]; profile amund-kristiansen; census spans; #755 requests entry; views. The case record at 303 waits for the adoption writer, as for T-230.
- Draft PR https://github.com/jlevy/squares/pull/757 (labels intake, S3), branch claude/intake-2026-10-23-755. Main merged at 7335d0098 (#752), 05e95db36 (#751) and 769e441e1 (#748), with a re-pin after each. Explainer v0.4.22 (collides with #753's and #745's; the later merge re-cuts); no-change record for the other three papers. Id contiguity fails until T-231 to T-237 merge.
- Deferral: think-vvrx (a derived fact's source URL for a gist).
- Open question to the coordinator: the S3+ News entry cannot pass render_changelog --check before merge (it needs a delivery record); the draft entry is saved in lane-755/news-entry.diff.
- Next (after the review lane think-jdz0 returns): map the review, T-238 to V3/C3 if accepted, adopt at 303, regularize (owner row-7 item think-ykgh), re-date and re-pin at merge.

## Acknowledgement / import reply draft (not posted; post after merge from main with check_requests --draft 755)
See scratchpad lane-755/755-ack.md; the text follows.

@amundsk, thank you for the report and for the clear account of how the packing was made.

**What we received.** One upper bound, s(303) ≤ 17.909762327476, in your gist
[amundsk/78f9f0e7…](https://gist.github.com/amundsk/78f9f0e7b4669f2f509a281845081768/511f56bf6e6afb4eb22f12d31371c2a2fe7b4767)
at revision `511f56bf6e6afb4eb22f12d31371c2a2fe7b4767`, its only revision. Both SHA-256 digests in
the issue match the pinned files. The certificate's exact side,
223872029093440709529093216833/12500000000000000000000000000 = 17.90976232747525676232745734664…,
rounds up at 12 places to the value you claim.

**How it is kept.** Neither the gist nor the issue states a licence, so the record keeps no copy of
your files. It pins all three by digest, and keeps the certificate as an exact derived fact (the same
squares, as a Witness/v2 file) in the packet
[`amundsk-n303-2026-10-23`](https://github.com/jlevy/squares/tree/main/packing/resources/web/amundsk-n303-2026-10-23).

**What we checked.**

- Report order: yours is the only open report below T-230 (Evan Daniel, #728) at 303, and it is below
  every report the record holds there. The margin below T-230 is exactly
  9889799071009889799071/10^27 ≈ 9.89 × 10⁻⁶.
- Replay: this repository's two exact rational routes (the `sqpack` witness verifier and an
  independent corner checker, neither of them your code or Evan Daniel's checkers) accept the
  certificate and refuse a duplicated square and a square moved outside the box. They also meet the
  two sharp controls exactly: the side lowered to the least wall clearance, and the tightest pair
  closed to contact, are accepted at contact and refused 10⁻³⁰ past it. Least wall clearance
  6.02 × 10⁻¹³, least pair gap 1.205 × 10⁻¹².
- Dilation: the certificate is your binary64 packing dilated by 1 + 10⁻¹² as you describe (centres
  within 5 × 10⁻³¹ of the dilated input).
- Identity: measured square by square, it pairs one to one with T-230's packing. The largest move is
  0.547, 12 squares move more than 0.1 and 31 more than 0.01, and it has 96 tilted squares against
  91: your figures. By the record's convention (a refinement moves no square beyond a tenth) it is a
  new arrangement near T-230's packing, not a refinement, as you say.
- One small note: the long decimal "17.909762327475256427…" in the issue is the binary64 value
  nearest the side, about 3.4 × 10⁻¹⁶ below it, not its decimal expansion. The 12-place bound you
  claim is correct, and the record quotes the exact side.

**Where it stands.** It is registered as **T-238** at V0/C0, as reported, credited to Amund
Kristiansen after Evan Daniel's packing and tools (Kristiansen after Daniel, Ostashev, Levy), with
your disclosure of Claude assistance recorded. An independent mathematical review of the certificate
is under way. When it is accepted, T-238 becomes the house best packing at 303 and its drawing is
regularized; we will follow up here at each step.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
