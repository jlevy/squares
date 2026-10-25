import S12.Markers

/-!
Exact fast marker compatibility, factored through the three D4 orbits.
Only representatives 0, 8, and 12 need rational-distance normalization.
All original coordinates and compatibility definitions remain unchanged.
This is kernel-checkable source; no native evaluation is introduced.
-/

namespace S12

def rotateMarker (i : Marker) : Marker :=
  match i.val with
  | 0 => 3 | 1 => 2 | 2 => 5 | 3 => 4
  | 4 => 7 | 5 => 6 | 6 => 1 | 7 => 0
  | 8 => 9 | 9 => 10 | 10 => 11 | 11 => 8
  | 12 => 13 | 13 => 14 | 14 => 15 | _ => 12

def transposeMarker (i : Marker) : Marker :=
  match i.val with
  | 0 => 1 | 1 => 0 | 2 => 7 | 3 => 6
  | 4 => 5 | 5 => 4 | 6 => 3 | 7 => 2
  | 8 => 8 | 9 => 11 | 10 => 10 | 11 => 9
  | 12 => 13 | 13 => 12 | 14 => 15 | _ => 14

def rotateMarker2 (i : Marker) : Marker := rotateMarker (rotateMarker i)
def rotateMarker3 (i : Marker) : Marker := rotateMarker (rotateMarker2 i)
def transposeRotateMarker (i : Marker) : Marker := transposeMarker (rotateMarker i)
def transposeRotateMarker2 (i : Marker) : Marker := transposeMarker (rotateMarker2 i)
def transposeRotateMarker3 (i : Marker) : Marker := transposeMarker (rotateMarker3 i)

theorem marker_rotate (i : Marker) :
    marker (rotateMarker i) = (4 - (marker i).2, (marker i).1) := by
  fin_cases i <;> norm_num [rotateMarker, marker]

theorem marker_transpose (i : Marker) :
    marker (transposeMarker i) = ((marker i).2, (marker i).1) := by
  fin_cases i <;> norm_num [transposeMarker, marker]

theorem markerCompatible_rotate (i j : Marker) :
    markerCompatible (rotateMarker i) (rotateMarker j) ↔ markerCompatible i j := by
  unfold markerCompatible
  rw [marker_rotate, marker_rotate]
  rw [show distSq (4 - (marker i).2, (marker i).1)
      (4 - (marker j).2, (marker j).1) = distSq (marker i) (marker j) by
        unfold distSq
        ring]

theorem markerCompatible_transpose (i j : Marker) :
    markerCompatible (transposeMarker i) (transposeMarker j) ↔ markerCompatible i j := by
  unfold markerCompatible
  rw [marker_transpose, marker_transpose]
  rw [show distSq ((marker i).2, (marker i).1)
      ((marker j).2, (marker j).1) = distSq (marker i) (marker j) by
        unfold distSq
        ring]

theorem markerCompatible_rotate2 (i j : Marker) :
    markerCompatible (rotateMarker2 i) (rotateMarker2 j) ↔ markerCompatible i j :=
  (markerCompatible_rotate (rotateMarker i) (rotateMarker j)).trans
    (markerCompatible_rotate i j)

theorem markerCompatible_rotate3 (i j : Marker) :
    markerCompatible (rotateMarker3 i) (rotateMarker3 j) ↔ markerCompatible i j :=
  (markerCompatible_rotate (rotateMarker2 i) (rotateMarker2 j)).trans
    (markerCompatible_rotate2 i j)

theorem markerCompatible_transposeRotate (i j : Marker) :
    markerCompatible (transposeRotateMarker i) (transposeRotateMarker j) ↔
      markerCompatible i j :=
  (markerCompatible_transpose (rotateMarker i) (rotateMarker j)).trans
    (markerCompatible_rotate i j)

theorem markerCompatible_transposeRotate2 (i j : Marker) :
    markerCompatible (transposeRotateMarker2 i) (transposeRotateMarker2 j) ↔
      markerCompatible i j :=
  (markerCompatible_transpose (rotateMarker2 i) (rotateMarker2 j)).trans
    (markerCompatible_rotate2 i j)

theorem markerCompatible_transposeRotate3 (i j : Marker) :
    markerCompatible (transposeRotateMarker3 i) (transposeRotateMarker3 j) ↔
      markerCompatible i j :=
  (markerCompatible_transpose (rotateMarker3 i) (rotateMarker3 j)).trans
    (markerCompatible_rotate3 i j)

/- Each representative row needs only sixteen exact rational comparisons.
The three masks include their diagonal/self entries, as the original
strict-diameter relation does. -/
theorem markerCompatible_row0 (j : Marker) :
    markerCompatible 0 j ↔ (12547 : Nat).testBit j.val = true := by
  fin_cases j <;> norm_num [markerCompatible, marker, distSq, diameterLimit] <;> decide

theorem markerCompatible_row8 (j : Marker) :
    markerCompatible 8 j ↔ (16131 : Nat).testBit j.val = true := by
  fin_cases j <;> norm_num [markerCompatible, marker, distSq, diameterLimit] <;> decide

theorem markerCompatible_row12 (j : Marker) :
    markerCompatible 12 j ↔ (6595 : Nat).testBit j.val = true := by
  fin_cases j <;> norm_num [markerCompatible, marker, distSq, diameterLimit] <;> decide

/-- Each row is a canonical integer row evaluated at an isometric column.
This avoids recomputing rational squared distances during clique checking. -/
def fastCompatibility (i j : Marker) : Bool :=
  match i.val with
  | 0 => (12547 : Nat).testBit j.val
  | 1 => (12547 : Nat).testBit (transposeMarker j).val
  | 2 => (12547 : Nat).testBit (transposeRotateMarker3 j).val
  | 3 => (12547 : Nat).testBit (rotateMarker3 j).val
  | 4 => (12547 : Nat).testBit (rotateMarker2 j).val
  | 5 => (12547 : Nat).testBit (transposeRotateMarker2 j).val
  | 6 => (12547 : Nat).testBit (transposeRotateMarker j).val
  | 7 => (12547 : Nat).testBit (rotateMarker j).val
  | 8 => (16131 : Nat).testBit j.val
  | 9 => (16131 : Nat).testBit (rotateMarker3 j).val
  | 10 => (16131 : Nat).testBit (rotateMarker2 j).val
  | 11 => (16131 : Nat).testBit (rotateMarker j).val
  | 12 => (6595 : Nat).testBit j.val
  | 13 => (6595 : Nat).testBit (rotateMarker3 j).val
  | 14 => (6595 : Nat).testBit (rotateMarker2 j).val
  | _ => (6595 : Nat).testBit (rotateMarker j).val

def fastMarkerCompatible (i j : Marker) : Prop := fastCompatibility i j = true

instance : DecidableRel fastMarkerCompatible :=
  fun _ _ => inferInstanceAs (Decidable (_ = _))

theorem markerCompatible_iff_fast (i j : Marker) :
    markerCompatible i j ↔ fastMarkerCompatible i j := by
  fin_cases i
  · exact markerCompatible_row0 j
  · exact (markerCompatible_transpose 1 j).symm.trans
      (markerCompatible_row0 (transposeMarker j))
  · exact (markerCompatible_transposeRotate3 2 j).symm.trans
      (markerCompatible_row0 (transposeRotateMarker3 j))
  · exact (markerCompatible_rotate3 3 j).symm.trans
      (markerCompatible_row0 (rotateMarker3 j))
  · exact (markerCompatible_rotate2 4 j).symm.trans
      (markerCompatible_row0 (rotateMarker2 j))
  · exact (markerCompatible_transposeRotate2 5 j).symm.trans
      (markerCompatible_row0 (transposeRotateMarker2 j))
  · exact (markerCompatible_transposeRotate 6 j).symm.trans
      (markerCompatible_row0 (transposeRotateMarker j))
  · exact (markerCompatible_rotate 7 j).symm.trans
      (markerCompatible_row0 (rotateMarker j))
  · exact markerCompatible_row8 j
  · exact (markerCompatible_rotate3 9 j).symm.trans
      (markerCompatible_row8 (rotateMarker3 j))
  · exact (markerCompatible_rotate2 10 j).symm.trans
      (markerCompatible_row8 (rotateMarker2 j))
  · exact (markerCompatible_rotate 11 j).symm.trans
      (markerCompatible_row8 (rotateMarker j))
  · exact markerCompatible_row12 j
  · exact (markerCompatible_rotate3 13 j).symm.trans
      (markerCompatible_row12 (rotateMarker3 j))
  · exact (markerCompatible_rotate2 14 j).symm.trans
      (markerCompatible_row12 (rotateMarker2 j))
  · exact (markerCompatible_rotate 15 j).symm.trans
      (markerCompatible_row12 (rotateMarker j))

end S12
