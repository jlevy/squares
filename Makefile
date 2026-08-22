# Markdown formatting for this repository.
#
# Flowmark is the ONLY formatter that owns Markdown here (per its project-setup
# guidance). Do not add Prettier, Biome, or dprint Markdown handling alongside it;
# two Markdown formatters churn each other's output and make hooks nondeterministic.

# Pinned to the latest Rust port of flowmark. The Rust build is the fast one
# (50x+ over the Python reference) and is what we standardise on.
#
# Pinned rather than floating on purpose: an unpinned `uvx --from flowmark-rs`
# re-resolves to whatever is newest on every single run, which is exactly the
# unpinned-zero-install-runner pattern that guidelines/supply-chain-hardening.md
# rule 6 warns against. Bumping this pin is a deliberate, reviewable act.
FLOWMARK := uvx --from flowmark-rs==0.3.2 flowmark

.PHONY: format format-check hooks-install

## Format all Markdown in the repository.
format:
	$(FLOWMARK) --auto .

## Report whether any Markdown would change, without writing. Not wired into CI
## on purpose: formatting drift should never break a build (see lefthook.yml).
format-check:
	$(FLOWMARK) --auto --check .

## Install the git hooks. Run once after cloning.
hooks-install:
	npx lefthook install
