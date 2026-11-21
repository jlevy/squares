# Review evidence for the 305-square packing


The corrected witness preserves the original 305 squares. `n305_31_quarter_turns.json` is a separate packing variant at the identical rational side. The third witness, `n305_37_aligned.json`, makes all 36 near-axis squares and square 43 exactly axis-aligned at the same side. It uses the nine one-dimensional rational center shifts in `axis-alignment-moves.csv`. Six move upward and three to the right. Square IDs in the reply and both CSVs start at one. The two source archives for the earlier stages were `squaremath_four_hour_20261118.zip` (member `upper/305/exact.json`) and `squaremath_adaptive_four_hours_20261118.zip` (member `upper/n305/packing.json.gz`).

Run from this directory with Python 3.10 or later. The corrected-witness reader also uses PyYAML.

    python3 -B check_corrected.py
    python3 -B quarter_turns.py
    python3 -B recover_enclosure.py
    python3 -B verify_exact.py n305_31_quarter_turns.json
    python3 -B check_area.py n305_31_quarter_turns.json
    python3 -B check_alignment.py
    python3 -B verify_exact.py n305_37_aligned.json
    python3 -B check_area.py n305_37_aligned.json

For the refitted packing, a linear program nominated the moving centers and a separating axis for each close pair. An exact rational linear-arithmetic solver found shifts satisfying the selected pair and wall constraints. The final shifts are decimal multiples of 10⁻⁸³. The nine rational shifts and specified orientations reproduce the entire submitted file from the original packing. The offline checker verifies it without an optimization or constraint solver.

## Why nine movements are necessary locally

Fix the enclosing side and the directions of every square. The 36 near-axis squares are upright. Square 43 can either keep its original direction or be upright. Each center coordinate may change by at most 2 × 10⁻¹¹. Under each of these two orientation choices the minimum number of moved centers is nine.

For each of the 17 groups in `local-move-conflicts.json`, the checker retains only the listed nearby tiles. Holding the group’s original centers fixed makes this smaller packing infeasible even while every other retained center can move anywhere in its coordinate box. For each pair of tiles it tests separation along both signed normals of each tile, giving a disjunction of exact rational linear inequalities. Walls and coordinate limits give further rational inequalities. Z3 checks each of the 34 small feasibility problems with exact linear arithmetic. The Python checker enumerates the ways to hit every group and finds that at least nine centers must move. The explicit witness establishes sufficiency. No restriction on permissible center movements beyond the stated coordinate box is imposed.

    python3 -B check_minimum_moves.py

This additional lower-bound check requires the Z3 executable or its shared library. Verifying the packing coordinates themselves uses the earlier commands.

The two reviewer modules are the project’s `r1052_reader.py` and `r1052_poses.py` from its [review packet](https://github.com/jlevy/squares/tree/main/packing/resources/web/de-winter-n305-1052-review-2026-11-20/programs). The original JSON and the two geometry checks come from [Joost de Winter’s public certificate](https://github.com/JoostdeWinter/square-packing/tree/db8efcb6bf05906e977bc62f1f6d8ccfcaa296ef/n305). The arrangement is due to Tomáš Kodaj and JoeGun. This follow-up was prepared with OpenAI Codex.