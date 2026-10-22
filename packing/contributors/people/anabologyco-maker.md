---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: anabologyco-maker
  display_name: anabologyco-maker
  links:
    - kind: github
      url: https://github.com/anabologyco-maker
      handle: anabologyco-maker
  sources:
    - id: source-intake
      archive_path: packing/resources/web/n17-github-certificates-2026/README.md
      locator: Chronology names anabologyco-maker; the anabologyco-maker/square17-lower-bound section records the source repository and retained release.
  provenance:
    - field: /display_name
      sources: [source-intake]
    - field: /links/0
      sources: [source-intake]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
