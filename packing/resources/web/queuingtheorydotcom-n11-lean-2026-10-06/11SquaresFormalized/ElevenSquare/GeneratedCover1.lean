import ElevenSquare.CoverChecks

/-! Generated exact dyadic covering witness. Every numerical premise is
proved by kernel-checked `norm_num`; no external PASS flag is assumed. -/
namespace ElevenSquare
set_option maxHeartbeats 0
set_option linter.unnecessarySeqFocus false

theorem coverQ1_0 : BoxCovered (1 / 2) 0 (1 / 32) := by
  apply boxCovered_leaf (1 / 2) 0 (1 / 32) (186601 / 500000) (45503 / 1000000) (4939 / 31250) (45503 / 1000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_1 : BoxCovered (17 / 32) 0 (1 / 32) := by
  apply boxCovered_leaf (17 / 32) 0 (1 / 32) (1267243 / 2000000) (34689 / 250000) (204743 / 2000000) (34689 / 250000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_2 : BoxCovered (1 / 2) (1 / 32) (1 / 32) := by
  apply boxCovered_leaf (1 / 2) (1 / 32) (1 / 32) (186601 / 500000) (45503 / 1000000) (4939 / 31250) (16997 / 1000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_3 : BoxCovered (17 / 32) (1 / 32) (1 / 32) := by
  apply boxCovered_leaf (17 / 32) (1 / 32) (1 / 32) (1267243 / 2000000) (34689 / 250000) (204743 / 2000000) (53753 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_4 : BoxCovered (1 / 2) 0 (1 / 16) := by
  apply boxCovered_split
  · convert coverQ1_0 using 1 <;> norm_num
  · convert coverQ1_1 using 1 <;> norm_num
  · convert coverQ1_2 using 1 <;> norm_num
  · convert coverQ1_3 using 1 <;> norm_num

theorem coverQ1_5 : BoxCovered (9 / 16) 0 (1 / 16) := by
  apply boxCovered_leaf (9 / 16) 0 (1 / 16) (1267243 / 2000000) (34689 / 250000) (142243 / 2000000) (34689 / 250000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_6 : BoxCovered (1 / 2) (1 / 16) (1 / 16) := by
  apply boxCovered_leaf (1 / 2) (1 / 16) (1 / 16) (1267243 / 2000000) (34689 / 250000) (267243 / 2000000) (2383 / 31250) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_7 : BoxCovered (9 / 16) (1 / 16) (1 / 16) := by
  apply boxCovered_leaf (9 / 16) (1 / 16) (1 / 16) (1267243 / 2000000) (34689 / 250000) (142243 / 2000000) (2383 / 31250) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_8 : BoxCovered (1 / 2) 0 (1 / 8) := by
  apply boxCovered_split
  · convert coverQ1_4 using 1 <;> norm_num
  · convert coverQ1_5 using 1 <;> norm_num
  · convert coverQ1_6 using 1 <;> norm_num
  · convert coverQ1_7 using 1 <;> norm_num

theorem coverQ1_9 : BoxCovered (5 / 8) 0 (1 / 16) := by
  apply boxCovered_leaf (5 / 8) 0 (1 / 16) (1267243 / 2000000) (34689 / 250000) (107757 / 2000000) (34689 / 250000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_10 : BoxCovered (11 / 16) 0 (1 / 32) := by
  apply boxCovered_leaf (11 / 16) 0 (1 / 32) (1267243 / 2000000) (34689 / 250000) (170257 / 2000000) (34689 / 250000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_11 : BoxCovered (23 / 32) 0 (1 / 64) := by
  apply boxCovered_leaf (23 / 32) 0 (1 / 64) (1267243 / 2000000) (34689 / 250000) (201507 / 2000000) (34689 / 250000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_12 : BoxCovered (47 / 64) 0 (1 / 64) := by
  apply boxCovered_leaf (47 / 64) 0 (1 / 64) (1731123 / 2000000) (25701 / 250000) (262373 / 2000000) (25701 / 250000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_13 : BoxCovered (23 / 32) (1 / 64) (1 / 64) := by
  apply boxCovered_leaf (23 / 32) (1 / 64) (1 / 64) (1267243 / 2000000) (34689 / 250000) (201507 / 2000000) (123131 / 1000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_14 : BoxCovered (47 / 64) (1 / 64) (1 / 64) := by
  apply boxCovered_leaf (47 / 64) (1 / 64) (1 / 64) (1267243 / 2000000) (34689 / 250000) (232757 / 2000000) (123131 / 1000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_15 : BoxCovered (23 / 32) 0 (1 / 32) := by
  apply boxCovered_split
  · convert coverQ1_11 using 1 <;> norm_num
  · convert coverQ1_12 using 1 <;> norm_num
  · convert coverQ1_13 using 1 <;> norm_num
  · convert coverQ1_14 using 1 <;> norm_num

theorem coverQ1_16 : BoxCovered (11 / 16) (1 / 32) (1 / 32) := by
  apply boxCovered_leaf (11 / 16) (1 / 32) (1 / 32) (1267243 / 2000000) (34689 / 250000) (170257 / 2000000) (53753 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_17 : BoxCovered (23 / 32) (1 / 32) (1 / 32) := by
  apply boxCovered_leaf (23 / 32) (1 / 32) (1 / 32) (1267243 / 2000000) (34689 / 250000) (232757 / 2000000) (53753 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_18 : BoxCovered (11 / 16) 0 (1 / 16) := by
  apply boxCovered_split
  · convert coverQ1_10 using 1 <;> norm_num
  · convert coverQ1_15 using 1 <;> norm_num
  · convert coverQ1_16 using 1 <;> norm_num
  · convert coverQ1_17 using 1 <;> norm_num

theorem coverQ1_19 : BoxCovered (5 / 8) (1 / 16) (1 / 16) := by
  apply boxCovered_leaf (5 / 8) (1 / 16) (1 / 16) (1267243 / 2000000) (34689 / 250000) (107757 / 2000000) (2383 / 31250) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_20 : BoxCovered (11 / 16) (1 / 16) (1 / 16) := by
  apply boxCovered_leaf (11 / 16) (1 / 16) (1 / 16) (1267243 / 2000000) (34689 / 250000) (232757 / 2000000) (2383 / 31250) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_21 : BoxCovered (5 / 8) 0 (1 / 8) := by
  apply boxCovered_split
  · convert coverQ1_9 using 1 <;> norm_num
  · convert coverQ1_18 using 1 <;> norm_num
  · convert coverQ1_19 using 1 <;> norm_num
  · convert coverQ1_20 using 1 <;> norm_num

theorem coverQ1_22 : BoxCovered (1 / 2) (1 / 8) (1 / 16) := by
  apply boxCovered_leaf (1 / 2) (1 / 8) (1 / 16) (1267243 / 2000000) (34689 / 250000) (267243 / 2000000) (6093 / 125000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_23 : BoxCovered (9 / 16) (1 / 8) (1 / 16) := by
  apply boxCovered_leaf (9 / 16) (1 / 8) (1 / 16) (1267243 / 2000000) (34689 / 250000) (142243 / 2000000) (6093 / 125000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_24 : BoxCovered (1 / 2) (3 / 16) (1 / 32) := by
  apply boxCovered_leaf (1 / 2) (3 / 16) (1 / 32) (1267243 / 2000000) (34689 / 250000) (267243 / 2000000) (39997 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_25 : BoxCovered (17 / 32) (3 / 16) (1 / 32) := by
  apply boxCovered_leaf (17 / 32) (3 / 16) (1 / 32) (1267243 / 2000000) (34689 / 250000) (204743 / 2000000) (39997 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_26 : BoxCovered (1 / 2) (7 / 32) (1 / 64) := by
  apply boxCovered_leaf (1 / 2) (7 / 32) (1 / 64) (1267243 / 2000000) (34689 / 250000) (267243 / 2000000) (95619 / 1000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_27 : BoxCovered (33 / 64) (7 / 32) (1 / 64) := by
  apply boxCovered_leaf (33 / 64) (7 / 32) (1 / 64) (1267243 / 2000000) (34689 / 250000) (235993 / 2000000) (95619 / 1000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_28 : BoxCovered (1 / 2) (15 / 64) (1 / 64) := by
  apply boxCovered_leaf (1 / 2) (15 / 64) (1 / 64) (742311 / 2000000) (312933 / 1000000) (288939 / 2000000) (39279 / 500000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_29 : BoxCovered (33 / 64) (15 / 64) (1 / 64) := by
  apply boxCovered_leaf (33 / 64) (15 / 64) (1 / 64) (1267243 / 2000000) (34689 / 250000) (235993 / 2000000) (27811 / 250000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_30 : BoxCovered (1 / 2) (7 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ1_26 using 1 <;> norm_num
  · convert coverQ1_27 using 1 <;> norm_num
  · convert coverQ1_28 using 1 <;> norm_num
  · convert coverQ1_29 using 1 <;> norm_num

theorem coverQ1_31 : BoxCovered (17 / 32) (7 / 32) (1 / 32) := by
  apply boxCovered_leaf (17 / 32) (7 / 32) (1 / 32) (1267243 / 2000000) (34689 / 250000) (204743 / 2000000) (27811 / 250000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_32 : BoxCovered (1 / 2) (3 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ1_24 using 1 <;> norm_num
  · convert coverQ1_25 using 1 <;> norm_num
  · convert coverQ1_30 using 1 <;> norm_num
  · convert coverQ1_31 using 1 <;> norm_num

theorem coverQ1_33 : BoxCovered (9 / 16) (3 / 16) (1 / 16) := by
  apply boxCovered_leaf (9 / 16) (3 / 16) (1 / 16) (1267243 / 2000000) (34689 / 250000) (142243 / 2000000) (27811 / 250000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_34 : BoxCovered (1 / 2) (1 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ1_22 using 1 <;> norm_num
  · convert coverQ1_23 using 1 <;> norm_num
  · convert coverQ1_32 using 1 <;> norm_num
  · convert coverQ1_33 using 1 <;> norm_num

theorem coverQ1_35 : BoxCovered (5 / 8) (1 / 8) (1 / 8) := by
  apply boxCovered_leaf (5 / 8) (1 / 8) (1 / 8) (1267243 / 2000000) (34689 / 250000) (232757 / 2000000) (27811 / 250000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_36 : BoxCovered (1 / 2) 0 (1 / 4) := by
  apply boxCovered_split
  · convert coverQ1_8 using 1 <;> norm_num
  · convert coverQ1_21 using 1 <;> norm_num
  · convert coverQ1_34 using 1 <;> norm_num
  · convert coverQ1_35 using 1 <;> norm_num

theorem coverQ1_37 : BoxCovered (3 / 4) 0 (1 / 8) := by
  apply boxCovered_leaf (3 / 4) 0 (1 / 8) (1731123 / 2000000) (25701 / 250000) (231123 / 2000000) (25701 / 250000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_38 : BoxCovered (7 / 8) 0 (1 / 8) := by
  apply boxCovered_leaf (7 / 8) 0 (1 / 8) (1731123 / 2000000) (25701 / 250000) (268877 / 2000000) (25701 / 250000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_39 : BoxCovered (3 / 4) (1 / 8) (1 / 16) := by
  apply boxCovered_leaf (3 / 4) (1 / 8) (1 / 16) (1731123 / 2000000) (25701 / 250000) (231123 / 2000000) (10587 / 125000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_40 : BoxCovered (13 / 16) (1 / 8) (1 / 16) := by
  apply boxCovered_leaf (13 / 16) (1 / 8) (1 / 16) (1731123 / 2000000) (25701 / 250000) (106123 / 2000000) (10587 / 125000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_41 : BoxCovered (3 / 4) (3 / 16) (1 / 32) := by
  apply boxCovered_leaf (3 / 4) (3 / 16) (1 / 32) (1267243 / 2000000) (34689 / 250000) (295257 / 2000000) (39997 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_42 : BoxCovered (25 / 32) (3 / 16) (1 / 32) := by
  apply boxCovered_leaf (25 / 32) (3 / 16) (1 / 32) (1731123 / 2000000) (25701 / 250000) (168623 / 2000000) (57973 / 500000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_43 : BoxCovered (3 / 4) (7 / 32) (1 / 64) := by
  apply boxCovered_leaf (3 / 4) (7 / 32) (1 / 64) (1267243 / 2000000) (34689 / 250000) (264007 / 2000000) (95619 / 1000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_44 : BoxCovered (49 / 64) (7 / 32) (1 / 64) := by
  apply boxCovered_leaf (49 / 64) (7 / 32) (1 / 64) (1731123 / 2000000) (25701 / 250000) (199873 / 2000000) (131571 / 1000000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_45 : BoxCovered (3 / 4) (15 / 64) (1 / 64) := by
  apply boxCovered_leaf (3 / 4) (15 / 64) (1 / 64) (1267243 / 2000000) (34689 / 250000) (264007 / 2000000) (27811 / 250000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_46 : BoxCovered (49 / 64) (15 / 64) (1 / 64) := by
  apply boxCovered_leaf (49 / 64) (15 / 64) (1 / 64) (445439 / 500000) (167763 / 500000) (125253 / 1000000) (101151 / 1000000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_47 : BoxCovered (3 / 4) (7 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ1_43 using 1 <;> norm_num
  · convert coverQ1_44 using 1 <;> norm_num
  · convert coverQ1_45 using 1 <;> norm_num
  · convert coverQ1_46 using 1 <;> norm_num

theorem coverQ1_48 : BoxCovered (25 / 32) (7 / 32) (1 / 32) := by
  apply boxCovered_leaf (25 / 32) (7 / 32) (1 / 32) (1731123 / 2000000) (25701 / 250000) (168623 / 2000000) (36799 / 250000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_49 : BoxCovered (3 / 4) (3 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ1_41 using 1 <;> norm_num
  · convert coverQ1_42 using 1 <;> norm_num
  · convert coverQ1_47 using 1 <;> norm_num
  · convert coverQ1_48 using 1 <;> norm_num

theorem coverQ1_50 : BoxCovered (13 / 16) (3 / 16) (1 / 16) := by
  apply boxCovered_leaf (13 / 16) (3 / 16) (1 / 16) (1731123 / 2000000) (25701 / 250000) (106123 / 2000000) (36799 / 250000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_51 : BoxCovered (3 / 4) (1 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ1_39 using 1 <;> norm_num
  · convert coverQ1_40 using 1 <;> norm_num
  · convert coverQ1_49 using 1 <;> norm_num
  · convert coverQ1_50 using 1 <;> norm_num

theorem coverQ1_52 : BoxCovered (7 / 8) (1 / 8) (1 / 16) := by
  apply boxCovered_leaf (7 / 8) (1 / 8) (1 / 16) (1731123 / 2000000) (25701 / 250000) (143877 / 2000000) (10587 / 125000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_53 : BoxCovered (15 / 16) (1 / 8) (1 / 16) := by
  apply boxCovered_leaf (15 / 16) (1 / 8) (1 / 16) (1731123 / 2000000) (25701 / 250000) (268877 / 2000000) (10587 / 125000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_54 : BoxCovered (7 / 8) (3 / 16) (1 / 16) := by
  apply boxCovered_leaf (7 / 8) (3 / 16) (1 / 16) (1731123 / 2000000) (25701 / 250000) (143877 / 2000000) (36799 / 250000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_55 : BoxCovered (15 / 16) (3 / 16) (1 / 32) := by
  apply boxCovered_leaf (15 / 16) (3 / 16) (1 / 32) (1731123 / 2000000) (25701 / 250000) (206377 / 2000000) (57973 / 500000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_56 : BoxCovered (31 / 32) (3 / 16) (1 / 64) := by
  apply boxCovered_leaf (31 / 32) (3 / 16) (1 / 64) (1731123 / 2000000) (25701 / 250000) (237627 / 2000000) (100321 / 1000000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_57 : BoxCovered (63 / 64) (3 / 16) (1 / 64) := by
  apply boxCovered_leaf (63 / 64) (3 / 16) (1 / 64) (1731123 / 2000000) (25701 / 250000) (268877 / 2000000) (100321 / 1000000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_58 : BoxCovered (31 / 32) (13 / 64) (1 / 64) := by
  apply boxCovered_leaf (31 / 32) (13 / 64) (1 / 64) (1731123 / 2000000) (25701 / 250000) (237627 / 2000000) (57973 / 500000) ⟨3, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_59 : BoxCovered (63 / 64) (13 / 64) (1 / 64) := by
  apply boxCovered_leaf (63 / 64) (13 / 64) (1 / 64) (445439 / 500000) (167763 / 500000) (54561 / 500000) (132401 / 1000000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_60 : BoxCovered (31 / 32) (3 / 16) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ1_56 using 1 <;> norm_num
  · convert coverQ1_57 using 1 <;> norm_num
  · convert coverQ1_58 using 1 <;> norm_num
  · convert coverQ1_59 using 1 <;> norm_num

theorem coverQ1_61 : BoxCovered (15 / 16) (7 / 32) (1 / 32) := by
  apply boxCovered_leaf (15 / 16) (7 / 32) (1 / 32) (445439 / 500000) (167763 / 500000) (4867 / 62500) (14597 / 125000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_62 : BoxCovered (31 / 32) (7 / 32) (1 / 32) := by
  apply boxCovered_leaf (31 / 32) (7 / 32) (1 / 32) (445439 / 500000) (167763 / 500000) (54561 / 500000) (14597 / 125000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_63 : BoxCovered (15 / 16) (3 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ1_55 using 1 <;> norm_num
  · convert coverQ1_60 using 1 <;> norm_num
  · convert coverQ1_61 using 1 <;> norm_num
  · convert coverQ1_62 using 1 <;> norm_num

theorem coverQ1_64 : BoxCovered (7 / 8) (1 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ1_52 using 1 <;> norm_num
  · convert coverQ1_53 using 1 <;> norm_num
  · convert coverQ1_54 using 1 <;> norm_num
  · convert coverQ1_63 using 1 <;> norm_num

theorem coverQ1_65 : BoxCovered (3 / 4) 0 (1 / 4) := by
  apply boxCovered_split
  · convert coverQ1_37 using 1 <;> norm_num
  · convert coverQ1_38 using 1 <;> norm_num
  · convert coverQ1_51 using 1 <;> norm_num
  · convert coverQ1_64 using 1 <;> norm_num

theorem coverQ1_66 : BoxCovered (1 / 2) (1 / 4) (1 / 32) := by
  apply boxCovered_leaf (1 / 2) (1 / 4) (1 / 32) (742311 / 2000000) (312933 / 1000000) (320189 / 2000000) (62933 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_67 : BoxCovered (17 / 32) (1 / 4) (1 / 64) := by
  apply boxCovered_leaf (17 / 32) (1 / 4) (1 / 64) (1267243 / 2000000) (34689 / 250000) (204743 / 2000000) (126869 / 1000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_68 : BoxCovered (35 / 64) (1 / 4) (1 / 64) := by
  apply boxCovered_leaf (35 / 64) (1 / 4) (1 / 64) (1267243 / 2000000) (34689 / 250000) (173493 / 2000000) (126869 / 1000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_69 : BoxCovered (17 / 32) (17 / 64) (1 / 128) := by
  apply boxCovered_leaf (17 / 32) (17 / 64) (1 / 128) (1267243 / 2000000) (34689 / 250000) (204743 / 2000000) (269363 / 2000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_70 : BoxCovered (69 / 128) (17 / 64) (1 / 128) := by
  apply boxCovered_leaf (69 / 128) (17 / 64) (1 / 128) (1267243 / 2000000) (34689 / 250000) (94559 / 1000000) (269363 / 2000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_71 : BoxCovered (17 / 32) (35 / 128) (1 / 128) := by
  apply boxCovered_leaf (17 / 32) (35 / 128) (1 / 128) (742311 / 2000000) (312933 / 1000000) (167907 / 1000000) (78991 / 2000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_72 : BoxCovered (69 / 128) (35 / 128) (1 / 128) := by
  apply boxCovered_leaf (69 / 128) (35 / 128) (1 / 128) (1267243 / 2000000) (34689 / 250000) (94559 / 1000000) (71247 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_73 : BoxCovered (17 / 32) (17 / 64) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ1_69 using 1 <;> norm_num
  · convert coverQ1_70 using 1 <;> norm_num
  · convert coverQ1_71 using 1 <;> norm_num
  · convert coverQ1_72 using 1 <;> norm_num

theorem coverQ1_74 : BoxCovered (35 / 64) (17 / 64) (1 / 64) := by
  apply boxCovered_leaf (35 / 64) (17 / 64) (1 / 64) (1267243 / 2000000) (34689 / 250000) (173493 / 2000000) (71247 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_75 : BoxCovered (17 / 32) (1 / 4) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ1_67 using 1 <;> norm_num
  · convert coverQ1_68 using 1 <;> norm_num
  · convert coverQ1_73 using 1 <;> norm_num
  · convert coverQ1_74 using 1 <;> norm_num

theorem coverQ1_76 : BoxCovered (1 / 2) (9 / 32) (1 / 32) := by
  apply boxCovered_leaf (1 / 2) (9 / 32) (1 / 32) (742311 / 2000000) (312933 / 1000000) (320189 / 2000000) (31683 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_77 : BoxCovered (17 / 32) (9 / 32) (1 / 32) := by
  apply boxCovered_leaf (17 / 32) (9 / 32) (1 / 32) (635257 / 1000000) (166409 / 400000) (104007 / 1000000) (53909 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_78 : BoxCovered (1 / 2) (1 / 4) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ1_66 using 1 <;> norm_num
  · convert coverQ1_75 using 1 <;> norm_num
  · convert coverQ1_76 using 1 <;> norm_num
  · convert coverQ1_77 using 1 <;> norm_num

theorem coverQ1_79 : BoxCovered (9 / 16) (1 / 4) (1 / 32) := by
  apply boxCovered_leaf (9 / 16) (1 / 4) (1 / 32) (1267243 / 2000000) (34689 / 250000) (142243 / 2000000) (71247 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_80 : BoxCovered (19 / 32) (1 / 4) (1 / 32) := by
  apply boxCovered_leaf (19 / 32) (1 / 4) (1 / 32) (1267243 / 2000000) (34689 / 250000) (79743 / 2000000) (71247 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_81 : BoxCovered (9 / 16) (9 / 32) (1 / 32) := by
  apply boxCovered_leaf (9 / 16) (9 / 32) (1 / 32) (635257 / 1000000) (166409 / 400000) (72757 / 1000000) (53909 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_82 : BoxCovered (19 / 32) (9 / 32) (1 / 32) := by
  apply boxCovered_leaf (19 / 32) (9 / 32) (1 / 32) (635257 / 1000000) (166409 / 400000) (41507 / 1000000) (53909 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_83 : BoxCovered (9 / 16) (1 / 4) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ1_79 using 1 <;> norm_num
  · convert coverQ1_80 using 1 <;> norm_num
  · convert coverQ1_81 using 1 <;> norm_num
  · convert coverQ1_82 using 1 <;> norm_num

theorem coverQ1_84 : BoxCovered (1 / 2) (5 / 16) (1 / 16) := by
  apply boxCovered_leaf (1 / 2) (5 / 16) (1 / 16) (635257 / 1000000) (166409 / 400000) (135257 / 1000000) (41409 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_85 : BoxCovered (9 / 16) (5 / 16) (1 / 16) := by
  apply boxCovered_leaf (9 / 16) (5 / 16) (1 / 16) (635257 / 1000000) (166409 / 400000) (72757 / 1000000) (41409 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_86 : BoxCovered (1 / 2) (1 / 4) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ1_78 using 1 <;> norm_num
  · convert coverQ1_83 using 1 <;> norm_num
  · convert coverQ1_84 using 1 <;> norm_num
  · convert coverQ1_85 using 1 <;> norm_num

theorem coverQ1_87 : BoxCovered (5 / 8) (1 / 4) (1 / 32) := by
  apply boxCovered_leaf (5 / 8) (1 / 4) (1 / 32) (1267243 / 2000000) (34689 / 250000) (45257 / 2000000) (71247 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_88 : BoxCovered (21 / 32) (1 / 4) (1 / 32) := by
  apply boxCovered_leaf (21 / 32) (1 / 4) (1 / 32) (1267243 / 2000000) (34689 / 250000) (107757 / 2000000) (71247 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_89 : BoxCovered (5 / 8) (9 / 32) (1 / 32) := by
  apply boxCovered_leaf (5 / 8) (9 / 32) (1 / 32) (635257 / 1000000) (166409 / 400000) (20993 / 1000000) (53909 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_90 : BoxCovered (21 / 32) (9 / 32) (1 / 32) := by
  apply boxCovered_leaf (21 / 32) (9 / 32) (1 / 32) (635257 / 1000000) (166409 / 400000) (52243 / 1000000) (53909 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_91 : BoxCovered (5 / 8) (1 / 4) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ1_87 using 1 <;> norm_num
  · convert coverQ1_88 using 1 <;> norm_num
  · convert coverQ1_89 using 1 <;> norm_num
  · convert coverQ1_90 using 1 <;> norm_num

theorem coverQ1_92 : BoxCovered (11 / 16) (1 / 4) (1 / 32) := by
  apply boxCovered_leaf (11 / 16) (1 / 4) (1 / 32) (1267243 / 2000000) (34689 / 250000) (170257 / 2000000) (71247 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_93 : BoxCovered (23 / 32) (1 / 4) (1 / 64) := by
  apply boxCovered_leaf (23 / 32) (1 / 4) (1 / 64) (1267243 / 2000000) (34689 / 250000) (201507 / 2000000) (126869 / 1000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_94 : BoxCovered (47 / 64) (1 / 4) (1 / 64) := by
  apply boxCovered_leaf (47 / 64) (1 / 4) (1 / 64) (1267243 / 2000000) (34689 / 250000) (232757 / 2000000) (126869 / 1000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_95 : BoxCovered (23 / 32) (17 / 64) (1 / 128) := by
  apply boxCovered_leaf (23 / 32) (17 / 64) (1 / 128) (1267243 / 2000000) (34689 / 250000) (92941 / 1000000) (269363 / 2000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_96 : BoxCovered (93 / 128) (17 / 64) (1 / 128) := by
  apply boxCovered_leaf (93 / 128) (17 / 64) (1 / 128) (1267243 / 2000000) (34689 / 250000) (201507 / 2000000) (269363 / 2000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_97 : BoxCovered (23 / 32) (35 / 128) (1 / 128) := by
  apply boxCovered_leaf (23 / 32) (35 / 128) (1 / 128) (1267243 / 2000000) (34689 / 250000) (92941 / 1000000) (71247 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_98 : BoxCovered (93 / 128) (35 / 128) (1 / 256) := by
  apply boxCovered_leaf (93 / 128) (35 / 128) (1 / 256) (1267243 / 2000000) (34689 / 250000) (387389 / 4000000) (554351 / 4000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_99 : BoxCovered (187 / 256) (35 / 128) (1 / 256) := by
  apply boxCovered_leaf (187 / 256) (35 / 128) (1 / 256) (1267243 / 2000000) (34689 / 250000) (201507 / 2000000) (554351 / 4000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_100 : BoxCovered (93 / 128) (71 / 256) (1 / 256) := by
  apply boxCovered_leaf (93 / 128) (71 / 256) (1 / 256) (1267243 / 2000000) (34689 / 250000) (387389 / 4000000) (71247 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_101 : BoxCovered (187 / 256) (71 / 256) (1 / 256) := by
  apply boxCovered_leaf (187 / 256) (71 / 256) (1 / 256) (635257 / 1000000) (166409 / 400000) (49559 / 500000) (110943 / 800000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_102 : BoxCovered (93 / 128) (35 / 128) (1 / 128) := by
  apply boxCovered_split
  · convert coverQ1_98 using 1 <;> norm_num
  · convert coverQ1_99 using 1 <;> norm_num
  · convert coverQ1_100 using 1 <;> norm_num
  · convert coverQ1_101 using 1 <;> norm_num

theorem coverQ1_103 : BoxCovered (23 / 32) (17 / 64) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ1_95 using 1 <;> norm_num
  · convert coverQ1_96 using 1 <;> norm_num
  · convert coverQ1_97 using 1 <;> norm_num
  · convert coverQ1_102 using 1 <;> norm_num

theorem coverQ1_104 : BoxCovered (47 / 64) (17 / 64) (1 / 64) := by
  apply boxCovered_leaf (47 / 64) (17 / 64) (1 / 64) (445439 / 500000) (167763 / 500000) (156503 / 1000000) (69901 / 1000000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_105 : BoxCovered (23 / 32) (1 / 4) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ1_93 using 1 <;> norm_num
  · convert coverQ1_94 using 1 <;> norm_num
  · convert coverQ1_103 using 1 <;> norm_num
  · convert coverQ1_104 using 1 <;> norm_num

theorem coverQ1_106 : BoxCovered (11 / 16) (9 / 32) (1 / 32) := by
  apply boxCovered_leaf (11 / 16) (9 / 32) (1 / 32) (635257 / 1000000) (166409 / 400000) (83493 / 1000000) (53909 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_107 : BoxCovered (23 / 32) (9 / 32) (1 / 64) := by
  apply boxCovered_leaf (23 / 32) (9 / 32) (1 / 64) (635257 / 1000000) (166409 / 400000) (49559 / 500000) (53909 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_108 : BoxCovered (47 / 64) (9 / 32) (1 / 64) := by
  apply boxCovered_leaf (47 / 64) (9 / 32) (1 / 64) (445439 / 500000) (167763 / 500000) (156503 / 1000000) (13569 / 250000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_109 : BoxCovered (23 / 32) (19 / 64) (1 / 64) := by
  apply boxCovered_leaf (23 / 32) (19 / 64) (1 / 64) (635257 / 1000000) (166409 / 400000) (49559 / 500000) (47659 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_110 : BoxCovered (47 / 64) (19 / 64) (1 / 64) := by
  apply boxCovered_leaf (47 / 64) (19 / 64) (1 / 64) (635257 / 1000000) (166409 / 400000) (114743 / 1000000) (47659 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_111 : BoxCovered (23 / 32) (9 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ1_107 using 1 <;> norm_num
  · convert coverQ1_108 using 1 <;> norm_num
  · convert coverQ1_109 using 1 <;> norm_num
  · convert coverQ1_110 using 1 <;> norm_num

theorem coverQ1_112 : BoxCovered (11 / 16) (1 / 4) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ1_92 using 1 <;> norm_num
  · convert coverQ1_105 using 1 <;> norm_num
  · convert coverQ1_106 using 1 <;> norm_num
  · convert coverQ1_111 using 1 <;> norm_num

theorem coverQ1_113 : BoxCovered (5 / 8) (5 / 16) (1 / 16) := by
  apply boxCovered_leaf (5 / 8) (5 / 16) (1 / 16) (635257 / 1000000) (166409 / 400000) (52243 / 1000000) (41409 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_114 : BoxCovered (11 / 16) (5 / 16) (1 / 16) := by
  apply boxCovered_leaf (11 / 16) (5 / 16) (1 / 16) (635257 / 1000000) (166409 / 400000) (114743 / 1000000) (41409 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_115 : BoxCovered (5 / 8) (1 / 4) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ1_91 using 1 <;> norm_num
  · convert coverQ1_112 using 1 <;> norm_num
  · convert coverQ1_113 using 1 <;> norm_num
  · convert coverQ1_114 using 1 <;> norm_num

theorem coverQ1_116 : BoxCovered (1 / 2) (3 / 8) (1 / 8) := by
  apply boxCovered_leaf (1 / 2) (3 / 8) (1 / 8) (635257 / 1000000) (166409 / 400000) (135257 / 1000000) (33591 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_117 : BoxCovered (5 / 8) (3 / 8) (1 / 8) := by
  apply boxCovered_leaf (5 / 8) (3 / 8) (1 / 8) (635257 / 1000000) (166409 / 400000) (114743 / 1000000) (33591 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_118 : BoxCovered (1 / 2) (1 / 4) (1 / 4) := by
  apply boxCovered_split
  · convert coverQ1_86 using 1 <;> norm_num
  · convert coverQ1_115 using 1 <;> norm_num
  · convert coverQ1_116 using 1 <;> norm_num
  · convert coverQ1_117 using 1 <;> norm_num

theorem coverQ1_119 : BoxCovered (3 / 4) (1 / 4) (1 / 8) := by
  apply boxCovered_leaf (3 / 4) (1 / 4) (1 / 8) (445439 / 500000) (167763 / 500000) (70439 / 500000) (42763 / 500000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_120 : BoxCovered (7 / 8) (1 / 4) (1 / 8) := by
  apply boxCovered_leaf (7 / 8) (1 / 4) (1 / 8) (445439 / 500000) (167763 / 500000) (54561 / 500000) (42763 / 500000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_121 : BoxCovered (3 / 4) (3 / 8) (1 / 32) := by
  apply boxCovered_leaf (3 / 4) (3 / 8) (1 / 32) (635257 / 1000000) (166409 / 400000) (145993 / 1000000) (16409 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_122 : BoxCovered (25 / 32) (3 / 8) (1 / 32) := by
  apply boxCovered_leaf (25 / 32) (3 / 8) (1 / 32) (445439 / 500000) (167763 / 500000) (27407 / 250000) (17681 / 250000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_123 : BoxCovered (3 / 4) (13 / 32) (1 / 32) := by
  apply boxCovered_leaf (3 / 4) (13 / 32) (1 / 32) (635257 / 1000000) (166409 / 400000) (145993 / 1000000) (8591 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_124 : BoxCovered (25 / 32) (13 / 32) (1 / 32) := by
  apply boxCovered_leaf (25 / 32) (13 / 32) (1 / 32) (445439 / 500000) (167763 / 500000) (27407 / 250000) (50987 / 500000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_125 : BoxCovered (3 / 4) (3 / 8) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ1_121 using 1 <;> norm_num
  · convert coverQ1_122 using 1 <;> norm_num
  · convert coverQ1_123 using 1 <;> norm_num
  · convert coverQ1_124 using 1 <;> norm_num

theorem coverQ1_126 : BoxCovered (13 / 16) (3 / 8) (1 / 16) := by
  apply boxCovered_leaf (13 / 16) (3 / 8) (1 / 16) (445439 / 500000) (167763 / 500000) (39189 / 500000) (50987 / 500000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_127 : BoxCovered (3 / 4) (7 / 16) (1 / 32) := by
  apply boxCovered_leaf (3 / 4) (7 / 16) (1 / 32) (635257 / 1000000) (166409 / 400000) (145993 / 1000000) (21091 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_128 : BoxCovered (25 / 32) (7 / 16) (1 / 32) := by
  apply boxCovered_leaf (25 / 32) (7 / 16) (1 / 32) (445439 / 500000) (167763 / 500000) (27407 / 250000) (16653 / 125000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_129 : BoxCovered (3 / 4) (15 / 32) (1 / 32) := by
  apply boxCovered_leaf (3 / 4) (15 / 32) (1 / 32) (635257 / 1000000) (166409 / 400000) (145993 / 1000000) (33591 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_130 : BoxCovered (25 / 32) (15 / 32) (1 / 128) := by
  apply boxCovered_leaf (25 / 32) (15 / 32) (1 / 128) (635257 / 1000000) (166409 / 400000) (307611 / 2000000) (3027 / 50000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_131 : BoxCovered (101 / 128) (15 / 32) (1 / 128) := by
  apply boxCovered_leaf (101 / 128) (15 / 32) (1 / 128) (635257 / 1000000) (166409 / 400000) (80809 / 500000) (3027 / 50000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_132 : BoxCovered (25 / 32) (61 / 128) (1 / 128) := by
  apply boxCovered_leaf (25 / 32) (61 / 128) (1 / 128) (635257 / 1000000) (166409 / 400000) (307611 / 2000000) (27341 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_133 : BoxCovered (101 / 128) (61 / 128) (1 / 128) := by
  apply boxCovered_leaf (101 / 128) (61 / 128) (1 / 128) (1793819 / 2000000) (599621 / 1000000) (107847 / 1000000) (246117 / 2000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_134 : BoxCovered (25 / 32) (15 / 32) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ1_130 using 1 <;> norm_num
  · convert coverQ1_131 using 1 <;> norm_num
  · convert coverQ1_132 using 1 <;> norm_num
  · convert coverQ1_133 using 1 <;> norm_num

theorem coverQ1_135 : BoxCovered (51 / 64) (15 / 32) (1 / 64) := by
  apply boxCovered_leaf (51 / 64) (15 / 32) (1 / 64) (1793819 / 2000000) (599621 / 1000000) (200069 / 2000000) (130871 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_136 : BoxCovered (25 / 32) (31 / 64) (1 / 64) := by
  apply boxCovered_leaf (25 / 32) (31 / 64) (1 / 64) (1793819 / 2000000) (599621 / 1000000) (231319 / 2000000) (57623 / 500000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_137 : BoxCovered (51 / 64) (31 / 64) (1 / 64) := by
  apply boxCovered_leaf (51 / 64) (31 / 64) (1 / 64) (1793819 / 2000000) (599621 / 1000000) (200069 / 2000000) (57623 / 500000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_138 : BoxCovered (25 / 32) (15 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ1_134 using 1 <;> norm_num
  · convert coverQ1_135 using 1 <;> norm_num
  · convert coverQ1_136 using 1 <;> norm_num
  · convert coverQ1_137 using 1 <;> norm_num

theorem coverQ1_139 : BoxCovered (3 / 4) (7 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ1_127 using 1 <;> norm_num
  · convert coverQ1_128 using 1 <;> norm_num
  · convert coverQ1_129 using 1 <;> norm_num
  · convert coverQ1_138 using 1 <;> norm_num

theorem coverQ1_140 : BoxCovered (13 / 16) (7 / 16) (1 / 32) := by
  apply boxCovered_leaf (13 / 16) (7 / 16) (1 / 32) (445439 / 500000) (167763 / 500000) (39189 / 500000) (16653 / 125000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_141 : BoxCovered (27 / 32) (7 / 16) (1 / 32) := by
  apply boxCovered_leaf (27 / 32) (7 / 16) (1 / 32) (445439 / 500000) (167763 / 500000) (5891 / 125000) (16653 / 125000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_142 : BoxCovered (13 / 16) (15 / 32) (1 / 32) := by
  apply boxCovered_leaf (13 / 16) (15 / 32) (1 / 32) (1793819 / 2000000) (599621 / 1000000) (168819 / 2000000) (130871 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_143 : BoxCovered (27 / 32) (15 / 32) (1 / 32) := by
  apply boxCovered_leaf (27 / 32) (15 / 32) (1 / 32) (445439 / 500000) (167763 / 500000) (5891 / 125000) (82237 / 500000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_144 : BoxCovered (13 / 16) (7 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ1_140 using 1 <;> norm_num
  · convert coverQ1_141 using 1 <;> norm_num
  · convert coverQ1_142 using 1 <;> norm_num
  · convert coverQ1_143 using 1 <;> norm_num

theorem coverQ1_145 : BoxCovered (3 / 4) (3 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ1_125 using 1 <;> norm_num
  · convert coverQ1_126 using 1 <;> norm_num
  · convert coverQ1_139 using 1 <;> norm_num
  · convert coverQ1_144 using 1 <;> norm_num

theorem coverQ1_146 : BoxCovered (7 / 8) (3 / 8) (1 / 16) := by
  apply boxCovered_leaf (7 / 8) (3 / 8) (1 / 16) (445439 / 500000) (167763 / 500000) (23311 / 500000) (50987 / 500000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_147 : BoxCovered (15 / 16) (3 / 8) (1 / 16) := by
  apply boxCovered_leaf (15 / 16) (3 / 8) (1 / 16) (445439 / 500000) (167763 / 500000) (54561 / 500000) (50987 / 500000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_148 : BoxCovered (7 / 8) (7 / 16) (1 / 16) := by
  apply boxCovered_leaf (7 / 8) (7 / 16) (1 / 16) (445439 / 500000) (167763 / 500000) (23311 / 500000) (82237 / 500000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_149 : BoxCovered (15 / 16) (7 / 16) (1 / 32) := by
  apply boxCovered_leaf (15 / 16) (7 / 16) (1 / 32) (445439 / 500000) (167763 / 500000) (4867 / 62500) (16653 / 125000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_150 : BoxCovered (31 / 32) (7 / 16) (1 / 32) := by
  apply boxCovered_leaf (31 / 32) (7 / 16) (1 / 32) (445439 / 500000) (167763 / 500000) (54561 / 500000) (16653 / 125000) ⟨7, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_151 : BoxCovered (15 / 16) (15 / 32) (1 / 32) := by
  apply boxCovered_leaf (15 / 16) (15 / 32) (1 / 32) (1793819 / 2000000) (599621 / 1000000) (143681 / 2000000) (130871 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_152 : BoxCovered (31 / 32) (15 / 32) (1 / 32) := by
  apply boxCovered_leaf (31 / 32) (15 / 32) (1 / 32) (1793819 / 2000000) (599621 / 1000000) (206181 / 2000000) (130871 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ1_153 : BoxCovered (15 / 16) (7 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ1_149 using 1 <;> norm_num
  · convert coverQ1_150 using 1 <;> norm_num
  · convert coverQ1_151 using 1 <;> norm_num
  · convert coverQ1_152 using 1 <;> norm_num

theorem coverQ1_154 : BoxCovered (7 / 8) (3 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ1_146 using 1 <;> norm_num
  · convert coverQ1_147 using 1 <;> norm_num
  · convert coverQ1_148 using 1 <;> norm_num
  · convert coverQ1_153 using 1 <;> norm_num

theorem coverQ1_155 : BoxCovered (3 / 4) (1 / 4) (1 / 4) := by
  apply boxCovered_split
  · convert coverQ1_119 using 1 <;> norm_num
  · convert coverQ1_120 using 1 <;> norm_num
  · convert coverQ1_145 using 1 <;> norm_num
  · convert coverQ1_154 using 1 <;> norm_num

theorem coverQ1_156 : BoxCovered (1 / 2) 0 (1 / 2) := by
  apply boxCovered_split
  · convert coverQ1_36 using 1 <;> norm_num
  · convert coverQ1_65 using 1 <;> norm_num
  · convert coverQ1_118 using 1 <;> norm_num
  · convert coverQ1_155 using 1 <;> norm_num

theorem coverQuadrant1 : BoxCovered (1 / 2) 0 (1/2) := coverQ1_156

end ElevenSquare
