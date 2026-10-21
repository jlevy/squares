---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: thierry-gensane
  display_name: Thierry Gensane
  surname: Gensane
  real_name: Thierry Gensane
  aliases: [Gensane]
  sources:
    - id: paper-byline
      archive_path: packing/resources/papers/gensane-ryckelynck-2005-improved-dense-packings.raw.md
      url: https://doi.org/10.1007/s00454-004-1129-z
      locator: 'Opening byline, “Thierry Gensane and Philippe Ryckelynck”, LMPA, Université du Littoral, Calais; Discrete Comput Geom 34:97–109 (2005); the abstract and the cases n = 17, 18, 29 and 37.'
    - id: spheres-byline
      archive_path: packing/resources/papers/gensane-2004-dense-packings-equal-spheres-cube.raw.md
      locator: 'Opening byline, “Th. Gensane”, Laboratoire de Mathématiques Pures et Appliquées Joseph Liouville, Calais; Electron. J. Combin. 11 (2004), #R33; the abstract.'
    - id: picture-credits
      archive_path: packing/resources/web/known-best-packings/receipts/kingbird-2026-10-05-pictures.json
      locator: 'The n = 17 credits read from the catalogue SVG: “First high-precision analytic solution by Thierry Gensane and Philippe Ryckelynck before May 19, 2004.”'
    - id: catalogue-credits
      archive_path: packing/resources/web/kingbird-squares-in-squares-compared.md
      locator: 'Entries 18 and 29: “Alternative found by” and “Found by Thierry Gensane and Philippe Ryckelynck in April 2004, using a computer program they wrote.”'
    - id: archive-index
      archive_path: packing/resources/README.md
      locator: 'Papers table: the key [Gensane–Ryckelynck 2005], under which the frontier records cite the paper, with authors “T. Gensane, P. Ryckelynck”; and the key [Gensane 2004].'
  provenance:
    - field: /surname
      sources: [paper-byline, archive-index]
    - field: /display_name
      sources: [paper-byline, catalogue-credits]
    - field: /real_name
      sources: [paper-byline]
    - field: /aliases/0
      sources: [paper-byline, archive-index]
  bio_sources: [paper-byline, spheres-byline]
---
Thierry Gensane coauthored “Improved Dense Packings of Congruent Squares in a Square”
with Philippe Ryckelynck.
Their inflation algorithm produced improved square packings.
He also wrote about dense packings of equal spheres in a cube.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
