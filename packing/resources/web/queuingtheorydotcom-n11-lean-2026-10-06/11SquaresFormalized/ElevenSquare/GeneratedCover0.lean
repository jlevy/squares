import ElevenSquare.CoverChecks

/-! Generated exact dyadic covering witness. Every numerical premise is
proved by kernel-checked `norm_num`; no external PASS flag is assumed. -/
namespace ElevenSquare
set_option maxHeartbeats 0
set_option linter.unnecessarySeqFocus false

theorem coverQ0_0 : BoxCovered 0 0 (1 / 8) := by
  apply boxCovered_leaf 0 0 (1 / 8) (104991 / 1000000) (265837 / 2000000) (104991 / 1000000) (265837 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_1 : BoxCovered (1 / 8) 0 (1 / 16) := by
  apply boxCovered_leaf (1 / 8) 0 (1 / 16) (104991 / 1000000) (265837 / 2000000) (82509 / 1000000) (265837 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_2 : BoxCovered (3 / 16) 0 (1 / 64) := by
  apply boxCovered_leaf (3 / 16) 0 (1 / 64) (104991 / 1000000) (265837 / 2000000) (49067 / 500000) (265837 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_3 : BoxCovered (13 / 64) 0 (1 / 128) := by
  apply boxCovered_leaf (13 / 64) 0 (1 / 128) (104991 / 1000000) (265837 / 2000000) (211893 / 2000000) (265837 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_4 : BoxCovered (27 / 128) 0 (1 / 128) := by
  apply boxCovered_leaf (27 / 128) 0 (1 / 128) (186601 / 500000) (45503 / 1000000) (324529 / 2000000) (45503 / 1000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_5 : BoxCovered (13 / 64) (1 / 128) (1 / 128) := by
  apply boxCovered_leaf (13 / 64) (1 / 128) (1 / 128) (104991 / 1000000) (265837 / 2000000) (211893 / 2000000) (62553 / 500000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_6 : BoxCovered (27 / 128) (1 / 128) (1 / 128) := by
  apply boxCovered_leaf (27 / 128) (1 / 128) (1 / 128) (104991 / 1000000) (265837 / 2000000) (113759 / 1000000) (62553 / 500000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_7 : BoxCovered (13 / 64) 0 (1 / 64) := by
  apply boxCovered_split
  · convert coverQ0_3 using 1 <;> norm_num
  · convert coverQ0_4 using 1 <;> norm_num
  · convert coverQ0_5 using 1 <;> norm_num
  · convert coverQ0_6 using 1 <;> norm_num

theorem coverQ0_8 : BoxCovered (3 / 16) (1 / 64) (1 / 64) := by
  apply boxCovered_leaf (3 / 16) (1 / 64) (1 / 64) (104991 / 1000000) (265837 / 2000000) (49067 / 500000) (234587 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_9 : BoxCovered (13 / 64) (1 / 64) (1 / 64) := by
  apply boxCovered_leaf (13 / 64) (1 / 64) (1 / 64) (104991 / 1000000) (265837 / 2000000) (113759 / 1000000) (234587 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_10 : BoxCovered (3 / 16) 0 (1 / 32) := by
  apply boxCovered_split
  · convert coverQ0_2 using 1 <;> norm_num
  · convert coverQ0_7 using 1 <;> norm_num
  · convert coverQ0_8 using 1 <;> norm_num
  · convert coverQ0_9 using 1 <;> norm_num

theorem coverQ0_11 : BoxCovered (7 / 32) 0 (1 / 32) := by
  apply boxCovered_leaf (7 / 32) 0 (1 / 32) (186601 / 500000) (45503 / 1000000) (38613 / 250000) (45503 / 1000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_12 : BoxCovered (3 / 16) (1 / 32) (1 / 32) := by
  apply boxCovered_leaf (3 / 16) (1 / 32) (1 / 32) (104991 / 1000000) (265837 / 2000000) (113759 / 1000000) (203337 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_13 : BoxCovered (7 / 32) (1 / 32) (1 / 32) := by
  apply boxCovered_leaf (7 / 32) (1 / 32) (1 / 32) (186601 / 500000) (45503 / 1000000) (38613 / 250000) (16997 / 1000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_14 : BoxCovered (3 / 16) 0 (1 / 16) := by
  apply boxCovered_split
  · convert coverQ0_10 using 1 <;> norm_num
  · convert coverQ0_11 using 1 <;> norm_num
  · convert coverQ0_12 using 1 <;> norm_num
  · convert coverQ0_13 using 1 <;> norm_num

theorem coverQ0_15 : BoxCovered (1 / 8) (1 / 16) (1 / 16) := by
  apply boxCovered_leaf (1 / 8) (1 / 16) (1 / 16) (104991 / 1000000) (265837 / 2000000) (82509 / 1000000) (140837 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_16 : BoxCovered (3 / 16) (1 / 16) (1 / 16) := by
  apply boxCovered_leaf (3 / 16) (1 / 16) (1 / 16) (104991 / 1000000) (265837 / 2000000) (145009 / 1000000) (140837 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_17 : BoxCovered (1 / 8) 0 (1 / 8) := by
  apply boxCovered_split
  · convert coverQ0_1 using 1 <;> norm_num
  · convert coverQ0_14 using 1 <;> norm_num
  · convert coverQ0_15 using 1 <;> norm_num
  · convert coverQ0_16 using 1 <;> norm_num

theorem coverQ0_18 : BoxCovered 0 (1 / 8) (1 / 8) := by
  apply boxCovered_leaf 0 (1 / 8) (1 / 8) (104991 / 1000000) (265837 / 2000000) (104991 / 1000000) (234163 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_19 : BoxCovered (1 / 8) (1 / 8) (1 / 16) := by
  apply boxCovered_leaf (1 / 8) (1 / 8) (1 / 16) (104991 / 1000000) (265837 / 2000000) (82509 / 1000000) (109163 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_20 : BoxCovered (3 / 16) (1 / 8) (1 / 16) := by
  apply boxCovered_leaf (3 / 16) (1 / 8) (1 / 16) (104991 / 1000000) (265837 / 2000000) (145009 / 1000000) (109163 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_21 : BoxCovered (1 / 8) (3 / 16) (1 / 16) := by
  apply boxCovered_leaf (1 / 8) (3 / 16) (1 / 16) (104991 / 1000000) (265837 / 2000000) (82509 / 1000000) (234163 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_22 : BoxCovered (3 / 16) (3 / 16) (1 / 32) := by
  apply boxCovered_leaf (3 / 16) (3 / 16) (1 / 32) (104991 / 1000000) (265837 / 2000000) (113759 / 1000000) (171663 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_23 : BoxCovered (7 / 32) (3 / 16) (1 / 32) := by
  apply boxCovered_leaf (7 / 32) (3 / 16) (1 / 32) (104991 / 1000000) (265837 / 2000000) (145009 / 1000000) (171663 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_24 : BoxCovered (3 / 16) (7 / 32) (1 / 32) := by
  apply boxCovered_leaf (3 / 16) (7 / 32) (1 / 32) (104991 / 1000000) (265837 / 2000000) (113759 / 1000000) (234163 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_25 : BoxCovered (7 / 32) (7 / 32) (1 / 64) := by
  apply boxCovered_leaf (7 / 32) (7 / 32) (1 / 64) (104991 / 1000000) (265837 / 2000000) (16173 / 125000) (202913 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_26 : BoxCovered (15 / 64) (7 / 32) (1 / 64) := by
  apply boxCovered_leaf (15 / 64) (7 / 32) (1 / 64) (742311 / 2000000) (312933 / 1000000) (273561 / 2000000) (94183 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_27 : BoxCovered (7 / 32) (15 / 64) (1 / 64) := by
  apply boxCovered_leaf (7 / 32) (15 / 64) (1 / 64) (742311 / 2000000) (312933 / 1000000) (304811 / 2000000) (39279 / 500000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_28 : BoxCovered (15 / 64) (15 / 64) (1 / 64) := by
  apply boxCovered_leaf (15 / 64) (15 / 64) (1 / 64) (742311 / 2000000) (312933 / 1000000) (273561 / 2000000) (39279 / 500000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_29 : BoxCovered (7 / 32) (7 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ0_25 using 1 <;> norm_num
  · convert coverQ0_26 using 1 <;> norm_num
  · convert coverQ0_27 using 1 <;> norm_num
  · convert coverQ0_28 using 1 <;> norm_num

theorem coverQ0_30 : BoxCovered (3 / 16) (3 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ0_22 using 1 <;> norm_num
  · convert coverQ0_23 using 1 <;> norm_num
  · convert coverQ0_24 using 1 <;> norm_num
  · convert coverQ0_29 using 1 <;> norm_num

theorem coverQ0_31 : BoxCovered (1 / 8) (1 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ0_19 using 1 <;> norm_num
  · convert coverQ0_20 using 1 <;> norm_num
  · convert coverQ0_21 using 1 <;> norm_num
  · convert coverQ0_30 using 1 <;> norm_num

theorem coverQ0_32 : BoxCovered 0 0 (1 / 4) := by
  apply boxCovered_split
  · convert coverQ0_0 using 1 <;> norm_num
  · convert coverQ0_17 using 1 <;> norm_num
  · convert coverQ0_18 using 1 <;> norm_num
  · convert coverQ0_31 using 1 <;> norm_num

theorem coverQ0_33 : BoxCovered (1 / 4) 0 (1 / 8) := by
  apply boxCovered_leaf (1 / 4) 0 (1 / 8) (186601 / 500000) (45503 / 1000000) (61601 / 500000) (79497 / 1000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_34 : BoxCovered (3 / 8) 0 (1 / 8) := by
  apply boxCovered_leaf (3 / 8) 0 (1 / 8) (186601 / 500000) (45503 / 1000000) (63399 / 500000) (79497 / 1000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_35 : BoxCovered (1 / 4) (1 / 8) (1 / 32) := by
  apply boxCovered_leaf (1 / 4) (1 / 8) (1 / 32) (186601 / 500000) (45503 / 1000000) (61601 / 500000) (110747 / 1000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_36 : BoxCovered (9 / 32) (1 / 8) (1 / 32) := by
  apply boxCovered_leaf (9 / 32) (1 / 8) (1 / 32) (186601 / 500000) (45503 / 1000000) (5747 / 62500) (110747 / 1000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_37 : BoxCovered (1 / 4) (5 / 32) (1 / 64) := by
  apply boxCovered_leaf (1 / 4) (5 / 32) (1 / 64) (104991 / 1000000) (265837 / 2000000) (80317 / 500000) (77913 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_38 : BoxCovered (17 / 64) (5 / 32) (1 / 64) := by
  apply boxCovered_leaf (17 / 64) (5 / 32) (1 / 64) (186601 / 500000) (45503 / 1000000) (107577 / 1000000) (31593 / 250000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_39 : BoxCovered (1 / 4) (11 / 64) (1 / 64) := by
  apply boxCovered_leaf (1 / 4) (11 / 64) (1 / 64) (104991 / 1000000) (265837 / 2000000) (80317 / 500000) (109163 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_40 : BoxCovered (17 / 64) (11 / 64) (1 / 128) := by
  apply boxCovered_leaf (17 / 64) (11 / 64) (1 / 128) (186601 / 500000) (45503 / 1000000) (107577 / 1000000) (268369 / 2000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_41 : BoxCovered (35 / 128) (11 / 64) (1 / 128) := by
  apply boxCovered_leaf (35 / 128) (11 / 64) (1 / 128) (186601 / 500000) (45503 / 1000000) (199529 / 2000000) (268369 / 2000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_42 : BoxCovered (17 / 64) (23 / 128) (1 / 128) := by
  apply boxCovered_leaf (17 / 64) (23 / 128) (1 / 128) (742311 / 2000000) (312933 / 1000000) (211061 / 2000000) (266491 / 2000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_43 : BoxCovered (35 / 128) (23 / 128) (1 / 128) := by
  apply boxCovered_leaf (35 / 128) (23 / 128) (1 / 128) (742311 / 2000000) (312933 / 1000000) (48859 / 500000) (266491 / 2000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_44 : BoxCovered (17 / 64) (11 / 64) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ0_40 using 1 <;> norm_num
  · convert coverQ0_41 using 1 <;> norm_num
  · convert coverQ0_42 using 1 <;> norm_num
  · convert coverQ0_43 using 1 <;> norm_num

theorem coverQ0_45 : BoxCovered (1 / 4) (5 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ0_37 using 1 <;> norm_num
  · convert coverQ0_38 using 1 <;> norm_num
  · convert coverQ0_39 using 1 <;> norm_num
  · convert coverQ0_44 using 1 <;> norm_num

theorem coverQ0_46 : BoxCovered (9 / 32) (5 / 32) (1 / 32) := by
  apply boxCovered_leaf (9 / 32) (5 / 32) (1 / 32) (186601 / 500000) (45503 / 1000000) (5747 / 62500) (141997 / 1000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_47 : BoxCovered (1 / 4) (1 / 8) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ0_35 using 1 <;> norm_num
  · convert coverQ0_36 using 1 <;> norm_num
  · convert coverQ0_45 using 1 <;> norm_num
  · convert coverQ0_46 using 1 <;> norm_num

theorem coverQ0_48 : BoxCovered (5 / 16) (1 / 8) (1 / 16) := by
  apply boxCovered_leaf (5 / 16) (1 / 8) (1 / 16) (186601 / 500000) (45503 / 1000000) (30351 / 500000) (141997 / 1000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_49 : BoxCovered (1 / 4) (3 / 16) (1 / 128) := by
  apply boxCovered_leaf (1 / 4) (3 / 16) (1 / 128) (104991 / 1000000) (265837 / 2000000) (305643 / 2000000) (31197 / 500000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_50 : BoxCovered (33 / 128) (3 / 16) (1 / 128) := by
  apply boxCovered_leaf (33 / 128) (3 / 16) (1 / 128) (104991 / 1000000) (265837 / 2000000) (80317 / 500000) (31197 / 500000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_51 : BoxCovered (1 / 4) (25 / 128) (1 / 128) := by
  apply boxCovered_leaf (1 / 4) (25 / 128) (1 / 128) (104991 / 1000000) (265837 / 2000000) (305643 / 2000000) (140413 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_52 : BoxCovered (33 / 128) (25 / 128) (1 / 128) := by
  apply boxCovered_leaf (33 / 128) (25 / 128) (1 / 128) (742311 / 2000000) (312933 / 1000000) (113343 / 1000000) (235241 / 2000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_53 : BoxCovered (1 / 4) (3 / 16) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ0_49 using 1 <;> norm_num
  · convert coverQ0_50 using 1 <;> norm_num
  · convert coverQ0_51 using 1 <;> norm_num
  · convert coverQ0_52 using 1 <;> norm_num

theorem coverQ0_54 : BoxCovered (17 / 64) (3 / 16) (1 / 64) := by
  apply boxCovered_leaf (17 / 64) (3 / 16) (1 / 64) (742311 / 2000000) (312933 / 1000000) (211061 / 2000000) (125433 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_55 : BoxCovered (1 / 4) (13 / 64) (1 / 64) := by
  apply boxCovered_leaf (1 / 4) (13 / 64) (1 / 64) (742311 / 2000000) (312933 / 1000000) (242311 / 2000000) (6863 / 62500) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_56 : BoxCovered (17 / 64) (13 / 64) (1 / 64) := by
  apply boxCovered_leaf (17 / 64) (13 / 64) (1 / 64) (742311 / 2000000) (312933 / 1000000) (211061 / 2000000) (6863 / 62500) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_57 : BoxCovered (1 / 4) (3 / 16) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ0_53 using 1 <;> norm_num
  · convert coverQ0_54 using 1 <;> norm_num
  · convert coverQ0_55 using 1 <;> norm_num
  · convert coverQ0_56 using 1 <;> norm_num

theorem coverQ0_58 : BoxCovered (9 / 32) (3 / 16) (1 / 32) := by
  apply boxCovered_leaf (9 / 32) (3 / 16) (1 / 32) (742311 / 2000000) (312933 / 1000000) (179811 / 2000000) (125433 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_59 : BoxCovered (1 / 4) (7 / 32) (1 / 32) := by
  apply boxCovered_leaf (1 / 4) (7 / 32) (1 / 32) (742311 / 2000000) (312933 / 1000000) (242311 / 2000000) (94183 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_60 : BoxCovered (9 / 32) (7 / 32) (1 / 32) := by
  apply boxCovered_leaf (9 / 32) (7 / 32) (1 / 32) (742311 / 2000000) (312933 / 1000000) (179811 / 2000000) (94183 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_61 : BoxCovered (1 / 4) (3 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ0_57 using 1 <;> norm_num
  · convert coverQ0_58 using 1 <;> norm_num
  · convert coverQ0_59 using 1 <;> norm_num
  · convert coverQ0_60 using 1 <;> norm_num

theorem coverQ0_62 : BoxCovered (5 / 16) (3 / 16) (1 / 16) := by
  apply boxCovered_leaf (5 / 16) (3 / 16) (1 / 16) (742311 / 2000000) (312933 / 1000000) (117311 / 2000000) (125433 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_63 : BoxCovered (1 / 4) (1 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ0_47 using 1 <;> norm_num
  · convert coverQ0_48 using 1 <;> norm_num
  · convert coverQ0_61 using 1 <;> norm_num
  · convert coverQ0_62 using 1 <;> norm_num

theorem coverQ0_64 : BoxCovered (3 / 8) (1 / 8) (1 / 16) := by
  apply boxCovered_leaf (3 / 8) (1 / 8) (1 / 16) (186601 / 500000) (45503 / 1000000) (32149 / 500000) (141997 / 1000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_65 : BoxCovered (7 / 16) (1 / 8) (1 / 32) := by
  apply boxCovered_leaf (7 / 16) (1 / 8) (1 / 32) (186601 / 500000) (45503 / 1000000) (23887 / 250000) (110747 / 1000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_66 : BoxCovered (15 / 32) (1 / 8) (1 / 32) := by
  apply boxCovered_leaf (15 / 32) (1 / 8) (1 / 32) (186601 / 500000) (45503 / 1000000) (63399 / 500000) (110747 / 1000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_67 : BoxCovered (7 / 16) (5 / 32) (1 / 32) := by
  apply boxCovered_leaf (7 / 16) (5 / 32) (1 / 32) (186601 / 500000) (45503 / 1000000) (23887 / 250000) (141997 / 1000000) ⟨1, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_68 : BoxCovered (15 / 32) (5 / 32) (1 / 32) := by
  apply boxCovered_leaf (15 / 32) (5 / 32) (1 / 32) (1267243 / 2000000) (34689 / 250000) (329743 / 2000000) (6093 / 125000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_69 : BoxCovered (7 / 16) (1 / 8) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ0_65 using 1 <;> norm_num
  · convert coverQ0_66 using 1 <;> norm_num
  · convert coverQ0_67 using 1 <;> norm_num
  · convert coverQ0_68 using 1 <;> norm_num

theorem coverQ0_70 : BoxCovered (3 / 8) (3 / 16) (1 / 16) := by
  apply boxCovered_leaf (3 / 8) (3 / 16) (1 / 16) (742311 / 2000000) (312933 / 1000000) (132689 / 2000000) (125433 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_71 : BoxCovered (7 / 16) (3 / 16) (1 / 32) := by
  apply boxCovered_leaf (7 / 16) (3 / 16) (1 / 32) (742311 / 2000000) (312933 / 1000000) (195189 / 2000000) (125433 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_72 : BoxCovered (15 / 32) (3 / 16) (1 / 64) := by
  apply boxCovered_leaf (15 / 32) (3 / 16) (1 / 64) (742311 / 2000000) (312933 / 1000000) (226439 / 2000000) (125433 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_73 : BoxCovered (31 / 64) (3 / 16) (1 / 64) := by
  apply boxCovered_leaf (31 / 64) (3 / 16) (1 / 64) (1267243 / 2000000) (34689 / 250000) (298493 / 2000000) (64369 / 1000000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_74 : BoxCovered (15 / 32) (13 / 64) (1 / 64) := by
  apply boxCovered_leaf (15 / 32) (13 / 64) (1 / 64) (742311 / 2000000) (312933 / 1000000) (226439 / 2000000) (6863 / 62500) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_75 : BoxCovered (31 / 64) (13 / 64) (1 / 64) := by
  apply boxCovered_leaf (31 / 64) (13 / 64) (1 / 64) (1267243 / 2000000) (34689 / 250000) (298493 / 2000000) (39997 / 500000) ⟨2, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_76 : BoxCovered (15 / 32) (3 / 16) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ0_72 using 1 <;> norm_num
  · convert coverQ0_73 using 1 <;> norm_num
  · convert coverQ0_74 using 1 <;> norm_num
  · convert coverQ0_75 using 1 <;> norm_num

theorem coverQ0_77 : BoxCovered (7 / 16) (7 / 32) (1 / 32) := by
  apply boxCovered_leaf (7 / 16) (7 / 32) (1 / 32) (742311 / 2000000) (312933 / 1000000) (195189 / 2000000) (94183 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_78 : BoxCovered (15 / 32) (7 / 32) (1 / 32) := by
  apply boxCovered_leaf (15 / 32) (7 / 32) (1 / 32) (742311 / 2000000) (312933 / 1000000) (257689 / 2000000) (94183 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_79 : BoxCovered (7 / 16) (3 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ0_71 using 1 <;> norm_num
  · convert coverQ0_76 using 1 <;> norm_num
  · convert coverQ0_77 using 1 <;> norm_num
  · convert coverQ0_78 using 1 <;> norm_num

theorem coverQ0_80 : BoxCovered (3 / 8) (1 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ0_64 using 1 <;> norm_num
  · convert coverQ0_69 using 1 <;> norm_num
  · convert coverQ0_70 using 1 <;> norm_num
  · convert coverQ0_79 using 1 <;> norm_num

theorem coverQ0_81 : BoxCovered (1 / 4) 0 (1 / 4) := by
  apply boxCovered_split
  · convert coverQ0_33 using 1 <;> norm_num
  · convert coverQ0_34 using 1 <;> norm_num
  · convert coverQ0_63 using 1 <;> norm_num
  · convert coverQ0_80 using 1 <;> norm_num

theorem coverQ0_82 : BoxCovered 0 (1 / 4) (1 / 64) := by
  apply boxCovered_leaf 0 (1 / 4) (1 / 64) (104991 / 1000000) (265837 / 2000000) (104991 / 1000000) (265413 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_83 : BoxCovered (1 / 64) (1 / 4) (1 / 64) := by
  apply boxCovered_leaf (1 / 64) (1 / 4) (1 / 64) (104991 / 1000000) (265837 / 2000000) (44683 / 500000) (265413 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_84 : BoxCovered 0 (17 / 64) (1 / 64) := by
  apply boxCovered_leaf 0 (17 / 64) (1 / 64) (206181 / 2000000) (400379 / 1000000) (206181 / 2000000) (67377 / 500000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_85 : BoxCovered (1 / 64) (17 / 64) (1 / 64) := by
  apply boxCovered_leaf (1 / 64) (17 / 64) (1 / 64) (206181 / 2000000) (400379 / 1000000) (174931 / 2000000) (67377 / 500000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_86 : BoxCovered 0 (1 / 4) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ0_82 using 1 <;> norm_num
  · convert coverQ0_83 using 1 <;> norm_num
  · convert coverQ0_84 using 1 <;> norm_num
  · convert coverQ0_85 using 1 <;> norm_num

theorem coverQ0_87 : BoxCovered (1 / 32) (1 / 4) (1 / 32) := by
  apply boxCovered_leaf (1 / 32) (1 / 4) (1 / 32) (104991 / 1000000) (265837 / 2000000) (73741 / 1000000) (296663 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_88 : BoxCovered 0 (9 / 32) (1 / 32) := by
  apply boxCovered_leaf 0 (9 / 32) (1 / 32) (206181 / 2000000) (400379 / 1000000) (206181 / 2000000) (119129 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_89 : BoxCovered (1 / 32) (9 / 32) (1 / 32) := by
  apply boxCovered_leaf (1 / 32) (9 / 32) (1 / 32) (206181 / 2000000) (400379 / 1000000) (143681 / 2000000) (119129 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_90 : BoxCovered 0 (1 / 4) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ0_86 using 1 <;> norm_num
  · convert coverQ0_87 using 1 <;> norm_num
  · convert coverQ0_88 using 1 <;> norm_num
  · convert coverQ0_89 using 1 <;> norm_num

theorem coverQ0_91 : BoxCovered (1 / 16) (1 / 4) (1 / 16) := by
  apply boxCovered_leaf (1 / 16) (1 / 4) (1 / 16) (206181 / 2000000) (400379 / 1000000) (81181 / 2000000) (150379 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_92 : BoxCovered 0 (5 / 16) (1 / 16) := by
  apply boxCovered_leaf 0 (5 / 16) (1 / 16) (206181 / 2000000) (400379 / 1000000) (206181 / 2000000) (87879 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_93 : BoxCovered (1 / 16) (5 / 16) (1 / 16) := by
  apply boxCovered_leaf (1 / 16) (5 / 16) (1 / 16) (206181 / 2000000) (400379 / 1000000) (81181 / 2000000) (87879 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_94 : BoxCovered 0 (1 / 4) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ0_90 using 1 <;> norm_num
  · convert coverQ0_91 using 1 <;> norm_num
  · convert coverQ0_92 using 1 <;> norm_num
  · convert coverQ0_93 using 1 <;> norm_num

theorem coverQ0_95 : BoxCovered (1 / 8) (1 / 4) (1 / 16) := by
  apply boxCovered_leaf (1 / 8) (1 / 4) (1 / 16) (206181 / 2000000) (400379 / 1000000) (168819 / 2000000) (150379 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_96 : BoxCovered (3 / 16) (1 / 4) (1 / 64) := by
  apply boxCovered_leaf (3 / 16) (1 / 4) (1 / 64) (104991 / 1000000) (265837 / 2000000) (49067 / 500000) (265413 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_97 : BoxCovered (13 / 64) (1 / 4) (1 / 128) := by
  apply boxCovered_leaf (13 / 64) (1 / 4) (1 / 128) (104991 / 1000000) (265837 / 2000000) (211893 / 2000000) (62447 / 500000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_98 : BoxCovered (27 / 128) (1 / 4) (1 / 128) := by
  apply boxCovered_leaf (27 / 128) (1 / 4) (1 / 128) (104991 / 1000000) (265837 / 2000000) (113759 / 1000000) (62447 / 500000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_99 : BoxCovered (13 / 64) (33 / 128) (1 / 128) := by
  apply boxCovered_leaf (13 / 64) (33 / 128) (1 / 128) (104991 / 1000000) (265837 / 2000000) (211893 / 2000000) (265413 / 2000000) ⟨0, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_100 : BoxCovered (27 / 128) (33 / 128) (1 / 128) := by
  apply boxCovered_leaf (27 / 128) (33 / 128) (1 / 128) (742311 / 2000000) (312933 / 1000000) (80109 / 500000) (110241 / 2000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_101 : BoxCovered (13 / 64) (1 / 4) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ0_97 using 1 <;> norm_num
  · convert coverQ0_98 using 1 <;> norm_num
  · convert coverQ0_99 using 1 <;> norm_num
  · convert coverQ0_100 using 1 <;> norm_num

theorem coverQ0_102 : BoxCovered (3 / 16) (17 / 64) (1 / 64) := by
  apply boxCovered_leaf (3 / 16) (17 / 64) (1 / 64) (206181 / 2000000) (400379 / 1000000) (200069 / 2000000) (67377 / 500000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_103 : BoxCovered (13 / 64) (17 / 64) (1 / 128) := by
  apply boxCovered_leaf (13 / 64) (17 / 64) (1 / 128) (206181 / 2000000) (400379 / 1000000) (107847 / 1000000) (67377 / 500000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_104 : BoxCovered (27 / 128) (17 / 64) (1 / 128) := by
  apply boxCovered_leaf (27 / 128) (17 / 64) (1 / 128) (742311 / 2000000) (312933 / 1000000) (80109 / 500000) (11827 / 250000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_105 : BoxCovered (13 / 64) (35 / 128) (1 / 128) := by
  apply boxCovered_leaf (13 / 64) (35 / 128) (1 / 128) (206181 / 2000000) (400379 / 1000000) (107847 / 1000000) (253883 / 2000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_106 : BoxCovered (27 / 128) (35 / 128) (1 / 128) := by
  apply boxCovered_leaf (27 / 128) (35 / 128) (1 / 128) (206181 / 2000000) (400379 / 1000000) (231319 / 2000000) (253883 / 2000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_107 : BoxCovered (13 / 64) (17 / 64) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ0_103 using 1 <;> norm_num
  · convert coverQ0_104 using 1 <;> norm_num
  · convert coverQ0_105 using 1 <;> norm_num
  · convert coverQ0_106 using 1 <;> norm_num

theorem coverQ0_108 : BoxCovered (3 / 16) (1 / 4) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ0_96 using 1 <;> norm_num
  · convert coverQ0_101 using 1 <;> norm_num
  · convert coverQ0_102 using 1 <;> norm_num
  · convert coverQ0_107 using 1 <;> norm_num

theorem coverQ0_109 : BoxCovered (7 / 32) (1 / 4) (1 / 32) := by
  apply boxCovered_leaf (7 / 32) (1 / 4) (1 / 32) (742311 / 2000000) (312933 / 1000000) (304811 / 2000000) (62933 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_110 : BoxCovered (3 / 16) (9 / 32) (1 / 32) := by
  apply boxCovered_leaf (3 / 16) (9 / 32) (1 / 32) (206181 / 2000000) (400379 / 1000000) (231319 / 2000000) (119129 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_111 : BoxCovered (7 / 32) (9 / 32) (1 / 32) := by
  apply boxCovered_leaf (7 / 32) (9 / 32) (1 / 32) (742311 / 2000000) (312933 / 1000000) (304811 / 2000000) (31683 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_112 : BoxCovered (3 / 16) (1 / 4) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ0_108 using 1 <;> norm_num
  · convert coverQ0_109 using 1 <;> norm_num
  · convert coverQ0_110 using 1 <;> norm_num
  · convert coverQ0_111 using 1 <;> norm_num

theorem coverQ0_113 : BoxCovered (1 / 8) (5 / 16) (1 / 16) := by
  apply boxCovered_leaf (1 / 8) (5 / 16) (1 / 16) (206181 / 2000000) (400379 / 1000000) (168819 / 2000000) (87879 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_114 : BoxCovered (3 / 16) (5 / 16) (1 / 16) := by
  apply boxCovered_leaf (3 / 16) (5 / 16) (1 / 16) (206181 / 2000000) (400379 / 1000000) (293819 / 2000000) (87879 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_115 : BoxCovered (1 / 8) (1 / 4) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ0_95 using 1 <;> norm_num
  · convert coverQ0_112 using 1 <;> norm_num
  · convert coverQ0_113 using 1 <;> norm_num
  · convert coverQ0_114 using 1 <;> norm_num

theorem coverQ0_116 : BoxCovered 0 (3 / 8) (1 / 8) := by
  apply boxCovered_leaf 0 (3 / 8) (1 / 8) (206181 / 2000000) (400379 / 1000000) (206181 / 2000000) (99621 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_117 : BoxCovered (1 / 8) (3 / 8) (1 / 16) := by
  apply boxCovered_leaf (1 / 8) (3 / 8) (1 / 16) (206181 / 2000000) (400379 / 1000000) (168819 / 2000000) (37121 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_118 : BoxCovered (3 / 16) (3 / 8) (1 / 16) := by
  apply boxCovered_leaf (3 / 16) (3 / 8) (1 / 16) (206181 / 2000000) (400379 / 1000000) (293819 / 2000000) (37121 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_119 : BoxCovered (1 / 8) (7 / 16) (1 / 16) := by
  apply boxCovered_leaf (1 / 8) (7 / 16) (1 / 16) (206181 / 2000000) (400379 / 1000000) (168819 / 2000000) (99621 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_120 : BoxCovered (3 / 16) (7 / 16) (1 / 32) := by
  apply boxCovered_leaf (3 / 16) (7 / 16) (1 / 32) (206181 / 2000000) (400379 / 1000000) (231319 / 2000000) (68371 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_121 : BoxCovered (7 / 32) (7 / 16) (1 / 32) := by
  apply boxCovered_leaf (7 / 32) (7 / 16) (1 / 32) (206181 / 2000000) (400379 / 1000000) (293819 / 2000000) (68371 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_122 : BoxCovered (3 / 16) (15 / 32) (1 / 32) := by
  apply boxCovered_leaf (3 / 16) (15 / 32) (1 / 32) (206181 / 2000000) (400379 / 1000000) (231319 / 2000000) (99621 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_123 : BoxCovered (7 / 32) (15 / 32) (1 / 64) := by
  apply boxCovered_leaf (7 / 32) (15 / 32) (1 / 64) (206181 / 2000000) (400379 / 1000000) (262569 / 2000000) (20999 / 250000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_124 : BoxCovered (15 / 64) (15 / 32) (1 / 64) := by
  apply boxCovered_leaf (15 / 64) (15 / 32) (1 / 64) (206181 / 2000000) (400379 / 1000000) (293819 / 2000000) (20999 / 250000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_125 : BoxCovered (7 / 32) (31 / 64) (1 / 64) := by
  apply boxCovered_leaf (7 / 32) (31 / 64) (1 / 64) (206181 / 2000000) (400379 / 1000000) (262569 / 2000000) (99621 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_126 : BoxCovered (15 / 64) (31 / 64) (1 / 64) := by
  apply boxCovered_leaf (15 / 64) (31 / 64) (1 / 64) (364743 / 1000000) (233591 / 400000) (2037 / 15625) (39841 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_127 : BoxCovered (7 / 32) (15 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ0_123 using 1 <;> norm_num
  · convert coverQ0_124 using 1 <;> norm_num
  · convert coverQ0_125 using 1 <;> norm_num
  · convert coverQ0_126 using 1 <;> norm_num

theorem coverQ0_128 : BoxCovered (3 / 16) (7 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ0_120 using 1 <;> norm_num
  · convert coverQ0_121 using 1 <;> norm_num
  · convert coverQ0_122 using 1 <;> norm_num
  · convert coverQ0_127 using 1 <;> norm_num

theorem coverQ0_129 : BoxCovered (1 / 8) (3 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ0_117 using 1 <;> norm_num
  · convert coverQ0_118 using 1 <;> norm_num
  · convert coverQ0_119 using 1 <;> norm_num
  · convert coverQ0_128 using 1 <;> norm_num

theorem coverQ0_130 : BoxCovered 0 (1 / 4) (1 / 4) := by
  apply boxCovered_split
  · convert coverQ0_94 using 1 <;> norm_num
  · convert coverQ0_115 using 1 <;> norm_num
  · convert coverQ0_116 using 1 <;> norm_num
  · convert coverQ0_129 using 1 <;> norm_num

theorem coverQ0_131 : BoxCovered (1 / 4) (1 / 4) (1 / 8) := by
  apply boxCovered_leaf (1 / 4) (1 / 4) (1 / 8) (742311 / 2000000) (312933 / 1000000) (242311 / 2000000) (62933 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_132 : BoxCovered (3 / 8) (1 / 4) (1 / 8) := by
  apply boxCovered_leaf (3 / 8) (1 / 4) (1 / 8) (742311 / 2000000) (312933 / 1000000) (257689 / 2000000) (62933 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_133 : BoxCovered (1 / 4) (3 / 8) (1 / 32) := by
  apply boxCovered_leaf (1 / 4) (3 / 8) (1 / 32) (742311 / 2000000) (312933 / 1000000) (242311 / 2000000) (93317 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_134 : BoxCovered (9 / 32) (3 / 8) (1 / 32) := by
  apply boxCovered_leaf (9 / 32) (3 / 8) (1 / 32) (742311 / 2000000) (312933 / 1000000) (179811 / 2000000) (93317 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_135 : BoxCovered (1 / 4) (13 / 32) (1 / 64) := by
  apply boxCovered_leaf (1 / 4) (13 / 32) (1 / 64) (206181 / 2000000) (400379 / 1000000) (325069 / 2000000) (2687 / 125000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_136 : BoxCovered (17 / 64) (13 / 32) (1 / 64) := by
  apply boxCovered_leaf (17 / 64) (13 / 32) (1 / 64) (742311 / 2000000) (312933 / 1000000) (211061 / 2000000) (54471 / 500000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_137 : BoxCovered (1 / 4) (27 / 64) (1 / 64) := by
  apply boxCovered_leaf (1 / 4) (27 / 64) (1 / 64) (206181 / 2000000) (400379 / 1000000) (325069 / 2000000) (37121 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_138 : BoxCovered (17 / 64) (27 / 64) (1 / 64) := by
  apply boxCovered_leaf (17 / 64) (27 / 64) (1 / 64) (742311 / 2000000) (312933 / 1000000) (211061 / 2000000) (124567 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_139 : BoxCovered (1 / 4) (13 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ0_135 using 1 <;> norm_num
  · convert coverQ0_136 using 1 <;> norm_num
  · convert coverQ0_137 using 1 <;> norm_num
  · convert coverQ0_138 using 1 <;> norm_num

theorem coverQ0_140 : BoxCovered (9 / 32) (13 / 32) (1 / 32) := by
  apply boxCovered_leaf (9 / 32) (13 / 32) (1 / 32) (742311 / 2000000) (312933 / 1000000) (179811 / 2000000) (124567 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_141 : BoxCovered (1 / 4) (3 / 8) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ0_133 using 1 <;> norm_num
  · convert coverQ0_134 using 1 <;> norm_num
  · convert coverQ0_139 using 1 <;> norm_num
  · convert coverQ0_140 using 1 <;> norm_num

theorem coverQ0_142 : BoxCovered (5 / 16) (3 / 8) (1 / 16) := by
  apply boxCovered_leaf (5 / 16) (3 / 8) (1 / 16) (742311 / 2000000) (312933 / 1000000) (117311 / 2000000) (124567 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_143 : BoxCovered (1 / 4) (7 / 16) (1 / 64) := by
  apply boxCovered_leaf (1 / 4) (7 / 16) (1 / 64) (206181 / 2000000) (400379 / 1000000) (325069 / 2000000) (26373 / 500000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_144 : BoxCovered (17 / 64) (7 / 16) (1 / 128) := by
  apply boxCovered_leaf (17 / 64) (7 / 16) (1 / 128) (742311 / 2000000) (312933 / 1000000) (211061 / 2000000) (264759 / 2000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_145 : BoxCovered (35 / 128) (7 / 16) (1 / 128) := by
  apply boxCovered_leaf (35 / 128) (7 / 16) (1 / 128) (742311 / 2000000) (312933 / 1000000) (48859 / 500000) (264759 / 2000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_146 : BoxCovered (17 / 64) (57 / 128) (1 / 128) := by
  apply boxCovered_leaf (17 / 64) (57 / 128) (1 / 128) (364743 / 1000000) (233591 / 400000) (49559 / 500000) (27733 / 200000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_147 : BoxCovered (35 / 128) (57 / 128) (1 / 128) := by
  apply boxCovered_leaf (35 / 128) (57 / 128) (1 / 128) (742311 / 2000000) (312933 / 1000000) (48859 / 500000) (4381 / 31250) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_148 : BoxCovered (17 / 64) (7 / 16) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ0_144 using 1 <;> norm_num
  · convert coverQ0_145 using 1 <;> norm_num
  · convert coverQ0_146 using 1 <;> norm_num
  · convert coverQ0_147 using 1 <;> norm_num

theorem coverQ0_149 : BoxCovered (1 / 4) (29 / 64) (1 / 128) := by
  apply boxCovered_leaf (1 / 4) (29 / 64) (1 / 128) (206181 / 2000000) (400379 / 1000000) (77361 / 500000) (121117 / 2000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_150 : BoxCovered (33 / 128) (29 / 64) (1 / 128) := by
  apply boxCovered_leaf (33 / 128) (29 / 64) (1 / 128) (364743 / 1000000) (233591 / 400000) (213861 / 2000000) (52341 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_151 : BoxCovered (1 / 4) (59 / 128) (1 / 128) := by
  apply boxCovered_leaf (1 / 4) (59 / 128) (1 / 128) (206181 / 2000000) (400379 / 1000000) (77361 / 500000) (68371 / 1000000) ⟨4, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_152 : BoxCovered (33 / 128) (59 / 128) (1 / 128) := by
  apply boxCovered_leaf (33 / 128) (59 / 128) (1 / 128) (364743 / 1000000) (233591 / 400000) (213861 / 2000000) (769 / 6250) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_153 : BoxCovered (1 / 4) (29 / 64) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ0_149 using 1 <;> norm_num
  · convert coverQ0_150 using 1 <;> norm_num
  · convert coverQ0_151 using 1 <;> norm_num
  · convert coverQ0_152 using 1 <;> norm_num

theorem coverQ0_154 : BoxCovered (17 / 64) (29 / 64) (1 / 64) := by
  apply boxCovered_leaf (17 / 64) (29 / 64) (1 / 64) (364743 / 1000000) (233591 / 400000) (49559 / 500000) (52341 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_155 : BoxCovered (1 / 4) (7 / 16) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ0_143 using 1 <;> norm_num
  · convert coverQ0_148 using 1 <;> norm_num
  · convert coverQ0_153 using 1 <;> norm_num
  · convert coverQ0_154 using 1 <;> norm_num

theorem coverQ0_156 : BoxCovered (9 / 32) (7 / 16) (1 / 32) := by
  apply boxCovered_leaf (9 / 32) (7 / 16) (1 / 32) (364743 / 1000000) (233591 / 400000) (83493 / 1000000) (58591 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_157 : BoxCovered (1 / 4) (15 / 32) (1 / 32) := by
  apply boxCovered_leaf (1 / 4) (15 / 32) (1 / 32) (364743 / 1000000) (233591 / 400000) (114743 / 1000000) (46091 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_158 : BoxCovered (9 / 32) (15 / 32) (1 / 32) := by
  apply boxCovered_leaf (9 / 32) (15 / 32) (1 / 32) (364743 / 1000000) (233591 / 400000) (83493 / 1000000) (46091 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_159 : BoxCovered (1 / 4) (7 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ0_155 using 1 <;> norm_num
  · convert coverQ0_156 using 1 <;> norm_num
  · convert coverQ0_157 using 1 <;> norm_num
  · convert coverQ0_158 using 1 <;> norm_num

theorem coverQ0_160 : BoxCovered (5 / 16) (7 / 16) (1 / 16) := by
  apply boxCovered_leaf (5 / 16) (7 / 16) (1 / 16) (364743 / 1000000) (233591 / 400000) (52243 / 1000000) (58591 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_161 : BoxCovered (1 / 4) (3 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ0_141 using 1 <;> norm_num
  · convert coverQ0_142 using 1 <;> norm_num
  · convert coverQ0_159 using 1 <;> norm_num
  · convert coverQ0_160 using 1 <;> norm_num

theorem coverQ0_162 : BoxCovered (3 / 8) (3 / 8) (1 / 16) := by
  apply boxCovered_leaf (3 / 8) (3 / 8) (1 / 16) (742311 / 2000000) (312933 / 1000000) (132689 / 2000000) (124567 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_163 : BoxCovered (7 / 16) (3 / 8) (1 / 32) := by
  apply boxCovered_leaf (7 / 16) (3 / 8) (1 / 32) (742311 / 2000000) (312933 / 1000000) (195189 / 2000000) (93317 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_164 : BoxCovered (15 / 32) (3 / 8) (1 / 32) := by
  apply boxCovered_leaf (15 / 32) (3 / 8) (1 / 32) (742311 / 2000000) (312933 / 1000000) (257689 / 2000000) (93317 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_165 : BoxCovered (7 / 16) (13 / 32) (1 / 32) := by
  apply boxCovered_leaf (7 / 16) (13 / 32) (1 / 32) (742311 / 2000000) (312933 / 1000000) (195189 / 2000000) (124567 / 1000000) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_166 : BoxCovered (15 / 32) (13 / 32) (1 / 32) := by
  apply boxCovered_leaf (15 / 32) (13 / 32) (1 / 32) (635257 / 1000000) (166409 / 400000) (166507 / 1000000) (8591 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_167 : BoxCovered (7 / 16) (3 / 8) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ0_163 using 1 <;> norm_num
  · convert coverQ0_164 using 1 <;> norm_num
  · convert coverQ0_165 using 1 <;> norm_num
  · convert coverQ0_166 using 1 <;> norm_num

theorem coverQ0_168 : BoxCovered (3 / 8) (7 / 16) (1 / 16) := by
  apply boxCovered_leaf (3 / 8) (7 / 16) (1 / 16) (364743 / 1000000) (233591 / 400000) (72757 / 1000000) (58591 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_169 : BoxCovered (7 / 16) (7 / 16) (1 / 64) := by
  apply boxCovered_leaf (7 / 16) (7 / 16) (1 / 64) (742311 / 2000000) (312933 / 1000000) (163939 / 2000000) (4381 / 31250) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_170 : BoxCovered (29 / 64) (7 / 16) (1 / 64) := by
  apply boxCovered_leaf (29 / 64) (7 / 16) (1 / 64) (742311 / 2000000) (312933 / 1000000) (195189 / 2000000) (4381 / 31250) ⟨5, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_171 : BoxCovered (7 / 16) (29 / 64) (1 / 64) := by
  apply boxCovered_leaf (7 / 16) (29 / 64) (1 / 64) (364743 / 1000000) (233591 / 400000) (44191 / 500000) (52341 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_172 : BoxCovered (29 / 64) (29 / 64) (1 / 64) := by
  apply boxCovered_leaf (29 / 64) (29 / 64) (1 / 64) (364743 / 1000000) (233591 / 400000) (104007 / 1000000) (52341 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_173 : BoxCovered (7 / 16) (7 / 16) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ0_169 using 1 <;> norm_num
  · convert coverQ0_170 using 1 <;> norm_num
  · convert coverQ0_171 using 1 <;> norm_num
  · convert coverQ0_172 using 1 <;> norm_num

theorem coverQ0_174 : BoxCovered (15 / 32) (7 / 16) (1 / 64) := by
  apply boxCovered_leaf (15 / 32) (7 / 16) (1 / 64) (635257 / 1000000) (166409 / 400000) (166507 / 1000000) (14841 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_175 : BoxCovered (31 / 64) (7 / 16) (1 / 64) := by
  apply boxCovered_leaf (31 / 64) (7 / 16) (1 / 64) (635257 / 1000000) (166409 / 400000) (75441 / 500000) (14841 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_176 : BoxCovered (15 / 32) (29 / 64) (1 / 128) := by
  apply boxCovered_leaf (15 / 32) (29 / 64) (1 / 128) (635257 / 1000000) (166409 / 400000) (166507 / 1000000) (8983 / 200000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_177 : BoxCovered (61 / 128) (29 / 64) (1 / 128) := by
  apply boxCovered_leaf (61 / 128) (29 / 64) (1 / 128) (635257 / 1000000) (166409 / 400000) (317389 / 2000000) (8983 / 200000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_178 : BoxCovered (15 / 32) (59 / 128) (1 / 128) := by
  apply boxCovered_leaf (15 / 32) (59 / 128) (1 / 128) (364743 / 1000000) (233591 / 400000) (223639 / 2000000) (769 / 6250) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_179 : BoxCovered (61 / 128) (59 / 128) (1 / 128) := by
  apply boxCovered_leaf (61 / 128) (59 / 128) (1 / 128) (635257 / 1000000) (166409 / 400000) (317389 / 2000000) (21091 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_180 : BoxCovered (15 / 32) (29 / 64) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ0_176 using 1 <;> norm_num
  · convert coverQ0_177 using 1 <;> norm_num
  · convert coverQ0_178 using 1 <;> norm_num
  · convert coverQ0_179 using 1 <;> norm_num

theorem coverQ0_181 : BoxCovered (31 / 64) (29 / 64) (1 / 64) := by
  apply boxCovered_leaf (31 / 64) (29 / 64) (1 / 64) (635257 / 1000000) (166409 / 400000) (75441 / 500000) (21091 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_182 : BoxCovered (15 / 32) (7 / 16) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ0_174 using 1 <;> norm_num
  · convert coverQ0_175 using 1 <;> norm_num
  · convert coverQ0_180 using 1 <;> norm_num
  · convert coverQ0_181 using 1 <;> norm_num

theorem coverQ0_183 : BoxCovered (7 / 16) (15 / 32) (1 / 32) := by
  apply boxCovered_leaf (7 / 16) (15 / 32) (1 / 32) (364743 / 1000000) (233591 / 400000) (104007 / 1000000) (46091 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_184 : BoxCovered (15 / 32) (15 / 32) (1 / 64) := by
  apply boxCovered_leaf (15 / 32) (15 / 32) (1 / 64) (364743 / 1000000) (233591 / 400000) (7477 / 62500) (46091 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_185 : BoxCovered (31 / 64) (15 / 32) (1 / 64) := by
  apply boxCovered_leaf (31 / 64) (15 / 32) (1 / 64) (635257 / 1000000) (166409 / 400000) (75441 / 500000) (27341 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_186 : BoxCovered (15 / 32) (31 / 64) (1 / 64) := by
  apply boxCovered_leaf (15 / 32) (31 / 64) (1 / 64) (364743 / 1000000) (233591 / 400000) (7477 / 62500) (39841 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_187 : BoxCovered (31 / 64) (31 / 64) (1 / 64) := by
  apply boxCovered_leaf (31 / 64) (31 / 64) (1 / 64) (635257 / 1000000) (166409 / 400000) (75441 / 500000) (33591 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ0_188 : BoxCovered (15 / 32) (15 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ0_184 using 1 <;> norm_num
  · convert coverQ0_185 using 1 <;> norm_num
  · convert coverQ0_186 using 1 <;> norm_num
  · convert coverQ0_187 using 1 <;> norm_num

theorem coverQ0_189 : BoxCovered (7 / 16) (7 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ0_173 using 1 <;> norm_num
  · convert coverQ0_182 using 1 <;> norm_num
  · convert coverQ0_183 using 1 <;> norm_num
  · convert coverQ0_188 using 1 <;> norm_num

theorem coverQ0_190 : BoxCovered (3 / 8) (3 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ0_162 using 1 <;> norm_num
  · convert coverQ0_167 using 1 <;> norm_num
  · convert coverQ0_168 using 1 <;> norm_num
  · convert coverQ0_189 using 1 <;> norm_num

theorem coverQ0_191 : BoxCovered (1 / 4) (1 / 4) (1 / 4) := by
  apply boxCovered_split
  · convert coverQ0_131 using 1 <;> norm_num
  · convert coverQ0_132 using 1 <;> norm_num
  · convert coverQ0_161 using 1 <;> norm_num
  · convert coverQ0_190 using 1 <;> norm_num

theorem coverQ0_192 : BoxCovered 0 0 (1 / 2) := by
  apply boxCovered_split
  · convert coverQ0_32 using 1 <;> norm_num
  · convert coverQ0_81 using 1 <;> norm_num
  · convert coverQ0_130 using 1 <;> norm_num
  · convert coverQ0_191 using 1 <;> norm_num

theorem coverQuadrant0 : BoxCovered 0 0 (1/2) := coverQ0_192

end ElevenSquare
