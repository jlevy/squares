# Stopped-search audit — 17 October 2026

**Verdict: three valid improvements over the website-listed bounds.** All numerical search is stopped. The frozen exact geometry was unchanged by the audit.

| Squares | Website-listed side | Certified decimal upper bound | Pairs per algorithm |
| ---: | ---: | ---: | ---: |
| 227 | 15.57106781186547 | 15.563796703670 | 25,651 |
| 229 | 15.65685424949238 | 15.650174756949 | 26,106 |
| 260 | 16.65685424949238 | 16.645778804182 | 33,670 |

Each witness passes three rational geometry algorithms: center/basis separation, vertex projection, and exact convex polygon clipping/intersection area. Each checks unit geometry, wall containment and every pair. The clipping checker additionally passed 12 corrupted-input controls and seven analytic area tests. All implementations were created within the same AI-assisted campaign and share Fraction arithmetic and rational witnesses; outside independent review is not claimed.

The website baselines were rechecked. The audited finite public corpus, including deletion, integer framing and uniform product closure, supplies no stronger bound for these three counts. This establishes feasible upper-bound improvements against that corpus, not global optimality or exhaustive worldwide novelty.

227 and 260 share the Young-corner/slipped-ribbon construction framework. 229 descends from 260 by erosion and refinement. There are three improved counts, not three independent construction families. Retired 507/553 claims, larger composites 965/969/1097, ties and repeated refinements add no records. No further promotable improvement was found in the watched candidate files.

## Repairs

- Corrected early-cancellation status and actual duration.
- Excluded mutable Python bytecode from package checksums and archives.
- Repaired three derived-composite source paths to matching immutable rational witnesses; geometry and original proof outcomes were unchanged.
- Narrowed the upstream statement to no tracked source modifications. The excluded local clone contains one untracked temporary certificate artifact.

## Visual audit

All nine figure metadata sets and three combined sheets passed witness-hash checks. The matching is a bijection after a square symmetry; SVG geometry agrees with the delivered witnesses. Orange marks changed near-contact adjacencies at distance <=0.001 unit. Matching is noncanonical and contact is approximate, independent of the exact feasibility proofs.

## Stop and handoff

The four-hour extension was planned for 09:20:12-13:20:12 UTC. The user canceled at 12:49:15 UTC; all optimization was confirmed stopped by 12:51:59 UTC, about 3 hours 32 minutes into that extension. The campaign used 25 distinct workers across the session, at most six concurrent workers. No numerical search was resumed during the audit.

The GitHub-ready package contains exact JSON/certificates, three standard-library checkers, hashes, figures, a PDF and a result-registration issue draft. Nothing has been published or submitted. Full machine-readable receipts are beside this summary.
