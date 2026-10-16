import Shard0768
import Shard0800
import Shard1408
import Shard1920
import Shard2240

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Aggregate
theorem block060 (k : ℕ) (hk : k < 64) : checkNat (3840 + k) = true := by
  interval_cases k
  · exact Shard0768.case3840
  · exact Shard1408.case3841
  · exact Shard1920.case3842
  · exact Shard2240.case3843
  · exact Shard0768.case3844
  · exact Shard1408.case3845
  · exact Shard1920.case3846
  · exact Shard2240.case3847
  · exact Shard0768.case3848
  · exact Shard1408.case3849
  · exact Shard1920.case3850
  · exact Shard2240.case3851
  · exact Shard0768.case3852
  · exact Shard1408.case3853
  · exact Shard1920.case3854
  · exact Shard2240.case3855
  · exact Shard0768.case3856
  · exact Shard1408.case3857
  · exact Shard1920.case3858
  · exact Shard2240.case3859
  · exact Shard0768.case3860
  · exact Shard1408.case3861
  · exact Shard1920.case3862
  · exact Shard2240.case3863
  · exact Shard0768.case3864
  · exact Shard1408.case3865
  · exact Shard1920.case3866
  · exact Shard2240.case3867
  · exact Shard0768.case3868
  · exact Shard1408.case3869
  · exact Shard1920.case3870
  · exact Shard2240.case3871
  · exact Shard0800.case3872
  · exact Shard1408.case3873
  · exact Shard1920.case3874
  · exact Shard2240.case3875
  · exact Shard0800.case3876
  · exact Shard1408.case3877
  · exact Shard1920.case3878
  · exact Shard2240.case3879
  · exact Shard0800.case3880
  · exact Shard1408.case3881
  · exact Shard1920.case3882
  · exact Shard2240.case3883
  · exact Shard0800.case3884
  · exact Shard1408.case3885
  · exact Shard1920.case3886
  · exact Shard2240.case3887
  · exact Shard0800.case3888
  · exact Shard1408.case3889
  · exact Shard1920.case3890
  · exact Shard2240.case3891
  · exact Shard0800.case3892
  · exact Shard1408.case3893
  · exact Shard1920.case3894
  · exact Shard2240.case3895
  · exact Shard0800.case3896
  · exact Shard1408.case3897
  · exact Shard1920.case3898
  · exact Shard2240.case3899
  · exact Shard0800.case3900
  · exact Shard1408.case3901
  · exact Shard1920.case3902
  · exact Shard2240.case3903
end Sq19.Endgame.Reduction.Aggregate
