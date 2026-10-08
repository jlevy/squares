import ElevenSquare.CoverChecks

/-! Generated exact dyadic covering witness. Every numerical premise is
proved by kernel-checked `norm_num`; no external PASS flag is assumed. -/
namespace ElevenSquare
set_option maxHeartbeats 0
set_option linter.unnecessarySeqFocus false

theorem coverQ2_0 : BoxCovered 0 (1 / 2) (1 / 32) := by
  apply boxCovered_leaf 0 (1 / 2) (1 / 32) (206181 / 2000000) (400379 / 1000000) (206181 / 2000000) (130871 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_1 : BoxCovered (1 / 32) (1 / 2) (1 / 32) := by
  apply boxCovered_leaf (1 / 32) (1 / 2) (1 / 32) (206181 / 2000000) (400379 / 1000000) (143681 / 2000000) (130871 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_2 : BoxCovered 0 (17 / 32) (1 / 32) := by
  apply boxCovered_leaf 0 (17 / 32) (1 / 32) (54561 / 500000) (332237 / 500000) (54561 / 500000) (16653 / 125000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_3 : BoxCovered (1 / 32) (17 / 32) (1 / 32) := by
  apply boxCovered_leaf (1 / 32) (17 / 32) (1 / 32) (54561 / 500000) (332237 / 500000) (4867 / 62500) (16653 / 125000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_4 : BoxCovered 0 (1 / 2) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ2_0 using 1 <;> norm_num
  · convert coverQ2_1 using 1 <;> norm_num
  · convert coverQ2_2 using 1 <;> norm_num
  · convert coverQ2_3 using 1 <;> norm_num

theorem coverQ2_5 : BoxCovered (1 / 16) (1 / 2) (1 / 16) := by
  apply boxCovered_leaf (1 / 16) (1 / 2) (1 / 16) (206181 / 2000000) (400379 / 1000000) (81181 / 2000000) (162121 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_6 : BoxCovered 0 (9 / 16) (1 / 16) := by
  apply boxCovered_leaf 0 (9 / 16) (1 / 16) (54561 / 500000) (332237 / 500000) (54561 / 500000) (50987 / 500000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_7 : BoxCovered (1 / 16) (9 / 16) (1 / 16) := by
  apply boxCovered_leaf (1 / 16) (9 / 16) (1 / 16) (54561 / 500000) (332237 / 500000) (23311 / 500000) (50987 / 500000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_8 : BoxCovered 0 (1 / 2) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ2_4 using 1 <;> norm_num
  · convert coverQ2_5 using 1 <;> norm_num
  · convert coverQ2_6 using 1 <;> norm_num
  · convert coverQ2_7 using 1 <;> norm_num

theorem coverQ2_9 : BoxCovered (1 / 8) (1 / 2) (1 / 32) := by
  apply boxCovered_leaf (1 / 8) (1 / 2) (1 / 32) (206181 / 2000000) (400379 / 1000000) (106319 / 2000000) (130871 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_10 : BoxCovered (5 / 32) (1 / 2) (1 / 32) := by
  apply boxCovered_leaf (5 / 32) (1 / 2) (1 / 32) (206181 / 2000000) (400379 / 1000000) (168819 / 2000000) (130871 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_11 : BoxCovered (1 / 8) (17 / 32) (1 / 32) := by
  apply boxCovered_leaf (1 / 8) (17 / 32) (1 / 32) (206181 / 2000000) (400379 / 1000000) (106319 / 2000000) (162121 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_12 : BoxCovered (5 / 32) (17 / 32) (1 / 32) := by
  apply boxCovered_leaf (5 / 32) (17 / 32) (1 / 32) (54561 / 500000) (332237 / 500000) (39189 / 500000) (16653 / 125000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_13 : BoxCovered (1 / 8) (1 / 2) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ2_9 using 1 <;> norm_num
  · convert coverQ2_10 using 1 <;> norm_num
  · convert coverQ2_11 using 1 <;> norm_num
  · convert coverQ2_12 using 1 <;> norm_num

theorem coverQ2_14 : BoxCovered (3 / 16) (1 / 2) (1 / 64) := by
  apply boxCovered_leaf (3 / 16) (1 / 2) (1 / 64) (206181 / 2000000) (400379 / 1000000) (200069 / 2000000) (57623 / 500000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_15 : BoxCovered (13 / 64) (1 / 2) (1 / 64) := by
  apply boxCovered_leaf (13 / 64) (1 / 2) (1 / 64) (206181 / 2000000) (400379 / 1000000) (231319 / 2000000) (57623 / 500000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_16 : BoxCovered (3 / 16) (33 / 64) (1 / 64) := by
  apply boxCovered_leaf (3 / 16) (33 / 64) (1 / 64) (206181 / 2000000) (400379 / 1000000) (200069 / 2000000) (130871 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_17 : BoxCovered (13 / 64) (33 / 64) (1 / 128) := by
  apply boxCovered_leaf (13 / 64) (33 / 64) (1 / 128) (206181 / 2000000) (400379 / 1000000) (107847 / 1000000) (246117 / 2000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_18 : BoxCovered (27 / 128) (33 / 64) (1 / 128) := by
  apply boxCovered_leaf (27 / 128) (33 / 64) (1 / 128) (206181 / 2000000) (400379 / 1000000) (231319 / 2000000) (246117 / 2000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_19 : BoxCovered (13 / 64) (67 / 128) (1 / 128) := by
  apply boxCovered_leaf (13 / 64) (67 / 128) (1 / 128) (206181 / 2000000) (400379 / 1000000) (107847 / 1000000) (130871 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_20 : BoxCovered (27 / 128) (67 / 128) (1 / 128) := by
  apply boxCovered_leaf (27 / 128) (67 / 128) (1 / 128) (364743 / 1000000) (233591 / 400000) (307611 / 2000000) (3027 / 50000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_21 : BoxCovered (13 / 64) (33 / 64) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ2_17 using 1 <;> norm_num
  · convert coverQ2_18 using 1 <;> norm_num
  · convert coverQ2_19 using 1 <;> norm_num
  · convert coverQ2_20 using 1 <;> norm_num

theorem coverQ2_22 : BoxCovered (3 / 16) (1 / 2) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ2_14 using 1 <;> norm_num
  · convert coverQ2_15 using 1 <;> norm_num
  · convert coverQ2_16 using 1 <;> norm_num
  · convert coverQ2_21 using 1 <;> norm_num

theorem coverQ2_23 : BoxCovered (7 / 32) (1 / 2) (1 / 32) := by
  apply boxCovered_leaf (7 / 32) (1 / 2) (1 / 32) (364743 / 1000000) (233591 / 400000) (145993 / 1000000) (33591 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_24 : BoxCovered (3 / 16) (17 / 32) (1 / 32) := by
  apply boxCovered_leaf (3 / 16) (17 / 32) (1 / 32) (54561 / 500000) (332237 / 500000) (27407 / 250000) (16653 / 125000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_25 : BoxCovered (7 / 32) (17 / 32) (1 / 32) := by
  apply boxCovered_leaf (7 / 32) (17 / 32) (1 / 32) (364743 / 1000000) (233591 / 400000) (145993 / 1000000) (21091 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_26 : BoxCovered (3 / 16) (1 / 2) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ2_22 using 1 <;> norm_num
  · convert coverQ2_23 using 1 <;> norm_num
  · convert coverQ2_24 using 1 <;> norm_num
  · convert coverQ2_25 using 1 <;> norm_num

theorem coverQ2_27 : BoxCovered (1 / 8) (9 / 16) (1 / 16) := by
  apply boxCovered_leaf (1 / 8) (9 / 16) (1 / 16) (54561 / 500000) (332237 / 500000) (39189 / 500000) (50987 / 500000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_28 : BoxCovered (3 / 16) (9 / 16) (1 / 32) := by
  apply boxCovered_leaf (3 / 16) (9 / 16) (1 / 32) (54561 / 500000) (332237 / 500000) (27407 / 250000) (50987 / 500000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_29 : BoxCovered (7 / 32) (9 / 16) (1 / 32) := by
  apply boxCovered_leaf (7 / 32) (9 / 16) (1 / 32) (364743 / 1000000) (233591 / 400000) (145993 / 1000000) (8591 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_30 : BoxCovered (3 / 16) (19 / 32) (1 / 32) := by
  apply boxCovered_leaf (3 / 16) (19 / 32) (1 / 32) (54561 / 500000) (332237 / 500000) (27407 / 250000) (17681 / 250000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_31 : BoxCovered (7 / 32) (19 / 32) (1 / 32) := by
  apply boxCovered_leaf (7 / 32) (19 / 32) (1 / 32) (54561 / 500000) (332237 / 500000) (70439 / 500000) (17681 / 250000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_32 : BoxCovered (3 / 16) (9 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ2_28 using 1 <;> norm_num
  · convert coverQ2_29 using 1 <;> norm_num
  · convert coverQ2_30 using 1 <;> norm_num
  · convert coverQ2_31 using 1 <;> norm_num

theorem coverQ2_33 : BoxCovered (1 / 8) (1 / 2) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ2_13 using 1 <;> norm_num
  · convert coverQ2_26 using 1 <;> norm_num
  · convert coverQ2_27 using 1 <;> norm_num
  · convert coverQ2_32 using 1 <;> norm_num

theorem coverQ2_34 : BoxCovered 0 (5 / 8) (1 / 8) := by
  apply boxCovered_leaf 0 (5 / 8) (1 / 8) (54561 / 500000) (332237 / 500000) (54561 / 500000) (42763 / 500000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_35 : BoxCovered (1 / 8) (5 / 8) (1 / 8) := by
  apply boxCovered_leaf (1 / 8) (5 / 8) (1 / 8) (54561 / 500000) (332237 / 500000) (70439 / 500000) (42763 / 500000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_36 : BoxCovered 0 (1 / 2) (1 / 4) := by
  apply boxCovered_split
  · convert coverQ2_8 using 1 <;> norm_num
  · convert coverQ2_33 using 1 <;> norm_num
  · convert coverQ2_34 using 1 <;> norm_num
  · convert coverQ2_35 using 1 <;> norm_num

theorem coverQ2_37 : BoxCovered (1 / 4) (1 / 2) (1 / 8) := by
  apply boxCovered_leaf (1 / 4) (1 / 2) (1 / 8) (364743 / 1000000) (233591 / 400000) (114743 / 1000000) (33591 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_38 : BoxCovered (3 / 8) (1 / 2) (1 / 8) := by
  apply boxCovered_leaf (3 / 8) (1 / 2) (1 / 8) (364743 / 1000000) (233591 / 400000) (135257 / 1000000) (33591 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_39 : BoxCovered (1 / 4) (5 / 8) (1 / 16) := by
  apply boxCovered_leaf (1 / 4) (5 / 8) (1 / 16) (364743 / 1000000) (233591 / 400000) (114743 / 1000000) (41409 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_40 : BoxCovered (5 / 16) (5 / 8) (1 / 16) := by
  apply boxCovered_leaf (5 / 16) (5 / 8) (1 / 16) (364743 / 1000000) (233591 / 400000) (52243 / 1000000) (41409 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_41 : BoxCovered (1 / 4) (11 / 16) (1 / 64) := by
  apply boxCovered_leaf (1 / 4) (11 / 16) (1 / 64) (54561 / 500000) (332237 / 500000) (156503 / 1000000) (38651 / 1000000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_42 : BoxCovered (17 / 64) (11 / 16) (1 / 64) := by
  apply boxCovered_leaf (17 / 64) (11 / 16) (1 / 64) (364743 / 1000000) (233591 / 400000) (49559 / 500000) (47659 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_43 : BoxCovered (1 / 4) (45 / 64) (1 / 64) := by
  apply boxCovered_leaf (1 / 4) (45 / 64) (1 / 64) (54561 / 500000) (332237 / 500000) (156503 / 1000000) (13569 / 250000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_44 : BoxCovered (17 / 64) (45 / 64) (1 / 64) := by
  apply boxCovered_leaf (17 / 64) (45 / 64) (1 / 64) (364743 / 1000000) (233591 / 400000) (49559 / 500000) (53909 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_45 : BoxCovered (1 / 4) (11 / 16) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ2_41 using 1 <;> norm_num
  · convert coverQ2_42 using 1 <;> norm_num
  · convert coverQ2_43 using 1 <;> norm_num
  · convert coverQ2_44 using 1 <;> norm_num

theorem coverQ2_46 : BoxCovered (9 / 32) (11 / 16) (1 / 32) := by
  apply boxCovered_leaf (9 / 32) (11 / 16) (1 / 32) (364743 / 1000000) (233591 / 400000) (83493 / 1000000) (53909 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_47 : BoxCovered (1 / 4) (23 / 32) (1 / 64) := by
  apply boxCovered_leaf (1 / 4) (23 / 32) (1 / 64) (54561 / 500000) (332237 / 500000) (156503 / 1000000) (69901 / 1000000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_48 : BoxCovered (17 / 64) (23 / 32) (1 / 256) := by
  apply boxCovered_leaf (17 / 64) (23 / 32) (1 / 256) (54561 / 500000) (332237 / 500000) (641637 / 4000000) (232729 / 4000000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_49 : BoxCovered (69 / 256) (23 / 32) (1 / 256) := by
  apply boxCovered_leaf (69 / 256) (23 / 32) (1 / 256) (364743 / 1000000) (233591 / 400000) (380847 / 4000000) (110943 / 800000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_50 : BoxCovered (17 / 64) (185 / 256) (1 / 256) := by
  apply boxCovered_leaf (17 / 64) (185 / 256) (1 / 256) (54561 / 500000) (332237 / 500000) (641637 / 4000000) (124177 / 2000000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_51 : BoxCovered (69 / 256) (185 / 256) (1 / 256) := by
  apply boxCovered_leaf (69 / 256) (185 / 256) (1 / 256) (364743 / 1000000) (233591 / 400000) (380847 / 4000000) (28517 / 200000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_52 : BoxCovered (17 / 64) (23 / 32) (1 / 128) := by
  apply boxCovered_split
  · convert coverQ2_48 using 1 <;> norm_num
  · convert coverQ2_49 using 1 <;> norm_num
  · convert coverQ2_50 using 1 <;> norm_num
  · convert coverQ2_51 using 1 <;> norm_num

theorem coverQ2_53 : BoxCovered (35 / 128) (23 / 32) (1 / 128) := by
  apply boxCovered_leaf (35 / 128) (23 / 32) (1 / 128) (364743 / 1000000) (233591 / 400000) (182611 / 2000000) (28517 / 200000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_54 : BoxCovered (17 / 64) (93 / 128) (1 / 128) := by
  apply boxCovered_leaf (17 / 64) (93 / 128) (1 / 128) (732757 / 2000000) (215311 / 250000) (201507 / 2000000) (269363 / 2000000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_55 : BoxCovered (35 / 128) (93 / 128) (1 / 128) := by
  apply boxCovered_leaf (35 / 128) (93 / 128) (1 / 128) (732757 / 2000000) (215311 / 250000) (92941 / 1000000) (269363 / 2000000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_56 : BoxCovered (17 / 64) (23 / 32) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ2_52 using 1 <;> norm_num
  · convert coverQ2_53 using 1 <;> norm_num
  · convert coverQ2_54 using 1 <;> norm_num
  · convert coverQ2_55 using 1 <;> norm_num

theorem coverQ2_57 : BoxCovered (1 / 4) (47 / 64) (1 / 64) := by
  apply boxCovered_leaf (1 / 4) (47 / 64) (1 / 64) (732757 / 2000000) (215311 / 250000) (232757 / 2000000) (126869 / 1000000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_58 : BoxCovered (17 / 64) (47 / 64) (1 / 64) := by
  apply boxCovered_leaf (17 / 64) (47 / 64) (1 / 64) (732757 / 2000000) (215311 / 250000) (201507 / 2000000) (126869 / 1000000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_59 : BoxCovered (1 / 4) (23 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ2_47 using 1 <;> norm_num
  · convert coverQ2_56 using 1 <;> norm_num
  · convert coverQ2_57 using 1 <;> norm_num
  · convert coverQ2_58 using 1 <;> norm_num

theorem coverQ2_60 : BoxCovered (9 / 32) (23 / 32) (1 / 32) := by
  apply boxCovered_leaf (9 / 32) (23 / 32) (1 / 32) (732757 / 2000000) (215311 / 250000) (170257 / 2000000) (71247 / 500000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_61 : BoxCovered (1 / 4) (11 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ2_45 using 1 <;> norm_num
  · convert coverQ2_46 using 1 <;> norm_num
  · convert coverQ2_59 using 1 <;> norm_num
  · convert coverQ2_60 using 1 <;> norm_num

theorem coverQ2_62 : BoxCovered (5 / 16) (11 / 16) (1 / 32) := by
  apply boxCovered_leaf (5 / 16) (11 / 16) (1 / 32) (364743 / 1000000) (233591 / 400000) (52243 / 1000000) (53909 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_63 : BoxCovered (11 / 32) (11 / 16) (1 / 32) := by
  apply boxCovered_leaf (11 / 32) (11 / 16) (1 / 32) (364743 / 1000000) (233591 / 400000) (20993 / 1000000) (53909 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_64 : BoxCovered (5 / 16) (23 / 32) (1 / 32) := by
  apply boxCovered_leaf (5 / 16) (23 / 32) (1 / 32) (732757 / 2000000) (215311 / 250000) (107757 / 2000000) (71247 / 500000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_65 : BoxCovered (11 / 32) (23 / 32) (1 / 32) := by
  apply boxCovered_leaf (11 / 32) (23 / 32) (1 / 32) (364743 / 1000000) (233591 / 400000) (20993 / 1000000) (66409 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_66 : BoxCovered (5 / 16) (11 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ2_62 using 1 <;> norm_num
  · convert coverQ2_63 using 1 <;> norm_num
  · convert coverQ2_64 using 1 <;> norm_num
  · convert coverQ2_65 using 1 <;> norm_num

theorem coverQ2_67 : BoxCovered (1 / 4) (5 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ2_39 using 1 <;> norm_num
  · convert coverQ2_40 using 1 <;> norm_num
  · convert coverQ2_61 using 1 <;> norm_num
  · convert coverQ2_66 using 1 <;> norm_num

theorem coverQ2_68 : BoxCovered (3 / 8) (5 / 8) (1 / 16) := by
  apply boxCovered_leaf (3 / 8) (5 / 8) (1 / 16) (364743 / 1000000) (233591 / 400000) (72757 / 1000000) (41409 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_69 : BoxCovered (7 / 16) (5 / 8) (1 / 16) := by
  apply boxCovered_leaf (7 / 16) (5 / 8) (1 / 16) (364743 / 1000000) (233591 / 400000) (135257 / 1000000) (41409 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_70 : BoxCovered (3 / 8) (11 / 16) (1 / 32) := by
  apply boxCovered_leaf (3 / 8) (11 / 16) (1 / 32) (364743 / 1000000) (233591 / 400000) (41507 / 1000000) (53909 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_71 : BoxCovered (13 / 32) (11 / 16) (1 / 32) := by
  apply boxCovered_leaf (13 / 32) (11 / 16) (1 / 32) (364743 / 1000000) (233591 / 400000) (72757 / 1000000) (53909 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_72 : BoxCovered (3 / 8) (23 / 32) (1 / 32) := by
  apply boxCovered_leaf (3 / 8) (23 / 32) (1 / 32) (364743 / 1000000) (233591 / 400000) (41507 / 1000000) (66409 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_73 : BoxCovered (13 / 32) (23 / 32) (1 / 32) := by
  apply boxCovered_leaf (13 / 32) (23 / 32) (1 / 32) (732757 / 2000000) (215311 / 250000) (142243 / 2000000) (71247 / 500000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_74 : BoxCovered (3 / 8) (11 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ2_70 using 1 <;> norm_num
  · convert coverQ2_71 using 1 <;> norm_num
  · convert coverQ2_72 using 1 <;> norm_num
  · convert coverQ2_73 using 1 <;> norm_num

theorem coverQ2_75 : BoxCovered (7 / 16) (11 / 16) (1 / 32) := by
  apply boxCovered_leaf (7 / 16) (11 / 16) (1 / 32) (364743 / 1000000) (233591 / 400000) (104007 / 1000000) (53909 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_76 : BoxCovered (15 / 32) (11 / 16) (1 / 32) := by
  apply boxCovered_leaf (15 / 32) (11 / 16) (1 / 32) (1257689 / 2000000) (687067 / 1000000) (320189 / 2000000) (31683 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_77 : BoxCovered (7 / 16) (23 / 32) (1 / 64) := by
  apply boxCovered_leaf (7 / 16) (23 / 32) (1 / 64) (732757 / 2000000) (215311 / 250000) (173493 / 2000000) (71247 / 500000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_78 : BoxCovered (29 / 64) (23 / 32) (1 / 128) := by
  apply boxCovered_leaf (29 / 64) (23 / 32) (1 / 128) (364743 / 1000000) (233591 / 400000) (192389 / 2000000) (28517 / 200000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_79 : BoxCovered (59 / 128) (23 / 32) (1 / 128) := by
  apply boxCovered_leaf (59 / 128) (23 / 32) (1 / 128) (1257689 / 2000000) (687067 / 1000000) (167907 / 1000000) (78991 / 2000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_80 : BoxCovered (29 / 64) (93 / 128) (1 / 128) := by
  apply boxCovered_leaf (29 / 64) (93 / 128) (1 / 128) (732757 / 2000000) (215311 / 250000) (94559 / 1000000) (269363 / 2000000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_81 : BoxCovered (59 / 128) (93 / 128) (1 / 128) := by
  apply boxCovered_leaf (59 / 128) (93 / 128) (1 / 128) (732757 / 2000000) (215311 / 250000) (204743 / 2000000) (269363 / 2000000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_82 : BoxCovered (29 / 64) (23 / 32) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ2_78 using 1 <;> norm_num
  · convert coverQ2_79 using 1 <;> norm_num
  · convert coverQ2_80 using 1 <;> norm_num
  · convert coverQ2_81 using 1 <;> norm_num

theorem coverQ2_83 : BoxCovered (7 / 16) (47 / 64) (1 / 64) := by
  apply boxCovered_leaf (7 / 16) (47 / 64) (1 / 64) (732757 / 2000000) (215311 / 250000) (173493 / 2000000) (126869 / 1000000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_84 : BoxCovered (29 / 64) (47 / 64) (1 / 64) := by
  apply boxCovered_leaf (29 / 64) (47 / 64) (1 / 64) (732757 / 2000000) (215311 / 250000) (204743 / 2000000) (126869 / 1000000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_85 : BoxCovered (7 / 16) (23 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ2_77 using 1 <;> norm_num
  · convert coverQ2_82 using 1 <;> norm_num
  · convert coverQ2_83 using 1 <;> norm_num
  · convert coverQ2_84 using 1 <;> norm_num

theorem coverQ2_86 : BoxCovered (15 / 32) (23 / 32) (1 / 32) := by
  apply boxCovered_leaf (15 / 32) (23 / 32) (1 / 32) (1257689 / 2000000) (687067 / 1000000) (320189 / 2000000) (62933 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_87 : BoxCovered (7 / 16) (11 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ2_75 using 1 <;> norm_num
  · convert coverQ2_76 using 1 <;> norm_num
  · convert coverQ2_85 using 1 <;> norm_num
  · convert coverQ2_86 using 1 <;> norm_num

theorem coverQ2_88 : BoxCovered (3 / 8) (5 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ2_68 using 1 <;> norm_num
  · convert coverQ2_69 using 1 <;> norm_num
  · convert coverQ2_74 using 1 <;> norm_num
  · convert coverQ2_87 using 1 <;> norm_num

theorem coverQ2_89 : BoxCovered (1 / 4) (1 / 2) (1 / 4) := by
  apply boxCovered_split
  · convert coverQ2_37 using 1 <;> norm_num
  · convert coverQ2_38 using 1 <;> norm_num
  · convert coverQ2_67 using 1 <;> norm_num
  · convert coverQ2_88 using 1 <;> norm_num

theorem coverQ2_90 : BoxCovered 0 (3 / 4) (1 / 32) := by
  apply boxCovered_leaf 0 (3 / 4) (1 / 32) (54561 / 500000) (332237 / 500000) (54561 / 500000) (14597 / 125000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_91 : BoxCovered (1 / 32) (3 / 4) (1 / 32) := by
  apply boxCovered_leaf (1 / 32) (3 / 4) (1 / 32) (54561 / 500000) (332237 / 500000) (4867 / 62500) (14597 / 125000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_92 : BoxCovered 0 (25 / 32) (1 / 64) := by
  apply boxCovered_leaf 0 (25 / 32) (1 / 64) (54561 / 500000) (332237 / 500000) (54561 / 500000) (132401 / 1000000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_93 : BoxCovered (1 / 64) (25 / 32) (1 / 64) := by
  apply boxCovered_leaf (1 / 64) (25 / 32) (1 / 64) (54561 / 500000) (332237 / 500000) (93497 / 1000000) (132401 / 1000000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_94 : BoxCovered 0 (51 / 64) (1 / 64) := by
  apply boxCovered_leaf 0 (51 / 64) (1 / 64) (268877 / 2000000) (224299 / 250000) (268877 / 2000000) (100321 / 1000000) ⟨12, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_95 : BoxCovered (1 / 64) (51 / 64) (1 / 64) := by
  apply boxCovered_leaf (1 / 64) (51 / 64) (1 / 64) (268877 / 2000000) (224299 / 250000) (237627 / 2000000) (100321 / 1000000) ⟨12, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_96 : BoxCovered 0 (25 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ2_92 using 1 <;> norm_num
  · convert coverQ2_93 using 1 <;> norm_num
  · convert coverQ2_94 using 1 <;> norm_num
  · convert coverQ2_95 using 1 <;> norm_num

theorem coverQ2_97 : BoxCovered (1 / 32) (25 / 32) (1 / 32) := by
  apply boxCovered_leaf (1 / 32) (25 / 32) (1 / 32) (54561 / 500000) (332237 / 500000) (4867 / 62500) (74013 / 500000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_98 : BoxCovered 0 (3 / 4) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ2_90 using 1 <;> norm_num
  · convert coverQ2_91 using 1 <;> norm_num
  · convert coverQ2_96 using 1 <;> norm_num
  · convert coverQ2_97 using 1 <;> norm_num

theorem coverQ2_99 : BoxCovered (1 / 16) (3 / 4) (1 / 16) := by
  apply boxCovered_leaf (1 / 16) (3 / 4) (1 / 16) (54561 / 500000) (332237 / 500000) (23311 / 500000) (74013 / 500000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_100 : BoxCovered 0 (13 / 16) (1 / 16) := by
  apply boxCovered_leaf 0 (13 / 16) (1 / 16) (268877 / 2000000) (224299 / 250000) (268877 / 2000000) (10587 / 125000) ⟨12, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_101 : BoxCovered (1 / 16) (13 / 16) (1 / 16) := by
  apply boxCovered_leaf (1 / 16) (13 / 16) (1 / 16) (268877 / 2000000) (224299 / 250000) (143877 / 2000000) (10587 / 125000) ⟨12, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_102 : BoxCovered 0 (3 / 4) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ2_98 using 1 <;> norm_num
  · convert coverQ2_99 using 1 <;> norm_num
  · convert coverQ2_100 using 1 <;> norm_num
  · convert coverQ2_101 using 1 <;> norm_num

theorem coverQ2_103 : BoxCovered (1 / 8) (3 / 4) (1 / 16) := by
  apply boxCovered_leaf (1 / 8) (3 / 4) (1 / 16) (54561 / 500000) (332237 / 500000) (39189 / 500000) (74013 / 500000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_104 : BoxCovered (3 / 16) (3 / 4) (1 / 32) := by
  apply boxCovered_leaf (3 / 16) (3 / 4) (1 / 32) (54561 / 500000) (332237 / 500000) (27407 / 250000) (14597 / 125000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_105 : BoxCovered (7 / 32) (3 / 4) (1 / 64) := by
  apply boxCovered_leaf (7 / 32) (3 / 4) (1 / 64) (54561 / 500000) (332237 / 500000) (125253 / 1000000) (101151 / 1000000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_106 : BoxCovered (15 / 64) (3 / 4) (1 / 64) := by
  apply boxCovered_leaf (15 / 64) (3 / 4) (1 / 64) (732757 / 2000000) (215311 / 250000) (264007 / 2000000) (27811 / 250000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_107 : BoxCovered (7 / 32) (49 / 64) (1 / 64) := by
  apply boxCovered_leaf (7 / 32) (49 / 64) (1 / 64) (54561 / 500000) (332237 / 500000) (125253 / 1000000) (14597 / 125000) ⟨8, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_108 : BoxCovered (15 / 64) (49 / 64) (1 / 64) := by
  apply boxCovered_leaf (15 / 64) (49 / 64) (1 / 64) (732757 / 2000000) (215311 / 250000) (264007 / 2000000) (95619 / 1000000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_109 : BoxCovered (7 / 32) (3 / 4) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ2_105 using 1 <;> norm_num
  · convert coverQ2_106 using 1 <;> norm_num
  · convert coverQ2_107 using 1 <;> norm_num
  · convert coverQ2_108 using 1 <;> norm_num

theorem coverQ2_110 : BoxCovered (3 / 16) (25 / 32) (1 / 32) := by
  apply boxCovered_leaf (3 / 16) (25 / 32) (1 / 32) (268877 / 2000000) (224299 / 250000) (168623 / 2000000) (57973 / 500000) ⟨12, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_111 : BoxCovered (7 / 32) (25 / 32) (1 / 32) := by
  apply boxCovered_leaf (7 / 32) (25 / 32) (1 / 32) (268877 / 2000000) (224299 / 250000) (231123 / 2000000) (57973 / 500000) ⟨12, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_112 : BoxCovered (3 / 16) (3 / 4) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ2_104 using 1 <;> norm_num
  · convert coverQ2_109 using 1 <;> norm_num
  · convert coverQ2_110 using 1 <;> norm_num
  · convert coverQ2_111 using 1 <;> norm_num

theorem coverQ2_113 : BoxCovered (1 / 8) (13 / 16) (1 / 16) := by
  apply boxCovered_leaf (1 / 8) (13 / 16) (1 / 16) (268877 / 2000000) (224299 / 250000) (106123 / 2000000) (10587 / 125000) ⟨12, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_114 : BoxCovered (3 / 16) (13 / 16) (1 / 16) := by
  apply boxCovered_leaf (3 / 16) (13 / 16) (1 / 16) (268877 / 2000000) (224299 / 250000) (231123 / 2000000) (10587 / 125000) ⟨12, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_115 : BoxCovered (1 / 8) (3 / 4) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ2_103 using 1 <;> norm_num
  · convert coverQ2_112 using 1 <;> norm_num
  · convert coverQ2_113 using 1 <;> norm_num
  · convert coverQ2_114 using 1 <;> norm_num

theorem coverQ2_116 : BoxCovered 0 (7 / 8) (1 / 8) := by
  apply boxCovered_leaf 0 (7 / 8) (1 / 8) (268877 / 2000000) (224299 / 250000) (268877 / 2000000) (25701 / 250000) ⟨12, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_117 : BoxCovered (1 / 8) (7 / 8) (1 / 8) := by
  apply boxCovered_leaf (1 / 8) (7 / 8) (1 / 8) (268877 / 2000000) (224299 / 250000) (231123 / 2000000) (25701 / 250000) ⟨12, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_118 : BoxCovered 0 (3 / 4) (1 / 4) := by
  apply boxCovered_split
  · convert coverQ2_102 using 1 <;> norm_num
  · convert coverQ2_115 using 1 <;> norm_num
  · convert coverQ2_116 using 1 <;> norm_num
  · convert coverQ2_117 using 1 <;> norm_num

theorem coverQ2_119 : BoxCovered (1 / 4) (3 / 4) (1 / 8) := by
  apply boxCovered_leaf (1 / 4) (3 / 4) (1 / 8) (732757 / 2000000) (215311 / 250000) (232757 / 2000000) (27811 / 250000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_120 : BoxCovered (3 / 8) (3 / 4) (1 / 16) := by
  apply boxCovered_leaf (3 / 8) (3 / 4) (1 / 16) (732757 / 2000000) (215311 / 250000) (142243 / 2000000) (27811 / 250000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_121 : BoxCovered (7 / 16) (3 / 4) (1 / 32) := by
  apply boxCovered_leaf (7 / 16) (3 / 4) (1 / 32) (732757 / 2000000) (215311 / 250000) (204743 / 2000000) (27811 / 250000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_122 : BoxCovered (15 / 32) (3 / 4) (1 / 64) := by
  apply boxCovered_leaf (15 / 32) (3 / 4) (1 / 64) (732757 / 2000000) (215311 / 250000) (235993 / 2000000) (27811 / 250000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_123 : BoxCovered (31 / 64) (3 / 4) (1 / 64) := by
  apply boxCovered_leaf (31 / 64) (3 / 4) (1 / 64) (1257689 / 2000000) (687067 / 1000000) (288939 / 2000000) (39279 / 500000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_124 : BoxCovered (15 / 32) (49 / 64) (1 / 64) := by
  apply boxCovered_leaf (15 / 32) (49 / 64) (1 / 64) (732757 / 2000000) (215311 / 250000) (235993 / 2000000) (95619 / 1000000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_125 : BoxCovered (31 / 64) (49 / 64) (1 / 64) := by
  apply boxCovered_leaf (31 / 64) (49 / 64) (1 / 64) (1257689 / 2000000) (687067 / 1000000) (288939 / 2000000) (94183 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_126 : BoxCovered (15 / 32) (3 / 4) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ2_122 using 1 <;> norm_num
  · convert coverQ2_123 using 1 <;> norm_num
  · convert coverQ2_124 using 1 <;> norm_num
  · convert coverQ2_125 using 1 <;> norm_num

theorem coverQ2_127 : BoxCovered (7 / 16) (25 / 32) (1 / 32) := by
  apply boxCovered_leaf (7 / 16) (25 / 32) (1 / 32) (732757 / 2000000) (215311 / 250000) (204743 / 2000000) (39997 / 500000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_128 : BoxCovered (15 / 32) (25 / 32) (1 / 32) := by
  apply boxCovered_leaf (15 / 32) (25 / 32) (1 / 32) (732757 / 2000000) (215311 / 250000) (267243 / 2000000) (39997 / 500000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_129 : BoxCovered (7 / 16) (3 / 4) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ2_121 using 1 <;> norm_num
  · convert coverQ2_126 using 1 <;> norm_num
  · convert coverQ2_127 using 1 <;> norm_num
  · convert coverQ2_128 using 1 <;> norm_num

theorem coverQ2_130 : BoxCovered (3 / 8) (13 / 16) (1 / 16) := by
  apply boxCovered_leaf (3 / 8) (13 / 16) (1 / 16) (732757 / 2000000) (215311 / 250000) (142243 / 2000000) (6093 / 125000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_131 : BoxCovered (7 / 16) (13 / 16) (1 / 16) := by
  apply boxCovered_leaf (7 / 16) (13 / 16) (1 / 16) (732757 / 2000000) (215311 / 250000) (267243 / 2000000) (6093 / 125000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_132 : BoxCovered (3 / 8) (3 / 4) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ2_120 using 1 <;> norm_num
  · convert coverQ2_129 using 1 <;> norm_num
  · convert coverQ2_130 using 1 <;> norm_num
  · convert coverQ2_131 using 1 <;> norm_num

theorem coverQ2_133 : BoxCovered (1 / 4) (7 / 8) (1 / 16) := by
  apply boxCovered_leaf (1 / 4) (7 / 8) (1 / 16) (732757 / 2000000) (215311 / 250000) (232757 / 2000000) (2383 / 31250) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_134 : BoxCovered (5 / 16) (7 / 8) (1 / 16) := by
  apply boxCovered_leaf (5 / 16) (7 / 8) (1 / 16) (732757 / 2000000) (215311 / 250000) (107757 / 2000000) (2383 / 31250) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_135 : BoxCovered (1 / 4) (15 / 16) (1 / 32) := by
  apply boxCovered_leaf (1 / 4) (15 / 16) (1 / 32) (268877 / 2000000) (224299 / 250000) (293623 / 2000000) (35777 / 500000) ⟨12, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_136 : BoxCovered (9 / 32) (15 / 16) (1 / 32) := by
  apply boxCovered_leaf (9 / 32) (15 / 16) (1 / 32) (732757 / 2000000) (215311 / 250000) (170257 / 2000000) (53753 / 500000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_137 : BoxCovered (1 / 4) (31 / 32) (1 / 64) := by
  apply boxCovered_leaf (1 / 4) (31 / 32) (1 / 64) (268877 / 2000000) (224299 / 250000) (262373 / 2000000) (87179 / 1000000) ⟨12, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_138 : BoxCovered (17 / 64) (31 / 32) (1 / 64) := by
  apply boxCovered_leaf (17 / 64) (31 / 32) (1 / 64) (268877 / 2000000) (224299 / 250000) (293623 / 2000000) (87179 / 1000000) ⟨12, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_139 : BoxCovered (1 / 4) (63 / 64) (1 / 64) := by
  apply boxCovered_leaf (1 / 4) (63 / 64) (1 / 64) (268877 / 2000000) (224299 / 250000) (262373 / 2000000) (25701 / 250000) ⟨12, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_140 : BoxCovered (17 / 64) (63 / 64) (1 / 64) := by
  apply boxCovered_leaf (17 / 64) (63 / 64) (1 / 64) (732757 / 2000000) (215311 / 250000) (201507 / 2000000) (34689 / 250000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_141 : BoxCovered (1 / 4) (31 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ2_137 using 1 <;> norm_num
  · convert coverQ2_138 using 1 <;> norm_num
  · convert coverQ2_139 using 1 <;> norm_num
  · convert coverQ2_140 using 1 <;> norm_num

theorem coverQ2_142 : BoxCovered (9 / 32) (31 / 32) (1 / 32) := by
  apply boxCovered_leaf (9 / 32) (31 / 32) (1 / 32) (732757 / 2000000) (215311 / 250000) (170257 / 2000000) (34689 / 250000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_143 : BoxCovered (1 / 4) (15 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ2_135 using 1 <;> norm_num
  · convert coverQ2_136 using 1 <;> norm_num
  · convert coverQ2_141 using 1 <;> norm_num
  · convert coverQ2_142 using 1 <;> norm_num

theorem coverQ2_144 : BoxCovered (5 / 16) (15 / 16) (1 / 16) := by
  apply boxCovered_leaf (5 / 16) (15 / 16) (1 / 16) (732757 / 2000000) (215311 / 250000) (107757 / 2000000) (34689 / 250000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_145 : BoxCovered (1 / 4) (7 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ2_133 using 1 <;> norm_num
  · convert coverQ2_134 using 1 <;> norm_num
  · convert coverQ2_143 using 1 <;> norm_num
  · convert coverQ2_144 using 1 <;> norm_num

theorem coverQ2_146 : BoxCovered (3 / 8) (7 / 8) (1 / 16) := by
  apply boxCovered_leaf (3 / 8) (7 / 8) (1 / 16) (732757 / 2000000) (215311 / 250000) (142243 / 2000000) (2383 / 31250) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_147 : BoxCovered (7 / 16) (7 / 8) (1 / 16) := by
  apply boxCovered_leaf (7 / 16) (7 / 8) (1 / 16) (732757 / 2000000) (215311 / 250000) (267243 / 2000000) (2383 / 31250) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_148 : BoxCovered (3 / 8) (15 / 16) (1 / 16) := by
  apply boxCovered_leaf (3 / 8) (15 / 16) (1 / 16) (732757 / 2000000) (215311 / 250000) (142243 / 2000000) (34689 / 250000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_149 : BoxCovered (7 / 16) (15 / 16) (1 / 32) := by
  apply boxCovered_leaf (7 / 16) (15 / 16) (1 / 32) (732757 / 2000000) (215311 / 250000) (204743 / 2000000) (53753 / 500000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_150 : BoxCovered (15 / 32) (15 / 16) (1 / 32) := by
  apply boxCovered_leaf (15 / 32) (15 / 16) (1 / 32) (732757 / 2000000) (215311 / 250000) (267243 / 2000000) (53753 / 500000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_151 : BoxCovered (7 / 16) (31 / 32) (1 / 32) := by
  apply boxCovered_leaf (7 / 16) (31 / 32) (1 / 32) (732757 / 2000000) (215311 / 250000) (204743 / 2000000) (34689 / 250000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_152 : BoxCovered (15 / 32) (31 / 32) (1 / 32) := by
  apply boxCovered_leaf (15 / 32) (31 / 32) (1 / 32) (313399 / 500000) (954497 / 1000000) (4939 / 31250) (45503 / 1000000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ2_153 : BoxCovered (7 / 16) (15 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ2_149 using 1 <;> norm_num
  · convert coverQ2_150 using 1 <;> norm_num
  · convert coverQ2_151 using 1 <;> norm_num
  · convert coverQ2_152 using 1 <;> norm_num

theorem coverQ2_154 : BoxCovered (3 / 8) (7 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ2_146 using 1 <;> norm_num
  · convert coverQ2_147 using 1 <;> norm_num
  · convert coverQ2_148 using 1 <;> norm_num
  · convert coverQ2_153 using 1 <;> norm_num

theorem coverQ2_155 : BoxCovered (1 / 4) (3 / 4) (1 / 4) := by
  apply boxCovered_split
  · convert coverQ2_119 using 1 <;> norm_num
  · convert coverQ2_132 using 1 <;> norm_num
  · convert coverQ2_145 using 1 <;> norm_num
  · convert coverQ2_154 using 1 <;> norm_num

theorem coverQ2_156 : BoxCovered 0 (1 / 2) (1 / 2) := by
  apply boxCovered_split
  · convert coverQ2_36 using 1 <;> norm_num
  · convert coverQ2_89 using 1 <;> norm_num
  · convert coverQ2_118 using 1 <;> norm_num
  · convert coverQ2_155 using 1 <;> norm_num

theorem coverQuadrant2 : BoxCovered 0 (1 / 2) (1/2) := coverQ2_156

end ElevenSquare
