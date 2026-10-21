---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: s-el-moumni
  display_name: Said El Moumni
  surname: El Moumni
  aliases:
  - El Moumni
  - S. El Moumni
  sources:
  - id: primary-byline
    archive_path: packing/resources/papers/el-moumni-1999-optimal-packings-unit-squares.pdf
    locator: The archived file is a volume scan. PDF page 287, printed page 281, gives the article title Optimal
      Packings of Unit Squares in a Square and byline S. EL MOUMNI. PDF page 296, printed page 290, repeats S. EL
      MOUMNI; neither page expands S. to a given name.
  - id: atlas-credit
    archive_path: packing/atlas/known-best/credit-attributions.json
    locator: name_aliases maps S. El Moumni to El Moumni; optimality.contributors lists El Moumni for el-moumni-1999-seven
      and el-moumni-1999-fifteen. The expanded Said spelling in the case records is not accepted as a profile alias
      without evidence.
  - id: survey-credit
    archive_path: packing/resources/papers/friedman-ds7-packing-unit-squares-in-squares.md
    url: https://erich-friedman.github.io/papers/squares/squares.html
    locator: The Introduction explicitly names Said El Moumni for s(7), s(8) and s(15), citing reference [12], which
      identifies Optimal Packings of Unit Squares in a Square (1999), the same article whose retained byline prints
      S. El Moumni. This supplies the expanded given name without changing the archived byline.
  provenance:
  - field: /display_name
    sources:
    - survey-credit
  - field: /surname
    sources:
    - primary-byline
    - atlas-credit
  - field: /aliases
    sources:
    - primary-byline
    - atlas-credit
  - field: /real_name
    sources:
    - survey-credit
  real_name: Said El Moumni
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
