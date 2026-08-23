---
type: is
id: is-01m0r3zv2hh2jj64rb8mhqbtre
title: Define basin identity for non-rigid optima, or the census counts family members
kind: bug
status: open
priority: 0
version: 7
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0pw86qg81x5qnjvzge42f4v
  - type: blocks
    target: is-01m0pw8698kc2bqm7d7fy0xydy
  - type: blocks
    target: is-01m0p4asxdaenzfkx53j4vh6qs
  - type: blocks
    target: is-01m0qxpb7634zbzt638d239jks
parent_id: is-01m0p49s01h862tq6wp0dd085c
created_at: 2026-08-23T20:11:30.757Z
updated_at: 2026-08-23T20:33:15.131Z
---
BLOCKS THE CENSUS. D-034. Found by reading the n = 5 golden, which is the campaign's first census cell.

THE EVIDENCE

Two rows in the n = 5 census are the same packing:

  side 2.767766952966372  geo 0373183838f6  con 851ea31d85f1  contacts 4  angles (2,3)
  side 2.767766952966370  geo 07860b128b38  con 851ea31d85f1  contacts 4  angles (2,3)

Same side to 12 decimals, same closed form (4 + 5*sqrt(2))/4, same contact certificate byte for byte, same angle signature, same contact count. The contact structures are isomorphic -- a star on square 4 in one, a star on square 1 in the other, with identical wall-touch multisets {0,1,2,2,2}. The atlas stores them as two basins because Atlas.add dedups on the tuple (geometric, contact) and requires BOTH to match.

WHY THEY DIFFER, AND WHY IT IS NOT A QUANTIZATION BUG

This is not the seam (D-031) and not float noise. The angle steps are identical in both -- [0, 0, 0, 785398, 785398]. The POSITIONS differ by 0.06 in x and 0.21 in y: real distance, not a straddled cell boundary.

Count the constraints. Four pair contacts plus seven wall touches is 11, against 5 squares x 3 DOF plus the side = 16. The configuration is NOT RIGID: five degrees of freedom remain, so the optimum at this side is a positive-dimensional FAMILY, not a point. Different quenches land on different members. The geometric key encodes coordinates the optimum does not determine, so it splits the family; the contact certificate, correctly, does not.

BasinKey.agrees_with already names this case `same-arrangement-different-metric`, and its own docstring says it "is usually one basin the quantizer split". Atlas.add never consults it.

WHY IT BLOCKS

distinct_basins would count family members. The discovery curve then never plateaus, so H-011's saturation criterion cannot be met and H-012's rarity ranking inherits the inflation -- the same failure shape as D-030 from a different cause, and flattering in the same two directions: a richer-looking landscape, and a record basin that looks rarer than it is.

THE DECISION, WHICH IS A DEFINITION AND NOT A CODE TWEAK

1. Dedup on (contact certificate, side within the 1e-11 tier floor). Cheap, and defensible: two packings with the same contact graph and the same side to solver precision are not distinct optima in any sense the campaign uses. Risk: the contact graph could merge two genuinely different optima that coincidentally share a side.
2. Canonicalize within the family -- pick a representative, e.g. lexicographically minimal under the family's own freedom. Correct, but needs the freedom characterised first, which is real work.
3. Report FAMILIES rather than basins, carrying the family's dimension as a field. Most honest about the mathematics; changes the deliverable's shape.

Do not pick one without measuring how often non-rigid optima occur. The related open question -- whether "basin" is well-posed at all where the optimum has slack -- is the same question, and n = 3 shows it too: three unit squares in a 2x2 box have slack, so the optimal set there is a continuum and the reported "3 basins" is a sample of it.

## Notes

2026-08-23, after writing the correction into the research doc: there is a much better route to the fix than the three options in the description, and it should be tried first.

A flat optimum is, in LP terms, a cell whose linear program has a NON-UNIQUE OPTIMAL FACE rather than an optimal vertex -- the objective is constant along a face of the feasible polytope. That is ordinary LP degeneracy. It is a property the solver can be asked about at the exact moment the quench already runs, so measuring flatness needs no new instrument and no new pass over the configuration.

That changes the shape of the work. Instead of choosing a basin definition and hoping it survives, MEASURE flatness first and let the data pick:

1. Have the quench report the dimension of the optimal face (equivalently: the surplus of degrees of freedom over active constraints, cross-checked against the LP's own degeneracy).
2. Carry it as a per-basin field in the atlas. A row then says whether it is a point or a family, and of what dimension.
3. Only then choose. If flat optima turn out to be rare at the n the campaign cares about, option 1 (dedup on contact certificate + side within the tier floor) is enough. If they are common, option 3 (report families with their dimension) is the honest deliverable and the census's headline number becomes "rigid optima, plus families" rather than a single count.

The cross-check is cheap and worth keeping even after the LP path works: n squares carry 3n degrees of freedom plus one for the side, and each pair contact and wall touch removes one. At n = 5 that gave 11 against 16 -- a five-dimensional family -- with no solver involvement at all.

Sequencing: this is the measurement that unblocks the decision, so it comes before multistart, not after. It is also the thing that makes think-siui's quantization-boundary work well-posed, because until flatness is measured there is no way to tell a boundary artifact from a genuine family member.

2026-08-23 20:35, MERGE HAZARD. The codex review branch independently allocated D-034 to a different defect ("a timed-out free sweep was reported as a convergence certificate"). Ours is the flat-basin one. One of the two renumbers on merge -- see think-o48b, which also records that their fix invalidates the convergence counts this branch committed, including the converged_frequency field added for exactly this kind of question. Regenerate the golden under their fix before quoting any convergence number from this branch.
