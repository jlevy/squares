import Sq19Lean.Endgame.ReductionAggregate
import Sq19Lean.Endgame.ReductionIndexed
import Block000
import Block001
import Block002
import Block003
import Block004
import Block005
import Block006
import Block007
import Block008
import Block009
import Block010
import Block011
import Block012
import Block013
import Block014
import Block015
import Block016
import Block017
import Block018
import Block019
import Block020
import Block021
import Block022
import Block023
import Block024
import Block025
import Block026
import Block027
import Block028
import Block029
import Block030
import Block031
import Block032
import Block033
import Block034
import Block035
import Block036
import Block037
import Block038
import Block039
import Block040
import Block041
import Block042
import Block043
import Block044
import Block045
import Block046
import Block047
import Block048
import Block049
import Block050
import Block051
import Block052
import Block053
import Block054
import Block055
import Block056
import Block057
import Block058
import Block059
import Block060
import Block061
import Block062
import Block063

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction
open Sq19.Milp
theorem all_index_checks : ∀ n < 4096, checkNat n = true := by
  apply indices_of_blocks (P := fun n => checkNat n = true) 64 64 (by decide)
  intro b hb r hr
  interval_cases b
  · exact Aggregate.block000 r hr
  · exact Aggregate.block001 r hr
  · exact Aggregate.block002 r hr
  · exact Aggregate.block003 r hr
  · exact Aggregate.block004 r hr
  · exact Aggregate.block005 r hr
  · exact Aggregate.block006 r hr
  · exact Aggregate.block007 r hr
  · exact Aggregate.block008 r hr
  · exact Aggregate.block009 r hr
  · exact Aggregate.block010 r hr
  · exact Aggregate.block011 r hr
  · exact Aggregate.block012 r hr
  · exact Aggregate.block013 r hr
  · exact Aggregate.block014 r hr
  · exact Aggregate.block015 r hr
  · exact Aggregate.block016 r hr
  · exact Aggregate.block017 r hr
  · exact Aggregate.block018 r hr
  · exact Aggregate.block019 r hr
  · exact Aggregate.block020 r hr
  · exact Aggregate.block021 r hr
  · exact Aggregate.block022 r hr
  · exact Aggregate.block023 r hr
  · exact Aggregate.block024 r hr
  · exact Aggregate.block025 r hr
  · exact Aggregate.block026 r hr
  · exact Aggregate.block027 r hr
  · exact Aggregate.block028 r hr
  · exact Aggregate.block029 r hr
  · exact Aggregate.block030 r hr
  · exact Aggregate.block031 r hr
  · exact Aggregate.block032 r hr
  · exact Aggregate.block033 r hr
  · exact Aggregate.block034 r hr
  · exact Aggregate.block035 r hr
  · exact Aggregate.block036 r hr
  · exact Aggregate.block037 r hr
  · exact Aggregate.block038 r hr
  · exact Aggregate.block039 r hr
  · exact Aggregate.block040 r hr
  · exact Aggregate.block041 r hr
  · exact Aggregate.block042 r hr
  · exact Aggregate.block043 r hr
  · exact Aggregate.block044 r hr
  · exact Aggregate.block045 r hr
  · exact Aggregate.block046 r hr
  · exact Aggregate.block047 r hr
  · exact Aggregate.block048 r hr
  · exact Aggregate.block049 r hr
  · exact Aggregate.block050 r hr
  · exact Aggregate.block051 r hr
  · exact Aggregate.block052 r hr
  · exact Aggregate.block053 r hr
  · exact Aggregate.block054 r hr
  · exact Aggregate.block055 r hr
  · exact Aggregate.block056 r hr
  · exact Aggregate.block057 r hr
  · exact Aggregate.block058 r hr
  · exact Aggregate.block059 r hr
  · exact Aggregate.block060 r hr
  · exact Aggregate.block061 r hr
  · exact Aggregate.block062 r hr
  · exact Aggregate.block063 r hr

theorem side19_le_of_hull {θ dx dy : ℕ → ℝ} {L : ℝ}
    (hg : Good Hull.prob θ dx dy L) : side19 ≤ L :=
  side19_le_of_hull_of_index_checks all_index_checks hg
end Sq19.Endgame.Reduction
#print axioms Sq19.Endgame.Reduction.all_index_checks
#print axioms Sq19.Endgame.Reduction.side19_le_of_hull
