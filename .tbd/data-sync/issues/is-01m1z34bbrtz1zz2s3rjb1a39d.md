---
type: is
id: is-01m1z34bbrtz1zz2s3rjb1a39d
title: Give Figure 1 a concise algebraic side-length caption
kind: task
status: closed
priority: 2
version: 5
labels: []
dependencies: []
parent_id: is-01m1z0patm2bp8vk8h8ntk3gwe
created_at: 2026-09-07T23:26:52.790Z
updated_at: 2026-09-07T23:41:58.728Z
closed_at: 2026-09-07T23:41:58.728Z
close_reason: "Completed in PR #117 at 83a2e6f3. All required hosted checks and the paper build passed; the timing-only CI failure passed one unchanged-commit retry. Three agent reviews and root review accepted the work. HTML, Markdown and the 17-page PDF were rebuilt; the web preview and Preview PDF were opened. The latest upstream deployment also passed all 26 live-site checks. Separate selector issue think-oe1g remains open."
resolution: null
duplicate_of: null
---
Replace the duplicate Figure 1 upper-bound caption with a concise description of eleven unit squares inside the outer square. Verify and mention that its side length 3.8770835... is a root of an eighth-degree polynomial; keep provenance/details in the existing Trump footnote. User specifically wants new information without repeating the immediately preceding sentence. Review with the mathematical subagent, rebuild HTML/PDF, and include in PR117.

## Notes

Figure 1 now reads: Eleven unit squares inside a square of side 3.8770835..., a root of an eighth-degree polynomial. The preceding sentence retains Trump’s attribution and upper bound; the caption adds the algebraic fact. The existing Trump footnote points to Kingbird’s defining polynomial. Verified against the live and archived register; the mathematical subagent also confirmed the existing exact derivation and construction verification, including P(side) = 0 and irreducibility over Q. Trump’s 2023 note prints a polynomial for cos(phi), so the side polynomial is correctly sourced to Kingbird. Root reviewed the final caption on PDF page 1. Committed in 83a2e6f3 and pushed to PR #117.
