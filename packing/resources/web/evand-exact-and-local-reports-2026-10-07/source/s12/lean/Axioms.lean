import Sqpack
#print axioms SquarePacking.wall_strip_le_three
#print axioms SquarePacking.wall_strip_le_three_of_packing
#print axioms SquarePacking.wall_strip_le_three_line
#print axioms SquarePacking.wall_strip_le_three_line_of_packing
#print axioms SquarePacking.packing_le_weight_regions_choice
#print axioms SquarePacking.sum_assign_eq_sum_counts
-- zero-margin checker primitives (Sqpack/ZeroMargin.lean, search/RUNG2.md)
#print axioms SquarePacking.sq_subset_box_iff
#print axioms SquarePacking.mem_sq_of_corners
#print axioms SquarePacking.lemmaA
#print axioms SquarePacking.le_maxQuad
#print axioms SquarePacking.maxQuad_mem
#print axioms SquarePacking.mem_sq_iff_gval
#print axioms SquarePacking.gsum_le_corners
#print axioms SquarePacking.gsum_le_gmax
#print axioms SquarePacking.gmax_mem
#print axioms SquarePacking.lemmaG
#print axioms SquarePacking.lemmaG'
#print axioms SquarePacking.lemmaH
#print axioms SquarePacking.lemmaG_box
#print axioms SquarePacking.lemmaH_box
#print axioms SquarePacking.gval_le_of_gmax_sub
#print axioms SquarePacking.chain_regions_cover
#print axioms SquarePacking.chain_region_down
#print axioms SquarePacking.widU_strictMonoOn
#print axioms SquarePacking.adm_widU_le
#print axioms SquarePacking.clip_bin_no_loss
#print axioms SquarePacking.xnR_spec
#print axioms SquarePacking.xnW_spec
#print axioms SquarePacking.xnM_spec
#print axioms SquarePacking.condPoly_eq_gval
#print axioms SquarePacking.condPoly_nonpos_iff
#print axioms SquarePacking.condPoly_rect
#print axioms SquarePacking.qeval4_eq_bern
#print axioms SquarePacking.bern_le_max
#print axioms SquarePacking.qeval4_le_maxBern
#print axioms SquarePacking.bern_endpoints
#print axioms SquarePacking.polyOk_bern
#print axioms SquarePacking.polyOk_quad
-- D4 reduction (Sqpack/D4.lean, search/S32_EXACT.md §7, §11.3(d))
#print axioms SquarePacking.sq_add_pi_div_two
#print axioms SquarePacking.mem_sq_reflX
#print axioms SquarePacking.mem_sq_swapXY
#print axioms SquarePacking.capt_reflX
#print axioms SquarePacking.capt_swapXY
#print axioms SquarePacking.d4_reduce
#print axioms SquarePacking.d4_reduction
#print axioms SquarePacking.d4_reduction_u
-- weighted covers as integer data (Sqpack/Cover.lean)
#print axioms SquarePacking.sum_filter_coverA
#print axioms SquarePacking.sum_coverA
#print axioms SquarePacking.D4Inv_cover
#print axioms SquarePacking.PTree.mem_sound
#print axioms SquarePacking.PTree.nodup_of_chainB
-- s(32) = 6 (Sqpack/S32.lean, notes/lean-s32.md)
#print axioms SquarePacking.not_packs_of_cover
#print axioms SquarePacking.packs_grid
#print axioms SquarePacking.S32Data.check_ok
#print axioms SquarePacking.S32Data.wsum_tree
#print axioms SquarePacking.S32Data.card_entries
#print axioms SquarePacking.S32Data.total_lt
#print axioms SquarePacking.S32Data.d4Inv
#print axioms SquarePacking.S32CheckerCover.region
#print axioms SquarePacking.s32_cover_all
#print axioms SquarePacking.s32_not_packs
#print axioms SquarePacking.s32_packs
#print axioms SquarePacking.s32_isLeast
#print axioms SquarePacking.s32_eq_six
#print axioms SquarePacking.s32_eq_six_of_checker
-- measures and mixed covers (Sqpack/MixedMeasure.lean, notes/lean-s21.md)
#print axioms SquarePacking.packing_le_measure
#print axioms SquarePacking.not_packs_of_measure
#print axioms SquarePacking.d4_reduction_measure
#print axioms SquarePacking.d4_reduction_measure_u
#print axioms SquarePacking.segMeasure_comm
#print axioms SquarePacking.segFrac_comm
#print axioms SquarePacking.MixedCover.measure_apply
#print axioms SquarePacking.MixedCover.measure_univ_le
#print axioms SquarePacking.MixedCover.measure_univ_eq
#print axioms SquarePacking.MixedCover.measure_preimage_invol
#print axioms SquarePacking.MixedCover.d4InvM
#print axioms SquarePacking.STree.mem_sound
-- s(21) = 5 (Sqpack/S21.lean, notes/lean-s21.md)
#print axioms SquarePacking.S21Data.check_ok
#print axioms SquarePacking.S21Data.pwsum_tree
#print axioms SquarePacking.S21Data.swsum_tree
#print axioms SquarePacking.S21Data.card_pentries
#print axioms SquarePacking.S21Data.card_sentries
#print axioms SquarePacking.S21Data.total_eq
#print axioms SquarePacking.S21Data.mu_box_lt
#print axioms SquarePacking.S21Data.mu_sq
#print axioms SquarePacking.S21Data.d4
#print axioms SquarePacking.S21CheckerCover.region
#print axioms SquarePacking.s21_cover_all
#print axioms SquarePacking.s21_not_packs
#print axioms SquarePacking.s21_packs
#print axioms SquarePacking.s21_isLeast
#print axioms SquarePacking.s21_eq_five
#print axioms SquarePacking.s21_eq_five_of_checker
-- box-tree verifier and the pilot rung of the lower-bound ladder (Sqpack/BoxTree.lean, lean/LADDER.md)
#print axioms SquarePacking.BoxTree.sound
#print axioms SquarePacking.BoxTree.le_minSide
#print axioms SquarePacking.s12_ge_35_9
#print axioms SquarePacking.s12_ge_3920_997
-- opt-in (not in the default target, ~30 core-minutes): `lake build Sqpack.S11Lower`, then
-- #print axioms SquarePacking.s11_ge_3040_797
-- opt-in (7.3 CPU-h, ≤ 31 GB per part): `lean/scripts/gen_data.sh S12H`, then
-- `lean/scripts/build_parts.sh S12H Sqpack.S12HLower 1`, then
-- #print axioms SquarePacking.s12_ge_15680_3951
-- zero-margin leaves (Sqpack/ZMTree.lean, lean/LADDER.md rung 2)
#print axioms SquarePacking.ZMTree.qOk_sound
#print axioms SquarePacking.ZMTree.bOk_sound
#print axioms SquarePacking.ZMTree.pairOk_sound
#print axioms SquarePacking.ZMTree.admK_sound
#print axioms SquarePacking.ZMTree.ptOkK_sound
#print axioms SquarePacking.ZMTree.E_cov
#print axioms SquarePacking.ZMTree.C_cov
#print axioms SquarePacking.ZMTree.Z_cov
#print axioms SquarePacking.ZMTree.sound
-- opt-in (not in the default target, ~33 core-minutes, ~9 min on 4 cores): `lake build
-- Sqpack.S13Lower`, then
-- #print axioms SquarePacking.s13_ge_4
-- #print axioms SquarePacking.s13_eq_4
-- mixed covers: CovM, piece leaves (Lemma S, Lemma T pair form, Lemma P), the mixed tree
-- (Sqpack/{CovM,SegParts,ZMTreeM}.lean, notes/lean-segments.md), and the toy end-to-end s(3) >= 2
#print axioms SquarePacking.ZMTreeM.le_minSide_mixed
#print axioms SquarePacking.ZMTreeM.parts_le_segMass
#print axioms SquarePacking.ZMTreeM.pair_capture
#print axioms SquarePacking.ZMTreeM.admAll_sound
#print axioms SquarePacking.ZMTreeM.pc_sound
#print axioms SquarePacking.ZMTreeM.ZM_cov
#print axioms SquarePacking.ZMTreeM.soundM
#print axioms SquarePacking.s3_ge_2
#print axioms SquarePacking.ZMTreeM.lblk_sound
#print axioms SquarePacking.ZMTreeM.pc_soundX
#print axioms SquarePacking.s3_ge_2_mixed
-- s(k^2 - 3) = k for all k >= 6, from the one finite hypothesis Valid7 (Sqpack/Bentz.lean, certificates/k2m3/)
#print axioms SquarePacking.Bentz.bentz_of_valid7
-- s(k^2 - 4) = k for all k >= 8, from the one finite hypothesis Valid9 (Sqpack/BentzFam.lean, Sqpack/Bentz4.lean)
#print axioms SquarePacking.BentzFam.fileCover_measure
#print axioms SquarePacking.BentzFam.mass_shift
#print axioms SquarePacking.BentzFam.famCover_total
#print axioms SquarePacking.BentzFam.minSide_eq
#print axioms SquarePacking.Bentz4.box9Cover_measure
#print axioms SquarePacking.Bentz4.famCover_total4
#print axioms SquarePacking.Bentz4.bentz4_of_valid9
-- Valid7 / Valid9 split: D4 reduction and Lemma Z (theta = 0) in Lean, only the tilted run's region left
-- (Sqpack/ValidSplit.lean, ValidSplit7.lean, ValidSplit9.lean, notes/lean-valid-split.md)
#print axioms SquarePacking.ValidSplit.valid_of_tilt_axis
#print axioms SquarePacking.ValidSplit.d4InvM_gridCover
#print axioms SquarePacking.ValidSplit.validAxis_gridCover
#print axioms SquarePacking.ValidSplit.famCover_measure_eq
#print axioms SquarePacking.ValidSplit.gridCover_fit
#print axioms SquarePacking.ValidSplit.d4InvM_packed
#print axioms SquarePacking.ValidSplit.validAxis_packed
#print axioms SquarePacking.Bentz.box7_grid
#print axioms SquarePacking.Bentz.d4_box7
#print axioms SquarePacking.Bentz.validAxis7
#print axioms SquarePacking.Bentz.valid7_of_tilt_axis
#print axioms SquarePacking.Bentz.valid7_of_tilt
#print axioms SquarePacking.Bentz.bentz_of_validTilt7
#print axioms SquarePacking.Bentz4.box9_grid
#print axioms SquarePacking.Bentz4.d4_box9
#print axioms SquarePacking.Bentz4.validAxis9
#print axioms SquarePacking.Bentz4.valid9_of_tilt_axis
#print axioms SquarePacking.Bentz4.valid9_of_tilt
#print axioms SquarePacking.Bentz4.bentz4_of_validTilt9
-- clique-family.md Lemma 2, the transversal threshold at a wall (Sqpack/AnchorLemma2.lean)
#print axioms SquarePacking.anchor_lemma2
#print axioms SquarePacking.anchor_lemma2_sharp
#print axioms SquarePacking.anchor_lemma2_iff
-- common specification (Sqpack/Spec.lean, namespace UnitSquarePacking) and the bridge from ours
-- (Sqpack/SpecBridge.lean); the headline restatements are in the opt-in Sqpack/SpecHeadline.lean
#print axioms UnitSquarePacking.unitSq_eq_setOf
#print axioms UnitSquarePacking.interior_unitSq
#print axioms UnitSquarePacking.packs_iff
#print axioms UnitSquarePacking.minSide_eq
#print axioms UnitSquarePacking.lower_of_le_minSide
#print axioms UnitSquarePacking.isLeast_of_le_minSide
#print axioms UnitSquarePacking.s12_lower_3920_997
#print axioms UnitSquarePacking.s32_isLeast_of_checker
-- bridge to google-deepmind/formal-conjectures' Packing (Sqpack/{FCSquarePacking,SpecFC}.lean)
#print axioms UnitSquarePacking.exists_frame
#print axioms UnitSquarePacking.frame_image
#print axioms UnitSquarePacking.packs_iff_nonempty_packing
#print axioms UnitSquarePacking.setOf_packs_eq
-- bridge to chelokot/square-packing-archive's IsMinimumSide (restated, Sqpack/SpecChelokot.lean)
#print axioms UnitSquarePacking.Chelokot.hasPacking_iff
#print axioms UnitSquarePacking.Chelokot.hasPacking_iff_packs
#print axioms UnitSquarePacking.Chelokot.isLowerBound_iff
#print axioms UnitSquarePacking.Chelokot.isMinimumSide_iff_isLeast
#print axioms UnitSquarePacking.Chelokot.isMinimumSide_iff_minSide_eq
#print axioms UnitSquarePacking.Chelokot.isMinimumSide_zero
-- attainment: s(n) is a minimum for n >= 1 (Sqpack/Attain.lean)
#print axioms SquarePacking.packs_mono
#print axioms SquarePacking.packs_nonempty
#print axioms SquarePacking.one_le_of_packs
#print axioms SquarePacking.bddBelow_packs
#print axioms SquarePacking.minSide_le
#print axioms SquarePacking.le_minSide_iff
#print axioms SquarePacking.isLeast_minSide
#print axioms SquarePacking.packs_minSide
#print axioms SquarePacking.packs_iff_minSide_le
#print axioms SquarePacking.minSide_eq_iff_isLeast
#print axioms SquarePacking.s3_eq_2
#print axioms SquarePacking.s3_isLeast
-- Lemma U (LEB) and Lemma K (CAP): Lebesgue-square leaf tests (Sqpack/LebMass.lean, notes/lean-leb-mass.md)
#print axioms SquarePacking.LebMass.validTilt_of_covT
#print axioms SquarePacking.LebMass.widU_le_whi
#print axioms SquarePacking.LebMass.volume_sq
#print axioms SquarePacking.LebMass.leb_sound
#print axioms SquarePacking.LebMass.gridCover_vol_le
#print axioms SquarePacking.LebMass.leb_sound_grid
#print axioms SquarePacking.LebMass.vol_hsl_le
#print axioms SquarePacking.LebMass.vol_below_le
#print axioms SquarePacking.LebMass.sq_below_le
#print axioms SquarePacking.LebMass.sq_left_le
#print axioms SquarePacking.LebMass.segMeasure_h
#print axioms SquarePacking.LebMass.segMeasure_v
#print axioms SquarePacking.LebMass.cone_BL
#print axioms SquarePacking.LebMass.cone_TL
#print axioms SquarePacking.LebMass.chordY
#print axioms SquarePacking.LebMass.chordX
#print axioms SquarePacking.LebMass.gridCover_ge
#print axioms SquarePacking.LebMass.cap_sound
-- smoke test: all 689 LEB and 374 CAP leaves of the k^2 - 3 run V3 (Sqpack/LebMass7.lean)
#print axioms SquarePacking.Bentz.leb7_ok
#print axioms SquarePacking.Bentz.cap7_ok
#print axioms SquarePacking.Bentz.leb7_cov
#print axioms SquarePacking.Bentz.cap7_cov
#print axioms UnitSquarePacking.packs_of_cert
#print axioms UnitSquarePacking.N5.packs_five
#print axioms UnitSquarePacking.EC.packs_exact
#print axioms UnitSquarePacking.EC.N5c.packs
#print axioms UnitSquarePacking.EC.N11c.packs
#print axioms UnitSquarePacking.LM.isLocalMin_of_rows
#print axioms UnitSquarePacking.LMC.isLocalMin_of_lcert
#print axioms UnitSquarePacking.EC.N11L.localmin
#print axioms UnitSquarePacking.Shadow.packs_of_shadow
-- band (wall-to-wall row) local minima for integer-side records (Sqpack/ChainLocalMin.lean)
#print axioms UnitSquarePacking.le_side_of_band
#print axioms UnitSquarePacking.isLocalMin_of_band
#print axioms UnitSquarePacking.isLocalMin_of_axisCert
#print axioms UnitSquarePacking.Chain.N8.localMin
