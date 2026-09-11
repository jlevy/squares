# The checkers’ probes

One JavaScript expression per file, loaded by `probes.probe("<name>")` and handed to
`page.evaluate`. See [`../probes.py`](../probes.py) for the contract; the short version
is that a probe takes its values as its **one argument** rather than having them
formatted into its text.

Names are grouped by what they are about, not by which checker uses them, so two
checkers asking the same question of the page ask it with the same file.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
