/-
Copyright 2025 The Formal Conjectures Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-/
import Mathlib

/-!
# The square-packing definitions of `google-deepmind/formal-conjectures`

Copied from `FormalConjectures/Wikipedia/SquarePacking.lean` of
<https://github.com/google-deepmind/formal-conjectures> (Apache-2.0, see the header above), commit
`df3f12d7bd06feb3f71ae37abae0ca7cb798d9b1`, so that `Sqpack/SpecFC.lean` can state a bridge
without depending on that repository.  Changes: the definitions `Square`, `UnitSquare` and
`Packing` only (their text unchanged), in the namespace `FCSquarePacking` instead of
`SquarePacking` (which is this project's namespace), with the notation `ℝ²` (from their
`FormalConjecturesUtil`) defined locally, and without their `module`/`public` header lines.
-/

namespace FCSquarePacking

/-- The Euclidean plane (`FormalConjecturesUtil`'s notation). -/
scoped notation "ℝ²" => EuclideanSpace ℝ (Fin 2)

/--
A square of a particular side length as a subset of the Euclidean plane.
Not including border, so that squares that touch at the border are disjoint,
but a square internal to another shape is a subset of that shape.
-/
def Square (side : ℝ) : Set ℝ² :=
  {p : ℝ² | 0 < p 0 ∧ p 0 < side ∧ 0 < p 1 ∧ p 1 < side}

/--
The unit square as a subset of the Euclidean plane.
-/
def UnitSquare : Set ℝ² := Square 1

/--
A structure representing a packing of `n` isometric embeddings
of a set `s` inside a (presumably larger) set `S`.
-/
structure Packing (n : ℕ) (s : Set ℝ²) (S : Set ℝ²) where
  /-- The isometric equivalences
  that represent the transformations of the base shape to their locations in the packing. -/
  embeddings : Fin n → (ℝ² ≃ᵢ ℝ²)
  /-- The images of the embeddings are pairwise disjoint -/
  disjoint : Pairwise fun i j => Disjoint (embeddings i '' s) (embeddings j '' s)
  /-- The images of the embeddings are all inside the larger set `S` -/
  inside : ∀ i : Fin n, embeddings i '' s ⊆ S

end FCSquarePacking
