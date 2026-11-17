# Packing 977 unit squares — computational reconstruction of a Göbel-type bound

**Contributor: Miguel Lara (independent).**

Proposed construction: 441 unit squares in a compact central 21×21 diamond rotated 45°, with 536 unrotated squares in four identical corner staircases (134 each). The exact construction gives:

\[s(977)\le 17+21/\sqrt{2}\approx31.8492424049<32.\]

The bound is **not a newly discovered record**: it follows from Göbel's classical construction and an L-border extension. This repository documents Miguel Lara's separate 977-square geometric layout and its numerical verification. Independent external checking of this specific coordinate file is still welcome.

## Historical context and attribution

This 0°/45° central-diamond and axis-aligned corner packing is part of the **classical square-packing tradition pioneered by Frits Göbel (1979)**. It should **not** be presented as a new record or a novel upper bound. The same side-length bound follows from Göbel's published family (as documented by Erich Friedman):

- With \((a,b)=(15,21)\), Göbel's formula yields \(2a^2+2a+b^2=921\) squares at side \(a+1+b/\sqrt2=16+21/\sqrt2\).
- Adding a standard outer L-shaped border yields \(921+(2\lfloor 16+21/\sqrt2\rfloor+1)=982\) squares at side \(17+21/\sqrt2\).
- Removing five squares gives a packing of 977 at the same side.

This reasoning gives the **same upper bound** as the construction here, although the coordinates and staircase arrangement need not be identical. **Credit to Frits Göbel for the underlying classical method; credit to Miguel Lara for this particular computational reconstruction, coordinate data, code, visualization and documentation**, developed with AI assistance. No originality or best-known-record claim is made.

**References:**
- F. Göbel, “Geometrical Packing and Covering Problems,” *Mathematical Centre Tracts* 106 (1979), pp. 179–199: https://ir.cwi.nl/pub/12685/12685D.pdf
- E. Friedman, “Packing Unit Squares in Squares: A Survey and New Results,” *Electronic Journal of Combinatorics*, Dynamic Survey DS7, Göbel construction and L-border discussion: https://www.combinatorics.org/files/Surveys/ds7/ds7v5-2009/ds7-2009.html

## Files

- `certificates/n977_certificate.md` — mathematical construction and geometric non-overlap argument.
- `certificates/n977_coordinates.csv` — 977 numeric square centers and angles (radians), using the relaxed side 31.85 and the container's lower-left corner as the coordinate origin.
- `verification/verify_977.py` — independent-library numerical check of the **published CSV**, not a re-generation of it.
- `verification/n977_verification.json` — recorded checker output (includes machine-specific timing).
- `visualization/n977.svg` — illustration of the **same** relaxed 31.85 CSV coordinates.
- `SUBMISSION.md` — suggested record-report text and transparent AI disclosure.

## Reproduce

```bash
python3 -m pip install 'shapely>=2.1,<3'
python3 verification/verify_977.py
```

The checker reads the committed CSV; it never overwrites it. It uses floating-point polygon tests with a documented area tolerance, not symbolic or interval arithmetic. The exact construction is discussed separately in the certificate.

## Attribution and limitations

Underlying Göbel-type packing method: Frits Göbel (1979). This specific layout, coordinates, numerical experimentation, code, and documentation: Miguel Lara, with OpenAI ChatGPT assistance. Independent third-party review of the specific construction remains outstanding.
