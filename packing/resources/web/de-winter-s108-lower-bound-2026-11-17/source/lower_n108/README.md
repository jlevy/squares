# Lower bound for n = 108 and n = 109

A square that contains 108 unit squares has side at least

    1700799526134255846599/159999384348528500000 = 10.630037940829...

The same bound holds for 109 unit squares, because a packing of 109 contains a packing of 108. The Squares Project listed the lower bound 10.62 for n = 108 on 17 November 2026 (T-216, Hiroaki Hosono). The improvement is 0.0100.

## Construction

The certificate starts from Hosono's measure for 108 squares in a square of side 10.62. Every rectangle coordinate is multiplied by 1063/1062 and every mass is kept, which gives a measure of total mass 107.99999 in a square of side 10.63. For each of 401 directions, with half-angle tangents r·83/80000 (r = 0, …, 400), the Squares Project verifier certifies that every closed square of side 0.99896 at that direction, with its centre in the allowed range, captures mass at least one. A short rational argument then enlarges the side from 10.63 to the bound above. The proof is on one page in `proof_n108.pdf`.

## Files

- `proof_n108.pdf`: the proof.
- `evidence/Hosono_n108.json.gz`: Hosono's original measure (Squares Project, T-216).
- `evidence/n108_measure.json.gz`: the rescaled measure.
- `evidence/direction_runs/`: the unmodified outputs of the Squares Project verifier `sqverify_fast` for all 401 directions, in twelve ranges. Together they visited 266,337,510 branch-and-bound nodes.
- `evidence/SOUNDNESS.md`, `evidence/squares-project-license.txt`: the soundness argument and licence of the verifier, copied from jlevy/squares.
- `stretch_measure.py`: builds the rescaled measure from Hosono's measure.
- `check_lower.py`: audit in exact rational arithmetic. Run `python3 check_lower.py` (Python 3.9 or later, standard library only). It checks the measure, the rescaling, the input and source hashes, one verified record per direction, an independent integration at the axis direction, and the final enlargement. Output in `lower_checks.txt`.
- `replay_lower.sh`: recomputes all 401 directions from scratch with the verifier (Rust 1.98 or later, Cargo), then runs the audit.
- `sqverify_fast/`: the verifier source of jlevy/squares at commit f9ddfeeef9070ede581142154ab992149b278ab0, under the licence of that repository.
- `SHA256SUMS`: checksums.

## Method and AI assistance

The rescaling, the computation and the proof were produced with GPT-6.2 Astra (OpenAI). The repository files and checks were produced with Claude (Anthropic). Both worked under the direction of Joost de Winter.
