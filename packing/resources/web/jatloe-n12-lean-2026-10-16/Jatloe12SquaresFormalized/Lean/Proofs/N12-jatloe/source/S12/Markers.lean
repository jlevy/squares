import S12.Diagonal
import Mathlib.Data.Finset.Powerset
import Mathlib.Order.Fin.Basic
import Mathlib.Data.Fintype.Fin
import Mathlib.Tactic.FinCases

namespace S12
abbrev Marker := Fin 16
def marker (i : Marker) : ℚ × ℚ :=
  match i.val with
  | 0 => (1, (457 / 500))
  | 1 => ((457 / 500), 1)
  | 2 => (3, (457 / 500))
  | 3 => ((1543 / 500), 1)
  | 4 => (3, (1543 / 500))
  | 5 => ((1543 / 500), 3)
  | 6 => (1, (1543 / 500))
  | 7 => ((457 / 500), 3)
  | 8 => ((33 / 20), (33 / 20))
  | 9 => ((47 / 20), (33 / 20))
  | 10 => ((47 / 20), (47 / 20))
  | 11 => ((33 / 20), (47 / 20))
  | 12 => ((457 / 500), 2)
  | 13 => (2, (457 / 500))
  | 14 => ((1543 / 500), 2)
  | _ => (2, (1543 / 500))

def diameterLimit : ℚ := 2000000 / 982081
def distSq (p q : ℚ × ℚ) : ℚ := (p.1-q.1)^2+(p.2-q.2)^2
def DiameterOK (g : Finset Marker) : Prop :=
  g.Nonempty ∧ ∀ i ∈ g, ∀ j ∈ g, distSq (marker i) (marker j) < diameterLimit
instance (g : Finset Marker) : Decidable (DiameterOK g) := inferInstanceAs (Decidable (_ ∧ _))
def groupList : List (Finset Marker) := [{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {0, 1}, {0, 8}, {0, 12}, {0, 13}, {1, 8}, {1, 12}, {1, 13}, {2, 3}, {2, 9}, {2, 13}, {2, 14}, {3, 9}, {3, 13}, {3, 14}, {4, 5}, {4, 10}, {4, 14}, {4, 15}, {5, 10}, {5, 14}, {5, 15}, {6, 7}, {6, 11}, {6, 12}, {6, 15}, {7, 11}, {7, 12}, {7, 15}, {8, 9}, {8, 10}, {8, 11}, {8, 12}, {8, 13}, {9, 10}, {9, 11}, {9, 13}, {9, 14}, {10, 11}, {10, 14}, {10, 15}, {11, 12}, {11, 15}, {0, 1, 8}, {0, 1, 12}, {0, 1, 13}, {0, 8, 12}, {0, 8, 13}, {1, 8, 12}, {1, 8, 13}, {2, 3, 9}, {2, 3, 13}, {2, 3, 14}, {2, 9, 13}, {2, 9, 14}, {3, 9, 13}, {3, 9, 14}, {4, 5, 10}, {4, 5, 14}, {4, 5, 15}, {4, 10, 14}, {4, 10, 15}, {5, 10, 14}, {5, 10, 15}, {6, 7, 11}, {6, 7, 12}, {6, 7, 15}, {6, 11, 12}, {6, 11, 15}, {7, 11, 12}, {7, 11, 15}, {8, 9, 10}, {8, 9, 11}, {8, 9, 13}, {8, 10, 11}, {8, 11, 12}, {9, 10, 11}, {9, 10, 14}, {10, 11, 15}, {0, 1, 8, 12}, {0, 1, 8, 13}, {2, 3, 9, 13}, {2, 3, 9, 14}, {4, 5, 10, 14}, {4, 5, 10, 15}, {6, 7, 11, 12}, {6, 7, 11, 15}, {8, 9, 10, 11}]
def groupTable : Finset (Finset Marker) := groupList.toFinset
def markerCompatible (i j : Marker) : Prop :=
  distSq (marker i) (marker j) < diameterLimit
instance : DecidableRel markerCompatible := fun _ _ => inferInstanceAs (Decidable (_ < _))
end S12
