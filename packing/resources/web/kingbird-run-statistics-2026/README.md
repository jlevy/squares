# Kingbird Search Run Statistics for n = 51 and n = 55

First-party snapshots of run statistics published by David Ellsworth for his modified
version of Thomas Schadt's simulated-annealing program. Retrieved from the Kingbird
Squares in Squares catalogue on 31 August 2026.

- `square-51.stats.txt` covers nine data-gathering sessions on 31 January–1 February
  2026, using an NVIDIA RTX 3080 Ti and 65,536 search threads. Four of 3,004 categorized
  instances refined to the current record basin. The source estimates 4.917 hours per
  record-refinable hit under its tuned setup.
- `square-55.stats.txt` covers five data-gathering sessions on 4–5 February 2026 with
  the same GPU and thread count. The source estimates 40.604 minutes per hit that both
  crosses its screening threshold and refines to the current record.

These are setup-specific observations, not portable runtime predictions. They are useful
because they distinguish basin frequency from the later analytic refinement step and
put a measured cost on attempting head-on record search without the unpublished search
implementation and settings.

Source URLs:

- <https://kingbird.myphotos.cc/packing/square-51.stats.txt>
- <https://kingbird.myphotos.cc/packing/square-55.stats.txt>

SHA-256 hashes of the retained source bytes:

| File | SHA-256 |
| --- | --- |
| `square-51.stats.txt` | `7f88e364c940a65b104a39c86e808f15b1c7d6543534a28d6af832c67a37674a` |
| `square-55.stats.txt` | `cb48d77f0eb57c1c19e8025481124ee2ef89f41a70a52aaca82eeef3a832087b` |

Retained for private research use. Consult the author before redistribution.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
