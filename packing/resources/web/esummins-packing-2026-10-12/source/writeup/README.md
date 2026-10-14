# writeup/ — the six documents of the s(11) lab

Living documents, edited IN PLACE (no attempt agents for edits; the coordinator and the PI revise directly).
Started 2026-09-09 at the PI's request; 05 and 06 added 2026-09-10 (A195) at the external review's request.

**Start here: [`01_summary.md`](01_summary.md).** The canonical status table is
[`05_status_sheet.md`](05_status_sheet.md); the capped compute plan is [`06_compute_plan.md`](06_compute_plan.md).

| file | audience | what it is |
|---|---|---|
| [`01_summary.md`](01_summary.md) | anyone | the two-page brief: the result, why it was open, how it was done, the human–AI loop with three worked figures, and what remains |
| [`02_mathematics.md`](02_mathematics.md) | mathematicians / the certificate reader | the full mathematical write-up: definitions, every lemma the proof needs (stated for general n where possible), how they compose into s(11) = ŝ with uniqueness, what is Lean-checked, what is certificate-backed, what is pending compute |
| [`03_lab_timeline.md`](03_lab_timeline.md) | AI–mathematics practitioners | the lab timeline in detail: the attempts, the dead ends, where the AI got stuck and the PI unblocked it, the visualisation loop (SVG pages → readings → leaves) |
| [`04_related_work.md`](04_related_work.md) | anyone placing this work | a survey of recent AI-assisted mathematics results categorised by interaction depth, who managed the AI, the human's training, what the human contributed, and verification; the direct contribution statement is its lead |
| [`05_status_sheet.md`](05_status_sheet.md) | **the canonical reference** | ONE table pinned to a commit: every result and every unfinished family, with columns result / proved in prose / exact checker (verifier + sha) / concrete Lean theorem or replay / open dependency. Nothing in the repo may state a status that disagrees with this file |
| [`06_compute_plan.md`](06_compute_plan.md) | anyone asked to fund or review the campaign | one page: reconciled components, hardware normalisation, the $300–500 calibration pilot, replay allowance, stop conditions, the ceiling, and the E1–E5 exit criteria for "only compute remains" |

`sources/` holds raw material copied from outside the repo (the coordinator's dated lab memory, the drawing rules,
the standing priority rules); `figures/` holds the figures the documents cite (copied, not linked, so the
directory is self-contained). Primary in-repo sources: `LOG.md`, `attempts/REGISTRY.md`, `docs/known_results.md`,
`docs/residue_ledger.md`, `docs/budget.md`, `docs/proofs/*.md`, `docs/paper/outline.md`, `lean/`.

Conventions: every mathematical claim carries its status tag — **[T]** proved in prose, **[L]** Lean-checked,
**[C]** certificate-backed *under a named verifier and its sha*, **[P]** pending compute with a priced route,
**[O]** an open proof obligation with no priced route, **[M]** measured, **[S]** supported. The legend is stated
in full at the top of [`01_summary.md`](01_summary.md) and [`05_status_sheet.md`](05_status_sheet.md) and is
identical in both. Attempt notes older than 2026-09-09 sometimes use [C] for "open"; in `writeup/` it never does.
Every timeline claim cites the attempt id (A###) and the date; nothing is stated as done that is not.
