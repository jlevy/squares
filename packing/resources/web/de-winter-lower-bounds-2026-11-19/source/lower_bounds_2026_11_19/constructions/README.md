# Building stronger exclusion measures

The first strip construction for 114 squares starts from the 73-square measure on the board of side 8.826 in the earlier submission for issue 1039. Mark the unit interval centered on each coordinate axis. Copy that middle interval three times in succession on each axis and translate the exterior pieces so that they meet. A source rectangle crossing a cut contributes in proportion to the area on each side. This increases the side by two to 10.826. A common multiplier gives total mass 113.999999.

The accompanying n114-strip.png shows those two measures. The original certificate for 10.826 remains in strip_n114. To recompute every center and angle for it, run `python3 proof/replay.py constructions/strip_n114 --workers 4 --controls` from the packet root.

The strongest direct result for each square count is listed in ../lower_bounds.csv. Some improved measures mix independently transplanted donor measures. Each component is moved to the new board, divided by its own mass and assigned the integer mixing weight recorded in mix_cases.json. The compact variants round coordinates to the nearest billionth and component masses to units of 10⁻¹³ before the final exact normalization. All reported bounds use the resulting exact rational rectangle weights.

Run `python3 verify.py` in this directory to reconstruct the single-source strip measures and `python3 mixture_rebuild.py` to reproduce the mixtures. The board-wide proofs are in ../proof. The input filenames and their digests identify the specific earlier de Winter and Hosono measures.

Source https://github.com/jlevy/squares/issues/1039

## Included mixtures

| Target count | Source board side after transplantation | Original square counts | Integer mixture weights |
|---:|---:|---|---|
| 109 | 10703/1000 | 109, 89 | 87676731, 12323269 |
| 114 | 87/8 | 92, 93, 74 | 9184590, 73911664, 16903746 |
| 115 | 87/8 | 74, 92, 93 | 21045448, 3777258, 75177294 |
| 130 | 11491/1000 | 105, 86, 105 | 27881767, 17448336, 54669897 |
| 131 | 11551/1000 | 106, 87, 107 | 51291519, 3704884, 45003597 |
| 134 | 2339/200 | 89, 109 | 23030766, 76969234 |
| 135 | 11747/1000 | 112, 110, 90 | 43816770, 24648413, 31534817 |
| 137 | 1478/125 | 73, 92, 92 | 59652415, 12998500, 27349085 |

The width-adjusted rectangle measures are reconstructed from their inputs by smooth_check.py. Each thin interval is widened about its midpoint and kept inside the board, preserving its assigned mass.
