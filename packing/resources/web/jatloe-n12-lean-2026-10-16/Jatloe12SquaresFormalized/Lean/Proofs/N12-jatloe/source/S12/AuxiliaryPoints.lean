import S12.LocalRejection
namespace S12
open S12Pilot

def fPoints : List (ℚ × ℚ) := [(1,(87/50)),(1,(113/50)),((8/5),1),((8/5),3),(2,(87/50)),(2,(113/50)),((12/5),1),((12/5),3),(3,(87/50)),(3,(113/50))]
def gPoints : List (ℚ × ℚ) := [(1,(8/5)),(1,(12/5)),((87/50),1),((87/50),2),((87/50),3),((113/50),1),((113/50),2),((113/50),3),(3,(8/5)),(3,(12/5))]
def auxPoints (kind : Fin 3) : List (ℚ × ℚ) :=
  match kind.val with
  | 0 => fPoints
  | 1 => gPoints
  | _ => fPoints ++ gPoints
end S12
