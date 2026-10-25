import S12.Cliques
import S12.MarkerAdjacency

/-! Cached suffix calculations for the original clique recursion.
Each equality unfolds exactly one recursion step and uses the already proved
suffix equality. All table entries are ordinary finite sets, checked in Lean's
kernel; the tables do not introduce axioms or native computation. -/
namespace S12

set_option Elab.async false

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def markerCliques16 : List (Finset Marker) :=
  [∅]

theorem markerCliques16_correct :
    cliques fastMarkerCompatible ([] : List Marker) = markerCliques16 := by
  rfl

def markerCliques15 : List (Finset Marker) :=
  [∅, {15}]

theorem markerCliques15_correct :
    cliques fastMarkerCompatible ([15] : List Marker) = markerCliques15 := by
  rw [cliques, markerCliques16_correct]
  decide

def markerCliques14 : List (Finset Marker) :=
  [∅, {15}, {14}]

theorem markerCliques14_correct :
    cliques fastMarkerCompatible ([14, 15] : List Marker) = markerCliques14 := by
  rw [cliques, markerCliques15_correct]
  decide

def markerCliques13 : List (Finset Marker) :=
  [∅, {15}, {14}, {13}]

theorem markerCliques13_correct :
    cliques fastMarkerCompatible ([13, 14, 15] : List Marker) = markerCliques13 := by
  rw [cliques, markerCliques14_correct]
  decide

def markerCliques12 : List (Finset Marker) :=
  [∅, {15}, {14}, {13}, {12}]

theorem markerCliques12_correct :
    cliques fastMarkerCompatible ([12, 13, 14, 15] : List Marker) = markerCliques12 := by
  rw [cliques, markerCliques13_correct]
  decide

def markerCliques11 : List (Finset Marker) :=
  [∅, {15}, {14}, {13}, {12}, {11}, {11, 15}, {11, 12}]

theorem markerCliques11_correct :
    cliques fastMarkerCompatible ([11, 12, 13, 14, 15] : List Marker) = markerCliques11 := by
  rw [cliques, markerCliques12_correct]
  decide

def markerCliques10 : List (Finset Marker) :=
  [∅, {15}, {14}, {13}, {12}, {11}, {11, 15}, {11, 12}, {10}, {10, 15}, {10, 14}, {10, 11},
   {10, 11, 15}]

theorem markerCliques10_correct :
    cliques fastMarkerCompatible ([10, 11, 12, 13, 14, 15] : List Marker) = markerCliques10 := by
  rw [cliques, markerCliques11_correct]
  decide

def markerCliques9 : List (Finset Marker) :=
  [∅, {15}, {14}, {13}, {12}, {11}, {11, 15}, {11, 12}, {10}, {10, 15}, {10, 14}, {10, 11},
   {10, 11, 15}, {9}, {9, 14}, {9, 13}, {9, 11}, {9, 10}, {9, 10, 14}, {9, 10, 11}]

theorem markerCliques9_correct :
    cliques fastMarkerCompatible ([9, 10, 11, 12, 13, 14, 15] : List Marker) = markerCliques9 := by
  rw [cliques, markerCliques10_correct]
  decide

def markerCliques8 : List (Finset Marker) :=
  [∅, {15}, {14}, {13}, {12}, {11}, {11, 15}, {11, 12}, {10}, {10, 15}, {10, 14}, {10, 11},
   {10, 11, 15}, {9}, {9, 14}, {9, 13}, {9, 11}, {9, 10}, {9, 10, 14}, {9, 10, 11}, {8}, {8, 13},
   {8, 12}, {8, 11}, {8, 11, 12}, {8, 10}, {8, 10, 11}, {8, 9}, {8, 9, 13}, {8, 9, 11},
   {8, 9, 10}, {8, 9, 10, 11}]

theorem markerCliques8_correct :
    cliques fastMarkerCompatible ([8, 9, 10, 11, 12, 13, 14, 15] : List Marker) = markerCliques8 := by
  rw [cliques, markerCliques9_correct]
  decide

def markerCliques7 : List (Finset Marker) :=
  [∅, {15}, {14}, {13}, {12}, {11}, {11, 15}, {11, 12}, {10}, {10, 15}, {10, 14}, {10, 11},
   {10, 11, 15}, {9}, {9, 14}, {9, 13}, {9, 11}, {9, 10}, {9, 10, 14}, {9, 10, 11}, {8}, {8, 13},
   {8, 12}, {8, 11}, {8, 11, 12}, {8, 10}, {8, 10, 11}, {8, 9}, {8, 9, 13}, {8, 9, 11},
   {8, 9, 10}, {8, 9, 10, 11}, {7}, {7, 15}, {7, 12}, {7, 11}, {7, 11, 15}, {7, 11, 12}]

theorem markerCliques7_correct :
    cliques fastMarkerCompatible ([7, 8, 9, 10, 11, 12, 13, 14, 15] : List Marker) = markerCliques7 := by
  rw [cliques, markerCliques8_correct]
  decide

def markerCliques6 : List (Finset Marker) :=
  [∅, {15}, {14}, {13}, {12}, {11}, {11, 15}, {11, 12}, {10}, {10, 15}, {10, 14}, {10, 11},
   {10, 11, 15}, {9}, {9, 14}, {9, 13}, {9, 11}, {9, 10}, {9, 10, 14}, {9, 10, 11}, {8}, {8, 13},
   {8, 12}, {8, 11}, {8, 11, 12}, {8, 10}, {8, 10, 11}, {8, 9}, {8, 9, 13}, {8, 9, 11},
   {8, 9, 10}, {8, 9, 10, 11}, {7}, {7, 15}, {7, 12}, {7, 11}, {7, 11, 15}, {7, 11, 12}, {6},
   {6, 15}, {6, 12}, {6, 11}, {6, 11, 15}, {6, 11, 12}, {6, 7}, {6, 7, 15}, {6, 7, 12},
   {6, 7, 11}, {6, 7, 11, 15}, {6, 7, 11, 12}]

theorem markerCliques6_correct :
    cliques fastMarkerCompatible ([6, 7, 8, 9, 10, 11, 12, 13, 14, 15] : List Marker) = markerCliques6 := by
  rw [cliques, markerCliques7_correct]
  decide

def markerCliques5 : List (Finset Marker) :=
  [∅, {15}, {14}, {13}, {12}, {11}, {11, 15}, {11, 12}, {10}, {10, 15}, {10, 14}, {10, 11},
   {10, 11, 15}, {9}, {9, 14}, {9, 13}, {9, 11}, {9, 10}, {9, 10, 14}, {9, 10, 11}, {8}, {8, 13},
   {8, 12}, {8, 11}, {8, 11, 12}, {8, 10}, {8, 10, 11}, {8, 9}, {8, 9, 13}, {8, 9, 11},
   {8, 9, 10}, {8, 9, 10, 11}, {7}, {7, 15}, {7, 12}, {7, 11}, {7, 11, 15}, {7, 11, 12}, {6},
   {6, 15}, {6, 12}, {6, 11}, {6, 11, 15}, {6, 11, 12}, {6, 7}, {6, 7, 15}, {6, 7, 12},
   {6, 7, 11}, {6, 7, 11, 15}, {6, 7, 11, 12}, {5}, {5, 15}, {5, 14}, {5, 10}, {5, 10, 15},
   {5, 10, 14}]

theorem markerCliques5_correct :
    cliques fastMarkerCompatible ([5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] : List Marker) = markerCliques5 := by
  rw [cliques, markerCliques6_correct]
  decide

def markerCliques4 : List (Finset Marker) :=
  [∅, {15}, {14}, {13}, {12}, {11}, {11, 15}, {11, 12}, {10}, {10, 15}, {10, 14}, {10, 11},
   {10, 11, 15}, {9}, {9, 14}, {9, 13}, {9, 11}, {9, 10}, {9, 10, 14}, {9, 10, 11}, {8}, {8, 13},
   {8, 12}, {8, 11}, {8, 11, 12}, {8, 10}, {8, 10, 11}, {8, 9}, {8, 9, 13}, {8, 9, 11},
   {8, 9, 10}, {8, 9, 10, 11}, {7}, {7, 15}, {7, 12}, {7, 11}, {7, 11, 15}, {7, 11, 12}, {6},
   {6, 15}, {6, 12}, {6, 11}, {6, 11, 15}, {6, 11, 12}, {6, 7}, {6, 7, 15}, {6, 7, 12},
   {6, 7, 11}, {6, 7, 11, 15}, {6, 7, 11, 12}, {5}, {5, 15}, {5, 14}, {5, 10}, {5, 10, 15},
   {5, 10, 14}, {4}, {4, 15}, {4, 14}, {4, 10}, {4, 10, 15}, {4, 10, 14}, {4, 5}, {4, 5, 15},
   {4, 5, 14}, {4, 5, 10}, {4, 5, 10, 15}, {4, 5, 10, 14}]

theorem markerCliques4_correct :
    cliques fastMarkerCompatible ([4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] : List Marker) = markerCliques4 := by
  rw [cliques, markerCliques5_correct]
  decide

def markerCliques3 : List (Finset Marker) :=
  [∅, {15}, {14}, {13}, {12}, {11}, {11, 15}, {11, 12}, {10}, {10, 15}, {10, 14}, {10, 11},
   {10, 11, 15}, {9}, {9, 14}, {9, 13}, {9, 11}, {9, 10}, {9, 10, 14}, {9, 10, 11}, {8}, {8, 13},
   {8, 12}, {8, 11}, {8, 11, 12}, {8, 10}, {8, 10, 11}, {8, 9}, {8, 9, 13}, {8, 9, 11},
   {8, 9, 10}, {8, 9, 10, 11}, {7}, {7, 15}, {7, 12}, {7, 11}, {7, 11, 15}, {7, 11, 12}, {6},
   {6, 15}, {6, 12}, {6, 11}, {6, 11, 15}, {6, 11, 12}, {6, 7}, {6, 7, 15}, {6, 7, 12},
   {6, 7, 11}, {6, 7, 11, 15}, {6, 7, 11, 12}, {5}, {5, 15}, {5, 14}, {5, 10}, {5, 10, 15},
   {5, 10, 14}, {4}, {4, 15}, {4, 14}, {4, 10}, {4, 10, 15}, {4, 10, 14}, {4, 5}, {4, 5, 15},
   {4, 5, 14}, {4, 5, 10}, {4, 5, 10, 15}, {4, 5, 10, 14}, {3}, {3, 14}, {3, 13}, {3, 9},
   {3, 9, 14}, {3, 9, 13}]

theorem markerCliques3_correct :
    cliques fastMarkerCompatible ([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] : List Marker) = markerCliques3 := by
  rw [cliques, markerCliques4_correct]
  decide

def markerCliques2 : List (Finset Marker) :=
  [∅, {15}, {14}, {13}, {12}, {11}, {11, 15}, {11, 12}, {10}, {10, 15}, {10, 14}, {10, 11},
   {10, 11, 15}, {9}, {9, 14}, {9, 13}, {9, 11}, {9, 10}, {9, 10, 14}, {9, 10, 11}, {8}, {8, 13},
   {8, 12}, {8, 11}, {8, 11, 12}, {8, 10}, {8, 10, 11}, {8, 9}, {8, 9, 13}, {8, 9, 11},
   {8, 9, 10}, {8, 9, 10, 11}, {7}, {7, 15}, {7, 12}, {7, 11}, {7, 11, 15}, {7, 11, 12}, {6},
   {6, 15}, {6, 12}, {6, 11}, {6, 11, 15}, {6, 11, 12}, {6, 7}, {6, 7, 15}, {6, 7, 12},
   {6, 7, 11}, {6, 7, 11, 15}, {6, 7, 11, 12}, {5}, {5, 15}, {5, 14}, {5, 10}, {5, 10, 15},
   {5, 10, 14}, {4}, {4, 15}, {4, 14}, {4, 10}, {4, 10, 15}, {4, 10, 14}, {4, 5}, {4, 5, 15},
   {4, 5, 14}, {4, 5, 10}, {4, 5, 10, 15}, {4, 5, 10, 14}, {3}, {3, 14}, {3, 13}, {3, 9},
   {3, 9, 14}, {3, 9, 13}, {2}, {2, 14}, {2, 13}, {2, 9}, {2, 9, 14}, {2, 9, 13}, {2, 3},
   {2, 3, 14}, {2, 3, 13}, {2, 3, 9}, {2, 3, 9, 14}, {2, 3, 9, 13}]

theorem markerCliques2_correct :
    cliques fastMarkerCompatible ([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] : List Marker) = markerCliques2 := by
  rw [cliques, markerCliques3_correct]
  decide

def markerCliques1 : List (Finset Marker) :=
  [∅, {15}, {14}, {13}, {12}, {11}, {11, 15}, {11, 12}, {10}, {10, 15}, {10, 14}, {10, 11},
   {10, 11, 15}, {9}, {9, 14}, {9, 13}, {9, 11}, {9, 10}, {9, 10, 14}, {9, 10, 11}, {8}, {8, 13},
   {8, 12}, {8, 11}, {8, 11, 12}, {8, 10}, {8, 10, 11}, {8, 9}, {8, 9, 13}, {8, 9, 11},
   {8, 9, 10}, {8, 9, 10, 11}, {7}, {7, 15}, {7, 12}, {7, 11}, {7, 11, 15}, {7, 11, 12}, {6},
   {6, 15}, {6, 12}, {6, 11}, {6, 11, 15}, {6, 11, 12}, {6, 7}, {6, 7, 15}, {6, 7, 12},
   {6, 7, 11}, {6, 7, 11, 15}, {6, 7, 11, 12}, {5}, {5, 15}, {5, 14}, {5, 10}, {5, 10, 15},
   {5, 10, 14}, {4}, {4, 15}, {4, 14}, {4, 10}, {4, 10, 15}, {4, 10, 14}, {4, 5}, {4, 5, 15},
   {4, 5, 14}, {4, 5, 10}, {4, 5, 10, 15}, {4, 5, 10, 14}, {3}, {3, 14}, {3, 13}, {3, 9},
   {3, 9, 14}, {3, 9, 13}, {2}, {2, 14}, {2, 13}, {2, 9}, {2, 9, 14}, {2, 9, 13}, {2, 3},
   {2, 3, 14}, {2, 3, 13}, {2, 3, 9}, {2, 3, 9, 14}, {2, 3, 9, 13}, {1}, {1, 13}, {1, 12},
   {1, 8}, {1, 8, 13}, {1, 8, 12}]

theorem markerCliques1_correct :
    cliques fastMarkerCompatible ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] : List Marker) = markerCliques1 := by
  rw [cliques, markerCliques2_correct]
  decide

def markerCliques0 : List (Finset Marker) :=
  [∅, {15}, {14}, {13}, {12}, {11}, {11, 15}, {11, 12}, {10}, {10, 15}, {10, 14}, {10, 11},
   {10, 11, 15}, {9}, {9, 14}, {9, 13}, {9, 11}, {9, 10}, {9, 10, 14}, {9, 10, 11}, {8}, {8, 13},
   {8, 12}, {8, 11}, {8, 11, 12}, {8, 10}, {8, 10, 11}, {8, 9}, {8, 9, 13}, {8, 9, 11},
   {8, 9, 10}, {8, 9, 10, 11}, {7}, {7, 15}, {7, 12}, {7, 11}, {7, 11, 15}, {7, 11, 12}, {6},
   {6, 15}, {6, 12}, {6, 11}, {6, 11, 15}, {6, 11, 12}, {6, 7}, {6, 7, 15}, {6, 7, 12},
   {6, 7, 11}, {6, 7, 11, 15}, {6, 7, 11, 12}, {5}, {5, 15}, {5, 14}, {5, 10}, {5, 10, 15},
   {5, 10, 14}, {4}, {4, 15}, {4, 14}, {4, 10}, {4, 10, 15}, {4, 10, 14}, {4, 5}, {4, 5, 15},
   {4, 5, 14}, {4, 5, 10}, {4, 5, 10, 15}, {4, 5, 10, 14}, {3}, {3, 14}, {3, 13}, {3, 9},
   {3, 9, 14}, {3, 9, 13}, {2}, {2, 14}, {2, 13}, {2, 9}, {2, 9, 14}, {2, 9, 13}, {2, 3},
   {2, 3, 14}, {2, 3, 13}, {2, 3, 9}, {2, 3, 9, 14}, {2, 3, 9, 13}, {1}, {1, 13}, {1, 12},
   {1, 8}, {1, 8, 13}, {1, 8, 12}, {0}, {0, 13}, {0, 12}, {0, 8}, {0, 8, 13}, {0, 8, 12}, {0, 1},
   {0, 1, 13}, {0, 1, 12}, {0, 1, 8}, {0, 1, 8, 13}, {0, 1, 8, 12}]

theorem markerCliques0_correct :
    cliques fastMarkerCompatible ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] : List Marker) = markerCliques0 := by
  rw [cliques, markerCliques1_correct]
  decide

end S12
