import ElevenSquare.CoverChecks

/-! Generated exact dyadic covering witness. Every numerical premise is
proved by kernel-checked `norm_num`; no external PASS flag is assumed. -/
namespace ElevenSquare
set_option maxHeartbeats 0
set_option linter.unnecessarySeqFocus false

theorem coverQ3_0 : BoxCovered (1 / 2) (1 / 2) (1 / 64) := by
  apply boxCovered_leaf (1 / 2) (1 / 2) (1 / 64) (635257 / 1000000) (166409 / 400000) (135257 / 1000000) (39841 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_1 : BoxCovered (33 / 64) (1 / 2) (1 / 64) := by
  apply boxCovered_leaf (33 / 64) (1 / 2) (1 / 64) (635257 / 1000000) (166409 / 400000) (7477 / 62500) (39841 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_2 : BoxCovered (1 / 2) (33 / 64) (1 / 64) := by
  apply boxCovered_leaf (1 / 2) (33 / 64) (1 / 64) (364743 / 1000000) (233591 / 400000) (75441 / 500000) (27341 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_3 : BoxCovered (33 / 64) (33 / 64) (1 / 64) := by
  apply boxCovered_leaf (33 / 64) (33 / 64) (1 / 64) (635257 / 1000000) (166409 / 400000) (7477 / 62500) (46091 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_4 : BoxCovered (1 / 2) (1 / 2) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ3_0 using 1 <;> norm_num
  · convert coverQ3_1 using 1 <;> norm_num
  · convert coverQ3_2 using 1 <;> norm_num
  · convert coverQ3_3 using 1 <;> norm_num

theorem coverQ3_5 : BoxCovered (17 / 32) (1 / 2) (1 / 32) := by
  apply boxCovered_leaf (17 / 32) (1 / 2) (1 / 32) (635257 / 1000000) (166409 / 400000) (104007 / 1000000) (46091 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_6 : BoxCovered (1 / 2) (17 / 32) (1 / 64) := by
  apply boxCovered_leaf (1 / 2) (17 / 32) (1 / 64) (364743 / 1000000) (233591 / 400000) (75441 / 500000) (21091 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_7 : BoxCovered (33 / 64) (17 / 32) (1 / 128) := by
  apply boxCovered_leaf (33 / 64) (17 / 32) (1 / 128) (635257 / 1000000) (166409 / 400000) (7477 / 62500) (769 / 6250) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_8 : BoxCovered (67 / 128) (17 / 32) (1 / 128) := by
  apply boxCovered_leaf (67 / 128) (17 / 32) (1 / 128) (635257 / 1000000) (166409 / 400000) (223639 / 2000000) (769 / 6250) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_9 : BoxCovered (33 / 64) (69 / 128) (1 / 128) := by
  apply boxCovered_leaf (33 / 64) (69 / 128) (1 / 128) (364743 / 1000000) (233591 / 400000) (317389 / 2000000) (8983 / 200000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_10 : BoxCovered (67 / 128) (69 / 128) (1 / 128) := by
  apply boxCovered_leaf (67 / 128) (69 / 128) (1 / 128) (635257 / 1000000) (166409 / 400000) (223639 / 2000000) (52341 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_11 : BoxCovered (33 / 64) (17 / 32) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ3_7 using 1 <;> norm_num
  · convert coverQ3_8 using 1 <;> norm_num
  · convert coverQ3_9 using 1 <;> norm_num
  · convert coverQ3_10 using 1 <;> norm_num

theorem coverQ3_12 : BoxCovered (1 / 2) (35 / 64) (1 / 64) := by
  apply boxCovered_leaf (1 / 2) (35 / 64) (1 / 64) (364743 / 1000000) (233591 / 400000) (75441 / 500000) (14841 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_13 : BoxCovered (33 / 64) (35 / 64) (1 / 64) := by
  apply boxCovered_leaf (33 / 64) (35 / 64) (1 / 64) (364743 / 1000000) (233591 / 400000) (166507 / 1000000) (14841 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_14 : BoxCovered (1 / 2) (17 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ3_6 using 1 <;> norm_num
  · convert coverQ3_11 using 1 <;> norm_num
  · convert coverQ3_12 using 1 <;> norm_num
  · convert coverQ3_13 using 1 <;> norm_num

theorem coverQ3_15 : BoxCovered (17 / 32) (17 / 32) (1 / 64) := by
  apply boxCovered_leaf (17 / 32) (17 / 32) (1 / 64) (635257 / 1000000) (166409 / 400000) (104007 / 1000000) (52341 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_16 : BoxCovered (35 / 64) (17 / 32) (1 / 64) := by
  apply boxCovered_leaf (35 / 64) (17 / 32) (1 / 64) (635257 / 1000000) (166409 / 400000) (44191 / 500000) (52341 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_17 : BoxCovered (17 / 32) (35 / 64) (1 / 64) := by
  apply boxCovered_leaf (17 / 32) (35 / 64) (1 / 64) (1257689 / 2000000) (687067 / 1000000) (195189 / 2000000) (4381 / 31250) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_18 : BoxCovered (35 / 64) (35 / 64) (1 / 64) := by
  apply boxCovered_leaf (35 / 64) (35 / 64) (1 / 64) (635257 / 1000000) (166409 / 400000) (44191 / 500000) (58591 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_19 : BoxCovered (17 / 32) (17 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ3_15 using 1 <;> norm_num
  · convert coverQ3_16 using 1 <;> norm_num
  · convert coverQ3_17 using 1 <;> norm_num
  · convert coverQ3_18 using 1 <;> norm_num

theorem coverQ3_20 : BoxCovered (1 / 2) (1 / 2) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ3_4 using 1 <;> norm_num
  · convert coverQ3_5 using 1 <;> norm_num
  · convert coverQ3_14 using 1 <;> norm_num
  · convert coverQ3_19 using 1 <;> norm_num

theorem coverQ3_21 : BoxCovered (9 / 16) (1 / 2) (1 / 16) := by
  apply boxCovered_leaf (9 / 16) (1 / 2) (1 / 16) (635257 / 1000000) (166409 / 400000) (72757 / 1000000) (58591 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_22 : BoxCovered (1 / 2) (9 / 16) (1 / 32) := by
  apply boxCovered_leaf (1 / 2) (9 / 16) (1 / 32) (364743 / 1000000) (233591 / 400000) (166507 / 1000000) (8591 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_23 : BoxCovered (17 / 32) (9 / 16) (1 / 32) := by
  apply boxCovered_leaf (17 / 32) (9 / 16) (1 / 32) (1257689 / 2000000) (687067 / 1000000) (195189 / 2000000) (124567 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_24 : BoxCovered (1 / 2) (19 / 32) (1 / 32) := by
  apply boxCovered_leaf (1 / 2) (19 / 32) (1 / 32) (364743 / 1000000) (233591 / 400000) (166507 / 1000000) (16409 / 400000) ⟨9, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_25 : BoxCovered (17 / 32) (19 / 32) (1 / 32) := by
  apply boxCovered_leaf (17 / 32) (19 / 32) (1 / 32) (1257689 / 2000000) (687067 / 1000000) (195189 / 2000000) (93317 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_26 : BoxCovered (1 / 2) (9 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ3_22 using 1 <;> norm_num
  · convert coverQ3_23 using 1 <;> norm_num
  · convert coverQ3_24 using 1 <;> norm_num
  · convert coverQ3_25 using 1 <;> norm_num

theorem coverQ3_27 : BoxCovered (9 / 16) (9 / 16) (1 / 16) := by
  apply boxCovered_leaf (9 / 16) (9 / 16) (1 / 16) (1257689 / 2000000) (687067 / 1000000) (132689 / 2000000) (124567 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_28 : BoxCovered (1 / 2) (1 / 2) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ3_20 using 1 <;> norm_num
  · convert coverQ3_21 using 1 <;> norm_num
  · convert coverQ3_26 using 1 <;> norm_num
  · convert coverQ3_27 using 1 <;> norm_num

theorem coverQ3_29 : BoxCovered (5 / 8) (1 / 2) (1 / 16) := by
  apply boxCovered_leaf (5 / 8) (1 / 2) (1 / 16) (635257 / 1000000) (166409 / 400000) (52243 / 1000000) (58591 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_30 : BoxCovered (11 / 16) (1 / 2) (1 / 32) := by
  apply boxCovered_leaf (11 / 16) (1 / 2) (1 / 32) (635257 / 1000000) (166409 / 400000) (83493 / 1000000) (46091 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_31 : BoxCovered (23 / 32) (1 / 2) (1 / 32) := by
  apply boxCovered_leaf (23 / 32) (1 / 2) (1 / 32) (635257 / 1000000) (166409 / 400000) (114743 / 1000000) (46091 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_32 : BoxCovered (11 / 16) (17 / 32) (1 / 32) := by
  apply boxCovered_leaf (11 / 16) (17 / 32) (1 / 32) (635257 / 1000000) (166409 / 400000) (83493 / 1000000) (58591 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_33 : BoxCovered (23 / 32) (17 / 32) (1 / 64) := by
  apply boxCovered_leaf (23 / 32) (17 / 32) (1 / 64) (635257 / 1000000) (166409 / 400000) (49559 / 500000) (52341 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_34 : BoxCovered (47 / 64) (17 / 32) (1 / 128) := by
  apply boxCovered_leaf (47 / 64) (17 / 32) (1 / 128) (635257 / 1000000) (166409 / 400000) (213861 / 2000000) (769 / 6250) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_35 : BoxCovered (95 / 128) (17 / 32) (1 / 128) := by
  apply boxCovered_leaf (95 / 128) (17 / 32) (1 / 128) (635257 / 1000000) (166409 / 400000) (114743 / 1000000) (769 / 6250) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_36 : BoxCovered (47 / 64) (69 / 128) (1 / 128) := by
  apply boxCovered_leaf (47 / 64) (69 / 128) (1 / 128) (635257 / 1000000) (166409 / 400000) (213861 / 2000000) (52341 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_37 : BoxCovered (95 / 128) (69 / 128) (1 / 128) := by
  apply boxCovered_leaf (95 / 128) (69 / 128) (1 / 128) (1793819 / 2000000) (599621 / 1000000) (77361 / 500000) (121117 / 2000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_38 : BoxCovered (47 / 64) (17 / 32) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ3_34 using 1 <;> norm_num
  · convert coverQ3_35 using 1 <;> norm_num
  · convert coverQ3_36 using 1 <;> norm_num
  · convert coverQ3_37 using 1 <;> norm_num

theorem coverQ3_39 : BoxCovered (23 / 32) (35 / 64) (1 / 128) := by
  apply boxCovered_leaf (23 / 32) (35 / 64) (1 / 128) (635257 / 1000000) (166409 / 400000) (182611 / 2000000) (27733 / 200000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_40 : BoxCovered (93 / 128) (35 / 64) (1 / 128) := by
  apply boxCovered_leaf (93 / 128) (35 / 64) (1 / 128) (635257 / 1000000) (166409 / 400000) (49559 / 500000) (27733 / 200000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_41 : BoxCovered (23 / 32) (71 / 128) (1 / 128) := by
  apply boxCovered_leaf (23 / 32) (71 / 128) (1 / 128) (635257 / 1000000) (166409 / 400000) (182611 / 2000000) (58591 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_42 : BoxCovered (93 / 128) (71 / 128) (1 / 128) := by
  apply boxCovered_leaf (93 / 128) (71 / 128) (1 / 128) (1257689 / 2000000) (687067 / 1000000) (211061 / 2000000) (264759 / 2000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_43 : BoxCovered (23 / 32) (35 / 64) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ3_39 using 1 <;> norm_num
  · convert coverQ3_40 using 1 <;> norm_num
  · convert coverQ3_41 using 1 <;> norm_num
  · convert coverQ3_42 using 1 <;> norm_num

theorem coverQ3_44 : BoxCovered (47 / 64) (35 / 64) (1 / 64) := by
  apply boxCovered_leaf (47 / 64) (35 / 64) (1 / 64) (1793819 / 2000000) (599621 / 1000000) (325069 / 2000000) (26373 / 500000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_45 : BoxCovered (23 / 32) (17 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ3_33 using 1 <;> norm_num
  · convert coverQ3_38 using 1 <;> norm_num
  · convert coverQ3_43 using 1 <;> norm_num
  · convert coverQ3_44 using 1 <;> norm_num

theorem coverQ3_46 : BoxCovered (11 / 16) (1 / 2) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ3_30 using 1 <;> norm_num
  · convert coverQ3_31 using 1 <;> norm_num
  · convert coverQ3_32 using 1 <;> norm_num
  · convert coverQ3_45 using 1 <;> norm_num

theorem coverQ3_47 : BoxCovered (5 / 8) (9 / 16) (1 / 16) := by
  apply boxCovered_leaf (5 / 8) (9 / 16) (1 / 16) (1257689 / 2000000) (687067 / 1000000) (117311 / 2000000) (124567 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_48 : BoxCovered (11 / 16) (9 / 16) (1 / 32) := by
  apply boxCovered_leaf (11 / 16) (9 / 16) (1 / 32) (1257689 / 2000000) (687067 / 1000000) (179811 / 2000000) (124567 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_49 : BoxCovered (23 / 32) (9 / 16) (1 / 64) := by
  apply boxCovered_leaf (23 / 32) (9 / 16) (1 / 64) (1257689 / 2000000) (687067 / 1000000) (211061 / 2000000) (124567 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_50 : BoxCovered (47 / 64) (9 / 16) (1 / 64) := by
  apply boxCovered_leaf (47 / 64) (9 / 16) (1 / 64) (1793819 / 2000000) (599621 / 1000000) (325069 / 2000000) (37121 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_51 : BoxCovered (23 / 32) (37 / 64) (1 / 64) := by
  apply boxCovered_leaf (23 / 32) (37 / 64) (1 / 64) (1257689 / 2000000) (687067 / 1000000) (211061 / 2000000) (54471 / 500000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_52 : BoxCovered (47 / 64) (37 / 64) (1 / 64) := by
  apply boxCovered_leaf (47 / 64) (37 / 64) (1 / 64) (1257689 / 2000000) (687067 / 1000000) (242311 / 2000000) (54471 / 500000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_53 : BoxCovered (23 / 32) (9 / 16) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ3_49 using 1 <;> norm_num
  · convert coverQ3_50 using 1 <;> norm_num
  · convert coverQ3_51 using 1 <;> norm_num
  · convert coverQ3_52 using 1 <;> norm_num

theorem coverQ3_54 : BoxCovered (11 / 16) (19 / 32) (1 / 32) := by
  apply boxCovered_leaf (11 / 16) (19 / 32) (1 / 32) (1257689 / 2000000) (687067 / 1000000) (179811 / 2000000) (93317 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_55 : BoxCovered (23 / 32) (19 / 32) (1 / 32) := by
  apply boxCovered_leaf (23 / 32) (19 / 32) (1 / 32) (1257689 / 2000000) (687067 / 1000000) (242311 / 2000000) (93317 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_56 : BoxCovered (11 / 16) (9 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ3_48 using 1 <;> norm_num
  · convert coverQ3_53 using 1 <;> norm_num
  · convert coverQ3_54 using 1 <;> norm_num
  · convert coverQ3_55 using 1 <;> norm_num

theorem coverQ3_57 : BoxCovered (5 / 8) (1 / 2) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ3_29 using 1 <;> norm_num
  · convert coverQ3_46 using 1 <;> norm_num
  · convert coverQ3_47 using 1 <;> norm_num
  · convert coverQ3_56 using 1 <;> norm_num

theorem coverQ3_58 : BoxCovered (1 / 2) (5 / 8) (1 / 8) := by
  apply boxCovered_leaf (1 / 2) (5 / 8) (1 / 8) (1257689 / 2000000) (687067 / 1000000) (257689 / 2000000) (62933 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_59 : BoxCovered (5 / 8) (5 / 8) (1 / 8) := by
  apply boxCovered_leaf (5 / 8) (5 / 8) (1 / 8) (1257689 / 2000000) (687067 / 1000000) (242311 / 2000000) (62933 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_60 : BoxCovered (1 / 2) (1 / 2) (1 / 4) := by
  apply boxCovered_split
  · convert coverQ3_28 using 1 <;> norm_num
  · convert coverQ3_57 using 1 <;> norm_num
  · convert coverQ3_58 using 1 <;> norm_num
  · convert coverQ3_59 using 1 <;> norm_num

theorem coverQ3_61 : BoxCovered (3 / 4) (1 / 2) (1 / 64) := by
  apply boxCovered_leaf (3 / 4) (1 / 2) (1 / 64) (635257 / 1000000) (166409 / 400000) (2037 / 15625) (39841 / 400000) ⟨6, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_62 : BoxCovered (49 / 64) (1 / 2) (1 / 64) := by
  apply boxCovered_leaf (49 / 64) (1 / 2) (1 / 64) (1793819 / 2000000) (599621 / 1000000) (262569 / 2000000) (99621 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_63 : BoxCovered (3 / 4) (33 / 64) (1 / 64) := by
  apply boxCovered_leaf (3 / 4) (33 / 64) (1 / 64) (1793819 / 2000000) (599621 / 1000000) (293819 / 2000000) (20999 / 250000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_64 : BoxCovered (49 / 64) (33 / 64) (1 / 64) := by
  apply boxCovered_leaf (49 / 64) (33 / 64) (1 / 64) (1793819 / 2000000) (599621 / 1000000) (262569 / 2000000) (20999 / 250000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_65 : BoxCovered (3 / 4) (1 / 2) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ3_61 using 1 <;> norm_num
  · convert coverQ3_62 using 1 <;> norm_num
  · convert coverQ3_63 using 1 <;> norm_num
  · convert coverQ3_64 using 1 <;> norm_num

theorem coverQ3_66 : BoxCovered (25 / 32) (1 / 2) (1 / 32) := by
  apply boxCovered_leaf (25 / 32) (1 / 2) (1 / 32) (1793819 / 2000000) (599621 / 1000000) (231319 / 2000000) (99621 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_67 : BoxCovered (3 / 4) (17 / 32) (1 / 32) := by
  apply boxCovered_leaf (3 / 4) (17 / 32) (1 / 32) (1793819 / 2000000) (599621 / 1000000) (293819 / 2000000) (68371 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_68 : BoxCovered (25 / 32) (17 / 32) (1 / 32) := by
  apply boxCovered_leaf (25 / 32) (17 / 32) (1 / 32) (1793819 / 2000000) (599621 / 1000000) (231319 / 2000000) (68371 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_69 : BoxCovered (3 / 4) (1 / 2) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ3_65 using 1 <;> norm_num
  · convert coverQ3_66 using 1 <;> norm_num
  · convert coverQ3_67 using 1 <;> norm_num
  · convert coverQ3_68 using 1 <;> norm_num

theorem coverQ3_70 : BoxCovered (13 / 16) (1 / 2) (1 / 16) := by
  apply boxCovered_leaf (13 / 16) (1 / 2) (1 / 16) (1793819 / 2000000) (599621 / 1000000) (168819 / 2000000) (99621 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_71 : BoxCovered (3 / 4) (9 / 16) (1 / 16) := by
  apply boxCovered_leaf (3 / 4) (9 / 16) (1 / 16) (1793819 / 2000000) (599621 / 1000000) (293819 / 2000000) (37121 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_72 : BoxCovered (13 / 16) (9 / 16) (1 / 16) := by
  apply boxCovered_leaf (13 / 16) (9 / 16) (1 / 16) (1793819 / 2000000) (599621 / 1000000) (168819 / 2000000) (37121 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_73 : BoxCovered (3 / 4) (1 / 2) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ3_69 using 1 <;> norm_num
  · convert coverQ3_70 using 1 <;> norm_num
  · convert coverQ3_71 using 1 <;> norm_num
  · convert coverQ3_72 using 1 <;> norm_num

theorem coverQ3_74 : BoxCovered (7 / 8) (1 / 2) (1 / 8) := by
  apply boxCovered_leaf (7 / 8) (1 / 2) (1 / 8) (1793819 / 2000000) (599621 / 1000000) (206181 / 2000000) (99621 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_75 : BoxCovered (3 / 4) (5 / 8) (1 / 16) := by
  apply boxCovered_leaf (3 / 4) (5 / 8) (1 / 16) (1793819 / 2000000) (599621 / 1000000) (293819 / 2000000) (87879 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_76 : BoxCovered (13 / 16) (5 / 8) (1 / 16) := by
  apply boxCovered_leaf (13 / 16) (5 / 8) (1 / 16) (1793819 / 2000000) (599621 / 1000000) (168819 / 2000000) (87879 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_77 : BoxCovered (3 / 4) (11 / 16) (1 / 32) := by
  apply boxCovered_leaf (3 / 4) (11 / 16) (1 / 32) (1257689 / 2000000) (687067 / 1000000) (304811 / 2000000) (31683 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_78 : BoxCovered (25 / 32) (11 / 16) (1 / 32) := by
  apply boxCovered_leaf (25 / 32) (11 / 16) (1 / 32) (1793819 / 2000000) (599621 / 1000000) (231319 / 2000000) (119129 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_79 : BoxCovered (3 / 4) (23 / 32) (1 / 32) := by
  apply boxCovered_leaf (3 / 4) (23 / 32) (1 / 32) (1257689 / 2000000) (687067 / 1000000) (304811 / 2000000) (62933 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_80 : BoxCovered (25 / 32) (23 / 32) (1 / 128) := by
  apply boxCovered_leaf (25 / 32) (23 / 32) (1 / 128) (1257689 / 2000000) (687067 / 1000000) (80109 / 500000) (78991 / 2000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_81 : BoxCovered (101 / 128) (23 / 32) (1 / 128) := by
  apply boxCovered_leaf (101 / 128) (23 / 32) (1 / 128) (1257689 / 2000000) (687067 / 1000000) (336061 / 2000000) (78991 / 2000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_82 : BoxCovered (25 / 32) (93 / 128) (1 / 128) := by
  apply boxCovered_leaf (25 / 32) (93 / 128) (1 / 128) (1257689 / 2000000) (687067 / 1000000) (80109 / 500000) (11827 / 250000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_83 : BoxCovered (101 / 128) (93 / 128) (1 / 128) := by
  apply boxCovered_leaf (101 / 128) (93 / 128) (1 / 128) (1793819 / 2000000) (599621 / 1000000) (107847 / 1000000) (67377 / 500000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_84 : BoxCovered (25 / 32) (23 / 32) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ3_80 using 1 <;> norm_num
  · convert coverQ3_81 using 1 <;> norm_num
  · convert coverQ3_82 using 1 <;> norm_num
  · convert coverQ3_83 using 1 <;> norm_num

theorem coverQ3_85 : BoxCovered (51 / 64) (23 / 32) (1 / 64) := by
  apply boxCovered_leaf (51 / 64) (23 / 32) (1 / 64) (1793819 / 2000000) (599621 / 1000000) (200069 / 2000000) (67377 / 500000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_86 : BoxCovered (25 / 32) (47 / 64) (1 / 128) := by
  apply boxCovered_leaf (25 / 32) (47 / 64) (1 / 128) (1257689 / 2000000) (687067 / 1000000) (80109 / 500000) (110241 / 2000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_87 : BoxCovered (101 / 128) (47 / 64) (1 / 128) := by
  apply boxCovered_leaf (101 / 128) (47 / 64) (1 / 128) (895009 / 1000000) (1734163 / 2000000) (211893 / 2000000) (265413 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_88 : BoxCovered (25 / 32) (95 / 128) (1 / 128) := by
  apply boxCovered_leaf (25 / 32) (95 / 128) (1 / 128) (1257689 / 2000000) (687067 / 1000000) (80109 / 500000) (62933 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_89 : BoxCovered (101 / 128) (95 / 128) (1 / 128) := by
  apply boxCovered_leaf (101 / 128) (95 / 128) (1 / 128) (895009 / 1000000) (1734163 / 2000000) (211893 / 2000000) (62447 / 500000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_90 : BoxCovered (25 / 32) (47 / 64) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ3_86 using 1 <;> norm_num
  · convert coverQ3_87 using 1 <;> norm_num
  · convert coverQ3_88 using 1 <;> norm_num
  · convert coverQ3_89 using 1 <;> norm_num

theorem coverQ3_91 : BoxCovered (51 / 64) (47 / 64) (1 / 64) := by
  apply boxCovered_leaf (51 / 64) (47 / 64) (1 / 64) (895009 / 1000000) (1734163 / 2000000) (49067 / 500000) (265413 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_92 : BoxCovered (25 / 32) (23 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ3_84 using 1 <;> norm_num
  · convert coverQ3_85 using 1 <;> norm_num
  · convert coverQ3_90 using 1 <;> norm_num
  · convert coverQ3_91 using 1 <;> norm_num

theorem coverQ3_93 : BoxCovered (3 / 4) (11 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ3_77 using 1 <;> norm_num
  · convert coverQ3_78 using 1 <;> norm_num
  · convert coverQ3_79 using 1 <;> norm_num
  · convert coverQ3_92 using 1 <;> norm_num

theorem coverQ3_94 : BoxCovered (13 / 16) (11 / 16) (1 / 16) := by
  apply boxCovered_leaf (13 / 16) (11 / 16) (1 / 16) (1793819 / 2000000) (599621 / 1000000) (168819 / 2000000) (150379 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_95 : BoxCovered (3 / 4) (5 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ3_75 using 1 <;> norm_num
  · convert coverQ3_76 using 1 <;> norm_num
  · convert coverQ3_93 using 1 <;> norm_num
  · convert coverQ3_94 using 1 <;> norm_num

theorem coverQ3_96 : BoxCovered (7 / 8) (5 / 8) (1 / 16) := by
  apply boxCovered_leaf (7 / 8) (5 / 8) (1 / 16) (1793819 / 2000000) (599621 / 1000000) (81181 / 2000000) (87879 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_97 : BoxCovered (15 / 16) (5 / 8) (1 / 16) := by
  apply boxCovered_leaf (15 / 16) (5 / 8) (1 / 16) (1793819 / 2000000) (599621 / 1000000) (206181 / 2000000) (87879 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_98 : BoxCovered (7 / 8) (11 / 16) (1 / 16) := by
  apply boxCovered_leaf (7 / 8) (11 / 16) (1 / 16) (1793819 / 2000000) (599621 / 1000000) (81181 / 2000000) (150379 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_99 : BoxCovered (15 / 16) (11 / 16) (1 / 32) := by
  apply boxCovered_leaf (15 / 16) (11 / 16) (1 / 32) (1793819 / 2000000) (599621 / 1000000) (143681 / 2000000) (119129 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_100 : BoxCovered (31 / 32) (11 / 16) (1 / 32) := by
  apply boxCovered_leaf (31 / 32) (11 / 16) (1 / 32) (1793819 / 2000000) (599621 / 1000000) (206181 / 2000000) (119129 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_101 : BoxCovered (15 / 16) (23 / 32) (1 / 32) := by
  apply boxCovered_leaf (15 / 16) (23 / 32) (1 / 32) (1793819 / 2000000) (599621 / 1000000) (143681 / 2000000) (150379 / 1000000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_102 : BoxCovered (31 / 32) (23 / 32) (1 / 64) := by
  apply boxCovered_leaf (31 / 32) (23 / 32) (1 / 64) (1793819 / 2000000) (599621 / 1000000) (174931 / 2000000) (67377 / 500000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_103 : BoxCovered (63 / 64) (23 / 32) (1 / 64) := by
  apply boxCovered_leaf (63 / 64) (23 / 32) (1 / 64) (1793819 / 2000000) (599621 / 1000000) (206181 / 2000000) (67377 / 500000) ⟨11, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_104 : BoxCovered (31 / 32) (47 / 64) (1 / 64) := by
  apply boxCovered_leaf (31 / 32) (47 / 64) (1 / 64) (895009 / 1000000) (1734163 / 2000000) (44683 / 500000) (265413 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_105 : BoxCovered (63 / 64) (47 / 64) (1 / 64) := by
  apply boxCovered_leaf (63 / 64) (47 / 64) (1 / 64) (895009 / 1000000) (1734163 / 2000000) (104991 / 1000000) (265413 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_106 : BoxCovered (31 / 32) (23 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ3_102 using 1 <;> norm_num
  · convert coverQ3_103 using 1 <;> norm_num
  · convert coverQ3_104 using 1 <;> norm_num
  · convert coverQ3_105 using 1 <;> norm_num

theorem coverQ3_107 : BoxCovered (15 / 16) (11 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ3_99 using 1 <;> norm_num
  · convert coverQ3_100 using 1 <;> norm_num
  · convert coverQ3_101 using 1 <;> norm_num
  · convert coverQ3_106 using 1 <;> norm_num

theorem coverQ3_108 : BoxCovered (7 / 8) (5 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ3_96 using 1 <;> norm_num
  · convert coverQ3_97 using 1 <;> norm_num
  · convert coverQ3_98 using 1 <;> norm_num
  · convert coverQ3_107 using 1 <;> norm_num

theorem coverQ3_109 : BoxCovered (3 / 4) (1 / 2) (1 / 4) := by
  apply boxCovered_split
  · convert coverQ3_73 using 1 <;> norm_num
  · convert coverQ3_74 using 1 <;> norm_num
  · convert coverQ3_95 using 1 <;> norm_num
  · convert coverQ3_108 using 1 <;> norm_num

theorem coverQ3_110 : BoxCovered (1 / 2) (3 / 4) (1 / 32) := by
  apply boxCovered_leaf (1 / 2) (3 / 4) (1 / 32) (1257689 / 2000000) (687067 / 1000000) (257689 / 2000000) (94183 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_111 : BoxCovered (17 / 32) (3 / 4) (1 / 32) := by
  apply boxCovered_leaf (17 / 32) (3 / 4) (1 / 32) (1257689 / 2000000) (687067 / 1000000) (195189 / 2000000) (94183 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_112 : BoxCovered (1 / 2) (25 / 32) (1 / 64) := by
  apply boxCovered_leaf (1 / 2) (25 / 32) (1 / 64) (1257689 / 2000000) (687067 / 1000000) (257689 / 2000000) (6863 / 62500) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_113 : BoxCovered (33 / 64) (25 / 32) (1 / 64) := by
  apply boxCovered_leaf (33 / 64) (25 / 32) (1 / 64) (1257689 / 2000000) (687067 / 1000000) (226439 / 2000000) (6863 / 62500) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_114 : BoxCovered (1 / 2) (51 / 64) (1 / 64) := by
  apply boxCovered_leaf (1 / 2) (51 / 64) (1 / 64) (732757 / 2000000) (215311 / 250000) (298493 / 2000000) (64369 / 1000000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_115 : BoxCovered (33 / 64) (51 / 64) (1 / 64) := by
  apply boxCovered_leaf (33 / 64) (51 / 64) (1 / 64) (1257689 / 2000000) (687067 / 1000000) (226439 / 2000000) (125433 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_116 : BoxCovered (1 / 2) (25 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ3_112 using 1 <;> norm_num
  · convert coverQ3_113 using 1 <;> norm_num
  · convert coverQ3_114 using 1 <;> norm_num
  · convert coverQ3_115 using 1 <;> norm_num

theorem coverQ3_117 : BoxCovered (17 / 32) (25 / 32) (1 / 32) := by
  apply boxCovered_leaf (17 / 32) (25 / 32) (1 / 32) (1257689 / 2000000) (687067 / 1000000) (195189 / 2000000) (125433 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_118 : BoxCovered (1 / 2) (3 / 4) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ3_110 using 1 <;> norm_num
  · convert coverQ3_111 using 1 <;> norm_num
  · convert coverQ3_116 using 1 <;> norm_num
  · convert coverQ3_117 using 1 <;> norm_num

theorem coverQ3_119 : BoxCovered (9 / 16) (3 / 4) (1 / 16) := by
  apply boxCovered_leaf (9 / 16) (3 / 4) (1 / 16) (1257689 / 2000000) (687067 / 1000000) (132689 / 2000000) (125433 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_120 : BoxCovered (1 / 2) (13 / 16) (1 / 32) := by
  apply boxCovered_leaf (1 / 2) (13 / 16) (1 / 32) (732757 / 2000000) (215311 / 250000) (329743 / 2000000) (6093 / 125000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_121 : BoxCovered (17 / 32) (13 / 16) (1 / 32) := by
  apply boxCovered_leaf (17 / 32) (13 / 16) (1 / 32) (313399 / 500000) (954497 / 1000000) (23887 / 250000) (141997 / 1000000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_122 : BoxCovered (1 / 2) (27 / 32) (1 / 32) := by
  apply boxCovered_leaf (1 / 2) (27 / 32) (1 / 32) (732757 / 2000000) (215311 / 250000) (329743 / 2000000) (8747 / 500000) ⟨13, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_123 : BoxCovered (17 / 32) (27 / 32) (1 / 32) := by
  apply boxCovered_leaf (17 / 32) (27 / 32) (1 / 32) (313399 / 500000) (954497 / 1000000) (23887 / 250000) (110747 / 1000000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_124 : BoxCovered (1 / 2) (13 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ3_120 using 1 <;> norm_num
  · convert coverQ3_121 using 1 <;> norm_num
  · convert coverQ3_122 using 1 <;> norm_num
  · convert coverQ3_123 using 1 <;> norm_num

theorem coverQ3_125 : BoxCovered (9 / 16) (13 / 16) (1 / 16) := by
  apply boxCovered_leaf (9 / 16) (13 / 16) (1 / 16) (313399 / 500000) (954497 / 1000000) (32149 / 500000) (141997 / 1000000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_126 : BoxCovered (1 / 2) (3 / 4) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ3_118 using 1 <;> norm_num
  · convert coverQ3_119 using 1 <;> norm_num
  · convert coverQ3_124 using 1 <;> norm_num
  · convert coverQ3_125 using 1 <;> norm_num

theorem coverQ3_127 : BoxCovered (5 / 8) (3 / 4) (1 / 16) := by
  apply boxCovered_leaf (5 / 8) (3 / 4) (1 / 16) (1257689 / 2000000) (687067 / 1000000) (117311 / 2000000) (125433 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_128 : BoxCovered (11 / 16) (3 / 4) (1 / 32) := by
  apply boxCovered_leaf (11 / 16) (3 / 4) (1 / 32) (1257689 / 2000000) (687067 / 1000000) (179811 / 2000000) (94183 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_129 : BoxCovered (23 / 32) (3 / 4) (1 / 32) := by
  apply boxCovered_leaf (23 / 32) (3 / 4) (1 / 32) (1257689 / 2000000) (687067 / 1000000) (242311 / 2000000) (94183 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_130 : BoxCovered (11 / 16) (25 / 32) (1 / 32) := by
  apply boxCovered_leaf (11 / 16) (25 / 32) (1 / 32) (1257689 / 2000000) (687067 / 1000000) (179811 / 2000000) (125433 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_131 : BoxCovered (23 / 32) (25 / 32) (1 / 64) := by
  apply boxCovered_leaf (23 / 32) (25 / 32) (1 / 64) (1257689 / 2000000) (687067 / 1000000) (211061 / 2000000) (6863 / 62500) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_132 : BoxCovered (47 / 64) (25 / 32) (1 / 64) := by
  apply boxCovered_leaf (47 / 64) (25 / 32) (1 / 64) (1257689 / 2000000) (687067 / 1000000) (242311 / 2000000) (6863 / 62500) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_133 : BoxCovered (23 / 32) (51 / 64) (1 / 64) := by
  apply boxCovered_leaf (23 / 32) (51 / 64) (1 / 64) (1257689 / 2000000) (687067 / 1000000) (211061 / 2000000) (125433 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_134 : BoxCovered (47 / 64) (51 / 64) (1 / 128) := by
  apply boxCovered_leaf (47 / 64) (51 / 64) (1 / 128) (1257689 / 2000000) (687067 / 1000000) (113343 / 1000000) (235241 / 2000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_135 : BoxCovered (95 / 128) (51 / 64) (1 / 128) := by
  apply boxCovered_leaf (95 / 128) (51 / 64) (1 / 128) (1257689 / 2000000) (687067 / 1000000) (242311 / 2000000) (235241 / 2000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_136 : BoxCovered (47 / 64) (103 / 128) (1 / 128) := by
  apply boxCovered_leaf (47 / 64) (103 / 128) (1 / 128) (1257689 / 2000000) (687067 / 1000000) (113343 / 1000000) (125433 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_137 : BoxCovered (95 / 128) (103 / 128) (1 / 128) := by
  apply boxCovered_leaf (95 / 128) (103 / 128) (1 / 128) (895009 / 1000000) (1734163 / 2000000) (305643 / 2000000) (31197 / 500000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_138 : BoxCovered (47 / 64) (51 / 64) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ3_134 using 1 <;> norm_num
  · convert coverQ3_135 using 1 <;> norm_num
  · convert coverQ3_136 using 1 <;> norm_num
  · convert coverQ3_137 using 1 <;> norm_num

theorem coverQ3_139 : BoxCovered (23 / 32) (25 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ3_131 using 1 <;> norm_num
  · convert coverQ3_132 using 1 <;> norm_num
  · convert coverQ3_133 using 1 <;> norm_num
  · convert coverQ3_138 using 1 <;> norm_num

theorem coverQ3_140 : BoxCovered (11 / 16) (3 / 4) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ3_128 using 1 <;> norm_num
  · convert coverQ3_129 using 1 <;> norm_num
  · convert coverQ3_130 using 1 <;> norm_num
  · convert coverQ3_139 using 1 <;> norm_num

theorem coverQ3_141 : BoxCovered (5 / 8) (13 / 16) (1 / 16) := by
  apply boxCovered_leaf (5 / 8) (13 / 16) (1 / 16) (313399 / 500000) (954497 / 1000000) (30351 / 500000) (141997 / 1000000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_142 : BoxCovered (11 / 16) (13 / 16) (1 / 32) := by
  apply boxCovered_leaf (11 / 16) (13 / 16) (1 / 32) (313399 / 500000) (954497 / 1000000) (5747 / 62500) (141997 / 1000000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_143 : BoxCovered (23 / 32) (13 / 16) (1 / 128) := by
  apply boxCovered_leaf (23 / 32) (13 / 16) (1 / 128) (1257689 / 2000000) (687067 / 1000000) (48859 / 500000) (266491 / 2000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_144 : BoxCovered (93 / 128) (13 / 16) (1 / 128) := by
  apply boxCovered_leaf (93 / 128) (13 / 16) (1 / 128) (1257689 / 2000000) (687067 / 1000000) (211061 / 2000000) (266491 / 2000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_145 : BoxCovered (23 / 32) (105 / 128) (1 / 128) := by
  apply boxCovered_leaf (23 / 32) (105 / 128) (1 / 128) (1257689 / 2000000) (687067 / 1000000) (48859 / 500000) (70529 / 500000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_146 : BoxCovered (93 / 128) (105 / 128) (1 / 128) := by
  apply boxCovered_leaf (93 / 128) (105 / 128) (1 / 128) (313399 / 500000) (954497 / 1000000) (107577 / 1000000) (268369 / 2000000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_147 : BoxCovered (23 / 32) (13 / 16) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ3_143 using 1 <;> norm_num
  · convert coverQ3_144 using 1 <;> norm_num
  · convert coverQ3_145 using 1 <;> norm_num
  · convert coverQ3_146 using 1 <;> norm_num

theorem coverQ3_148 : BoxCovered (47 / 64) (13 / 16) (1 / 64) := by
  apply boxCovered_leaf (47 / 64) (13 / 16) (1 / 64) (895009 / 1000000) (1734163 / 2000000) (80317 / 500000) (109163 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_149 : BoxCovered (23 / 32) (53 / 64) (1 / 64) := by
  apply boxCovered_leaf (23 / 32) (53 / 64) (1 / 64) (313399 / 500000) (954497 / 1000000) (107577 / 1000000) (31593 / 250000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_150 : BoxCovered (47 / 64) (53 / 64) (1 / 64) := by
  apply boxCovered_leaf (47 / 64) (53 / 64) (1 / 64) (895009 / 1000000) (1734163 / 2000000) (80317 / 500000) (77913 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_151 : BoxCovered (23 / 32) (13 / 16) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ3_147 using 1 <;> norm_num
  · convert coverQ3_148 using 1 <;> norm_num
  · convert coverQ3_149 using 1 <;> norm_num
  · convert coverQ3_150 using 1 <;> norm_num

theorem coverQ3_152 : BoxCovered (11 / 16) (27 / 32) (1 / 32) := by
  apply boxCovered_leaf (11 / 16) (27 / 32) (1 / 32) (313399 / 500000) (954497 / 1000000) (5747 / 62500) (110747 / 1000000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_153 : BoxCovered (23 / 32) (27 / 32) (1 / 32) := by
  apply boxCovered_leaf (23 / 32) (27 / 32) (1 / 32) (313399 / 500000) (954497 / 1000000) (61601 / 500000) (110747 / 1000000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_154 : BoxCovered (11 / 16) (13 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ3_142 using 1 <;> norm_num
  · convert coverQ3_151 using 1 <;> norm_num
  · convert coverQ3_152 using 1 <;> norm_num
  · convert coverQ3_153 using 1 <;> norm_num

theorem coverQ3_155 : BoxCovered (5 / 8) (3 / 4) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ3_127 using 1 <;> norm_num
  · convert coverQ3_140 using 1 <;> norm_num
  · convert coverQ3_141 using 1 <;> norm_num
  · convert coverQ3_154 using 1 <;> norm_num

theorem coverQ3_156 : BoxCovered (1 / 2) (7 / 8) (1 / 8) := by
  apply boxCovered_leaf (1 / 2) (7 / 8) (1 / 8) (313399 / 500000) (954497 / 1000000) (63399 / 500000) (79497 / 1000000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_157 : BoxCovered (5 / 8) (7 / 8) (1 / 8) := by
  apply boxCovered_leaf (5 / 8) (7 / 8) (1 / 8) (313399 / 500000) (954497 / 1000000) (61601 / 500000) (79497 / 1000000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_158 : BoxCovered (1 / 2) (3 / 4) (1 / 4) := by
  apply boxCovered_split
  · convert coverQ3_126 using 1 <;> norm_num
  · convert coverQ3_155 using 1 <;> norm_num
  · convert coverQ3_156 using 1 <;> norm_num
  · convert coverQ3_157 using 1 <;> norm_num

theorem coverQ3_159 : BoxCovered (3 / 4) (3 / 4) (1 / 64) := by
  apply boxCovered_leaf (3 / 4) (3 / 4) (1 / 64) (1257689 / 2000000) (687067 / 1000000) (273561 / 2000000) (39279 / 500000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_160 : BoxCovered (49 / 64) (3 / 4) (1 / 64) := by
  apply boxCovered_leaf (49 / 64) (3 / 4) (1 / 64) (1257689 / 2000000) (687067 / 1000000) (304811 / 2000000) (39279 / 500000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_161 : BoxCovered (3 / 4) (49 / 64) (1 / 64) := by
  apply boxCovered_leaf (3 / 4) (49 / 64) (1 / 64) (1257689 / 2000000) (687067 / 1000000) (273561 / 2000000) (94183 / 1000000) ⟨10, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_162 : BoxCovered (49 / 64) (49 / 64) (1 / 64) := by
  apply boxCovered_leaf (49 / 64) (49 / 64) (1 / 64) (895009 / 1000000) (1734163 / 2000000) (16173 / 125000) (202913 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_163 : BoxCovered (3 / 4) (3 / 4) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ3_159 using 1 <;> norm_num
  · convert coverQ3_160 using 1 <;> norm_num
  · convert coverQ3_161 using 1 <;> norm_num
  · convert coverQ3_162 using 1 <;> norm_num

theorem coverQ3_164 : BoxCovered (25 / 32) (3 / 4) (1 / 32) := by
  apply boxCovered_leaf (25 / 32) (3 / 4) (1 / 32) (895009 / 1000000) (1734163 / 2000000) (113759 / 1000000) (234163 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_165 : BoxCovered (3 / 4) (25 / 32) (1 / 32) := by
  apply boxCovered_leaf (3 / 4) (25 / 32) (1 / 32) (895009 / 1000000) (1734163 / 2000000) (145009 / 1000000) (171663 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_166 : BoxCovered (25 / 32) (25 / 32) (1 / 32) := by
  apply boxCovered_leaf (25 / 32) (25 / 32) (1 / 32) (895009 / 1000000) (1734163 / 2000000) (113759 / 1000000) (171663 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_167 : BoxCovered (3 / 4) (3 / 4) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ3_163 using 1 <;> norm_num
  · convert coverQ3_164 using 1 <;> norm_num
  · convert coverQ3_165 using 1 <;> norm_num
  · convert coverQ3_166 using 1 <;> norm_num

theorem coverQ3_168 : BoxCovered (13 / 16) (3 / 4) (1 / 16) := by
  apply boxCovered_leaf (13 / 16) (3 / 4) (1 / 16) (895009 / 1000000) (1734163 / 2000000) (82509 / 1000000) (234163 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_169 : BoxCovered (3 / 4) (13 / 16) (1 / 16) := by
  apply boxCovered_leaf (3 / 4) (13 / 16) (1 / 16) (895009 / 1000000) (1734163 / 2000000) (145009 / 1000000) (109163 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_170 : BoxCovered (13 / 16) (13 / 16) (1 / 16) := by
  apply boxCovered_leaf (13 / 16) (13 / 16) (1 / 16) (895009 / 1000000) (1734163 / 2000000) (82509 / 1000000) (109163 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_171 : BoxCovered (3 / 4) (3 / 4) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ3_167 using 1 <;> norm_num
  · convert coverQ3_168 using 1 <;> norm_num
  · convert coverQ3_169 using 1 <;> norm_num
  · convert coverQ3_170 using 1 <;> norm_num

theorem coverQ3_172 : BoxCovered (7 / 8) (3 / 4) (1 / 8) := by
  apply boxCovered_leaf (7 / 8) (3 / 4) (1 / 8) (895009 / 1000000) (1734163 / 2000000) (104991 / 1000000) (234163 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_173 : BoxCovered (3 / 4) (7 / 8) (1 / 16) := by
  apply boxCovered_leaf (3 / 4) (7 / 8) (1 / 16) (895009 / 1000000) (1734163 / 2000000) (145009 / 1000000) (140837 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_174 : BoxCovered (13 / 16) (7 / 8) (1 / 16) := by
  apply boxCovered_leaf (13 / 16) (7 / 8) (1 / 16) (895009 / 1000000) (1734163 / 2000000) (82509 / 1000000) (140837 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_175 : BoxCovered (3 / 4) (15 / 16) (1 / 32) := by
  apply boxCovered_leaf (3 / 4) (15 / 16) (1 / 32) (313399 / 500000) (954497 / 1000000) (38613 / 250000) (16997 / 1000000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_176 : BoxCovered (25 / 32) (15 / 16) (1 / 32) := by
  apply boxCovered_leaf (25 / 32) (15 / 16) (1 / 32) (895009 / 1000000) (1734163 / 2000000) (113759 / 1000000) (203337 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_177 : BoxCovered (3 / 4) (31 / 32) (1 / 32) := by
  apply boxCovered_leaf (3 / 4) (31 / 32) (1 / 32) (313399 / 500000) (954497 / 1000000) (38613 / 250000) (45503 / 1000000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_178 : BoxCovered (25 / 32) (31 / 32) (1 / 64) := by
  apply boxCovered_leaf (25 / 32) (31 / 32) (1 / 64) (313399 / 500000) (954497 / 1000000) (170077 / 1000000) (14939 / 500000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_179 : BoxCovered (51 / 64) (31 / 32) (1 / 64) := by
  apply boxCovered_leaf (51 / 64) (31 / 32) (1 / 64) (895009 / 1000000) (1734163 / 2000000) (49067 / 500000) (234587 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_180 : BoxCovered (25 / 32) (63 / 64) (1 / 128) := by
  apply boxCovered_leaf (25 / 32) (63 / 64) (1 / 128) (313399 / 500000) (954497 / 1000000) (324529 / 2000000) (75381 / 2000000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_181 : BoxCovered (101 / 128) (63 / 64) (1 / 128) := by
  apply boxCovered_leaf (101 / 128) (63 / 64) (1 / 128) (895009 / 1000000) (1734163 / 2000000) (211893 / 2000000) (62553 / 500000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_182 : BoxCovered (25 / 32) (127 / 128) (1 / 128) := by
  apply boxCovered_leaf (25 / 32) (127 / 128) (1 / 128) (313399 / 500000) (954497 / 1000000) (324529 / 2000000) (45503 / 1000000) ⟨14, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_183 : BoxCovered (101 / 128) (127 / 128) (1 / 128) := by
  apply boxCovered_leaf (101 / 128) (127 / 128) (1 / 128) (895009 / 1000000) (1734163 / 2000000) (211893 / 2000000) (265837 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_184 : BoxCovered (25 / 32) (63 / 64) (1 / 64) := by
  apply boxCovered_split
  · convert coverQ3_180 using 1 <;> norm_num
  · convert coverQ3_181 using 1 <;> norm_num
  · convert coverQ3_182 using 1 <;> norm_num
  · convert coverQ3_183 using 1 <;> norm_num

theorem coverQ3_185 : BoxCovered (51 / 64) (63 / 64) (1 / 64) := by
  apply boxCovered_leaf (51 / 64) (63 / 64) (1 / 64) (895009 / 1000000) (1734163 / 2000000) (49067 / 500000) (265837 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_186 : BoxCovered (25 / 32) (31 / 32) (1 / 32) := by
  apply boxCovered_split
  · convert coverQ3_178 using 1 <;> norm_num
  · convert coverQ3_179 using 1 <;> norm_num
  · convert coverQ3_184 using 1 <;> norm_num
  · convert coverQ3_185 using 1 <;> norm_num

theorem coverQ3_187 : BoxCovered (3 / 4) (15 / 16) (1 / 16) := by
  apply boxCovered_split
  · convert coverQ3_175 using 1 <;> norm_num
  · convert coverQ3_176 using 1 <;> norm_num
  · convert coverQ3_177 using 1 <;> norm_num
  · convert coverQ3_186 using 1 <;> norm_num

theorem coverQ3_188 : BoxCovered (13 / 16) (15 / 16) (1 / 16) := by
  apply boxCovered_leaf (13 / 16) (15 / 16) (1 / 16) (895009 / 1000000) (1734163 / 2000000) (82509 / 1000000) (265837 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_189 : BoxCovered (3 / 4) (7 / 8) (1 / 8) := by
  apply boxCovered_split
  · convert coverQ3_173 using 1 <;> norm_num
  · convert coverQ3_174 using 1 <;> norm_num
  · convert coverQ3_187 using 1 <;> norm_num
  · convert coverQ3_188 using 1 <;> norm_num

theorem coverQ3_190 : BoxCovered (7 / 8) (7 / 8) (1 / 8) := by
  apply boxCovered_leaf (7 / 8) (7 / 8) (1 / 8) (895009 / 1000000) (1734163 / 2000000) (104991 / 1000000) (265837 / 2000000) ⟨15, by decide⟩ (by norm_num [coverSite]) <;> norm_num [coverRadius]

theorem coverQ3_191 : BoxCovered (3 / 4) (3 / 4) (1 / 4) := by
  apply boxCovered_split
  · convert coverQ3_171 using 1 <;> norm_num
  · convert coverQ3_172 using 1 <;> norm_num
  · convert coverQ3_189 using 1 <;> norm_num
  · convert coverQ3_190 using 1 <;> norm_num

theorem coverQ3_192 : BoxCovered (1 / 2) (1 / 2) (1 / 2) := by
  apply boxCovered_split
  · convert coverQ3_60 using 1 <;> norm_num
  · convert coverQ3_109 using 1 <;> norm_num
  · convert coverQ3_158 using 1 <;> norm_num
  · convert coverQ3_191 using 1 <;> norm_num

theorem coverQuadrant3 : BoxCovered (1 / 2) (1 / 2) (1/2) := coverQ3_192

end ElevenSquare
